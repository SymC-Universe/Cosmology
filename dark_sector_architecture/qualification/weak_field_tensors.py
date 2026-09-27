"""Weak-field tidal and velocity-shear reconstruction on periodic grids.

These are development/qualification representations for gevolution outputs.
They are not relabeled as the full electric Weyl tensor or full covariant
shear. Full-GR/covariant correspondence remains a separate qualification gate.
"""

from __future__ import annotations

import numpy as np


def _validate_scalar_field(field: np.ndarray) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 3:
        raise ValueError("scalar field must have shape (Nx, Ny, Nz)")
    if min(arr.shape) < 2:
        raise ValueError("each grid dimension must have at least 2 points")
    if not np.all(np.isfinite(arr)):
        raise ValueError("field entries must be finite")
    return arr


def _validate_boxsize(boxsize: float) -> float:
    value = float(boxsize)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("boxsize must be finite and positive")
    return value


def _wavevectors(shape: tuple[int, int, int], boxsize: float):
    axes = []
    for n in shape:
        dx = boxsize / n
        axes.append(2.0 * np.pi * np.fft.fftfreq(n, d=dx))
    return np.meshgrid(*axes, indexing="ij", sparse=True)


def spectral_hessian_periodic(field: np.ndarray, boxsize: float) -> np.ndarray:
    """Return Hessian d_i d_j field on a periodic Cartesian box.

    Output shape is field.shape + (3, 3).
    """
    scalar = _validate_scalar_field(field)
    boxsize = _validate_boxsize(boxsize)
    spectrum = np.fft.fftn(scalar)
    k = _wavevectors(scalar.shape, boxsize)

    hessian = np.empty(scalar.shape + (3, 3), dtype=float)
    for i in range(3):
        for j in range(i, 3):
            derivative = np.fft.ifftn(-(k[i] * k[j]) * spectrum).real
            hessian[..., i, j] = derivative
            hessian[..., j, i] = derivative
    return hessian


def _trace_free_hessian(field: np.ndarray, boxsize: float) -> np.ndarray:
    hessian = spectral_hessian_periodic(field, boxsize)
    trace = np.trace(hessian, axis1=-2, axis2=-1)
    tensor = np.array(hessian, copy=True)
    for i in range(3):
        tensor[..., i, i] -= trace / 3.0
    return tensor


def weak_field_tidal_tensor(phi: np.ndarray, boxsize: float) -> np.ndarray:
    """Return STF Hessian of gevolution Phi.

    This is the legacy Newtonian/negligible-slip scalar tidal development
    object. It must not be relabeled as the full electric Weyl tensor.
    """
    return _trace_free_hessian(phi, boxsize)


def scalar_weyl_shape_tensor(
    phi: np.ndarray, chi_gev: np.ndarray, boxsize: float
) -> np.ndarray:
    """Return first-order scalar electric-Weyl spatial shape.

    gevolution defines chi_gev = Phi - Psi, so the scalar Weyl/lensing
    potential is

        (Phi + Psi) / 2 = Phi - chi_gev / 2.

    This function returns the symmetric trace-free Hessian of that potential.
    It intentionally omits the epoch-dependent physical a^-2 normalization and
    does not include vector B_i or tensor h_ij sectors. Therefore it is a
    scalar-sector shape tensor, not the full electric Weyl tensor.
    """
    phi_arr = _validate_scalar_field(phi)
    chi_arr = _validate_scalar_field(chi_gev)
    if phi_arr.shape != chi_arr.shape:
        raise ValueError("phi and chi_gev must have matching grid shapes")
    weyl_potential = phi_arr - 0.5 * chi_arr
    return _trace_free_hessian(weyl_potential, boxsize)


def spectral_velocity_gradient_periodic(
    velocity: np.ndarray, boxsize: float
) -> np.ndarray:
    """Return gradient G_ij = d_i v_j for a periodic vector field.

    velocity must have shape (3, Nx, Ny, Nz).
    Output shape is (Nx, Ny, Nz, 3, 3).
    """
    vel = np.asarray(velocity, dtype=float)
    if vel.ndim != 4 or vel.shape[0] != 3:
        raise ValueError("velocity must have shape (3, Nx, Ny, Nz)")
    if min(vel.shape[1:]) < 2:
        raise ValueError("each grid dimension must have at least 2 points")
    if not np.all(np.isfinite(vel)):
        raise ValueError("velocity entries must be finite")
    boxsize = _validate_boxsize(boxsize)

    k = _wavevectors(tuple(vel.shape[1:]), boxsize)
    gradient = np.empty(tuple(vel.shape[1:]) + (3, 3), dtype=float)

    for j in range(3):
        spectrum = np.fft.fftn(vel[j])
        for i in range(3):
            derivative = np.fft.ifftn((1j * k[i]) * spectrum).real
            gradient[..., i, j] = derivative
    return gradient


def velocity_shear_tensor(
    velocity: np.ndarray, boxsize: float
) -> tuple[np.ndarray, np.ndarray]:
    """Return symmetric trace-free velocity shear and expansion/divergence."""
    gradient = spectral_velocity_gradient_periodic(velocity, boxsize)
    symmetric = 0.5 * (gradient + np.swapaxes(gradient, -1, -2))
    theta = np.trace(gradient, axis1=-2, axis2=-1)

    shear = np.array(symmetric, copy=True)
    for i in range(3):
        shear[..., i, i] -= theta / 3.0
    return shear, theta


def tensor_symmetry_residual(tensor_field: np.ndarray) -> float:
    tensor = np.asarray(tensor_field, dtype=float)
    if tensor.ndim < 2 or tensor.shape[-2:] != (3, 3):
        raise ValueError("tensor field must end in shape (3, 3)")
    residual = tensor - np.swapaxes(tensor, -1, -2)
    return float(np.max(np.linalg.norm(residual, axis=(-2, -1))))


def tensor_trace_residual(tensor_field: np.ndarray) -> float:
    tensor = np.asarray(tensor_field, dtype=float)
    if tensor.ndim < 2 or tensor.shape[-2:] != (3, 3):
        raise ValueError("tensor field must end in shape (3, 3)")
    return float(np.max(np.abs(np.trace(tensor, axis1=-2, axis2=-1))))
