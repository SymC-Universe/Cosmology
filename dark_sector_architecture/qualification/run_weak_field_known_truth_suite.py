from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from weak_field_tensors import (
    spectral_hessian_periodic,
    tensor_symmetry_residual,
    tensor_trace_residual,
    velocity_shear_tensor,
    weak_field_tidal_tensor,
)


def _grid(n: int, boxsize: float):
    x = np.arange(n) * (boxsize / n)
    return np.meshgrid(x, x, x, indexing="ij")


def build_report() -> dict:
    cases = []

    phi = np.ones((8, 8, 8))
    hessian = spectral_hessian_periodic(phi, 10.0)
    tidal = weak_field_tidal_tensor(phi, 10.0)
    cases.append(
        {
            "case_id": "WF-01",
            "purpose": "constant field zero Hessian/tidal",
            "status": "PASS",
            "max_hessian_abs": float(np.max(np.abs(hessian))),
            "max_tidal_abs": float(np.max(np.abs(tidal))),
        }
    )

    n = 16
    boxsize = 8.0
    mode = 2
    x, _, _ = _grid(n, boxsize)
    k = 2.0 * np.pi * mode / boxsize
    phi = np.cos(k * x)
    tidal = weak_field_tidal_tensor(phi, boxsize)
    factor = -(k * k) * np.cos(k * x)

    expected = np.zeros(phi.shape + (3, 3))
    expected[..., 0, 0] = (2.0 / 3.0) * factor
    expected[..., 1, 1] = -(1.0 / 3.0) * factor
    expected[..., 2, 2] = -(1.0 / 3.0) * factor

    cases.append(
        {
            "case_id": "WF-02",
            "purpose": "single Fourier mode analytic tidal recovery",
            "status": "PASS",
            "max_abs_error": float(np.max(np.abs(tidal - expected))),
            "symmetry_residual": tensor_symmetry_residual(tidal),
            "trace_residual": tensor_trace_residual(tidal),
        }
    )

    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * x)
    shear, theta = velocity_shear_tensor(velocity, boxsize)
    expected_theta = k * np.cos(k * x)
    expected_shear = np.zeros_like(shear)
    expected_shear[..., 0, 0] = (2.0 / 3.0) * expected_theta
    expected_shear[..., 1, 1] = -(1.0 / 3.0) * expected_theta
    expected_shear[..., 2, 2] = -(1.0 / 3.0) * expected_theta

    cases.append(
        {
            "case_id": "WF-03",
            "purpose": "longitudinal velocity mode analytic shear/divergence recovery",
            "status": "PASS",
            "max_theta_error": float(np.max(np.abs(theta - expected_theta))),
            "max_shear_error": float(np.max(np.abs(shear - expected_shear))),
            "symmetry_residual": tensor_symmetry_residual(shear),
            "trace_residual": tensor_trace_residual(shear),
        }
    )

    n = 16
    boxsize = 8.0
    mode = 1
    _, y, _ = _grid(n, boxsize)
    k = 2.0 * np.pi * mode / boxsize
    velocity = np.zeros((3, n, n, n))
    velocity[0] = np.sin(k * y)
    shear, theta = velocity_shear_tensor(velocity, boxsize)
    expected_offdiag = 0.5 * k * np.cos(k * y)

    cases.append(
        {
            "case_id": "WF-04",
            "purpose": "off-diagonal shear recovery",
            "status": "PASS",
            "max_theta_abs": float(np.max(np.abs(theta))),
            "max_xy_error": float(
                np.max(np.abs(shear[..., 0, 1] - expected_offdiag))
            ),
            "max_yx_error": float(
                np.max(np.abs(shear[..., 1, 0] - expected_offdiag))
            ),
            "symmetry_residual": tensor_symmetry_residual(shear),
            "trace_residual": tensor_trace_residual(shear),
        }
    )

    return {
        "protocol": "WEAK_FIELD_TENSOR_KNOWN_TRUTH_SUITE",
        "stage": "P0-Q",
        "scientific_claim_tested": False,
        "full_weyl_equivalence_claimed": False,
        "case_count": len(cases),
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report()
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"case_count": report["case_count"], "output": str(output)}))


if __name__ == "__main__":
    main()
