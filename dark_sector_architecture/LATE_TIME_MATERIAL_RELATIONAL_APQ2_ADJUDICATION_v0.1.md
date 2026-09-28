# Late-Time Band-L Material Relational APQ-2 Adjudication v0.1

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q development design
**APQ level:** APQ-2 SUBSTANTIAL
**Date:** 2026-09-28
**Parent plan:** LATE_TIME_MATERIAL_RELATIONAL_APQ2_PLAN_PACKET_v0.1.md
**P1 status:** CLOSED
**Outcome:** PLAN QUALIFIED WITH ONE MATERIAL DELTA / DEVELOPMENT EXECUTION LICENSED

## 1. Bounded stopping rule

APQ stops when every prespecified BLOCKER/MATERIAL attack in the parent packet is either resolved, prospectively repaired, converted into an explicit sensitivity/limitation, or assigned NEED_MORE_INFO semantics, and no unresolved item can change the development claim, primary endpoint, comparator family, primary scale, validation structure, or outcome namespace without new evidence.

That condition is met after the Plan Delta below.

## 2. Attack A: 8 Mpc/h primary material-patch scale

**Class:** MATERIAL, resolved.

Band L is frozen to 0<|n|<4 in L=64 Mpc/h, so the shortest retained wavelength is approximately 16 Mpc/h. An 8 Mpc/h material-patch spacing is therefore the Nyquist sampling scale for the retained band rather than an outcome-selected convenience.

At N64, the 8x8x8 reference partition contains 512 patches and approximately 512 equal-mass CDM particles per patch before late-time deformation. The qualified interpolation/ID-frozen aggregation machinery supports this scale.

The scale is not claimed to be physically unique. The predeclared 4x4x4 and 16x16x16 families remain directional sensitivities. If they materially reverse interpretation, the result is NEED_MORE_INFO rather than scale selection.

**Disposition:** primary 8x8x8 retained.

## 3. Attack B: material-patch averaging may erase local relational information

**Class:** MATERIAL, resolved by claim scope.

A patch mean is not intended to preserve every local E-sigma relation. It defines the prospectively chosen coarse-grained material state after component interpolation and ID-frozen aggregation.

The claim is therefore about the **8 Mpc/h material-patch relation**, not the voxel-level or particle-level relation.

MP-01 through MP-12 already qualify deterministic component interpolation, lineage preservation, patch means, and aggregate-then-diagonalize semantics.

**Disposition:** no method change. Fine/coarse scale sensitivity remains mandatory.

## 4. Attack C: normalized eigenshape-change endpoint

**Class:** MATERIAL, resolved.

The endpoint is not constructed from the relational feature block and therefore does not leak B1 into Y.

For each trace-free tensor, ordered eigenvalues normalized by Frobenius norm encode modal shape independently of overall amplitude. Using the first two ordered normalized eigenvalues is redundant only in the benign sense that the trace-free third eigenvalue is determined from them; it does not import relational geometry.

The z~2 baseline already includes the corresponding marginal spectra, making the target a true subsequent change relative to an autoregressive state.

**Disposition:** Y_2->1 retained as primary; Y_2->0.5 remains secondary continuation only.

## 5. Attack D: strongest standard tidal/kinematic baseline

**Class:** MATERIAL, resolved.

Prior literature already establishes that tidal anisotropy contains information beyond density [Ram19, Par17], that T-web and V-web diverge nonlinearly [Hof12b], and that velocity-shear eigenframes evolve with nonlinearity [Lib13]. Electric Weyl reduces to the Newtonian tidal tensor in the appropriate limit [Ehl09, Ip16].

Therefore B0 must not be a density-only comparator.

The frozen B0 contains material count contrast, Band-L velocity divergence, E norm, sigma norm, complete ordered normalized E spectrum, and complete ordered normalized sigma spectrum. Density plus the complete E spectrum contains standard tidal-anisotropy/T-web sign information; sigma spectrum contains the V-web marginal state. B1 adds only relational E-sigma geometry.

