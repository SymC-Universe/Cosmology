# Modal Known-Truth Independent Validation Checkpoint

**Stage:** P0-Q representation qualification  
**Date:** 2026-09-27  
**Status:** INDEPENDENT FORMULA/LOGIC VALIDATION PASS; CI EXECUTION NOT YET INDEPENDENTLY OBSERVED

## Scope

This checkpoint independently reproduces the mathematical behavior expected from the committed production-facing tensor extractor and KT-01 through KT-12 logic.

It is not the GitHub Actions artifact and does not substitute for an observed CI run.

## Results

All twelve known-truth logic checks reproduced their expected outcomes.

### Degeneracy behavior

KT-01 isotropic tensor:
- both adjacent eigenvalue pairs numerically degenerate;
- directional condition number diverges;
- preferred directional interpretation must be refused.

KT-08 exact pair degeneracy:
- one degenerate eigenspace detected;
- unique axes inside that eigenspace are not physically identifiable.

### Conditioning behavior

KT-04:
- separated-spectrum conditioning proxy: approximately 6.5;
- near-isotropic conditioning proxy: approximately (1.0	imes10^6).

KT-07 eigengap sweep:

| imposed gap | conditioning proxy |
|---:|---:|
| (10^{-2}) | (2.0	imes10^2) |
| (10^{-4}) | (2.0	imes10^4) |
| (10^{-6}) | (2.0	imes10^6) |
| (10^{-8}) | (2.0	imes10^8) |
| (10^{-10}) | (2.0	imes10^{10}) |
| (10^{-12}) | (2.0	imes10^{12}) |

The expected inverse-gap deterioration is reproduced.

No scientific refusal threshold is frozen from this sweep.

### Scalar information loss

KT-05 uses two tensors with:
- identical trace (=0);
- identical (mathrm{tr}(S^2)=6);
- identical Frobenius norm;

but different:
- eigenvalue spectra;
- determinant ((2) versus (0)).

This establishes a known-truth example in which the chosen scalar subset does not uniquely specify the modal tensor state.

It does **not** yet establish that this modal difference matters cosmologically.

### Rotation covariance

KT-02 and KT-06 recover:
- invariant ordered eigenvalues;
- invariant scalar tensor contractions;
- eigenvectors that rotate covariantly with the imposed coordinate rotation.

KT-10 recovers the same shear-Weyl relative alignment before and after a common global coordinate rotation.

### Direction uncertainty

Using the continuous perturbation/gap diagnostic with perturbation operator norm (10^{-5}):

| eigengap | direction-sensitivity proxy |
|---:|---:|
| (0.8) | (1.25	imes10^{-5}) |
| (0.1) | (1.0	imes10^{-4}) |
| (10^{-2}) | (1.0	imes10^{-3}) |
| (10^{-3}) | (1.0	imes10^{-2}) |
| (10^{-4}) | (1.0	imes10^{-1}) |

This supports propagating directional uncertainty continuously from numerical tensor uncertainty and eigengap rather than imposing a universal eigengap cutoff.

### Known-bad refusal

KT-12 materially non-symmetric input is refused rather than silently symmetrized.

## Qualification consequence

The implementation logic is suitable to proceed to infrastructure/cosmological pilot qualification.

No P1 claim is activated.

No empirical or scientific modal threshold has been frozen.

The preferred downstream rule is:

> Estimate tensor uncertainty from numerical/convergence evidence, propagate directional uncertainty using eigengap-sensitive perturbation bounds, and adjudicate the claim-specific uncertainty rather than using a universal modal eigengap threshold.

## CI status

Workflow file:
`.github/workflows/cosmology-modal-known-truth.yml`

The connected GitHub commit-status interface did not expose a push-triggered run at the time of this checkpoint. Therefore the suite is **not labeled CI-passed yet**.

The hourly continuation monitor should inspect/continue this mechanical status without changing the scientific qualification logic.
