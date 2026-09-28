"""Corrected fixed-band qualification for gevolution centered velocity shear."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from electric_weyl import symmetric_trace_free
from fourier_resolution import (
    active_overlap_modes,
    spectral_project_tensor_to_modes,
    spectral_project_vector_to_modes,
)
from gevolution_velocity_operators import (
    velocity_divergence_centered,
    velocity_kinematic_diagnostics,
    velocity_shear_centered,
    velocity_vorticity_centered,
)
from latfield2_native_operators import lattice_vector_symmetric_gradient
from latfield_hdf5 import load_vector_field
from modal_convergence import (
    directional_bound_from_tensor_error,
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_operator_error,
)
from weak_field_tensors import velocity_shear_tensor


def _tensor_difference(reference: np.ndarray, candidate: np.ndarray) -> dict:
    ref = np.asarray(reference, dtype=float)
    cand = np.asarray(candidate, dtype=float)
    if ref.shape != cand.shape or ref.shape[-2:] != (3, 3):
        raise ValueError("tensor fields must match and end in (3,3)")
    ref_values, ref_vectors = ordered_eigensystem(ref)
    cand_values, cand_vectors = ordered_eigensystem(cand)
    ref_gaps = eigengaps(ref_values)
    cand_gaps = eigengaps(cand_values)
    op_error = tensor_operator_error(ref, cand)
    ref_norm = np.linalg.norm(ref, ord=2, axis=(-2, -1))
    direction = directional_bound_from_tensor_error(op_error, ref_values)
    alignment = eigenframe_absolute_alignment(ref_vectors, cand_vectors)
    diagonal = np.diagonal(alignment, axis1=-2, axis2=-1)
    return {
        "operator_error_quantiles": quantile_summary(op_error),
        "relative_operator_error_quantiles": quantile_summary(
            op_error / np.maximum(ref_norm, np.finfo(float).tiny)
        ),
        "eigenvalue_abs_error_quantiles_by_order": [
            quantile_summary(np.abs(cand_values[..., i] - ref_values[..., i]))
            for i in range(3)
        ],
        "eigengap_abs_error_quantiles_by_pair": [
            quantile_summary(np.abs(cand_gaps[..., i] - ref_gaps[..., i]))
            for i in range(2)
        ],
        "eigenframe_diagonal_alignment_quantiles_by_order": [
            quantile_summary(diagonal[..., i]) for i in range(3)
        ],
        "directional_error_over_reference_gap_quantiles_by_pair": [
            quantile_summary(direction[..., i]) for i in range(2)
        ],
    }


def _tensor_frob_rms(tensor: np.ndarray) -> float:
    arr=np.asarray(tensor,dtype=float)
    return float(np.sqrt(np.mean(np.sum(arr*arr,axis=(-2,-1)))))


def _vector_rms(vector: np.ndarray) -> float:
    arr=np.asarray(vector,dtype=float)
    return float(np.sqrt(np.mean(np.sum(arr*arr,axis=0))))


def _load_member(
    grid: int,
    velocity_path: pathlib.Path,
    metadata_path: pathlib.Path,
    target_n: int,
    modes: list[tuple[int,int,int]],
) -> dict:
    velocity=load_vector_field(velocity_path)
    n=velocity.shape[1]
    if n != grid or velocity.shape != (3,n,n,n):
        raise ValueError(f"N{grid} velocity shape mismatch: {velocity.shape}")
    metadata=json.loads(metadata_path.read_text())
    if int(metadata["grid"]) != grid:
        raise ValueError("metadata grid mismatch")

    centered_shear, centered_theta = velocity_shear_centered(velocity, 1.0)
    centered_omega = velocity_vorticity_centered(velocity, 1.0)

    prior_staggered = symmetric_trace_free(
        lattice_vector_symmetric_gradient(velocity, 1.0)
    )
    continuum_shear, continuum_theta = velocity_shear_tensor(velocity, 1.0)

    centered_band=spectral_project_tensor_to_modes(
        centered_shear,target_n,modes,keep_zero=True
    )
    prior_band=spectral_project_tensor_to_modes(
        prior_staggered,target_n,modes,keep_zero=True
    )
    continuum_band=spectral_project_tensor_to_modes(
        continuum_shear,target_n,modes,keep_zero=True
    )
    omega_band=spectral_project_vector_to_modes(
        centered_omega,target_n,modes,keep_zero=True
    )

    return {
        "grid":grid,
        "metadata":metadata,
        "native_diagnostics":velocity_kinematic_diagnostics(velocity,1.0),
        "common_band_diagnostics":{
            "centered_shear_frobenius_rms":_tensor_frob_rms(centered_band),
            "centered_vorticity_vector_rms":_vector_rms(omega_band),
            "centered_vs_prior_staggered":_tensor_difference(centered_band,prior_band),
            "centered_vs_continuum":_tensor_difference(centered_band,continuum_band),
        },
        "centered_band":centered_band,
        "prior_band":prior_band,
        "continuum_band":continuum_band,
    }


def build_report(
    members:list[tuple[int,pathlib.Path,pathlib.Path]],
    target_n:int,
    boxsize_mpc_over_h:float,
) -> dict:
    if [m[0] for m in members] != [32,64,128]:
        raise ValueError("frozen correction requires grids [32,64,128]")
    if target_n != 32:
        raise ValueError("frozen target grid is N32")
    modes=active_overlap_modes(target_n)
    loaded=[_load_member(g,v,m,target_n,modes) for g,v,m in members]

    adjacent=[]
    for low,high in zip(loaded,loaded[1:]):
        adjacent.append({
            "low_grid":low["grid"],
            "high_grid":high["grid"],
            "centered_native_shear":_tensor_difference(
                low["centered_band"],high["centered_band"]
            ),
        })

    first=adjacent[0]["centered_native_shear"]
    second=adjacent[1]["centered_native_shear"]
    f=first["relative_operator_error_quantiles"]
    s=second["relative_operator_error_quantiles"]
    median_improves=s["median"] < f["median"]
    q95_improves=s["q95"] < f["q95"]

    align_first=first["eigenframe_diagonal_alignment_quantiles_by_order"]
    align_second=second["eigenframe_diagonal_alignment_quantiles_by_order"]
    eigenframe_median_nonworsening=all(
        align_second[i]["median"] >= align_first[i]["median"] for i in range(3)
    )
    dir_first=first["directional_error_over_reference_gap_quantiles_by_pair"]
    dir_second=second["directional_error_over_reference_gap_quantiles_by_pair"]
    direction_median_improves=all(
        dir_second[i]["median"] < dir_first[i]["median"] for i in range(2)
    )

    zs=[float(x["metadata"]["actual_redshift"]) for x in loaded]
    taus=[float(x["metadata"]["tau_over_boxsize"]) for x in loaded]
    epoch={
        "actual_redshift_by_grid":{str(x["grid"]):float(x["metadata"]["actual_redshift"]) for x in loaded},
        "tau_over_boxsize_by_grid":{str(x["grid"]):float(x["metadata"]["tau_over_boxsize"]) for x in loaded},
        "redshift_spread":float(max(zs)-min(zs)),
        "tau_spread":float(max(taus)-min(taus)),
    }

    if median_improves and q95_improves and eigenframe_median_nonworsening and direction_median_improves:
        candidate="CENTERED_VELOCITY_SHEAR_QUALIFICATION_CANDIDATE"
    elif (s["median"] > f["median"]) and (s["q95"] > f["q95"]):
        candidate="REFUSAL_DIRECTION_CANDIDATE"
    else:
        candidate="NEED_MORE_INFO_DIRECTION_CANDIDATE"

    summaries=[]
    for x in loaded:
        summaries.append({
            "grid":x["grid"],
            "metadata":x["metadata"],
            "native_diagnostics":x["native_diagnostics"],
            "common_band_diagnostics":x["common_band_diagnostics"],
        })

    return {
        "protocol":"P0-Q_NATIVE_CENTERED_VELOCITY_SHEAR_CORRECTION",
        "stage":"P0-Q",
        "preregistration":"NATIVE_CENTERED_VELOCITY_SHEAR_CORRECTION_PREREG.md",
        "scientific_claim_tested":False,
        "scientific_thresholds_frozen":False,
        "boxsize_mpc_over_h":float(boxsize_mpc_over_h),
        "target_grid":target_n,
        "common_band":{
            "definition":"0 < |n| < 15 and |n_i| < 15",
            "mode_count":len(modes),
            "order_of_operations":"centered-native shear first; common-band projection second",
        },
        "epoch_alignment":epoch,
        "members":summaries,
        "adjacent_resolution_comparisons":adjacent,
        "direction_checks":{
            "median_relative_operator_error_improves":median_improves,
            "q95_relative_operator_error_improves":q95_improves,
            "eigenframe_medians_nonworsening":eigenframe_median_nonworsening,
            "directional_error_medians_improve":direction_median_improves,
        },
        "mechanical_outcome_candidate":candidate,
        "limitations":[
            "representation correction only; no P1 claim",
            "single early epoch and one development seed",
            "velocity field is a coarse-grained mass-weighted gevolution field",
            "late-time multistream validity remains an APQ development question",
        ],
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--target-grid",type=int,required=True)
    p.add_argument("--boxsize-mpc-over-h",type=float,required=True)
    p.add_argument("--member",action="append",nargs=3,metavar=("GRID","V","META"),required=True)
    p.add_argument("--output",required=True)
    a=p.parse_args()
    members=[(int(g),pathlib.Path(v),pathlib.Path(m)) for g,v,m in a.member]
    report=build_report(members,a.target_grid,a.boxsize_mpc_over_h)
    out=pathlib.Path(a.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"outcome":report["mechanical_outcome_candidate"],"output":str(out)}))


if __name__=="__main__":
    main()
