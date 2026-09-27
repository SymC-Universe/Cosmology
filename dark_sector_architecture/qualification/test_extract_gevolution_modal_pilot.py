from __future__ import annotations

import pathlib
import sys

import h5py
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from extract_gevolution_modal_pilot import extract


def _write_scalar(path, logical):
    stored = np.transpose(logical, (2, 1, 0))
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=stored)


def _write_vector(path, logical):
    stored = np.moveaxis(logical, 0, -1)
    stored = np.transpose(stored, (2, 1, 0, 3))
    dtype = np.dtype((np.float64, (3,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=stored.shape[:3], dtype=dtype
        )
        dataset[...] = stored


def test_end_to_end_extract_on_synthetic_latfield_hdf5(tmp_path):
    n = 8
    boxsize = 8.0
    x = np.arange(n) * (boxsize / n)
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi / boxsize

    phi = np.cos(k * xx) + 0.3 * np.cos(2.0 * k * yy)

    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * xx)
    velocity[1] = 0.4 * np.sin(k * zz)

    phi_path = tmp_path / "phi.h5"
    velocity_path = tmp_path / "v.h5"
    _write_scalar(phi_path, phi)
    _write_vector(velocity_path, velocity)

    summary, arrays = extract(phi_path, velocity_path, boxsize)

    assert summary["grid_shape"] == [n, n, n]
    assert summary["scientific_claim_tested"] is False
    assert summary["scientific_thresholds_frozen"] is False
    assert summary["full_weyl_equivalence_claimed"] is False

    assert summary["tidal"]["symmetry_residual"] < 1e-12
    assert summary["tidal"]["trace_residual"] < 1e-12
    assert summary["shear"]["symmetry_residual"] < 1e-12
    assert summary["shear"]["trace_residual"] < 1e-12

    assert arrays["theta"].shape == (n, n, n)
    assert arrays["tidal_eigenvalues"].shape == (n, n, n, 3)
    assert arrays["shear_eigenvalues"].shape == (n, n, n, 3)
    assert arrays["tidal_eigengaps"].shape == (n, n, n, 2)
    assert arrays["shear_eigengaps"].shape == (n, n, n, 2)
    assert arrays["shear_tidal_alignment"].shape == (n, n, n, 3, 3)

    for value in arrays.values():
        assert np.all(np.isfinite(value))

    np.testing.assert_allclose(
        np.sum(arrays["tidal_eigenvalues"], axis=-1),
        0.0,
        atol=1e-10,
    )
    np.testing.assert_allclose(
        np.sum(arrays["shear_eigenvalues"], axis=-1),
        0.0,
        atol=1e-10,
    )
