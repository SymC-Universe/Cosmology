from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from modal_pairing_null import (
    conditional_permutation_indices,
    normalized_commutator_field,
    pairing_null_distances,
    wasserstein_1d,
)
from modal_tensor import rotate_tensor, rotation_matrix


def test_mp01_aligned_field_has_zero_commutator():
    e = np.stack([np.diag([3.0, 0.4, -2.1])] * 8)
    s = np.stack([np.diag([1.7, 0.2, -1.0])] * 8)
    values = normalized_commutator_field(e, s)
    np.testing.assert_allclose(values, 0.0, atol=1e-12, rtol=0.0)


def test_mp02_same_marginal_spectra_different_pairing_changes_relation():
    e = []
    s = []
    base_e = np.diag([3.0, 0.4, -2.1])
    base_s = np.diag([1.7, 0.2, -1.0])
    for angle in np.linspace(0.05, 0.65, 12):
        e.append(base_e)
        s.append(rotate_tensor(base_s, rotation_matrix(np.array([0, 0, 1.0]), angle)))
    e = np.stack(e)
    s = np.stack(s)

    observed = normalized_commutator_field(e, s)
    perm = np.arange(len(e))[::-1]
    shuffled = normalized_commutator_field(e, s[perm])

    assert wasserstein_1d(observed, shuffled) > 0.0


def test_mp03_common_rotation_preserves_field_values():
    e = []
    s = []
    base_e = np.diag([3.0, 0.4, -2.1])
    base_s = np.diag([1.7, 0.2, -1.0])
    for angle in np.linspace(0.1, 0.6, 9):
        e.append(base_e)
        s.append(rotate_tensor(base_s, rotation_matrix(np.array([0, 1.0, 0]), angle)))
    e = np.stack(e)
    s = np.stack(s)

    r = rotation_matrix(np.array([1.0, -0.4, 0.2]), 0.72)
    er = np.einsum("ab,nbc,dc->nad", r, e, r)
    sr = np.einsum("ab,nbc,dc->nad", r, s, r)

    np.testing.assert_allclose(
        normalized_commutator_field(er, sr),
        normalized_commutator_field(e, s),
        atol=1e-11,
        rtol=1e-11,
    )


def test_mp04_conditional_permutation_never_crosses_strata():
    labels = np.array([0, 0, 0, 1, 1, 2, 2, 2, 2])
    rng = np.random.default_rng(7)
    perm = conditional_permutation_indices(labels, rng)
    np.testing.assert_array_equal(labels[perm], labels)


def test_mp05_singleton_stratum_is_fixed():
    labels = np.array([0, 0, 1, 2, 2])
    rng = np.random.default_rng(11)
    perm = conditional_permutation_indices(labels, rng)
    assert perm[2] == 2


def test_mp06_pairing_null_detects_planted_relational_pairing():
    # Every E has the same spectrum. Every S has the same spectrum.
    # The observed pairings use small relative rotations; within-stratum
    # permutations break the angle pairing and broaden the relation.
    base_e = np.diag([3.0, 0.4, -2.1])
    base_s = np.diag([1.7, 0.2, -1.0])
    angles = np.linspace(0.02, 0.45, 40)
    e = np.stack([
        rotate_tensor(base_e, rotation_matrix(np.array([0, 0, 1.0]), a))
        for a in angles
    ])
    s = np.stack([
        rotate_tensor(base_s, rotation_matrix(np.array([0, 0, 1.0]), a + 0.03))
        for a in angles
    ])
    labels = np.zeros(len(angles), dtype=int)

    report = pairing_null_distances(
        s, e, labels, n_permutations=128, seed=123
    )
    assert report["finite_fraction"] == 1.0
    assert np.median(report["w1_distances"]) > 0.01


def test_mp07_null_pairing_with_identical_commuting_pairs_stays_zero():
    e = np.stack([np.diag([3.0, 0.4, -2.1])] * 16)
    s = np.stack([np.diag([1.7, 0.2, -1.0])] * 16)
    labels = np.zeros(16, dtype=int)
    report = pairing_null_distances(
        s, e, labels, n_permutations=32, seed=91
    )
    np.testing.assert_allclose(report["w1_distances"], 0.0, atol=1e-12, rtol=0.0)


def test_mp08_sparse_strata_do_not_fabricate_cross_stratum_null():
    e = np.stack([np.diag([3.0, 0.4, -2.1])] * 6)
    s = np.stack([
        rotate_tensor(
            np.diag([1.7, 0.2, -1.0]),
            rotation_matrix(np.array([0, 0, 1.0]), angle),
        )
        for angle in (0.0, 0.1, 0.2, 0.3, 0.4, 0.5)
    ])
    labels = np.arange(6)
    report = pairing_null_distances(
        s, e, labels, n_permutations=16, seed=5
    )
    np.testing.assert_allclose(report["w1_distances"], 0.0, atol=1e-12, rtol=0.0)
