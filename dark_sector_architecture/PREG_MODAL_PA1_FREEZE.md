# PREG-MODAL-PA-1 FREEZE

**Project:** Cosmic Stability Architecture
**Stage:** P1-M preregistration freeze
**Status:** FROZEN / NOT YET EXECUTED
**Date:** 2026-09-28
**Parent qualification:** NATIVE_FIXED_BAND_QUALIFIED_P0Q
**Parent development:** Development 011

## 1. Residual claim after literature subtraction

The broad claims that tidal anisotropy contains information beyond density, that velocity-shear and tidal-web classifications differ in the nonlinear regime, and that shear/electric-Weyl coupling is theoretically real are already occupied by the literature.

The irreducible modal residual is narrower:

> In late-time nonlinear large-scale-structure evolution, the relational state between the native electric-Weyl tensor and the native velocity-shear tensor develops reproducible non-commuting structure beyond the aligned/linear or silent-limit expectation, and the evolution of that relational state is not exhausted by scalar amplitude variables or by either tensor's standalone eigenvalue spectrum.

This is a modal-architecture claim only. It does not claim dark-matter replacement, dark-energy replacement, a new force, a new substance, or a universal scalar chi.

## 2. Primary native statistic

Let S_ij be the native velocity-shear tensor and E_ij the native electric-Weyl tensor on the qualified common physical band.

Define the commutator

\[
C = [S,E] = SE-ES.
\]

The primary dimensionless non-commutation statistic is

\[
\mathcal C_{SE}
=
\frac{\|[S,E]\|_F}
{\|S\|_F\,\|E\|_F}
\]

for cells where both denominator norms are numerically resolvable under the frozen qualification floor.

Properties:
- rotationally invariant;
- zero when S and E commute and therefore admit a common eigenframe;
- does not require choosing an eigenvector direction in a near-degenerate eigenspace;
- does not itself imply magnetic Weyl curvature or gravitational radiation;
- is interpreted as a relational modal coordinate, not a new physical degree of freedom.

Secondary descriptive diagnostics, frozen but not primary:
- ordered eigenvalue spectra of S and E;
- principal-angle/eigenframe alignment only where eigengaps are qualified;
- scalar/vector/tensor electric-Weyl sector participation;
- vorticity magnitude as a nonlinear kinematic covariate;
- density, expansion/divergence, shear norm, Weyl norm, and tidal-anisotropy scalars.

## 3. Validity regime

Primary decisive regime:
- standard LambdaCDM background and conventional early dark gravitational component permitted;
- late matter era into nonlinear structure formation;
- gevolution native weak-field relativistic representation;
- identical box size, cosmological parameters, IC generator family, output definitions, and frozen common physical Fourier support across development and decisive realizations.

The claim is representation-limited to the qualified gevolution native objects unless separately promoted by a full-GR robustness test.

## 4. Strongest admitted literature/native comparators

The preregistration explicitly subtracts:

1. local density or overdensity alone;
2. scalar shear amplitude/norm alone;
3. scalar electric-Weyl/tidal amplitude alone;
4. static tidal anisotropy/eigenvalue-spectrum summaries;
5. standalone velocity-shear eigenvalue-spectrum summaries;
6. standard cosmic-web class labels;
7. matched FLRW/linear-transfer expectation where S and E are proportional/aligned in the linear regime.

The primary modal null is therefore not 'density explains everything.'

The primary modal null is:

> Once the declared scalar amplitudes and standalone tensor spectra are conditioned on, the S-E relational non-commutation field contains no reproducible nonlinear organization beyond finite-resolution, mode-tracking, and ordinary web-environment variation.

## 5. Decisive evidence independence

Qualification and development data already inspected include the known-truth suites, temporal pilot, N32/N64/N128 fixed-band ladder, and all prior gevolution development seeds.

None of those data may confirm PREG-MODAL-PA-1.

Decisive P1-M evidence must use new seeds generated only after this freeze.

