# PREG-MODAL-PA-1 Adversarial Plan Qualification

**Project:** Cosmic Stability Architecture  
**Stage:** APQ before P1-M activation  
**Status:** QUALIFIED PLAN AFTER MATERIAL REVISIONS / NOT YET ACTIVATED  
**Date:** 2026-09-28

## Plan packet

### Question

Does the local noncommutativity of the native velocity-shear tensor and full electric-Weyl tensor carry predictive information about subsequent nonlinear shear reorganization after current scalar state, the complete separate tensor spectra, and a simpler static tensor-alignment scalar are already provided?

### Primary predictor

\[
C_{\sigma E}
=
\frac{\|[\sigma,E]\|_F}
{\sqrt{2}\,\|\sigma\|_F\,\|E\|_F}.
\]

### Primary target

\[
R_\sigma(t_0,t_1)
=
\frac{\|\sigma(t_1)-\sigma(t_0)\|_F}
{\|\sigma(t_1)\|_F+\|\sigma(t_0)\|_F}.
\]

### Prediction epoch and horizon

- prediction epoch: a0 = 1/3, z0 = 2;
- future epoch: a1 = 1/2, z1 = 1;
- all modal fields are compared on the already-qualified K32 physical Fourier support in a 64 Mpc/h box.

### Strong baseline

The baseline contains present scalar state, both separate tensor spectra, and one simpler static cross-tensor relation:

- delta_T00;
- native velocity divergence theta;
- Phi;
- chi_gev;
- ||E||_F;
- q_E = 3 sqrt(6) det(E) / [tr(E^2)]^(3/2);
- ||sigma||_F;
- q_sigma = 3 sqrt(6) det(sigma) / [tr(sigma^2)]^(3/2);
- A_sigmaE = tr(sigma E) / (||sigma||_F ||E||_F).

The augmented model adds only C_sigmaE.

### Untouched evidence route

Hash source string:

`SymC PREG-MODAL-PA-1 P1-M seeds v1`

SHA-256 32-bit chunks modulo 2^31-1 give:

- N64 seed A: 171802845;
- N64 seed B: 351644392;
- N64 seed C: 591375351;
- N128 final holdout: 1968479875.

Repository search before freeze found none of these seeds in the existing Cosmology branch.

Qualification seed 424242 is prohibited from P1-M confirmation.

### Prediction model

Primary estimator:

`sklearn.ensemble.HistGradientBoostingRegressor` from scikit-learn 1.7.2.

Frozen parameters:

- loss = squared_error;
- learning_rate = 0.05;
- max_iter = 300;
- max_leaf_nodes = 31;
- max_depth = None;
- min_samples_leaf = 64;
- l2_regularization = 1.0;
- max_bins = 255;
- early_stopping = False;
- random_state = 20260928.

No outcome-dependent hyperparameter search is allowed.

### Cross-validation

For the three N64 seeds, use leave-one-seed-out prediction:

- train on two seeds;
- evaluate on the untouched third seed;
- rotate through all three seeds.

The N128 seed is not used for model selection or N64 adjudication. After the N64 gate is evaluated, train on all three N64 seeds using the unchanged frozen model and evaluate once on the N128 holdout.

### Spatial uncertainty

Each K32 holdout grid is partitioned into 4 x 4 x 4 macroblocks of 8 x 8 x 8 cells, corresponding to 16 Mpc/h blocks.

For each block compute

\[
D_b = \mathrm{MSE}_{baseline,b}-\mathrm{MSE}_{augmented,b}.
\]

A positive value favors the commutator-augmented model.

Use a hierarchical bootstrap with 10,000 replicates:

1. resample the three N64 held-out seeds with replacement;
2. within each selected seed, resample its 64 spatial blocks with replacement;
3. calculate the pooled mean D_b.

Bootstrap RNG seed: 20260928.

### Deterministic spatial-shift controls

On the K32 grid define the seven nonzero half-box offsets using 16-cell shifts in x, y, and z:

(16,0,0), (0,16,0), (0,0,16), (16,16,0), (16,0,16), (0,16,16), (16,16,16).

For each control, shift C_sigmaE relative to every baseline feature and target in both training and test seeds, refit the unchanged augmented estimator, and compute the same out-of-sample improvement.

This preserves the commutator field distribution and large-scale texture while breaking the local relational pairing.

## Adversarial attacks and resolutions

### APQ-01: Broad novelty collapse

**Attack:** Tidal anisotropy beyond density is already established. Generic modal added value would rediscover prior art.

**Severity:** BLOCKER for the broad candidate.

**Resolution:** Narrow the residual to the shear-electric-Weyl noncommutativity predictor after the static tidal/shear spectra and scalar state are already controlled.

### APQ-02: The commutator itself is known

**Attack:** [sigma,E]=0 and simultaneous diagonalization are established covariant constraints in silent/purely electric irrotational dust.

