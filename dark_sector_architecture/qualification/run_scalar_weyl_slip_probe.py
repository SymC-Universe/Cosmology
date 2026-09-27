"""Measure the gevolution gravitational-slip correction to scalar Weyl shape.

P0-Q development only. Compares the legacy STF Hessian of Phi against the
first-order scalar Weyl/lensing-potential shape built from
Phi - chi_gev / 2.

No vector/tensor Weyl sectors are included and no scientific threshold is
imposed.
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

from latfield_hdf5 import load_scalar_field
from modal_convergence import (
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_operator_error,
)
from weak_field_tensors import (
    scalar_weyl_shape_tensor,
    weak_field_tidal_tensor,
)


def build_report(
    phi_path: pathlib.Path,
    chi_path: pathlib.Path,
    boxsize: float,
) -> dict:
    phi = load_scalar_field(phi_path)
    chi = load_scalar_field(chi_path)
    if phi.shape != chi.shape:
        raise ValueError("phi and chi grids do not match")

    effective = phi - 0.5 * chi
    legacy = weak_field_tidal_tensor(phi, boxsize)
    scalar_weyl = scalar_weyl_shape_tensor(phi, chi, boxsize)

    legacy_values, legacy_vectors = ordered_eigensystem(legacy)
    weyl_values, weyl_vectors = ordered_eigensystem(scalar_weyl)
    legacy_gaps = eigengaps(legacy_values)
    weyl_gaps = eigengaps(weyl_values)

    op_error = tensor_operator_error(legacy, scalar_weyl)
    legacy_norm = np.linalg.norm(legacy, ord=2, axis=(-2, -1))
    alignment = eigenframe_absolute_alignment(legacy_vectors, weyl_vectors)
    diagonal = np.diagonal(alignment, axis1=-2, axis2=-1)

    phi_rms = float(np.sqrt(np.mean(phi * phi)))
    chi_rms = float(np.sqrt(np.mean(chi * chi)))
    effective_rms = float(np.sqrt(np.mean(effective * effective)))

    return {
        "protocol": "P0-Q_SCALAR_WEYL_SLIP_PROBE",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "full_electric_weyl_claimed": False,
        "boxsize_mpc_over_h": float(boxsize),
        "grid_shape": list(phi.shape),
        "potential_statistics": {
            "phi_rms": phi_rms,
            "chi_gev_rms": chi_rms,
            "weyl_potential_rms": effective_rms,
            "chi_rms_over_phi_rms": (
                chi_rms / phi_rms if phi_rms > 0.0 else None
            ),
            "weyl_potential_minus_phi_rms": float(
                np.sqrt(np.mean((effective - phi) ** 2))
            ),
            "phi_effective_pearson_correlation": (
                float(np.corrcoef(phi.reshape(-1), effective.reshape(-1))[0, 1])
                if np.std(phi) > 0.0 and np.std(effective) > 0.0
                else None
            ),
        },
        "tensor_difference": {
            "operator_error_quantiles": quantile_summary(op_error),
            "relative_operator_error_quantiles": quantile_summary(
                op_error / np.maximum(legacy_norm, np.finfo(float).tiny)
            ),
            "eigenvalue_abs_error_quantiles_by_order": [
                quantile_summary(
                    np.abs(weyl_values[..., i] - legacy_values[..., i])
                )
                for i in range(3)
            ],
            "eigengap_abs_error_quantiles_by_pair": [
                quantile_summary(
                    np.abs(weyl_gaps[..., i] - legacy_gaps[..., i])
                )
                for i in range(2)
            ],
            "eigenframe_diagonal_alignment_quantiles_by_order": [
                quantile_summary(diagonal[..., i]) for i in range(3)
            ],
        },
        "limitations": [
            "scalar sector only",
            "physical a^-2 normalization omitted",
            "B_i and h_ij electric-Weyl contributions not included",
            "one early development epoch only",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phi", required=True)
    parser.add_argument("--chi", required=True)
    parser.add_argument("--boxsize", type=float, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(
        pathlib.Path(args.phi),
        pathlib.Path(args.chi),
        args.boxsize,
    )
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"protocol": report["protocol"], "output": str(output)}))


if __name__ == "__main__":
    main()
