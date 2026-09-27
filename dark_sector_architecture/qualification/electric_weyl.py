"""First-order electric-Weyl reconstruction for gevolution Poisson-gauge fields.

Project convention
------------------
R^rho_{ sigma mu nu } =
    d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma} + ...

Metric
------
ds^2 = a^2 [-(1+2 Psi)d tau^2 - 2 B_i dx^i d tau
             + ((1-2 Phi)delta_ij + h_ij) dx^i dx^j]

with chi_gev = Phi - Psi.

The conformal-coordinate electric-Weyl tensor is reconstructed as

E_conf_ij =
    STF[d_i d_j (Phi - chi_gev/2)]
    - 1/2 d_(i B'_{j)}
    - 1/4 (h''_ij + Laplacian h_ij).

The physical orthonormal-frame tensor is E_phys = a^-2 E_conf.

This is P0-Q representation code. Temporal derivatives supplied to this module
must be qualified separately before a real-data result may be labeled full
electric Weyl.
"""

from __future__ import annotations

import numpy as np

from weak_field_tensors import scalar_weyl_shape_tensor
from latfield2_native_operators import (
    lattice_scalar_stf_hessian,
    lattice_tensor_laplacian,
    lattice_vector_symmetric_gradient,
)


def _validate_boxsize(boxsize: float) -> float:
    value = float(boxsize)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("boxsize must be finite and positive")
    return value


def _validate_vector(field: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 4 or arr.shape[0] != 3:
        raise ValueError(f"{name} must have shape (3, Nx, Ny, Nz)")
    if min(arr.shape[1:]) < 2:
        raise ValueError(f"{name} spatial dimensions must be at least 2")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} entries must be finite")
    return arr


def _validate_tensor(field: np.ndarray, name: str) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 5 or arr.shape[-2:] != (3, 3):
        raise ValueError(f"{name} must have shape (Nx, Ny, Nz, 3, 3)")
    if min(arr.shape[:3]) < 2:
        raise ValueError(f"{name} spatial dimensions must be at least 2")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} entries must be finite")
    return arr


def _wavevectors(shape: tuple[int, int, int], boxsize: float):
    axes = []
    for n in shape:
        dx = boxsize / n
        axes.append(2.0 * np.pi * np.fft.fftfreq(n, d=dx))
    return np.meshgrid(*axes, indexing="ij", sparse=True)


def symmetric_trace_free(tensor: np.ndarray) -> np.ndarray:
    arr = _validate_tensor(tensor, "tensor")
    sym = 0.5 * (arr + np.swapaxes(arr, -1, -2))
    trace = np.trace(sym, axis1=-2, axis2=-1)
    out = np.array(sym, copy=True)
    for i in range(3):
        out[..., i, i] -= trace / 3.0
    return out


def vector_gradient_periodic(vector: np.ndarray, boxsize: float) -> np.ndarray:
    """Return G_ij = d_i vector_j with shape (Nx,Ny,Nz,3,3)."""
    vec = _validate_vector(vector, "vector")
    boxsize = _validate_boxsize(boxsize)
    shape = tuple(vec.shape[1:])
    k = _wavevectors(shape, boxsize)
    gradient = np.empty(shape + (3, 3), dtype=float)

    for j in range(3):
        spectrum = np.fft.fftn(vec[j])
        for i in range(3):
            gradient[..., i, j] = np.fft.ifftn(
                1j * k[i] * spectrum
            ).real
    return gradient


def vector_divergence_periodic(vector: np.ndarray, boxsize: float) -> np.ndarray:
    gradient = vector_gradient_periodic(vector, boxsize)
    return np.trace(gradient, axis1=-2, axis2=-1)