**Disposition:** comparator judged sufficiently strong for the P0-Q development screen.

## 6. Attack E: spatial blocking and pseudo-replication

**Class:** MATERIAL, resolved as development-only limitation.

Leave-one-octant-out validation prevents random neighboring-patch leakage, but Band-L includes wavelengths comparable to or larger than a 32 Mpc/h octant. Therefore the eight folds are not independent cosmological realizations.

Spatial-block CV is used only to measure within-volume transfer during P0-Q development. It cannot provide P1 replication or a sample-size claim.

Untouched P1, if later frozen, must use independently seeded volumes as the primary replication unit.

**Disposition:** octant CV retained with explicit claim ceiling.

## 7. Attack F: 511 periodic spatial-shift null

**Class:** MATERIAL, resolved as a development randomization screen.

Random/torus-shift literature warns that toroidal wrapping can invalidate nulls for non-periodic smooth fields by introducing an autocorrelation crack [Mrk19]. The present gevolution box is itself periodic, so the boundary crack failure mechanism does not apply in the same way.

However, the 511 translated values are not independent draws, especially under long Band-L modes. They are therefore not interpreted as a formal P1 p-value.

The shift screen asks only whether the observed zero-shift relational block is unusually useful compared with all nonzero periodic re-pairings under the same one-volume geometry.

**Disposition:** full 511-shift null retained solely for development screening.

## 8. Attack G: OLS multicollinearity and relational-block capacity

**Class:** MATERIAL, resolved with fail-closed diagnostics.

The 9 absolute overlap entries and normalized commutator are intentionally retained as one block to avoid outcome-selected relational features. Their internal constraints can create conditioning problems.

Primary fitting remains deterministic standardized multi-output least squares using a Moore-Penrose/least-squares solution. For every fold report B0/B1 nonconstant column count, numerical matrix rank, condition number, and coefficient/prediction finiteness.

No coefficient-level mechanistic interpretation is allowed.

If B1 numerical nonidentifiability produces unstable/nonfinite held-out prediction, outcome is NEED_MORE_INFO. No feature is dropped after exposure.

**Disposition:** OLS retained for the development screen.

## 9. Attack H: missing persistence/autoregressive benchmark

**Class:** MATERIAL PLAN DEFECT, prospectively repaired.

The parent APQ lineage explicitly required a persistence/autoregressive comparator, but v0.1 did not instantiate one as a separate benchmark.

### Plan Delta APQ2-D1

Add baseline P with prediction Y_hat_P = 0 for the primary change target, equivalent to predicting that the z~2 normalized marginal modal shapes persist unchanged to z~1.

Report SSE_P, SSE_B0, and SSE_B1.

DEVELOPMENT_SIGNAL_PRESENT now requires all of:

1. observed Delta_rel=(SSE_B0-SSE_B1)/SSE_B0 > 0;
2. observed Delta_rel exceeds the empirical 95th percentile of the 511 nonzero-shift null;
3. SSE_B1 < SSE_P.

If B1 beats B0 but does not beat persistence, classify DEVELOPMENT_EQUIVALENT_OR_UNRESOLVED.

Persistence does not enter the shift-null recalculation because it contains no relational block and is invariant under the shifts.

**Disposition:** repaired before outcome exposure.

## 10. Attack I: temporal derivative density

**Class:** MATERIAL, resolved by inherited qualification.

Each central epoch uses five requested scale factors with +/-0.25% and +/-0.5% offsets, actual logged conformal times, and the already-qualified arbitrary-node inner/outer temporal derivative machinery.

The time-step limit 0.0005 previously produced distinct neighboring cycles in the electric-Weyl temporal qualification.

If any requested late-time cluster collapses onto non-distinct cycles or inner/outer uncertainty becomes comparable to the endpoint change, the development result is NEED_MORE_INFO/REFUSED according to the parent plan.

