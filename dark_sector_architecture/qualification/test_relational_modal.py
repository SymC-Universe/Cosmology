from __future__ import annotations

import pathlib
import sys

import numpy as np
import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from relational_modal import (
    normalized_commutator_kappa,
    ordered_eigenvalues,
    relational_modal_record,
)


def _rotation_z(theta: float) -> np.ndarray:
    c = np.cos(theta)
    s = np.sin(theta)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def _random_rotation(rng: np.random.Generator) -> np.ndarray:
    q, r = np.linalg.qr(rng.normal(size=(3, 3)))
    signs = np.sign(np.diag(r))
    signs[signs == 0.0] = 1.0
    q = q @ np.diag(signs)
    if np.linalg.det(q) < 0.0:
        q[:, 0] *= -1.0
    return q


def _stf_from_random(rng: np.random.Generator) -> np.ndarray:
    raw = rng.normal(size=(3, 3))
    sym = 0.5 * (raw + raw.T)
    return sym - np.eye(3) * np.trace(sym) / 3.0


def test_rm01_common_eigenframe_has_zero_kappa():
    a = np.diag([-1.0, 0.2, 0.8])
    b = np.diag([-2.0, 0.5, 1.5])
    value = float(normalized_commutator_kappa(a, b))
    assert value == pytest.approx(0.0, abs=1e-15)


def test_rm02_matched_marginals_rotation_changes_only_relation():
    a = np.diag([-1.0, 0.2, 0.8])
    b0 = np.diag([-2.0, 0.5, 1.5])
    q = _rotation_z(np.deg2rad(31.0))
    b1 = q @ b0 @ q.T

    np.testing.assert_allclose(
        ordered_eigenvalues(b1), ordered_eigenvalues(b0), atol=1e-14, rtol=1e-14
    )
    for power in (2, 3):
        assert np.trace(np.linalg.matrix_power(b1, power)) == pytest.approx(
            np.trace(np.linalg.matrix_power(b0, power)), abs=1e-13
        )

    k0 = float(normalized_commutator_kappa(a, b0))
    k1 = float(normalized_commutator_kappa(a, b1))
    assert k0 == pytest.approx(0.0, abs=1e-15)
    assert k1 > 0.0


def test_rm03_simultaneous_coordinate_rotation_invariance():
    rng = np.random.default_rng(301)
    a = _stf_from_random(rng)
    b = _stf_from_random(rng)
    q = _random_rotation(rng)

    baseline = float(normalized_commutator_kappa(a, b))
    rotated = float(normalized_commutator_kappa(q @ a @ q.T, q @ b @ q.T))
    assert rotated == pytest.approx(baseline, abs=2e-14, rel=2e-14)


def test_rm04_exchange_symmetry():
    rng = np.random.default_rng(302)
    a = _stf_from_random(rng)
    b = _stf_from_random(rng)
    assert float(normalized_commutator_kappa(a, b)) == pytest.approx(
        float(normalized_commutator_kappa(b, a)), abs=1e-15, rel=1e-15
    )


def test_rm05_boettcher_wenzel_bound_on_deterministic_ensemble():
    rng = np.random.default_rng(303)
    values = []
    for _ in range(512):
        a = _stf_from_random(rng)
        b = _stf_from_random(rng)
        values.append(float(normalized_commutator_kappa(a, b)))
    values = np.asarray(values)
    assert np.all(np.isfinite(values))
    assert np.min(values) >= -1e-14
    assert np.max(values) <= 1.0 + 1e-12


def test_rm06_zero_norm_is_refused_not_interpreted_as_alignment():
    a = np.zeros((3, 3))
    b = np.diag([-2.0, 0.5, 1.5])
    record = relational_modal_record(a, b)
    assert np.isnan(float(record["kappa"]))
    assert record["refusal_status"].item() == "REFUSED_ZERO_NORM_A"
    assert record["direction_status"].item() == "REFUSED"


def test_rm06_nonfinite_and_shape_refusals_are_explicit():
    bad = np.eye(3)
    bad[0, 0] = np.nan
    good = np.diag([-1.0, 0.2, 0.8])
    record = relational_modal_record(bad, good)
    assert record["refusal_status"] == "REFUSED_NONFINITE"
    assert record["kappa"] is None

    record = relational_modal_record(np.zeros((2, 2)), good)
    assert record["refusal_status"] == "REFUSED_SHAPE"
    assert record["kappa"] is None


def test_rm07_degenerate_tensor_keeps_kappa_but_refuses_direction():
    a = np.diag([1.0, 1.0, -2.0])
    q = _rotation_z(np.deg2rad(23.0))
    b0 = np.diag([-2.0, 0.3, 1.7])
    b = q @ b0 @ q.T
    record = relational_modal_record(a, b)
    assert np.isfinite(float(record["kappa"]))
    assert bool(record["degenerate_a"])
    assert record["direction_status"].item() == "DEGENERATE_NONIDENTIFIABLE"
    assert record["refusal_status"].item() == "OK"


def test_low_level_nonfinite_refuses_via_exception():
    a = np.diag([-1.0, 0.2, 0.8])
    b = np.array(a, copy=True)
    b[0, 0] = np.inf
    with pytest.raises(ValueError, match="non-finite"):
        normalized_commutator_kappa(a, b)
