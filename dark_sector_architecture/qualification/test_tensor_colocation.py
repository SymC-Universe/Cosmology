from __future__ import annotations

import pathlib
import sys

import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from tensor_colocation import (
    colocate_offdiagonal_component_to_vertices,
    colocate_symmetric_tensor_to_vertices,
    colocation_transfer_factor,
)


def _coords(n: int, shifts=(0.0, 0.0, 0.0)):
    axes = [(np.arange(n) + shifts[i]) / n for i in range(3)]
    return np.meshgrid(*axes, indexing="ij")


def _mode_field(n: int, mode, shifts=(0.0, 0.0, 0.0)):
    x, y, z = _coords(n, shifts)
    phase = 2.0 * np.pi * (mode[0] * x + mode[1] * y + mode[2] * z)
    return np.cos(phase)


def _smooth_native_tensor(n: int):
    x, y, z = _coords(n)
    tensor = np.zeros((n, n, n, 3, 3), dtype=float)
    tensor[..., 0, 0] = np.sin(2*np.pi*x) + 0.2*np.cos(2*np.pi*y)
    tensor[..., 1, 1] = -0.3*np.sin(2*np.pi*y) + 0.1*np.cos(2*np.pi*z)
    tensor[..., 2, 2] = -tensor[..., 0, 0] - tensor[..., 1, 1]

    truth = np.array(tensor, copy=True)
    specs = {
        (0, 1): lambda a,b,c: 0.4*np.cos(2*np.pi*(a + 2*b)) + 0.1*np.sin(2*np.pi*c),
        (0, 2): lambda a,b,c: 0.3*np.sin(2*np.pi*(a - c)) + 0.05*np.cos(4*np.pi*b),
        (1, 2): lambda a,b,c: 0.25*np.cos(2*np.pi*(b + c)) + 0.07*np.sin(2*np.pi*a),
    }
    xv, yv, zv = _coords(n)
    for (i, j), fn in specs.items():
        vertex = fn(xv, yv, zv)
        shifts = [0.0, 0.0, 0.0]
        shifts[i] = 0.5
        shifts[j] = 0.5
        xs, ys, zs = _coords(n, shifts)
        staggered = fn(xs, ys, zs)
        truth[..., i, j] = vertex
        truth[..., j, i] = vertex
        tensor[..., i, j] = staggered
        tensor[..., j, i] = staggered
    return tensor, truth


def test_tc01_diagonal_passthrough():
    rng = np.random.default_rng(1)
    tensor = np.zeros((8, 8, 8, 3, 3))
    for i in range(3):
        tensor[..., i, i] = rng.normal(size=(8, 8, 8))
    out = colocate_symmetric_tensor_to_vertices(tensor)
    for i in range(3):
        np.testing.assert_array_equal(out[..., i, i], tensor[..., i, i])


def test_tc02_explicit_four_point_periodic_formula_and_wraparound():
    n = 7
    base = np.arange(n**3, dtype=float).reshape(n, n, n)
    actual = colocate_offdiagonal_component_to_vertices(base, 0, 2)
    expected = 0.25 * (
        base
        + np.roll(base, 1, axis=0)
        + np.roll(base, 1, axis=2)
        + np.roll(np.roll(base, 1, axis=0), 1, axis=2)
    )
    np.testing.assert_array_equal(actual, expected)
    assert actual[0, 3, 0] == pytest.approx(
        0.25*(base[0,3,0]+base[-1,3,0]+base[0,3,-1]+base[-1,3,-1])
    )


def test_tc03_symmetry_is_preserved():
    native, _ = _smooth_native_tensor(12)
    out = colocate_symmetric_tensor_to_vertices(native)
    np.testing.assert_allclose(out, np.swapaxes(out, -1, -2), atol=0.0, rtol=0.0)


def test_tc04_single_mode_transfer_matches_cosine_factor_and_vertex_phase():
    n = 32
    mode = (3, 5, 0)
    staggered = _mode_field(n, mode, shifts=(0.5, 0.5, 0.0))
    actual = colocate_offdiagonal_component_to_vertices(staggered, 0, 1)
    truth = _mode_field(n, mode)
    factor = colocation_transfer_factor(mode, n, 0, 1)
    np.testing.assert_allclose(actual, factor * truth, atol=2e-14, rtol=2e-14)


def test_tc05_smooth_periodic_recovery_is_second_order():
    errors = []
    for n in (16, 32, 64):
        native, truth = _smooth_native_tensor(n)
        out = colocate_symmetric_tensor_to_vertices(native)
        diff = out - truth
        errors.append(float(np.sqrt(np.mean(diff*diff))))
    ratio1 = errors[0] / errors[1]
    ratio2 = errors[1] / errors[2]
    assert 3.7 < ratio1 < 4.3
    assert 3.7 < ratio2 < 4.3


def test_tc06_nyquist_along_staggered_axis_is_filtered_not_inverted():
    n = 32
    mode = (n//2, 2, 0)
    staggered = _mode_field(n, mode, shifts=(0.5, 0.5, 0.0))
    actual = colocate_offdiagonal_component_to_vertices(staggered, 0, 1)
    factor = colocation_transfer_factor(mode, n, 0, 1)
    assert abs(factor) < 1e-15
    assert float(np.max(np.abs(actual))) < 2e-14


def test_tc07_linearity():
    rng = np.random.default_rng(7)
    a = rng.normal(size=(9,9,9))
    b = rng.normal(size=(9,9,9))
    alpha, beta = 1.3, -0.4
    lhs = colocate_offdiagonal_component_to_vertices(alpha*a + beta*b, 1, 2)
    rhs = (
        alpha*colocate_offdiagonal_component_to_vertices(a,1,2)
        + beta*colocate_offdiagonal_component_to_vertices(b,1,2)
    )
    np.testing.assert_allclose(lhs, rhs, atol=2e-15, rtol=2e-15)


def test_tc08_refuses_nonfinite_shape_noncubic_and_nonsymmetric():
    good = np.zeros((8,8,8,3,3))
    bad_nonfinite = good.copy()
    bad_nonfinite[0,0,0,0,0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        colocate_symmetric_tensor_to_vertices(bad_nonfinite)
    with pytest.raises(ValueError, match="shape"):
        colocate_symmetric_tensor_to_vertices(np.zeros((8,8,8,6)))
    with pytest.raises(ValueError, match="cubic"):
        colocate_symmetric_tensor_to_vertices(np.zeros((8,7,8,3,3)))
    bad_sym = good.copy()
    bad_sym[...,0,1] = 1.0
    with pytest.raises(ValueError, match="symmetric"):
        colocate_symmetric_tensor_to_vertices(bad_sym)
