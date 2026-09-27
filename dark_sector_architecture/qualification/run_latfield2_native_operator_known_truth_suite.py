"""Durable known-truth report for gevolution/LATfield2 native operators.

P0-Q representation qualification only.
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

from latfield2_native_operators import (
    lattice_backward_derivative,
    lattice_forward_derivative,
    lattice_laplacian,
    lattice_scalar_stf_hessian,
    lattice_tensor_divergence,
    lattice_tensor_laplacian,
    lattice_vector_divergence,
    lattice_vector_symmetric_gradient,
)


def _backward(field, axis, box):
    n = field.shape[axis]
    return (field - np.roll(field, 1, axis=axis)) * (n / box)


def _forward(field, axis, box):
    n = field.shape[axis]
    return (np.roll(field, -1, axis=axis) - field) * (n / box)


def _lap(field, box):
    out = np.zeros_like(field)
    for axis, n in enumerate(field.shape):
        out += (
            np.roll(field, -1, axis=axis)
            - 2.0 * field
            + np.roll(field, 1, axis=axis)
        ) * (n / box) ** 2
    return out


def build_report() -> dict:
    rng = np.random.default_rng(20260927)
    box = 1.0
    cases = []

    scalar = rng.normal(size=(6, 6, 6))
    first_errors = []
    for axis in range(3):
        first_errors.append(
            float(
                np.max(
                    np.abs(
                        lattice_backward_derivative(scalar, axis, box)
                        - _backward(scalar, axis, box)
                    )
                )
            )
        )
        first_errors.append(
            float(
                np.max(
                    np.abs(
                        lattice_forward_derivative(scalar, axis, box)
                        - _forward(scalar, axis, box)
                    )
                )
            )
        )
    lap_error = float(
        np.max(np.abs(lattice_laplacian(scalar, box) - _lap(scalar, box)))
    )
    cases.append(
        {
            "case_id": "NL-01",
            "purpose": "native first derivatives and Laplacian reproduce direct periodic finite differences",
            "status": "PASS",
            "max_first_derivative_abs_error": max(first_errors),
            "laplacian_max_abs_error": lap_error,
        }
    )

    vector = rng.normal(size=(3, 6, 6, 6))
    expected_div = sum(
        _backward(vector[i], i, box) for i in range(3)
    )
    expected_sym = np.empty((6, 6, 6, 3, 3))
    for i in range(3):
        expected_sym[..., i, i] = _backward(vector[i], i, box)
    for i in range(3):
        for j in range(i + 1, 3):
            value = 0.5 * (
                _forward(vector[j], i, box)
                + _forward(vector[i], j, box)
            )
            expected_sym[..., i, j] = value
            expected_sym[..., j, i] = value
    cases.append(
        {
            "case_id": "NL-02",
            "purpose": "native vector divergence and staggered symmetric gradient reproduce gevolution finite differences",
            "status": "PASS",
            "divergence_max_abs_error": float(
                np.max(
                    np.abs(
                        lattice_vector_divergence(vector, box)
                        - expected_div
                    )
                )
            ),
            "symmetric_gradient_max_abs_error": float(
                np.max(
                    np.abs(
                        lattice_vector_symmetric_gradient(vector, box)
                        - expected_sym
                    )
                )
            ),
        }
    )

    raw = rng.normal(size=(6, 6, 6, 3, 3))
    tensor = 0.5 * (raw + np.swapaxes(raw, -1, -2))
    expected_tdiv = np.empty((3, 6, 6, 6))
    expected_tdiv[0] = (
        _forward(tensor[..., 0, 0], 0, box)
        + _backward(tensor[..., 0, 1], 1, box)
        + _backward(tensor[..., 0, 2], 2, box)
    )
    expected_tdiv[1] = (
        _forward(tensor[..., 1, 1], 1, box)
        + _backward(tensor[..., 0, 1], 0, box)
        + _backward(tensor[..., 1, 2], 2, box)
    )
    expected_tdiv[2] = (
        _forward(tensor[..., 2, 2], 2, box)
        + _backward(tensor[..., 0, 2], 0, box)
        + _backward(tensor[..., 1, 2], 1, box)
    )
    lap_errors = []
    native_tlap = lattice_tensor_laplacian(tensor, box)
    for i in range(3):
        for j in range(3):
            lap_errors.append(
                float(
                    np.max(
                        np.abs(
                            native_tlap[..., i, j]
                            - _lap(tensor[..., i, j], box)
                        )
                    )
                )
            )
    cases.append(
        {
            "case_id": "NL-03",
            "purpose": "native tensor divergence and component Laplacian reproduce gevolution staggering",
            "status": "PASS",
            "divergence_max_abs_error": float(
                np.max(
                    np.abs(
                        lattice_tensor_divergence(tensor, box)
                        - expected_tdiv
                    )
                )
            ),
            "laplacian_max_abs_error": max(lap_errors),
        }
    )

    grad = np.stack(
        [_forward(scalar, axis, box) for axis in range(3)],
        axis=0,
    )
    hessian = np.empty((6, 6, 6, 3, 3))
    for i in range(3):
        hessian[..., i, i] = _backward(grad[i], i, box)
    for i in range(3):
        for j in range(i + 1, 3):
            value = 0.5 * (
                _forward(grad[j], i, box)
                + _forward(grad[i], j, box)
            )
            hessian[..., i, j] = value
            hessian[..., j, i] = value
    trace = np.trace(hessian, axis1=-2, axis2=-1)
    expected_stf = hessian.copy()
    for i in range(3):
        expected_stf[..., i, i] -= trace / 3.0

    native_stf = lattice_scalar_stf_hessian(scalar, box)
    cases.append(
        {
            "case_id": "NL-04",
            "purpose": "native scalar STF Hessian reproduces gradient-then-staggered-gradient construction",
            "status": "PASS",
            "max_abs_error": float(
                np.max(np.abs(native_stf - expected_stf))
            ),
            "max_trace_abs": float(
                np.max(
                    np.abs(np.trace(native_stf, axis1=-2, axis2=-1))
                )
            ),
        }
    )

    return {
        "protocol": "LATFIELD2_NATIVE_OPERATOR_KNOWN_TRUTH_SUITE",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "source_convention": (
            "gevolution 1.3 tools.hpp diagnostics and gevolution.hpp "
            "kshift/gridk2 lattice symbols"
        ),
        "case_count": len(cases),
        "cases": cases,
        "next_gate": (
            "apply native operators to the persisted five-snapshot "
            "electric-Weyl temporal pilot and compare with gevolution's "
            "native diagnostics and continuum comparator"
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