Frozen primary decisive set:
- three new independent gevolution seeds;
- one development-independent box per seed;
- N=128 primary resolution;
- identical L=64 Mpc/h box and native fixed physical support inherited from qualification;
- at least four predeclared late-time output epochs spanning increasing nonlinearity;
- no seed replacement because its result is inconvenient;
- a failed realization is preserved and root-caused before any replacement is considered.

An additional N=64 realization for each seed is reserved only for prospective robustness if the N128 result triggers a numerical ambiguity. It is not part of the primary acceptance count.

## 6. Frozen temporal sampling

The decisive run must sample four ordered epochs chosen before outcome inspection by scale factor rather than structure-dependent stopping:

- T1: a = 0.25;
- T2: a = 0.50;
- T3: a = 0.75;
- T4: a = 1.00.

If gevolution cannot stably deliver one of these exact requested outputs, use the actual logged nearest crossing and preserve the discrepancy. Do not retune epochs after inspecting modal results.

## 7. Frozen spatial support and masking

Primary Fourier support remains the qualified N32 active-overlap sphere transferred to N128:

\[
0<|\mathbf n|<15,\qquad |n_i|<15.
\]

No Fourier mode may be removed after outcome inspection.

Cell-level denominator refusal is allowed only under a prospectively computed numerical resolvability mask:
- both ||S||_F and ||E||_F must exceed their propagated reconstruction noise floor;
- the mask is determined from qualification/paired-resolution uncertainty, not from the observed commutator value;
- masked fraction is reported at every epoch and seed;
- if the retained support becomes environmentally selective enough to alter interpretation, outcome is NEED_MORE_INFO rather than a post hoc remask.

## 8. Frozen environment variables

Environment is descriptive/conditioning, not an outcome-tuned classifier.

Predeclared scalar/environment covariates:
- overdensity delta;
- velocity divergence / expansion proxy;
- shear norm;
- electric-Weyl norm;
- tidal anisotropy from the electric-Weyl eigenvalue spectrum;
- standalone ordered spectra of S and E;
- vorticity magnitude.

No learned environment classifier, PCA component, DMD mode, or web-label threshold may replace these primary covariates after outcome inspection.

## 9. Primary tests

### M1. Nonlinear departure test

For each seed and epoch, measure the distribution of C_SE.

The primary within-seed contrast is the predeclared temporal change:

\[
\Delta\mathcal C_{SE}^{1\to4}
=
\mathrm{median}(\mathcal C_{SE,T4})
-
\mathrm{median}(\mathcal C_{SE,T1}).
\]

Secondary temporal contrasts T1->T2, T2->T3, and T3->T4 are descriptive and multiplicity-controlled.

### M2. Scalar/spectrum-conditioned residual test

Fit the frozen null model using only the declared scalar amplitudes, standalone S spectrum, standalone E spectrum, and epoch.

Then test whether C_SE retains structured residual variation across nonlinear environments that is reproducible across all three untouched seeds.

The modal claim does not require a specific sign of association with density, filamentarity, or vorticity. Direction is discovery-level unless separately preregistered.

### M3. Relational-added-information test

Compare two frozen out-of-sample models for a later relational state C_SE(T4):

- Comparator A: T1 scalar/environment covariates plus standalone S and E spectra;
- Comparator B: the same variables plus T1 C_SE.

The endpoint is T4 C_SE itself, not density, halo abundance, lensing, or expansion. Those belong to later joint/conglomerate gates.

Added value is evaluated across held-out seeds, never by in-sample fit.

## 10. Acceptance / refusal / need-more-info logic

### ACCEPT: MODAL_RELATION_ADDS

Accept the residual modal claim only if all are true:

1. C_SE is numerically identifiable on the frozen support in all three decisive seeds;
2. the T1->T4 change has the same non-zero direction in all three seeds and its across-seed uncertainty excludes the numerical-equivalence region defined from qualification uncertainty;
3. the scalar/spectrum-conditioned residual structure is reproducible across seeds;
4. Comparator B improves held-out T4 C_SE prediction over Comparator A in every seed or in the pooled leave-one-seed-out analysis without a seed showing material subtraction;
5. the improvement is larger than the precomputed numerical/representation uncertainty budget;
6. no result requires post hoc Fourier, environment, eigengap, epoch, or masking changes.

