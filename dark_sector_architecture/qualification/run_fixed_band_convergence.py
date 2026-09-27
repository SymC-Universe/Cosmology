"""Fixed-physical-band convergence for scalar-Weyl and shear tensors.

Unlike adjacent Q-R2 pair comparisons, this protocol freezes one target Fourier
band/grid and projects all higher-resolution simulations onto that same target.
It therefore tests convergence of the same physical modes instead of expanding
the compared bandwidth as numerical resolution increases.

No scientific acceptance threshold is imposed.
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
from weak_field_tensors import (
    scalar_weyl_shape_tensor,
    velocity_shear_tensor,
)


def _project_native_target_band(field: np.ndarray) -> np.ndarray:
    """Remove target-grid Nyquist planes without changing grid size."""
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 3 or len(set(arr.shape)) != 1:
        raise ValueError("field must be a cubic 3D scalar grid")
    n = arr.shape[0]
    if n % 2 != 0:
        raise ValueError("target grid must be even")
    spectrum = np.fft.fftn(arr)
    nyquist = n // 2
    spectrum[nyquist, :, :] = 0.0
    spectrum[:, nyquist, :] = 0.0
    spectrum[:, :, nyquist] = 0.0
    return np.fft.ifftn(spectrum).real


def _restrict_scalar(field: np.ndarray, target_n: int) -> np.ndarray:
    n = field.shape[0]
    if field.shape != (n, n, n):
        raise ValueError("scalar field must be cubic")
    if n == target_n:
        return _project_native_target_band(field)
    return spectral_restrict_to_grid(field, target_n)


def _restrict_vector(field: np.ndarray, target_n: int) -> np.ndarray:
    if field.ndim != 4 or field.shape[0] != 3:
        raise ValueError("vector field must have shape (3,N,N,N)")
    n = field.shape[1]
    if field.shape != (3, n, n, n):
        raise ValueError("vector field must be cubic")
    if n == target_n:
        return np.stack(
            [_project_native_target_band(field[i]) for i in range(3)],
            axis=0,
        )
    return spectral_restrict_vector_to_grid(field, target_n)


def _field_difference(reference: np.ndarray, candidate: np.ndarray) -> dict:
    ref = np.asarray(reference, dtype=float)
    cand = np.asarray(candidate, dtype=float)
    if ref.shape != cand.shape:
        raise ValueError("field shapes do not match")
    diff = cand - ref
    ref_rms = float(np.sqrt(np.mean(ref * ref)))
    err_rms = float(np.sqrt(np.mean(diff * diff)))
    return {
        "rms_error": err_rms,
        "reference_rms": ref_rms,
        "rms_error_over_reference_rms": (
            err_rms / ref_rms if ref_rms > 0.0 else None
        ),
        "absolute_error_quantiles": quantile_summary(np.abs(diff)),
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
    op_error = tensor_operator_error(ref, cand)
    ref_norm = np.linalg.norm(ref, ord=2, axis=(-2, -1))
    direction_bound = directional_bound_from_tensor_error(
        op_error, ref_values
    )
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
            quantile_summary(direction_bound[..., i]) for i in range(2)
        ],
    }


def _load_member(
    phi_path: pathlib.Path,
    chi_path: pathlib.Path,
    velocity_path: pathlib.Path,
    target_n: int,
    boxsize: float,
) -> dict:
    phi_native = load_scalar_field(phi_path)
    chi_native = load_scalar_field(chi_path)
    velocity_native = load_vector_field(velocity_path)

    if phi_native.shape != chi_native.shape:
        raise ValueError("phi and chi native grids do not match")
    n = phi_native.shape[0]
    if velocity_native.shape != (3, n, n, n):
        raise ValueError("velocity native grid does not match scalar grid")
    if n < target_n or n % target_n != 0:
        raise ValueError("member grid must equal or integer-refine target grid")

    phi = _restrict_scalar(phi_native, target_n)
    chi = _restrict_scalar(chi_native, target_n)
    velocity = _restrict_vector(velocity_native, target_n)

    weyl_potential = phi - 0.5 * chi
    scalar_weyl = scalar_weyl_shape_tensor(phi, chi, boxsize)
    shear, theta = velocity_shear_tensor(velocity, boxsize)

    return {
        "native_grid": int(n),
        "phi": phi,
        "chi": chi,
        "velocity": velocity,
        "weyl_potential": weyl_potential,
        "scalar_weyl": scalar_weyl,
        "shear": shear,
        "theta": theta,
    }


def build_report(
    members: list[tuple[pathlib.Path, pathlib.Path, pathlib.Path]],
    target_n: int,
    boxsize: float,
) -> dict:
    if len(members) < 3:
        raise ValueError("fixed-band convergence requires at least three members")

    loaded = [
        _load_member(phi, chi, vel, target_n, boxsize)
        for phi, chi, vel in members
    ]
    grids = [m["native_grid"] for m in loaded]
    if grids != sorted(grids) or len(set(grids)) != len(grids):
        raise ValueError("member grids must be unique and ascending")
    if grids[0] != target_n:
        raise ValueError("lowest member grid must equal target_n")

    comparisons = []
    for i in range(len(loaded) - 1):
        low = loaded[i]
        high = loaded[i + 1]
        comparisons.append(
            {
                "low_grid": low["native_grid"],
                "high_grid": high["native_grid"],
                "phi": _field_difference(low["phi"], high["phi"]),
                "chi_gev": _field_difference(low["chi"], high["chi"]),
                "weyl_potential": _field_difference(
                    low["weyl_potential"], high["weyl_potential"]
                ),
                "theta": _field_difference(low["theta"], high["theta"]),
                "scalar_weyl_shape": _tensor_difference(
                    low["scalar_weyl"], high["scalar_weyl"]
                ),
                "shear": _tensor_difference(low["shear"], high["shear"]),
            }
        )

    reference = loaded[0]
    to_reference = []
    for candidate in loaded[1:]:
        to_reference.append(
            {
                "reference_grid": reference["native_grid"],
                "candidate_grid": candidate["native_grid"],
                "phi": _field_difference(reference["phi"], candidate["phi"]),
                "weyl_potential": _field_difference(
                    reference["weyl_potential"],
                    candidate["weyl_potential"],
                ),
                "scalar_weyl_shape": _tensor_difference(
                    reference["scalar_weyl"], candidate["scalar_weyl"]
                ),
                "shear": _tensor_difference(
                    reference["shear"], candidate["shear"]
                ),
            }
        )

    ratio = {}
    if len(comparisons) >= 2:
        first = comparisons[-2]
        second = comparisons[-1]
        for family in ("scalar_weyl_shape", "shear"):
            e1 = first[family]["operator_error_quantiles"]["median"]
            e2 = second[family]["operator_error_quantiles"]["median"]
            ratio[family] = {
                "previous_adjacent_median_operator_error": e1,
                "latest_adjacent_median_operator_error": e2,
                "latest_over_previous": e2 / e1 if e1 > 0.0 else None,
            }
        for family in ("phi", "weyl_potential"):
            e1 = first[family]["rms_error"]
            e2 = second[family]["rms_error"]
            ratio[family] = {
                "previous_adjacent_rms_error": e1,
                "latest_adjacent_rms_error": e2,
                "latest_over_previous": e2 / e1 if e1 > 0.0 else None,
            }

    return {
        "protocol": "Q-R3_FIXED_PHYSICAL_BAND_CONVERGENCE",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "target_grid": int(target_n),
        "boxsize_mpc_over_h": float(boxsize),
        "native_grids": grids,
        "definition": (
            "all member fields are spectrally projected onto one fixed target "
            "Fourier grid before scalar-Weyl and velocity-shear reconstruction"
        ),
        "adjacent_comparisons": comparisons,
        "target_reference_comparisons": to_reference,
        "latest_vs_previous_error_ratio": ratio,
        "limitations": [
            "fixed-band development convergence only; no P1 claim",
            "full vector/tensor electric-Weyl sectors remain outside this scalar-Weyl test",
            "no universal convergence threshold or Richardson order is inferred automatically",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-grid", type=int, required=True)
    parser.add_argument("--boxsize", type=float, required=True)
    parser.add_argument("--member", action="append", nargs=3, metavar=("PHI", "CHI", "V"))
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if not args.member:
        raise SystemExit("at least three --member PHI CHI V triples are required")

    report = build_report(
        [
            (pathlib.Path(phi), pathlib.Path(chi), pathlib.Path(vel))
            for phi, chi, vel in args.member
        ],
        args.target_grid,
        args.boxsize,
    )
    path = pathlib.Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "protocol": report["protocol"],
                "target_grid": report["target_grid"],
                "native_grids": report["native_grids"],
                "output": str(path),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
