"""Focused co-located electric-Weyl N32/N64/N128 fixed-band requalification.

Development 015 repair. Native staggered electric-Weyl component fields are
reconstructed first, co-located to the scalar/vertex lattice second, and only
then treated as local matrices for eigensystem and operator comparisons.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from electric_weyl import (
    electric_weyl_conformal_sectors,
    electric_weyl_conformal_sectors_latfield2,
)
from fourier_resolution import active_overlap_modes, spectral_project_tensor_to_modes
from latfield2_native_operators import lattice_tensor_diagnostics, lattice_vector_diagnostics
from latfield_hdf5 import load_scalar_field, load_symmetric_tensor_field, load_vector_field
from modal_convergence import (
    directional_bound_from_tensor_error,
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_operator_error,
)
from temporal_derivatives import finite_difference_weights
from tensor_colocation import colocate_symmetric_tensor_to_vertices, tensor_colocation_diagnostics


FAMILIES = ("scalar", "vector", "tensor", "total")


def _rms(arr):
    x=np.asarray(arr,dtype=float)
    return float(np.sqrt(np.mean(x*x)))


def _tensor_frobenius_rms(arr):
    x=np.asarray(arr,dtype=float)
    return float(np.sqrt(np.mean(np.sum(x*x,axis=(-2,-1)))))


def _tensor_difference(reference,candidate):
    ref=np.asarray(reference,dtype=float)
    cand=np.asarray(candidate,dtype=float)
    if ref.shape != cand.shape or ref.shape[-2:] != (3,3):
        raise ValueError("tensor fields must match and end in (3,3)")
    ref_values,ref_vectors=ordered_eigensystem(ref)
    cand_values,cand_vectors=ordered_eigensystem(cand)
    ref_gaps=eigengaps(ref_values)
    cand_gaps=eigengaps(cand_values)
    error=tensor_operator_error(ref,cand)
    ref_norm=np.linalg.norm(ref,ord=2,axis=(-2,-1))
    align=eigenframe_absolute_alignment(ref_vectors,cand_vectors)
    diag=np.diagonal(align,axis1=-2,axis2=-1)
    direction=directional_bound_from_tensor_error(error,ref_values)
    return {
        "operator_error_quantiles":quantile_summary(error),
        "relative_operator_error_quantiles":quantile_summary(
            error/np.maximum(ref_norm,np.finfo(float).tiny)
        ),
        "eigenvalue_abs_error_quantiles_by_order":[
            quantile_summary(np.abs(cand_values[...,i]-ref_values[...,i]))
            for i in range(3)
        ],
        "eigengap_abs_error_quantiles_by_pair":[
            quantile_summary(np.abs(cand_gaps[...,i]-ref_gaps[...,i]))
            for i in range(2)
        ],
        "eigenframe_diagonal_alignment_quantiles_by_order":[
            quantile_summary(diag[...,i]) for i in range(3)
        ],
        "directional_error_over_reference_gap_quantiles_by_pair":[
            quantile_summary(direction[...,i]) for i in range(2)
        ],
    }


def _field_paths(root,index):
    tag=f"{index:03d}"
    out={}
    for token in ("phi","chi","B","hij"):
        matches=sorted(root.glob(f"*snap{tag}_{token}.h5"))
        if len(matches)!=1:
            raise ValueError(f"expected one snap{tag}_{token}.h5 in {root}, found {matches}")
        out[token]=matches[0]
    return out


def _weighted_sum(paths,indices,weights,loader):
    out=None
    for idx,w in zip(indices,weights):
        value=np.asarray(loader(paths[idx]),dtype=float)
        if out is None:
            out=np.zeros_like(value,dtype=float)
        out += float(w)*value
    if out is None:
        raise ValueError("empty weighted sum")
    return out


def _project(tensor,target_n,modes):
    return spectral_project_tensor_to_modes(tensor,target_n,modes,keep_zero=True)


def _direction_status(previous,latest):
    p=previous["relative_operator_error_quantiles"]
    q=latest["relative_operator_error_quantiles"]
    if q["median"] < p["median"] and q["q95"] < p["q95"]:
        return "CONVERGENT_DIRECTION"
    if q["median"] > p["median"] and q["q95"] > p["q95"]:
        return "WORSENING_DIRECTION"
    return "MIXED_DIRECTION"


def _member(grid,snapshot_dir,metadata_path,target_n,modes):
    metadata=json.loads(metadata_path.read_text())
    if int(metadata["grid"]) != int(grid):
        raise ValueError(f"metadata grid mismatch for N{grid}")
    snapshots=metadata["snapshots"]
    if len(snapshots)!=5:
        raise ValueError("exactly five snapshots required")
    tau=np.array([float(x["tau_over_boxsize"]) for x in snapshots])
    cycles=[int(x["cycle"]) for x in snapshots]
    if not np.all(np.diff(tau)>0.0):
        raise ValueError(f"N{grid} conformal times must increase")
    if len(set(cycles))!=5:
        raise ValueError(f"N{grid} snapshots must occupy distinct cycles")

    paths=[_field_paths(snapshot_dir,i) for i in range(5)]
    inner=[1,2,3]; outer=[0,2,4]; center=2
    b_in_w=finite_difference_weights(tau[inner],tau[center],1)
    b_out_w=finite_difference_weights(tau[outer],tau[center],1)
    h_in_w=finite_difference_weights(tau[inner],tau[center],2)
    h_out_w=finite_difference_weights(tau[outer],tau[center],2)

    bpaths=[x["B"] for x in paths]; hpaths=[x["hij"] for x in paths]
    b_in=_weighted_sum(bpaths,inner,b_in_w,load_vector_field)
    b_out=_weighted_sum(bpaths,outer,b_out_w,load_vector_field)
    h_in=_weighted_sum(hpaths,inner,h_in_w,load_symmetric_tensor_field)
    h_out=_weighted_sum(hpaths,outer,h_out_w,load_symmetric_tensor_field)
    phi=load_scalar_field(paths[center]["phi"])
    chi=load_scalar_field(paths[center]["chi"])
    h_center=load_symmetric_tensor_field(paths[center]["hij"])

    native_in_raw=electric_weyl_conformal_sectors_latfield2(
        phi,chi,b_in,h_center,h_in,1.0
    )
    native_out_raw=electric_weyl_conformal_sectors_latfield2(
        phi,chi,b_out,h_center,h_out,1.0
    )
    continuum_in=electric_weyl_conformal_sectors(phi,chi,b_in,h_center,h_in,1.0)
    continuum_out=electric_weyl_conformal_sectors(phi,chi,b_out,h_center,h_out,1.0)

    native_in={k:colocate_symmetric_tensor_to_vertices(native_in_raw[k]) for k in FAMILIES}
    native_out={k:colocate_symmetric_tensor_to_vertices(native_out_raw[k]) for k in FAMILIES}

    colocation={k:tensor_colocation_diagnostics(native_in_raw[k],native_in[k]) for k in FAMILIES}
    native_band={k:_project(native_in[k],target_n,modes) for k in FAMILIES}
    native_band_outer={k:_project(native_out[k],target_n,modes) for k in FAMILIES}
    continuum_band={k:_project(continuum_in[k],target_n,modes) for k in FAMILIES}
    continuum_band_outer={k:_project(continuum_out[k],target_n,modes) for k in FAMILIES}

    constraints=[]
    for i in range(5):
        constraints.append({
            "index":i,
            "B":lattice_vector_diagnostics(load_vector_field(paths[i]["B"]),1.0),
            "h":lattice_tensor_diagnostics(load_symmetric_tensor_field(paths[i]["hij"]),1.0),
        })

    temporal={k:_tensor_difference(native_band[k],native_band_outer[k]) for k in FAMILIES}
    split={k:_tensor_difference(native_band[k],continuum_band[k]) for k in FAMILIES}
    scalar_rms=_tensor_frobenius_rms(native_band["scalar"])
    sector_rms={k:_tensor_frobenius_rms(native_band[k]) for k in FAMILIES}

    return {
        "grid":grid,
        "central_actual_redshift":float(snapshots[center]["actual_redshift"]),
        "central_actual_scale_factor":float(snapshots[center]["actual_scale_factor"]),
        "central_tau_over_boxsize":float(tau[center]),
        "cycles":cycles,
        "temporal_weights":{
            "b_inner":b_in_w.tolist(),"b_outer":b_out_w.tolist(),
            "h_inner":h_in_w.tolist(),"h_outer":h_out_w.tolist(),
        },
        "temporal_derivative_rms":{
            "b_inner":_rms(b_in),"b_outer":_rms(b_out),
            "h_inner":_rms(h_in),"h_outer":_rms(h_out),
        },
        "native_constraints_logged":metadata.get("native_field_diagnostics"),
        "native_constraints_reproduced":constraints,
        "colocation_change":colocation,
        "common_band_sector_frobenius_rms":sector_rms,
        "common_band_sector_relative_to_scalar":{
            k:(sector_rms[k]/scalar_rms if scalar_rms>0 else None)
            for k in ("vector","tensor","total")
        },
        "temporal_inner_vs_outer":temporal,
        "native_vs_continuum":split,
        "_native":native_band,
        "_continuum":continuum_band,
        "_metadata":metadata,
    }


def build_report(members,target_n,boxsize_mpc_over_h):
    grids=[x[0] for x in members]
    if grids != [32,64,128]:
        raise ValueError("frozen ladder requires grids [32,64,128]")
    if target_n != 32:
        raise ValueError("frozen common target grid is N32")
    modes=active_overlap_modes(target_n)
    loaded=[_member(g,d,m,target_n,modes) for g,d,m in members]

    adjacent=[]
    for low,high in zip(loaded,loaded[1:]):
        row={"low_grid":low["grid"],"high_grid":high["grid"]}
        for family in FAMILIES:
            row[family]=_tensor_difference(low["_native"][family],high["_native"][family])
        adjacent.append(row)

    direction={}
    for family in FAMILIES:
        a=adjacent[0][family]; b=adjacent[1][family]
        direction[family]={
            "status":_direction_status(a,b),
            "n32_n64_median_relative_operator_error":a["relative_operator_error_quantiles"]["median"],
            "n64_n128_median_relative_operator_error":b["relative_operator_error_quantiles"]["median"],
            "n32_n64_q95_relative_operator_error":a["relative_operator_error_quantiles"]["q95"],
            "n64_n128_q95_relative_operator_error":b["relative_operator_error_quantiles"]["q95"],
            "n32_n64_eigenframe_median":[
                x["median"] for x in a["eigenframe_diagonal_alignment_quantiles_by_order"]
            ],
            "n64_n128_eigenframe_median":[
                x["median"] for x in b["eigenframe_diagonal_alignment_quantiles_by_order"]
            ],
            "n32_n64_eigenframe_q05":[
                x["q05"] for x in a["eigenframe_diagonal_alignment_quantiles_by_order"]
            ],
            "n64_n128_eigenframe_q05":[
                x["q05"] for x in b["eigenframe_diagonal_alignment_quantiles_by_order"]
            ],
        }

    split={}
    for family in FAMILIES:
        med=[m["native_vs_continuum"][family]["relative_operator_error_quantiles"]["median"] for m in loaded]
        latest=adjacent[1][family]["relative_operator_error_quantiles"]["median"]
        if med[0]>med[1]>med[2] and med[2] <= latest:
            status="COLLAPSES_ON_COMMON_BAND"
        elif med[2] > latest and not (med[0]>med[1]>med[2]):
            status="PERSISTS_ON_COMMON_BAND"
        else:
            status="NEED_MORE_INFO"
        split[family]={
            "status":status,
            "median_native_vs_continuum_by_grid":{str(m["grid"]):v for m,v in zip(loaded,med)},
            "native_n64_n128_median_resolution_error":latest,
        }

    total_prev=direction["total"]
    med_align_improve=all(
        b>=a for a,b in zip(total_prev["n32_n64_eigenframe_median"],total_prev["n64_n128_eigenframe_median"])
    )
    q05_align_improve=all(
        b>=a for a,b in zip(total_prev["n32_n64_eigenframe_q05"],total_prev["n64_n128_eigenframe_q05"])
    )
    if (
        direction["total"]["status"]=="CONVERGENT_DIRECTION"
        and direction["scalar"]["status"]=="CONVERGENT_DIRECTION"
        and med_align_improve and q05_align_improve
    ):
        candidate="COLOCATED_LOCAL_WEYL_QUALIFICATION_CANDIDATE"
    elif (
        direction["total"]["status"]=="WORSENING_DIRECTION"
        and direction["scalar"]["status"]=="WORSENING_DIRECTION"
    ):
        candidate="COLOCATED_LOCAL_WEYL_REFUSAL_DIRECTION_CANDIDATE"
    else:
        candidate="COLOCATED_LOCAL_WEYL_NEED_MORE_INFO_CANDIDATE"

    taus=[m["central_tau_over_boxsize"] for m in loaded]
    zs=[m["central_actual_redshift"] for m in loaded]
    summaries=[]
    for m in loaded:
        summaries.append({k:v for k,v in m.items() if not k.startswith("_")})

    return {
        "protocol":"P0-Q_COLOCATED_WEYL_FIXED_BAND_REQUALIFICATION_v0.1",
        "stage":"P0-Q",
        "scientific_claim_tested":False,
        "p1_exposed":False,
        "preregistration":"COLOCATED_WEYL_FIXED_BAND_REQUALIFICATION_PLAN_v0.1.md",
        "target_grid":target_n,
        "boxsize_mpc_over_h":boxsize_mpc_over_h,
        "common_band":{
            "definition":"0 < |n| < 15 and |n_i| < 15",
            "mode_count":len(modes),
            "order":"native staggered reconstruction -> vertex co-location -> eigensystem -> fixed-band projection",
        },
        "central_epoch_alignment":{
            "tau_by_grid":{str(m["grid"]):m["central_tau_over_boxsize"] for m in loaded},
            "redshift_by_grid":{str(m["grid"]):m["central_actual_redshift"] for m in loaded},
            "tau_spread":float(max(taus)-min(taus)),
            "redshift_spread":float(max(zs)-min(zs)),
        },
        "members":summaries,
        "adjacent_resolution_comparisons":adjacent,
        "resolution_direction":direction,
        "native_vs_continuum_classification":split,
        "eigenframe_refinement":{
            "median_all_orders_improve":med_align_improve,
            "q05_all_orders_improve":q05_align_improve,
        },
        "mechanical_outcome_candidate":candidate,
        "limitations":[
            "single early epoch and one development/qualification seed",
            "P0-Q representation requalification only",
            "co-location is interpolation/filtering and is not inverted",
            "magnetic Weyl tensor is not reconstructed",
        ],
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--target-grid",type=int,required=True)
    parser.add_argument("--boxsize-mpc-over-h",type=float,required=True)
    parser.add_argument("--member",action="append",nargs=3,metavar=("GRID","DIR","META"),required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    members=[(int(g),pathlib.Path(d),pathlib.Path(m)) for g,d,m in args.member]
    report=build_report(members,args.target_grid,args.boxsize_mpc_over_h)
    out=pathlib.Path(args.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"outcome_candidate":report["mechanical_outcome_candidate"],"output":str(out)},sort_keys=True))


if __name__=="__main__":
    main()
