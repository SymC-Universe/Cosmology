from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_relational_metrics import (
    commutator,
    density_log_growth,
    frobenius_norm,
    normalized_commutator,
    relation_feature_report,
    shear_reorganization,
    t00_density_contrast,
    tensor_cosine,
    tracefree_spectral_shape,
)


ATOL = 1e-12


def _rotation_z(angle: float) -> np.ndarray:
    c = np.cos(angle)
    s = np.sin(angle)
    return np.array(
        [
            [c, -s, 0.0],
            [s, c, 0.0],
            [0.0, 0.0, 1.0],
        ]
    )


def _rotate_tensor(tensor: np.ndarray, rotation: np.ndarray) -> np.ndarray:
    return rotation @ tensor @ rotation.T


def test_commuting_diagonal_tensors_have_zero_commutator():
    a = np.diag([2.0, -0.5, -1.5])
    b = np.diag([1.0, 0.25, -1.25])

    c = normalized_commutator(a, b)
    assert c == 0.0
    np.testing.assert_allclose(commutator(a, b), 0.0, atol=ATOL)


def test_noncommuting_rotation_has_positive_bounded_commutator():
    a = np.diag([2.0, -0.5, -1.5])
    b0 = np.diag([1.0, 0.25, -1.25])
    r = _rotation_z(np.deg2rad(31.0))
    b = _rotate_tensor(b0, r)

    c = normalized_commutator(a, b)
    assert np.isfinite(c)
    assert 0.0 < c <= 1.0 + 1e-12


def test_commutator_is_invariant_under_common_rotation():
    a = np.diag([2.0, -0.5, -1.5])
    b0 = np.diag([1.0, 0.25, -1.25])
    b = _rotate_tensor(b0, _rotation_z(np.deg2rad(27.0)))

    common = _rotation_z(np.deg2rad(63.0))

    original = normalized_commutator(a, b)
    rotated = normalized_commutator(
        _rotate_tensor(a, common),
        _rotate_tensor(b, common),
    )
    np.testing.assert_allclose(rotated, original, atol=ATOL, rtol=0.0)


def test_commutator_is_amplitude_invariant():
    a = np.diag([2.0, -0.5, -1.5])
    b = _rotate_tensor(
        np.diag([1.0, 0.25, -1.25]),
        _rotation_z(np.deg2rad(40.0)),
    )

    original = normalized_commutator(a, b)
    scaled = normalized_commutator(7.3 * a, -4.1 * b)
    np.testing.assert_allclose(scaled, original, atol=ATOL, rtol=0.0)


def test_zero_norm_relation_is_undefined_not_forced_to_zero():
    a = np.zeros((3, 3))
    b = np.diag([1.0, 0.0, -1.0])

    assert np.isnan(normalized_commutator(a, b))
    assert np.isnan(tensor_cosine(a, b))
    assert np.isnan(tracefree_spectral_shape(a))


def test_tracefree_spectral_shape_is_rotation_invariant_and_bounded():
    a = np.diag([2.0, -0.5, -1.5])
    r = _rotation_z(np.deg2rad(22.0))
    q0 = tracefree_spectral_shape(a)
    q1 = tracefree_spectral_shape(_rotate_tensor(a, r))

    np.testing.assert_allclose(q0, q1, atol=ATOL, rtol=0.0)
    assert -1.0 - 1e-12 <= q0 <= 1.0 + 1e-12


def test_tensor_cosine_is_common_rotation_invariant():
    a = np.diag([2.0, -0.5, -1.5])
    b = _rotate_tensor(
        np.diag([1.0, 0.25, -1.25]),
        _rotation_z(np.deg2rad(35.0)),
    )
    r = _rotation_z(np.deg2rad(57.0))

    c0 = tensor_cosine(a, b)
    c1 = tensor_cosine(
        _rotate_tensor(a, r),
        _rotate_tensor(b, r),
    )
    np.testing.assert_allclose(c0, c1, atol=ATOL, rtol=0.0)


def test_shear_reorganization_bounds_and_identity():
    a = np.diag([2.0, -0.5, -1.5])
    same = shear_reorganization(a, a)
    assert same == 0.0

    b = -a
    opposite = shear_reorganization(a, b)
    np.testing.assert_allclose(opposite, 1.0, atol=ATOL)

    rotated = _rotate_tensor(a, _rotation_z(np.deg2rad(40.0)))
    value = shear_reorganization(a, rotated)
    assert 0.0 <= value <= 1.0 + 1e-12


def test_zero_zero_shear_reorganization_is_undefined():
    z = np.zeros((3, 3))
    assert np.isnan(shear_reorganization(z, z))


def test_t00_contrast_has_zero_mean_and_growth_is_exact():
    t0 = np.array(
        [
            [[1.0, 2.0], [3.0, 4.0]],
            [[5.0, 6.0], [7.0, 8.0]],
        ]
    )
    t1 = 1.25 * t0

    d0 = t00_density_contrast(t0)
    d1 = t00_density_contrast(t1)

    np.testing.assert_allclose(np.mean(d0), 0.0, atol=ATOL)
    np.testing.assert_allclose(np.mean(d1), 0.0, atol=ATOL)
    np.testing.assert_allclose(density_log_growth(d0, d1), 0.0, atol=ATOL)


def test_relation_feature_report_names_are_frozen():
    a = np.diag([2.0, -0.5, -1.5])
    b = _rotate_tensor(
        np.diag([1.0, 0.25, -1.25]),
        _rotation_z(np.deg2rad(29.0)),
    )
    report = relation_feature_report(a, b)
    assert set(report) == {"C_sigmaE", "A_sigmaE"}
    assert np.isfinite(report["C_sigmaE"])
    assert np.isfinite(report["A_sigmaE"])


def test_frobenius_norm_matches_direct_definition():
    a = np.array(
        [
            [2.0, 0.3, -0.1],
            [0.3, -0.5, 0.2],
            [-0.1, 0.2, -1.5],
        ]
    )
    np.testing.assert_allclose(
        frobenius_norm(a),
        np.sqrt(np.sum(a * a)),
        atol=ATOL,
    )
