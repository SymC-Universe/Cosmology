# Late-Time Material Relational Scale Map P0-D Adjudication v0.1

**Project:** Cosmic Stability Architecture  
**Date:** 2026-09-29  
**Governance:** SymC GOM v1.0  
**Stage:** post-result P0-D Function/Limit Map  
**Parent plan:** `LATE_TIME_MATERIAL_SCALE_MAP_P0D_PLAN_v0.1.md`  
**Frozen plan commit:** `2eeba60c563d7d32d85c8edf3620471d6c05e406`  
**Workflow:** `36609082654`, SUCCESS  
**Durable result:** `qualification/results/late_time_material_scale_map_p0d.json`  
**Result commit:** `3053cdad168bd80f25a9a5b6b0bd8066ba7c40d1`  
**Seed:** 424242, development-only  
**P1 status:** CLOSED  
**Outcome:** `SCALE_MAP_COMPLETE`

## Governing interpretation

This map is post-result P0-D evidence created after Development 018 exposed material scale dependence. It cannot select a favorable scale, activate P1, or convert seed 424242 into confirmation. It establishes descriptive coarse-graining dependence of the frozen E-sigma relational predictor, not a physical transition threshold from five dyadic points and not a mechanism.

## Frozen scale map

All results reuse N64, L=64 Mpc/h, Band L `0<|n|<4`, z~2 ID-frozen material membership, native co-located electric Weyl, corrected centered velocity shear, the frozen B0/B1 definitions, persistence comparator, and leave-one-octant-out development validation.

| Patch side | Grid | z~2->z~1 Delta_rel | z~2->z~0.5 Delta_rel | Direction | Interpretation |
|---|---:|---:|---:|---|---|
| 32 Mpc/h | 2^3 | -28.7179 | -602.9514 | 5 positive / 3 negative at both endpoints | B1 rank-deficient in 8/8 folds; only 7 training patches/fold; numerical identifiability limit |
| 16 Mpc/h | 4^3 | -0.67395 | -0.75522 | 1/7 then 2/6 positive/negative | full rank but B1 condition number reaches ~847; relational block subtracts strongly |
| 8 Mpc/h | 8^3 | +0.002848 | -0.042384 | 5/3 then 4/4 | full rank; weak/transient signal that does not persist to z~0.5 |
| 4 Mpc/h | 16^3 | +0.009826 | +0.013753 | 5/3 then 6/2 | full rank; relational block adds at both endpoints |
| 2 Mpc/h | 32^3 | +0.021551 | +0.018065 | 7/1 at both endpoints | full rank; relational block adds at both endpoints, with sparse particle support in some patches |

No scale had representation-level patch refusal.

## Function Map

Within seed 424242, 2 and 4 Mpc/h material patches show positive incremental relational prediction at both frozen endpoints. The 8 Mpc/h scale is intermediate and temporally unstable. The 16 Mpc/h scale is strongly subtractive at both endpoints.

Across the estimable 2, 4, 8, and 16 Mpc/h scales, relational utility decreases descriptively with increasing coarse-graining in this realization. This is a same-seed P0-D observation only, not a universal scaling law.

## Limit Map

The 32 Mpc/h partition is structurally underdetermined: eight total patches leave seven training rows per fold for a 19-column B1 design, so every B1 fold is rank-deficient. Its extreme negative Delta_rel values are therefore not admissible subtraction evidence.

The 16 Mpc/h partition is full-rank but poorly conditioned relative to finer scales and strongly negative at both endpoints. The current evidence cannot distinguish genuine coarse-graining loss/reversal from finite-sample regression instability, or a mixture of both.

At 8 Mpc/h, the positive z~1 result does not persist to z~0.5, so the scale is a temporal-stability limit for seed 424242.

## Scientific consequence

Development 018 is refined from generic `SCALE_DEPENDENT_RELATIONAL_ARCHITECTURE_UNRESOLVED` to `P0D_MULTISCALE_RELATIONAL_ORDERING_OBSERVED_SINGLE_REALIZATION`.

The next prospective question is whether this multiscale ordering survives an independent development realization without choosing a best scale. The 32 Mpc/h point remains a prespecified identifiability-limit control and cannot be forced into the predictive claim.

## Next licensed action

Construct and adversarially qualify an APQ-2 Plan Packet for an independent-seed P0-Q scale-pattern validation. Preserve the full dyadic scale family, Band L, z~2 material lineage, z~1 endpoint, z~0.5 continuation, and the frozen relational/marginal feature architecture. Define reproduction, partial reproduction, equivalence, subtraction, need-more-info, and refusal before exposure.

No new seed may be opened before that APQ closes and its plan is frozen. P1 remains closed.
