"""Analyze a five-snapshot gevolution electric-Weyl temporal pilot.

P0-Q representation qualification only.

The workflow supplies five matched snapshots and a metadata JSON containing
the actual logged dimensionless conformal times tau/boxsize. Spatial
derivatives are therefore taken on a unit periodic box, so temporal and spatial
derivatives use the same dimensionless gevolution coordinate system.

The physical orthonormal electric-Weyl tensor in inverse comoving-length
squared units would additionally carry 1/(a^2 L^2), where L is the simulation
box length in the desired comoving length unit. The common positive factor does
not affect one-epoch eigenframes.
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
    tensor_divergence_periodic,
    vector_divergence_periodic,
)
from latfield2_native_operators import (
    lattice_tensor_diagnostics,
    lattice_vector_diagnostics,
)
from latfield_hdf5 import (
    load_scalar_field,
    load_symmetric_tensor_field,
    load_vector_field,
)
from modal_convergence import (
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_operator_error,
)
from temporal_derivatives import (
    nested_center_derivatives,
    relative_rms_difference,
)


def _rms(values: np.ndarray) -> float:
    arr = np.asarray(values, dtype=float)
    return float(np.sqrt(np.mean(arr * arr)))


def _tensor_frobenius_rms(tensor: np.ndarray) -> float:
    arr = np.asarray(tensor, dtype=float)
    return float(np.sqrt(np.mean(np.sum(arr * arr, axis=(-2, -1)))))


def _relative_tensor_operator_quantiles(
    reference: np.ndarray, candidate: np.ndarray
) -> dict:
    error = tensor_operator_error(reference, candidate)
    reference_norm = np.linalg.norm(reference, ord=2, axis=(-2, -1))
    relative = error / np.maximum(reference_norm, np.finfo(float).tiny)
    return {
        "absolute": quantile_summary(error),
        "relative_to_reference": quantile_summary(relative),
    }


def _modal_comparison(reference: np.ndarray, candidate: np.ndarray) -> dict:
    ref_values, ref_vectors = ordered_eigensystem(reference)
    cand_values, cand_vectors = ordered_eigensystem(candidate)

    ref_gaps = eigengaps(ref_values)
    op_error = tensor_operator_error(reference, candidate)
    alignment = eigenframe_absolute_alignment(ref_vectors, cand_vectors)
    diagonal = np.diagonal(alignment, axis1=-2, axis2=-1)

    with np.errstate(divide="ignore", invalid="ignore"):
        direction = op_error[..., None] / ref_gaps

    return {
        "tensor_error": _relative_tensor_operator_quantiles(reference, candidate),
        "eigenvalue_abs_error_quantiles_by_order": [
            quantile_summary(np.abs(cand_values[..., i] - ref_values[..., i]))
            for i in range(3)
        ],
        "eigenframe_diagonal_alignment_quantiles_by_order": [
            quantile_summary(diagonal[..., i]) for i in range(3)
        ],
        "directional_error_over_reference_gap_quantiles_by_pair": [
            quantile_summary(direction[..., i]) for i in range(2)
        ],
    }


def _field_files(snapshot_dir: pathlib.Path, index: int) -> dict[str, pathlib.Path]:
    tag = f"{index:03d}"
    result = {}
    for field in ("phi", "chi", "B", "hij"):
        matches = sorted(snapshot_dir.glob(f"*snap{tag}_{field}.h5"))
        if len(matches) != 1:
            raise ValueError(
                f"expected exactly one snap{tag}_{field}.h5 file, found {matches}"
            )
        result[field] = matches[0]
    return result


def build_report(
    snapshot_dir: pathlib.Path,
    metadata_path: pathlib.Path,
    boxsize_mpc_over_h: float,
) -> tuple[dict, dict[str, np.ndarray]]:
    metadata = json.loads(metadata_path.read_text())
    snapshots = metadata.get("snapshots")
    if not isinstance(snapshots, list) or len(snapshots) != 5:
        raise ValueError("metadata must contain exactly five snapshots")

    tau = np.array([float(item["tau_over_boxsize"]) for item in snapshots])
    actual_z = np.array([float(item["actual_redshift"]) for item in snapshots])
    requested_z = np.array([float(item["requested_redshift"]) for item in snapshots])
    cycles = [int(item["cycle"]) for item in snapshots]

    if not np.all(np.diff(tau) > 0.0):
        raise ValueError(f"actual conformal times are not strictly increasing: {tau}")
    if len(set(cycles)) != 5:
        raise ValueError(f"five snapshots did not land on distinct cycles: {cycles}")

    phi = []
    chi = []
    b = []
    h = []
    files = []
    for index in range(5):
        paths = _field_files(snapshot_dir, index)
        files.append({key: str(value) for key, value in paths.items()})
        phi.append(load_scalar_field(paths["phi"]))
        chi.append(load_scalar_field(paths["chi"]))
        b.append(load_vector_field(paths["B"]))
        h.append(load_symmetric_tensor_field(paths["hij"]))

    phi = np.stack(phi, axis=0)
    chi = np.stack(chi, axis=0)
    b = np.stack(b, axis=0)
    h = np.stack(h, axis=0)

    if len({tuple(item.shape) for item in phi}) != 1:
        raise ValueError("phi snapshot grids do not match")

    # gevolution evolution coordinates use x/L and tau/L. Use a unit box here
    # so every derivative entering E_conf is in inverse box-coordinate units.
    coordinate_boxsize = 1.0

    derivatives = nested_center_derivatives(b, h, tau)
    center = 2

    sectors_inner_continuum = electric_weyl_conformal_sectors(
        phi[center],
        chi[center],
        derivatives["b_prime_inner"],
        h[center],
        derivatives["h_second_inner"],
        coordinate_boxsize,
    )
    sectors_outer_continuum = electric_weyl_conformal_sectors(
        phi[center],
        chi[center],
        derivatives["b_prime_outer"],
        h[center],
        derivatives["h_second_outer"],
        coordinate_boxsize,
    )

    sectors_inner = electric_weyl_conformal_sectors_latfield2(
        phi[center],
        chi[center],
        derivatives["b_prime_inner"],
        h[center],
        derivatives["h_second_inner"],
        coordinate_boxsize,
    )
    sectors_outer = electric_weyl_conformal_sectors_latfield2(
        phi[center],
        chi[center],
        derivatives["b_prime_outer"],
        h[center],
        derivatives["h_second_outer"],
        coordinate_boxsize,
    )

    native_postprocessing = []
    for i in range(5):
        native_postprocessing.append(
            {
                "index": i,
                "B": lattice_vector_diagnostics(b[i], coordinate_boxsize),
                "h": lattice_tensor_diagnostics(h[i], coordinate_boxsize),
            }
        )

    native_logged = metadata.get("native_field_diagnostics")
    native_log_reproduction = None
    if native_logged is not None:
        if len(native_logged) != 5:
            raise ValueError("native_field_diagnostics must contain five entries")
        native_log_reproduction = []
        for i in range(5):
            logged = native_logged[i]
            post = native_postprocessing[i]
            native_log_reproduction.append(
                {
                    "index": i,
                    "B_divergence_abs_difference": abs(
                        post["B"]["max_abs_divergence"]
                        - float(logged["B_max_abs_divergence"])
                    ),
                    "h_divergence_abs_difference": abs(
                        post["h"]["max_divergence_norm"]
                        - float(logged["h_max_abs_divergence"])
                    ),
                    "h_trace_abs_difference": abs(
                        post["h"]["max_abs_trace"]
                        - float(logged["h_max_abs_trace"])
                    ),
                    "h_norm_abs_difference": abs(
                        post["h"]["max_frobenius_norm"]
                        - float(logged["h_max_norm"])
                    ),
                }
            )

    b_divergence = [
        vector_divergence_periodic(b[i], coordinate_boxsize)
        for i in range(5)
    ]
    h_divergence = [
        tensor_divergence_periodic(h[i], coordinate_boxsize)
        for i in range(5)
    ]
    h_trace = [
        np.trace(h[i], axis1=-2, axis2=-1)
        for i in range(5)
    ]
    h_symmetry = [
        h[i] - np.swapaxes(h[i], -1, -2)
        for i in range(5)
    ]

    central_a = 1.0 / (1.0 + actual_z[center])
    physical_factor = 1.0 / (
        central_a * central_a * float(boxsize_mpc_over_h) ** 2
    )

    sector_rms_inner = {
        key: _tensor_frobenius_rms(sectors_inner[key])
        for key in ("scalar", "vector", "tensor", "total")
    }
    sector_rms_outer = {
        key: _tensor_frobenius_rms(sectors_outer[key])
        for key in ("scalar", "vector", "tensor", "total")
    }

    scalar_rms = sector_rms_inner["scalar"]
    sector_relative_to_scalar = {
        key: (
            sector_rms_inner[key] / scalar_rms
            if scalar_rms > 0.0 else None
        )
        for key in ("vector", "tensor", "total")
    }

    continuum_sector_rms_inner = {
        key: _tensor_frobenius_rms(sectors_inner_continuum[key])
        for key in ("scalar", "vector", "tensor", "total")
    }
    continuum_sector_rms_outer = {
        key: _tensor_frobenius_rms(sectors_outer_continuum[key])
        for key in ("scalar", "vector", "tensor", "total")
    }

    report = {
        "protocol": "P0-Q_ELECTRIC_WEYL_TEMPORAL_PILOT",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "full_electric_weyl_p1_claimed": False,
        "representation": {
            "project_riemann_convention": (
                "R^rho_{sigma mu nu}=d_mu Gamma^rho_{nu sigma}"
                "-d_nu Gamma^rho_{mu sigma}+..."
            ),
            "coordinate_system": (
                "dimensionless gevolution x/L and tau/L for derivative combination"
            ),
            "coordinate_boxsize": coordinate_boxsize,
            "boxsize_mpc_over_h": float(boxsize_mpc_over_h),
            "central_scale_factor": central_a,
            "box_coordinate_to_physical_E_factor_h2_per_Mpc2": physical_factor,
            "hij_source": (
                "dynamically evolved hijFT inverse-transformed by qualification-only "
                "snapshot patch compiled with TENSOR_EVOLUTION"
            ),
            "primary_spatial_operator": "LATFIELD2_GEVOLUTION_NATIVE",
            "continuum_spatial_operator_role": "COMPARATOR_ONLY",
        },
        "snapshots": [
            {
                **snapshots[i],
                "files": files[i],
            }
            for i in range(5)
        ],
        "requested_redshifts": requested_z.tolist(),
        "actual_redshifts": actual_z.tolist(),
        "actual_tau_over_boxsize": tau.tolist(),
        "cycles": cycles,
        "temporal_derivatives": {
            "b_inner_weights": derivatives["b_inner_weights"].tolist(),
            "b_outer_weights": derivatives["b_outer_weights"].tolist(),
            "h_inner_weights": derivatives["h_inner_weights"].tolist(),
            "h_outer_weights": derivatives["h_outer_weights"].tolist(),
            "b_prime_inner_outer_relative_rms_difference": (
                relative_rms_difference(
                    derivatives["b_prime_inner"],
                    derivatives["b_prime_outer"],
                    reference=derivatives["b_prime_inner"],
                )
            ),
            "h_second_inner_outer_relative_rms_difference": (
                relative_rms_difference(
                    derivatives["h_second_inner"],
                    derivatives["h_second_outer"],
                    reference=derivatives["h_second_inner"],
                )
            ),
            "b_prime_inner_rms": _rms(derivatives["b_prime_inner"]),
            "b_prime_outer_rms": _rms(derivatives["b_prime_outer"]),
            "h_second_inner_rms": _rms(derivatives["h_second_inner"]),
            "h_second_outer_rms": _rms(derivatives["h_second_outer"]),
        },
        "constraint_diagnostics": {
            "qualification_source": (
                "gevolution native LATfield2 finite-difference diagnostics "
                "and independently reproduced native post-processing"
            ),
            "native_gevolution_logged": native_logged,
            "native_postprocessing": native_postprocessing,
            "native_log_reproduction": native_log_reproduction,
            "continuum_fft_crosscheck": {
                "status": "CROSSCHECK_ONLY_NOT_TRANSVERSALITY_GATE",
                "reason": (
                    "continuum spectral derivatives do not reproduce the "
                    "staggered/discrete LATfield2 derivative used by "
                    "gevolution's native spin-1/spin-2 projections"
                ),
                "B_divergence_rms_by_snapshot": [_rms(x) for x in b_divergence],
                "B_field_rms_by_snapshot": [_rms(x) for x in b],
                "h_divergence_rms_by_snapshot": [_rms(x) for x in h_divergence],
                "h_field_rms_by_snapshot": [_rms(x) for x in h],
                "h_trace_rms_by_snapshot": [_rms(x) for x in h_trace],
                "h_symmetry_residual_rms_by_snapshot": [_rms(x) for x in h_symmetry],
            },
        },
        "sector_frobenius_rms": {
            "inner": sector_rms_inner,
            "outer": sector_rms_outer,
            "inner_relative_to_scalar": sector_relative_to_scalar,
        },
        "modal_diagnostics": {
            "primary_spatial_operator": "LATFIELD2_GEVOLUTION_NATIVE",
            "inner_full_vs_scalar": _modal_comparison(
                sectors_inner["scalar"], sectors_inner["total"]
            ),
            "outer_full_vs_scalar": _modal_comparison(
                sectors_outer["scalar"], sectors_outer["total"]
            ),
            "inner_vs_outer_full": _modal_comparison(
                sectors_inner["total"], sectors_outer["total"]
            ),
        },
        "spatial_operator_comparison": {
            "continuum_sector_frobenius_rms": {
                "inner": continuum_sector_rms_inner,
                "outer": continuum_sector_rms_outer,
            },
            "native_vs_continuum_scalar": _modal_comparison(
                sectors_inner["scalar"], sectors_inner_continuum["scalar"]
            ),
            "native_vs_continuum_vector": _modal_comparison(
                sectors_inner["vector"], sectors_inner_continuum["vector"]
            ),
            "native_vs_continuum_tensor": _modal_comparison(
                sectors_inner["tensor"], sectors_inner_continuum["tensor"]
            ),
            "native_vs_continuum_total": _modal_comparison(
                sectors_inner["total"], sectors_inner_continuum["total"]
            ),
        },
        "limitations": [
            "single early development epoch",
            "one N64 realization",
            "no scientific acceptance threshold frozen",
            "temporal inner/outer comparison is a discretization diagnostic, not P1 evidence",
            "magnetic Weyl tensor not reconstructed in this pilot",
            "continuum FFT derivatives are retained only as a comparator because gevolution uses a staggered LATfield2 lattice derivative",
            "nonlinear observer dependence beyond first order is not tested here",
        ],
    }

    arrays = {
        "b_prime_inner": derivatives["b_prime_inner"],
        "b_prime_outer": derivatives["b_prime_outer"],
        "h_second_inner": derivatives["h_second_inner"],
        "h_second_outer": derivatives["h_second_outer"],
        "E_scalar_native": sectors_inner["scalar"],
        "E_vector_inner_native": sectors_inner["vector"],
        "E_tensor_inner_native": sectors_inner["tensor"],
        "E_total_inner_native": sectors_inner["total"],
        "E_total_outer_native": sectors_outer["total"],
        "E_scalar_continuum": sectors_inner_continuum["scalar"],
        "E_vector_inner_continuum": sectors_inner_continuum["vector"],
        "E_tensor_inner_continuum": sectors_inner_continuum["tensor"],
        "E_total_inner_continuum": sectors_inner_continuum["total"],
        "E_total_outer_continuum": sectors_outer_continuum["total"],
    }
    return report, arrays


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-dir", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--boxsize-mpc-over-h", type=float, required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--npz-output", required=True)
    args = parser.parse_args()

    report, arrays = build_report(
        pathlib.Path(args.snapshot_dir),
        pathlib.Path(args.metadata),
        args.boxsize_mpc_over_h,
    )

    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")

    npz_output = pathlib.Path(args.npz_output)
    npz_output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(npz_output, **arrays)

    print(
        json.dumps(
            {
                "protocol": report["protocol"],
                "output": str(output),
                "npz_output": str(npz_output),
                "actual_redshifts": report["actual_redshifts"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
