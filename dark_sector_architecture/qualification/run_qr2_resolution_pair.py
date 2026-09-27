"""Q-R2 paired simulation-resolution qualification.

This script assumes two gevolution runs with the same box, cosmology, seed,
template family, and output epoch, but different Ngrid. It first measures
Fourier phase compatibility on modes actively initialized by the low grid.
It then spectrally restricts the high-grid phi and velocity fields to the
low-grid Fourier support and applies the same low-grid extraction operator to
both fields.

No scientific pass/fail threshold is imposed.
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

from fourier_resolution import (
    phase_overlap_report,
    spectral_restrict_to_grid,
    spectral_restrict_vector_to_grid,
)
from latfield_hdf5 import load_scalar_field, load_vector_field
from modal_convergence import (
    directional_bound_from_tensor_error,
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_operator_error,
)
from weak_field_tensors import velocity_shear_tensor, weak_field_tidal_tensor


def _field_difference(reference: np.ndarray, candidate: np.ndarray) -> dict:
    ref = np.asarray(reference, dtype=float)
    cand = np.asarray(candidate, dtype=float)
    if ref.shape != cand.shape:
        raise ValueError("field shapes do not match")
    diff = cand - ref
    abs_diff = np.abs(diff)
    ref_abs = np.abs(ref)
    tiny = np.finfo(float).tiny
    return {
        "absolute_error_quantiles": quantile_summary(abs_diff),
        "reference_absolute_quantiles": quantile_summary(ref_abs),
        "relative_error_to_global_reference_rms_quantiles": quantile_summary(
            abs_diff / max(float(np.sqrt(np.mean(ref * ref))), tiny)
        ),
        "rms_error": float(np.sqrt(np.mean(diff * diff))),
        "reference_rms": float(np.sqrt(np.mean(ref * ref))),
        "pearson_correlation": (
            float(np.corrcoef(ref.reshape(-1), cand.reshape(-1))[0, 1])
            if np.std(ref) > 0.0 and np.std(cand) > 0.0
            else None
        ),
    }


def _tensor_difference(reference: np.ndarray, candidate: np.ndarray) -> dict:
    ref = np.asarray(reference, dtype=float)
    cand = np.asarray(candidate, dtype=float)
    if ref.shape != cand.shape or ref.shape[-2:] != (3, 3):
        raise ValueError("tensor fields must match and end in (3,3)")

    ref_values, ref_vectors = ordered_eigensystem(ref)
    cand_values, cand_vectors = ordered_eigensystem(cand)
    ref_gaps = eigengaps(ref_values)
    cand_gaps = eigengaps(cand_values)
    operator_error = tensor_operator_error(ref, cand)
    dir_bound = directional_bound_from_tensor_error(operator_error, ref_values)

    alignment = eigenframe_absolute_alignment(ref_vectors, cand_vectors)
    diag_alignment = np.diagonal(alignment, axis1=-2, axis2=-1)

    ref_norm = np.linalg.norm(ref, ord=2, axis=(-2, -1))
    tiny = np.finfo(float).tiny

    return {
        "operator_error_quantiles": quantile_summary(operator_error),
        "relative_operator_error_quantiles": quantile_summary(
            operator_error / np.maximum(ref_norm, tiny)
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
            quantile_summary(diag_alignment[..., i]) for i in range(3)
        ],
        "directional_error_over_reference_gap_quantiles_by_pair": [
            quantile_summary(dir_bound[..., i]) for i in range(2)
        ],
        "reference_exact_zero_gap_counts_by_pair": [
            int(np.count_nonzero(ref_gaps[..., i] == 0.0)) for i in range(2)
        ],
    }


def build_report(
    low_phi_path: pathlib.Path,
    low_velocity_path: pathlib.Path,
    high_phi_path: pathlib.Path,
    high_velocity_path: pathlib.Path,
    boxsize: float,
) -> dict:
    low_phi = load_scalar_field(low_phi_path)
    low_velocity = load_vector_field(low_velocity_path)
    high_phi = load_scalar_field(high_phi_path)
    high_velocity = load_vector_field(high_velocity_path)

    low_n = low_phi.shape[0]
    high_n = high_phi.shape[0]
    if low_phi.shape != (low_n, low_n, low_n):
        raise ValueError("low phi grid must be cubic")
    if high_phi.shape != (high_n, high_n, high_n):
        raise ValueError("high phi grid must be cubic")
    if low_velocity.shape != (3, low_n, low_n, low_n):
        raise ValueError("low velocity shape mismatch")
    if high_velocity.shape != (3, high_n, high_n, high_n):
        raise ValueError("high velocity shape mismatch")
    if high_n <= low_n or high_n % low_n != 0:
        raise ValueError("high grid must be integer refinement of low grid")

    phase = {
        "phi": phase_overlap_report(low_phi, high_phi),
        "velocity_components": [
            phase_overlap_report(low_velocity[i], high_velocity[i])
            for i in range(3)
        ],
    }

    high_phi_restricted = spectral_restrict_to_grid(high_phi, low_n)
    high_velocity_restricted = spectral_restrict_vector_to_grid(
        high_velocity, low_n
    )

    low_tidal = weak_field_tidal_tensor(low_phi, boxsize)
    high_tidal_common = weak_field_tidal_tensor(high_phi_restricted, boxsize)

    low_shear, low_theta = velocity_shear_tensor(low_velocity, boxsize)
    high_shear_common, high_theta_common = velocity_shear_tensor(
        high_velocity_restricted, boxsize
    )

    return {
        "protocol": "Q-R2_PAIRED_SIMULATION_RESOLUTION",
        "stage": "P0-Q",
        "purpose": (
            "test same-seed overlapping-mode compatibility and simulation "
            "resolution sensitivity on a common low-grid Fourier support"
        ),
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "boxsize_mpc_over_h": float(boxsize),
        "low_grid": int(low_n),
        "high_grid": int(high_n),
        "refinement_ratio": int(high_n // low_n),
        "phase_overlap": phase,
        "common_grid_comparison": {
            "definition": (
                "spectrally restrict high-grid phi/velocity onto low-grid "
                "non-Nyquist Fourier support; reconstruct both low and restricted "
                "high tensors with the identical low-grid operator"
            ),
            "phi": _field_difference(low_phi, high_phi_restricted),
            "velocity_components": [
                _field_difference(
                    low_velocity[i], high_velocity_restricted[i]
                )
                for i in range(3)
            ],
            "tidal": _tensor_difference(low_tidal, high_tidal_common),
            "shear": _tensor_difference(low_shear, high_shear_common),
            "theta": _field_difference(low_theta, high_theta_common),
        },
        "limitations": [
            "development pair only; no P1 claim",
            "same-seed phase compatibility is measured rather than assumed",
            "common-grid comparison removes high-only Fourier modes before tensor reconstruction",
            "weak-field scalar tidal Hessian is not asserted to equal full electric Weyl curvature",
            "no universal resolution or directional threshold is inferred from this pair",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--low-phi", required=True)
    parser.add_argument("--low-velocity", required=True)
    parser.add_argument("--high-phi", required=True)
    parser.add_argument("--high-velocity", required=True)
    parser.add_argument("--boxsize", type=float, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(
        pathlib.Path(args.low_phi),
        pathlib.Path(args.low_velocity),
        pathlib.Path(args.high_phi),
        pathlib.Path(args.high_velocity),
        args.boxsize,
    )
    path = pathlib.Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "protocol": report["protocol"],
                "low_grid": report["low_grid"],
                "high_grid": report["high_grid"],
                "output": str(path),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
