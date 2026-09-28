"""Periodic grid-to-particle tensor interpolation and ID-frozen material patches.

P0-Q representation utilities. Scientific patch scales and epochs are not
encoded here.
"""

from __future__ import annotations

import numpy as np


_EPS=np.finfo(float).eps


def _symmetry_tolerance(scale: float) -> float:
    return 1024.0*_EPS*max(1.0,float(scale))


def _validate_tensor_grid(tensor: np.ndarray) -> np.ndarray:
    arr=np.asarray(tensor,dtype=float)
    if arr.ndim != 5 or arr.shape[-2:] != (3,3):
        raise ValueError("tensor grid must have shape (N,N,N,3,3)")
    if arr.shape[0] != arr.shape[1] or arr.shape[1] != arr.shape[2] or arr.shape[0] < 2:
        raise ValueError("tensor grid must be cubic with N>=2")
    if not np.all(np.isfinite(arr)):
        raise ValueError("tensor grid must be finite")
    resid=float(np.max(np.abs(arr-np.swapaxes(arr,-1,-2))))
    scale=float(np.max(np.abs(arr))) if arr.size else 0.0
    if resid > _symmetry_tolerance(scale):
        raise ValueError(f"tensor grid must be symmetric; max residual={resid:.6e}")
    return arr


def _validate_positions(positions: np.ndarray) -> np.ndarray:
    pos=np.asarray(positions,dtype=float)
    if pos.ndim != 2 or pos.shape[1] != 3:
        raise ValueError("positions must have shape (P,3)")
    if not np.all(np.isfinite(pos)):
        raise ValueError("positions must be finite")
    return pos


def _validate_ids(ids: np.ndarray, name: str="ids") -> np.ndarray:
    arr=np.asarray(ids,dtype=np.int64)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be one-dimensional")
    if len(np.unique(arr)) != len(arr):
        raise ValueError(f"{name} must be unique")
    return arr


def _validate_tensor_samples(samples: np.ndarray) -> np.ndarray:
    arr=np.asarray(samples,dtype=float)
    if arr.ndim != 3 or arr.shape[-2:] != (3,3):
        raise ValueError("tensor samples must have shape (P,3,3)")
    if not np.all(np.isfinite(arr)):
        raise ValueError("tensor samples must be finite")
    resid=float(np.max(np.abs(arr-np.swapaxes(arr,-1,-2)))) if arr.size else 0.0
    scale=float(np.max(np.abs(arr))) if arr.size else 0.0
    if resid > _symmetry_tolerance(scale):
        raise ValueError(f"tensor samples must be symmetric; max residual={resid:.6e}")
    return arr


def interpolate_vertex_tensor_periodic(
    tensor_grid: np.ndarray,
    positions: np.ndarray,
) -> np.ndarray:
    """Periodic trilinear interpolation of vertex tensor components."""
    grid=_validate_tensor_grid(tensor_grid)
    pos=_validate_positions(positions)
    n=grid.shape[0]
    wrapped=np.mod(pos,1.0)
    u=wrapped*n
    base=np.floor(u).astype(np.int64)
    frac=u-base
    base%=n
    out=np.zeros((len(pos),3,3),dtype=float)
    for dx in (0,1):
        wx=frac[:,0] if dx else 1.0-frac[:,0]
        ix=(base[:,0]+dx)%n
        for dy in (0,1):
            wy=frac[:,1] if dy else 1.0-frac[:,1]
            iy=(base[:,1]+dy)%n
            for dz in (0,1):
                wz=frac[:,2] if dz else 1.0-frac[:,2]
                iz=(base[:,2]+dz)%n
                w=(wx*wy*wz)[:,None,None]
                out += w*grid[ix,iy,iz]
    return out


def interpolate_vertex_tensor_by_id(
    tensor_grid: np.ndarray,
    ids: np.ndarray,
    positions: np.ndarray,
) -> dict[str,np.ndarray]:
    """Return ID-sorted interpolated tensors for order-independent joins."""
    pid=_validate_ids(ids)
    pos=_validate_positions(positions)
    if len(pid) != len(pos):
        raise ValueError("ids and positions length must match")
    values=interpolate_vertex_tensor_periodic(tensor_grid,pos)
    order=np.argsort(pid)
    return {"ID":pid[order],"tensor":values[order]}


