from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from gevolution_velocity_operators import (
    centered_derivative_periodic,
    velocity_divergence_centered,
    velocity_gradient_centered,
    velocity_shear_centered,
    velocity_vorticity_centered,
)


ATOL = 2e-11
RTOL = 2e-11


def _direct_centered(field, axis, box):
    n = field.shape[axis]
    return (
        np.roll(field, -1, axis=axis) - np.roll(field, 1, axis=axis)
    ) * (n / (2.0 * box))


def test_gv01_centered_derivative_matches_direct_periodic_difference():
    rng = np.random.default_rng(101)
    field = rng.normal(size=(8, 7, 6))
    box = 2.75
    for axis in range(3):
        np.testing.assert_allclose(
            centered_derivative_periodic(field, axis, box),
            _direct_centered(field, axis, box),
            atol=ATOL,
            rtol=RTOL,
        )


def test_gv02_gradient_divergence_and_shear_match_direct_centered_formulas():
    rng = np.random.default_rng(202)
    velocity = rng.normal(size=(3, 8, 8, 8))
    box = 1.0

    grad_expected = np.empty((8, 8, 8, 3, 3))
    for i in range(3):
        for j in range(3):
            grad_expected[..., i, j] = _direct_centered(
                velocity[j], i, box
            )

    grad = velocity_gradient_centered(velocity, box)
    np.testing.assert_allclose(grad, grad_expected, atol=ATOL, rtol=RTOL)

    theta_expected = np.trace(grad_expected, axis1=-2, axis2=-1)
    theta = velocity_divergence_centered(velocity, box)
    np.testing.assert_allclose(theta, theta_expected, atol=ATOL, rtol=RTOL)

    sym = 0.5 * (grad_expected + np.swapaxes(grad_expected, -1, -2))
    shear_expected = np.array(sym, copy=True)
    for i in range(3):
        shear_expected[..., i, i] -= theta_expected / 3.0
    shear, theta2 = velocity_shear_centered(velocity, box)
    np.testing.assert_allclose(shear, shear_expected, atol=ATOL, rtol=RTOL)
    np.testing.assert_allclose(theta2, theta_expected, atol=ATOL, rtol=RTOL)
    np.testing.assert_allclose(
        np.trace(shear, axis1=-2, axis2=-1), 0.0, atol=ATOL, rtol=0.0
    )


def test_gv03_vorticity_matches_direct_centered_curl():
    rng = np.random.default_rng(303)
    velocity = rng.normal(size=(3, 8, 8, 8))
    box = 1.0
    omega_expected = np.stack(
        [
            _direct_centered(velocity[2], 1, box)
            - _direct_centered(velocity[1], 2, box),
            _direct_centered(velocity[0], 2, box)
            - _direct_centered(velocity[2], 0, box),
            _direct_centered(velocity[1], 0, box)
            - _direct_centered(velocity[0], 1, box),
        ],
        axis=0,
    )
    np.testing.assert_allclose(
        velocity_vorticity_centered(velocity, box),
        omega_expected,
        atol=ATOL,
        rtol=RTOL,
    )


def test_gv04_fourier_divergence_matches_gevolution_projectFTtheta_symbol():
    rng = np.random.default_rng(404)
    velocity = rng.normal(size=(3, 8, 8, 8))
    n = 8
    box = 1.0
    theta = velocity_divergence_centered(velocity, box)

    index = np.arange(n, dtype=float)
    gridk = n * np.sin(2.0 * np.pi * index / n)
    kx, ky, kz = np.meshgrid(gridk, gridk, gridk, indexing='ij', sparse=True)
    spectra = [np.fft.fftn(velocity[i]) for i in range(3)]
    expected_ft = 1j * (
        kx * spectra[0] + ky * spectra[1] + kz * spectra[2]
    )
    np.testing.assert_allclose(
        np.fft.fftn(theta), expected_ft, atol=2e-9, rtol=2e-11
    )


def test_gv05_fourier_vorticity_matches_gevolution_centered_symbol():
    rng = np.random.default_rng(505)
    velocity = rng.normal(size=(3, 8, 8, 8))
    n = 8
    box = 1.0
    omega = velocity_vorticity_centered(velocity, box)

    index = np.arange(n, dtype=float)
    gridk = n * np.sin(2.0 * np.pi * index / n)
    kx, ky, kz = np.meshgrid(gridk, gridk, gridk, indexing='ij', sparse=True)
    spectra = [np.fft.fftn(velocity[i]) for i in range(3)]
    expected = [
        1j * (ky * spectra[2] - kz * spectra[1]),
        1j * (kz * spectra[0] - kx * spectra[2]),
        1j * (kx * spectra[1] - ky * spectra[0]),
    ]
    for i in range(3):
        np.testing.assert_allclose(
            np.fft.fftn(omega[i]), expected[i], atol=2e-9, rtol=2e-11
        )


def test_gv06_irrotational_periodic_gradient_has_zero_discrete_vorticity():
    n = 12
    x = np.arange(n) / n
    xx, yy, zz = np.meshgrid(x, x, x, indexing='ij')
    potential = (
        np.cos(2.0 * np.pi * xx)
        + 0.4 * np.sin(4.0 * np.pi * yy)
        + 0.2 * np.cos(2.0 * np.pi * (xx + zz))
    )
    velocity = np.stack(
        [centered_derivative_periodic(potential, i, 1.0) for i in range(3)],
        axis=0,
    )
    omega = velocity_vorticity_centered(velocity, 1.0)
    np.testing.assert_allclose(omega, 0.0, atol=2e-10, rtol=0.0)


def test_gv07_staggered_and_centered_symbols_are_not_silently_interchangeable():
    n = 16
    x = np.arange(n) / n
    field = np.sin(2.0 * np.pi * 5.0 * x)
    cube = field[:, None, None] * np.ones((1, n, n))
    centered = centered_derivative_periodic(cube, 0, 1.0)
    backward = (cube - np.roll(cube, 1, axis=0)) * n
    assert np.sqrt(np.mean((centered - backward) ** 2)) > 1e-3
