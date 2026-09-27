from __future__ import annotations

import pathlib
import sys

import h5py
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_fixed_band_convergence import build_report


def _write_scalar(path, logical):
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=np.transpose(logical, (2, 1, 0)))


def _write_vector(path, logical):
    stored = np.moveaxis(logical, 0, -1)
    stored = np.transpose(stored, (2, 1, 0, 3))
    dtype = np.dtype((np.float64, (3,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=stored.shape[:3], dtype=dtype
        )
        dataset[...] = stored


def _shared_fields(n, box):
    x = np.arange(n) * box / n
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi / box
    phi = (
        np.cos(k * xx + 0.31)
        + 0.4 * np.sin(2.0 * k * yy - 0.27)
        + 0.2 * np.cos(k * (xx + zz) + 0.61)
    )
    chi = 0.1 * phi
    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * xx + 0.17)
    velocity[1] = 0.5 * np.cos(k * yy - 0.44)
    velocity[2] = 0.25 * np.sin(k * zz + 0.28)
    return phi, chi, velocity


def _paths(tmp_path, n, phi, chi, velocity):
    phi_path = tmp_path / f"phi_{n}.h5"
    chi_path = tmp_path / f"chi_{n}.h5"
    vel_path = tmp_path / f"vel_{n}.h5"
    _write_scalar(phi_path, phi)
    _write_scalar(chi_path, chi)
    _write_vector(vel_path, velocity)
    return phi_path, chi_path, vel_path


def test_identical_shared_modes_are_exact_on_fixed_band(tmp_path):
    box = 64.0
    members = []
    for n in (8, 16, 32):
        members.append(_paths(tmp_path, n, *_shared_fields(n, box)))

    report = build_report(members, target_n=8, boxsize=box)

    assert report["native_grids"] == [8, 16, 32]
    for comparison in report["adjacent_comparisons"]:
        assert comparison["phi"]["rms_error"] < 1e-12
        assert comparison["weyl_potential"]["rms_error"] < 1e-12
        assert (
            comparison["scalar_weyl_shape"]["operator_error_quantiles"]["max"]
            < 1e-12
        )
        assert comparison["shear"]["operator_error_quantiles"]["max"] < 1e-12


def test_high_frequency_content_outside_fixed_band_is_removed(tmp_path):
    box = 64.0
    members = []
    for n in (8, 16, 32):
        phi, chi, velocity = _shared_fields(n, box)
        if n > 8:
            x = np.arange(n) * box / n
            xx, _, _ = np.meshgrid(x, x, x, indexing="ij")
            high_mode = (n // 4) - 1
            phi = phi + 0.7 * np.cos(
                2.0 * np.pi * high_mode * xx / box + 0.12
            )
            chi = chi + 0.03 * np.cos(
                2.0 * np.pi * high_mode * xx / box + 0.12
            )
        members.append(_paths(tmp_path, n, phi, chi, velocity))

    report = build_report(members, target_n=8, boxsize=box)

    for comparison in report["adjacent_comparisons"]:
        assert comparison["phi"]["rms_error"] < 1e-12
        assert (
            comparison["scalar_weyl_shape"]["operator_error_quantiles"]["max"]
            < 1e-12
        )