def reference_patch_membership(
    ids: np.ndarray,
    reference_positions: np.ndarray,
    patch_grid_shape: tuple[int,int,int],
) -> dict[str,np.ndarray]:
    """Freeze one periodic reference-patch label per unique particle ID."""
    pid=_validate_ids(ids)
    pos=_validate_positions(reference_positions)
    if len(pid) != len(pos):
        raise ValueError("ids and reference_positions length must match")
    if len(patch_grid_shape) != 3:
        raise ValueError("patch_grid_shape must contain three integers")
    shape=np.asarray(patch_grid_shape,dtype=int)
    if np.any(shape <= 0) or tuple(shape.tolist()) != tuple(patch_grid_shape):
        raise ValueError("patch_grid_shape entries must be positive integers")
    wrapped=np.mod(pos,1.0)
    cell=np.floor(wrapped*shape[None,:]).astype(np.int64)%shape[None,:]
    patch=(cell[:,0]*shape[1]*shape[2]+cell[:,1]*shape[2]+cell[:,2]).astype(np.int64)
    order=np.argsort(pid)
    return {
        "ID":pid[order],
        "patch_id":patch[order],
        "patch_grid_shape":shape.astype(np.int64),
    }


def align_frozen_patch_membership(
    reference_ids: np.ndarray,
    reference_patch_ids: np.ndarray,
    current_ids: np.ndarray,
) -> np.ndarray:
    """Map frozen reference patch labels onto current record order by ID."""
    ref=_validate_ids(reference_ids,"reference_ids")
    cur=_validate_ids(current_ids,"current_ids")
    patch=np.asarray(reference_patch_ids,dtype=np.int64)
    if patch.ndim != 1 or len(patch) != len(ref):
        raise ValueError("reference_patch_ids must align with reference_ids")
    if len(cur) != len(ref) or not np.array_equal(np.sort(cur),np.sort(ref)):
        raise ValueError("current_ids must contain exactly the frozen reference ID set")
    order=np.argsort(ref)
    sorted_ref=ref[order]
    sorted_patch=patch[order]
    loc=np.searchsorted(sorted_ref,cur)
    if np.any(loc >= len(sorted_ref)) or not np.array_equal(sorted_ref[loc],cur):
        raise ValueError("current_ids could not be joined to reference IDs")
    return sorted_patch[loc]


def aggregate_material_patch_tensors(
    current_ids: np.ndarray,
    tensor_samples: np.ndarray,
    reference_ids: np.ndarray,
    reference_patch_ids: np.ndarray,
) -> dict[str,np.ndarray]:
    """Equal-particle mean tensor per nonempty frozen material patch."""
    cur=_validate_ids(current_ids,"current_ids")
    samples=_validate_tensor_samples(tensor_samples)
    if len(cur) != len(samples):
        raise ValueError("current_ids and tensor_samples length must match")
    patch=align_frozen_patch_membership(reference_ids,reference_patch_ids,cur)
    unique=np.unique(patch)
    means=np.empty((len(unique),3,3),dtype=float)
    counts=np.empty(len(unique),dtype=np.int64)
    for q,p in enumerate(unique):
        mask=patch==p
        counts[q]=int(np.count_nonzero(mask))
        if counts[q] == 0:
            raise RuntimeError("internal empty-patch aggregation error")
        means[q]=np.mean(samples[mask],axis=0)
    return {"patch_id":unique,"count":counts,"tensor":means}


def interpolate_and_aggregate_material_tensors(
    tensor_grid: np.ndarray,
    current_ids: np.ndarray,
    current_positions: np.ndarray,
    reference_ids: np.ndarray,
    reference_patch_ids: np.ndarray,
) -> dict[str,np.ndarray]:
    samples=interpolate_vertex_tensor_periodic(tensor_grid,current_positions)
    return aggregate_material_patch_tensors(
        current_ids,samples,reference_ids,reference_patch_ids
    )
