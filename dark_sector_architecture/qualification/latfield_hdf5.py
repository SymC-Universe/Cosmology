"""Read LATfield2/gevolution HDF5 fields into NumPy axis conventions.

LATfield2 writes spatial dimensions in reversed order for HDF5 storage. This
loader restores logical (x, y, z) spatial order and places field components on
an explicit leading axis for vector-valued fields.

Qualification scope:
- scalar fields such as phi and chi;
- 3-component vector fields such as B and v;
- generic component-last array datatypes for inspection.

Tensor-component semantic mapping remains a separate qualification gate.
"""

from __future__ import annotations

import pathlib
from typing import Iterable

import h5py
import numpy as np


DEFAULT_DATASET = "data"


def dataset_names(path: str | pathlib.Path) -> list[str]:
    names: list[str] = []
    with h5py.File(path, "r") as handle:
        handle.visititems(
            lambda name, obj: names.append(name) if isinstance(obj, h5py.Dataset) else None
        )
    return names


def _read_dataset(path: str | pathlib.Path, dataset: str = DEFAULT_DATASET) -> np.ndarray:
    with h5py.File(path, "r") as handle:
        if dataset not in handle:
            available = dataset_names(path)
            raise ValueError(
                f"dataset {dataset!r} not found in {path}; available={available}"
            )
        data = np.asarray(handle[dataset][...])
    if not np.all(np.isfinite(data)):
        raise ValueError(f"non-finite values found in {path}:{dataset}")
    return data


def restore_latfield_spatial_order(data: np.ndarray, spatial_dims: int = 3) -> np.ndarray:
    """Restore LATfield logical spatial order from HDF5-reversed dimensions."""
    arr = np.asarray(data)
    if arr.ndim < spatial_dims:
        raise ValueError(
            f"array has ndim={arr.ndim}, fewer than spatial_dims={spatial_dims}"
        )
    permutation = list(range(arr.ndim))
    permutation[:spatial_dims] = reversed(permutation[:spatial_dims])
    return np.transpose(arr, axes=permutation)


def load_scalar_field(
    path: str | pathlib.Path, dataset: str = DEFAULT_DATASET
) -> np.ndarray:
    data = _read_dataset(path, dataset)
    if data.ndim != 3:
        raise ValueError(
            f"expected scalar LATfield dataset with 3 stored spatial dims, got shape={data.shape}"
        )
    restored = restore_latfield_spatial_order(data, spatial_dims=3)
    return np.asarray(restored, dtype=float)


def load_component_field(
    path: str | pathlib.Path,
    expected_components: int,
    dataset: str = DEFAULT_DATASET,
) -> np.ndarray:
    """Return component-first field with shape (C, Nx, Ny, Nz)."""
    data = _read_dataset(path, dataset)

    if data.ndim != 4:
        raise ValueError(
            "expected LATfield component dataset to read as "
            f"(stored spatial dims + component axis), got shape={data.shape}"
        )
    if data.shape[-1] != expected_components:
        raise ValueError(
            f"expected {expected_components} components, got shape={data.shape}"
        )

    restored = restore_latfield_spatial_order(data, spatial_dims=3)
    component_first = np.moveaxis(restored, -1, 0)
    return np.asarray(component_first, dtype=float)


def load_vector_field(
    path: str | pathlib.Path, dataset: str = DEFAULT_DATASET
) -> np.ndarray:
    return load_component_field(path, expected_components=3, dataset=dataset)


def summarize_hdf5_field(
    path: str | pathlib.Path, dataset: str = DEFAULT_DATASET
) -> dict:
    data = _read_dataset(path, dataset)
    return {
        "path": str(path),
        "dataset": dataset,
        "stored_shape": list(data.shape),
        "dtype": str(data.dtype),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "mean": float(np.mean(data)),
        "finite": bool(np.all(np.isfinite(data))),
    }
