"""LATfield2/gevolution native lattice differential operators.

These operators reproduce the second-order staggered lattice symbols used by
gevolution 1.3 / LATfield2 for its scalar, vector, and tensor spin sectors.

For one axis with N sites on a periodic box of coordinate length L,

    kshift(n) = 2 (N/L) sin(pi n/N) exp(-i pi n/N)

and

    gridk2(n) = |kshift(n)|^2.

With NumPy's FFT convention:
- backward derivative has multiplier +i kshift;
- forward derivative has multiplier +i conjugate(kshift);
- native lattice Laplacian has multiplier -sum(gridk2).

The staggering rules below follow gevolution's computeVectorDiagnostics,
computeTensorDiagnostics, projectFTscalar, projectFTvector, and
projectFTtensor/evolveFTtensor conventions.
"""

from __future__ import annotations

import numpy as np


def _validate_boxsize(boxsize: float) -> float:
    value = float(boxsize)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("boxsize must be finite and positive")
    return value


def _symbols(shape: tuple[int, int, int], boxsize: float):
    box = _validate_boxsize(boxsize)
    kshift_axes = []
    k2_axes = []
    for n in shape:
        if int(n) < 2:
            raise ValueError("each spatial dimension must be at least 2")
        index = np.arange(int(n), dtype=float)
        theta = np.pi * index / float(n)
        scale = float(n) / box
        kshift = (
            2.0
            * scale
            * np.sin(theta)
            * np.exp(-1j * theta)
        )
        kshift_axes.append(kshift)
        k2_axes.append(np.abs(kshift) ** 2)

    kshift_mesh = np.meshgrid(*kshift_axes, indexing="ij", sparse=True)
    k2_mesh = np.meshgrid(*k2_axes, indexing="ij", sparse=True)
    return kshift_mesh, k2_mesh


def _validate_scalar(field: np.ndarray) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 3:
        raise ValueError("scalar field must have shape (Nx,Ny,Nz)")
    if not np.all(np.isfinite(arr)):
        raise ValueError("scalar field must be finite")
    return arr


def _validate_vector(field: np.ndarray) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 4 or arr.shape[0] != 3:
        raise ValueError("vector field must have shape (3,Nx,Ny,Nz)")
    if not np.all(np.isfinite(arr)):
        raise ValueError("vector field must be finite")
    return arr


def _validate_tensor(field: np.ndarray) -> np.ndarray:
    arr = np.asarray(field, dtype=float)
    if arr.ndim != 5 or arr.shape[-2:] != (3, 3):
        raise ValueError("tensor field must have shape (Nx,Ny,Nz,3,3)")
    if not np.all(np.isfinite(arr)):
        raise ValueError("tensor field must be finite")
    return arr


def lattice_backward_derivative(
    field: np.ndarray, axis: int, boxsize: float = 1.0
) -> np.ndarray:
    scalar = _validate_scalar(field)
    kshift, _ = _symbols(tuple(scalar.shape), boxsize)
    spectrum = np.fft.fftn(scalar)
    return np.fft.ifftn(1j * kshift[axis] * spectrum).real


def lattice_forward_derivative(
    field: np.ndarray, axis: int, boxsize: float = 1.0
) -> np.ndarray:
    scalar = _validate_scalar(field)
    kshift, _ = _symbols(tuple(scalar.shape), boxsize)
    spectrum = np.fft.fftn(scalar)
    return np.fft.ifftn(1j * np.conjugate(kshift[axis]) * spectrum).real


