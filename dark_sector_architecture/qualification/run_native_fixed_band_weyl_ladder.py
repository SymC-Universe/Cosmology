"""Native fixed-band electric-Weyl resolution ladder.

P0-Q representation qualification under
NATIVE_FIXED_BAND_WEYL_RESOLUTION_PREREG.md.

Primary order of operations:
1. reconstruct with each native grid operator;
2. project reconstructed tensors onto the frozen K_32 support;
3. compare N32/N64/N128 on the common grid.

Continuum FFT objects are comparator representations only.
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
    symmetric_trace_free,
)
from fourier_resolution import (
    active_overlap_modes,
    spectral_project_tensor_to_modes,
)
from latfield2_native_operators import (
    lattice_tensor_diagnostics,
    lattice_vector_diagnostics,
    lattice_vector_symmetric_gradient,
)
from latfield_hdf5 import (
    load_scalar_field,
    load_symmetric_tensor_field,
    load_vector_field,
)
from modal_convergence import (
    directional_bound_from_tensor_error,
    eigenframe_absolute_alignment,
    eigengaps,
    ordered_eigensystem,
    quantile_summary,
    tensor_operator_error,
)
from temporal_derivatives import finite_difference_weights
from weak_field_tensors import velocity_shear_tensor


def _rms(arr: np.ndarray) -> float:
    x = np.asarray(arr, dtype=float)
    return float(np.sqrt(np.mean(x * x)))


def _tensor_frobenius_rms(arr: np.ndarray) -> float:
    x = np.asarray(arr, dtype=float)
    return float(np.sqrt(np.mean(np.sum(x * x, axis=(-2, -1)))))


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
    alignment = eigenframe_absolute_alignment(ref_vectors, cand_vectors)
    diagonal = np.diagonal(alignment, axis1=-2, axis2=-1)
    direction = directional_bound_from_tensor_error(op_error, ref_values)

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


def _field_paths(snapshot_dir: pathlib.Path, index: int) -> dict[str, pathlib.Path]:
    tag = f"{index:03d}"
    result = {}
    for token in ("phi", "chi", "B", "hij", "v"):
        matches = sorted(snapshot_dir.glob(f"*snap{tag}_{token}.h5"))
        if len(matches) != 1:
            raise ValueError(
                f"expected one snap{tag}_{token}.h5 in {snapshot_dir}, found {matches}"
            )
        result[token] = matches[0]
    return result


def _weighted_sum(
    paths: list[pathlib.Path],
    indices: list[int],
    weights: np.ndarray,
    loader,
) -> np.ndarray:
    out = None
    for index, weight in zip(indices, weights):
        value = np.asarray(loader(paths[index]), dtype=float)
        if out is None:
            out = np.zeros_like(value, dtype=float)
        out += float(weight) * value
    if out is None:
        raise ValueError("empty weighted sum")
    return out


def _project_tensor(
    tensor: np.ndarray, target_n: int, modes: list[tuple[int, int, int]]
) -> np.ndarray:
    return spectral_project_tensor_to_modes(
        tensor, target_n, modes, keep_zero=True
    )


def _direction_status(previous: dict, latest: dict) -> str:
    p = previous["relative_operator_error_quantiles"]
    q = latest["relative_operator_error_quantiles"]
    med_improves = q["median"] < p["median"]
    q95_improves = q["q95"] < p["q95"]
    if med_improves and q95_improves:
        return "CONVERGENT_DIRECTION"
    if (q["median"] > p["median"]) and (q["q95"] > p["q95"]):
        return "WORSENING_DIRECTION"
    return "MIXED_DIRECTION"


def _member(
    grid: int,
    snapshot_dir: pathlib.Path,
    metadata_path: pathlib.Path,
    target_n: int,
    modes: list[tuple[int, int, int]],
    coordinate_boxsize: float,
) -> dict:
    metadata = json.loads(metadata_path.read_text())
    if int(metadata["grid"]) != int(grid):
        raise ValueError(f"metadata grid mismatch for N{grid}")
    snapshots = metadata.get("snapshots")
    if not isinstance(snapshots, list) or len(snapshots) != 5:
        raise ValueError("metadata must contain five snapshots")
    tau = np.array([float(x["tau_over_boxsize"]) for x in snapshots])
    if not np.all(np.diff(tau) > 0.0):
        raise ValueError(f"N{grid} conformal times are not increasing")
    cycles = [int(x["cycle"]) for x in snapshots]
    if len(set(cycles)) != 5:
        raise ValueError(f"N{grid} snapshots do not occupy five distinct cycles")

    paths = [_field_paths(snapshot_dir, i) for i in range(5)]
    center = 2
    inner = [1, 2, 3]
    outer = [0, 2, 4]
    b_inner_w = finite_difference_weights(tau[inner], tau[center], 1)
    b_outer_w = finite_difference_weights(tau[outer], tau[center], 1)
    h_inner_w = finite_difference_weights(tau[inner], tau[center], 2)
    h_outer_w = finite_difference_weights(tau[outer], tau[center], 2)

    b_paths = [x["B"] for x in paths]
    h_paths = [x["hij"] for x in paths]
    b_inner = _weighted_sum(b_paths, inner, b_inner_w, load_vector_field)
    b_outer = _weighted_sum(b_paths, outer, b_outer_w, load_vector_field)
    h_inner = _weighted_sum(
        h_paths, inner, h_inner_w, load_symmetric_tensor_field
    )
    h_outer = _weighted_sum(
        h_paths, outer, h_outer_w, load_symmetric_tensor_field
    )

    phi = load_scalar_field(paths[center]["phi"])
    chi = load_scalar_field(paths[center]["chi"])
    h_center = load_symmetric_tensor_field(paths[center]["hij"])
    velocity = load_vector_field(paths[center]["v"])

    native_inner = electric_weyl_conformal_sectors_latfield2(
        phi, chi, b_inner, h_center, h_inner, coordinate_boxsize
    )
    native_outer = electric_weyl_conformal_sectors_latfield2(
        phi, chi, b_outer, h_center, h_outer, coordinate_boxsize
    )
    continuum_inner = electric_weyl_conformal_sectors(
        phi, chi, b_inner, h_center, h_inner, coordinate_boxsize
    )
    continuum_outer = electric_weyl_conformal_sectors(
        phi, chi, b_outer, h_center, h_outer, coordinate_boxsize
    )

    native_shear = symmetric_trace_free(
        lattice_vector_symmetric_gradient(velocity, coordinate_boxsize)
    )
    continuum_shear, _ = velocity_shear_tensor(velocity, coordinate_boxsize)

    families = ("scalar", "vector", "tensor", "total")
    native_band_inner = {
        key: _project_tensor(native_inner[key], target_n, modes)
        for key in families
    }
    native_band_outer = {
        key: _project_tensor(native_outer[key], target_n, modes)
        for key in families
    }
    continuum_band_inner = {
        key: _project_tensor(continuum_inner[key], target_n, modes)
        for key in families
    }
    continuum_band_outer = {
        key: _project_tensor(continuum_outer[key], target_n, modes)
        for key in families
    }
    native_shear_band = _project_tensor(native_shear, target_n, modes)
    continuum_shear_band = _project_tensor(continuum_shear, target_n, modes)

    native_constraints = []
    for i in range(5):
        b_i = load_vector_field(paths[i]["B"])
        h_i = load_symmetric_tensor_field(paths[i]["hij"])
        native_constraints.append(
            {
                "index": i,
                "B": lattice_vector_diagnostics(b_i, coordinate_boxsize),
                "h": lattice_tensor_diagnostics(h_i, coordinate_boxsize),
            }
        )

    temporal_band = {
        key: _tensor_difference(native_band_inner[key], native_band_outer[key])
        for key in families
    }

    native_vs_continuum = {
        key: _tensor_difference(
            native_band_inner[key], continuum_band_inner[key]
        )
        for key in families
    }
    native_vs_continuum["shear"] = _tensor_difference(
        native_shear_band, continuum_shear_band
    )

    scalar_rms = _tensor_frobenius_rms(native_band_inner["scalar"])
    sector_rms = {
        key: _tensor_frobenius_rms(native_band_inner[key])
        for key in families
    }
    sector_relative = {
        key: (sector_rms[key] / scalar_rms if scalar_rms > 0.0 else None)
        for key in ("vector", "tensor", "total")
    }

    return {
        "grid": int(grid),
        "metadata": metadata,
        "central_actual_redshift": float(snapshots[center]["actual_redshift"]),
        "central_actual_scale_factor": float(snapshots[center]["actual_scale_factor"]),
        "central_tau_over_boxsize": float(tau[center]),
        "cycles": cycles,
        "temporal_weights": {
            "b_inner": b_inner_w.tolist(),
            "b_outer": b_outer_w.tolist(),
            "h_inner": h_inner_w.tolist(),
            "h_outer": h_outer_w.tolist(),
        },
        "temporal_derivative_field_rms": {
            "b_prime_inner": _rms(b_inner),
            "b_prime_outer": _rms(b_outer),
            "b_prime_inner_outer_relative_rms": (
                _rms(b_inner - b_outer) / _rms(b_inner)
                if _rms(b_inner) > 0.0 else None
            ),
            "h_second_inner": _rms(h_inner),
            "h_second_outer": _rms(h_outer),
            "h_second_inner_outer_relative_rms": (
                _rms(h_inner - h_outer) / _rms(h_inner)
                if _rms(h_inner) > 0.0 else None
            ),
        },
        "native_constraints_logged": metadata.get("native_field_diagnostics"),
        "native_constraints_reproduced": native_constraints,
        "common_band_sector_frobenius_rms": sector_rms,
        "common_band_sector_relative_to_scalar": sector_relative,
        "temporal_common_band_inner_vs_outer": temporal_band,
        "native_vs_continuum_common_band": native_vs_continuum,
        "native_common_band": {
            **native_band_inner,
            "shear": native_shear_band,
        },
        "continuum_common_band": {
            **continuum_band_inner,
            "shear": continuum_shear_band,
        },
    }


def build_report(
    members: list[tuple[int, pathlib.Path, pathlib.Path]],
    target_n: int,
    boxsize_mpc_over_h: float,
) -> dict:
    grids = [int(x[0]) for x in members]
    if grids != [32, 64, 128]:
        raise ValueError("frozen ladder requires grids exactly [32,64,128]")
    if target_n != 32:
        raise ValueError("frozen common target grid is N=32")

    modes = active_overlap_modes(target_n)
    coordinate_boxsize = 1.0
    loaded = [
        _member(
            grid, directory, metadata, target_n, modes, coordinate_boxsize
        )
        for grid, directory, metadata in members
    ]

    families = ("scalar", "vector", "tensor", "total", "shear")
    adjacent = []
    for low, high in zip(loaded, loaded[1:]):
        comparison = {
            "low_grid": low["grid"],
            "high_grid": high["grid"],
        }
        for family in families:
            comparison[family] = _tensor_difference(
                low["native_common_band"][family],
                high["native_common_band"][family],
            )
        adjacent.append(comparison)

    directional = {}
    for family in families:
        directional[family] = {
            "status": _direction_status(
                adjacent[0][family], adjacent[1][family]
            ),
            "n32_n64_median_relative_operator_error": adjacent[0][family][
                "relative_operator_error_quantiles"
            ]["median"],
            "n64_n128_median_relative_operator_error": adjacent[1][family][
                "relative_operator_error_quantiles"
            ]["median"],
            "n32_n64_q95_relative_operator_error": adjacent[0][family][
                "relative_operator_error_quantiles"
            ]["q95"],
            "n64_n128_q95_relative_operator_error": adjacent[1][family][
                "relative_operator_error_quantiles"
            ]["q95"],
        }

    split = {}
    for family in families:
        medians = [
            m["native_vs_continuum_common_band"][family][
                "relative_operator_error_quantiles"
            ]["median"]
            for m in loaded
        ]
        native_latest = adjacent[1][family][
            "relative_operator_error_quantiles"
        ]["median"]
        if medians[0] > medians[1] > medians[2] and medians[2] <= native_latest:
            status = "SPLIT_COLLAPSES_ON_COMMON_BAND"
        elif medians[2] > native_latest and not (medians[0] > medians[1] > medians[2]):
            status = "SPLIT_PERSISTS_ON_COMMON_BAND"
        else:
            status = "SPLIT_NEED_MORE_INFO"
        split[family] = {
            "status": status,
            "native_vs_continuum_median_relative_operator_error_by_grid": {
                str(m["grid"]): value for m, value in zip(loaded, medians)
            },
            "native_n64_n128_median_resolution_error": native_latest,
        }

    central_taus = [m["central_tau_over_boxsize"] for m in loaded]
    central_redshifts = [m["central_actual_redshift"] for m in loaded]
    min_inner_halfspan = min(
        min(
            abs(float(m["metadata"]["snapshots"][2]["tau_over_boxsize"])
                - float(m["metadata"]["snapshots"][1]["tau_over_boxsize"])),
            abs(float(m["metadata"]["snapshots"][3]["tau_over_boxsize"])
                - float(m["metadata"]["snapshots"][2]["tau_over_boxsize"])),
        )
        for m in loaded
    )
    tau_spread = max(central_taus) - min(central_taus)

    member_summaries = []
    for m in loaded:
        member_summaries.append(
            {
                key: value
                for key, value in m.items()
                if key not in ("native_common_band", "continuum_common_band")
            }
        )

    core_full = directional["total"]["status"]
    core_scalar = directional["scalar"]["status"]
    if core_full == "CONVERGENT_DIRECTION" and core_scalar == "CONVERGENT_DIRECTION":
        mechanical_candidate = "NATIVE_FIXED_BAND_QUALIFICATION_CANDIDATE"
    elif core_full == "WORSENING_DIRECTION" and core_scalar == "WORSENING_DIRECTION":
        mechanical_candidate = "REFUSAL_DIRECTION_CANDIDATE"
    else:
        mechanical_candidate = "NEED_MORE_INFO_DIRECTION_CANDIDATE"

    return {
        "protocol": "P0-Q_NATIVE_FIXED_BAND_WEYL_RESOLUTION_LADDER",
        "stage": "P0-Q",
        "preregistration": "NATIVE_FIXED_BAND_WEYL_RESOLUTION_PREREG.md",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "target_grid": int(target_n),
        "boxsize_mpc_over_h": float(boxsize_mpc_over_h),
        "common_band": {
            "definition": "0 < |n| < 15 and |n_i| < 15",
            "mode_count": int(len(modes)),
            "source": "gevolution N32 active-overlap sphere",
            "order_of_operations": "native reconstruction first; fixed-band projection second",
        },
        "central_epoch_alignment": {
            "tau_over_boxsize_by_grid": {
                str(m["grid"]): m["central_tau_over_boxsize"] for m in loaded
            },
            "actual_redshift_by_grid": {
                str(m["grid"]): m["central_actual_redshift"] for m in loaded
            },
            "tau_spread": float(tau_spread),
            "tau_spread_over_min_inner_halfspan": (
                float(tau_spread / min_inner_halfspan)
                if min_inner_halfspan > 0.0 else None
            ),
            "redshift_spread": float(max(central_redshifts) - min(central_redshifts)),
        },
        "members": member_summaries,
        "native_adjacent_resolution_comparisons": adjacent,
        "native_resolution_direction": directional,
        "native_vs_continuum_split": split,
        "mechanical_outcome_candidate": mechanical_candidate,
        "limitations": [
            "P0-Q representation qualification only; no P1 claim",
            "single early epoch and one seed",
            "magnetic Weyl tensor is not reconstructed",
            "no post hoc eigengap or percentage threshold is introduced",
            "sector-level indeterminacy must not be hidden inside total-Weyl convergence",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-grid", type=int, required=True)
    parser.add_argument("--boxsize-mpc-over-h", type=float, required=True)
    parser.add_argument(
        "--member",
        action="append",
        nargs=3,
        metavar=("GRID", "SNAPSHOT_DIR", "METADATA_JSON"),
        required=True,
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    members = [
        (int(grid), pathlib.Path(directory), pathlib.Path(metadata))
        for grid, directory, metadata in args.member
    ]
    report = build_report(members, args.target_grid, args.boxsize_mpc_over_h)
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "protocol": report["protocol"],
                "mode_count": report["common_band"]["mode_count"],
                "mechanical_outcome_candidate": report["mechanical_outcome_candidate"],
                "output": str(output),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
