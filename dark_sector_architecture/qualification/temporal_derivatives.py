"""Temporal derivative qualification utilities for gevolution snapshot fields.

The routines use polynomial-interpolation finite-difference weights on the
actual conformal times. No equal-spacing assumption is made.

For a five-snapshot sequence around one central epoch, the qualification uses:
- inner stencil: snapshots [1, 2, 3]
- outer stencil: snapshots [0, 2, 4]

Both estimate derivatives at snapshot 2. Their difference is a temporal
discretization diagnostic, not a pre-frozen PASS/FAIL threshold.
"""

from __future__ import annotations

import math
import numpy as np


def finite_difference_weights(
    times: np.ndarray,
    target_time: float,
    derivative_order: int,
) -> np.ndarray:
    """Return interpolation-based derivative weights for arbitrary nodes."""
    x = np.asarray(times, dtype=float)
    x0 = float(target_time)
    order = int(derivative_order)

    if x.ndim != 1:
        raise ValueError("times must be one-dimensional")
    if len(x) < 2:
        raise ValueError("at least two time nodes are required")
    if order < 0 or order >= len(x):
        raise ValueError("derivative_order must be between 0 and len(times)-1")
    if not np.all(np.isfinite(x)) or not np.isfinite(x0):
        raise ValueError("times must be finite")
    if len(np.unique(x)) != len(x):
        raise ValueError("time nodes must be distinct")

    offsets = x - x0
    matrix = np.vstack([offsets ** p for p in range(len(x))])
    rhs = np.zeros(len(x), dtype=float)
    rhs[order] = math.factorial(order)
    return np.linalg.solve(matrix, rhs)


def derivative_from_samples(
    values: np.ndarray,
    times: np.ndarray,
    target_time: float,
    derivative_order: int,
) -> np.ndarray:
    """Differentiate an arbitrary array-valued time series along axis 0."""
    arr = np.asarray(values, dtype=float)
    x = np.asarray(times, dtype=float)
    if arr.ndim < 1:
        raise ValueError("values must have a time axis")
    if arr.shape[0] != len(x):
        raise ValueError("values time axis must match times")
    if not np.all(np.isfinite(arr)):
        raise ValueError("values must be finite")

    weights = finite_difference_weights(x, target_time, derivative_order)
    return np.tensordot(weights, arr, axes=(0, 0))


def nested_center_derivatives(
    b_snapshots: np.ndarray,
    h_snapshots: np.ndarray,
    conformal_times: np.ndarray,
) -> dict[str, np.ndarray]:
    """Compute inner/outer B' and h'' estimates at snapshot index 2.

    Parameters
    ----------
    b_snapshots
        Shape (5, 3, Nx, Ny, Nz).
    h_snapshots
        Shape (5, Nx, Ny, Nz, 3, 3).
    conformal_times
        Five strictly increasing conformal times in any common time unit.

    Returns
    -------
    dict
        Inner and outer derivative estimates, absolute differences, and
        finite-difference weights.
    """
    b = np.asarray(b_snapshots, dtype=float)
    h = np.asarray(h_snapshots, dtype=float)
    tau = np.asarray(conformal_times, dtype=float)

    if tau.shape != (5,):
        raise ValueError("conformal_times must contain exactly five values")
    if not np.all(np.diff(tau) > 0.0):
        raise ValueError("conformal_times must be strictly increasing")
    if b.ndim != 5 or b.shape[:2] != (5, 3):
        raise ValueError("b_snapshots must have shape (5,3,Nx,Ny,Nz)")
    if h.ndim != 6 or h.shape[0] != 5 or h.shape[-2:] != (3, 3):
        raise ValueError("h_snapshots must have shape (5,Nx,Ny,Nz,3,3)")
    if tuple(b.shape[2:]) != tuple(h.shape[1:4]):
        raise ValueError("B and h snapshot grids must match")
    if not np.all(np.isfinite(b)) or not np.all(np.isfinite(h)):
        raise ValueError("snapshot fields must be finite")

    center = tau[2]
    inner_idx = np.array([1, 2, 3])
    outer_idx = np.array([0, 2, 4])

    b_inner_weights = finite_difference_weights(
        tau[inner_idx], center, derivative_order=1
    )
    b_outer_weights = finite_difference_weights(
        tau[outer_idx], center, derivative_order=1
    )
    h_inner_weights = finite_difference_weights(
        tau[inner_idx], center, derivative_order=2
    )
    h_outer_weights = finite_difference_weights(
        tau[outer_idx], center, derivative_order=2
    )

    b_prime_inner = np.tensordot(
        b_inner_weights, b[inner_idx], axes=(0, 0)
    )
    b_prime_outer = np.tensordot(
        b_outer_weights, b[outer_idx], axes=(0, 0)
    )
    h_second_inner = np.tensordot(
        h_inner_weights, h[inner_idx], axes=(0, 0)
    )
    h_second_outer = np.tensordot(
        h_outer_weights, h[outer_idx], axes=(0, 0)
    )

    return {
        "b_prime_inner": b_prime_inner,
        "b_prime_outer": b_prime_outer,
        "h_second_inner": h_second_inner,
        "h_second_outer": h_second_outer,
        "b_prime_difference": b_prime_inner - b_prime_outer,
        "h_second_difference": h_second_inner - h_second_outer,
        "b_inner_weights": b_inner_weights,
        "b_outer_weights": b_outer_weights,
        "h_inner_weights": h_inner_weights,
        "h_outer_weights": h_outer_weights,
        "center_time": np.array(center),
    }


def relative_rms_difference(
    first: np.ndarray,
    second: np.ndarray,
    reference: np.ndarray | None = None,
) -> float | None:
    """RMS(first-second) divided by RMS(reference or second)."""
    a = np.asarray(first, dtype=float)
    b = np.asarray(second, dtype=float)
    if a.shape != b.shape:
        raise ValueError("arrays must have matching shapes")
    ref = b if reference is None else np.asarray(reference, dtype=float)
    if ref.shape != a.shape:
        raise ValueError("reference shape must match arrays")

    numerator = float(np.sqrt(np.mean((a - b) ** 2)))
    denominator = float(np.sqrt(np.mean(ref ** 2)))
    if denominator == 0.0:
        return None
    return numerator / denominator