def lattice_laplacian(
    field: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    scalar = _validate_scalar(field)
    _, k2 = _symbols(tuple(scalar.shape), boxsize)
    k2_total = k2[0] + k2[1] + k2[2]
    spectrum = np.fft.fftn(scalar)
    return np.fft.ifftn(-k2_total * spectrum).real


def lattice_scalar_stf_hessian(
    field: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    """Return gevolution-compatible staggered STF Hessian of a scalar."""
    scalar = _validate_scalar(field)
    shape = tuple(scalar.shape)
    kshift, k2 = _symbols(shape, boxsize)
    k2_total = k2[0] + k2[1] + k2[2]
    spectrum = np.fft.fftn(scalar)

    out = np.empty(shape + (3, 3), dtype=float)
    for i in range(3):
        multiplier = -k2[i] + k2_total / 3.0
        out[..., i, i] = np.fft.ifftn(multiplier * spectrum).real

    for i in range(3):
        for j in range(i + 1, 3):
            multiplier = -np.conjugate(kshift[i]) * np.conjugate(kshift[j])
            value = np.fft.ifftn(multiplier * spectrum).real
            out[..., i, j] = value
            out[..., j, i] = value

    return out


def lattice_vector_divergence(
    vector: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    """Match gevolution computeVectorDiagnostics divergence operator."""
    vec = _validate_vector(vector)
    shape = tuple(vec.shape[1:])
    kshift, _ = _symbols(shape, boxsize)

    total = np.zeros(shape, dtype=complex)
    for i in range(3):
        total += 1j * kshift[i] * np.fft.fftn(vec[i])
    return np.fft.ifftn(total).real


def lattice_vector_symmetric_gradient(
    vector: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    """Map a staggered gevolution vector field to a symmetric tensor field.

    Diagonal components use the native backward derivative. Off-diagonal
    components use the forward derivative needed to land on the symmetric
    tensor component staggering. This is the negative-adjoint partner of the
    native tensor-divergence operator.
    """
    vec = _validate_vector(vector)
    shape = tuple(vec.shape[1:])
    kshift, _ = _symbols(shape, boxsize)
    spectra = [np.fft.fftn(vec[i]) for i in range(3)]

    out = np.empty(shape + (3, 3), dtype=float)
    for i in range(3):
        out[..., i, i] = np.fft.ifftn(
            1j * kshift[i] * spectra[i]
        ).real

    for i in range(3):
        for j in range(i + 1, 3):
            value = np.fft.ifftn(
                0.5j
                * (
                    np.conjugate(kshift[i]) * spectra[j]
                    + np.conjugate(kshift[j]) * spectra[i]
                )
            ).real
            out[..., i, j] = value
            out[..., j, i] = value

    return out


def lattice_tensor_laplacian(
    tensor: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    arr = _validate_tensor(tensor)
    shape = tuple(arr.shape[:3])
    _, k2 = _symbols(shape, boxsize)
    k2_total = k2[0] + k2[1] + k2[2]

    out = np.empty_like(arr)
    for i in range(3):
        for j in range(3):
            out[..., i, j] = np.fft.ifftn(
                -k2_total * np.fft.fftn(arr[..., i, j])
            ).real
    return out


def lattice_tensor_divergence(
    tensor: np.ndarray, boxsize: float = 1.0
) -> np.ndarray:
    """Match gevolution computeTensorDiagnostics divergence staggering."""
    arr = _validate_tensor(tensor)
    shape = tuple(arr.shape[:3])
    kshift, _ = _symbols(shape, boxsize)
    spectra = {
        (i, j): np.fft.fftn(arr[..., i, j])
        for i in range(3)
        for j in range(i, 3)
    }

    out = np.zeros((3,) + shape, dtype=float)
    for i in range(3):
        total = 1j * np.conjugate(kshift[i]) * spectra[(i, i)]
        for j in range(3):
            if j == i:
                continue
            a, b = (i, j) if i < j else (j, i)
            total += 1j * kshift[j] * spectra[(a, b)]
        out[i] = np.fft.ifftn(total).real
    return out


def lattice_vector_diagnostics(
    vector: np.ndarray, boxsize: float = 1.0
) -> dict[str, float]:
    vec = _validate_vector(vector)
    divergence = lattice_vector_divergence(vec, boxsize)
    return {
        "max_abs_divergence": float(np.max(np.abs(divergence))),
        "field_rms": float(np.sqrt(np.mean(vec * vec))),
    }


def lattice_tensor_diagnostics(
    tensor: np.ndarray, boxsize: float = 1.0
) -> dict[str, float]:
    arr = _validate_tensor(tensor)
    divergence = lattice_tensor_divergence(arr, boxsize)
    divergence_norm = np.sqrt(np.sum(divergence * divergence, axis=0))
    trace = np.trace(arr, axis1=-2, axis2=-1)
    frobenius = np.sqrt(np.sum(arr * arr, axis=(-2, -1)))
    symmetry = arr - np.swapaxes(arr, -1, -2)
    return {
        "max_divergence_norm": float(np.max(divergence_norm)),
        "max_abs_trace": float(np.max(np.abs(trace))),
        "max_frobenius_norm": float(np.max(frobenius)),
        "max_symmetry_residual": float(np.max(np.abs(symmetry))),
    }
