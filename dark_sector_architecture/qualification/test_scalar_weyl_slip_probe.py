from __future__ import annotations

import pathlib
import sys

import h5py
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_scalar_weyl_slip_probe import build_report


def _write_scalar(path, logical):
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=np.transpose(logical, (2, 1, 0)))


def test_zero_slip_produces_exact_legacy_identity(tmp_path):
    n = 8
    box = 64.0
    x = np.arange(n) * box / n
    xx, yy, _ = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi / box
    phi = np.cos(k * xx) + 0.3 * np.sin(k * yy)
    chi = np.zeros_like(phi)

    phi_path = tmp_path / "phi.h5"
    chi_path = tmp_path / "chi.h5"
    _write_scalar(phi_path, phi)
    _write_scalar(chi_path, chi)

    report = build_report(phi_path, chi_path, box)

    assert report["potential_statistics"]["chi_rms_over_phi_rms"] == 0.0
    assert (
        report["tensor_difference"]["operator_error_quantiles"]["max"]
        == 0.0
    )
    for item in report["tensor_difference"][
        "eigenframe_diagonal_alignment_quantiles_by_order"
    ]:
        assert item["min"] > 1.0 - 1e-12


def test_proportional_slip_preserves_axes_and_scales_tensor(tmp_path):
    n = 8
    box = 64.0
    x = np.arange(n) * box / n
    xx, yy, _ = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi / box
    phi = np.cos(k * xx) + 0.4 * np.cos(2.0 * k * yy)
    chi = 0.2 * phi

    phi_path = tmp_path / "phi.h5"
    chi_path = tmp_path / "chi.h5"
    _write_scalar(phi_path, phi)
    _write_scalar(chi_path, chi)

    report = build_report(phi_path, chi_path, box)

    assert abs(report["potential_statistics"]["chi_rms_over_phi_rms"] - 0.2) < 1e-12
    median_rel = report["tensor_difference"][
        "relative_operator_error_quantiles"
    ]["median"]
    assert abs(median_rel - 0.1) < 1e-10
    for item in report["tensor_difference"][
        "eigenframe_diagonal_alignment_quantiles_by_order"
    ]:
        assert item["median"] > 1.0 - 1e-12
