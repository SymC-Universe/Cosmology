"""Inspect gevolution particle HDF5 snapshots for stable lineage fields."""

from __future__ import annotations

import argparse
import json
import pathlib

import h5py
import numpy as np


def _dataset_inventory(path: pathlib.Path) -> list[dict]:
    rows = []
    with h5py.File(path, "r") as h:
        def visitor(name, obj):
            if isinstance(obj, h5py.Dataset):
                rows.append({
                    "path": name,
                    "shape": list(obj.shape),
                    "dtype": str(obj.dtype),
                    "dtype_names": list(obj.dtype.names) if obj.dtype.names else None,
                })
        h.visititems(visitor)
    return rows


def _collect_named_arrays(path: pathlib.Path) -> dict[str, np.ndarray]:
    arrays = {}
    with h5py.File(path, "r") as h:
        def visitor(name, obj):
            if not isinstance(obj, h5py.Dataset):
                return
            data = obj[...]
            if data.dtype.names:
                for field in data.dtype.names:
                    arrays[f"{name}:{field}"] = np.asarray(data[field])
            else:
                arrays[name] = np.asarray(data)
        h.visititems(visitor)
    return arrays


def _find_id_candidate(arrays: dict[str, np.ndarray]):
    explicit = []
    integer = []
    for name, arr in arrays.items():
        lower = name.lower()
        flat = np.asarray(arr).reshape(-1)
        if "id" in lower and np.issubdtype(flat.dtype, np.integer):
            explicit.append((name, flat))
        elif np.issubdtype(flat.dtype, np.integer) and flat.size > 0:
            integer.append((name, flat))
    pool = explicit if explicit else integer
    if not pool:
        return None, None
    # Prefer a unique integer vector, since particle IDs must be unique within a snapshot.
    for name, flat in pool:
        if flat.ndim == 1 and len(np.unique(flat)) == flat.size:
            return name, flat
    return pool[0]


def build_report(first: pathlib.Path, second: pathlib.Path) -> dict:
    first_arrays = _collect_named_arrays(first)
    second_arrays = _collect_named_arrays(second)
    id_name_1, ids1 = _find_id_candidate(first_arrays)
    id_name_2, ids2 = _find_id_candidate(second_arrays)

    lineage = {
        "id_field_first": id_name_1,
        "id_field_second": id_name_2,
        "id_join_qualified": False,
    }
    if ids1 is not None and ids2 is not None:
        set1 = set(int(x) for x in np.asarray(ids1).reshape(-1))
        set2 = set(int(x) for x in np.asarray(ids2).reshape(-1))
        common = set1 & set2
        lineage.update({
            "first_id_count": len(set1),
            "second_id_count": len(set2),
            "common_id_count": len(common),
            "first_unique": len(set1) == np.asarray(ids1).size,
            "second_unique": len(set2) == np.asarray(ids2).size,
            "same_id_set": set1 == set2,
            "id_join_qualified": (
                len(set1) == np.asarray(ids1).size
                and len(set2) == np.asarray(ids2).size
                and set1 == set2
            ),
        })

    return {
        "protocol": "GEVOLUTION_PARTICLE_LINEAGE_SCHEMA_SMOKE",
        "stage": "P0-Q infrastructure",
        "scientific_claim_tested": False,
        "first_file": str(first),
        "second_file": str(second),
        "first_inventory": _dataset_inventory(first),
        "second_inventory": _dataset_inventory(second),
        "lineage": lineage,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--first", required=True)
    p.add_argument("--second", required=True)
    p.add_argument("--output", required=True)
    a = p.parse_args()
    report = build_report(pathlib.Path(a.first), pathlib.Path(a.second))
    out = pathlib.Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report["lineage"], sort_keys=True))


if __name__ == "__main__":
    main()
