# Relational Modal Descriptor Preflight v0.1

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q estimator qualification
**APQ level:** APQ-2 bounded preflight under parent APQ-3
**Status:** FROZEN BEFORE M0 OUTPUT
**Date:** 2026-09-27
**Parent Plan Packet:** apq/PREG_MODAL_PA1_PLAN_PACKET_v0.1.md
**Parent Plan Delta:** apq/PREG_MODAL_PA1_PLAN_DELTA_v0.1.md

## Purpose

Qualify a rotation-invariant descriptor of the relational state between two symmetric trace-free modal tensors before any simulation is used to test predictive utility.

This gate does not test cosmological novelty, prediction, dark-sector architecture, or P1 evidence.

## Frozen primary statistic

For finite nonzero symmetric tensors A and B, define

\[
\kappa(A,B)
=
\frac{\|AB-BA\|_F}
{\sqrt{2}\,\|A\|_F\,\|B\|_F}.
\]

For the intended application A = E and B = sigma.

The normalization is chosen from the Böttcher-Wenzel Frobenius commutator bound, so finite matrices satisfy 0 <= kappa <= 1 up to floating-point tolerance.

## Frozen refusal semantics

`REFUSED_ZERO_NORM` when either input tensor has zero Frobenius norm.

`REFUSED_NONFINITE` when either input contains non-finite values.

`REFUSED_SHAPE` when the input is not a 3x3 tensor or tensor field ending in 3x3.

Exact eigenvalue degeneracy does not refuse kappa itself. It refuses directional eigenframe interpretation for the degenerate eigenspace.

No empirical eigengap threshold is introduced in M0.

## Required known-truth cases

### RM-01 Common eigenframe
Two nondegenerate diagonal STF tensors commute.
Expected: kappa = 0 within floating-point precision.

### RM-02 Matched marginals, rotated relation
Keep both eigenvalue spectra fixed and orthogonally rotate only B relative to A.
Expected:
- all one-tensor spectral invariants remain unchanged;
- kappa becomes nonzero for a noncommuting rotation;
- therefore kappa contains relational information not present in the marginal spectra alone.

### RM-03 Coordinate covariance
Apply the same orthogonal coordinate rotation Q to both tensors.
Expected:
\[
\kappa(QAQ^T,QBQ^T)=\kappa(A,B).
\]

### RM-04 Exchange symmetry
Expected:
\[
\kappa(A,B)=\kappa(B,A).
\]

### RM-05 Bound
Across a deterministic random ensemble of finite real 3x3 tensor pairs:
Expected: kappa remains within [0,1] up to numerical tolerance.

### RM-06 Zero-norm refusal
At least one tensor identically zero.
Expected: explicit refusal, not kappa = 0.

### RM-07 Degenerate eigenframe distinction
Use a tensor with a repeated eigenvalue and a finite nonzero partner.
Expected:
- kappa remains numerically defined when norms are nonzero;
- eigenframe-direction status is `DEGENERATE_NONIDENTIFIABLE` for the repeated eigenspace;
- no directional conclusion is silently made from kappa.

## Secondary diagnostics

The implementation may report:
- Frobenius norms;
- commutator norm;
- ordered eigenvalues;
- eigengaps;
- absolute eigenframe alignment where nondegenerate;
- normalized trace alignment tr(AB)/(||A||_F ||B||_F).

These are diagnostics only. They cannot replace kappa as the primary M0 object after results are seen.

## Acceptance

`RELATIONAL_DESCRIPTOR_QUALIFIED_P0Q` only if RM-01 through RM-07 all pass without outcome-dependent changes.

## Need more information

`NEED_MORE_INFO` if:
- a numerical tolerance cannot be justified from floating-point/known-truth behavior;
- degeneracy semantics are ambiguous;
- the implementation passes some identities but not others for a reason that is not yet classified.

## Refusal

`RELATIONAL_DESCRIPTOR_REFUSED` if:
- coordinate invariance fails;
- matched-marginal rotation does not change the statistic as expected;
- zero-norm inputs are silently interpreted as alignment;
- the bound is violated beyond explained floating-point error;
- implementation requires post-result special cases.

## Consequence

If QUALIFIED:
- M0 licenses only the descriptor as a measurement/tool object;
- the next gate is a separately APQ-qualified standard-dynamics development preflight for conditional predictive utility.

If REFUSED:
- do not repair by changing the statistic after viewing cosmological outcomes;
- standalone PREG-MODAL-PA-1 remains NOT_ACTIVATED unless a new independently justified descriptor enters P0-D/P0-Q.

Conglomerate/System and joint exploration remain open under every outcome.
