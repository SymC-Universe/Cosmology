"""Q-R1 extraction-resolution qualification for modal tensor reconstruction.

Given a development NPZ containing a single fixed physical realization at a
fine grid, compare two paths at coarser representations:

A. reconstruct tensor on fine grid, then block-average the tensor;
B. block-average the underlying field, then reconstruct the tensor.

The difference measures extraction/coarse-graining sensitivity on the same
physical realization. It is not a simulation-resolution comparison and it does
not apply or infer a scientific pass/fail threshold.
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

from modal_convergence import (
    block_average,
    directional_bound_from_tensor_error,
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_frobenius_error,
    tensor_operator_error,
)
from weak_field_tensors import velocity_shear_tensor, weak_field_tidal_tensor


def _abs_error_quantiles(
    reference: np.ndarray, candidate: np.ndarray
) -> list[dict[str, float | int | None]]:
    if reference.shape != candidate.shape:
        raise ValueError("reference and candidate arrays must have matching shapes")
    return [
        quantile_summary(np.abs(candidate[..., i] - reference[..., i]))
        for i in range(reference.shape[-1])
    ]


def _alignment_quantiles(
    reference_vectors: np.ndarray, candidate_vectors: np.ndarray
) -> list[dict[str, float | int | None]]:
    alignment = eigenframe_absolute_alignment(reference_vectors, candidate_vectors)
    diagonal = np.diagonal(alignment, axis1=-2, axis2=-1)
    return [quantile_summary(diagonal[..., i]) for i in range(3)]


def _tensor_comparison(
    reference_tensor: np.ndarray, candidate_tensor: np.ndarray
) -> dict:
    reference_values, reference_vectors = ordered_eigensystem(reference_tensor)
    candidate_values, candidate_vectors = ordered_eigensystem(candidate_tensor)

    frobenius_error = tensor_frobenius_error(reference_tensor, candidate_tensor)
    operator_error = tensor_operator_error(reference_tensor, candidate_tensor)

    reference_gaps = eigengaps(reference_values)
    candidate_gaps = eigengaps(candidate_values)

    directional_bound = directional_bound_from_tensor_error(
        operator_error, reference_values
    )

    return {
        "reference_tensor_norm_quantiles": quantile_summary(
            np.linalg.norm(reference_tensor, axis=(-2, -1))
        ),
        "candidate_tensor_norm_quantiles": quantile_summary(
            np.linalg.norm(candidate_tensor, axis=(-2, -1))
        ),
        "frobenius_error_quantiles": quantile_summary(frobenius_error),
        "operator_error_quantiles": quantile_summary(operator_error),
        "relative_operator_error_quantiles": quantile_summary(
            operator_error
            / np.maximum(
                np.linalg.norm(reference_tensor, ord=2, axis=(-2, -1)),
                np.finfo(float).tiny,
            )
        ),
        "eigenvalue_abs_error_quantiles_by_order": _abs_error_quantiles(
            reference_values, candidate_values
        ),
        "eigengap_abs_error_quantiles_by_pair": _abs_error_quantiles(
            reference_gaps, candidate_gaps
        ),
        "eigenframe_diagonal_alignment_quantiles_by_order": _alignment_quantiles(
            reference_vectors, candidate_vectors
        ),
        "directional_error_over_reference_gap_quantiles_by_pair": [
            quantile_summary(directional_bound[..., i]) for i in range(2)
        ],
        "reference_exact_zero_gap_counts_by_pair": [
            int(np.count_nonzero(reference_gaps[..., i] == 0.0)) for i in range(2)
        ],
        "reference_cell_count": int(np.prod(reference_tensor.shape[:3])),
    }


def build_report(
    npz_path: pathlib.Path,
    boxsize: float,
    factors: tuple[int, ...] = (2, 4),
) -> dict:
    with np.load(npz_path) as data:
        required = {
            "phi",
            "velocity",
            "tidal_tensor",
            "shear_tensor",
            "theta",
        }
        missing = sorted(required.difference(data.files))
        if missing:
            raise ValueError(f"NPZ is missing required arrays: {missing}")

        phi = np.asarray(data["phi"], dtype=float)
        velocity = np.asarray(data["velocity"], dtype=float)
        tidal_fine = np.asarray(data["tidal_tensor"], dtype=float)
        shear_fine = np.asarray(data["shear_tensor"], dtype=float)
        theta_fine = np.asarray(data["theta"], dtype=float)

    if phi.ndim != 3:
        raise ValueError(f"phi must be 3D, got {phi.shape}")
    if velocity.shape != (3,) + phi.shape:
        raise ValueError(
            f"velocity must have shape (3,) + phi.shape, got {velocity.shape}"
        )
    if tidal_fine.shape != phi.shape + (3, 3):
        raise ValueError("tidal tensor shape does not match phi grid")
    if shear_fine.shape != phi.shape + (3, 3):
        raise ValueError("shear tensor shape does not match phi grid")
    if theta_fine.shape != phi.shape:
        raise ValueError("theta shape does not match phi grid")

    if not all(
        np.all(np.isfinite(arr))
        for arr in (phi, velocity, tidal_fine, shear_fine, theta_fine)
    ):
        raise ValueError("development arrays must all be finite")

    levels = []
    for factor in factors:
        factors3 = (factor, factor, factor)

        phi_coarse = block_average(phi, factors3)
        velocity_coarse = block_average(velocity, factors3)

        tidal_reference = block_average(tidal_fine, factors3)
        shear_reference = block_average(shear_fine, factors3)
        theta_reference = block_average(theta_fine, factors3)

        tidal_candidate = weak_field_tidal_tensor(phi_coarse, boxsize)
        shear_candidate, theta_candidate = velocity_shear_tensor(
            velocity_coarse, boxsize
        )

        levels.append(
            {
                "coarse_factor": int(factor),
                "coarse_grid_shape": list(phi_coarse.shape),
                "fine_cell_size_mpc_over_h": float(boxsize / phi.shape[0]),
                "coarse_cell_size_mpc_over_h": float(
                    boxsize / phi_coarse.shape[0]
                ),
                "tidal": _tensor_comparison(
                    tidal_reference, tidal_candidate
                ),
                "shear": _tensor_comparison(
                    shear_reference, shear_candidate
                ),
                "theta_abs_error_quantiles": quantile_summary(
                    np.abs(theta_candidate - theta_reference)
                ),
            }
        )

    return {
        "protocol": "Q-R1_MODAL_EXTRACTION_RESOLUTION",
        "stage": "P0-Q",
        "purpose": (
            "measure finite-grid extraction/coarse-graining sensitivity on one "
            "fixed real gevolution development realization"
        ),
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "simulation_resolution_tested": False,
        "input_npz": str(npz_path),
        "boxsize_mpc_over_h": float(boxsize),
        "fine_grid_shape": list(phi.shape),
        "comparison_definition": {
            "reference_path": "fine-grid tensor reconstruction then block average",
            "candidate_path": "block-average underlying field then reconstruct tensor",
            "directional_diagnostic": "local operator tensor error divided by reference adjacent eigengap",
        },
        "levels": levels,
        "limitations": [
            "development field is a single Ngrid=8 smoke realization",
            "Q-R1 measures extraction/coarse-graining sensitivity, not simulation convergence",
            "no acceptance threshold is inferred from this field",
            "weak-field scalar tidal Hessian is not asserted to equal full electric Weyl curvature",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-npz", required=True)
    parser.add_argument("--boxsize", type=float, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument(
        "--factors",
        default="2,4",
        help="comma-separated integer block factors; default: 2,4",
    )
    args = parser.parse_args()

    factors = tuple(int(v.strip()) for v in args.factors.split(",") if v.strip())
    if not factors:
        raise SystemExit("at least one coarse factor is required")

    report = build_report(
        pathlib.Path(args.input_npz),
        args.boxsize,
        factors=factors,
    )
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(
        json.dumps(
            {
                "protocol": report["protocol"],
                "levels": len(report["levels"]),
                "output": str(output),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
