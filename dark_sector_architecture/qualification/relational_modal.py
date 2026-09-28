"""Relational modal diagnostics for pairs of symmetric 3x3 tensors.

P0-Q estimator layer only. The primary statistic is the normalized
Frobenius commutator

    kappa(A,B) = ||AB-BA||_F / (sqrt(2)||A||_F||B||_F).

The normalization follows the Boettcher-Wenzel commutator bound.
"""

from __future__ import annotations

import numpy as np


def _as_tensor_field(tensor: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(tensor, dtype=float)
    if arr.ndim < 2 or arr.shape[-2:] != (3, 3):
        raise ValueError(f"{name} must end in shape (3,3)")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values")
    return arr


def frobenius_norm(tensor: np.ndarray) -> np.ndarray:
    arr = _as_tensor_field(tensor, "tensor")
    return np.sqrt(np.sum(arr * arr, axis=(-2, -1)))


def commutator(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    aa = _as_tensor_field(a, "a")
    bb = _as_tensor_field(b, "b")
    if aa.shape != bb.shape:
        raise ValueError("a and b must have matching shapes")
    return aa @ bb - bb @ aa


def normalized_commutator_kappa(
    a: np.ndarray,
    b: np.ndarray,
) -> np.ndarray:
    """Return kappa for nonzero finite tensor pairs.

    Zero-norm pairs are returned as NaN so they cannot be silently
    interpreted as aligned.
    """
    aa = _as_tensor_field(a, "a")
    bb = _as_tensor_field(b, "b")
    if aa.shape != bb.shape:
        raise ValueError("a and b must have matching shapes")

    na = frobenius_norm(aa)
    nb = frobenius_norm(bb)
    c = commutator(aa, bb)
    nc = np.sqrt(np.sum(c * c, axis=(-2, -1)))
    denom = np.sqrt(2.0) * na * nb

    result = np.full_like(denom, np.nan, dtype=float)
    valid = denom > 0.0
    result[valid] = nc[valid] / denom[valid]
    return result


def normalized_trace_alignment(
    a: np.ndarray,
    b: np.ndarray,
) -> np.ndarray:
    aa = _as_tensor_field(a, "a")
    bb = _as_tensor_field(b, "b")
    if aa.shape != bb.shape:
        raise ValueError("a and b must have matching shapes")
    na = frobenius_norm(aa)
    nb = frobenius_norm(bb)
    denom = na * nb
    inner = np.sum(aa * bb, axis=(-2, -1))
    result = np.full_like(denom, np.nan, dtype=float)
    valid = denom > 0.0
    result[valid] = inner[valid] / denom[valid]
    return result


def ordered_eigenvalues(tensor: np.ndarray) -> np.ndarray:
    arr = _as_tensor_field(tensor, "tensor")
    values = np.linalg.eigvalsh(arr)
    return np.sort(values, axis=-1)


def eigengaps(tensor: np.ndarray) -> np.ndarray:
    values = ordered_eigenvalues(tensor)
    return np.diff(values, axis=-1)


def exact_degeneracy_status(
    tensor: np.ndarray,
    atol: float = 1e-12,
) -> np.ndarray:
    """Return True where an exact/known-truth repeated eigenvalue is present.

    This is intentionally not an empirical cosmological eigengap threshold.
    It is only a numerical known-truth detector for M0.
    """
    gaps = np.abs(eigengaps(tensor))
    scale = np.maximum(frobenius_norm(tensor), 1.0)
    return np.any(gaps <= atol * scale[..., None], axis=-1)


def relational_modal_record(
    a: np.ndarray,
    b: np.ndarray,
    degeneracy_atol: float = 1e-12,
) -> dict[str, np.ndarray | str]:
    aa = _as_tensor_field(a, "a")
    bb = _as_tensor_field(b, "b")
    if aa.shape != bb.shape:
        raise ValueError("a and b must have matching shapes")

    na = frobenius_norm(aa)
    nb = frobenius_norm(bb)
    kappa = normalized_commutator_kappa(aa, bb)
    deg_a = exact_degeneracy_status(aa, degeneracy_atol)
    deg_b = exact_degeneracy_status(bb, degeneracy_atol)

    refusal = np.full(na.shape, "OK", dtype=object)
    refusal[na == 0.0] = "REFUSED_ZERO_NORM_A"
    refusal[nb == 0.0] = "REFUSED_ZERO_NORM_B"
    refusal[(na == 0.0) & (nb == 0.0)] = "REFUSED_ZERO_NORM_BOTH"

    direction = np.full(na.shape, "IDENTIFIABLE_IN_KNOWN_TRUTH", dtype=object)
    direction[deg_a | deg_b] = "DEGENERATE_NONIDENTIFIABLE"
    direction[na == 0.0] = "REFUSED"
    direction[nb == 0.0] = "REFUSED"

    return {
        "kappa": kappa,
        "norm_a": na,
        "norm_b": nb,
        "trace_alignment": normalized_trace_alignment(aa, bb),
        "eigenvalues_a": ordered_eigenvalues(aa),
        "eigenvalues_b": ordered_eigenvalues(bb),
        "eigengaps_a": eigengaps(aa),
        "eigengaps_b": eigengaps(bb),
        "degenerate_a": deg_a,
        "degenerate_b": deg_b,
        "direction_status": direction,
        "refusal_status": refusal,
    }
