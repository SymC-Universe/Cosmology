# Modal Resolution and Convergence Qualification Plan

**Stage:** P0-Q  
**Status:** PROSPECTIVE DESIGN, NOT YET EXECUTED  
**Parent:** PREG-MODAL-PA-1 candidate

## Purpose

Separate two distinct uncertainty sources before activating a modal claim:

1. **extraction uncertainty** from reconstructing tidal/shear tensors and eigensystems on a finite grid;
2. **simulation uncertainty** from the underlying relativistic evolution.

These may not be pooled into one tolerance.

## Q-R1: Extraction-resolution qualification

Input:
- one fixed physical field realization;
- a highest available reference grid;
- prospectively fixed spectral/coarse-graining operators.

Procedure:
1. treat the highest-resolution field as the fixed source realization;
2. construct lower-resolution representations by explicit low-pass/coarse-graining of that same field;
3. reconstruct tidal/shear tensors at each resolution;
4. compare on a common physical grid/scale;
5. measure tensor operator-norm error, invariant error, eigengap error, eigenvalue error, and eigenframe-angle error;
6. propagate tensor perturbation magnitude through the eigengap-sensitive direction bound.

Outputs:
- error versus grid scale;
- error versus physical smoothing scale;
- directional uncertainty versus eigengap;
- exact-degeneracy refusal map.

No universal acceptance threshold is pre-imposed.

## Q-R2: Simulation-resolution qualification

This begins only after Q-R1 and gevolution smoke PASS.

Paired runs must preserve:
- cosmology;
- box;
- random realization or an explicitly reconstructible common IC source;
- output epochs;
- gravity theory;
- extraction definition.

Only numerical resolution/time-stepping may vary in a given comparison.

If same-seed gevolution IC generation does not create phase-identical overlapping modes across grid sizes, the run is **not** treated as a paired resolution experiment. A fixed IC/restart route must be constructed first.

Candidate development ladder:
- Ngrid 8: infrastructure only;
- Ngrid 16: first development field;
- Ngrid 32: paired/convergence candidate only if resource behavior is clean.

These values are computational qualification choices, not scientific thresholds.

## Error objects

For tensor fields (A) and (B) after physical-scale matching:

[
epsilon_T = |A-B|_2
]

locally or by prospectively declared distributional summaries.

For modal direction:

[
epsilon_{m dir}
propto
rac{epsilon_T}{Deltalambda}
]

as a perturbation-bound diagnostic.

Additional summaries:
- ordered eigenvalue differences;
- eigengap differences;
- subspace principal angles;
- scalar-invariant differences;
- shear-tidal alignment differences.

## Refusal conditions

REFUSE directional comparison when:
- exact/numerical degeneracy makes the eigenvector non-identifiable;
- grids cannot be mapped to a common physical scale without outcome-dependent choices;
- IC realizations differ in a way that confounds simulation resolution;
- extraction and simulation errors cannot be separated;
- periodic/box aliasing dominates the target mode.

## Qualification outcomes

- `EXTRACTION_QUALIFIED`
- `SIMULATION_RESOLUTION_QUALIFIED`
- `INDETERMINATE_NEED_MORE_INFO`
- `REFUSED`

No PREG-MODAL-PA-1 activation occurs until both extraction and simulation uncertainty have an admissible route for the intended regime.

## Exact next action

After the current gevolution smoke gate:
1. inspect real-field shapes and HDF5 semantics;
2. if PASS, build Q-R1 using the real smoke field only as development data;
3. do not freeze an empirical tolerance from the smoke field;
4. then determine whether a phase-identical IC strategy is available for Q-R2.
