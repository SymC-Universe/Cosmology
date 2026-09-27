# Cosmology Qualification Results Index

**Project:** Cosmic Stability Architecture  
**Branch:** `dark-sector-stability-architecture`  
**Stage:** P0-Q modal/representation qualification  
**Updated:** 2026-09-27

## Durable generated results

### Modal eigensystem known-truth suite

Path:
`dark_sector_architecture/qualification/results/modal_known_truth_report.json`

Status:
**GENERATED / DURABLE**

Cases:
KT-01 through KT-12.

Interpretation:
- exact degeneracy refuses unique direction;
- rotation covariance passes;
- scalar-matched/modal-different known truth passes;
- near-degeneracy is tracked continuously through eigengap/conditioning;
- known-bad nonsymmetric tensor is refused;
- no scientific eigengap threshold is frozen.

### Weak-field tensor reconstruction suite

Path:
`dark_sector_architecture/qualification/results/weak_field_known_truth_report.json`

Status:
**GENERATED / DURABLE**

Cases:
WF-01 through WF-04.

Interpretation:
- periodic spectral Hessian recovery passes;
- trace-free tidal construction passes;
- velocity divergence/shear recovery passes;
- off-diagonal shear recovery passes;
- this does not assert equivalence to the full electric Weyl tensor.

## Pending durable results

The following files are created only after the pinned gevolution smoke workflow itself passes:

- `dark_sector_architecture/qualification/results/gevolution_modal_pilot_metadata.json`
- `dark_sector_architecture/qualification/results/gevolution_modal_pilot_manifest.txt`
- `dark_sector_architecture/qualification/results/gevolution_modal_extraction_summary.json`

Current status:
**PENDING GEVOlution SMOKE EXECUTION**

The workflow is required to:
1. build exact pinned gevolution/LATfield2 revisions;
2. generate the deterministic Gadget-2 template;
3. run the frozen (8^3), (z=100	o99) smoke case;
4. verify `phi`, `B`, `chi`, `hij`, and `v` HDF5 outputs;
5. load real LATfield2 HDF5 `phi` and `v`;
6. reconstruct weak-field tidal/shear tensors;
7. diagonalize and summarize modal eigenstructure;
8. upload raw small artifacts;
9. commit metadata, manifest, and extraction summary back to this branch.

## Pipeline source files

- `qualification/modal_tensor.py`
- `qualification/weak_field_tensors.py`
- `qualification/latfield_hdf5.py`
- `qualification/extract_gevolution_modal_pilot.py`
- `qualification/make_minimal_gadget_template.py`

## Qualification tests

- `test_modal_tensor_known_truth.py`
- `test_weak_field_tensors.py`
- `test_latfield_hdf5.py`
- `test_extract_gevolution_modal_pilot.py`

## Workflow state

- `.github/workflows/cosmology-modal-known-truth.yml`
  - persists modal and weak-field JSON reports to the branch.
- `.github/workflows/cosmology-gevolution-modal-pilot.yml`
  - persists gevolution metadata/manifest/extraction summary to the branch.

No P1 claim is activated by any result in this index.
