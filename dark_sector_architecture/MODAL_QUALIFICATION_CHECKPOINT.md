# Modal Qualification Checkpoint

**Stage:** P0-Q  
**Date:** 2026-09-27  
**Status:** KNOWN-TRUTH PIPELINE QUALIFIED LOCALLY; GEVOlution SMOKE PENDING

## Mechanical correction

The original qualification workflow generated `modal_known_truth_report.json` only inside the GitHub Actions runner and uploaded it as an artifact. It did not persist the JSON in the repository.

That defect is corrected.

The result is now durable at:

`dark_sector_architecture/qualification/results/modal_known_truth_report.json`

The workflow was changed so future successful runs commit refreshed qualification JSON back to the research branch. Result-only commits do not retrigger the workflow.

## Modal eigensystem result

KT-01 through KT-12 have a durable machine-readable report.

No failed known-truth case is present.

No scientific eigengap threshold has been introduced.

## Weak-field reconstruction result

The periodic spectral reconstruction layer now has a durable machine-readable known-truth report.

Observed numerical errors in the synthetic tests are at floating-point scale:
- tidal analytic recovery max error: approximately (6.2	imes10^{-15});
- longitudinal shear max error: approximately (2.0	imes10^{-15});
- divergence max error: approximately (3.1	imes10^{-15});
- off-diagonal shear max error: approximately (7.2	imes10^{-16}).

This qualifies implementation mathematics only.

## LATfield2 HDF5 schema

Pinned LATfield2 source confirms:
- default dataset name is `data`;
- stored spatial axes are reversed relative to LATfield logical order;
- vector/tensor components use an HDF5 array datatype.

The loader restores logical spatial order and returns vector fields component-first.

Exact-subarray HDF5 tests are included and fail closed on:
- missing dataset;
- wrong component count;
- non-finite content.

## Gevolution pilot repair

The initial pilot referenced upstream `sc1_crystal.dat`, which is absent at the pinned gevolution revision.

The dependency was removed.

The repository now contains a deterministic Gadget-2 template generator. Independent local validation confirms:
- 256-byte Gadget-2 header;
- one CDM template particle;
- one file;
- unit template box;
- valid position block;
- total file size 284 bytes.

The frozen smoke configuration now uses that self-generated template and baryon treatment `ignore` for infrastructure qualification.

## Current gevolution gate

Pinned revisions:
- gevolution: `0cca42e51a824002ae4fb602cbd79d671e8ffe60`
- LATfield2: `b9dcddfc972ba12177e8a92f94394bd8058fde5b`

Frozen smoke:
- (N_{m grid}=8);
- (z=100	o99);
- standard GR;
- required fields: `phi`, `B`, `chi`, `hij`, `v`.

A valid smoke pass must also execute the real-file pipeline:

[
{phi,v}_{m LATfield2 HDF5}
	o
{	ext{tidal tensor},	ext{velocity shear}}
	o
{lambda_i,mathbf e_i,	ext{alignment}}
	o
	ext{machine-readable summary}.
]

The pilot workflow persists:
- metadata JSON;
- HDF5 output manifest;
- modal extraction summary JSON.

## Claim state

- PREG-SCALAR-PA-0: NOT_ACTIVATED.
- PREG-MODAL-PA-1: CANDIDATE, not activated.
- PREG-CONGLOMERATE-PA-1: CANDIDATE, not activated.
- PREG-JOINT-PA-1: CANDIDATE, not activated.
- PREG-JOINT-PA-2: CANDIDATE, not activated.

## Next exact action

1. observe durable gevolution smoke outputs;
2. if absent, diagnose workflow mechanically;
3. if present, inspect real-field extraction summary;
4. only then define resolution/convergence qualification for tensor uncertainty;
5. only after that decide whether PREG-MODAL-PA-1 is fit to activate.
