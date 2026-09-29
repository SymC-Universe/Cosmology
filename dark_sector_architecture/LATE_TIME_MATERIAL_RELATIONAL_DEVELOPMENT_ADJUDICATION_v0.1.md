# Late-Time Material Relational Development Adjudication v0.1

**Project:** Cosmic Stability Architecture  
**Date:** 2026-09-29  
**Governance:** SymC GOM v1.0  
**Source workflow:** 36414756245  
**Source result:** dark_sector_architecture/qualification/results/late_time_material_relational_development.json  
**Frozen APQ:** LATE_TIME_MATERIAL_RELATIONAL_APQ2_ADJUDICATION_v0.1.md  
**Final development disposition:** NEED_MORE_INFO  
**P1 status:** CLOSED

## Adjudication

The machine outcome NEED_MORE_INFO is confirmed under the frozen APQ-2 rules. The reason is specifically the predeclared material-scale sensitivity reversal. It is not a temporal-derivative failure, patch-refusal failure, numerical nonfiniteness failure, or failure of the primary 8 Mpc/h relation itself.

At the frozen primary 8x8x8 material partition, corresponding to 8 Mpc/h patch side length:

- Delta_rel = 0.0028475226718052958;
- shift-null q95 = -0.013009648886971408;
- SSE_B0 = 7.492815392496604;
- SSE_B1 = 7.4714794307908186;
- SSE_persistence = 7.8336779686362785;
- refused patches = 0.

Therefore the primary result alone satisfies all three frozen signal conditions: Delta_rel is positive, it exceeds the shift-null 95th percentile, and B1 beats persistence.

The 16x16x16 sensitivity, corresponding to 4 Mpc/h patch side length, remains directionally positive:

- Delta_rel = 0.009826114779448173;
- SSE_B0 = 67.38727575205485;
- SSE_B1 = 66.72512064584083;
- SSE_persistence = 72.55220923370723.

The 4x4x4 sensitivity, corresponding to 16 Mpc/h patch side length, reverses strongly:

- Delta_rel = -0.6739536170305738;
- SSE_B0 = 0.53093471162734;
- SSE_B1 = 0.8887600809356704;
- SSE_persistence = 0.42810947075422046.

At 16 Mpc/h, B1 is worse than both B0 and persistence. Seven of eight spatial folds are negative, while the primary and fine-scale cases contain majority-positive fold directions. This is a material reversal under the frozen APQ and therefore forces NEED_MORE_INFO.

Temporal E inner/outer relative RMS uncertainty is approximately 3.8e-9 at z~2, 5.2e-9 at z~1, and 6.6e-9 at z~0.5. No patch was refused at the three prespecified scales. The current unresolved issue is therefore scale dependence, not obvious temporal or representation breakdown.

## Scientific interpretation

The result does not justify selecting 8 Mpc/h or 4 Mpc/h because they are favorable. It establishes that the relation is not scale-invariant over the prespecified 4, 8, and 16 Mpc/h material-patch family.

The correct current statement is:

**SCALE_DEPENDENT_RELATIONAL_ARCHITECTURE_UNRESOLVED**

The 8 Mpc/h primary result is preserved as a positive development observation, the 4 Mpc/h sensitivity is preserved as directionally compatible, and the 16 Mpc/h reversal is preserved as equally important counterevidence.

No result activates P1, and seed 424242 remains development-only.

## Continuity failure

Workflow 36414756245 completed successfully on 2026-09-28 and persisted the result, but the development artifact was not adjudicated or advanced for approximately one day because the project continuation monitor was disabled.

Classification:

**CONTINUITY_FAILURE_MONITOR_DISABLED**

This is an operations failure, not a scientific result.

## Next licensed action

Open a post-result P0-D scale-resolution map on the same development seed using a fixed dyadic patch family. The purpose is to locate the scale dependence and identify numerical/conditioning boundaries, not to select a favorable scale or rescue the primary result.

Any future P1 design must be frozen prospectively on independent seeds after the scale issue is understood.
