"""End-to-end gevolution modal pilot extraction.

This is P0-Q infrastructure/representation qualification only. It reads
LATfield2 HDF5 scalar potential and velocity fields, constructs weak-field
tidal and velocity-shear tensors, computes their eigensystems, and writes a
machine-readable summary plus a compact NPZ artifact.

No scientific modal threshold or P1 claim is adjudicated here.
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

from latfield_hdf5 import load_scalar_field, load_vector_field, summarize_hdf5_field
from weak_field_tensors import (
    tensor_symmetry_residual,
    tensor_trace_residual,
    velocity_shear_tensor,
    weak_field_tidal_tensor,
)


def batch_ordered_eigensystem(tensor_field: np.ndarray):
    tensor = np.asarray(tensor_field, dtype=float)
    if tensor.ndim < 2 or tensor.shape[-2:] != (3, 3):
        raise ValueError("tensor field must end in shape (3, 3)")
    values, vectors = np.linalg.eigh(tensor)
    values = values[..., ::-1]
    vectors = vectors[..., :, ::-1]
    gaps = np.stack(
        [
            np.abs(values[..., 0] - values[..., 1]),
            np.abs(values[..., 1] - values[..., 2]),
        ],
        axis=-1,
    )
    return values, vectors, gaps


def _quantiles(values: np.ndarray) -> dict[str, float]:
    finite = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(finite)):
        raise ValueError("non-finite values in quantile input")
    q = np.quantile(finite, [0.0, 0.05, 0.5, 0.95, 1.0])
    return {
        "min": float(q[0]),
        "q05": float(q[1]),
        "median": float(q[2]),
        "q95": float(q[3]),
        "max": float(q[4]),
    }


def extract(phi_path: pathlib.Path, velocity_path: pathlib.Path, boxsize: float):
    phi = load_scalar_field(phi_path)
    velocity = load_vector_field(velocity_path)

    if tuple(velocity.shape[1:]) != tuple(phi.shape):
        raise ValueError(
            f"phi grid {phi.shape} and velocity grid {velocity.shape[1:]} do not match"
        )

    tidal = weak_field_tidal_tensor(phi, boxsize)
    shear, theta = velocity_shear_tensor(velocity, boxsize)

    tidal_values, tidal_vectors, tidal_gaps = batch_ordered_eigensystem(tidal)
    shear_values, shear_vectors, shear_gaps = batch_ordered_eigensystem(shear)

    alignment = np.abs(
        np.matmul(
            np.swapaxes(shear_vectors, -1, -2),
            tidal_vectors,
        )
    )
    diagonal_alignment = np.diagonal(alignment, axis1=-2, axis2=-1)

    summary = {
        "stage": "P0-Q",
        "purpose": "gevolution weak-field modal extraction smoke test",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "full_weyl_equivalence_claimed": False,
        "boxsize_mpc_over_h": float(boxsize),
        "grid_shape": list(phi.shape),
        "phi_source": summarize_hdf5_field(phi_path),
        "velocity_source": summarize_hdf5_field(velocity_path),
        "tidal": {
            "symmetry_residual": tensor_symmetry_residual(tidal),
            "trace_residual": tensor_trace_residual(tidal),
            "eigenvalue_quantiles_by_order": [
                _quantiles(tidal_values[..., i]) for i in range(3)
            ],
            "eigengap_quantiles_by_pair": [
                _quantiles(tidal_gaps[..., i]) for i in range(2)
            ],
        },
        "shear": {
            "symmetry_residual": tensor_symmetry_residual(shear),
            "trace_residual": tensor_trace_residual(shear),
            "theta_quantiles": _quantiles(theta),
            "eigenvalue_quantiles_by_order": [
                _quantiles(shear_values[..., i]) for i in range(3)
            ],
            "eigengap_quantiles_by_pair": [
                _quantiles(shear_gaps[..., i]) for i in range(2)
            ],
        },
        "shear_tidal_alignment": {
            "diagonal_alignment_quantiles_by_order": [
                _quantiles(diagonal_alignment[..., i]) for i in range(3)
            ]
        },
        "limitations": [
            "weak-field tidal Hessian is not relabeled as full electric Weyl curvature",
            "vector B and tensor hij are presence-checked by the smoke workflow but not yet incorporated in this scalar-potential/velocity extraction",
            "no modal refusal threshold is applied in this infrastructure extraction",
        ],
    }

    arrays = {
        "phi": phi,
        "velocity": velocity,
        "tidal_tensor": tidal,
        "shear_tensor": shear,
        "theta": theta,
        "tidal_eigenvalues": tidal_values,
        "shear_eigenvalues": shear_values,
        "tidal_eigengaps": tidal_gaps,
        "shear_eigengaps": shear_gaps,
        "shear_tidal_alignment": alignment,
    }
    return summary, arrays


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phi", required=True)
    parser.add_argument("--velocity", required=True)
    parser.add_argument("--boxsize", type=float, required=True)
    parser.add_argument("--summary-output", required=True)
    parser.add_argument("--npz-output", required=True)
    args = parser.parse_args()

    summary, arrays = extract(
        pathlib.Path(args.phi),
        pathlib.Path(args.velocity),
        args.boxsize,
    )

    summary_path = pathlib.Path(args.summary_output)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")

    npz_path = pathlib.Path(args.npz_output)
    npz_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(npz_path, **arrays)

    print(
        json.dumps(
            {
                "summary_output": str(summary_path),
                "npz_output": str(npz_path),
                "grid_shape": summary["grid_shape"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
