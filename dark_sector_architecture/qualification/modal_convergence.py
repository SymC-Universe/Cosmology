"""Resolution/convergence utilities for modal tensor qualification.

Q-R1 compares tensor extraction at different grid representations of the same
physical field. It deliberately does not define a scientific acceptance
threshold.
"""

from __future__ import annotations

import numpy as np


def block_average(field: np.ndarray, factors: tuple[int, int, int]) -> np.ndarray:
    """Block-average the last/only three spatial axes by integer factors.

    Supported layouts:
    - scalar: (Nx, Ny, Nz)
    - component-first vector: (C, Nx, Ny, Nz)
    - tensor-last: (Nx, Ny, Nz, 3, 3)
    """
    arr = np.asarray(field, dtype=float)
    fx, fy, fz = (int(v) for v in factors)
    if min(fx, fy, fz) < 1:
        raise ValueError("coarse-graining factors must be positive integers")

    if arr.ndim == 3:
        spatial_axes = (0, 1, 2)
        prefix = ()
        suffix = ()
    elif arr.ndim == 4:
        spatial_axes = (1, 2, 3)
        prefix = (arr.shape[0],)
        suffix = ()
    elif arr.ndim == 5 and arr.shape[-2:] == (3, 3):
        spatial_axes = (0, 1, 2)
        prefix = ()
        suffix = (3, 3)
    else:
        raise ValueError(
            "supported shapes are (Nx,Ny,Nz), (C,Nx,Ny,Nz), "
            "or (Nx,Ny,Nz,3,3)"
        )

    sx, sy, sz = [arr.shape[a] for a in spatial_axes]
    if sx % fx or sy % fy or sz % fz:
        raise ValueError(
            f"spatial shape {(sx, sy, sz)} not divisible by factors {(fx, fy, fz)}"
        )

    if arr.ndim == 3:
        reshaped = arr.reshape(sx // fx, fx, sy // fy, fy, sz // fz, fz)
        return reshaped.mean(axis=(1, 3, 5))

    if arr.ndim == 4:
        c = arr.shape[0]
        reshaped = arr.reshape(
            c, sx // fx, fx, sy // fy, fy, sz // fz, fz
        )
        return reshaped.mean(axis=(2, 4, 6))

    reshaped = arr.reshape(
        sx // fx, fx, sy // fy, fy, sz // fz, fz, 3, 3
    )
    return reshaped.mean(axis=(1, 3, 5))


def ordered_eigensystem(tensor_field: np.ndarray):
    tensor = np.asarray(tensor_field, dtype=float)
    if tensor.ndim != 5 or tensor.shape[-2:] != (3, 3):
        raise ValueError("tensor_field must have shape (Nx,Ny,Nz,3,3)")
    values, vectors = np.linalg.eigh(tensor)
    return values[..., ::-1], vectors[..., :, ::-1]


def eigenvalue_error(reference: np.ndarray, candidate: np.ndarray) -> np.ndarray:
    ref = np.asarray(reference, dtype=float)
    cand = np.asarray(candidate, dtype=float)
    if ref.shape != cand.shape or ref.shape[-1] != 3:
        raise ValueError("ordered eigenvalue arrays must match and end in 3")
    return cand - ref


def eigenframe_absolute_alignment(
    reference_vectors: np.ndarray, candidate_vectors: np.ndarray
) -> np.ndarray:
    ref = np.asarray(reference_vectors, dtype=float)
    cand = np.asarray(candidate_vectors, dtype=float)
    if ref.shape != cand.shape or ref.shape[-2:] != (3, 3):
        raise ValueError("eigenvector arrays must match and end in (3,3)")
    return np.abs(
        np.matmul(
            np.swapaxes(ref, -1, -2),
            cand,
        )
    )


def tensor_frobenius_error(
    reference: np.ndarray, candidate: np.ndarray
) -> np.ndarray:
    ref = np.asarray(reference, dtype=float)
    cand = np.asarray(candidate, dtype=float)
    if ref.shape != cand.shape or ref.shape[-2:] != (3, 3):
        raise ValueError("tensor arrays must match and end in (3,3)")
    return np.linalg.norm(cand - ref, axis=(-2, -1))


def tensor_operator_error(
    reference: np.ndarray, candidate: np.ndarray
) -> np.ndarray:
    """Largest singular-value error per cell."""
    ref = np.asarray(reference, dtype=float)
    cand = np.asarray(candidate, dtype=float)
    if ref.shape != cand.shape or ref.shape[-2:] != (3, 3):
        raise ValueError("tensor arrays must match and end in (3,3)")
    return np.linalg.norm(cand - ref, ord=2, axis=(-2, -1))


def eigengaps(ordered_values: np.ndarray) -> np.ndarray:
    values = np.asarray(ordered_values, dtype=float)
    if values.shape[-1] != 3:
        raise ValueError("ordered eigenvalues must end in 3")
    return np.stack(
        [
            np.abs(values[..., 0] - values[..., 1]),
            np.abs(values[..., 1] - values[..., 2]),
        ],
        axis=-1,
    )


def directional_bound_from_tensor_error(
    tensor_error: np.ndarray, ordered_values: np.ndarray
) -> np.ndarray:
    """Continuous error/gap diagnostic for each adjacent eigenspace pair.

    Infinite values are retained at exact zero gap. No pass/fail threshold is
    applied here.
    """
    error = np.asarray(tensor_error, dtype=float)
    gaps = eigengaps(ordered_values)
    if error.shape != gaps.shape[:-1]:
        raise ValueError("tensor_error spatial shape must match eigenvalues")
    with np.errstate(divide="ignore", invalid="ignore"):
        bound = error[..., None] / gaps
    return bound


def quantile_summary(values: np.ndarray) -> dict[str, float]:
    arr = np.asarray(values, dtype=float).reshape(-1)
    finite = arr[np.isfinite(arr)]
    if finite.size == 0:
        return {
            "finite_count": 0,
            "total_count": int(arr.size),
            "min": None,
            "q05": None,
            "median": None,
            "q95": None,
            "max": None,
        }
    q = np.quantile(finite, [0.0, 0.05, 0.5, 0.95, 1.0])
    return {
        "finite_count": int(finite.size),
        "total_count": int(arr.size),
        "min": float(q[0]),
        "q05": float(q[1]),
        "median": float(q[2]),
        "q95": float(q[3]),
        "max": float(q[4]),
    }
