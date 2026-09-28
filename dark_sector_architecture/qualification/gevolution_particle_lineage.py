"""Utilities for gevolution particle HDF5 lineage snapshots."""

from __future__ import annotations

import pathlib
import h5py
import numpy as np


FIELDS = (
    "ID",
    "positionX", "positionY", "positionZ",
    "velocityX", "velocityY", "velocityZ",
)


def load_particle_snapshot(path: str | pathlib.Path) -> dict[str, np.ndarray]:
    p = pathlib.Path(path)
    with h5py.File(p, "r") as h:
        if "data" not in h:
            raise ValueError(f"{p}: missing data dataset")
        data = h["data"][...]
    if not data.dtype.names:
        raise ValueError(f"{p}: particle data must be compound dtype")
    missing = [x for x in FIELDS if x not in data.dtype.names]
    if missing:
        raise ValueError(f"{p}: missing particle fields {missing}")
    ids = np.asarray(data["ID"], dtype=np.int64)
    positions = np.column_stack([
        np.asarray(data["positionX"], dtype=float),
        np.asarray(data["positionY"], dtype=float),
        np.asarray(data["positionZ"], dtype=float),
    ])
    velocities = np.column_stack([
        np.asarray(data["velocityX"], dtype=float),
        np.asarray(data["velocityY"], dtype=float),
        np.asarray(data["velocityZ"], dtype=float),
    ])
    if not np.all(np.isfinite(positions)) or not np.all(np.isfinite(velocities)):
        raise ValueError(f"{p}: non-finite particle values")
    return {"ID": ids, "position": positions, "velocity": velocities}


def lineage_report(paths: list[str | pathlib.Path]) -> dict:
    if len(paths) < 2:
        raise ValueError("lineage report requires at least two snapshots")
    snapshots = [load_particle_snapshot(p) for p in paths]
    ids0 = snapshots[0]["ID"]
    sorted0 = np.sort(ids0)
    unique0 = len(np.unique(ids0)) == len(ids0)
    rows = []
    all_same = unique0
    for i, snap in enumerate(snapshots):
        ids = snap["ID"]
        unique = len(np.unique(ids)) == len(ids)
        same = len(ids) == len(ids0) and np.array_equal(np.sort(ids), sorted0)
        all_same = all_same and unique and same
        rows.append({
            "snapshot_index": i,
            "particle_count": int(len(ids)),
            "ids_unique": bool(unique),
            "same_id_set_as_snapshot_0": bool(same),
            "position_min": np.min(snap["position"], axis=0).tolist(),
            "position_max": np.max(snap["position"], axis=0).tolist(),
            "particle_velocity_rms": float(np.sqrt(np.mean(snap["velocity"]**2))),
        })
    return {
        "lineage_qualified": bool(all_same),
        "snapshot_count": len(paths),
        "reference_particle_count": int(len(ids0)),
        "snapshots": rows,
    }
