"""Native lattice operators for gevolution exported peculiar velocity vi.

gevolution constructs vi on the scalar/vertex lattice from Ti0/T00 and uses
the centered Fourier symbol

    k_v(n) = (N/L) sin(2 pi n / N)

in projectFTtheta and projectFTomega.

This module is intentionally separate from latfield2_native_operators.py:
the metric vector B_i is staggered and uses a different kshift symbol.

No scientific acceptance threshold is encoded here.
"""

from __future__ import annotations

import numpy as np


def _validate_boxsize(boxsize: float) -> float:
    value = float(boxsize)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("boxsize must be finite and positive")
    return value


def _validate_vector(vector: np.ndarray) -> np.ndarray:
    arr = np.asarray(vector, dtype=float)
    if arr.ndim != 4 or arr.shape[0] != 3:
        raise ValueError("velocity must have shape (3,Nx,Ny,Nz)")
    if not np.all(np.isfinite(arr)):
        raise ValueError("velocity must be finite")
    if min(arr.shape[1:]) < 3:
        raise ValueError("each spatial dimension must contain at least 3 sites")
    return arr


def _centered_symbols(shape: tuple[int, int, int], boxsize: float):
    box = _validate_boxsize(boxsize)
    axes = []
    for n in shape:
        index = np.arange(int(n), dtype=float)
        axes.append((float(n) / box) * np.sin(2.0 * np.pi * index / float(n)))
    return np.meshgrid(*axes, indexing="ij", sparse=True)


def centered_derivative_periodic(
    field: np.ndarray, axis: int, boxsize: float = 1.0
) -> np.ndarray:
    """Centered first derivative matching gevolution velocity Fourier symbol."""
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 3:
        raise ValueError("field must have shape (Nx,Ny,Nz)")
    if not np.all(np.isfinite(arr)):
        raise ValueError("field must be finite")
    if axis not in (0, 1, 2):
        raise ValueError("axis must be 0, 1, or 2")
    symbols = _centered_symbols(tuple(arr.shape), boxsize)
    spectrum = np.fft.fftn(arr)
    return np.fft.ifftn(1j * symbols[axis] * spectrum).real


def velocity_gradient_centered(
    velocity: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    """Return grad_i v_j with output shape (Nx,Ny,Nz,3,3)."""
    vel = _validate_vector(velocity)
    shape = tuple(vel.shape[1:])
    symbols = _centered_symbols(shape, boxsize)
    spectra = [np.fft.fftn(vel[j]) for j in range(3)]
    out = np.empty(shape + (3, 3), dtype=float)
    for i in range(3):
        for j in range(3):
            out[..., i, j] = np.fft.ifftn(
                1j * symbols[i] * spectra[j]
            ).real
    return out


def velocity_divergence_centered(
    velocity: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    """Match gevolution projectFTtheta on the exported vi field."""
    grad = velocity_gradient_centered(velocity, boxsize)
    return np.trace(grad, axis1=-2, axis2=-1)


def velocity_shear_centered(
    velocity: np.ndarray, boxsize: float = 1.0
) -> tuple[np.ndarray, np.ndarray]:
    """Return symmetric trace-free velocity shear and divergence.

    sigma_ij = 1/2 (partial_i v_j + partial_j v_i)
               - delta_ij theta/3
    """
    grad = velocity_gradient_centered(velocity, boxsize)
    sym = 0.5 * (grad + np.swapaxes(grad, -1, -2))
    theta = np.trace(grad, axis1=-2, axis2=-1)
    shear = np.array(sym, copy=True)
    for i in range(3):
        shear[..., i, i] -= theta / 3.0
    return shear, theta


def velocity_vorticity_centered(
    velocity: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    """Return curl(v) with the same centered symbol as projectFTomega.

    gevolution first projects out the divergence part in Fourier space and then
    curls the remaining vector. With the same discrete symbol, curl(grad)=0,
    so curling the full vi field is algebraically equivalent.
    """
    grad = velocity_gradient_centered(velocity, boxsize)
    omega = np.empty(velocity.shape, dtype=float)
    omega[0] = grad[..., 1, 2] - grad[..., 2, 1]
    omega[1] = grad[..., 2, 0] - grad[..., 0, 2]
    omega[2] = grad[..., 0, 1] - grad[..., 1, 0]
    return omega


def velocity_kinematic_diagnostics(
    velocity: np.ndarray, boxsize: float = 1.0
) -> dict[str, float]:
    vel = _validate_vector(velocity)
    shear, theta = velocity_shear_centered(vel, boxsize)
    omega = velocity_vorticity_centered(vel, boxsize)
    return {
        "velocity_rms": float(np.sqrt(np.mean(vel * vel))),
        "divergence_rms": float(np.sqrt(np.mean(theta * theta))),
        "shear_frobenius_rms": float(
            np.sqrt(np.mean(np.sum(shear * shear, axis=(-2, -1))))
        ),
        "vorticity_rms": float(np.sqrt(np.mean(omega * omega))),
        "shear_max_trace_abs": float(
            np.max(np.abs(np.trace(shear, axis1=-2, axis2=-1)))
        ),
    }
