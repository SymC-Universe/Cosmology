from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from fourier_resolution import (
    active_overlap_modes,
    phase_overlap_report,
    spectral_project_scalar_to_modes,
    spectral_project_tensor_to_modes,
    spectral_project_vector_to_modes,
    spectral_restrict_to_grid,
    spectral_restrict_vector_to_grid,
)


def _analytic_field(n: int, box: float) -> np.ndarray:
    x = np.arange(n) * box / n
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi / box
    return (
        1.2 * np.cos(k * xx + 0.37)
        + 0.8 * np.sin(2.0 * k * yy - 0.21)
        + 0.4 * np.cos(k * (xx + zz) + 0.73)
    )


def test_same_continuous_modes_have_unit_phase_coherence():
    low = _analytic_field(8, 64.0)
    high = _analytic_field(16, 64.0)
    report = phase_overlap_report(low, high)

    assert report["valid_nonzero_mode_count"] > 0
    assert report["circular_phase_coherence"] > 1.0 - 1e-12
    assert report["weighted_complex_coherence"] > 1.0 - 1e-12
    assert report["absolute_phase_difference_radians"]["max"] < 1e-12


def test_spectral_restriction_recovers_shared_bandlimited_field():
    low = _analytic_field(8, 64.0)
    high = _analytic_field(16, 64.0)
    restricted = spectral_restrict_to_grid(high, 8)
    np.testing.assert_allclose(restricted, low, atol=1e-12, rtol=1e-12)


def test_vector_spectral_restriction_componentwise():
    low_scalar = _analytic_field(8, 64.0)
    high_scalar = _analytic_field(16, 64.0)
    low = np.stack([low_scalar, 2 * low_scalar, -0.5 * low_scalar], axis=0)
    high = np.stack([high_scalar, 2 * high_scalar, -0.5 * high_scalar], axis=0)

    restricted = spectral_restrict_vector_to_grid(high, 8)
    np.testing.assert_allclose(restricted, low, atol=1e-12, rtol=1e-12)



def test_explicit_mode_projection_recovers_same_common_support():
    low = _analytic_field(8, 64.0)
    high = _analytic_field(16, 64.0)
    modes = active_overlap_modes(8)

    low_projected = spectral_project_scalar_to_modes(low, 8, modes)
    high_projected = spectral_project_scalar_to_modes(high, 8, modes)
    np.testing.assert_allclose(
        high_projected, low_projected, atol=1e-12, rtol=1e-12
    )


def test_explicit_vector_and_tensor_projection_are_componentwise():
    low_scalar = _analytic_field(8, 64.0)
    high_scalar = _analytic_field(16, 64.0)
    modes = active_overlap_modes(8)

    low_vector = np.stack(
        [low_scalar, 2.0 * low_scalar, -0.5 * low_scalar], axis=0
    )
    high_vector = np.stack(
        [high_scalar, 2.0 * high_scalar, -0.5 * high_scalar], axis=0
    )

    low_v = spectral_project_vector_to_modes(low_vector, 8, modes)
    high_v = spectral_project_vector_to_modes(high_vector, 8, modes)
    np.testing.assert_allclose(high_v, low_v, atol=1e-12, rtol=1e-12)

    low_tensor = np.zeros((8, 8, 8, 3, 3))
    high_tensor = np.zeros((16, 16, 16, 3, 3))
    for i in range(3):
        for j in range(3):
            factor = (i + 1) * (j + 2) / 7.0
            low_tensor[..., i, j] = factor * low_scalar
            high_tensor[..., i, j] = factor * high_scalar

    low_t = spectral_project_tensor_to_modes(low_tensor, 8, modes)
    high_t = spectral_project_tensor_to_modes(high_tensor, 8, modes)
    np.testing.assert_allclose(high_t, low_t, atol=1e-12, rtol=1e-12)
