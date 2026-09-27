from __future__ import annotations

import pathlib
import sys

import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from temporal_derivatives import (
    derivative_from_samples,
    finite_difference_weights,
    nested_center_derivatives,
    relative_rms_difference,
)


def test_nonuniform_quadratic_first_and_second_derivatives_are_exact():
    times = np.array([-0.31, -0.07, 0.13], dtype=float)
    target = -0.07

    # f(t) = 3 t^2 - 2 t + 5
    values = 3.0 * times**2 - 2.0 * times + 5.0
    first = derivative_from_samples(values, times, target, 1)
    second = derivative_from_samples(values, times, target, 2)

    expected_first = 6.0 * target - 2.0
    expected_second = 6.0

    assert first == pytest.approx(expected_first, abs=1e-13)
    assert second == pytest.approx(expected_second, abs=1e-13)


def test_weights_reproduce_polynomial_moments_on_nonuniform_nodes():
    times = np.array([0.0, 0.17, 0.51], dtype=float)
    target = 0.17

    w1 = finite_difference_weights(times, target, 1)
    w2 = finite_difference_weights(times, target, 2)

    offsets = times - target
    assert np.dot(w1, np.ones_like(offsets)) == pytest.approx(0.0, abs=1e-13)
    assert np.dot(w1, offsets) == pytest.approx(1.0, abs=1e-13)
    assert np.dot(w1, offsets**2) == pytest.approx(0.0, abs=1e-13)

    assert np.dot(w2, np.ones_like(offsets)) == pytest.approx(0.0, abs=1e-13)
    assert np.dot(w2, offsets) == pytest.approx(0.0, abs=1e-13)
    assert np.dot(w2, offsets**2) == pytest.approx(2.0, abs=1e-13)


def test_nested_center_derivatives_recover_quadratic_tensor_series_exactly():
    times = np.array([0.00, 0.09, 0.21, 0.36, 0.55], dtype=float)
    center = times[2]

    n = 2
    b = np.empty((5, 3, n, n, n), dtype=float)
    h = np.empty((5, n, n, n, 3, 3), dtype=float)

    base_b = np.arange(3 * n**3, dtype=float).reshape(3, n, n, n) + 1.0
    base_h = np.arange(n**3 * 9, dtype=float).reshape(n, n, n, 3, 3) + 1.0
    base_h = 0.5 * (base_h + np.swapaxes(base_h, -1, -2))

    for p, t in enumerate(times):
        b[p] = base_b * (2.0 * t**2 - 3.0 * t + 4.0)
        h[p] = base_h * (-1.5 * t**2 + 0.7 * t + 2.0)

    result = nested_center_derivatives(b, h, times)

    expected_b_prime = base_b * (4.0 * center - 3.0)
    expected_h_second = base_h * (-3.0)

    np.testing.assert_allclose(result["b_prime_inner"], expected_b_prime, atol=1e-12)
    np.testing.assert_allclose(result["b_prime_outer"], expected_b_prime, atol=1e-12)
    np.testing.assert_allclose(result["h_second_inner"], expected_h_second, atol=1e-12)
    np.testing.assert_allclose(result["h_second_outer"], expected_h_second, atol=1e-12)


def test_inner_sinusoid_stencil_is_more_accurate_than_outer_for_small_spacing():
    # Equal spacing here is only a known-truth construction. The production
    # algorithm supports arbitrary actual conformal times.
    h = 0.02
    times = np.array([-2*h, -h, 0.0, h, 2*h], dtype=float)
    omega = 3.0

    n = 2
    b = np.zeros((5, 3, n, n, n), dtype=float)
    tensor = np.zeros((5, n, n, n, 3, 3), dtype=float)

    for p, t in enumerate(times):
        b[p, 0] = np.sin(omega * t)
        tensor[p, ..., 0, 0] = np.cos(omega * t)
        tensor[p, ..., 1, 1] = -np.cos(omega * t)

    result = nested_center_derivatives(b, tensor, times)

    expected_b_prime = omega
    expected_h_second_xx = -(omega**2)

    inner_b_error = abs(result["b_prime_inner"][0, 0, 0, 0] - expected_b_prime)
    outer_b_error = abs(result["b_prime_outer"][0, 0, 0, 0] - expected_b_prime)

    inner_h_error = abs(
        result["h_second_inner"][0, 0, 0, 0, 0] - expected_h_second_xx
    )
    outer_h_error = abs(
        result["h_second_outer"][0, 0, 0, 0, 0] - expected_h_second_xx
    )

    assert inner_b_error < outer_b_error
    assert inner_h_error < outer_h_error


def test_relative_rms_difference_handles_zero_reference_without_invention():
    a = np.ones((4,))
    b = np.zeros((4,))
    assert relative_rms_difference(a, b) is None

    ref = np.ones((4,)) * 2.0
    value = relative_rms_difference(a, b, reference=ref)
    assert value == pytest.approx(0.5)


def test_duplicate_and_nonmonotonic_times_refuse():
    with pytest.raises(ValueError, match="distinct"):
        finite_difference_weights(np.array([0.0, 0.0, 0.1]), 0.0, 1)

    b = np.zeros((5, 3, 2, 2, 2))
    h = np.zeros((5, 2, 2, 2, 3, 3))

    with pytest.raises(ValueError, match="strictly increasing"):
        nested_center_derivatives(
            b,
            h,
            np.array([0.0, 0.2, 0.1, 0.3, 0.4]),
        )


def test_shape_mismatch_refuses():
    times = np.linspace(0.0, 0.4, 5)
    b = np.zeros((5, 3, 2, 2, 2))
    h = np.zeros((5, 3, 2, 2, 3, 3))

    with pytest.raises(ValueError, match="grids must match"):
        nested_center_derivatives(b, h, times)

    with pytest.raises(ValueError, match="time axis"):
        derivative_from_samples(np.zeros((2, 3)), np.array([0.0, 0.1, 0.2]), 0.1, 1)
