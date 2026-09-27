from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from weak_field_tensors import (
    spectral_hessian_periodic,
    tensor_symmetry_residual,
    tensor_trace_residual,
    velocity_shear_tensor,
    weak_field_tidal_tensor,
)


ATOL = 1e-10
RTOL = 1e-10


def _grid(n: int, boxsize: float):
    x = np.arange(n) * (boxsize / n)
    return np.meshgrid(x, x, x, indexing="ij")


def test_constant_scalar_field_has_zero_hessian_and_tidal_tensor():
    phi = np.ones((8, 8, 8))
    hessian = spectral_hessian_periodic(phi, 10.0)
    tidal = weak_field_tidal_tensor(phi, 10.0)

    np.testing.assert_allclose(hessian, 0.0, atol=ATOL)
    np.testing.assert_allclose(tidal, 0.0, atol=ATOL)


def test_single_mode_scalar_field_recovers_analytic_tidal_tensor():
    n = 16
    boxsize = 8.0
    mode = 2
    x, _, _ = _grid(n, boxsize)
    k = 2.0 * np.pi * mode / boxsize
    phi = np.cos(k * x)

    tidal = weak_field_tidal_tensor(phi, boxsize)
    factor = -(k * k) * np.cos(k * x)

    expected = np.zeros(phi.shape + (3, 3))
    expected[..., 0, 0] = (2.0 / 3.0) * factor
    expected[..., 1, 1] = -(1.0 / 3.0) * factor
    expected[..., 2, 2] = -(1.0 / 3.0) * factor

    np.testing.assert_allclose(tidal, expected, atol=ATOL, rtol=RTOL)
    assert tensor_symmetry_residual(tidal) < ATOL
    assert tensor_trace_residual(tidal) < ATOL


def test_one_dimensional_velocity_mode_recovers_analytic_shear_and_divergence():
    n = 16
    boxsize = 8.0
    mode = 2
    x, _, _ = _grid(n, boxsize)
    k = 2.0 * np.pi * mode / boxsize

    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * x)

    shear, theta = velocity_shear_tensor(velocity, boxsize)
    expected_theta = k * np.cos(k * x)

    np.testing.assert_allclose(theta, expected_theta, atol=ATOL, rtol=RTOL)
    np.testing.assert_allclose(
        shear[..., 0, 0], (2.0 / 3.0) * expected_theta, atol=ATOL, rtol=RTOL
    )
    np.testing.assert_allclose(
        shear[..., 1, 1], -(1.0 / 3.0) * expected_theta, atol=ATOL, rtol=RTOL
    )
    np.testing.assert_allclose(
        shear[..., 2, 2], -(1.0 / 3.0) * expected_theta, atol=ATOL, rtol=RTOL
    )
    np.testing.assert_allclose(shear[..., 0, 1], 0.0, atol=ATOL)
    np.testing.assert_allclose(shear[..., 0, 2], 0.0, atol=ATOL)
    np.testing.assert_allclose(shear[..., 1, 2], 0.0, atol=ATOL)
    assert tensor_symmetry_residual(shear) < ATOL
    assert tensor_trace_residual(shear) < ATOL


def test_off_diagonal_shear_mode_recovers_known_cross_component():
    n = 16
    boxsize = 8.0
    mode = 1
    _, y, _ = _grid(n, boxsize)
    k = 2.0 * np.pi * mode / boxsize

    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * y)

    shear, theta = velocity_shear_tensor(velocity, boxsize)
    expected = 0.5 * k * np.cos(k * y)

    np.testing.assert_allclose(theta, 0.0, atol=ATOL)
    np.testing.assert_allclose(shear[..., 0, 1], expected, atol=ATOL, rtol=RTOL)
    np.testing.assert_allclose(shear[..., 1, 0], expected, atol=ATOL, rtol=RTOL)
    np.testing.assert_allclose(shear[..., 0, 0], 0.0, atol=ATOL)
    np.testing.assert_allclose(shear[..., 1, 1], 0.0, atol=ATOL)
    np.testing.assert_allclose(shear[..., 2, 2], 0.0, atol=ATOL)


def test_invalid_inputs_fail_closed():
    try:
        weak_field_tidal_tensor(np.ones((4, 4)), 10.0)
    except ValueError as exc:
        assert "shape" in str(exc)
    else:
        raise AssertionError("2D scalar field was accepted")

    bad_velocity = np.zeros((2, 4, 4, 4))
    try:
        velocity_shear_tensor(bad_velocity, 10.0)
    except ValueError as exc:
        assert "shape" in str(exc)
    else:
        raise AssertionError("bad velocity shape was accepted")

    try:
        weak_field_tidal_tensor(np.ones((4, 4, 4)), 0.0)
    except ValueError as exc:
        assert "boxsize" in str(exc)
    else:
        raise AssertionError("nonpositive boxsize was accepted")