**Severity:** MATERIAL.

**Resolution:** No novelty is claimed for the mathematical commutator. The residual is its prospective field-level predictive use under a hard baseline and untouched simulation evidence.

### APQ-03: Electric Weyl may merely restate Newtonian tides

**Attack:** Electric Weyl has a Newtonian tidal limit.

**Severity:** MATERIAL.

**Resolution:** No claim that E is intrinsically new relativistic information. The test concerns the relational state between independently reconstructed native E and velocity shear, with the native GR representation preserved.

### APQ-04: Static alignment could explain any commutator signal

**Attack:** C_sigmaE might win only because the baseline omits simpler tensor alignment.

**Severity:** MATERIAL.

**Resolution:** Include A_sigmaE = tr(sigma E)/(||sigma|| ||E||) in the baseline. C_sigmaE must add information beyond that simpler alignment scalar.

### APQ-05: Separate tensor spectra could explain any effect

**Attack:** Noncommutativity may only proxy eigenvalue anisotropy already known to affect evolution.

**Severity:** MATERIAL.

**Resolution:** Baseline includes amplitude and complete normalized cubic spectral shape for both E and sigma.

### APQ-06: Current shear trivially predicts future shear

**Attack:** The task could reduce to autocorrelation.

**Severity:** MATERIAL.

**Resolution:** Baseline already contains the complete current shear spectrum and scalar dynamical state. The hypothesis concerns incremental out-of-sample value of C_sigmaE.

### APQ-07: Spatial leakage

**Attack:** Random cell splits would place correlated neighboring cells in train and test and inflate performance.

**Severity:** BLOCKER.

**Resolution:** No random cell split. Primary validation is leave-one-independent-seed-out. Spatial blocks are used only for uncertainty quantification within held-out seeds.

### APQ-08: Qualification reuse as confirmation

**Attack:** Seed 424242 and early z approximately 99 fields have already influenced representation design.

**Severity:** BLOCKER.

**Resolution:** P1-M uses four hash-derived untouched seeds never used in the qualification chain. Seed 424242 is prohibited.

### APQ-09: Finite-resolution artifact

**Attack:** Added value may depend on N64 lattice behavior.

**Severity:** MATERIAL.

**Resolution:** Primary statistical development uses three independent N64 seeds on K32. A completely untouched N128 seed on the same K32 band is mandatory for final ACCEPT.

### APQ-10: Full-grid ultraviolet contamination

**Attack:** Development 010 showed strong finite-grid operator sensitivity.

**Severity:** BLOCKER if unrestricted grid is used.

**Resolution:** All tensors and scalar fields used in the prediction test are projected onto the prospectively fixed K32 band after native reconstruction.

### APQ-11: Early linear alignment makes the test vacuous

**Attack:** At z approximately 99, sigma and E are nearly aligned and C_sigmaE is expected to be tiny.

**Severity:** MATERIAL.

**Resolution:** P1-M prediction epoch is z=2 and outcome epoch is z=1. Early qualification fields are not used as decisive evidence.

### APQ-12: Temporal reconstruction could dominate C_sigmaE

**Attack:** Full electric-Weyl vector/tensor temporal derivatives may be poorly resolved at z=2.

**Severity:** MATERIAL.

**Resolution:** Use five actual-time snapshots around a0 and nested inner/outer derivative reconstructions. If the induced uncertainty competes with the observed relational signal or changes the P1 conclusion, outcome is NEED_MORE_INFO.

### APQ-13: Eulerian advection confound

**Attack:** Same-coordinate shear change is not a Lagrangian particle history.

**Severity:** MATERIAL to interpretation, not to the statistical test.

**Resolution:** The claim is explicitly field-level and Eulerian. No particle-history or halo-assembly interpretation is permitted from v1.

### APQ-14: Low-amplitude orientation instability

**Attack:** C_sigmaE is undefined when either tensor norm is zero and unstable near exact degeneracy.

**Severity:** MATERIAL.

**Resolution:** Exact zero-norm cells are recorded as undefined, not forced to zero. No nonzero amplitude cutoff is allowed. Eigengap and amplitude distributions are reported. If result interpretation depends on a post hoc amplitude or eigengap cut, outcome is REFUSED.

### APQ-15: Black-box model dependence

**Attack:** Hyperparameter search could manufacture incremental prediction.

**Severity:** MATERIAL.

**Resolution:** Freeze one estimator family and parameters before P1-M, prohibit hyperparameter tuning, require independent N128 holdout, and use deterministic shifted-field controls.

## APQ outcome

**QUALIFIED AFTER MATERIAL REVISION.**

The broad modal claim is refused. The surviving plan tests one bounded relational observable, one primary future target, one frozen estimator, independent-seed generalization, deterministic spatial controls, and a higher-resolution holdout.

No P1-M field from the four untouched seeds may be inspected until the final preregistration file is committed.
