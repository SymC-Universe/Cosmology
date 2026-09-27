# Electric-Weyl Temporal Qualification Gate

**Project:** Cosmic Stability Architecture  
**Stage:** P0-Q  
**Status:** PROSPECTIVE / FROZEN BEFORE REAL TEMPORAL RESULT  
**Date:** 2026-09-27

## Purpose

Determine whether the first-order scalar + vector + tensor electric-Weyl
representation can be evaluated from real gevolution outputs with an admissible
temporal-derivative uncertainty treatment.

This gate qualifies a representation. It does not test PREG-MODAL-PA-1 and
does not establish a dark-sector claim.

## Frozen object

Under the project curvature convention,

\[
\mathcal E^{\rm conf}_{ij}
=
D_{ij}\left(\Phi-\frac{\chi_{\rm gev}}{2}\right)
-\frac12\partial_{(i}B'_{j)}
-\frac14\left(h''_{ij}+\nabla^2h_{ij}\right).
\]

The gevolution temporal pilot uses dynamically evolved \(h_{ij}\), not the
ordinary instantaneous TT source projection.

## Frozen temporal design

Five snapshots bracket one central epoch.

Using actual logged conformal times \(\bar\tau=\tau/L\):

- inner derivative stencil: snapshots 1, 2, 3;
- outer derivative stencil: snapshots 0, 2, 4;
- both evaluate at snapshot 2;
- arbitrary-node polynomial weights are derived from the actual \(\bar\tau\)
  values;
- no equal-spacing approximation is allowed.

The inner/outer difference is the temporal discretization diagnostic.

## Required diagnostics

### Native field checks

Record, without outcome-dependent deletion:

- \(B_i\) divergence residual;
- \(h_{ij}\) trace residual;
- \(h_{ij}\) divergence residual;
- \(h_{ij}\) symmetry residual;
- finite/non-finite content;
- distinct output cycles and strictly increasing actual conformal times.

### Temporal checks

Record:

- \(B'_i\) inner and outer RMS;
- \(h''_{ij}\) inner and outer RMS;
- inner/outer relative RMS differences;
- finite-difference weights and time nodes.

### Full-Weyl checks

For both inner and outer temporal reconstructions record:

- scalar, vector, tensor, and total sector RMS;
- full-versus-scalar tensor error;
- full-versus-scalar eigenvalue differences;
- full-versus-scalar eigenframe alignment;
- error/eigengap direction diagnostics;
- inner-versus-outer full-Weyl tensor and eigenframe differences.

No scalar quantity may substitute for these modal diagnostics.

## Outcome A: REPRESENTATION_QUALIFIED_P0Q

Use only if all of the following hold:

1. all required fields are finite and map onto one common grid;
2. five snapshots occupy five distinct cycles with strictly increasing actual
   conformal times;
3. vector transversality and tensor TT diagnostics remain controlled rather
   than indicating a broken field interpretation;
4. both inner and outer stencils produce finite \(B'_i\), \(h''_{ij}\), and
   full electric-Weyl tensors;
5. the difference between inner and outer reconstructions can be propagated
   into the modal quantities without producing incompatible qualitative
   interpretations of the same central field;
6. no outcome-dependent filtering, eigengap cutoff, or time-spacing retuning is
   required to obtain that result.

This outcome qualifies the representation for further P0-Q/P1 preparation. It
does not activate a scientific preregistration automatically.

## Outcome B: NEED_MORE_INFO

Use when the fields are valid but the temporal data do not resolve the
vector/tensor contribution well enough to interpret it.

Examples include:

- inner and outer derivative reconstructions differ by an amount comparable to
  or larger than the vector/tensor sector being measured;
- modal eigenframe changes caused by the temporal stencil are comparable to or
  larger than the full-versus-scalar modal change;
- the full correction is so small that it lies below the demonstrated temporal
  reconstruction uncertainty;
- one early epoch is stable but does not license extrapolation to another
  dynamical regime.

A NEED_MORE_INFO result preserves the representation candidate. The next test
must be prospectively defined, for example a second temporal spacing or a later
epoch. It is not a failure.

## Outcome C: REFUSED

Use if the representation itself is not admissible under the current data or
implementation.

Refusal conditions include:

- non-finite field values;
- snapshot times/cycles are not distinct enough to define the frozen stencils;
- the dynamic \(h_{ij}\) snapshot patch does not output the evolved TT field;
- vector divergence or tensor trace/divergence behavior shows that the field
  semantics are wrong or numerically broken;
- component ordering, units, sign convention, or temporal/spatial normalization
  cannot be reconciled;
- the result requires deleting inconvenient modes or imposing a post hoc
  numerical threshold.

A refused representation must be repaired or replaced before PREG-MODAL-PA-1
can activate.

## Interpretation rule for a negligible vector/tensor correction

If the full scalar+vector+tensor tensor is indistinguishable from the scalar
Weyl tensor at this early epoch, that result is reported as an
**epoch-specific Function/Limit Map result**:

\[
\text{full first-order Weyl}
\approx
\text{scalar Weyl}
\quad
\text{within demonstrated temporal/numerical uncertainty at this epoch}.
\]

It does not establish that vector/tensor sectors are universally negligible.

A later-epoch or more nonlinear test remains open if required by the scientific
question.

## Interpretation rule for a material vector/tensor correction

If the full tensor differs materially from the scalar projection and the
difference survives the inner/outer temporal uncertainty treatment, the result
becomes a modal development requiring:

1. immediate update to WORKING_INVESTIGATION.md;
2. a Development entry in WORKING_SCIENTIFIC_DEVELOPMENTS.md;
3. no automatic promotion to P1;
4. explicit comparison with velocity-shear modal structure and the
   Conglomerate/System gate.

## Gate ownership

This gate belongs to **Modal P0-Q**.

It cannot close:
- Scalar exploration;
- Conglomerate/System exploration;
- joint Scalar + Modal + Conglomerate interpretation;
- full-route P0-D novelty search.

The GOM exploration gate remains open.
