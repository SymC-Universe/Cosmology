"""Late-time Band-L material E-sigma relational development analysis.

P0-Q development only. Implements the frozen design from:
- LATE_TIME_MATERIAL_RELATIONAL_APQ2_PLAN_PACKET_v0.1.md
- LATE_TIME_MATERIAL_RELATIONAL_APQ2_ADJUDICATION_v0.1.md

This script contains no P1 logic and no dark-sector mechanism claim.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
from dataclasses import dataclass

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from electric_weyl import electric_weyl_conformal_sectors_latfield2
from fourier_resolution import (
    signed_mode_numbers,
    spectral_project_scalar_to_modes,
    spectral_project_tensor_to_modes,
)
from gevolution_particle_lineage import load_particle_snapshot
from gevolution_velocity_operators import velocity_shear_centered
from latfield_hdf5 import (
    load_scalar_field,
    load_symmetric_tensor_field,
    load_vector_field,
)
from material_patch import (
    aggregate_material_patch_tensors,
    interpolate_vertex_tensor_periodic,
    reference_patch_membership,
)
from modal_relational import analyze_tensor_relation
from modal_tensor import analyze_symmetric_tensor
from temporal_derivatives import finite_difference_weights
from tensor_colocation import colocate_symmetric_tensor_to_vertices


@dataclass(frozen=True)
class EpochFiles:
    name: str
    center_index: int
    indices: tuple[int, int, int, int, int]


def band_l_modes(n: int) -> list[tuple[int, int, int]]:
    """Frozen Band L: 0 < |n| < 4."""
    modes = signed_mode_numbers(n)
    out: list[tuple[int, int, int]] = []
    for nx in modes:
        for ny in modes:
            for nz in modes:
                r2 = int(nx * nx + ny * ny + nz * nz)
                if r2 == 0 or r2 >= 16:
                    continue
                out.append((int(nx), int(ny), int(nz)))
    return out


def _one(paths: list[pathlib.Path], description: str) -> pathlib.Path:
    if len(paths) != 1:
        raise ValueError(f"expected one {description}, found {paths}")
    return paths[0]


def _snapshot_paths(root: pathlib.Path, index: int) -> dict[str, pathlib.Path]:
    tag = f"{index:03d}"
    return {
        "phi": _one(sorted(root.glob(f"*snap{tag}_phi.h5")), f"snap{tag} phi"),
        "chi": _one(sorted(root.glob(f"*snap{tag}_chi.h5")), f"snap{tag} chi"),
        "B": _one(sorted(root.glob(f"*snap{tag}_B.h5")), f"snap{tag} B"),
        "hij": _one(sorted(root.glob(f"*snap{tag}_hij.h5")), f"snap{tag} hij"),
        "v": _one(sorted(root.glob(f"*snap{tag}_v.h5")), f"snap{tag} v"),
        "cdm": _one(sorted(root.glob(f"*snap{tag}_cdm.h5")), f"snap{tag} cdm"),
    }


def _weighted_field(
    file_paths: list[pathlib.Path],
    indices: tuple[int, int, int],
    weights: np.ndarray,
    loader,
) -> np.ndarray:
    out = None
    for i, w in zip(indices, weights):
        value = np.asarray(loader(file_paths[i]), dtype=float)
        if out is None:
            out = np.zeros_like(value, dtype=float)
        out += float(w) * value
    if out is None:
        raise ValueError("empty derivative stencil")
    return out


def _scalar_patch_mean_via_tensor(
    scalar_grid: np.ndarray,
    current_ids: np.ndarray,
    current_positions: np.ndarray,
    reference_ids: np.ndarray,
    reference_patch_ids: np.ndarray,
) -> dict[str, np.ndarray]:
    field = np.asarray(scalar_grid, dtype=float)
    iso = np.zeros(field.shape + (3, 3), dtype=float)
    for i in range(3):
        iso[..., i, i] = field
    samples = interpolate_vertex_tensor_periodic(iso, current_positions)
    agg = aggregate_material_patch_tensors(
        current_ids, samples, reference_ids, reference_patch_ids
    )
    scalar_mean = np.trace(agg["tensor"], axis1=-2, axis2=-1) / 3.0
    return {
        "patch_id": agg["patch_id"],
        "count": agg["count"],
        "value": scalar_mean,
    }


def _aggregate_tensor_grid(
    tensor_grid: np.ndarray,
    current_ids: np.ndarray,
    current_positions: np.ndarray,
    reference_ids: np.ndarray,
    reference_patch_ids: np.ndarray,
) -> dict[str, np.ndarray]:
    samples = interpolate_vertex_tensor_periodic(tensor_grid, current_positions)
    return aggregate_material_patch_tensors(
        current_ids, samples, reference_ids, reference_patch_ids
    )


def _modal_patch_state(
    e_tensor: np.ndarray,
    s_tensor: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray | None, str | None]:
    e = analyze_symmetric_tensor(e_tensor)
    s = analyze_symmetric_tensor(s_tensor)
    e_norm = float(e.invariants["frobenius_norm"])
    s_norm = float(s.invariants["frobenius_norm"])
    if e_norm == 0.0 or s_norm == 0.0:
        return (
            np.array([e_norm, s_norm], dtype=float),
            np.full(4, np.nan),
            None,
            "ZERO_NORM",
        )
    marginal = np.array(
        [
            e.eigenvalues[0] / e_norm,
            e.eigenvalues[1] / e_norm,
            s.eigenvalues[0] / s_norm,
            s.eigenvalues[1] / s_norm,
        ],
        dtype=float,
    )
    if any(e.degenerate_pairs) or any(s.degenerate_pairs):
        return (
            np.array([e_norm, s_norm], dtype=float),
            marginal,
            None,
            "EXACT_DEGENERACY",
        )
    relation = analyze_tensor_relation(e_tensor, s_tensor)
    rel = np.concatenate(
        [
            relation.alignment_matrix_abs.reshape(-1),
            np.array([float(relation.normalized_commutator_frobenius)]),
        ]
    )
    return np.array([e_norm, s_norm], dtype=float), marginal, rel, None


def _epoch_state(
    root: pathlib.Path,
    metadata: dict,
    epoch: EpochFiles,
    modes: list[tuple[int, int, int]],
    reference_ids: np.ndarray,
    memberships: dict[int, dict[str, np.ndarray]],
) -> dict:
    paths = [_snapshot_paths(root, i) for i in range(len(metadata["snapshots"]))]
    snaps = metadata["snapshots"]
    tau = np.array([float(x["tau_over_boxsize"]) for x in snaps], dtype=float)

    idx = epoch.indices
    if idx[2] != epoch.center_index:
        raise ValueError("epoch center index mismatch")
    inner = (idx[1], idx[2], idx[3])
    outer = (idx[0], idx[2], idx[4])
    center_tau = tau[epoch.center_index]
    b_in_w = finite_difference_weights(tau[list(inner)], center_tau, 1)
    b_out_w = finite_difference_weights(tau[list(outer)], center_tau, 1)
    h_in_w = finite_difference_weights(tau[list(inner)], center_tau, 2)
    h_out_w = finite_difference_weights(tau[list(outer)], center_tau, 2)

    b_files = [p["B"] for p in paths]
    h_files = [p["hij"] for p in paths]
    b_inner = _weighted_field(b_files, inner, b_in_w, load_vector_field)
    b_outer = _weighted_field(b_files, outer, b_out_w, load_vector_field)
    h_second_inner = _weighted_field(
        h_files, inner, h_in_w, load_symmetric_tensor_field
    )
    h_second_outer = _weighted_field(
        h_files, outer, h_out_w, load_symmetric_tensor_field
    )

    cpath = paths[epoch.center_index]
    phi = load_scalar_field(cpath["phi"])
    chi = load_scalar_field(cpath["chi"])
    h_center = load_symmetric_tensor_field(cpath["hij"])
    velocity = load_vector_field(cpath["v"])
    particle = load_particle_snapshot(cpath["cdm"])

    if not np.array_equal(np.sort(particle["ID"]), np.sort(reference_ids)):
        raise ValueError(f"{epoch.name}: particle ID set differs from reference")

    e_inner_native = electric_weyl_conformal_sectors_latfield2(
        phi, chi, b_inner, h_center, h_second_inner, 1.0
    )["total"]
    e_outer_native = electric_weyl_conformal_sectors_latfield2(
        phi, chi, b_outer, h_center, h_second_outer, 1.0
    )["total"]
    e_inner = colocate_symmetric_tensor_to_vertices(e_inner_native)
    e_outer = colocate_symmetric_tensor_to_vertices(e_outer_native)

    sigma, theta = velocity_shear_centered(velocity, 1.0)

    e_band = spectral_project_tensor_to_modes(
        e_inner, e_inner.shape[0], modes, keep_zero=False
    )
    e_outer_band = spectral_project_tensor_to_modes(
        e_outer, e_outer.shape[0], modes, keep_zero=False
    )
    sigma_band = spectral_project_tensor_to_modes(
        sigma, sigma.shape[0], modes, keep_zero=False
    )
    theta_band = spectral_project_scalar_to_modes(
        theta, theta.shape[0], modes, keep_zero=False
    )

    temporal_num = float(
        np.sqrt(np.mean(np.sum((e_band - e_outer_band) ** 2, axis=(-2, -1))))
    )
    temporal_den = float(
        np.sqrt(np.mean(np.sum(e_band * e_band, axis=(-2, -1))))
    )

    patch_scales = {}
    for pgrid, membership in memberships.items():
        eagg = _aggregate_tensor_grid(
            e_band,
            particle["ID"],
            particle["position"],
            membership["ID"],
            membership["patch_id"],
        )
        sagg = _aggregate_tensor_grid(
            sigma_band,
            particle["ID"],
            particle["position"],
            membership["ID"],
            membership["patch_id"],
        )
        tagg = _scalar_patch_mean_via_tensor(
            theta_band,
            particle["ID"],
            particle["position"],
            membership["ID"],
            membership["patch_id"],
        )
        if not (
            np.array_equal(eagg["patch_id"], sagg["patch_id"])
            and np.array_equal(eagg["patch_id"], tagg["patch_id"])
        ):
            raise ValueError(f"{epoch.name}: patch IDs disagree across fields")

        patch_ids = eagg["patch_id"]
        states = []
        refused = {}
        for q, patch_id in enumerate(patch_ids):
            norms, marginal, relation, refusal = _modal_patch_state(
                eagg["tensor"][q], sagg["tensor"][q]
            )
            if refusal is not None:
                refused[str(int(patch_id))] = refusal
            states.append((norms, marginal, relation))

        norms = np.stack([x[0] for x in states])
        marginal = np.stack([x[1] for x in states])
        relation = np.full((len(states), 10), np.nan, dtype=float)
        for q, x in enumerate(states):
            if x[2] is not None:
                relation[q] = x[2]

        patch_scales[str(pgrid)] = {
            "patch_id": patch_ids,
            "count": eagg["count"],
            "theta": tagg["value"],
            "norms": norms,
            "marginal": marginal,
            "relation": relation,
            "refused": refused,
        }

    return {
        "name": epoch.name,
        "center_index": epoch.center_index,
        "actual_redshift": float(snaps[epoch.center_index]["actual_redshift"]),
        "actual_scale_factor": float(snaps[epoch.center_index]["actual_scale_factor"]),
        "tau_over_boxsize": float(center_tau),
        "temporal_e_inner_outer_relative_rms": (
            temporal_num / temporal_den if temporal_den > 0.0 else None
        ),
        "b_inner_weights": b_in_w.tolist(),
        "b_outer_weights": b_out_w.tolist(),
        "h_inner_weights": h_in_w.tolist(),
        "h_outer_weights": h_out_w.tolist(),
        "patch_scales": patch_scales,
    }


def _patch_coords(patch_ids: np.ndarray, pgrid: int) -> np.ndarray:
    pid = np.asarray(patch_ids, dtype=int)
    x = pid // (pgrid * pgrid)
    rem = pid % (pgrid * pgrid)
    y = rem // pgrid
    z = rem % pgrid
    return np.column_stack([x, y, z])


def _octant_labels(patch_ids: np.ndarray, pgrid: int) -> np.ndarray:
    coord = _patch_coords(patch_ids, pgrid)
    half = pgrid // 2
    return (
        (coord[:, 0] >= half).astype(int) * 4
        + (coord[:, 1] >= half).astype(int) * 2
        + (coord[:, 2] >= half).astype(int)
    )


def _standardized_lstsq_predict(
    x_train: np.ndarray,
    y_train: np.ndarray,
    x_test: np.ndarray,
) -> tuple[np.ndarray, dict]:
    xt = np.asarray(x_train, dtype=float)
    yt = np.asarray(y_train, dtype=float)
    xv = np.asarray(x_test, dtype=float)
    if not (
        np.all(np.isfinite(xt))
        and np.all(np.isfinite(yt))
        and np.all(np.isfinite(xv))
    ):
        raise ValueError("nonfinite design or target")

    mean = np.mean(xt, axis=0)
    std = np.std(xt, axis=0)
    nonconstant = std > 0.0
    zt = np.zeros_like(xt)
    zv = np.zeros_like(xv)
    if np.any(nonconstant):
        zt[:, nonconstant] = (
            xt[:, nonconstant] - mean[nonconstant]
        ) / std[nonconstant]
        zv[:, nonconstant] = (
            xv[:, nonconstant] - mean[nonconstant]
        ) / std[nonconstant]
    design = np.column_stack([np.ones(len(zt)), zt])
    test_design = np.column_stack([np.ones(len(zv)), zv])
    coef, _, rank, sing = np.linalg.lstsq(design, yt, rcond=None)
    pred = test_design @ coef
    positive = sing[sing > 0.0]
    condition = (
        float(np.max(positive) / np.min(positive))
        if len(positive) > 0
        else math.inf
    )
    return pred, {
        "rank": int(rank),
        "columns_with_intercept": int(design.shape[1]),
        "nonconstant_columns": int(np.count_nonzero(nonconstant)),
        "condition_number": condition,
        "prediction_finite": bool(np.all(np.isfinite(pred))),
    }


def _cv_sse(
    x: np.ndarray,
    y: np.ndarray,
    folds: np.ndarray,
) -> tuple[float, np.ndarray, list[dict]]:
    predictions = np.full_like(y, np.nan, dtype=float)
    diagnostics = []
    for fold in range(8):
        test = folds == fold
        train = ~test
        if np.count_nonzero(test) == 0 or np.count_nonzero(train) == 0:
            raise ValueError(f"empty fold {fold}")
        pred, diag = _standardized_lstsq_predict(
            x[train], y[train], x[test]
        )
        predictions[test] = pred
        diag["fold"] = fold
        diag["train_n"] = int(np.count_nonzero(train))
        diag["test_n"] = int(np.count_nonzero(test))
        diagnostics.append(diag)
    if not np.all(np.isfinite(predictions)):
        raise ValueError("cross-validation produced nonfinite predictions")
    residual = y - predictions
    return float(np.sum(residual * residual)), predictions, diagnostics


def _aligned_scale_data(
    baseline: dict,
    later: dict,
    pgrid: int,
) -> dict:
    b = baseline["patch_scales"][str(pgrid)]
    l = later["patch_scales"][str(pgrid)]
    common = np.intersect1d(b["patch_id"], l["patch_id"])
    b_index = {int(x): i for i, x in enumerate(b["patch_id"])}
    l_index = {int(x): i for i, x in enumerate(l["patch_id"])}
    rows = []
    refused = []
    mean_count = float(np.mean(b["count"]))
    for pid in common:
        ib = b_index[int(pid)]
        il = l_index[int(pid)]
        if not np.all(np.isfinite(b["relation"][ib])):
            refused.append(int(pid))
            continue
        if not (
            np.all(np.isfinite(b["marginal"][ib]))
            and np.all(np.isfinite(l["marginal"][il]))
        ):
            refused.append(int(pid))
            continue
        delta_n = float(b["count"][ib] / mean_count - 1.0)
        b0 = np.concatenate(
            [
                np.array(
                    [
                        delta_n,
                        b["theta"][ib],
                        b["norms"][ib, 0],
                        b["norms"][ib, 1],
                    ]
                ),
                b["marginal"][ib],
            ]
        )
        y = l["marginal"][il] - b["marginal"][ib]
        rows.append(
            (
                int(pid),
                b0,
                b["relation"][ib],
                y,
            )
        )
    if not rows:
        raise ValueError("no valid paired material patches")
    return {
        "patch_id": np.array([x[0] for x in rows], dtype=int),
        "b0": np.stack([x[1] for x in rows]),
        "relation": np.stack([x[2] for x in rows]),
        "y": np.stack([x[3] for x in rows]),
        "refused_patch_ids": refused,
    }


def _shift_relation(
    patch_ids: np.ndarray,
    relation: np.ndarray,
    pgrid: int,
    shift: tuple[int, int, int],
) -> tuple[np.ndarray, np.ndarray]:
    mapping = {int(pid): relation[i] for i, pid in enumerate(patch_ids)}
    coords = _patch_coords(patch_ids, pgrid)
    shifted_source = (coords - np.array(shift)[None, :]) % pgrid
    shifted_ids = (
        shifted_source[:, 0] * pgrid * pgrid
        + shifted_source[:, 1] * pgrid
        + shifted_source[:, 2]
    )
    keep = np.array([int(pid) in mapping for pid in shifted_ids], dtype=bool)
    out = np.full_like(relation, np.nan)
    for i, (ok, source_pid) in enumerate(zip(keep, shifted_ids)):
        if ok:
            out[i] = mapping[int(source_pid)]
    return out, keep


def _evaluate_scale(
    baseline: dict,
    later: dict,
    pgrid: int,
    *,
    run_shift_null: bool,
) -> dict:
    data = _aligned_scale_data(baseline, later, pgrid)
    pid = data["patch_id"]
    b0 = data["b0"]
    rel = data["relation"]
    y = data["y"]
    folds = _octant_labels(pid, pgrid)

    sse_b0, pred_b0, diag_b0 = _cv_sse(b0, y, folds)
    b1 = np.column_stack([b0, rel])
    sse_b1, pred_b1, diag_b1 = _cv_sse(b1, y, folds)
    sse_p = float(np.sum(y * y))
    delta = (sse_b0 - sse_b1) / sse_b0 if sse_b0 > 0.0 else None

    fold_delta = []
    for fold in range(8):
        mask = folds == fold
        r0 = y[mask] - pred_b0[mask]
        r1 = y[mask] - pred_b1[mask]
        e0 = float(np.sum(r0 * r0))
        e1 = float(np.sum(r1 * r1))
        fold_delta.append(
            {
                "fold": fold,
                "delta_rel": (e0 - e1) / e0 if e0 > 0.0 else None,
                "sse_b0": e0,
                "sse_b1": e1,
            }
        )

    shift_values = []
    shift_valid_counts = []
    if run_shift_null:
        for dx in range(pgrid):
            for dy in range(pgrid):
                for dz in range(pgrid):
                    if dx == dy == dz == 0:
                        continue
                    shifted, keep = _shift_relation(
                        pid, rel, pgrid, (dx, dy, dz)
                    )
                    if np.count_nonzero(keep) == 0:
                        shift_values.append(np.nan)
                        shift_valid_counts.append(0)
                        continue
                    # Preserve the subset for which the translated source
                    # relation is available. If any fold becomes unfittable,
                    # retain NaN and let the outcome become NEED_MORE_INFO.
                    subset = keep
                    try:
                        s0, _, _ = _cv_sse(b0[subset], y[subset], folds[subset])
                        s1, _, _ = _cv_sse(
                            np.column_stack([b0[subset], shifted[subset]]),
                            y[subset],
                            folds[subset],
                        )
                        d = (s0 - s1) / s0 if s0 > 0.0 else np.nan
                    except ValueError:
                        d = np.nan
                    shift_values.append(float(d))
                    shift_valid_counts.append(int(np.count_nonzero(subset)))

    comp_sse_b0 = np.sum((y - pred_b0) ** 2, axis=0)
    comp_sse_b1 = np.sum((y - pred_b1) ** 2, axis=0)
    report = {
        "patch_grid": pgrid,
        "valid_patch_count": int(len(pid)),
        "refused_patch_count": int(len(data["refused_patch_ids"])),
        "refused_patch_ids": data["refused_patch_ids"],
        "sse_persistence": sse_p,
        "sse_b0": sse_b0,
        "sse_b1": sse_b1,
        "delta_rel": delta,
        "target_component_sse_b0": comp_sse_b0.tolist(),
        "target_component_sse_b1": comp_sse_b1.tolist(),
        "foldwise": fold_delta,
        "b0_fold_diagnostics": diag_b0,
        "b1_fold_diagnostics": diag_b1,
    }
    if run_shift_null:
        arr = np.asarray(shift_values, dtype=float)
        finite = arr[np.isfinite(arr)]
        report["shift_null"] = {
            "requested_shift_count": int(pgrid ** 3 - 1),
            "finite_shift_count": int(len(finite)),
            "delta_rel_q05": float(np.quantile(finite, 0.05))
            if len(finite) else None,
            "delta_rel_median": float(np.quantile(finite, 0.50))
            if len(finite) else None,
            "delta_rel_q95": float(np.quantile(finite, 0.95))
            if len(finite) else None,
            "min_valid_patch_count": int(min(shift_valid_counts))
            if shift_valid_counts else 0,
            "max_valid_patch_count": int(max(shift_valid_counts))
            if shift_valid_counts else 0,
            "values": shift_values,
        }
    return report


def _primary_disposition(primary: dict, sensitivities: list[dict]) -> str:
    shift = primary.get("shift_null")
    if shift is None or shift["finite_shift_count"] < 511:
        return "NEED_MORE_INFO"
    delta = primary["delta_rel"]
    if delta is None or not np.isfinite(delta):
        return "NEED_MORE_INFO"

    signal = (
        delta > 0.0
        and delta > shift["delta_rel_q95"]
        and primary["sse_b1"] < primary["sse_persistence"]
    )
    subtracts = (
        delta < 0.0
        and delta < shift["delta_rel_q05"]
    ) or (
        primary["sse_b1"] > primary["sse_b0"]
        and primary["sse_b1"] > primary["sse_persistence"]
    )

    # Sensitivities do not rescue the primary result. If they point in a
    # qualitatively contradictory direction, force NEED_MORE_INFO.
    primary_sign = np.sign(delta)
    for s in sensitivities:
        sd = s["delta_rel"]
        if sd is not None and np.isfinite(sd) and np.sign(sd) != 0:
            if primary_sign != 0 and np.sign(sd) != primary_sign:
                return "NEED_MORE_INFO"

    if signal:
        return "DEVELOPMENT_SIGNAL_PRESENT"
    if subtracts:
        return "DEVELOPMENT_SUBTRACTS"
    return "DEVELOPMENT_EQUIVALENT_OR_UNRESOLVED"


def build_report(
    root: pathlib.Path,
    metadata_path: pathlib.Path,
) -> dict:
    metadata = json.loads(metadata_path.read_text())
    if int(metadata["grid"]) != 64:
        raise ValueError("frozen development requires N64")
    snaps = metadata["snapshots"]
    if len(snaps) != 15:
        raise ValueError("frozen development requires 15 snapshots")

    modes = band_l_modes(64)
    if len(modes) != 250:
        raise ValueError(f"Band L mode count changed: {len(modes)}")

    epochs = [
        EpochFiles("z2", 2, (0, 1, 2, 3, 4)),
        EpochFiles("z1", 7, (5, 6, 7, 8, 9)),
        EpochFiles("z0p5", 12, (10, 11, 12, 13, 14)),
    ]

    ref_particle = load_particle_snapshot(_snapshot_paths(root, 2)["cdm"])
    memberships = {
        pgrid: reference_patch_membership(
            ref_particle["ID"],
            ref_particle["position"],
            (pgrid, pgrid, pgrid),
        )
        for pgrid in (4, 8, 16)
    }

    states = {
        e.name: _epoch_state(
            root, metadata, e, modes, ref_particle["ID"], memberships
        )
        for e in epochs
    }

    primary = _evaluate_scale(states["z2"], states["z1"], 8, run_shift_null=True)
    coarse = _evaluate_scale(states["z2"], states["z1"], 4, run_shift_null=False)
    fine = _evaluate_scale(states["z2"], states["z1"], 16, run_shift_null=False)
    continuation = _evaluate_scale(
        states["z2"], states["z0p5"], 8, run_shift_null=False
    )

    outcome = _primary_disposition(primary, [coarse, fine])

    return {
        "protocol": "P0-Q_LATE_TIME_MATERIAL_RELATIONAL_DEVELOPMENT",
        "scientific_stage": "P0-Q_DEVELOPMENT",
        "p1_evidence": False,
        "seed": 424242,
        "grid": 64,
        "boxsize_mpc_over_h": 64.0,
        "band_l": {
            "definition": "0 < |n| < 4",
            "mode_count": len(modes),
        },
        "frozen_primary_patch_grid": [8, 8, 8],
        "sensitivity_patch_grids": [[4, 4, 4], [16, 16, 16]],
        "epochs": {
            key: {
                k: v
                for k, v in value.items()
                if k != "patch_scales"
            }
            for key, value in states.items()
        },
        "primary_z2_to_z1": primary,
        "coarse_sensitivity_z2_to_z1": coarse,
        "fine_sensitivity_z2_to_z1": fine,
        "secondary_z2_to_z0p5": continuation,
        "development_outcome": outcome,
        "claim_ceiling": (
            "development-only information/organization screen within the "
            "frozen weak-field LambdaCDM representation"
        ),
        "limitations": [
            "single development seed",
            "octant folds are spatial blocks, not independent cosmological realizations",
            "511 torus shifts are a development randomization screen, not a P1 p-value",
            "positive development outcome does not activate P1",
            "negative development outcome does not close independent exploration gates",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-dir", required=True)
    parser.add_argument("--metadata", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report(
        pathlib.Path(args.snapshot_dir),
        pathlib.Path(args.metadata),
    )
    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "development_outcome": report["development_outcome"],
                "delta_rel": report["primary_z2_to_z1"]["delta_rel"],
                "sse_persistence": report["primary_z2_to_z1"]["sse_persistence"],
                "sse_b0": report["primary_z2_to_z1"]["sse_b0"],
                "sse_b1": report["primary_z2_to_z1"]["sse_b1"],
                "output": str(out),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