def tensor_laplacian_periodic(
    tensor: np.ndarray, boxsize: float
) -> np.ndarray:
    """Return component-wise spatial Laplacian of a 3x3 tensor field."""
    arr = _validate_tensor(tensor, "tensor")
    boxsize = _validate_boxsize(boxsize)
    shape = tuple(arr.shape[:3])
    k = _wavevectors(shape, boxsize)
    k2 = k[0] * k[0] + k[1] * k[1] + k[2] * k[2]

    out = np.empty_like(arr)
    for i in range(3):
        for j in range(3):
            spectrum = np.fft.fftn(arr[..., i, j])
            out[..., i, j] = np.fft.ifftn(-k2 * spectrum).real
    return out


def tensor_divergence_periodic(
    tensor: np.ndarray, boxsize: float
) -> np.ndarray:
    """Return (div T)_i = d_j T_ij as component-first vector field."""
    arr = _validate_tensor(tensor, "tensor")
    boxsize = _validate_boxsize(boxsize)
    shape = tuple(arr.shape[:3])
    k = _wavevectors(shape, boxsize)
    out = np.zeros((3,) + shape, dtype=float)

    for i in range(3):
        total = np.zeros(shape, dtype=complex)
        for j in range(3):
            spectrum = np.fft.fftn(arr[..., i, j])
            total += 1j * k[j] * spectrum
        out[i] = np.fft.ifftn(total).real
    return out


def electric_weyl_conformal_sectors(
    phi: np.ndarray,
    chi_gev: np.ndarray,
    b_prime: np.ndarray,
    h: np.ndarray,
    h_second: np.ndarray,
    boxsize: float,
) -> dict[str, np.ndarray]:
    """Return scalar, vector, tensor, and total first-order Weyl sectors.

    Parameters
    ----------
    phi, chi_gev
        gevolution scalar fields with shape (Nx,Ny,Nz).
    b_prime
        conformal-time derivative d B_i / d tau, component-first.
    h
        gevolution transverse-traceless spatial metric perturbation h_ij.
    h_second
        conformal-time second derivative d^2 h_ij / d tau^2.
    boxsize
        Periodic comoving box length in the same coordinate-length units used
        for the derivative interpretation.

    Notes
    -----
    The returned total is projected to symmetric trace-free form to remove
    finite numerical residuals. Sector arrays are also STF-projected so their
    provenance remains explicit.
    """
    boxsize = _validate_boxsize(boxsize)
    scalar = scalar_weyl_shape_tensor(phi, chi_gev, boxsize)

    b_p = _validate_vector(b_prime, "b_prime")
    h_arr = _validate_tensor(h, "h")
    h_dd = _validate_tensor(h_second, "h_second")

    spatial_shape = scalar.shape[:3]
    if tuple(b_p.shape[1:]) != spatial_shape:
        raise ValueError("b_prime grid must match scalar grid")
    if tuple(h_arr.shape[:3]) != spatial_shape:
        raise ValueError("h grid must match scalar grid")
    if tuple(h_dd.shape[:3]) != spatial_shape:
        raise ValueError("h_second grid must match scalar grid")

    b_gradient = vector_gradient_periodic(b_p, boxsize)
    vector = -0.25 * (b_gradient + np.swapaxes(b_gradient, -1, -2))
    vector = symmetric_trace_free(vector)

    h_laplacian = tensor_laplacian_periodic(h_arr, boxsize)
    tensor = -0.25 * (h_dd + h_laplacian)
    tensor = symmetric_trace_free(tensor)

    total = symmetric_trace_free(scalar + vector + tensor)

    return {
        "scalar": scalar,
        "vector": vector,
        "tensor": tensor,
        "total": total,
        "h_laplacian": h_laplacian,
    }


def electric_weyl_conformal_tensor(
    phi: np.ndarray,
    chi_gev: np.ndarray,
    b_prime: np.ndarray,
    h: np.ndarray,
    h_second: np.ndarray,
    boxsize: float,
) -> np.ndarray:
    return electric_weyl_conformal_sectors(
        phi, chi_gev, b_prime, h, h_second, boxsize
    )["total"]


