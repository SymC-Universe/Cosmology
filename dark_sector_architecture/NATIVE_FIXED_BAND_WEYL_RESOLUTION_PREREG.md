# Native Fixed-Band Electric-Weyl Resolution Preregistration

**Project:** Cosmic Stability Architecture  
**Stage:** P0-Q modal/representation qualification  
**Status:** FROZEN BEFORE N32/N64/N128 RESULT INSPECTION  
**Date:** 2026-09-27  
**Parent development:** Development 010  
**Parent gate:** ELECTRIC_WEYL_TEMPORAL_QUALIFICATION_GATE.md

## Purpose

Test whether the gevolution/LATfield2-native electric-Weyl modal representation converges with numerical resolution when all comparisons are made on one prospectively frozen physical Fourier support.

This is a representation qualification. It is not P1 evidence and does not activate PREG-MODAL-PA-1 automatically.

A second, independent target is to determine whether the full-grid split between the native LATfield2 representation and the continuum-FFT comparator collapses on a common physical band or persists there.

## Frozen simulation family

All members use:

- gevolution commit 0cca42e51a824002ae4fb602cbd79d671e8ffe60;
- LATfield2 commit 2d8c737ab6adc965a1d2718c209f5085af27b09c;
- canonical gevolution sc1_crystal.dat template blob d4de9a5400ef58f6a0181fbe61f18056b233a425;
- box size L = 64 Mpc/h;
- seed 424242;
- grids N = 32, 64, 128;
- tiling factors 8, 16, 32;
- TENSOR_EVOLUTION and VELOCITY;
- the same qualification-only dynamic-h_ij snapshot patch used in the qualified N64 temporal pilot;
- five requested scale factors a = {0.009950, 0.009975, 0.010000, 0.010025, 0.010050};
- full-precision actual conformal times parsed separately for every grid;
- nested inner snapshots 1,2,3 and outer snapshots 0,2,4 for temporal derivatives;
- no equal-time-spacing approximation.

The central requested epoch is a = 0.010000, approximately z = 99.

## Frozen physical Fourier support

The common comparison band is fixed by the lowest-resolution gevolution initial support at N = 32.

Let n = (n_x,n_y,n_z) be signed integer Fourier mode numbers. The retained nonzero support is

\[
\mathcal K_{32}
=
\{
\mathbf n:
0<|\mathbf n|<15,
\ |n_x|<15,
\ |n_y|<15,
\ |n_z|<15
\}.
\]

This is the spherical active-overlap support implied by gevolution's k_max = N/2 - 1 low-grid initialization.

No mode may be removed after results are inspected because of poor agreement, small eigengap, sector amplitude, or inconvenient direction.

## Frozen order of operations

This experiment intentionally differs from the earlier Q-R3 comparator ladder.

For every native grid N:

1. load the five native-grid fields;
2. derive B'_i and h''_ij from that grid's own actual conformal times;
3. reconstruct scalar, vector, tensor, and total electric-Weyl sectors on the native grid using that grid's LATfield2/gevolution differential operator;
4. reconstruct the continuum-FFT comparator on the same native grid;
5. construct native velocity shear separately on the native grid;
6. only then project each resulting tensor onto K_32 and the common 32^3 comparison grid.

Thus the native discretization is part of the object being tested. Restricting the scalar fields first and differentiating afterward is prohibited for the primary result because that would erase the resolution dependence of the native lattice operator.

## Frozen primary objects

For each resolution:

\[
E^{(S)}_{ij},\quad
E^{(V)}_{ij},\quad
E^{(T)}_{ij},\quad
E^{(\mathrm{full})}_{ij},
\]

plus native velocity-shear tensor

\[
\sigma_{ij}=\mathrm{STF}[\partial_{(i}v_{j)}].
\]

Continuum-FFT versions are retained only as comparator representations.

## Required diagnostics

### Field validity

For every grid and snapshot record:

- distinct cycles;
- strictly increasing actual conformal times;
- finite fields;
- native gevolution B_i divergence/curl;
- native gevolution h_ij divergence/norm;
- native gevolution h_ij trace/norm;
- independently reproduced native post-processing diagnostics.

