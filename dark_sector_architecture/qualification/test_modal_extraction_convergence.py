from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_modal_extraction_convergence import build_report
from weak_field_tensors import velocity_shear_tensor, weak_field_tidal_tensor


def test_qr1_report_is_measurement_only_and_finite(tmp_path):
    n = 8
    boxsize = 8.0
    x = np.arange(n) * (boxsize / n)
    xx, yy, zz = np.meshgrid(x, x, x, indexing="ij")
    k = 2.0 * np.pi / boxsize

    phi = (
        np.cos(k * xx)
        + 0.25 * np.cos(k * yy)
        + 0.1 * np.cos(k * zz)
    )
    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * xx)
    velocity[1] = 0.4 * np.sin(k * yy)
    velocity[2] = 0.2 * np.sin(k * zz)

    tidal = weak_field_tidal_tensor(phi, boxsize)
    shear, theta = velocity_shear_tensor(velocity, boxsize)

    path = tmp_path / "development.npz"
    np.savez_compressed(
        path,
        phi=phi,
        velocity=velocity,
        tidal_tensor=tidal,
        shear_tensor=shear,
        theta=theta,
    )

    report = build_report(path, boxsize, factors=(2, 4))

    assert report["protocol"] == "Q-R1_MODAL_EXTRACTION_RESOLUTION"
    assert report["scientific_claim_tested"] is False
    assert report["scientific_thresholds_frozen"] is False
    assert report["simulation_resolution_tested"] is False
    assert len(report["levels"]) == 2

    assert report["levels"][0]["coarse_grid_shape"] == [4, 4, 4]
    assert report["levels"][1]["coarse_grid_shape"] == [2, 2, 2]

    for level in report["levels"]:
        for family in ("tidal", "shear"):
            q = level[family]["operator_error_quantiles"]
            assert q["finite_count"] == q["total_count"]
            assert q["min"] is not None
        theta_q = level["theta_abs_error_quantiles"]
        assert theta_q["finite_count"] == theta_q["total_count"]
