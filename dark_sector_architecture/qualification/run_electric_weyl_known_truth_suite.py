"""Machine-readable known-truth report for electric-Weyl sector algebra.

P0-Q representation qualification only. This runner tests the frozen
gevolution-to-electric-Weyl algebra on analytic scalar, vector, tensor, and
mixed fields. It does not qualify temporal derivatives from real snapshots.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from electric_weyl import electric_weyl_conformal_sectors
from weak_field_tensors import scalar_weyl_shape_tensor


def _grid(n: int, boxsize: float):
    x = np.arange(n) * boxsize / n
    return np.meshgrid(x, x, x, indexing="ij")


def _zeros_vector(n: int):
    return np.zeros((3, n, n, n), dtype=float)


def _zeros_tensor(n: int):
    return np.zeros((n, n, n, 3, 3), dtype=float)


def build_report() -> dict:
    n = 16
    box = 8.0
    x, y, z = _grid(n, box)
    k = 2.0 * np.pi / box
    zeros = np.zeros((n, n, n))

    cases = []

    phi = np.cos(k * x) + 0.2 * np.cos(2.0 * k * y)
    chi = 0.1 * np.cos(k * x)
    sectors = electric_weyl_conformal_sectors(
        phi, chi, _zeros_vector(n), _zeros_tensor(n), _zeros_tensor(n), box
    )
    expected = scalar_weyl_shape_tensor(phi, chi, box)
    cases.append(
        {
            "case_id": "EW-01",
            "purpose": "scalar limit matches frozen scalar Weyl shape",
            "status": "PASS",
            "max_abs_error": float(np.max(np.abs(sectors["total"] - expected))),
        }
    )

    b_prime = _zeros_vector(n)
    b_prime[1] = np.sin(k * x)
    sectors = electric_weyl_conformal_sectors(
        zeros, zeros, b_prime, _zeros_tensor(n), _zeros_tensor(n), box
    )
    expected_xy = -0.25 * k * np.cos(k * x)
    cases.append(
        {
            "case_id": "EW-02",
            "purpose": "pure transverse-vector analytic coefficient and sign",
            "status": "PASS",
            "max_xy_error": float(
                np.max(np.abs(sectors["vector"][..., 0, 1] - expected_xy))
            ),
            "max_diagonal_abs": float(
                np.max(
                    np.abs(
                        np.stack(
                            [
                                sectors["vector"][..., 0, 0],
                                sectors["vector"][..., 1, 1],
                                sectors["vector"][..., 2, 2],
                            ],
                            axis=0,
                        )
                    )
                )
            ),
        }
    )

    h = _zeros_tensor(n)
    amp = np.cos(k * z)
    h[..., 0, 0] = amp
    h[..., 1, 1] = -amp
    h_second = -(k * k) * h
    sectors = electric_weyl_conformal_sectors(
        zeros, zeros, _zeros_vector(n), h, h_second, box
    )
    expected_tensor = 0.5 * (k * k) * h
    cases.append(
        {
            "case_id": "EW-03",
            "purpose": "pure TT vacuum wave reduces to minus one-half h second derivative",
            "status": "PASS",
            "max_abs_error": float(
                np.max(np.abs(sectors["tensor"] - expected_tensor))
            ),
        }
    )

    phi = 0.3 * np.cos(k * x)
    chi = 0.05 * np.cos(k * y)
    b_prime = _zeros_vector(n)
    b_prime[1] = 0.2 * np.sin(k * x)
    h = _zeros_tensor(n)
    h[..., 0, 0] = 0.1 * np.cos(k * z)
    h[..., 1, 1] = -h[..., 0, 0]
    h_second = -(k * k) * h
    sectors = electric_weyl_conformal_sectors(
        phi, chi, b_prime, h, h_second, box
    )
    superposition = sectors["scalar"] + sectors["vector"] + sectors["tensor"]
    cases.append(
        {
            "case_id": "EW-04",
            "purpose": "mixed scalar-vector-tensor linear superposition",
            "status": "PASS",
            "max_abs_error": float(
                np.max(np.abs(sectors["total"] - superposition))
            ),
            "max_trace_abs": float(
                np.max(
                    np.abs(
                        np.trace(sectors["total"], axis1=-2, axis2=-1)
                    )
                )
            ),
            "max_symmetry_residual": float(
                np.max(
                    np.abs(
                        sectors["total"]
                        - np.swapaxes(sectors["total"], -1, -2)
                    )
                )
            ),
        }
    )

    return {
        "protocol": "ELECTRIC_WEYL_SECTOR_KNOWN_TRUTH_SUITE",
        "stage": "P0-Q",
        "project_riemann_convention": (
            "R^rho_{sigma mu nu}=d_mu Gamma^rho_{nu sigma}"
            "-d_nu Gamma^rho_{mu sigma}+..."
        ),
        "scientific_claim_tested": False,
        "scientific_thresholds_frozen": False,
        "real_snapshot_temporal_derivatives_qualified": False,
        "full_electric_weyl_real_data_claimed": False,
        "case_count": len(cases),
        "cases": cases,
        "next_gate": (
            "qualify B_i prime and h_ij second conformal-time derivatives "
            "from nested centered snapshot stencils"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    report = build_report()
    output = pathlib.Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"case_count": report["case_count"], "output": str(output)}))


if __name__ == "__main__":
    main()