### REFUSE: MODAL_RELATION_EQUIVALENT_OR_SUBTRACTS

Refuse the added modal claim for this regime if any decisive condition holds:

1. C_SE is reproducibly equivalent to its numerical-equivalence region across the nonlinear evolution;
2. after conditioning on scalar amplitudes and standalone spectra, no reproducible residual organization remains;
3. adding T1 C_SE is equivalent to or worse than Comparator A on untouched held-out prediction;
4. apparent relational structure disappears under the already-frozen numerical/representation robustness checks;
5. the observed result is fully explained by a known static tidal-anisotropy or standalone shear/tidal spectrum relation.

Refusal retires only this added relational modal claim for the tested regime. It does not erase descriptive shear/Weyl results, close Conglomerate/System exploration, or close P0-D.

### NEED_MORE_INFO: MODAL_RELATION_INDETERMINATE

Use NEED_MORE_INFO when:
- seeds disagree materially in direction;
- effect size is comparable to numerical/representation uncertainty;
- the resolvability mask becomes strongly environment-selective;
- finite-volume variance dominates the cross-seed result;
- one decisive seed fails scientifically or numerically in a way that cannot be repaired without changing the frozen design;
- Comparator B adds value only under one permissible fitting/regularization variant;
- eigenframe secondary diagnostics disagree while the invariant commutator remains ambiguous.

No threshold may be adjusted to convert NEED_MORE_INFO into ACCEPT.

## 11. Equivalence and uncertainty region

No arbitrary universal percentage is frozen.

The numerical-equivalence region is derived prospectively from the qualified representation stack:
- N64->N128 fixed-band difference;
- temporal inner/outer reconstruction difference;
- native-versus-continuum common-band discrepancy as a comparator uncertainty, not as native error;
- seed-independent machine precision/constraint residuals.

The uncertainty budget is propagated through C_SE using the same frozen operator and support before decisive modal outputs are interpreted.

## 12. Multiplicity

Primary family:
- one primary invariant C_SE;
- one primary temporal contrast T1->T4;
- one primary conditioned residual test;
- one primary held-out added-information comparison.

Secondary family:
- three intermediate temporal contrasts;
- eigenframe angles where identifiable;
- sector-specific electric-Weyl participation;
- vorticity-conditioned descriptive maps.

Secondary analyses cannot rescue a failed primary family.

## 13. Explicit falsifier

The modal-architecture residual is falsified for the tested regime if the shear-electric-Weyl relational invariant provides no reproducible information beyond the frozen scalar and standalone-spectrum comparator on untouched realizations, or if its apparent added value is at or below demonstrated numerical/representation uncertainty.

## 14. Hunting Friction targets before execution

Before opening decisive outputs, adversarial review must attempt to show that:

- C_SE is algebraically redundant with the declared spectra;
- C_SE is a disguised vorticity or density statistic;
- the statistic is dominated by weak-field gauge/observer choice;
- the common-band filter manufactures alignment or misalignment;
- denominator masking selects nonlinear environments;
- T1->T4 change is guaranteed trivially by shell crossing and therefore scientifically vacuous;
- the predictive M3 test leaks the endpoint through deterministic evolution;
- silent-universe theory already makes the proposed empirical result non-novel;
- existing T-web/V-web literature already performs the same relational test.

Any BLOCKER must be repaired before activation. MATERIAL objections require a frozen plan delta. MINOR objections are recorded but do not alter the freeze.

## 15. Gate separation

This preregistration tests modal relational structure only.

It does not test:
- whether modal structure improves prediction of growth/lensing/collapse beyond scalar state; that belongs to PREG-JOINT-PA-1;
- whether early modal organization predicts later conglomerate organization; that belongs to PREG-JOINT-PA-2;
- whether one conglomerate state explains collapse and expansion branches; that belongs to PREG-CONGLOMERATE-PA-1.

All exploration gates remain open.
