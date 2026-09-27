"""Native symmetric-tensor modal extraction for cosmology qualification.

This module is intentionally small and production-facing. The same functions are
used by known-truth qualification tests and later cosmological extraction.

Scientific thresholds are NOT encoded here. Exact/numerical degeneracy is
reported using a machine-precision identity tolerance. Near-degeneracy is
reported continuously through eigengaps and a conditioning proxy so that the
P0-Q suite can earn any later refusal tolerance prospectively.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any

import numpy as np


_MACHINE_EPS = np.finfo(float).eps
_NUMERIC_FACTOR = 256.0


def _numeric_tol(scale: float) -> float:
    """Numerical-identity tolerance, not a scientific decision threshold."""
    return _NUMERIC_FACTOR * _MACHINE_EPS * max(1.0, float(scale))


def _canonicalize_eigenvectors(vectors: np.ndarray) -> np.ndarray:
    """Fix arbitrary eigenvector signs for reproducible reporting."""
    out = np.array(vectors, dtype=float, copy=True)
    for column in range(out.shape[1]):
        pivot = int(np.argmax(np.abs(out[:, column])))
        if out[pivot, column] < 0.0:
            out[:, column] *= -1.0
    return out


@dataclass(frozen=True)
class TensorModalResult:
    matrix: np.ndarray
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray
    eigengaps: np.ndarray
    normalized_eigengaps: np.ndarray
    degenerate_pairs: tuple[bool, bool]
    directional_condition_number: float
    invariants: dict[str, float]
    symmetry_residual: float

    def as_jsonable(self) -> dict[str, Any]:
        return {
            "matrix": self.matrix.tolist(),
            "eigenvalues": self.eigenvalues.tolist(),
            "eigenvectors": self.eigenvectors.tolist(),
            "eigengaps": self.eigengaps.tolist(),
            "normalized_eigengaps": self.normalized_eigengaps.tolist(),
            "degenerate_pairs": list(self.degenerate_pairs),
            "directional_condition_number": (
                None
                if not math.isfinite(self.directional_condition_number)
                else float(self.directional_condition_number)
            ),
            "invariants": {k: float(v) for k, v in self.invariants.items()},
            "symmetry_residual": float(self.symmetry_residual),
        }


def analyze_symmetric_tensor(matrix: np.ndarray) -> TensorModalResult:
    """Return ordered eigensystem, invariants, and conditioning diagnostics.

    The input must already represent a physically symmetric tensor. This
    function refuses materially non-symmetric input rather than silently
    symmetrizing it.
    """
    tensor = np.asarray(matrix, dtype=float)
    if tensor.shape != (3, 3):
        raise ValueError("tensor must be a 3x3 matrix")
    if not np.all(np.isfinite(tensor)):
        raise ValueError("tensor entries must be finite")

    matrix_scale = max(1.0, float(np.linalg.norm(tensor, ord="fro")))
    symmetry_residual = float(np.linalg.norm(tensor - tensor.T, ord="fro"))
    if symmetry_residual > _numeric_tol(matrix_scale):
        raise ValueError(
            "tensor must be symmetric within numerical identity tolerance; "
            f"residual={symmetry_residual:.6e}"
        )

    eigenvalues, eigenvectors = np.linalg.eigh(tensor)
    order = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[order]
    eigenvectors = _canonicalize_eigenvectors(eigenvectors[:, order])

    eigengaps = np.array(
        [
            abs(float(eigenvalues[0] - eigenvalues[1])),
            abs(float(eigenvalues[1] - eigenvalues[2])),
        ],
        dtype=float,
    )

    eigen_scale = max(1.0, float(np.max(np.abs(eigenvalues))))
    normalized_eigengaps = eigengaps / eigen_scale
    identity_tol = _numeric_tol(eigen_scale)
    degenerate_pairs = tuple(bool(gap <= identity_tol) for gap in eigengaps)

    min_gap = float(np.min(eigengaps))
    directional_condition_number = (
        math.inf if min_gap <= identity_tol else eigen_scale / min_gap
    )

    invariants = {
        "trace": float(np.trace(tensor)),
        "trace_square": float(np.trace(tensor @ tensor)),
        "determinant": float(np.linalg.det(tensor)),
        "frobenius_norm": float(np.linalg.norm(tensor, ord="fro")),
    }

    return TensorModalResult(
        matrix=tensor,
        eigenvalues=eigenvalues,
        eigenvectors=eigenvectors,
        eigengaps=eigengaps,
        normalized_eigengaps=normalized_eigengaps,
        degenerate_pairs=degenerate_pairs,
        directional_condition_number=directional_condition_number,
        invariants=invariants,
        symmetry_residual=symmetry_residual,
    )


def rotation_matrix(axis: np.ndarray, angle_radians: float) -> np.ndarray:
    """Rodrigues rotation matrix for qualification controls."""
    axis = np.asarray(axis, dtype=float)
    if axis.shape != (3,):
        raise ValueError("axis must have shape (3,)")
    norm = float(np.linalg.norm(axis))
    if not math.isfinite(norm) or norm == 0.0:
        raise ValueError("axis must be finite and nonzero")

    x, y, z = axis / norm
    c = math.cos(float(angle_radians))
    s = math.sin(float(angle_radians))
    one_minus_c = 1.0 - c

    return np.array(
        [
            [
                c + x * x * one_minus_c,
                x * y * one_minus_c - z * s,
                x * z * one_minus_c + y * s,
            ],
            [
                y * x * one_minus_c + z * s,
                c + y * y * one_minus_c,
                y * z * one_minus_c - x * s,
            ],
            [
                z * x * one_minus_c - y * s,
                z * y * one_minus_c + x * s,
                c + z * z * one_minus_c,
            ],
        ],
        dtype=float,
    )


def rotate_tensor(matrix: np.ndarray, rotation: np.ndarray) -> np.ndarray:
    """Rotate a rank-2 Cartesian tensor as R S R^T."""
    tensor = np.asarray(matrix, dtype=float)
    rotation = np.asarray(rotation, dtype=float)
    if tensor.shape != (3, 3) or rotation.shape != (3, 3):
        raise ValueError("matrix and rotation must both be 3x3")
    return rotation @ tensor @ rotation.T


def eigenframe_alignment(
    first: TensorModalResult, second: TensorModalResult
) -> np.ndarray:
    """Absolute pairwise cosine matrix between ordered eigenframes.

    Absolute values remove the physically irrelevant eigenvector sign.
    Interpretation of columns/rows inside an exactly degenerate eigenspace must
    be refused by the caller.
    """
    return np.abs(first.eigenvectors.T @ second.eigenvectors)


def perturbation_direction_bound(
    result: TensorModalResult, perturbation_operator_norm: float
) -> float:
    """Davis-Kahan style continuous direction-sensitivity proxy.

    This is a diagnostic, not a calibrated uncertainty interval or refusal
    threshold. Infinite is returned for numerically degenerate eigenvalues.
    """
    perturbation_operator_norm = float(perturbation_operator_norm)
    if perturbation_operator_norm < 0.0 or not math.isfinite(perturbation_operator_norm):
        raise ValueError("perturbation_operator_norm must be finite and nonnegative")

    min_gap = float(np.min(result.eigengaps))
    if min_gap <= _numeric_tol(max(1.0, float(np.max(np.abs(result.eigenvalues))))):
        return math.inf
    return perturbation_operator_norm / min_gap
