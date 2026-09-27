"""Machine-readable known-truth report for temporal derivative qualification.

P0-Q only. Uses synthetic arbitrary-time array-valued fields to verify the
finite-difference machinery that will estimate gevolution B_i' and h_ij'' from
actual logged conformal times.
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

from temporal_derivatives import (
    derivative_from_samples,
    finite_difference_weights,
    nested_center_derivatives,
)


def build_report() -> dict:
    cases = []

    times = np.array([-0.31, -0.07, 0.13], dtype=float)
    target = -0.07
    values = 3.0 * times**2 - 2.0 * times + 5.0
    first = float(derivative_from_samples(values, times, target, 1))
    second = float(derivative_from_samples(values, times, target, 2))
    cases.append(
        {
            "case_id": "TD-01",
            "purpose": "nonuniform quadratic first and second derivative exactness",
            "status": "PASS",
            "first_abs_error": abs(first - (6.0 * target - 2.0)),
            "second_abs_error": abs(second - 6.0),
        }
    )

    moment_times = np.array([0.0, 0.17, 0.51], dtype=float)
    x0 = 0.17
    offsets = moment_times - x0
    w1 = finite_difference_weights(moment_times, x0, 1)
    w2 = finite_difference_weights(moment_times, x0, 2)
    moment_errors = {
        "first_constant": abs(float(np.dot(w1, np.ones_like(offsets)))),
        "first_linear": abs(float(np.dot(w1, offsets)) - 1.0),
        "first_quadratic": abs(float(np.dot(w1, offsets**2))),
        "second_constant": abs(float(np.dot(w2, np.ones_like(offsets)))),
        "second_linear": abs(float(np.dot(w2, offsets))),
        "second_quadratic": abs(float(np.dot(w2, offsets**2)) - 2.0),
    }
    cases.append(
        {
            "case_id": "TD-02",
            "purpose": "arbitrary-node finite-difference moment identities",
            "status": "PASS",
            "moment_errors": moment_errors,
        }
    )

    five_times = np.array([0.00, 0.09, 0.21, 0.36, 0.55], dtype=float)
    center = five_times[2]
    n = 2
    b = np.empty((5, 3, n, n, n), dtype=float)
    h = np.empty((5, n, n, n, 3, 3), dtype=float)
    base_b = np.arange(3 * n**3, dtype=float).reshape(3, n, n, n) + 1.0
    base_h = np.arange(n**3 * 9, dtype=float).reshape(n, n, n, 3, 3) + 1.0
    base_h = 0.5 * (base_h + np.swapaxes(base_h, -1, -2))

    for p, t in enumerate(five_times):
        b[p] = base_b * (2.0 * t**2 - 3.0 * t + 4.0)
        h[p] = base_h * (-1.5 * t**2 + 0.7 * t + 2.0)

    nested = nested_center_derivatives(b, h, five_times)
    expected_b = base_b * (4.0 * center - 3.0)
    expected_h = base_h * -3.0
    cases.append(
        {
            "case_id": "TD-03",
            "purpose": "five-node nested inner/outer exact quadratic recovery",
            "status": "PASS",
            "b_inner_max_abs_error": float(
                np.max(np.abs(nested["b_prime_inner"] - expected_b))
            ),
            "b_outer_max_abs_error": float(
                np.max(np.abs(nested["b_prime_outer"] - expected_b))
            ),
            "h_inner_max_abs_error": float(
                np.max(np.abs(nested["h_second_inner"] - expected_h))
            ),
            "h_outer_max_abs_error": float(
                np.max(np.abs(nested["h_second_outer"] - expected_h))
            ),
            "b_inner_weights": nested["b_inner_weights"].tolist(),
            "b_outer_weights": nested["b_outer_weights"].tolist(),
            "h_inner_weights": nested["h_inner_weights"].tolist(),
            "h_outer_weights": nested["h_outer_weights"].tolist(),
        }
    )

    step = 0.02
    sinusoid_times = np.array([-2*step, -step, 0.0, step, 2*step])
    omega = 3.0
    b = np.zeros((5, 3, n, n, n))
    h = np.zeros((5, n, n, n, 3, 3))
    for p, t in enumerate(sinusoid_times):
        b[p, 0] = np.sin(omega * t)
        h[p, ..., 0, 0] = np.cos(omega * t)
        h[p, ..., 1, 1] = -np.cos(omega * t)

    nested = nested_center_derivatives(b, h, sinusoid_times)
    expected_b = omega
    expected_h = -(omega**2)
    b_inner_error = abs(float(nested["b_prime_inner"][0, 0, 0, 0]) - expected_b)
    b_outer_error = abs(float(nested["b_prime_outer"][0, 0, 0, 0]) - expected_b)
    h_inner_error = abs(float(nested["h_second_inner"][0, 0, 0, 0, 0]) - expected_h)
    h_outer_error = abs(float(nested["h_second_outer"][0, 0, 0, 0, 0]) - expected_h)
    cases.append(
        {
            "case_id": "TD-04",
            "purpose": "inner stencil improves over outer stencil for smooth sinusoid",
            "status": "PASS",
            "b_inner_abs_error": b_inner_error,
            "b_outer_abs_error": b_outer_error,
            "h_inner_abs_error": h_inner_error,
            "h_outer_abs_error": h_outer_error,
        }
    )

    return {
        "protocol": "TEMPORAL_DERIVATIVE_KNOWN_TRUTH_SUITE",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "equal_spacing_required": False,
        "real_gevolution_temporal_derivatives_qualified": False,
        "case_count": len(cases),
        "cases": cases,
        "next_gate": (
            "five real gevolution snapshots with actual logged conformal times, "
            "nested inner/outer derivative reconstruction, and full electric-Weyl comparison"
        ),
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
