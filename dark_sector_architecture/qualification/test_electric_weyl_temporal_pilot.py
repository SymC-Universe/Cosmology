from __future__ import annotations

import json
import pathlib
import sys

import h5py
import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_electric_weyl_temporal_pilot import build_report


def _write_scalar(path: pathlib.Path, logical: np.ndarray):
    with h5py.File(path, "w") as handle:
        handle.create_dataset("data", data=np.transpose(logical, (2, 1, 0)))


def _write_vector(path: pathlib.Path, logical: np.ndarray):
    stored = np.moveaxis(logical, 0, -1)
    stored = np.transpose(stored, (2, 1, 0, 3))
    dtype = np.dtype((np.float64, (3,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=stored.shape[:3], dtype=dtype
        )
        dataset[...] = stored


def _write_symmetric_tensor(path: pathlib.Path, logical: np.ndarray):
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
    dtype = np.dtype((np.float64, (6,)))
    with h5py.File(path, "w") as handle:
        dataset = handle.create_dataset(
            "data", shape=stored.shape[:3], dtype=dtype
        )
        dataset[...] = stored


def test_temporal_pilot_end_to_end_on_synthetic_latfield_fields(tmp_path):
    n = 8
    x = np.arange(n) / n
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi

    tau = np.array([0.100, 0.111, 0.125, 0.142, 0.162])
    requested_z = [99.5, 99.25, 99.0, 98.75, 98.5]
    actual_z = [99.49, 99.24, 98.99, 98.74, 98.49]

    for index, t in enumerate(tau):
        phi = 1.0e-5 * np.cos(k * xx)
        chi = 1.0e-7 * np.cos(k * yy)

        b = np.zeros((3, n, n, n))
        b[1] = 2.0e-7 * np.sin(k * xx) * np.sin(2.0 * t)

        h = np.zeros((n, n, n, 3, 3))
        amp = 3.0e-8 * np.cos(k * zz) * np.cos(3.0 * t)
        h[..., 0, 0] = amp
        h[..., 1, 1] = -amp

        stem = tmp_path / f"synthetic_snap{index:03d}"
        _write_scalar(pathlib.Path(str(stem) + "_phi.h5"), phi)
        _write_scalar(pathlib.Path(str(stem) + "_chi.h5"), chi)
        _write_vector(pathlib.Path(str(stem) + "_B.h5"), b)
        _write_symmetric_tensor(pathlib.Path(str(stem) + "_hij.h5"), h)

    metadata = {
        "snapshots": [
            {
                "index": i,
                "requested_redshift": requested_z[i],
                "actual_redshift": actual_z[i],
                "cycle": 10 + 3 * i,
                "tau_over_boxsize": float(tau[i]),
            }
            for i in range(5)
        ]
    }
    metadata_path = tmp_path / "times.json"
    metadata_path.write_text(json.dumps(metadata))

    report, arrays = build_report(
        tmp_path,
        metadata_path,
        boxsize_mpc_over_h=64.0,
    )

    assert report["protocol"] == "P0-Q_ELECTRIC_WEYL_TEMPORAL_PILOT"
    assert report["scientific_claim_tested"] is False
    assert report["scientific_thresholds_frozen"] is False
    assert report["actual_tau_over_boxsize"] == tau.tolist()
    assert report["cycles"] == [10, 13, 16, 19, 22]

    crosscheck = report["constraint_diagnostics"]["continuum_fft_crosscheck"]
    assert crosscheck["status"] == "CROSSCHECK_ONLY_NOT_TRANSVERSALITY_GATE"
    assert crosscheck["B_divergence_rms_by_snapshot"][2] < 1e-18
    assert crosscheck["h_trace_rms_by_snapshot"][2] < 1e-18
    assert report["constraint_diagnostics"]["native_gevolution"] is None

    assert report["sector_frobenius_rms"]["inner"]["scalar"] > 0.0
    assert report["sector_frobenius_rms"]["inner"]["vector"] > 0.0
    assert report["sector_frobenius_rms"]["inner"]["tensor"] > 0.0

    for value in arrays.values():
        assert np.all(np.isfinite(value))

    total = arrays["E_total_inner"]
    np.testing.assert_allclose(
        np.trace(total, axis1=-2, axis2=-1),
        0.0,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        total,
        np.swapaxes(total, -1, -2),
        atol=1e-12,
    )
