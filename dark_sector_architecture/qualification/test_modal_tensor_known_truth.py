from __future__ import annotations

import math
import pathlib
import sys

import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_tensor import (
    analyze_symmetric_tensor,
    eigenframe_alignment,
    perturbation_direction_bound,
    rotate_tensor,
    rotation_matrix,
)


ATOL = 1e-11
RTOL = 1e-11


def _assert_orthonormal(vectors: np.ndarray) -> None:
    np.testing.assert_allclose(vectors.T @ vectors, np.eye(3), atol=ATOL, rtol=RTOL)


def test_kt01_isotropic_expansion_exact_degeneracy_refuses_direction():
    result = analyze_symmetric_tensor(np.eye(3) * 2.5)

    np.testing.assert_allclose(result.eigenvalues, [2.5, 2.5, 2.5], atol=ATOL)
    assert result.degenerate_pairs == (True, True)
    assert math.isinf(result.directional_condition_number)
    _assert_orthonormal(result.eigenvectors)


def test_kt02_one_axis_collapse_recovers_unique_principal_axis_under_rotation():
    tensor = np.diag([2.0, 0.5, -1.0])
    base = analyze_symmetric_tensor(tensor)

    rotation = rotation_matrix(np.array([1.0, 2.0, 3.0]), 0.71)
    rotated = analyze_symmetric_tensor(rotate_tensor(tensor, rotation))

    np.testing.assert_allclose(rotated.eigenvalues, base.eigenvalues, atol=ATOL, rtol=RTOL)
    overlap = np.abs(rotated.eigenvectors.T @ (rotation @ base.eigenvectors))
    np.testing.assert_allclose(overlap, np.eye(3), atol=ATOL, rtol=RTOL)
    assert rotated.degenerate_pairs == (False, False)


def test_kt03_two_axis_collapse_returns_ordered_distinct_spectrum():
    tensor = np.diag([0.8, -0.4, -1.2])
    result = analyze_symmetric_tensor(tensor)

    np.testing.assert_allclose(result.eigenvalues, [0.8, -0.4, -1.2], atol=ATOL)
    assert result.degenerate_pairs == (False, False)
    assert result.eigenvalues[1] < 0.0 and result.eigenvalues[2] < 0.0


def test_kt04_three_axis_collapse_near_isotropic_reports_worsening_conditioning():
    separated = analyze_symmetric_tensor(np.diag([-0.8, -1.0, -1.3]))
    close = analyze_symmetric_tensor(np.diag([-1.0, -1.000001, -1.000003]))

    assert np.all(close.eigenvalues < 0.0)
    assert close.directional_condition_number > separated.directional_condition_number
    assert close.degenerate_pairs == (False, False)


def test_kt05_matched_scalar_subset_can_hide_different_modal_spectra():
    # Both tensors have trace 0 and tr(S^2)=6, but different spectra/determinants.
    first = analyze_symmetric_tensor(np.diag([2.0, -1.0, -1.0]))
    second = analyze_symmetric_tensor(
        np.diag([math.sqrt(3.0), 0.0, -math.sqrt(3.0)])
    )

    assert first.invariants["trace"] == pytest.approx(second.invariants["trace"], abs=ATOL)
    assert first.invariants["trace_square"] == pytest.approx(
        second.invariants["trace_square"], abs=ATOL
    )
    assert first.invariants["determinant"] != pytest.approx(
        second.invariants["determinant"], abs=ATOL
    )
    assert not np.allclose(first.eigenvalues, second.eigenvalues, atol=ATOL, rtol=RTOL)


