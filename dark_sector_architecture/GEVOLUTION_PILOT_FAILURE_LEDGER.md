# gevolution Modal Pilot Failure Ledger

**Project:** Cosmic Stability Architecture  
**Stage:** P0-Q infrastructure qualification  
**Purpose:** Preserve failed pilot attempts as evidence and distinguish repeated infrastructure defects from scientific/numerical behavior.

No run in this ledger before the first successful smoke execution produced a scientific cosmology result.

## Failure family A - GPU-backend dependency on CPU runner

Affected runs:
- 36347877225
- 36349647148
- 36349659925
- 36349924242

Primary observed failure:
`LATfield2.hpp: fatal error: cufft.h: No such file or directory`

Classification:
- root cause: infrastructure/backend mismatch;
- scientific status: NOT_EXECUTED;
- anomaly status: systematic/reproducible across unchanged GPU-mirror backend;
- resolution: stop retrying unchanged GPU mirror; identify CPU-compatible backend.

## Failure family B - partial historical rollback still GPU-instrumented

Affected run:
- 36349998368

Primary observed failure:
`LATfield2_Field.hpp: fatal error: nvtx3/nvToolsExt.h: No such file or directory`

Classification:
- root cause: historical LATfield2 revision still contains unconditional NVIDIA NVTX instrumentation;
- scientific status: NOT_EXECUTED;
- anomaly status: systematic backend-history dependency;
- resolution: move earlier only as a diagnostic, then stop once API incompatibility becomes evident.

## Failure family C - pre-NVTX GitHub revision incompatible with current gevolution API

Affected run:
- 36350136012

Primary observed failure:
multiple Field/PlanFFT API errors, including protected `lattice_` access and missing public `lattice()` / `components()` methods.

Classification:
- root cause: version/API incompatibility between current gevolution 1.3 and old pre-NVTX GitHub LATfield2;
- scientific status: NOT_EXECUTED;
- anomaly status: expected after over-rollback, not a numerical outlier;
- resolution: abandon GPU-development GitHub history as CPU backend source.

## Canonical CPU resolution

gevolution CPU documentation specifies LATfield2 v1.1.

Canonical UZH LATfield2 v1.1 master:
`2d8c737ab6adc965a1d2718c209f5085af27b09c`

Current canonical smoke run:
- run: 36350236327
- gevolution: `0cca42e51a824002ae4fb602cbd79d671e8ffe60`
- LATfield2: `2d8c737ab6adc965a1d2718c209f5085af27b09c`

At ledger creation:
- dependency install: PASS
- source fetch: PASS
- deterministic template generation: PASS
- gevolution compile: PASS
- tiny smoke simulation: ACTIVE

## Interpretation rule

These failures cannot count against PREG-MODAL-PA-1 or any cosmological hypothesis because the scientific computation never executed.

They remain preserved because they establish the backend compatibility boundary and prevent repeated unchanged retries.


## Failure family D - invalid 2x2 launch masked by shell pipeline

Affected run:
- 36350374092

Observed behavior:
- canonical CPU backend compiled successfully;
- smoke command requested four MPI ranks on a runner exposing fewer slots;
- Open MPI refused launch and printed the insufficient-slots diagnostic;
- because the command was piped through `tee` without `pipefail`, the workflow step was incorrectly marked success;
- downstream field verification correctly failed because no HDF5 fields existed.

Classification:
- root cause: infrastructure/process-layout launch plus shell exit-code masking;
- scientific status: NOT_EXECUTED;
- anomaly status: isolated workflow defect, now reproduced/explained;
- evidence integrity: no simulation output was generated and no scientific claim was evaluated.

Repair:
- keep valid gevolution process grid `-n 2 -m 2`;
- add `mpirun --oversubscribe -np 4` for the tiny hosted-runner qualification;
- add `set -o pipefail` so MPI failure propagates through `tee`.

Successor run:
- 36350469640
- head commit `8f620e1e7f15d22a8531fc87b9b693b515f599da`


## Failure family E - structurally valid but numerically invalid sparse IC template

Affected run:
- 36350469640

Observed behavior:
- canonical CPU gevolution/LATfield2 compiled;
- valid 2x2 oversubscribed MPI launch executed;
- all five requested HDF5 fields were written;
- initialization reported only 8 CDM particles on an 8^3 mesh;
- maximum displacement was approximately -7.38e19 lattice units;
- average T00 was NaN at cycle 0;
- phi HDF5 consequently contained non-finite values and extraction refused it.

Classification:
- root cause: qualification initial-condition/template density, not cosmological dynamics or parser behavior;
- scientific status: INVALID_INPUT / NOT_ADJUDICABLE;
- anomaly status: reproducible root-cause signature of sparse template plus displacement correction;
- evidence integrity: finite-value loader correctly refused the result rather than sanitizing NaNs.

Repair:
- preserve one-particle deterministic Gadget-2 template;
- change tiling factor from 2 to 8 so the 8^3 smoke mesh receives 8^3 = 512 homogeneous template particles, one per grid cell;
- keep finite-value refusal and the same cosmology/transfer functions.

Successor run:
- 36350573345
- head commit `49a4a9648a51cf3d9c931675d000097f8fe5b2e4`
