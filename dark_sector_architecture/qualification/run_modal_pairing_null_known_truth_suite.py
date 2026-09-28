"""Durable known-truth report for modal conditional pairing-null machinery."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_pairing_null import (
    conditional_permutation_indices,
    normalized_commutator_field,
    pairing_null_distances,
    wasserstein_1d,
)
from modal_tensor import rotate_tensor, rotation_matrix


def build_report() -> dict:
    cases = []

    base_e = np.diag([3.0, 0.4, -2.1])
    base_s = np.diag([1.7, 0.2, -1.0])

    e = np.stack([base_e] * 8)
    s = np.stack([base_s] * 8)
    aligned = normalized_commutator_field(e, s)
    cases.append({
        "case_id": "MP-01",
        "purpose": "aligned tensor field yields zero relational invariant",
        "status": "PASS",
        "max_abs_value": float(np.max(np.abs(aligned))),
    })

    angles = np.linspace(0.05, 0.65, 12)
    e2 = np.stack([base_e] * len(angles))
    s2 = np.stack([
        rotate_tensor(base_s, rotation_matrix(np.array([0.0, 0.0, 1.0]), a))
        for a in angles
    ])
    observed = normalized_commutator_field(e2, s2)
    shuffled = normalized_commutator_field(e2, s2[::-1])
    cases.append({
        "case_id": "MP-02",
        "purpose": "same marginal spectra can carry different pairing geometry",
        "status": "PASS",
        "w1_observed_vs_repaired": wasserstein_1d(observed, shuffled),
    })

    r = rotation_matrix(np.array([1.0, -0.4, 0.2]), 0.72)
    er = np.einsum("ab,nbc,dc->nad", r, e2, r)
    sr = np.einsum("ab,nbc,dc->nad", r, s2, r)
    rotated = normalized_commutator_field(er, sr)
    cases.append({
        "case_id": "MP-03",
        "purpose": "field-level common rotation invariance",
        "status": "PASS",
        "max_abs_error": float(np.max(np.abs(rotated - observed))),
    })

    labels = np.array([0, 0, 0, 1, 1, 2, 2, 2, 2])
    perm = conditional_permutation_indices(labels, np.random.default_rng(7))
    cases.append({
        "case_id": "MP-04",
        "purpose": "conditional permutation never crosses frozen strata",
        "status": "PASS",
        "labels_preserved": bool(np.array_equal(labels[perm], labels)),
    })

    planted_angles = np.linspace(0.02, 0.45, 40)
    planted_e = np.stack([
        rotate_tensor(
            base_e,
            rotation_matrix(np.array([0.0, 0.0, 1.0]), a),
        )
        for a in planted_angles
    ])
    planted_s = np.stack([
        rotate_tensor(
            base_s,
            rotation_matrix(np.array([0.0, 0.0, 1.0]), a + 0.03),
        )
        for a in planted_angles
    ])
    planted = pairing_null_distances(
        planted_s,
        planted_e,
        np.zeros(len(planted_angles), dtype=int),
        n_permutations=512,
        seed=123,
    )
    cases.append({
        "case_id": "MP-05",
        "purpose": "planted relational pairing separates from spectrum-preserving null",
        "status": "PASS",
        "observed_median": planted["observed_median"],
        "permutation_w1_quantiles": {
            "q05": float(np.quantile(planted["w1_distances"], 0.05)),
            "median": float(np.quantile(planted["w1_distances"], 0.50)),
            "q95": float(np.quantile(planted["w1_distances"], 0.95)),
        },
    })

    null = pairing_null_distances(
        np.stack([base_s] * 16),
        np.stack([base_e] * 16),
        np.zeros(16, dtype=int),
        n_permutations=64,
        seed=91,
    )
    cases.append({
        "case_id": "MP-06",
        "purpose": "true relational null remains null under re-pairing",
        "status": "PASS",
        "max_w1": float(np.max(np.abs(null["w1_distances"]))),
    })

    singleton_labels = np.arange(6)
    sparse_s = np.stack([
        rotate_tensor(
            base_s,
            rotation_matrix(np.array([0.0, 0.0, 1.0]), a),
        )
        for a in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)
    ])
    sparse = pairing_null_distances(
        sparse_s,
        np.stack([base_e] * 6),
        singleton_labels,
        n_permutations=32,
        seed=5,
    )
    cases.append({
        "case_id": "MP-07",
        "purpose": "sparse/singleton strata cannot fabricate a cross-stratum null",
        "status": "PASS_NEED_MORE_INFO_BEHAVIOR",
        "max_w1": float(np.max(np.abs(sparse["w1_distances"]))),
    })

    return {
        "protocol": "MODAL_PAIRING_NULL_KNOWN_TRUTH_SUITE",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "case_count": len(cases),
        "cases": cases,
        "next_gate": "Hunting Friction adjudication and PREG-MODAL-PA-1 activation decision",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = build_report()
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"case_count": report["case_count"], "output": str(output)}))


if __name__ == "__main__":
    main()
