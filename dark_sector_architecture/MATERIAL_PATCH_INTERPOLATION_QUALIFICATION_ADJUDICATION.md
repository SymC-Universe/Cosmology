# Material-Patch Tensor Interpolation Qualification Adjudication

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q material representation qualification
**Date:** 2026-09-27
**Frozen plan:** MATERIAL_PATCH_INTERPOLATION_QUALIFICATION_PLAN_v0.1.md
**Frozen plan commit:** bf515b294f3f3b725a361c59177fbb083e201c21
**Decisive qualification run:** 36366019003
**Run head:** ba65b95f64f833af874a382d5e88c2b14302f93d
**P1 exposed:** NO

## Outcome

\[
\boxed{\text{MATERIAL\_PATCH\_INTERPOLATION\_QUALIFIED\_P0Q}}
\]

All frozen known-truth cases MP-01 through MP-12 pass.

## Preserved failure and root cause

The first integrated qualification run, 36365910881, failed MP-02 before report generation.

Root cause: the test harness compared the correct `(200,3,3)` interpolated constant-field output with an explicitly shaped `(1,3,3)` expected array. `numpy.testing.assert_allclose` does not broadcast mismatched shapes for this assertion. The numerical values shown in the failure were already the expected constant tensor.

Classification:
- mechanical/test-harness failure;
- not an interpolation implementation failure;
- not scientific evidence.

Repair:
- changed only the expected test array to an explicit broadcast with the same `(200,3,3)` shape;
- no interpolation code, qualification plan, tolerance, or scientific semantics changed.

The repaired run 36366019003 passes the full integrated suite and generated the durable report.

## Known-truth results

| Case | Result | Key diagnostic |
| --- | --- | --- |
| MP-01 vertex exactness | PASS | max error 0 |
| MP-02 constant tensor | PASS | max error 4.44e-16 |
| MP-03 periodic wrap | PASS | max error 8.33e-17 |
| MP-04 linearity | PASS | max error 8.88e-16 |
| MP-05 symmetry/trace | PASS | symmetry 0; trace 4.44e-16 |
| MP-06 smooth convergence | PASS | N16->32 ratio 3.902; N32->64 ratio 4.050 |
| MP-07 ID reorder invariance | PASS | max error 0 |
| MP-08 deterministic reference partition | PASS | 8 particles assigned exactly once |
| MP-09 frozen material membership | PASS | ID-joined patch labels preserved |
| MP-10 patch mean | PASS | mean error 5.55e-17; reorder error 0 |
| MP-11 patch modal recovery | PASS | nondegenerate eigensystem recovered; degenerate control flagged |
| MP-12 fail-closed semantics | PASS | duplicate IDs, changed ID set, bad patch shape, nonfinite positions, nonsymmetric tensors refused |

## Qualified semantics

The qualified material representation is:

1. co-located vertex tensor components are interpolated to particle positions by periodic trilinear interpolation;
2. local eigensystems are computed only after tensor-component interpolation;
3. particle identities are joined by stable ID, not array order;
4. material patch membership is frozen from a reference snapshot and follows those IDs thereafter;
5. equal-mass CDM patch tensors are arithmetic particle means and are therefore material-mass-weighted states, not volume averages;
6. empty patches are omitted/reported, never encoded as zero tensors;
7. patch-grid scale and reference epoch remain scientific design variables and were not selected by this infrastructure qualification.

## Claim ceiling

Supported:
- vertex-grid tensors can be interpolated reproducibly to tracked particle positions;
- ID-frozen non-overlapping material patch membership is operational;
- equal-mass patch tensor aggregation is deterministic and order-invariant;
- known patch eigensystems and degeneracy semantics are recovered.

Not supported:
- any particular scientific patch scale;
- any claim that a material patch is the correct cosmological coarse-graining scale;
- late-time E-sigma predictive added value;
- inheritance, conglomerate, or dark-sector mechanism claims;
- any P1 result.

## Next licensed action

Run APQ/freeze for the late-time Band-L material relational development design before inspecting any real E-sigma material-patch outcome.

The next plan must prospectively choose or bound:
- reference epoch;
- patch scale family;
- Band-L filtering order and lattice semantics;
- E and sigma relational descriptors;
- later modal endpoint;
- persistence/autoregressive comparator;
- development-only seed usage;
- acceptance/refusal/need-more-info semantics;
- stopping rule.

Seed 424242 remains development-only. Untouched P1 remains closed.
