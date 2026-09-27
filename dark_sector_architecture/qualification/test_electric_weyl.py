from __future__ import annotations

import pathlib
import sys

import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from electric_weyl import (
    electric_weyl_conformal_sectors,
    electric_weyl_conformal_tensor,
    electric_weyl_physical_tensor,
    tensor_divergence_periodic,
    vector_divergence_periodic,
)
from weak_field_tensors import scalar_weyl_shape_tensor


ATOL = 2e-10
RTOL = 2e-10


def _grid(n: int, boxsize: float):
    x = np.arange(n) * boxsize / n
    return np.meshgrid(x, x, x, indexing="ij")


def _zeros_vector(n: int):
    return np.zeros((3, n, n, n), dtype=float)


def _zeros_tensor(n: int):
    return np.zeros((n, n, n, 3, 3), dtype=float)


def test_scalar_limit_matches_existing_scalar_weyl_shape():
    n = 16
    box = 8.0
    x, y, _ = _grid(n, box)
    k = 2.0 * np.pi / box

    phi = np.cos(k * x) + 0.2 * np.cos(2.0 * k * y)
    chi = 0.1 * np.cos(k * x)

    total = electric_weyl_conformal_tensor(
        phi,
        chi,
        _zeros_vector(n),
        _zeros_tensor(n),
        _zeros_tensor(n),
        box,
    )
    expected = scalar_weyl_shape_tensor(phi, chi, box)

    np.testing.assert_allclose(total, expected, atol=ATOL, rtol=RTOL)


def test_pure_transverse_vector_mode_has_expected_xy_tide():
    n = 16
    box = 8.0
    x, _, _ = _grid(n, box)
    k = 2.0 * np.pi / box

    b_prime = _zeros_vector(n)
    b_prime[1] = np.sin(k * x)

    zeros = np.zeros((n, n, n))
    sectors = electric_weyl_conformal_sectors(
        zeros,
        zeros,
        b_prime,
        _zeros_tensor(n),
        _zeros_tensor(n),
        box,
    )

    expected_xy = -0.25 * k * np.cos(k * x)

    np.testing.assert_allclose(
        sectors["vector"][..., 0, 1], expected_xy, atol=ATOL, rtol=RTOL
    )
    np.testing.assert_allclose(
        sectors["vector"][..., 1, 0], expected_xy, atol=ATOL, rtol=RTOL
    )
    np.testing.assert_allclose(
        sectors["vector"][..., 0, 0], 0.0, atol=ATOL
    )
    np.testing.assert_allclose(
        sectors["vector"][..., 1, 1], 0.0, atol=ATOL
    )
    np.testing.assert_allclose(
        sectors["vector"][..., 2, 2], 0.0, atol=ATOL
    )
    np.testing.assert_allclose(
        vector_divergence_periodic(b_prime, box), 0.0, atol=ATOL
    )


def test_pure_tt_vacuum_wave_reduces_to_minus_half_h_second():
    n = 16
    box = 8.0
    _, _, z = _grid(n, box)
    k = 2.0 * np.pi / box

    h = _zeros_tensor(n)
    amplitude = np.cos(k * z)
    h[..., 0, 0] = amplitude
    h[..., 1, 1] = -amplitude

    # For h = cos(k z - k tau), evaluated at tau=0:
    # h'' = -k^2 h and Laplacian h = -k^2 h.
    h_second = -(k * k) * h

    zeros = np.zeros((n, n, n))
    sectors = electric_weyl_conformal_sectors(
        zeros,
        zeros,
        _zeros_vector(n),
        h,
        h_second,
        box,
    )

    expected = 0.5 * (k * k) * h
    np.testing.assert_allclose(
        sectors["tensor"], expected, atol=ATOL, rtol=RTOL
    )
    np.testing.assert_allclose(
        sectors["tensor"], -0.5 * h_second, atol=ATOL, rtol=RTOL
    )
    np.testing.assert_allclose(
        tensor_divergence_periodic(h, box), 0.0, atol=ATOL
    )


def test_mixed_sectors_superpose_exactly():
    n = 16
    box = 8.0
    x, y, z = _grid(n, box)
    k = 2.0 * np.pi / box

    phi = 0.3 * np.cos(k * x)
    chi = 0.05 * np.cos(k * y)

    b_prime = _zeros_vector(n)
    b_prime[1] = 0.2 * np.sin(k * x)

    h = _zeros_tensor(n)
    amp = 0.1 * np.cos(k * z)
    h[..., 0, 0] = amp
    h[..., 1, 1] = -amp
    h_second = -(k * k) * h

    sectors = electric_weyl_conformal_sectors(
        phi, chi, b_prime, h, h_second, box
    )

    np.testing.assert_allclose(
        sectors["total"],
        sectors["scalar"] + sectors["vector"] + sectors["tensor"],
        atol=ATOL,
        rtol=RTOL,
    )


def test_physical_tensor_has_a_minus_two_scaling():
    n = 8
    box = 8.0
    x, _, _ = _grid(n, box)
    k = 2.0 * np.pi / box
    phi = np.cos(k * x)
    chi = np.zeros_like(phi)

    conformal = electric_weyl_conformal_tensor(
        phi,
        chi,
        _zeros_vector(n),
        _zeros_tensor(n),
        _zeros_tensor(n),
        box,
    )
    physical = electric_weyl_physical_tensor(
        phi,
        chi,
        _zeros_vector(n),
        _zeros_tensor(n),
        _zeros_tensor(n),
        box,
        scale_factor=0.25,
    )
    np.testing.assert_allclose(physical, 16.0 * conformal, atol=ATOL, rtol=RTOL)


def test_full_result_is_symmetric_and_trace_free():
    n = 8
    box = 8.0
    x, y, z = _grid(n, box)
    k = 2.0 * np.pi / box

    phi = np.cos(k * x)
    chi = 0.03 * np.sin(k * y)
    b_prime = _zeros_vector(n)
    b_prime[1] = 0.02 * np.sin(k * x)

    h = _zeros_tensor(n)
    h[..., 0, 0] = 0.01 * np.cos(k * z)
    h[..., 1, 1] = -h[..., 0, 0]
    h_second = -(k * k) * h

    total = electric_weyl_conformal_tensor(
        phi, chi, b_prime, h, h_second, box
    )

    np.testing.assert_allclose(
        total, np.swapaxes(total, -1, -2), atol=ATOL
    )
    np.testing.assert_allclose(
        np.trace(total, axis1=-2, axis2=-1), 0.0, atol=ATOL
    )


def test_invalid_scale_factor_refuses():
    n = 4
    zeros = np.zeros((n, n, n))
    with pytest.raises(ValueError, match="scale_factor"):
        electric_weyl_physical_tensor(
            zeros,
            zeros,
            _zeros_vector(n),
            _zeros_tensor(n),
            _zeros_tensor(n),
            8.0,
            scale_factor=0.0,
        )
