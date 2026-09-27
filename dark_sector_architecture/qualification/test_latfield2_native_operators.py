from __future__ import annotations

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


ATOL = 5e-11
RTOL = 5e-11


def _backward(field, axis, boxsize):
    n = field.shape[axis]
    return (field - np.roll(field, 1, axis=axis)) * (n / boxsize)


def _forward(field, axis, boxsize):
    n = field.shape[axis]
    return (np.roll(field, -1, axis=axis) - field) * (n / boxsize)


def _laplacian(field, boxsize):
    out = np.zeros_like(field, dtype=float)
    for axis, n in enumerate(field.shape):
        scale2 = (n / boxsize) ** 2
        out += (
            np.roll(field, -1, axis=axis)
            - 2.0 * field
            + np.roll(field, 1, axis=axis)
        ) * scale2
    return out


def test_forward_backward_and_laplacian_match_direct_periodic_differences():
    rng = np.random.default_rng(1234)
    field = rng.normal(size=(7, 6, 5))
    box = 2.5

    for axis in range(3):
        np.testing.assert_allclose(
            lattice_backward_derivative(field, axis, box),
            _backward(field, axis, box),
            atol=ATOL,
            rtol=RTOL,
        )
        np.testing.assert_allclose(
            lattice_forward_derivative(field, axis, box),
            _forward(field, axis, box),
            atol=ATOL,
            rtol=RTOL,
        )

    np.testing.assert_allclose(
        lattice_laplacian(field, box),
        _laplacian(field, box),
        atol=ATOL,
        rtol=RTOL,
    )


def test_vector_divergence_matches_gevolution_tools_formula():
    rng = np.random.default_rng(2)
    vector = rng.normal(size=(3, 6, 6, 6))
    box = 1.0

    expected = (
        _backward(vector[0], 0, box)
        + _backward(vector[1], 1, box)
        + _backward(vector[2], 2, box)
    )

    np.testing.assert_allclose(
        lattice_vector_divergence(vector, box),
        expected,
        atol=ATOL,
        rtol=RTOL,
    )


def test_tensor_divergence_matches_gevolution_tools_formula():
    rng = np.random.default_rng(3)
    raw = rng.normal(size=(6, 6, 6, 3, 3))
    tensor = 0.5 * (raw + np.swapaxes(raw, -1, -2))
    box = 1.0

    expected = np.empty((3, 6, 6, 6), dtype=float)
    expected[0] = (
        _forward(tensor[..., 0, 0], 0, box)
        + _backward(tensor[..., 0, 1], 1, box)
        + _backward(tensor[..., 0, 2], 2, box)
    )
    expected[1] = (
        _forward(tensor[..., 1, 1], 1, box)
        + _backward(tensor[..., 0, 1], 0, box)
        + _backward(tensor[..., 1, 2], 2, box)
    )
    expected[2] = (
        _forward(tensor[..., 2, 2], 2, box)
        + _backward(tensor[..., 0, 2], 0, box)
        + _backward(tensor[..., 1, 2], 1, box)
    )

    np.testing.assert_allclose(
        lattice_tensor_divergence(tensor, box),
        expected,
        atol=ATOL,
        rtol=RTOL,
    )


def test_vector_symmetric_gradient_matches_staggered_direct_formula():
    rng = np.random.default_rng(4)
    vector = rng.normal(size=(3, 6, 6, 6))
    box = 1.0

    expected = np.empty((6, 6, 6, 3, 3), dtype=float)
    for i in range(3):
        expected[..., i, i] = _backward(vector[i], i, box)
    for i in range(3):
        for j in range(i + 1, 3):
            value = 0.5 * (
                _forward(vector[j], i, box)
                + _forward(vector[i], j, box)
            )
            expected[..., i, j] = value
            expected[..., j, i] = value

    np.testing.assert_allclose(
        lattice_vector_symmetric_gradient(vector, box),
        expected,
        atol=ATOL,
        rtol=RTOL,
    )


def test_scalar_stf_hessian_matches_gradient_then_symmetric_gradient():
    rng = np.random.default_rng(5)
    field = rng.normal(size=(6, 6, 6))
    box = 1.0

    grad = np.stack(
        [_forward(field, axis, box) for axis in range(3)],
        axis=0,
    )
    hessian = np.empty((6, 6, 6, 3, 3), dtype=float)

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
    expected = np.array(hessian, copy=True)
    for i in range(3):
        expected[..., i, i] -= trace / 3.0

    actual = lattice_scalar_stf_hessian(field, box)
    np.testing.assert_allclose(actual, expected, atol=ATOL, rtol=RTOL)
    np.testing.assert_allclose(
        np.trace(actual, axis1=-2, axis2=-1),
        0.0,
        atol=ATOL,
        rtol=0.0,
    )


def test_tensor_laplacian_is_componentwise_native_laplacian():
    rng = np.random.default_rng(6)
    raw = rng.normal(size=(5, 5, 5, 3, 3))
    tensor = 0.5 * (raw + np.swapaxes(raw, -1, -2))
    box = 1.0

    actual = lattice_tensor_laplacian(tensor, box)
    for i in range(3):
        for j in range(3):
            np.testing.assert_allclose(
                actual[..., i, j],
                _laplacian(tensor[..., i, j], box),
                atol=ATOL,
                rtol=RTOL,
            )
