from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_relational import analyze_tensor_relation, relation_under_common_rotation
from modal_tensor import rotate_tensor, rotation_matrix


ATOL = 1e-11
RTOL = 1e-11


def test_mr01_aligned_distinct_spectra_have_zero_commutator():
    e = np.diag([3.0, 0.4, -2.1])
    s = np.diag([1.7, 0.2, -1.0])
    result = analyze_tensor_relation(e, s)

    np.testing.assert_allclose(result.commutator, 0.0, atol=ATOL, rtol=0.0)
    np.testing.assert_allclose(result.alignment_matrix_abs, np.eye(3), atol=ATOL, rtol=RTOL)
    assert result.normalized_commutator_frobenius == 0.0
    assert result.as_jsonable()['unique_axis_interpretation_licensed'] is True


def test_mr02_same_separate_spectra_can_hide_different_relational_geometry():
    e = np.diag([3.0, 0.4, -2.1])
    s_aligned = np.diag([1.7, 0.2, -1.0])
    relative = rotation_matrix(np.array([0.0, 0.0, 1.0]), 0.43)
    s_rotated = rotate_tensor(s_aligned, relative)

    aligned = analyze_tensor_relation(e, s_aligned)
    rotated = analyze_tensor_relation(e, s_rotated)

    np.testing.assert_allclose(
        aligned.second.eigenvalues, rotated.second.eigenvalues, atol=ATOL, rtol=RTOL
    )
    assert aligned.second.invariants == rotated.second.invariants
    assert aligned.normalized_commutator_frobenius == 0.0
    assert rotated.normalized_commutator_frobenius is not None
    assert rotated.normalized_commutator_frobenius > 0.0
    assert not np.allclose(
        rotated.alignment_matrix_abs, np.eye(3), atol=ATOL, rtol=RTOL
    )


def test_mr03_common_rotation_preserves_alignment_and_commutator_norm():
    e = np.diag([3.0, 0.4, -2.1])
    relative = rotation_matrix(np.array([0.2, 1.0, -0.5]), 0.61)
    s = rotate_tensor(np.diag([1.7, 0.2, -1.0]), relative)
    base = analyze_tensor_relation(e, s)

    global_rotation = rotation_matrix(np.array([1.0, -2.0, 0.3]), 0.79)
    rotated = relation_under_common_rotation(e, s, global_rotation)

    np.testing.assert_allclose(
        rotated.alignment_matrix_abs, base.alignment_matrix_abs, atol=ATOL, rtol=RTOL
    )
    assert rotated.commutator_frobenius_norm == np.testing.assert_allclose if False else rotated.commutator_frobenius_norm
    np.testing.assert_allclose(
        rotated.commutator_frobenius_norm,
        base.commutator_frobenius_norm,
        atol=ATOL,
        rtol=RTOL,
    )
    np.testing.assert_allclose(
        rotated.normalized_commutator_frobenius,
        base.normalized_commutator_frobenius,
        atol=ATOL,
        rtol=RTOL,
    )
    np.testing.assert_allclose(
        rotated.commutator_axial_vector,
        global_rotation @ base.commutator_axial_vector,
        atol=ATOL,
        rtol=RTOL,
    )


def test_mr04_exact_degenerate_subspace_refuses_unique_axis_but_relation_survives():
    e = np.diag([1.0, 1.0, -2.0])
    within_degenerate_plane = rotation_matrix(np.array([0.0, 0.0, 1.0]), 0.71)
    s0 = np.diag([2.0, 2.0, -4.0])
    s = rotate_tensor(s0, within_degenerate_plane)

    result = analyze_tensor_relation(e, s)

    assert result.as_jsonable()['unique_axis_interpretation_licensed'] is False
    np.testing.assert_allclose(result.commutator, 0.0, atol=ATOL, rtol=0.0)


def test_mr05_zero_tensor_has_raw_relation_but_no_normalized_commutator():
    e = np.zeros((3, 3))
    s = np.diag([1.0, 0.0, -1.0])
    result = analyze_tensor_relation(e, s)

    np.testing.assert_allclose(result.commutator, 0.0, atol=ATOL, rtol=0.0)
    assert result.normalized_commutator_frobenius is None
    assert result.as_jsonable()['unique_axis_interpretation_licensed'] is False


def test_mr06_commutator_is_antisymmetric():
    e = np.diag([2.0, 0.5, -1.5])
    r = rotation_matrix(np.array([1.0, 1.0, 0.0]), 0.37)
    s = rotate_tensor(np.diag([1.2, 0.1, -0.8]), r)
    result = analyze_tensor_relation(e, s)

    np.testing.assert_allclose(
        result.commutator + result.commutator.T, 0.0, atol=ATOL, rtol=0.0
    )


def test_mr07_relative_rotation_changes_relation_continuously():
    e = np.diag([3.0, 0.5, -2.0])
    base = np.diag([1.4, 0.1, -0.9])
    norms = []
    for angle in (0.0, 0.1, 0.2, 0.3):
        r = rotation_matrix(np.array([0.0, 0.0, 1.0]), angle)
        relation = analyze_tensor_relation(e, rotate_tensor(base, r))
        norms.append(relation.commutator_frobenius_norm)
    assert norms[0] == 0.0
    assert norms[0] < norms[1] < norms[2] < norms[3]
