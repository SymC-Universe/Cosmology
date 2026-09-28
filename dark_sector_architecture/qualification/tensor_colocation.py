"""Vertex co-location for gevolution/LATfield2 staggered symmetric tensors.

Native geometry:
- diagonal T_ii components are vertex-centered;
- off-diagonal T_ij components live at x + (e_i + e_j) Delta/2.

The frozen P0-Q map sends every component to the vertex lattice using the
second-order symmetric four-point periodic average for off-diagonals.
No deconvolution is performed.
"""

from __future__ import annotations

import numpy as np


def _validate_tensor_field(tensor: np.ndarray) -> np.ndarray:
    arr = np.asarray(tensor, dtype=float)
    if arr.ndim != 5 or arr.shape[-2:] != (3, 3):
        raise ValueError("tensor must have shape (N,N,N,3,3)")
    if arr.shape[0] != arr.shape[1] or arr.shape[1] != arr.shape[2]:
        raise ValueError("tensor spatial grid must be cubic")
    if arr.shape[0] < 2:
        raise ValueError("tensor spatial grid must contain at least 2 sites")
    if not np.all(np.isfinite(arr)):
        raise ValueError("tensor must contain only finite values")

    symmetry_residual = float(np.max(np.abs(arr - np.swapaxes(arr, -1, -2))))
    scale = max(1.0, float(np.max(np.abs(arr))))
    tolerance = 1024.0 * np.finfo(float).eps * scale
    if symmetry_residual > tolerance:
        raise ValueError(
            "tensor must be symmetric before co-location; "
            f"max residual={symmetry_residual:.6e}"
        )
    return arr


def colocate_offdiagonal_component_to_vertices(
    component: np.ndarray,
    axis_i: int,
    axis_j: int,
) -> np.ndarray:
    """Co-locate one plaquette-centered T_ij component onto vertices.

    The input index x represents the physical location
    x + (e_i + e_j) Delta/2. The vertex value at x is therefore obtained
    by averaging input indices x, x-e_i, x-e_j, x-e_i-e_j.
    """
    field = np.asarray(component, dtype=float)
    if field.ndim != 3:
        raise ValueError("component must be a 3D field")
    if not np.all(np.isfinite(field)):
        raise ValueError("component must contain only finite values")
    if axis_i not in (0, 1, 2) or axis_j not in (0, 1, 2) or axis_i == axis_j:
        raise ValueError("axis_i and axis_j must be distinct spatial axes")

    minus_i = np.roll(field, 1, axis=axis_i)
    minus_j = np.roll(field, 1, axis=axis_j)
    minus_ij = np.roll(minus_i, 1, axis=axis_j)
    return 0.25 * (field + minus_i + minus_j + minus_ij)


def colocate_symmetric_tensor_to_vertices(tensor: np.ndarray) -> np.ndarray:
    """Return a vertex-co-located local symmetric tensor field."""
    arr = _validate_tensor_field(tensor)
    out = np.empty_like(arr)

    for i in range(3):
        out[..., i, i] = arr[..., i, i]

    for i in range(3):
        for j in range(i + 1, 3):
            value = colocate_offdiagonal_component_to_vertices(
                arr[..., i, j], i, j
            )
            out[..., i, j] = value
            out[..., j, i] = value

    return out


def colocation_transfer_factor(
    mode: tuple[int, int, int],
    grid_size: int,
    axis_i: int,
    axis_j: int,
) -> float:
    """Return cos(pi n_i/N) cos(pi n_j/N) for signed integer modes."""
    if grid_size < 2:
        raise ValueError("grid_size must be at least 2")
    if axis_i not in (0, 1, 2) or axis_j not in (0, 1, 2) or axis_i == axis_j:
        raise ValueError("axis_i and axis_j must be distinct spatial axes")
    if len(mode) != 3:
        raise ValueError("mode must contain three signed integer indices")
    return float(
        np.cos(np.pi * mode[axis_i] / grid_size)
        * np.cos(np.pi * mode[axis_j] / grid_size)
    )


def tensor_colocation_diagnostics(
    native_tensor: np.ndarray,
    colocated_tensor: np.ndarray | None = None,
) -> dict[str, float]:
    """Return representation-only diagnostics, with no scientific thresholds."""
    native = _validate_tensor_field(native_tensor)
    colocated = (
        colocate_symmetric_tensor_to_vertices(native)
        if colocated_tensor is None
        else _validate_tensor_field(colocated_tensor)
    )
    if colocated.shape != native.shape:
        raise ValueError("native and colocated tensor shapes must match")

    difference = colocated - native
    diag_difference = np.stack(
        [difference[..., i, i] for i in range(3)], axis=-1
    )
    offdiag_difference = np.stack(
        [
            difference[..., 0, 1],
            difference[..., 0, 2],
            difference[..., 1, 2],
        ],
        axis=-1,
    )
    return {
        "native_frobenius_rms": float(
            np.sqrt(np.mean(np.sum(native * native, axis=(-2, -1))))
        ),
        "colocated_frobenius_rms": float(
            np.sqrt(np.mean(np.sum(colocated * colocated, axis=(-2, -1))))
        ),
        "difference_frobenius_rms": float(
            np.sqrt(np.mean(np.sum(difference * difference, axis=(-2, -1))))
        ),
        "diagonal_difference_rms": float(np.sqrt(np.mean(diag_difference**2))),
        "offdiagonal_difference_rms": float(
            np.sqrt(np.mean(offdiag_difference**2))
        ),
        "colocated_symmetry_max_abs": float(
            np.max(np.abs(colocated - np.swapaxes(colocated, -1, -2)))
        ),
    }