### Temporal uncertainty

For every grid record:

- inner and outer derivative weights;
- B'_i inner/outer difference;
- h''_ij inner/outer difference;
- inner/outer full-Weyl tensor and eigenframe differences on K_32.

### Resolution convergence

For adjacent pairs 32->64 and 64->128, record separately for scalar, vector, tensor, full Weyl, and native shear:

- absolute and relative tensor-operator error quantiles;
- eigenvalue errors;
- eigengap errors;
- eigenframe diagonal alignment quantiles;
- error/eigengap direction diagnostics;
- sector Frobenius RMS.

### Representation split

At N = 32,64,128, on the same K_32, record native-versus-continuum diagnostics for scalar, vector, tensor, full Weyl, and shear.

## Frozen outcome logic

No universal percentage threshold is introduced.

### Outcome A: NATIVE_FIXED_BAND_QUALIFIED_P0Q

Use only if:

1. all three native simulations pass field-validity and native constraint checks;
2. the common band is applied exactly as frozen;
3. the 64->128 full-Weyl median and q95 relative operator errors are lower than the corresponding 32->64 errors;
4. full-Weyl eigenframe and error/eigengap diagnostics improve or remain consistent with the demonstrated temporal uncertainty rather than worsening with refinement;
5. the scalar sector follows the same convergent direction;
6. native shear either shows the same refinement direction or is explicitly classified NEED_MORE_INFO without being hidden inside the full-Weyl result;
7. vector and tensor sectors are reported independently even if their small amplitudes make their resolution status indeterminate;
8. no post hoc mode deletion, eigengap threshold, time-spacing retuning, or operator substitution is required.

This outcome qualifies the native fixed-band representation for modal preregistration reassessment. It does not activate P1.

### Outcome B: NEED_MORE_INFO

Use when the native objects are valid but the resolution evidence is mixed or not yet discriminating.

Examples include:

- full-Weyl median improves but q95 worsens materially;
- one adjacent pair improves while the next is unresolved at the temporal reconstruction floor;
- vector/tensor sectors are below their demonstrated reconstruction uncertainty;
- native shear remains substantially less converged than full Weyl;
- cross-resolution central-epoch mismatch is large enough to compete with the measured resolution difference;
- modal directions become ambiguous because of genuine eigengap collapse.

NEED_MORE_INFO preserves the representation and requires a prospectively defined follow-up rather than a retroactive threshold.

### Outcome C: REFUSED

Use if:

- native constraint semantics fail at one or more resolutions;
- fields are non-finite or cannot be mapped to the frozen band;
- the 64->128 full-Weyl resolution error systematically grows rather than shrinks while remaining above temporal uncertainty;
- the result depends on deleting inconvenient modes or retuning the common support after inspection;
- component ordering, units, staggering, sign convention, or temporal normalization cannot be reconciled.

A refused fixed-band qualification blocks PREG-MODAL-PA-1 activation until a new representation version is prospectively defined.

## Independent native-versus-continuum classification

This classification does not control whether the native representation itself qualifies.

### SPLIT_COLLAPSES_ON_COMMON_BAND

Use if the native-versus-continuum discrepancy decreases with resolution and, at N = 128, is no larger than the native 64->128 resolution uncertainty on the same band.

### SPLIT_PERSISTS_ON_COMMON_BAND

Use if the native-versus-continuum discrepancy remains larger than the native 64->128 resolution uncertainty and does not approach that uncertainty with refinement.

### SPLIT_NEED_MORE_INFO

Use for mixed or non-monotonic behavior.

No interpretation of a persistent split as physical is licensed by this classification alone. It is a representation result.

## Exploration firewall

This gate cannot close:

- scalar exploration;
- modal exploration outside this Weyl/shear representation;
- Conglomerate/System exploration;
- joint Scalar + Modal + Conglomerate investigation;
- discovery of an additional architecture component;
- P0-D novelty search.

A failure of this representation is evidence about this representation, not a global refusal of the cosmological architecture program.
