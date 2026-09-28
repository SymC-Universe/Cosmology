"""Durable M0 report for the relational modal descriptor.

This is a P0-Q estimator qualification only.
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

from relational_modal import (
    normalized_commutator_kappa,
    ordered_eigenvalues,
    relational_modal_record,
)


def _rotation_z(theta: float) -> np.ndarray:
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def _random_rotation(rng: np.random.Generator) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    q = q @ np.diag(signs)
    if np.linalg.det(q) < 0.0:
        q[:, 0] *= -1.0
    return q


def _stf(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(3, 3))
    sym = 0.5 * (raw + raw.T)
    return sym - np.eye(3) * np.trace(sym) / 3.0


def build_report() -> dict:
    cases = []

    a = np.diag([-1.0, 0.2, 0.8])
    b0 = np.diag([-2.0, 0.5, 1.5])
    k0 = float(normalized_commutator_kappa(a, b0))
    cases.append({
        "case_id": "RM-01",
        "purpose": "common nondegenerate eigenframe",
        "status": "PASS" if abs(k0) <= 1e-14 else "FAIL",
        "kappa": k0,
    })

    q = _rotation_z(np.deg2rad(31.0))
    b1 = q @ b0 @ q.T
    k1 = float(normalized_commutator_kappa(a, b1))
    eig_error = float(np.max(np.abs(ordered_eigenvalues(b1) - ordered_eigenvalues(b0))))
    inv2_error = abs(float(np.trace(b1 @ b1) - np.trace(b0 @ b0)))
    inv3_error = abs(float(np.trace(b1 @ b1 @ b1) - np.trace(b0 @ b0 @ b0)))
    cases.append({
        "case_id": "RM-02",
        "purpose": "matched marginal spectra with rotated relation",
        "status": "PASS" if (k1 > 0.0 and eig_error <= 1e-13 and inv2_error <= 1e-12 and inv3_error <= 1e-12) else "FAIL",
        "aligned_kappa": k0,
        "rotated_kappa": k1,
        "marginal_eigenvalue_max_abs_error": eig_error,
        "trace_B2_abs_error": inv2_error,
        "trace_B3_abs_error": inv3_error,
    })

    rng = np.random.default_rng(20260927)
    aa = _stf(rng)
    bb = _stf(rng)
    rot = _random_rotation(rng)
    before = float(normalized_commutator_kappa(aa, bb))
    after = float(normalized_commutator_kappa(rot @ aa @ rot.T, rot @ bb @ rot.T))
    cases.append({
        "case_id": "RM-03",
        "purpose": "simultaneous coordinate rotation invariance",
        "status": "PASS" if abs(after - before) <= 1e-12 else "FAIL",
        "kappa_before": before,
        "kappa_after": after,
        "abs_difference": abs(after - before),
    })

    exchanged = float(normalized_commutator_kappa(bb, aa))
    cases.append({
        "case_id": "RM-04",
        "purpose": "exchange symmetry",
        "status": "PASS" if abs(exchanged - before) <= 1e-14 else "FAIL",
        "kappa_ab": before,
        "kappa_ba": exchanged,
        "abs_difference": abs(exchanged - before),
    })

    ensemble = []
    for _ in range(2048):
        ensemble.append(float(normalized_commutator_kappa(_stf(rng), _stf(rng))))
    ensemble = np.asarray(ensemble)
    max_value = float(np.max(ensemble))
    min_value = float(np.min(ensemble))
    cases.append({
        "case_id": "RM-05",
        "purpose": "Boettcher-Wenzel normalized bound",
        "status": "PASS" if (min_value >= -1e-14 and max_value <= 1.0 + 1e-12) else "FAIL",
        "ensemble_size": int(ensemble.size),
        "min_kappa": min_value,
        "max_kappa": max_value,
        "median_kappa": float(np.median(ensemble)),
    })

    zero_record = relational_modal_record(np.zeros((3, 3)), b0)
    nonfinite = np.array(a, copy=True)
    nonfinite[0, 0] = np.nan
    nonfinite_record = relational_modal_record(nonfinite, b0)
    shape_record = relational_modal_record(np.zeros((2, 2)), b0)
    rm06_pass = (
        np.isnan(float(zero_record["kappa"]))
        and zero_record["refusal_status"].item() == "REFUSED_ZERO_NORM_A"
        and nonfinite_record["refusal_status"] == "REFUSED_NONFINITE"
        and shape_record["refusal_status"] == "REFUSED_SHAPE"
    )
    cases.append({
        "case_id": "RM-06",
        "purpose": "explicit zero-norm nonfinite and shape refusal semantics",
        "status": "PASS" if rm06_pass else "FAIL",
        "zero_norm_status": zero_record["refusal_status"].item(),
        "nonfinite_status": nonfinite_record["refusal_status"],
        "shape_status": shape_record["refusal_status"],
    })

    deg = np.diag([1.0, 1.0, -2.0])
    deg_partner = _rotation_z(np.deg2rad(23.0)) @ b0 @ _rotation_z(np.deg2rad(23.0)).T
    deg_record = relational_modal_record(deg, deg_partner)
    rm07_pass = (
        np.isfinite(float(deg_record["kappa"]))
        and bool(deg_record["degenerate_a"])
        and deg_record["direction_status"].item() == "DEGENERATE_NONIDENTIFIABLE"
        and deg_record["refusal_status"].item() == "OK"
    )
    cases.append({
        "case_id": "RM-07",
        "purpose": "degenerate eigenframe distinction",
        "status": "PASS" if rm07_pass else "FAIL",
        "kappa": float(deg_record["kappa"]),
        "degenerate_a": bool(deg_record["degenerate_a"]),
        "direction_status": deg_record["direction_status"].item(),
        "refusal_status": deg_record["refusal_status"].item(),
    })

    overall = "RELATIONAL_DESCRIPTOR_QUALIFIED_P0Q" if all(x["status"] == "PASS" for x in cases) else "RELATIONAL_DESCRIPTOR_REFUSED"
    return {
        "protocol": "RELATIONAL_MODAL_DESCRIPTOR_PREFLIGHT_v0.1",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "cosmological_prediction_tested": False,
        "primary_statistic": "||[A,B]||_F / (sqrt(2)||A||_F||B||_F)",
        "case_count": len(cases),
        "cases": cases,
        "outcome": overall,
        "next_gate_if_qualified": "APQ-qualified standard-dynamics development preflight for conditional predictive utility",
        "claim_ceiling": "descriptor/estimator qualification only",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = build_report()
    path = pathlib.Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"outcome": report["outcome"], "output": str(path)}, sort_keys=True))


if __name__ == "__main__":
    main()
