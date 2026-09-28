# SUPERSEDED PRE-EXPOSURE RECOVERY BRANCH - DO NOT ACTIVATE

This preregistration was frozen during timeout recovery before the authoritative later APQ-3 / Development 014-017 lineage was fully reloaded. No seed listed in this file was opened. It is superseded prospectively by:

- `PREG_MODAL_PA1_APQ3_PLAN_PACKET.md`;
- `PREG_MODAL_PA1_APQ3_ADJUDICATION.md`;
- `LATE_TIME_MATERIAL_RELATIONAL_APQ2_PLAN_PACKET_v0.1.md`;
- `LATE_TIME_MATERIAL_RELATIONAL_APQ2_ADJUDICATION_v0.1.md`.

The conflict is scientific-design, not evidence-driven: the authoritative lineage requires Band-L coarse-grained peculiar-velocity validity and ID-frozen material lineage, whereas this recovery branch proposed a direct Eulerian K32 target. Because no P1 evidence was opened, this branch is preserved as an abandoned preregistration and has no adjudication authority.

---
# PREG-MODAL-PA-1 v1

## Title

Prospective test of shear-electric-Weyl noncommutativity as added predictive information for nonlinear shear reorganization

**Project:** Cosmic Stability Architecture  
**Stage:** P1-M preregistration  
**Status:** FROZEN / NOT YET OPENED  
**Date:** 2026-09-28  
**Stage A residual:** PREG_MODAL_PA1_STAGE_A_RESIDUAL.md  
**APQ:** PREG_MODAL_PA1_APQ.md

## 1. Claim being tested

### H0

After current scalar state, the complete separate spectra of the native velocity-shear and full electric-Weyl tensors, and a simpler static tensor-alignment scalar are provided, the bounded shear-electric-Weyl noncommutativity observable C_sigmaE provides no reproducible out-of-sample improvement for predicting subsequent Eulerian shear reorganization.

### H1

Under the same controls, C_sigmaE provides reproducible out-of-sample predictive improvement for subsequent Eulerian shear reorganization on independent initial-condition realizations and an untouched higher-resolution holdout.

No claim is made that the commutator itself is novel, that electric Weyl is non-Newtonian by definition, or that a positive result establishes new physics.

## 2. Native representation

All modal objects use the already-qualified gevolution/LATfield2-native representation.

Full first-order electric Weyl:

