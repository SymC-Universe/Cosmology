"""Relational modal metrics for PREG-MODAL-PA-1 v1.

These definitions are frozen by dark_sector_architecture/PREG_MODAL_PA1_v1.md.
No nonzero amplitude or eigengap threshold is introduced here.
"""

from __future__ import annotations

import numpy as np


def _tensor(field: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim < 2 or arr.shape[-2:] != (3, 3):
        raise ValueError(f"{name} must end in shape (3,3)")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} must be finite")
    return arr


def frobenius_norm(field: np.ndarray) -> np.ndarray:
    arr = _tensor(field, "field")
    return np.sqrt(np.sum(arr * arr, axis=(-2, -1)))


def commutator(field_a: np.ndarray, field_b: np.ndarray) -> np.ndarray:
    a = _tensor(field_a, "field_a")
    b = _tensor(field_b, "field_b")
    if a.shape != b.shape:
        raise ValueError("tensor fields must have matching shapes")
    return np.matmul(a, b) - np.matmul(b, a)


def normalized_commutator(field_a: np.ndarray, field_b: np.ndarray) -> np.ndarray:
    """Bounded Böttcher-Wenzel-normalized commutator.

    C_AB = ||[A,B]||_F / (sqrt(2) ||A||_F ||B||_F).

    Exact zero-norm denominators are returned as NaN because the relational
    orientation is mathematically undefined.
    """
    a = _tensor(field_a, "field_a")
    b = _tensor(field_b, "field_b")
    if a.shape != b.shape:
        raise ValueError("tensor fields must have matching shapes")

    numerator = frobenius_norm(commutator(a, b))
    denominator = np.sqrt(2.0) * frobenius_norm(a) * frobenius_norm(b)

    out = np.full_like(denominator, np.nan, dtype=float)
    valid = denominator != 0.0
    out[valid] = numerator[valid] / denominator[valid]
    return out


def tensor_cosine(field_a: np.ndarray, field_b: np.ndarray) -> np.ndarray:
    """Frobenius tensor cosine tr(A B)/(||A|| ||B||)."""
    a = _tensor(field_a, "field_a")
    b = _tensor(field_b, "field_b")
    if a.shape != b.shape:
        raise ValueError("tensor fields must have matching shapes")
    numerator = np.sum(a * b, axis=(-2, -1))
    denominator = frobenius_norm(a) * frobenius_norm(b)
    out = np.full_like(denominator, np.nan, dtype=float)
    valid = denominator != 0.0
    out[valid] = numerator[valid] / denominator[valid]
    return out


def tracefree_spectral_shape(field: np.ndarray) -> np.ndarray:
    """Normalized cubic invariant q for a trace-free symmetric 3x3 tensor.

    q = 3 sqrt(6) det(A) / [tr(A^2)]^(3/2).

    Exact zero denominator is returned as NaN.
    """
    arr = _tensor(field, "field")
    tr_a2 = np.sum(arr * arr, axis=(-2, -1))
    determinant = np.linalg.det(arr)
    denominator = np.power(tr_a2, 1.5)
    out = np.full_like(denominator, np.nan, dtype=float)
    valid = denominator != 0.0
    out[valid] = 3.0 * np.sqrt(6.0) * determinant[valid] / denominator[valid]
    return out


def shear_reorganization(sigma_now: np.ndarray, sigma_future: np.ndarray) -> np.ndarray:
    """Frozen primary P1-M outcome R_sigma in [0,1] when defined."""
    a = _tensor(sigma_now, "sigma_now")
    b = _tensor(sigma_future, "sigma_future")
    if a.shape != b.shape:
        raise ValueError("shear fields must have matching shapes")
    numerator = frobenius_norm(b - a)
    denominator = frobenius_norm(b) + frobenius_norm(a)
    out = np.full_like(denominator, np.nan, dtype=float)
    valid = denominator != 0.0
    out[valid] = numerator[valid] / denominator[valid]
    return out


def t00_density_contrast(t00: np.ndarray) -> np.ndarray:
    arr = np.asarray(t00, dtype=float)
    if arr.ndim != 3:
        raise ValueError("T00 field must be a 3D scalar grid")
    if not np.all(np.isfinite(arr)):
        raise ValueError("T00 field must be finite")
    mean = float(np.mean(arr))
    if mean <= 0.0:
        raise ValueError("mean T00 must be positive")
    return arr / mean - 1.0


def density_log_growth(delta_now: np.ndarray, delta_future: np.ndarray) -> np.ndarray:
    a = np.asarray(delta_now, dtype=float)
    b = np.asarray(delta_future, dtype=float)
    if a.shape != b.shape:
        raise ValueError("density contrasts must have matching shapes")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("density contrasts must be finite")
    one_a = 1.0 + a
    one_b = 1.0 + b
    if np.any(one_a <= 0.0) or np.any(one_b <= 0.0):
        raise ValueError("1 + density contrast must be positive")
    return np.log(one_b / one_a)


def relation_feature_report(
    sigma: np.ndarray,
    electric_weyl: np.ndarray,
) -> dict[str, np.ndarray]:
    """Return the frozen cross-tensor feature pair."""
    c = normalized_commutator(sigma, electric_weyl)
    a = tensor_cosine(sigma, electric_weyl)
    return {
        "C_sigmaE": c,
        "A_sigmaE": a,
    }
