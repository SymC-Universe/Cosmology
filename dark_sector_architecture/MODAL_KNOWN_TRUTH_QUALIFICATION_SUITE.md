# Modal Known-Truth Qualification Suite

**Stage:** P0-Q  
**Parent:** MODAL_OBJECT_QUALIFICATION.md  
**Status:** PROSPECTIVE DESIGN, NOT YET EXECUTED

## Purpose

Qualify extraction, identifiability, invariance, and refusal behavior for the native shear/Weyl modal representation before cosmological production or P1 freeze.

The suite tests the representation. It does not confirm a cosmological claim about nature.

## Native objects

Primary:
- symmetric shear tensor (sigma_{ij});
- electric Weyl/tidal tensor (E_{ij});
- magnetic Weyl tensor (H_{ij}) where applicable.

Retain:
- ordered eigenvalues;
- eigenvectors/eigenframes;
- degeneracy flags;
- scalar invariants;
- alignment metrics;
- numerical conditioning.

## Frozen known-truth cases to implement

### KT-01 Isotropic expansion
Tensor:
[
S=alpha I.
]

Expected:
- all eigenvalues equal;
- eigenframe physically non-identifiable;
- algorithm must REFUSE directional interpretation;
- scalar invariant remains valid.

### KT-02 One-axis collapse
Tensor with one contraction eigenvalue distinct from two non-collapsing directions.

Expected:
- one unique principal collapse axis;
- stable eigenvector recovery under rotation.

### KT-03 Two-axis collapse
Expected:
- two collapsing directions;
- remaining expansion/least-collapse direction recovered.

### KT-04 Three-axis collapse
Expected:
- all directions collapsing;
- if eigenvalues are nearly equal, directional confidence must degrade appropriately.

### KT-05 Matched scalar norm, different spectra
Construct two trace-controlled tensors satisfying the same chosen scalar norm, e.g.

[
mathrm{tr}(S_A)=mathrm{tr}(S_B),
qquad
mathrm{tr}(S_A^2)=mathrm{tr}(S_B^2),
]

while using different admissible eigenvalue spectra when mathematically possible under the chosen constraints, or otherwise match the scalar subset actually used by the downstream scalar comparator.

Purpose:
- demonstrate exactly which modal information is not recoverable from the scalar summary.

### KT-06 Matched density/expansion, rotated eigenframe
Same eigenvalues, different coordinate orientation.

Expected:
- invariant eigenvalue content unchanged;
- eigenvectors rotate covariantly;
- coordinate rotation alone must not change physical classification.

### KT-07 Near-degenerate pair
Two eigenvalues separated by progressively smaller gaps.

Expected:
- eigenvalue estimates may remain stable;
- eigenvector direction uncertainty must increase as the gap closes;
- directional interpretation eventually REFUSED.

### KT-08 Exact degeneracy
Expected:
- eigenspace may be identifiable;
- individual eigenvectors inside the degenerate subspace are not;
- implementation must not fabricate a preferred direction.

### KT-09 Shear-Weyl aligned
Known common eigenframe.

Expected:
- alignment metric returns the known aligned state.

### KT-10 Shear-Weyl misaligned
Known relative rotation.

Expected:
- relative alignment recovered independent of global coordinate rotation.

### KT-11 Perturbation/noise sensitivity
Inject bounded tensor perturbations.

Expected:
- uncertainty scales with eigenvalue gap and perturbation magnitude;
- no hard numerical threshold is invented before observing qualification behavior.

### KT-12 Known-bad non-symmetric input
Expected:
- input/refusal gate catches invalid tensor semantics rather than silently symmetrizing unless the production definition explicitly requires symmetrization.

## Required outputs

For each case:
- exact truth tensor;
- recovered eigenvalues;
- recovered eigenspaces/eigenframes;
- scalar invariants;
- alignment metrics where applicable;
- condition/eigenvalue gaps;
- uncertainty estimate;
- PASS / INDETERMINATE / REFUSED;
- reason code.

## Qualification principles

1. No web-class threshold is part of the primary modal qualification.
2. Exact/near degeneracy must reduce directional confidence.
3. Rotation invariance/covariance must be demonstrated.
4. Scalar invariants and modal information remain separately reported.
5. A known-bad input must fail.
6. The production extraction code and the qualification tests must call the same implementation.
7. Numerical tolerances are earned from this suite and frozen only after the qualification behavior is inspected.
8. Any threshold learned here is qualification/calibration evidence and cannot confirm itself on the same cases.

## Next mechanical action

Implement the tensor extraction and known-truth tests in the Cosmology repository, with no cosmological outcome data opened.
