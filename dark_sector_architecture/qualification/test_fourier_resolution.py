from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from fourier_resolution import (
    phase_overlap_report,
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
