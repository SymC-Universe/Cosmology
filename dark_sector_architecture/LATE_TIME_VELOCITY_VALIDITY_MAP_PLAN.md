# Late-Time Coarse-Grained Velocity Validity Map Plan

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q modal preregistration development
**Status:** FROZEN BEFORE LATE-TIME VELOCITY RESULT INSPECTION
**Date:** 2026-09-27
**Parent:** PREG_MODAL_PA1_APQ3_ADJUDICATION.md
**Development seed:** 424242 only
**P1 status:** CLOSED

## Purpose

Map the numerical and physical interpretation regime of gevolution's coarse-grained peculiar-velocity field before using its shear tensor in a prospective E-sigma relational test.

This plan does not test whether E-sigma relational geometry adds predictive information.

## Frozen simulation family

- gevolution 1.3 commit `0cca42e51a824002ae4fb602cbd79d671e8ffe60`;
- LATfield2 commit `2d8c737ab6adc965a1d2718c209f5085af27b09c`;
- canonical crystal template blob `d4de9a5400ef58f6a0181fbe61f18056b233a425`;
- seed 424242;
- L = 64 Mpc/h;
- N = 32 and 64;
- tiling factors 8 and 16;
- time-step limit 0.02;
- snapshot outputs: `v, particles`;
- requested redshifts: z = 5, 2, 1, 0.5, 0.1.

N128 is intentionally not part of this first trajectory map. It may be used later only as a prospectively defined focused check after a candidate development domain is chosen from representation validity rather than predictive outcome.

## Native velocity operator

All kinematic fields use the Development 013 centered gevolution velocity operator:

\[
k_i^{(v)} = N\sin(2\pi n_i/N).
\]

Primary fields:
- centered divergence theta;
- centered STF shear sigma_ij;
- centered vorticity omega_i.

## Frozen physical Fourier families

Use signed mode number radius |n| on the fixed L=64 Mpc/h box.

### Band L
\[0<|\mathbf n|<4\]
approximately k < 0.393 h/Mpc.

### Band M
\[4\le|\mathbf n|<8\]
approximately 0.393 <= k < 0.785 h/Mpc.

### Band H
\[8\le|\mathbf n|<15\]
approximately 0.785 <= k < 1.473 h/Mpc.

### Band A
Full frozen N32 active-overlap support:
\[0<|\mathbf n|<15,\quad |n_i|<15.\]

No band may be added, removed, merged, or retuned after result inspection.

## Required diagnostics by redshift, resolution, and band

Record:
- velocity RMS;
- divergence RMS;
- shear Frobenius RMS;
- vorticity vector RMS;
- vorticity/shear RMS ratio;
- shear trace residual;
- N32 versus N64 shear tensor error/eigenframe diagnostics;
- N32 versus N64 vorticity vector RMS difference and field correlation;
- actual snapshot redshift and tau/L;
- stable particle-ID join across every snapshot.

## Particle-lineage requirement

For each resolution, the CDM particle ID set must be unique within every snapshot and identical across all five snapshots.

This run only verifies lineage continuity. It does not yet define material patches or use later outcomes.

## Interpretation rules

No universal 'acceptable vorticity' threshold is introduced.

The map is used to separate:

1. scales/epochs where the coarse-grained velocity field is predominantly potential/shear-like;
2. scales/epochs where resolved rotational/multistream-sensitive structure is material;
3. scales/epochs where N32/N64 numerical disagreement is comparable to or larger than the field structure being interpreted.

Vorticity is not treated as a failure. It changes the physical meaning from a dust-like local shear toward a coarse-grained multistream kinematic field.

## Domain-selection firewall

A later PREG-MODAL-PA-1 development domain may be selected from this map only on representation-validity grounds:
- numerical stability;
- identifiable tensor eigenstructure;
- lineage continuity;
- declared multistream interpretation.

It may not be selected because E-sigma predictive gain is large there. No predictive E-sigma outcome is generated in this run.

## Outcomes

### VALIDITY_MAP_COMPLETE
Use if all requested epochs and bands yield finite diagnostics and stable particle lineages.

### NEED_MORE_INFO
Use if one resolution/epoch/band is technically ambiguous, particle lineage fails, or the N32/N64 comparison is insufficient to characterize a prospective domain.

### REFUSED
Use only if the exported velocity semantics or particle lineage cannot support the planned coarse-grained interpretation at all.

## Next gate

After this map, prospectively define material-patch construction and tensor interpolation/averaging on one or more representation-admissible development domains. Do not inspect predictive E-sigma added value before that patch/interpolation gate is frozen.
