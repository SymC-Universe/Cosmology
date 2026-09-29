# Late-Time Material Relational Scale Map P0-D Plan v0.1

**Project:** Cosmic Stability Architecture  
**Date:** 2026-09-29  
**Governance:** SymC GOM v1.0  
**Stage:** post-result P0-D exploration  
**Trigger:** frozen development outcome NEED_MORE_INFO due scale reversal  
**P1 status:** CLOSED  
**Seed:** 424242 development-only

## Purpose

Map the material-patch scale dependence exposed by the frozen P0-Q development result without selecting a favorable scale.

The prior frozen result showed positive relational added information at 4 and 8 Mpc/h patch side lengths and strong negative added information at 16 Mpc/h. This plan is explicitly post-result. It cannot be relabeled confirmatory and cannot activate P1.

## Fixed scale family

Use the dyadic material-patch partitions:

- 2x2x2 -> 32 Mpc/h patch side;
- 4x4x4 -> 16 Mpc/h;
- 8x8x8 -> 8 Mpc/h;
- 16x16x16 -> 4 Mpc/h;
- 32x32x32 -> 2 Mpc/h.

The family is chosen because it is the complete practical dyadic hierarchy around the already prespecified 4/8/16 grids in the 64 Mpc/h box. It is not chosen from outcome maxima.

Do not add intermediate or non-dyadic scales after viewing this map.

## Frozen inherited physics and representation

Reuse exactly:

- N64, L=64 Mpc/h;
- seed 424242;
- Band L 0<|n|<4;
- z~2 reference material membership;
- z~1 primary development endpoint;
- z~0.5 continuation;
- native co-located electric Weyl;
- corrected centered velocity shear;
- ID-frozen material lineage;
- B0 marginal/scalar comparator;
- B1 = B0 plus the complete 10-feature E-sigma relation block;
- zero-change persistence benchmark;
- leave-one-octant-out prediction structure.

No new scalar chi is admitted.

## Outputs at every scale

For z~2 -> z~1 and z~2 -> z~0.5 record:

- valid and refused patch counts;
- mean, minimum, and maximum particles per patch;
- SSE_persistence;
- SSE_B0;
- SSE_B1;
- Delta_rel = (SSE_B0-SSE_B1)/SSE_B0;
- foldwise Delta_rel values;
- count of positive, negative, and zero/nonfinite fold directions;
- B0 and B1 matrix rank and condition-number diagnostics;
- whether any fold is rank-deficient relative to the fitted column count.

Do not run a new translation null at the newly added scales. The scale map is descriptive P0-D exploration.

## Interpretation rules

The map may establish descriptive regions such as:

- RELATIONAL_ADDS_AT_SCALE;
- RELATIONAL_SUBTRACTS_AT_SCALE;
- RELATIONAL_EQUIVALENT_OR_WEAK_AT_SCALE;
- NUMERICAL_IDENTIFIABILITY_LIMIT_AT_SCALE;
- REPRESENTATION_REFUSED_AT_SCALE.

These are P0-D map labels only. No threshold on Delta_rel is introduced beyond sign and exact comparator ordering.

Do not:
- choose a best scale;
- promote the first positive scale;
- interpolate a physical transition threshold from the five points;
- treat the same-seed map as replication;
- open P1.

## Stop rules

If the same frozen simulation cannot be reproduced mechanically, stop as MECHANICAL_HOLD.

If one or more scales are numerically underdetermined, preserve them as identifiability limits and continue the other fixed scales where possible.

If the map completes, update the Function Map and Limit Map and use it to construct the next prospectively testable independent-seed question. That later design requires fresh APQ before P1.
