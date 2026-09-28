"""Conditional pairing-null machinery for PREG-MODAL-PA-1.

This module operates on already-qualified relational tensors. It does not choose
scientific bins from outcomes and encodes no acceptance threshold.
"""

from __future__ import annotations

import numpy as np

from modal_relational import analyze_tensor_relation


def wasserstein_1d(x: np.ndarray, y: np.ndarray) -> float:
    """Equal-weight empirical one-dimensional Wasserstein distance."""
    a = np.asarray(x, dtype=float).ravel()
    b = np.asarray(y, dtype=float).ravel()
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) == 0 or len(b) == 0:
        raise ValueError("wasserstein_1d requires nonempty finite samples")

    a = np.sort(a)
    b = np.sort(b)
    q = np.linspace(0.0, 1.0, max(len(a), len(b)), endpoint=True)
    qa = np.linspace(0.0, 1.0, len(a), endpoint=True)
    qb = np.linspace(0.0, 1.0, len(b), endpoint=True)
    ai = np.interp(q, qa, a)
    bi = np.interp(q, qb, b)
    return float(np.trapezoid(np.abs(ai - bi), q))


def normalized_commutator_field(
    first: np.ndarray,
    second: np.ndarray,
) -> np.ndarray:
    """Compute normalized commutator for an array of paired 3x3 tensors."""
    a = np.asarray(first, dtype=float)
    b = np.asarray(second, dtype=float)
    if a.shape != b.shape or a.shape[-2:] != (3, 3):
        raise ValueError("paired tensor fields must match and end in (3,3)")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("tensor fields must be finite")

    flat_a = a.reshape((-1, 3, 3))
    flat_b = b.reshape((-1, 3, 3))
    out = np.full(len(flat_a), np.nan, dtype=float)
    for i, (x, y) in enumerate(zip(flat_a, flat_b)):
        value = analyze_tensor_relation(x, y).normalized_commutator_frobenius
        if value is not None:
            out[i] = value
    return out.reshape(a.shape[:-2])


def conditional_permutation_indices(
    stratum_ids: np.ndarray,
    rng: np.random.Generator,
) -> np.ndarray:
    """Return one permutation that re-pairs only within frozen strata."""
    labels = np.asarray(stratum_ids)
    if labels.ndim != 1 or len(labels) == 0:
        raise ValueError("stratum_ids must be a nonempty one-dimensional array")

    out = np.arange(len(labels), dtype=int)
    for label in np.unique(labels):
        idx = np.flatnonzero(labels == label)
        if len(idx) > 1:
            out[idx] = rng.permutation(idx)
    return out


def pairing_null_distances(
    first: np.ndarray,
    second: np.ndarray,
    stratum_ids: np.ndarray,
    *,
    n_permutations: int,
    seed: int,
) -> dict:
    """Compare observed pairing with within-stratum re-pairings.

    Strata must be constructed upstream from frozen scalar and standalone
    spectrum covariates. This function never derives strata from C_SE.
    """
    a = np.asarray(first, dtype=float)
    b = np.asarray(second, dtype=float)
    if a.shape != b.shape or a.shape[-2:] != (3, 3):
        raise ValueError("paired tensor fields must match and end in (3,3)")
    n = int(np.prod(a.shape[:-2]))
    labels = np.asarray(stratum_ids).reshape(-1)
    if len(labels) != n:
        raise ValueError("stratum_ids must match number of tensor pairs")

    count = int(n_permutations)
    if count < 1:
        raise ValueError("n_permutations must be positive")

    af = a.reshape((n, 3, 3))
    bf = b.reshape((n, 3, 3))
    observed = normalized_commutator_field(af, bf).reshape(-1)
    finite_obs = np.isfinite(observed)
    if not np.any(finite_obs):
        raise ValueError("no finite observed relational values")

    rng = np.random.default_rng(int(seed))
    distances = np.empty(count, dtype=float)
    null_medians = np.empty(count, dtype=float)

    for p in range(count):
        perm = conditional_permutation_indices(labels, rng)
        null = normalized_commutator_field(af, bf[perm]).reshape(-1)
        paired = finite_obs & np.isfinite(null)
        if not np.any(paired):
            raise ValueError("permutation produced no comparable pairs")
        distances[p] = wasserstein_1d(observed[paired], null[paired])
        null_medians[p] = float(np.median(null[paired]))

    return {
        "observed_median": float(np.median(observed[finite_obs])),
        "finite_fraction": float(np.mean(finite_obs)),
        "w1_distances": distances,
        "null_medians": null_medians,
    }
