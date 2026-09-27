from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_convergence import (
    block_average,
    directional_bound_from_tensor_error,
    eigenframe_absolute_alignment,
    eigengaps,
    eigenvalue_error,
    ordered_eigensystem,
    tensor_frobenius_error,
    tensor_operator_error,
)


def test_block_average_scalar_vector_and_tensor_shapes():
    scalar = np.arange(8 * 6 * 4, dtype=float).reshape(8, 6, 4)
    scalar_coarse = block_average(scalar, (2, 3, 2))
    assert scalar_coarse.shape == (4, 2, 2)

    vector = np.stack([scalar, scalar + 1.0, scalar + 2.0], axis=0)
    vector_coarse = block_average(vector, (2, 3, 2))
    assert vector_coarse.shape == (3, 4, 2, 2)

    tensor = np.zeros((8, 6, 4, 3, 3))
    tensor[..., 0, 0] = scalar
    tensor_coarse = block_average(tensor, (2, 3, 2))
    assert tensor_coarse.shape == (4, 2, 2, 3, 3)


def test_block_average_preserves_constant_fields():
    scalar = np.ones((8, 8, 8)) * 7.0
    np.testing.assert_allclose(block_average(scalar, (2, 2, 2)), 7.0)

    tensor = np.zeros((8, 8, 8, 3, 3))
    tensor[..., 0, 0] = 2.0
    tensor[..., 1, 1] = -1.0
    tensor[..., 2, 2] = -1.0
    coarse = block_average(tensor, (2, 2, 2))
    np.testing.assert_allclose(coarse, tensor[::2, ::2, ::2])


def test_identical_tensor_fields_have_zero_errors_and_identity_alignment():
    tensor = np.zeros((4, 4, 4, 3, 3))
    tensor[..., 0, 0] = 2.0
    tensor[..., 1, 1] = 0.5
    tensor[..., 2, 2] = -1.0

    values, vectors = ordered_eigensystem(tensor)
    ev_error = eigenvalue_error(values, values)
    frob = tensor_frobenius_error(tensor, tensor)
    op = tensor_operator_error(tensor, tensor)
    align = eigenframe_absolute_alignment(vectors, vectors)

    np.testing.assert_allclose(ev_error, 0.0)
    np.testing.assert_allclose(frob, 0.0)
    np.testing.assert_allclose(op, 0.0)
    expected = np.broadcast_to(np.eye(3), align.shape)
    np.testing.assert_allclose(align, expected)


def test_directional_bound_scales_with_error_over_gap():
    tensor = np.zeros((2, 2, 2, 3, 3))
    tensor[..., 0, 0] = 2.0
    tensor[..., 1, 1] = 1.0
    tensor[..., 2, 2] = -1.0
    values, _ = ordered_eigensystem(tensor)

    error = np.ones((2, 2, 2)) * 0.1
    bound = directional_bound_from_tensor_error(error, values)
    gaps = eigengaps(values)

    np.testing.assert_allclose(bound, error[..., None] / gaps)


def test_zero_gap_produces_infinite_directional_bound():
    tensor = np.zeros((1, 1, 1, 3, 3))
    tensor[..., 0, 0] = 1.0
    tensor[..., 1, 1] = 1.0
    tensor[..., 2, 2] = -2.0
    values, _ = ordered_eigensystem(tensor)

    bound = directional_bound_from_tensor_error(np.array([[[0.01]]]), values)
    assert np.isinf(bound[..., 0]).all()
    assert np.isfinite(bound[..., 1]).all()


def test_nondivisible_coarsening_refuses():
    bad = np.zeros((7, 8, 8))
    try:
        block_average(bad, (2, 2, 2))
    except ValueError as exc:
        assert "not divisible" in str(exc)
    else:
        raise AssertionError("nondivisible grid was accepted")
