"""Late-time coarse-grained velocity validity map.

Development-only P0-Q analysis under LATE_TIME_VELOCITY_VALIDITY_MAP_PLAN.md.
No E-sigma predictive outcome is constructed here.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

from fourier_resolution import (
    active_overlap_modes,
    spectral_project_scalar_to_modes,
    spectral_project_tensor_to_modes,
    spectral_project_vector_to_modes,
)
from gevolution_particle_lineage import lineage_report
from gevolution_velocity_operators import (
    velocity_divergence_centered,
    velocity_shear_centered,
    velocity_vorticity_centered,
)
from latfield_hdf5 import load_vector_field
from modal_convergence import (
    directional_bound_from_tensor_error,
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_operator_error,
)


def _tensor_rms(t):
    a=np.asarray(t,float)
    return float(np.sqrt(np.mean(np.sum(a*a,axis=(-2,-1)))))


def _vector_rms(v):
    a=np.asarray(v,float)
    return float(np.sqrt(np.mean(np.sum(a*a,axis=0))))


def _scalar_rms(x):
    a=np.asarray(x,float)
    return float(np.sqrt(np.mean(a*a)))


def _tensor_difference(ref,cand):
    rv,rvec=ordered_eigensystem(ref)
    cv,cvec=ordered_eigensystem(cand)
    rg=eigengaps(rv)
    cg=eigengaps(cv)
    err=tensor_operator_error(ref,cand)
    norm=np.linalg.norm(ref,ord=2,axis=(-2,-1))
    al=eigenframe_absolute_alignment(rvec,cvec)
    diag=np.diagonal(al,axis1=-2,axis2=-1)
    direction=directional_bound_from_tensor_error(err,rv)
    return {
        "operator_error_quantiles":quantile_summary(err),
        "relative_operator_error_quantiles":quantile_summary(
            err/np.maximum(norm,np.finfo(float).tiny)
        ),
        "eigenframe_diagonal_alignment_quantiles_by_order":[
            quantile_summary(diag[...,i]) for i in range(3)
        ],
        "eigengap_abs_error_quantiles_by_pair":[
            quantile_summary(np.abs(cg[...,i]-rg[...,i])) for i in range(2)
        ],
        "directional_error_over_reference_gap_quantiles_by_pair":[
            quantile_summary(direction[...,i]) for i in range(2)
        ],
    }


def _field_difference(ref,cand):
    a=np.asarray(ref,float)
    b=np.asarray(cand,float)
    diff=b-a
    ar=_scalar_rms(a)
    er=_scalar_rms(diff)
    return {
        "rms_error":er,
        "reference_rms":ar,
        "rms_error_over_reference_rms": er/ar if ar>0 else None,
        "pearson_correlation":(
            float(np.corrcoef(a.reshape(-1),b.reshape(-1))[0,1])
            if np.std(a)>0 and np.std(b)>0 else None
        ),
    }


def _vector_difference(ref,cand):
    a=np.asarray(ref,float)
    b=np.asarray(cand,float)
    diff=b-a
    ar=_vector_rms(a)
    er=_vector_rms(diff)
    return {
        "rms_error":er,
        "reference_rms":ar,
        "rms_error_over_reference_rms":er/ar if ar>0 else None,
        "pearson_correlation":(
            float(np.corrcoef(a.reshape(-1),b.reshape(-1))[0,1])
            if np.std(a)>0 and np.std(b)>0 else None
        ),
    }


def _band_modes():
    all_modes=active_overlap_modes(32)
    def radius(m):
        return math.sqrt(m[0]*m[0]+m[1]*m[1]+m[2]*m[2])
    return {
        "L":[m for m in all_modes if 0.0 < radius(m) < 4.0],
        "M":[m for m in all_modes if 4.0 <= radius(m) < 8.0],
        "H":[m for m in all_modes if 8.0 <= radius(m) < 15.0],
        "A":all_modes,
    }


def _find_snapshot_files(directory:pathlib.Path,index:int):
    tag=f"{index:03d}"
    v=sorted(directory.glob(f"*snap{tag}_v.h5"))
    p=sorted(directory.glob(f"*snap{tag}_cdm.h5"))
    if len(v)!=1 or len(p)!=1:
        raise ValueError(f"{directory}: snapshot {tag} files v={v} p={p}")
    return v[0],p[0]


def _member(grid:int,directory:pathlib.Path,metadata_path:pathlib.Path,bands):
    meta=json.loads(metadata_path.read_text())
    if int(meta["grid"])!=grid:
        raise ValueError("grid metadata mismatch")
    snaps=meta["snapshots"]
    if len(snaps)!=5:
        raise ValueError("frozen validity map requires five snapshots")
    products=[]
    particle_paths=[]
    raw={}
    for i,snap in enumerate(snaps):
        vpath,ppath=_find_snapshot_files(directory,i)
        particle_paths.append(ppath)
        vel=load_vector_field(vpath)
        if vel.shape != (3,grid,grid,grid):
            raise ValueError(f"N{grid} velocity shape {vel.shape}")
        shear,theta=velocity_shear_centered(vel,1.0)
        omega=velocity_vorticity_centered(vel,1.0)
        band_rows={}
        band_arrays={}
        for name,modes in bands.items():
            sh=spectral_project_tensor_to_modes(shear,32,modes,keep_zero=False)
            th=spectral_project_scalar_to_modes(theta,32,modes,keep_zero=False)
            om=spectral_project_vector_to_modes(omega,32,modes,keep_zero=False)
            shr=_tensor_rms(sh)
            omr=_vector_rms(om)
            band_rows[name]={
                "mode_count":len(modes),
                "shear_frobenius_rms":shr,
                "divergence_rms":_scalar_rms(th),
                "vorticity_vector_rms":omr,
                "vorticity_over_shear":omr/shr if shr>0 else None,
                "shear_max_trace_abs":float(np.max(np.abs(np.trace(sh,axis1=-2,axis2=-1)))),
            }
            band_arrays[name]={"shear":sh,"theta":th,"omega":om}
        products.append({
            "snapshot_index":i,
            "requested_redshift":float(snap["requested_redshift"]),
            "actual_redshift":float(snap["actual_redshift"]),
            "tau_over_boxsize":float(snap["tau_over_boxsize"]),
            "bands":band_rows,
        })
        raw[i]=band_arrays
    lineage=lineage_report(particle_paths)
    return {"grid":grid,"metadata":meta,"snapshots":products,"lineage":lineage,"raw":raw}


def build_report(members,target_grid=32):
    if [x[0] for x in members] != [32,64]:
        raise ValueError("frozen map requires N32 and N64")
    if target_grid != 32:
        raise ValueError("frozen comparison grid is N32")
    bands=_band_modes()
    loaded=[_member(g,d,m,bands) for g,d,m in members]
    low,high=loaded
    comparisons=[]
    for i in range(5):
        row={
            "snapshot_index":i,
            "requested_redshift":low["snapshots"][i]["requested_redshift"],
            "actual_redshift_n32":low["snapshots"][i]["actual_redshift"],
            "actual_redshift_n64":high["snapshots"][i]["actual_redshift"],
            "redshift_difference":abs(low["snapshots"][i]["actual_redshift"]-high["snapshots"][i]["actual_redshift"]),
            "bands":{},
        }
        for name in bands:
            a=low["raw"][i][name]
            b=high["raw"][i][name]
            row["bands"][name]={
                "shear":_tensor_difference(a["shear"],b["shear"]),
                "divergence":_field_difference(a["theta"],b["theta"]),
                "vorticity":_vector_difference(a["omega"],b["omega"]),
            }
        comparisons.append(row)
    summaries=[]
    for x in loaded:
        summaries.append({
            "grid":x["grid"],
            "metadata":x["metadata"],
            "snapshots":x["snapshots"],
            "lineage":x["lineage"],
        })
    finite=True
    for m in summaries:
        if not m["lineage"]["lineage_qualified"]:
            finite=False
        for s in m["snapshots"]:
            for b in s["bands"].values():
                vals=[b["shear_frobenius_rms"],b["divergence_rms"],b["vorticity_vector_rms"]]
                if not all(np.isfinite(v) for v in vals):
                    finite=False
    outcome="VALIDITY_MAP_COMPLETE" if finite else "NEED_MORE_INFO"
    return {
        "protocol":"P0-Q_LATE_TIME_COARSE_GRAINED_VELOCITY_VALIDITY_MAP",
        "stage":"P0-Q",
        "scientific_claim_tested":False,
        "p1_evidence_used":False,
        "development_seed":424242,
        "target_grid":32,
        "bands":{k:{"mode_count":len(v)} for k,v in bands.items()},
        "members":summaries,
        "n32_vs_n64":comparisons,
        "outcome":outcome,
        "limitations":[
            "vorticity is a multistream-sensitive coarse-grained diagnostic, not a direct shell-crossing count",
            "N32/N64 comparison is a development map, not a final convergence proof",
            "no E-sigma predictive outcome is computed",
            "no vorticity acceptance threshold is frozen",
        ],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--member",action="append",nargs=3,metavar=("GRID","DIR","META"),required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    members=[(int(g),pathlib.Path(d),pathlib.Path(m)) for g,d,m in a.member]
    r=build_report(members)
    out=pathlib.Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"outcome":r["outcome"],"output":str(out)}))


if __name__=="__main__":
    main()