def test_kt06_rotation_changes_frame_not_invariants_or_spectrum():
    tensor = np.diag([2.0, 0.3, -1.4])
    rotation = rotation_matrix(np.array([2.0, -1.0, 0.5]), 0.93)

    base = analyze_symmetric_tensor(tensor)
    rotated = analyze_symmetric_tensor(rotate_tensor(tensor, rotation))

    np.testing.assert_allclose(rotated.eigenvalues, base.eigenvalues, atol=ATOL, rtol=RTOL)
    for key in base.invariants:
        assert rotated.invariants[key] == pytest.approx(base.invariants[key], rel=RTOL, abs=ATOL)

    overlap = np.abs(rotated.eigenvectors.T @ (rotation @ base.eigenvectors))
    np.testing.assert_allclose(overlap, np.eye(3), atol=ATOL, rtol=RTOL)


def test_kt07_near_degenerate_pair_reports_continuous_conditioning_not_hard_threshold():
    gaps = [1e-2, 1e-4, 1e-6, 1e-8]
    condition_numbers = []

    for gap in gaps:
        result = analyze_symmetric_tensor(np.diag([1.0, 1.0 - gap, -2.0]))
        assert result.degenerate_pairs == (False, False)
        condition_numbers.append(result.directional_condition_number)

    assert all(
        later > earlier
        for earlier, later in zip(condition_numbers[:-1], condition_numbers[1:])
    )


def test_kt08_exact_pair_degeneracy_identifies_subspace_not_unique_axis():
    result = analyze_symmetric_tensor(np.diag([1.0, 1.0, -2.0]))

    assert result.degenerate_pairs == (True, False)
    assert math.isinf(result.directional_condition_number)
    _assert_orthonormal(result.eigenvectors)


def test_kt09_shear_weyl_aligned_returns_identity_alignment():
    shear = analyze_symmetric_tensor(np.diag([2.0, 0.5, -1.0]))
    weyl = analyze_symmetric_tensor(np.diag([3.0, 0.2, -2.0]))

    np.testing.assert_allclose(
        eigenframe_alignment(shear, weyl), np.eye(3), atol=ATOL, rtol=RTOL
    )


def test_kt10_shear_weyl_misalignment_is_coordinate_rotation_invariant():
    shear_tensor = np.diag([2.0, 0.5, -1.0])
    relative = rotation_matrix(np.array([0.0, 0.0, 1.0]), 0.4)
    weyl_tensor = rotate_tensor(np.diag([3.0, 0.2, -2.0]), relative)

    shear = analyze_symmetric_tensor(shear_tensor)
    weyl = analyze_symmetric_tensor(weyl_tensor)
    alignment_before = eigenframe_alignment(shear, weyl)

    global_rotation = rotation_matrix(np.array([1.0, 2.0, 0.5]), 0.77)
    shear_rotated = analyze_symmetric_tensor(rotate_tensor(shear_tensor, global_rotation))
    weyl_rotated = analyze_symmetric_tensor(rotate_tensor(weyl_tensor, global_rotation))
    alignment_after = eigenframe_alignment(shear_rotated, weyl_rotated)

    np.testing.assert_allclose(alignment_after, alignment_before, atol=ATOL, rtol=RTOL)


def test_kt11_direction_sensitivity_increases_as_gap_closes():
    wide = analyze_symmetric_tensor(np.diag([1.0, 0.2, -1.0]))
    narrow = analyze_symmetric_tensor(np.diag([1.0, 0.999, -1.0]))

    perturbation_norm = 1e-5
    wide_bound = perturbation_direction_bound(wide, perturbation_norm)
    narrow_bound = perturbation_direction_bound(narrow, perturbation_norm)

    assert narrow_bound > wide_bound
    assert wide_bound >= 0.0


def test_kt12_materially_nonsymmetric_input_is_refused_not_silently_symmetrized():
    bad = np.array(
        [
            [1.0, 0.2, 0.0],
            [0.0, -0.4, 0.1],
            [0.0, 0.1, -0.6],
        ]
    )

    with pytest.raises(ValueError, match="symmetric"):
        analyze_symmetric_tensor(bad)


def test_input_shape_and_finiteness_are_fail_closed():
    with pytest.raises(ValueError, match="3x3"):
        analyze_symmetric_tensor(np.eye(2))

    bad = np.eye(3)
    bad[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        analyze_symmetric_tensor(bad)