\[
E_{ij}
=
D_{ij}\left(\Phi-\frac{\chi_{\rm gev}}{2}\right)
-\frac12\partial_{(i}B'_{j)}
-\frac14\left(h''_{ij}+\nabla^2h_{ij}\right),
\]

with the frozen project curvature convention and native lattice spatial operators.

Native velocity shear:

\[
\sigma_{ij}=\mathrm{STF}[\partial_{(i}v_{j)}]
\]

using the same LATfield2/gevolution staggering.

All decisive fields are projected after native reconstruction onto the frozen K32 support:

\[
0<|\mathbf n|<15,\qquad |n_i|<15
\]

in a 64 Mpc/h periodic box.

## 3. Primary relational predictor

For cells where both tensor norms are nonzero:

\[
C_{\sigma E}
=
\frac{\|[\sigma,E]\|_F}
{\sqrt{2}\,\|\sigma\|_F\,\|E\|_F}.
\]

By the Frobenius commutator bound, C_sigmaE is bounded between 0 and 1.

Exact zero-norm cells are recorded as orientation-undefined and retained as missing predictor values. No nonzero amplitude or eigengap threshold may be introduced.

## 4. Baseline feature set

The baseline contains exactly nine present-state features:

1. delta_T00 = T00 / mean(T00) - 1;
2. native velocity divergence theta;
3. Phi;
4. chi_gev;
5. ||E||_F;
6. q_E = 3 sqrt(6) det(E) / [tr(E^2)]^(3/2);
7. ||sigma||_F;
8. q_sigma = 3 sqrt(6) det(sigma) / [tr(sigma^2)]^(3/2);
9. A_sigmaE = tr(sigma E) / (||sigma||_F ||E||_F).

q_E, q_sigma, and A_sigmaE are missing only where their exact mathematical denominator is zero. No outcome-dependent imputation or filtering is allowed.

The augmented model contains the same nine features plus C_sigmaE and no other added feature.

## 5. Primary outcome

Prediction epoch:

\[a_0=1/3,\qquad z_0=2.\]

Future epoch:

\[a_1=1/2,\qquad z_1=1.\]

At each K32 cell,

\[
R_\sigma
=
\frac{\|\sigma(a_1)-\sigma(a_0)\|_F}
{\|\sigma(a_1)\|_F+\|\sigma(a_0)\|_F}.
\]

R_sigma is the sole primary outcome.

If both shear norms are exactly zero, the outcome is undefined and the cell is excluded only because the mathematical target does not exist. The number of such cells is reported.

## 6. Secondary non-gating outcome

\[
G_\rho
=
\ln\left[
\frac{1+\delta_{T00}(a_1)}
{1+\delta_{T00}(a_0)}
\right].
\]

This secondary outcome is reported but cannot change the v1 ACCEPT / REFUSE / NEED_MORE_INFO classification.

## 7. Temporal reconstruction around a0

The requested five derivative snapshots are frozen at scale factors:

- 0.320000000000;
- 0.326666666667;
- 0.333333333333;
- 0.340000000000;
- 0.346666666667.

The center is the third snapshot.

Actual logged conformal times tau/L are used. No equal-spacing assumption is allowed.

Inner derivative stencil: snapshots 1,2,3.  
Outer derivative stencil: snapshots 0,2,4.

The inner reconstruction is primary. The complete prediction analysis is repeated with the outer electric-Weyl reconstruction as a temporal robustness analysis.

If derivative snapshots land on duplicate cycles, that simulation is mechanically invalid and its scientific fields remain unopened. The time-step limit may be halved and the simulation rerun until five distinct cycles are obtained. This mechanical repair does not alter the frozen scale factors, seeds, features, outcomes, or adjudication logic.

Future output at a1 = 0.5 provides native velocity and T00 for the primary and secondary outcomes.

## 8. Untouched simulations

Seed-generation string:

`SymC PREG-MODAL-PA-1 P1-M seeds v1`

The first four SHA-256 32-bit chunks modulo 2^31-1 define:

- N64 seed A = 171802845;
- N64 seed B = 351644392;
- N64 seed C = 591375351;
- N128 final holdout = 1968479875.

These seeds were absent from the repository before this freeze.

Qualification seed 424242 is prohibited from confirmation.

Common simulation settings:

- box = 64 Mpc/h;
- canonical gevolution 1.3 commit 0cca42e51a824002ae4fb602cbd79d671e8ffe60;
- canonical CPU LATfield2 commit 2d8c737ab6adc965a1d2718c209f5085af27b09c;
- canonical sc1_crystal.dat blob d4de9a5400ef58f6a0181fbe61f18056b233a425;
- TENSOR_EVOLUTION;
- VELOCITY;
- dynamic-hij snapshot patch already qualified at P0-Q;
- snapshot outputs required at a0 derivative epochs and a1: phi, chi, B, hij, v, T00.

Primary N64 tiling factor = 16.  
N128 holdout tiling factor = 32.

## 9. Primary estimator

Software:

- Python 3.12;
- scikit-learn 1.7.2.

Estimator:

`sklearn.ensemble.HistGradientBoostingRegressor`

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

No model-family search and no hyperparameter search are permitted after P1-M data are opened.

## 10. N64 leave-one-seed-out evaluation

For each of the three N64 seeds:

1. train the baseline estimator on the other two seeds;
2. train the augmented estimator on the same two seeds;
3. evaluate both once on the untouched held-out seed.

For held-out seed s define:

\[
\Delta_s
=
\mathrm{MSE}_{baseline,s}
-\mathrm{MSE}_{augmented,s}.
\]

Positive Delta_s favors added predictive information from C_sigmaE.

No random cell-level train/test split is allowed.

## 11. Hierarchical spatial uncertainty

Each held-out K32 grid is partitioned into 4 x 4 x 4 macroblocks, each 8 x 8 x 8 cells or 16 Mpc/h per side.

For each block b calculate:

\[
D_b=\mathrm{MSE}_{baseline,b}-\mathrm{MSE}_{augmented,b}.
\]

Hierarchical bootstrap:

- 10,000 replicates;
- first sample the three held-out seeds with replacement;
- then sample the 64 macroblocks within each selected seed with replacement;
- bootstrap RNG seed = 20260928;
- report percentile 95% interval for mean D_b.

## 12. Deterministic spatial-shift controls

Seven controls shift C_sigmaE by half a K32 box along every nonzero combination of axes:

- (16,0,0);
- (0,16,0);
- (0,0,16);
- (16,16,0);
- (16,0,16);
- (0,16,16);
- (16,16,16).

For each control, the shifted C_sigmaE replaces the local C_sigmaE in both training and testing, while every baseline feature and target remains unshifted.

The estimator and all parameters remain unchanged.

## 13. N128 final holdout

Only after the complete N64 leave-one-seed-out analysis is generated, train baseline and augmented models on all three N64 seeds and evaluate once on untouched N128 seed 1968479875 projected to the identical K32 support.

The seven spatial-shift controls are repeated on the N128 holdout using models trained with the corresponding shifted N64 commutator fields.

N128 may not be used to tune features, model parameters, temporal spacing, or outcome definitions.

## 14. Primary ACCEPT rule

Classify PREG-MODAL-PA-1 as ACCEPT only if all of the following are true:

1. Delta_s > 0 for all three N64 held-out seeds using the inner temporal reconstruction;
2. the lower endpoint of the frozen 95% hierarchical bootstrap interval for mean D_b is > 0;
3. the mean observed N64 Delta_s is greater than the mean improvement from each of the seven shifted-C controls;
4. N128 holdout Delta > 0;
5. the observed N128 improvement is greater than every shifted-C N128 control improvement;
6. repeating the primary analysis with the outer temporal reconstruction does not reverse the sign of any of the three N64 Delta_s values or the N128 Delta;
7. no amplitude cut, eigengap cut, cell deletion, feature replacement, or model retuning beyond the exact mathematical undefined cases is required.

ACCEPT licenses only the claim ceiling in Section 18.

## 15. Primary REFUSE rule

Classify as REFUSE only if all of the following are true:

1. Delta_s <= 0 for all three N64 held-out seeds;
2. the upper endpoint of the frozen hierarchical 95% interval for mean D_b is <= 0;
3. N128 holdout Delta <= 0;
4. field validity and temporal reconstruction remain admissible, so the negative result cannot be attributed to a broken representation.

REFUSE means this relational predictor did not add predictive information under the frozen test. It does not refuse scalar, modal, Conglomerate/System, joint, or broader cosmological exploration.

## 16. NEED_MORE_INFO rule

Use NEED_MORE_INFO for every outcome that is neither ACCEPT nor REFUSE, including:

- mixed signs across N64 seeds;
- hierarchical interval crossing zero;
- N64 improvement but N128 non-replication;
- observed improvement not exceeding the deterministic shifted-C controls;
- temporal inner/outer reconstruction changing the conclusion;
- exact-zero/degeneracy behavior making the relational feature uninterpretable without a new threshold;
- actual output or resolution effects that cannot be separated under the frozen design.

A NEED_MORE_INFO result may motivate a new prospectively frozen experiment but may not be converted into ACCEPT by post hoc filtering.

## 17. Secondary reports that cannot change the primary outcome

Report, without promotion:

- G_rho prediction with the same baseline and augmented models;
- distribution of C_sigmaE;
- A_sigmaE distribution;
- E and sigma eigengaps;
- full-versus-scalar Weyl difference;
- vector and tensor Weyl sector amplitudes;
- spatial maps of ACCEPT-supporting and failure/outlier regions;
- root-cause classification of failure/outlier blocks.

Failures and outliers remain part of the evidence and must be investigated, while the majority distribution remains visible.

## 18. Claim ceiling if ACCEPT

The strongest permitted claim is:

> In the frozen gevolution LambdaCDM experiment from z=2 to z=1 on the qualified K32 physical band, the bounded local noncommutativity of native velocity shear and full electric Weyl provides reproducible out-of-sample information about subsequent Eulerian shear reorganization beyond current scalar state, the separate tensor spectra, and a simpler static tensor-alignment scalar, with replication on an untouched higher-resolution realization.

Not licensed:

- new dark matter or dark energy ontology;
- removal of standard LambdaCDM components;
- direct measurement of magnetic Weyl curvature;
- universal cosmological stability law;
- universal scalar inadequacy;
- halo or galaxy assembly claims;
- Lagrangian-history claims;
- a claim that all modal information is captured by C_sigmaE.

## 19. Exploration firewall

Whatever the outcome, the following remain open:

- scalar Function/Limit mapping;
- other modal relational observables;
- vector/tensor modal sectors;
- Conglomerate/System spatial organization;
- joint Scalar + Modal + Conglomerate meaning;
- additional architecture components;
- full P0-D novelty search.

## 20. Opening rule

No field from seeds 171802845, 351644392, 591375351, or 1968479875 may be inspected before this preregistration is committed.

After commit, mechanical implementation may proceed continuously. Any scientific change to Sections 1-19 after opening P1-M evidence requires a versioned amendment and cannot retroactively alter the v1 adjudication.
