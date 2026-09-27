from __future__ import annotations

import pathlib
import sys

import h5py
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_qr2_resolution_pair import build_report


def _field(n: int, box: float):
    x = np.arange(n) * box / n
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi / box
    phi = (
        np.cos(k * xx + 0.31)
        + 0.4 * np.sin(2.0 * k * yy - 0.27)
        + 0.2 * np.cos(k * (xx + zz) + 0.61)
    )
    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * xx + 0.17)
    velocity[1] = 0.5 * np.cos(k * yy - 0.44)
    velocity[2] = 0.25 * np.sin(k * zz + 0.28)
    return phi, velocity


def _write_scalar(path: pathlib.Path, logical: np.ndarray):
    stored = np.transpose(logical, (2, 1, 0))
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=stored)


def _write_vector(path: pathlib.Path, logical: np.ndarray):
    stored = np.moveaxis(logical, 0, -1)
    stored = np.transpose(stored, (2, 1, 0, 3))
    dtype = np.dtype((np.float64, (3,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=stored.shape[:3], dtype=dtype
        )
        dataset[...] = stored


def test_qr2_identical_continuous_modes_are_phase_and_common_grid_identical(tmp_path):
    box = 64.0
    low_phi, low_v = _field(8, box)
    high_phi, high_v = _field(16, box)

    paths = {
        "low_phi": tmp_path / "low_phi.h5",
        "low_v": tmp_path / "low_v.h5",
        "high_phi": tmp_path / "high_phi.h5",
        "high_v": tmp_path / "high_v.h5",
    }
    _write_scalar(paths["low_phi"], low_phi)
    _write_vector(paths["low_v"], low_v)
    _write_scalar(paths["high_phi"], high_phi)
    _write_vector(paths["high_v"], high_v)

    report = build_report(
        paths["low_phi"],
        paths["low_v"],
        paths["high_phi"],
        paths["high_v"],
        box,
    )

    assert report["scientific_claim_tested"] is False
    assert report["scientific_thresholds_frozen"] is False

    assert report["phase_overlap"]["phi"]["circular_phase_coherence"] > 1 - 1e-12
    for item in report["phase_overlap"]["velocity_components"]:
        assert item["circular_phase_coherence"] > 1 - 1e-12

    assert report["common_grid_comparison"]["phi"]["rms_error"] < 1e-12
    for item in report["common_grid_comparison"]["velocity_components"]:
        assert item["rms_error"] < 1e-12

    assert (
        report["common_grid_comparison"]["tidal"]["operator_error_quantiles"]["max"]
        < 1e-12
    )
    assert (
        report["common_grid_comparison"]["shear"]["operator_error_quantiles"]["max"]
        < 1e-12
    )


def test_qr2_slip_corrected_scalar_weyl_is_identical_for_same_continuous_modes(tmp_path):
    box = 64.0
    low_phi, low_v = _field(8, box)
    high_phi, high_v = _field(16, box)
    low_chi = 0.2 * low_phi
    high_chi = 0.2 * high_phi

    paths = {
        "low_phi": tmp_path / "low_phi_slip.h5",
        "low_v": tmp_path / "low_v_slip.h5",
        "low_chi": tmp_path / "low_chi.h5",
        "high_phi": tmp_path / "high_phi_slip.h5",
        "high_v": tmp_path / "high_v_slip.h5",
        "high_chi": tmp_path / "high_chi.h5",
    }
    _write_scalar(paths["low_phi"], low_phi)
    _write_vector(paths["low_v"], low_v)
    _write_scalar(paths["low_chi"], low_chi)
    _write_scalar(paths["high_phi"], high_phi)
    _write_vector(paths["high_v"], high_v)
    _write_scalar(paths["high_chi"], high_chi)

    report = build_report(
        paths["low_phi"],
        paths["low_v"],
        paths["high_phi"],
        paths["high_v"],
        box,
        paths["low_chi"],
        paths["high_chi"],
    )

    assert "chi_gev" in report["phase_overlap"]
    assert "weyl_potential" in report["phase_overlap"]
    assert (
        report["phase_overlap"]["weyl_potential"]["circular_phase_coherence"]
        > 1 - 1e-12
    )
    assert (
        report["common_grid_comparison"]["weyl_potential"]["rms_error"]
        < 1e-12
    )
    assert (
        report["common_grid_comparison"]["scalar_weyl_shape"][
            "operator_error_quantiles"
        ]["max"]
        < 1e-12
    )
