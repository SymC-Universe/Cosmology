"""Relational modal diagnostics for pairs of native symmetric tensors.

This module represents information carried by the relationship between two
symmetric modal tensors, such as electric Weyl E_ij and velocity shear
sigma_ij. It deliberately preserves the full relational object instead of
reducing the relation to one scalar.

No scientific acceptance threshold is encoded here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from modal_tensor import TensorModalResult, analyze_symmetric_tensor, eigenframe_alignment


@dataclass(frozen=True)
class RelationalModalResult:
    first: TensorModalResult
    second: TensorModalResult
    alignment_matrix_abs: np.ndarray
    commutator: np.ndarray
    commutator_axial_vector: np.ndarray
    commutator_frobenius_norm: float
    normalized_commutator_frobenius: float | None

    def as_jsonable(self) -> dict[str, Any]:
        return {
            "first": self.first.as_jsonable(),
            "second": self.second.as_jsonable(),
            "alignment_matrix_abs": self.alignment_matrix_abs.tolist(),
            "commutator": self.commutator.tolist(),
            "commutator_axial_vector": self.commutator_axial_vector.tolist(),
            "commutator_frobenius_norm": float(self.commutator_frobenius_norm),
            "normalized_commutator_frobenius": (
                None
                if self.normalized_commutator_frobenius is None
                else float(self.normalized_commutator_frobenius)
            ),
            "unique_axis_interpretation_licensed": bool(
                not any(self.first.degenerate_pairs)
                and not any(self.second.degenerate_pairs)
            ),
        }


def _commutator_axial(commutator: np.ndarray) -> np.ndarray:
    """Return the axial vector of a 3x3 antisymmetric commutator."""
    k = np.asarray(commutator, dtype=float)
    if k.shape != (3, 3):
        raise ValueError("commutator must be 3x3")
    return np.array([k[2, 1], k[0, 2], k[1, 0]], dtype=float)


def analyze_tensor_relation(
    first_matrix: np.ndarray, second_matrix: np.ndarray
) -> RelationalModalResult:
    """Analyze the coordinate-covariant relation between two symmetric tensors.

    The commutator vanishes exactly when the two real symmetric tensors are
    simultaneously diagonalizable. The absolute alignment matrix is useful
    when both spectra have identifiable eigen-directions. Exact degeneracy is
    retained as a refusal flag rather than resolved by arbitrary axis choices.
    """
    first = analyze_symmetric_tensor(first_matrix)
    second = analyze_symmetric_tensor(second_matrix)

    commutator = first.matrix @ second.matrix - second.matrix @ first.matrix
    antisymmetry_residual = np.linalg.norm(commutator + commutator.T, ord="fro")
    scale = max(1.0, float(np.linalg.norm(commutator, ord="fro")))
    if antisymmetry_residual > 1024.0 * np.finfo(float).eps * scale:
        raise ValueError("symmetric-tensor commutator is not numerically antisymmetric")

    comm_norm = float(np.linalg.norm(commutator, ord="fro"))
    denominator = (
        float(first.invariants["frobenius_norm"])
        * float(second.invariants["frobenius_norm"])
    )
    normalized = comm_norm / denominator if denominator > 0.0 else None

    return RelationalModalResult(
        first=first,
        second=second,
        alignment_matrix_abs=eigenframe_alignment(first, second),
        commutator=commutator,
        commutator_axial_vector=_commutator_axial(commutator),
        commutator_frobenius_norm=comm_norm,
        normalized_commutator_frobenius=normalized,
    )


def relation_under_common_rotation(
    first_matrix: np.ndarray,
    second_matrix: np.ndarray,
    rotation: np.ndarray,
) -> RelationalModalResult:
    """Convenience control for a common passive/active Cartesian rotation."""
    r = np.asarray(rotation, dtype=float)
    if r.shape != (3, 3):
        raise ValueError("rotation must be 3x3")
    return analyze_tensor_relation(
        r @ np.asarray(first_matrix, dtype=float) @ r.T,
        r @ np.asarray(second_matrix, dtype=float) @ r.T,
    )
