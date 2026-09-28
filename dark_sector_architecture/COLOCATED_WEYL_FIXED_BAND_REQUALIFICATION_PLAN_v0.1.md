# Co-located Weyl Fixed-Band Requalification Plan v0.1

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q local modal representation requalification
**Status:** FROZEN BEFORE CO-LOCATED REAL-FIELD OUTCOME INSPECTION
**Date:** 2026-09-27
**Trigger:** Development 015
**Dependency:** TENSOR_COLOCATION_QUALIFICATION_PLAN_v0.1 outcome TENSOR_COLOCATION_QUALIFIED_P0Q
**P1 status:** CLOSED

## Purpose

Requalify finite-resolution local electric-Weyl eigensystems after placing every native staggered tensor component on the same physical vertex lattice.

This gate supersedes only the local-matrix/eigensystem interpretation of earlier raw-index native Weyl ladders. Componentwise native field results remain preserved.

## Frozen simulation family

Use the same early-epoch qualification family as the prior fixed-band ladder:
- gevolution commit 0cca42e51a824002ae4fb602cbd79d671e8ffe60;
- LATfield2 commit 2d8c737ab6adc965a1d2718c209f5085af27b09c;
- canonical sc1_crystal.dat template blob d4de9a5400ef58f6a0181fbe61f18056b233a425;
- box size 64 Mpc/h;
- seed 424242;
- N = 32, 64, 128;
- tiling factors 8, 16, 32;
- TENSOR_EVOLUTION and VELOCITY;
- qualification-only dynamic-h_ij snapshot patch;
- five requested scale factors a={0.009950,0.009975,0.010000,0.010025,0.010050};
- actual full-precision tau/L from each run;
- inner temporal stencil snapshots 1,2,3 and outer stencil 0,2,4.

## Frozen spatial support

Use the identical N32 active-overlap physical support:

\[
\mathcal K_{32}=\{\mathbf n:0<|\mathbf n|<15,\ |n_i|<15\}.
\]

No modes may be deleted after outcome inspection.

## Frozen order of operations

For each native grid:
1. reconstruct native scalar, vector, tensor, and total electric-Weyl component fields on their native LATfield2 staggering;
2. apply the frozen vertex co-location operator to each native tensor sector;
3. only after co-location compute local matrix eigensystems, eigengaps, operator norms, and modal comparisons;
4. project the co-located tensors onto K32 and the common 32^3 comparison grid;
5. reconstruct the continuum-FFT comparator on the same native grid and project it onto the identical K32 support;
6. compare co-located native versus continuum tensors and eigensystems.

Co-location precedes eigensystem analysis. Fourier restriction does not substitute for co-location.

## Required diagnostics

Per grid:
- native B and h constraint diagnostics;
- actual epoch/cycle metadata;
- temporal inner/outer uncertainty;
- co-location change diagnostics for scalar/vector/tensor/total sectors;
- common-band scalar/vector/tensor/full sector amplitudes;
- local eigenvalues, eigengaps, and eigenframe conditioning after co-location.

Adjacent N32->N64 and N64->N128:
- relative tensor-operator error quantiles;
- eigenvalue error quantiles;
- eigengap error quantiles;
- eigenframe diagonal alignment quantiles;
- error/eigengap directional diagnostics.

Native versus continuum at each N:
- same tensor/eigensystem diagnostics on K32 after both objects refer to the vertex lattice.

## Outcome A: COLOCATED_LOCAL_WEYL_QUALIFIED_P0Q

Use only if:
1. all three simulations and temporal reconstructions are valid;
2. co-location uses the frozen operator with no inverse filtering;
3. N64->N128 full-Weyl median and q95 relative operator errors are lower than N32->N64;
4. scalar-Weyl median and q95 errors move in the same convergent direction;
5. full-Weyl eigenframe median and q05 alignments improve with refinement rather than degrade;
6. error/eigengap diagnostics improve or remain bounded consistently with the refinement trend;
7. temporal inner/outer uncertainty is below the resolution differences being interpreted;
8. no post-result mode deletion, eigengap cutoff, or representation substitution is required.

Vector/tensor sector convergence must be reported independently but may remain NEED_MORE_INFO if their amplitude is below numerical/temporal identifiability. That does not silently convert them to zero.

## Outcome B: NEED_MORE_INFO

Use when local tensors are valid but:
- median and q95 convergence disagree materially;
- eigenframe convergence is mixed or degeneracy dominated;
- temporal or co-location uncertainty competes with the measured resolution difference;
- the N128 result remains insufficient to distinguish discretization from a stable representation mismatch.

## Outcome C: REFUSED

Use if:
- co-location semantics fail on real fields;
- local tensors are non-finite or nonsymmetric after the frozen mapping;
- full/scalar local eigensystem errors systematically worsen from N32->N64 to N64->N128 above the temporal floor;
- interpretation requires deconvolving the co-location filter or removing inconvenient modes after inspection.

## Native-versus-continuum classification

Record independently:
- COLLAPSES_ON_COMMON_BAND if the co-located native/continuum discrepancy decreases monotonically and by N128 is no larger than the native N64->N128 resolution uncertainty;
- PERSISTS_ON_COMMON_BAND if it remains larger than native resolution uncertainty without approaching it;
- NEED_MORE_INFO otherwise.

This is a representation classification, not a physical-mechanism claim.

## Downstream consequence

If QUALIFIED:
- `LOCAL_WEYL_EIGENSYSTEM_P0Q = QUALIFIED`;
- material-patch interpolation may resume with corrected centered velocity shear;
- E-sigma relational development remains P0-Q only until the parent APQ-3 plan is frozen for P1.

If NEED_MORE_INFO or REFUSED:
- preserve componentwise Weyl qualification;
- do not construct local E-sigma eigensystem relations;
- keep all other architecture exploration branches open.
