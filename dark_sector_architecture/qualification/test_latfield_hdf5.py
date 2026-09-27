from __future__ import annotations

import pathlib
import sys

import h5py
import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from latfield_hdf5 import (
    dataset_names,
    load_scalar_field,
    load_symmetric_tensor_field,
    load_vector_field,
    summarize_hdf5_field,
)


def test_scalar_latfield_axis_order_is_restored(tmp_path):
    nx, ny, nz = 4, 3, 2
    logical = np.zeros((nx, ny, nz), dtype=float)
    for x in range(nx):
        for y in range(ny):
            for z in range(nz):
                logical[x, y, z] = 100 * x + 10 * y + z

    stored = np.transpose(logical, (2, 1, 0))
    path = tmp_path / "scalar.h5"
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=stored)

    restored = load_scalar_field(path)
    np.testing.assert_array_equal(restored, logical)


def test_vector_hdf5_array_datatype_is_restored_component_first(tmp_path):
    nx, ny, nz = 4, 3, 2
    logical = np.zeros((3, nx, ny, nz), dtype=float)
    for component in range(3):
        for x in range(nx):
            for y in range(ny):
                for z in range(nz):
                    logical[component, x, y, z] = (
                        1000 * component + 100 * x + 10 * y + z
                    )

    stored_component_last = np.moveaxis(logical, 0, -1)
    stored_component_last = np.transpose(
        stored_component_last, (2, 1, 0, 3)
    )

    path = tmp_path / "vector.h5"
    vector_dtype = np.dtype((np.float64, (3,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=(nz, ny, nx), dtype=vector_dtype
        )
        dataset[...] = stored_component_last

    restored = load_vector_field(path)
    np.testing.assert_array_equal(restored, logical)


def test_dataset_listing_and_summary(tmp_path):
    path = tmp_path / "field.h5"
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=np.ones((2, 2, 2)))
        handle.create_dataset("aux", data=np.zeros((1,)))

    assert sorted(dataset_names(path)) == ["aux", "data"]
    summary = summarize_hdf5_field(path)
    assert summary["stored_shape"] == [2, 2, 2]
    assert summary["finite"] is True
    assert summary["mean"] == pytest.approx(1.0)


def test_missing_dataset_is_refused(tmp_path):
    path = tmp_path / "missing.h5"
    with h5py.File(path, "w") as handle:
        handle.create_dataset("other", data=np.ones((2, 2, 2)))

    with pytest.raises(ValueError, match="not found"):
        load_scalar_field(path)


def test_wrong_vector_component_count_is_refused(tmp_path):
    path = tmp_path / "wrong_components.h5"
    dtype = np.dtype((np.float64, (2,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset("data", shape=(2, 2, 2), dtype=dtype)
        dataset[...] = np.zeros((2, 2, 2, 2))

    with pytest.raises(ValueError, match="expected 3 components"):
        load_vector_field(path)


def test_nonfinite_data_is_refused(tmp_path):
    path = tmp_path / "nan.h5"
    data = np.ones((2, 2, 2))
    data[0, 0, 0] = np.nan
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=data)

    with pytest.raises(ValueError, match="non-finite"):
        load_scalar_field(path)



def test_symmetric_tensor_component_order_is_restored(tmp_path):
    nx, ny, nz = 4, 3, 2
    logical = np.zeros((nx, ny, nz, 3, 3), dtype=float)

    logical[..., 0, 0] = 11.0
    logical[..., 0, 1] = 12.0
    logical[..., 1, 0] = 12.0
    logical[..., 0, 2] = 13.0
    logical[..., 2, 0] = 13.0
    logical[..., 1, 1] = 22.0
    logical[..., 1, 2] = 23.0
    logical[..., 2, 1] = 23.0
    logical[..., 2, 2] = 33.0

    components = np.stack(
        [
            logical[..., 0, 0],
            logical[..., 0, 1],
            logical[..., 0, 2],
            logical[..., 1, 1],
            logical[..., 1, 2],
            logical[..., 2, 2],
        ],
        axis=-1,
    )
    stored = np.transpose(components, (2, 1, 0, 3))

    path = tmp_path / "tensor.h5"
    tensor_dtype = np.dtype((np.float64, (6,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=(nz, ny, nx), dtype=tensor_dtype
        )
        dataset[...] = stored

    restored = load_symmetric_tensor_field(path)
    np.testing.assert_array_equal(restored, logical)


def test_wrong_symmetric_tensor_component_count_is_refused(tmp_path):
    path = tmp_path / "bad_tensor.h5"
    tensor_dtype = np.dtype((np.float64, (5,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=(2, 2, 2), dtype=tensor_dtype
        )
        dataset[...] = np.zeros((2, 2, 2, 5))

    with pytest.raises(ValueError, match="expected 6 components"):
        load_symmetric_tensor_field(path)
