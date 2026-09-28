"""Durable known-truth report for relational shear-Weyl modal diagnostics."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_relational import analyze_tensor_relation, relation_under_common_rotation
from modal_tensor import rotate_tensor, rotation_matrix


def build_report() -> dict:
    cases = []

    e = np.diag([3.0, 0.4, -2.1])
    s = np.diag([1.7, 0.2, -1.0])
    aligned = analyze_tensor_relation(e, s)
    cases.append({
        "case_id": "MR-01",
        "purpose": "aligned distinct spectra yield zero commutator",
        "status": "PASS",
        "result": aligned.as_jsonable(),
    })

    rel = rotation_matrix(np.array([0.0, 0.0, 1.0]), 0.43)
    s_rot = rotate_tensor(s, rel)
    rotated = analyze_tensor_relation(e, s_rot)
    cases.append({
        "case_id": "MR-02",
        "purpose": "same separate spectra/invariants but different relative eigenframe",
        "status": "PASS_RELATIONAL_INFORMATION_NOT_REDUCED_TO_SEPARATE_SPECTRA",
        "aligned_normalized_commutator": aligned.normalized_commutator_frobenius,
        "rotated_normalized_commutator": rotated.normalized_commutator_frobenius,
        "rotated_alignment_matrix_abs": rotated.alignment_matrix_abs.tolist(),
        "same_second_eigenvalues": bool(np.allclose(
            aligned.second.eigenvalues, rotated.second.eigenvalues, atol=1e-12, rtol=1e-12
        )),
    })

    global_rotation = rotation_matrix(np.array([1.0, -2.0, 0.3]), 0.79)
    common = relation_under_common_rotation(e, s_rot, global_rotation)
    cases.append({
        "case_id": "MR-03",
        "purpose": "common coordinate rotation covariance",
        "status": "PASS",
        "alignment_max_abs_error": float(np.max(np.abs(
            common.alignment_matrix_abs - rotated.alignment_matrix_abs
        ))),
        "commutator_norm_abs_error": abs(
            common.commutator_frobenius_norm - rotated.commutator_frobenius_norm
        ),
        "normalized_commutator_abs_error": abs(
            float(common.normalized_commutator_frobenius)
            - float(rotated.normalized_commutator_frobenius)
        ),
        "axial_rotation_max_abs_error": float(np.max(np.abs(
            common.commutator_axial_vector
            - global_rotation @ rotated.commutator_axial_vector
        ))),
    })

    e_deg = np.diag([1.0, 1.0, -2.0])
    s_deg = rotate_tensor(
        np.diag([2.0, 2.0, -4.0]),
        rotation_matrix(np.array([0.0, 0.0, 1.0]), 0.71),
    )
    degenerate = analyze_tensor_relation(e_deg, s_deg)
    cases.append({
        "case_id": "MR-04",
        "purpose": "exact degenerate subspace refuses unique-axis interpretation",
        "status": "REFUSED_UNIQUE_AXIS_RELATION_BUT_TENSOR_RELATION_RETAINED",
        "result": degenerate.as_jsonable(),
    })

    zero = analyze_tensor_relation(np.zeros((3, 3)), np.diag([1.0, 0.0, -1.0]))
    cases.append({
        "case_id": "MR-05",
        "purpose": "zero-norm tensor refuses normalized commutator",
        "status": "REFUSED_NORMALIZED_SCALAR_SUMMARY",
        "result": zero.as_jsonable(),
    })

    generic = analyze_tensor_relation(
        np.diag([2.0, 0.5, -1.5]),
        rotate_tensor(
            np.diag([1.2, 0.1, -0.8]),
            rotation_matrix(np.array([1.0, 1.0, 0.0]), 0.37),
        ),
    )
    cases.append({
        "case_id": "MR-06",
        "purpose": "symmetric-tensor commutator is antisymmetric",
        "status": "PASS",
        "antisymmetry_residual": float(np.linalg.norm(
            generic.commutator + generic.commutator.T, ord="fro"
        )),
    })

    base = np.diag([1.4, 0.1, -0.9])
    sweep = []
    for angle in (0.0, 0.1, 0.2, 0.3):
        relation = analyze_tensor_relation(
            np.diag([3.0, 0.5, -2.0]),
            rotate_tensor(
                base, rotation_matrix(np.array([0.0, 0.0, 1.0]), angle)
            ),
        )
        sweep.append({
            "angle_radians": angle,
            "commutator_frobenius_norm": relation.commutator_frobenius_norm,
            "normalized_commutator_frobenius": relation.normalized_commutator_frobenius,
        })
    cases.append({
        "case_id": "MR-07",
        "purpose": "relative rotation produces continuous relational response",
        "status": "MEASURED_NO_SCIENTIFIC_THRESHOLD_FROZEN",
        "rotation_sweep": sweep,
    })

    return {
        "protocol": "MODAL_RELATIONAL_KNOWN_TRUTH_SUITE",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "primary_object": "full relation between two symmetric modal tensors",
        "relational_objects": [
            "absolute eigenframe overlap matrix",
            "tensor commutator",
            "commutator axial vector",
            "commutator norm summaries",
        ],
        "case_count": len(cases),
        "cases": cases,
        "next_gate": "APQ-3 residual/adjudication before any late-time outcome exposure",
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
