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
