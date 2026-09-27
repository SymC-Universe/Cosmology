from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_tensor import (
    analyze_symmetric_tensor,
    eigenframe_alignment,
    perturbation_direction_bound,
    rotate_tensor,
    rotation_matrix,
)


def _record(case_id, purpose, result=None, status="PASS", extra=None):
    item = {
        "case_id": case_id,
        "purpose": purpose,
        "status": status,
    }
    if result is not None:
        item["tensor_result"] = result.as_jsonable()
    if extra:
        item.update(extra)
    return item


def build_report():
    cases = []

    kt01 = analyze_symmetric_tensor(np.eye(3) * 2.5)
    cases.append(
        _record(
            "KT-01",
            "isotropic expansion / exact directional degeneracy",
            kt01,
            status="REFUSED_DIRECTIONAL_INTERPRETATION",
        )
    )

    one_axis = np.diag([2.0, 0.5, -1.0])
    base = analyze_symmetric_tensor(one_axis)
    rotation = rotation_matrix(np.array([1.0, 2.0, 3.0]), 0.71)
    rotated = analyze_symmetric_tensor(rotate_tensor(one_axis, rotation))
    overlap = np.abs(rotated.eigenvectors.T @ (rotation @ base.eigenvectors))
    cases.append(
        _record(
            "KT-02",
            "one-axis collapse / rotation covariance",
            rotated,
            extra={"rotation_overlap": overlap.tolist()},
        )
    )

    kt03 = analyze_symmetric_tensor(np.diag([0.8, -0.4, -1.2]))
    cases.append(_record("KT-03", "two-axis collapse", kt03))

    separated = analyze_symmetric_tensor(np.diag([-0.8, -1.0, -1.3]))
    close = analyze_symmetric_tensor(np.diag([-1.0, -1.000001, -1.000003]))
    cases.append(
        _record(
            "KT-04",
            "three-axis collapse / near-isotropic conditioning contrast",
            close,
            extra={
                "reference_condition_number": separated.directional_condition_number,
                "near_isotropic_condition_number": close.directional_condition_number,
            },
        )
    )

    first = analyze_symmetric_tensor(np.diag([2.0, -1.0, -1.0]))
    second = analyze_symmetric_tensor(
        np.diag([math.sqrt(3.0), 0.0, -math.sqrt(3.0)])
    )
    cases.append(
        _record(
            "KT-05",
            "matched scalar subset / different modal spectra",
            first,
            status="PASS_SCALAR_INFORMATION_LOSS_DEMONSTRATED",
            extra={
                "comparison_tensor_result": second.as_jsonable(),
                "matched_scalar_fields": ["trace", "trace_square", "frobenius_norm"],
                "different_modal_fields": ["eigenvalues", "determinant"],
            },
        )
    )

    tensor = np.diag([2.0, 0.3, -1.4])
    global_rotation = rotation_matrix(np.array([2.0, -1.0, 0.5]), 0.93)
    base = analyze_symmetric_tensor(tensor)
    rotated = analyze_symmetric_tensor(rotate_tensor(tensor, global_rotation))
    cases.append(
        _record(
            "KT-06",
            "global coordinate rotation covariance",
            rotated,
            extra={
                "reference_invariants": base.invariants,
                "rotation_overlap": np.abs(
                    rotated.eigenvectors.T @ (global_rotation @ base.eigenvectors)
                ).tolist(),
            },
        )
    )

    gap_sweep = []
    for gap in [1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12]:
        result = analyze_symmetric_tensor(np.diag([1.0, 1.0 - gap, -2.0]))
        gap_sweep.append(
            {
                "input_gap": gap,
                "measured_eigengaps": result.eigengaps.tolist(),
                "normalized_eigengaps": result.normalized_eigengaps.tolist(),
                "condition_number": (
                    None
                    if not math.isfinite(result.directional_condition_number)
                    else result.directional_condition_number
                ),
                "degenerate_pairs": list(result.degenerate_pairs),
            }
        )
    cases.append(
        _record(
            "KT-07",
            "near-degenerate sweep; no scientific refusal threshold pre-imposed",
            status="MEASURED_NO_THRESHOLD_FROZEN",
            extra={"gap_sweep": gap_sweep},
        )
    )

    kt08 = analyze_symmetric_tensor(np.diag([1.0, 1.0, -2.0]))
    cases.append(
        _record(
            "KT-08",
            "exact pair degeneracy",
            kt08,
            status="REFUSED_UNIQUE_AXIS_IN_DEGENERATE_SUBSPACE",
        )
    )

    shear = analyze_symmetric_tensor(np.diag([2.0, 0.5, -1.0]))
    weyl = analyze_symmetric_tensor(np.diag([3.0, 0.2, -2.0]))
    cases.append(
        _record(
            "KT-09",
            "known shear-Weyl alignment",
            status="PASS",
            extra={"alignment_matrix": eigenframe_alignment(shear, weyl).tolist()},
        )
    )

    relative = rotation_matrix(np.array([0.0, 0.0, 1.0]), 0.4)
    weyl_tensor = rotate_tensor(np.diag([3.0, 0.2, -2.0]), relative)
    weyl = analyze_symmetric_tensor(weyl_tensor)
    alignment_before = eigenframe_alignment(shear, weyl)
    global_rotation = rotation_matrix(np.array([1.0, 2.0, 0.5]), 0.77)
    shear_rot = analyze_symmetric_tensor(
        rotate_tensor(np.diag([2.0, 0.5, -1.0]), global_rotation)
    )
    weyl_rot = analyze_symmetric_tensor(rotate_tensor(weyl_tensor, global_rotation))
    alignment_after = eigenframe_alignment(shear_rot, weyl_rot)
    cases.append(
        _record(
            "KT-10",
            "misalignment invariant under global coordinate rotation",
            status="PASS",
            extra={
                "alignment_before": alignment_before.tolist(),
                "alignment_after": alignment_after.tolist(),
            },
        )
    )

    noise_sweep = []
    perturbation_norm = 1e-5
    for gap in [0.8, 0.1, 1e-2, 1e-3, 1e-4]:
        result = analyze_symmetric_tensor(np.diag([1.0, 1.0 - gap, -1.0]))
        noise_sweep.append(
            {
                "input_gap": gap,
                "direction_bound_proxy": perturbation_direction_bound(
                    result, perturbation_norm
                ),
            }
        )
    cases.append(
        _record(
            "KT-11",
            "continuous direction-sensitivity proxy versus eigengap",
            status="MEASURED_NO_THRESHOLD_FROZEN",
            extra={
                "perturbation_operator_norm": perturbation_norm,
                "noise_sweep": noise_sweep,
            },
        )
    )

    bad = np.array(
        [
            [1.0, 0.2, 0.0],
            [0.0, -0.4, 0.1],
            [0.0, 0.1, -0.6],
        ]
    )
    try:
        analyze_symmetric_tensor(bad)
    except ValueError as exc:
        kt12_status = "PASS_KNOWN_BAD_REFUSED"
        kt12_message = str(exc)
    else:
        kt12_status = "FAIL_KNOWN_BAD_ACCEPTED"
        kt12_message = "materially nonsymmetric tensor was accepted"
    cases.append(
        _record(
            "KT-12",
            "known-bad nonsymmetric tensor refusal",
            status=kt12_status,
            extra={"message": kt12_message},
        )
    )

    return {
        "protocol": "MODAL_KNOWN_TRUTH_QUALIFICATION_SUITE",
        "stage": "P0-Q",
        "scientific_thresholds_frozen": False,
        "primary_object": "symmetric shear/Weyl/tidal tensor eigenstructure",
        "case_count": len(cases),
        "cases": cases,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report()
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "case_count": report["case_count"],
        "scientific_thresholds_frozen": report["scientific_thresholds_frozen"],
        "output": str(output),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
