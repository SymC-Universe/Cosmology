"""Post-result P0-D material-patch scale map for Cosmic Stability Architecture.

This is explicitly exploratory after the frozen P0-Q result returned NEED_MORE_INFO
because the 16 Mpc/h sensitivity reversed the 4 and 8 Mpc/h directions.
It cannot activate P1 or select a favorable scale.
"""
from __future__ import annotations
import argparse, json, pathlib, sys
import numpy as np

HERE=pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

from run_late_time_material_relational_development import (
    EpochFiles, band_l_modes, _snapshot_paths, _epoch_state, _evaluate_scale
)
from gevolution_particle_lineage import load_particle_snapshot
from material_patch import reference_patch_membership

PGRIDS=(2,4,8,16,32)

def summarize(report: dict, counts: np.ndarray, boxsize: float) -> dict:
    diags=report["b1_fold_diagnostics"]
    rank_def=[d for d in diags if d["rank"] < d["columns_with_intercept"]]
    foldvals=[x["delta_rel"] for x in report["foldwise"] if x["delta_rel"] is not None and np.isfinite(x["delta_rel"])]
    delta=report["delta_rel"]
    labels=[]
    if rank_def:
        labels.append("NUMERICAL_IDENTIFIABILITY_LIMIT_AT_SCALE")
    if delta is None or not np.isfinite(delta):
        labels.append("RELATIONAL_EQUIVALENT_OR_WEAK_AT_SCALE")
    elif delta>0 and report["sse_b1"] < report["sse_b0"] and report["sse_b1"] < report["sse_persistence"]:
        labels.append("RELATIONAL_ADDS_AT_SCALE")
    elif delta<0 and report["sse_b1"] > report["sse_b0"] and report["sse_b1"] > report["sse_persistence"]:
        labels.append("RELATIONAL_SUBTRACTS_AT_SCALE")
    else:
        labels.append("RELATIONAL_EQUIVALENT_OR_WEAK_AT_SCALE")
    return {
        "patch_grid":report["patch_grid"],
        "patch_side_mpc_over_h":boxsize/report["patch_grid"],
        "valid_patch_count":report["valid_patch_count"],
        "refused_patch_count":report["refused_patch_count"],
        "particle_count_mean":float(np.mean(counts)),
        "particle_count_min":int(np.min(counts)),
        "particle_count_max":int(np.max(counts)),
        "sse_persistence":report["sse_persistence"],
        "sse_b0":report["sse_b0"],
        "sse_b1":report["sse_b1"],
        "delta_rel":delta,
        "positive_fold_count":int(sum(x>0 for x in foldvals)),
        "negative_fold_count":int(sum(x<0 for x in foldvals)),
        "zero_fold_count":int(sum(x==0 for x in foldvals)),
        "finite_fold_count":len(foldvals),
        "b0_fold_diagnostics":report["b0_fold_diagnostics"],
        "b1_fold_diagnostics":report["b1_fold_diagnostics"],
        "b1_rank_deficient_fold_count":len(rank_def),
        "labels":labels,
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--snapshot-dir",required=True)
    ap.add_argument("--metadata",required=True)
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    root=pathlib.Path(args.snapshot_dir)
    meta=json.loads(pathlib.Path(args.metadata).read_text())
    if int(meta["grid"])!=64 or int(meta["seed"])!=424242:
        raise ValueError("scale map requires frozen N64 seed 424242 development member")
    modes=band_l_modes(64)
    epochs=[
        EpochFiles("z2",2,(0,1,2,3,4)),
        EpochFiles("z1",7,(5,6,7,8,9)),
        EpochFiles("z0p5",12,(10,11,12,13,14)),
    ]
    ref=load_particle_snapshot(_snapshot_paths(root,2)["cdm"])
    memberships={
        p:reference_patch_membership(ref["ID"],ref["position"],(p,p,p))
        for p in PGRIDS
    }
    states={
        e.name:_epoch_state(root,meta,e,modes,ref["ID"],memberships)
        for e in epochs
    }
    scales={}
    for p in PGRIDS:
        entry={"patch_grid":p,"patch_side_mpc_over_h":64.0/p}
        try:
            r1=_evaluate_scale(states["z2"],states["z1"],p,run_shift_null=False)
            r05=_evaluate_scale(states["z2"],states["z0p5"],p,run_shift_null=False)
            counts=np.asarray(states["z2"]["patch_scales"][str(p)]["count"])
            entry["z2_to_z1"]=summarize(r1,counts,64.0)
            entry["z2_to_z0p5"]=summarize(r05,counts,64.0)
            entry["status"]="MAPPED"
        except Exception as e:
            entry["status"]="REPRESENTATION_REFUSED_AT_SCALE"
            entry["exception_type"]=type(e).__name__
            entry["exception"]=str(e)
        scales[str(p)]=entry
    mapped=sum(v["status"]=="MAPPED" for v in scales.values())
    disposition="SCALE_MAP_COMPLETE" if mapped==len(PGRIDS) else ("SCALE_MAP_PARTIAL_WITH_LIMITS" if mapped else "SCALE_MAP_INVALID")
    out={
        "protocol":"P0-D_LATE_TIME_MATERIAL_SCALE_MAP",
        "scientific_stage":"POST_RESULT_P0D_EXPLORATION",
        "p1_evidence":False,
        "seed":424242,
        "grid":64,
        "boxsize_mpc_over_h":64.0,
        "band_l":{"definition":"0 < |n| < 4","mode_count":len(modes)},
        "patch_grids":list(PGRIDS),
        "scales":scales,
        "disposition":disposition,
        "interpretation_firewall":[
            "do not choose a best scale from this map",
            "do not infer a physical transition threshold from five points",
            "do not treat same-seed scale mapping as replication",
            "P1 remains closed"
        ]
    }
    path=pathlib.Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    compact={k:{
        "status":v["status"],
        "patch_side_mpc_over_h":v["patch_side_mpc_over_h"],
        "z2_to_z1_delta_rel":v.get("z2_to_z1",{}).get("delta_rel"),
        "z2_to_z1_labels":v.get("z2_to_z1",{}).get("labels"),
        "z2_to_z0p5_delta_rel":v.get("z2_to_z0p5",{}).get("delta_rel"),
        "z2_to_z0p5_labels":v.get("z2_to_z0p5",{}).get("labels")
    } for k,v in scales.items()}
    print(json.dumps({"disposition":disposition,"scales":compact},sort_keys=True))

if __name__=="__main__":
    main()