**Disposition:** temporal design retained.

## 11. Attack J: tautology / deterministic-state objection

**Class:** MATERIAL, resolved by residual definition.

E and sigma are dynamically coupled, so some relationship is expected from standard dynamics. The test does not claim otherwise.

B0 already contains their complete current marginal spectra and scalar state. B1 asks whether their relative geometry contains incremental information about subsequent separate spectrum change along the same material lineage.

A positive result is therefore an information/organization result inside standard LambdaCDM dynamics, not evidence for a new force, new substance, or uniquely relativistic mechanism.

A negative result is scientifically admissible and retires this development route without erasing the qualified modal representations.

## 12. Attack K: novelty / literature collision

**Class:** MATERIAL, resolved by prior APQ narrowing.

The development claim excludes tidal anisotropy beyond density [Ram19, Par17], T/V-web nonlinear disagreement [Hof12b], shear eigenframe evolution/vorticity relation [Lib13], and Newtonian tidal information already carried by electric Weyl [Ehl09, Ip16].

The residual is prospective added information from the **relation between complete marginal tensor states** for subsequent marginal modal change along frozen material lineage.

No identified source in the adversarial search already performs this exact test.

This supports development novelty only. It is not yet a publication-level novelty verdict for a final P1 result.

## 13. Final frozen development design after Plan Delta

Primary:
- seed 424242 only;
- N64, L=64 Mpc/h;
- Band L 0<|n|<4;
- reference z~2 material membership;
- primary z~1 endpoint;
- 8x8x8 material patches;
- 4x4x4 and 16x16x16 sensitivity only;
- filter native co-located E, centered sigma, theta before particle interpolation;
- aggregate components by frozen IDs before eigensystem construction;
- B0 as frozen marginal/scalar comparator;
- B1=B0+entire 10-feature relation block;
- P: zero-change persistence predictor;
- leave-one-octant-out validation;
- 511 nonzero periodic relation-block shifts;
- primary Delta_rel plus SSE_P requirement.

## 14. Development outcome namespace

### DEVELOPMENT_SIGNAL_PRESENT

Use only if all representation/lineage/fold gates pass, Delta_rel > 0, Delta_rel exceeds the 95th percentile of the 511-shift development null, SSE_B1 < SSE_P, and the primary 8x8x8 result is not contradicted by a sensitivity result in a way requiring a new scientific design.

### DEVELOPMENT_SUBTRACTS

Use if Delta_rel < 0 and below the 5th percentile of the shift null, or B1 materially worsens prediction relative to both B0 and persistence.

### DEVELOPMENT_EQUIVALENT_OR_UNRESOLVED

Use when B1 does not satisfy the signal rule, B1 improves B0 but not persistence, observed Delta_rel lies within the shift-null central region, or the effect is directionally weak without a representation failure.

### NEED_MORE_INFO

Use for numerical nonidentifiability, excessive patch refusal, temporal uncertainty comparable to endpoint change, material scale sensitivities that materially change interpretation, or spatial/finite-volume behavior that prevents a stable development reading.

### REFUSED

Use only for a failed frozen representation/lineage/analysis contract.

## 15. APQ disposition

No unresolved BLOCKER remains.

All prespecified MATERIAL objections are resolved, prospectively repaired, or mapped to explicit NEED_MORE_INFO semantics.

Therefore:

LATE_TIME_MATERIAL_RELATIONAL_DEVELOPMENT = LICENSED
P1-M = CLOSED
SEED_424242 = DEVELOPMENT_ONLY

The first real patch-level E-sigma development outcome may now be opened under the frozen design and APQ2-D1.

## 16. Exploration firewall

Any development outcome leaves open modal P0-D exploration, Conglomerate/System, joint Scalar + Modal + Conglomerate, Stability Inheritance, and additional architecture components.

A positive development result cannot promote capital-Chi or dark-sector mechanism claims. A negative result cannot close those independent gates.
