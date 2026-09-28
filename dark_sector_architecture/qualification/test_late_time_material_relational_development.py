from __future__ import annotations

import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from run_late_time_material_relational_development import (
    _cv_sse,
    _octant_labels,
    _patch_coords,
    _primary_disposition,
    _shift_relation,
    _standardized_lstsq_predict,
    band_l_modes,
)


def test_lmr01_band_l_is_frozen_250_mode_sphere():
    modes = band_l_modes(64)
    assert len(modes) == 250
    assert (0, 0, 0) not in modes
    assert all(0 < nx*nx + ny*ny + nz*nz < 16 for nx, ny, nz in modes)


def test_lmr02_patch_coordinate_roundtrip_and_octants():
    pid = np.arange(512)
    coords = _patch_coords(pid, 8)
    rebuilt = coords[:,0]*64 + coords[:,1]*8 + coords[:,2]
    np.testing.assert_array_equal(rebuilt, pid)
    labels = _octant_labels(pid, 8)
    unique, counts = np.unique(labels, return_counts=True)
    np.testing.assert_array_equal(unique, np.arange(8))
    np.testing.assert_array_equal(counts, np.full(8, 64))


def test_lmr03_standardized_ols_recovers_linear_multioutput_known_truth():
    rng = np.random.default_rng(8)
    x = rng.normal(size=(300, 6))
    beta = rng.normal(size=(7, 4))
    design = np.column_stack([np.ones(len(x)), x])
    y = design @ beta
    pred, diag = _standardized_lstsq_predict(x[:240], y[:240], x[240:])
    np.testing.assert_allclose(pred, y[240:], atol=1e-11, rtol=1e-11)
    assert diag["prediction_finite"] is True


def test_lmr04_octant_cv_prefers_planted_relational_signal():
    rng = np.random.default_rng(9)
    pid = np.arange(512)
    folds = _octant_labels(pid, 8)
    b0 = rng.normal(size=(512, 8))
    rel = rng.normal(size=(512, 10))
    beta0 = rng.normal(size=(8, 4))*0.05
    betar = rng.normal(size=(10, 4))
    y = b0 @ beta0 + rel @ betar

    s0, _, _ = _cv_sse(b0, y, folds)
    s1, _, _ = _cv_sse(np.column_stack([b0, rel]), y, folds)
    assert s1 < s0 * 1e-10


def test_lmr05_persistence_can_beat_both_models_and_blocks_signal():
    primary = {
        "delta_rel": 0.2,
        "sse_b0": 10.0,
        "sse_b1": 8.0,
        "sse_persistence": 2.0,
        "shift_null": {
            "finite_shift_count": 511,
            "delta_rel_q05": -0.1,
            "delta_rel_q95": 0.1,
        },
    }
    sensitivity = [{"delta_rel": 0.1}]
    assert _primary_disposition(primary, sensitivity) == "DEVELOPMENT_EQUIVALENT_OR_UNRESOLVED"


def test_lmr06_frozen_signal_rule_requires_all_three_conditions():
    primary = {
        "delta_rel": 0.2,
        "sse_b0": 10.0,
        "sse_b1": 8.0,
        "sse_persistence": 9.0,
        "shift_null": {
            "finite_shift_count": 511,
            "delta_rel_q05": -0.1,
            "delta_rel_q95": 0.1,
        },
    }
    sensitivity = [{"delta_rel": 0.05}, {"delta_rel": 0.15}]
    assert _primary_disposition(primary, sensitivity) == "DEVELOPMENT_SIGNAL_PRESENT"


def test_lmr07_contradictory_patch_scale_forces_need_more_info():
    primary = {
        "delta_rel": 0.2,
        "sse_b0": 10.0,
        "sse_b1": 8.0,
        "sse_persistence": 9.0,
        "shift_null": {
            "finite_shift_count": 511,
            "delta_rel_q05": -0.1,
            "delta_rel_q95": 0.1,
        },
    }
    sensitivity = [{"delta_rel": -0.02}, {"delta_rel": 0.1}]
    assert _primary_disposition(primary, sensitivity) == "NEED_MORE_INFO"


def test_lmr08_shift_relation_is_periodic_and_moves_whole_block():
    pid = np.arange(512)
    rel = np.column_stack([pid, pid+1]).astype(float)
    shifted, keep = _shift_relation(pid, rel, 8, (1, 0, 0))
    assert np.all(keep)
    coords = _patch_coords(pid, 8)
    source = (coords - np.array([1,0,0])) % 8
    source_pid = source[:,0]*64 + source[:,1]*8 + source[:,2]
    np.testing.assert_allclose(shifted[:,0], source_pid)


def test_lmr09_subtracts_when_b1_worse_than_b0_and_persistence():
    primary = {
        "delta_rel": -0.3,
        "sse_b0": 10.0,
        "sse_b1": 13.0,
        "sse_persistence": 11.0,
        "shift_null": {
            "finite_shift_count": 511,
            "delta_rel_q05": -0.1,
            "delta_rel_q95": 0.1,
        },
    }
    assert _primary_disposition(primary, [{"delta_rel": -0.2}]) == "DEVELOPMENT_SUBTRACTS"