def electric_weyl_physical_tensor(
    phi: np.ndarray,
    chi_gev: np.ndarray,
    b_prime: np.ndarray,
    h: np.ndarray,
    h_second: np.ndarray,
    boxsize: float,
    scale_factor: float,
) -> np.ndarray:
    a = float(scale_factor)
    if not np.isfinite(a) or a <= 0.0:
        raise ValueError("scale_factor must be finite and positive")
    return electric_weyl_conformal_tensor(
        phi, chi_gev, b_prime, h, h_second, boxsize
    ) / (a * a)



def electric_weyl_conformal_sectors_latfield2(
    phi: np.ndarray,
    chi_gev: np.ndarray,
    b_prime: np.ndarray,
    h: np.ndarray,
    h_second: np.ndarray,
    boxsize: float,
) -> dict[str, np.ndarray]:
    """Return the full first-order Weyl sectors using gevolution lattice operators.

    This is the native-model-first representation for gevolution fields. Scalar,
    vector, and tensor spatial derivatives all use the same LATfield2/gevolution
    staggered lattice symbols. Temporal derivatives remain externally supplied
    and must be qualified separately.
    """
    boxsize = _validate_boxsize(boxsize)

    phi_arr = np.asarray(phi, dtype=float)
    chi_arr = np.asarray(chi_gev, dtype=float)
    if phi_arr.ndim != 3 or chi_arr.shape != phi_arr.shape:
        raise ValueError("phi and chi_gev must be matching scalar grids")
    if not np.all(np.isfinite(phi_arr)) or not np.all(np.isfinite(chi_arr)):
        raise ValueError("phi and chi_gev entries must be finite")

    b_p = _validate_vector(b_prime, "b_prime")
    h_arr = _validate_tensor(h, "h")
    h_dd = _validate_tensor(h_second, "h_second")

    spatial_shape = tuple(phi_arr.shape)
    if tuple(b_p.shape[1:]) != spatial_shape:
        raise ValueError("b_prime grid must match scalar grid")
    if tuple(h_arr.shape[:3]) != spatial_shape:
        raise ValueError("h grid must match scalar grid")
    if tuple(h_dd.shape[:3]) != spatial_shape:
        raise ValueError("h_second grid must match scalar grid")

    weyl_potential = phi_arr - 0.5 * chi_arr
    scalar = lattice_scalar_stf_hessian(weyl_potential, boxsize)

    b_symgrad = lattice_vector_symmetric_gradient(b_p, boxsize)
    vector = -0.5 * b_symgrad
    vector = symmetric_trace_free(vector)

    h_laplacian = lattice_tensor_laplacian(h_arr, boxsize)
    tensor = -0.25 * (h_dd + h_laplacian)
    tensor = symmetric_trace_free(tensor)

    total = symmetric_trace_free(scalar + vector + tensor)

    return {
        "scalar": scalar,
        "vector": vector,
        "tensor": tensor,
        "total": total,
        "h_laplacian": h_laplacian,
        "spatial_operator": "LATFIELD2_GEVOLUTION_NATIVE",
    }


def electric_weyl_conformal_tensor_latfield2(
    phi: np.ndarray,
    chi_gev: np.ndarray,
    b_prime: np.ndarray,
    h: np.ndarray,
    h_second: np.ndarray,
    boxsize: float,
) -> np.ndarray:
    return electric_weyl_conformal_sectors_latfield2(
        phi, chi_gev, b_prime, h, h_second, boxsize
    )["total"]


def electric_weyl_physical_tensor_latfield2(
    phi: np.ndarray,
    chi_gev: np.ndarray,
    b_prime: np.ndarray,
    h: np.ndarray,
    h_second: np.ndarray,
    boxsize: float,
    scale_factor: float,
) -> np.ndarray:
    a = float(scale_factor)
    if not np.isfinite(a) or a <= 0.0:
        raise ValueError("scale_factor must be finite and positive")
    return electric_weyl_conformal_tensor_latfield2(
        phi, chi_gev, b_prime, h, h_second, boxsize
    ) / (a * a)
