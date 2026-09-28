# Late-Time Band-L Material Relational Development APQ-2 Plan Packet v0.1

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q development design
**APQ level:** APQ-2 SUBSTANTIAL
**Status:** PLAN_DRAFT BEFORE REAL MATERIAL E-SIGMA OUTCOME EXPOSURE
**Date:** 2026-09-27
**Parent APQ:** PREG_MODAL_PA1_APQ3_PLAN_PACKET.md / PREG_MODAL_PA1_APQ3_ADJUDICATION.md
**P1 status:** CLOSED

## 1. Purpose

Run a development-only discriminating test of whether the qualified relation between material-patch electric-Weyl and velocity-shear tensors contains prospective information about later modal shape reorganization beyond a strong scalar + marginal-tensor baseline.

This is not a test of new physics, dark-matter replacement, dark-energy replacement, or a new relativistic degree of freedom.

## 2. Frozen development evidence class

- gevolution/LATfield2 qualified weak-field relativistic representation;
- seed 424242 only;
- box size 64 Mpc/h;
- N64 primary development grid;
- all outcomes are P0-Q development evidence and are permanently ineligible as untouched P1 confirmation;
- no P1 seed or external observational holdout is opened.

## 3. Frozen temporal window

Reference state: requested z = 2, central scale factor a = 1/3.

Primary later endpoint: requested z = 1, central scale factor a = 1/2.

Secondary continuation: requested z = 0.5, central scale factor a = 2/3.

These are inherited from Development 014, where Band L remains the most robust velocity-shear regime through this interval.

Patch membership is frozen from the central z~2 particle positions and follows those particle IDs at z~1 and z~0.5.

## 4. Frozen temporal reconstruction around each endpoint

For each central scale factor a_c in {1/3, 1/2, 2/3}, request five snapshots at

\[
a_c(1-0.005),\quad
a_c(1-0.0025),\quad
a_c,\quad
a_c(1+0.0025),\quad
a_c(1+0.005).
\]

Use the actual logged conformal times and the already-qualified arbitrary-node inner/outer temporal derivative machinery.

Time-step limit: 0.0005, matching the previously qualified full-Weyl temporal workflow and chosen to keep neighboring requested outputs on distinct cycles.

## 5. Frozen modal representation order

At each central epoch:
1. reconstruct native full electric-Weyl component fields with the qualified LATfield2 operators and temporal derivatives;
2. vertex-co-locate every native E sector before local matrix interpretation;
3. compute corrected centered native velocity shear sigma and velocity divergence theta;
4. apply the same Band-L Fourier projection to vertex-centered E, sigma, and theta;
5. interpolate the filtered tensor/scalar components to the central-epoch particle positions;
6. aggregate samples using the z~2 frozen particle-ID patch membership;
7. compute patch eigensystems only after patch tensor aggregation.

Primary band:

\[
0<|\mathbf n|<4.
\]

No higher-k band may replace Band L after outcome inspection.

## 6. Frozen material scale family

Primary patch grid:

\[
8\times8\times8
\]

giving 8 Mpc/h reference cells.

Justification: the shortest retained Band-L wavelength in the 64 Mpc/h box is approximately 16 Mpc/h, so 8 Mpc/h patch spacing is the natural Nyquist sampling scale for the frozen band.

Predeclared scale sensitivities:
- coarse 4x4x4 patches, 16 Mpc/h;
- fine 16x16x16 patches, 4 Mpc/h.

Only the 8x8x8 analysis controls the primary development disposition. The sensitivity scales cannot rescue or overturn the primary result.

## 7. Frozen baseline patch variables at z~2

For every valid primary patch, B0 contains:
- reference equal-volume particle count contrast delta_N = N_patch / mean(N_patch) - 1;
- Band-L material-mass-weighted velocity divergence theta;
- E Frobenius norm;
- sigma Frobenius norm;
- the first two ordered E eigenvalues normalized by ||E||_F;
- the first two ordered sigma eigenvalues normalized by ||sigma||_F.

Because E and sigma are trace-free, norm plus two ordered normalized eigenvalues contains the complete marginal eigenspectrum up to numerical precision. Tidal-anisotropy and web-sign information are therefore algebraically contained in the marginal comparator rather than omitted as a weak baseline.

## 8. Frozen relational feature set

The native relational object remains the qualified full E-sigma relation.

B1 adds to B0:
- all 9 entries of the absolute ordered eigenframe overlap matrix |(e_i^E)^T e_j^sigma|;
- normalized commutator Frobenius ||[E,sigma]||_F / (||E||_F ||sigma||_F).

The 10 relational features are added as one block. No individual relational feature may be selected or dropped based on development performance.

Patch relation features are refused when either tensor has zero norm or when the existing exact-degeneracy semantics do not license ordered eigen-directions. Refused patch IDs are removed from both B0 and B1 for paired comparison and their count is reported.

No empirical near-degeneracy cutoff is introduced here.

## 9. Frozen primary endpoint

The primary endpoint is the z~2 -> z~1 change in **marginal modal shape**, not the later E-sigma relation itself.

For each tensor T in {E,sigma}, define its ordered normalized eigenvalue shape

\[
s_T=(\lambda_1/||T||_F,\lambda_2/||T||_F).
\]

The four-component primary target is

\[
Y_{2\to1}=
[s_E(z\sim1)-s_E(z\sim2),\;
s_\sigma(z\sim1)-s_\sigma(z\sim2)].
\]

This avoids making persistence of the relational feature itself the primary target and asks whether baseline E-sigma organization predicts subsequent marginal modal reorganization beyond baseline marginals.

Secondary continuation target:

\[
Y_{2\to0.5}
\]

defined identically. It is descriptive/sensitivity evidence and cannot rescue the primary z~1 result.

## 10. Frozen predictor and validation architecture

Primary models are nested multi-output linear least-squares predictors with an intercept:
- B0 = baseline features;
- B1 = B0 + the entire frozen 10-feature relational block.

Within each training fold, nonconstant columns are standardized using training-fold means and standard deviations only. A column that is exactly constant within training data is represented as zero after centering and retained in provenance rather than outcome-selected.

No nonlinear learner is primary.

## 11. Frozen spatial validation

For the primary 8x8x8 patch grid, reference patches are grouped into eight fixed 32 Mpc/h octants (2x2x2 spatial blocks) using their z~2 reference location.

Use leave-one-octant-out cross-validation:
- train on 7 octants;
- predict the held-out octant;
- concatenate predictions from all 8 held-out octants.

Folds are fixed by reference location and are not shuffled after outcome exposure.

Particle-level or random-patch train/test splitting is prohibited.

## 12. Frozen primary performance statistic

For concatenated held-out predictions define total squared error over the four target components.

\[
\Delta_{rel}
=
\frac{SSE_{B0}-SSE_{B1}}{SSE_{B0}}.
\]

Positive Delta_rel means the relational block improves held-out prediction.

## 13. Frozen spatial-shift null

To test whether local relational pairing matters beyond the marginal spatial fields, construct the full periodic shift null on the 8x8x8 reference-patch lattice.

For every nonzero integer shift

\[
(d_x,d_y,d_z)\in\{0,...,7\}^3\setminus\{(0,0,0)\},
\]

circularly shift the entire 10-feature relational block together relative to B0 and the target, then repeat the identical eight-fold validation.

This yields 511 nonzero spatial-shift null values of Delta_rel while preserving the relational block's marginal distribution and periodic spatial organization.

Primary development signal threshold:
- `DEVELOPMENT_SIGNAL_PRESENT` only if observed Delta_rel > 0 and exceeds the empirical 95th percentile of the 511-shift null;
- `DEVELOPMENT_SUBTRACTS` if observed Delta_rel < 0 and lies below the empirical 5th percentile of the null;
- otherwise `DEVELOPMENT_EQUIVALENT_OR_UNRESOLVED`.

This is a development-screening rule, not a P1 significance claim.

## 14. Additional diagnostics

Always report:
- foldwise Delta_rel;
- target-component SSEs;
- B0/B1 design ranks and condition numbers;
- relation-refused patch count;
- patch particle-count distribution;
- z~2, z~1, z~0.5 actual epoch metadata;
- primary 8x8x8 result;
- predeclared 4x4x4 and 16x16x16 directional sensitivities without reclassification authority.

## 15. Refusal and need-more-info rules

`REFUSED` if:
- stable particle-ID membership fails;
- Band-L E or sigma cannot be reconstructed under qualified operators;
- material-patch interpolation/aggregation semantics fail;
- any primary fold has nonfinite predictors/targets;
- the target is constructed from information unavailable at the declared epoch;
- the analysis requires changing the relation feature block, patch family, band, folds, or target after outcome exposure.

`NEED_MORE_INFO` if:
- exact degeneracy/norm refusal removes enough patches that a primary fold cannot fit both nested models;
- the B0 or B1 design is numerically nonidentifiable in a way that prevents stable prediction;
- temporal reconstruction uncertainty becomes comparable to the modal changes being modeled;
- the z~0.5 continuation qualitatively contradicts z~1 in a way requiring a new discriminating design;
- primary scale is valid but coarse/fine sensitivity exposes an unresolved scale dependence that changes interpretation.

## 16. Outcome consequence

DEVELOPMENT_SIGNAL_PRESENT:
- does not activate P1;
- justifies a Plan Delta / APQ-3 final preregistration design using untouched realizations.

DEVELOPMENT_EQUIVALENT_OR_UNRESOLVED:
- standalone modal predictive claim is not promoted from this design;
- investigate whether the result is true equivalence or underpowered/scale-limited without tuning this dataset into confirmation;
- qualified modal variables remain available to Conglomerate and joint tests.

DEVELOPMENT_SUBTRACTS:
- treat the relational block as harmful for this reduced predictor in the tested regime;
- do not promote the standalone modal predictive claim from this design.

REFUSED:
- repair only the failed representation/method dependency;
- do not reinterpret as cosmological evidence.

## 17. APQ attack targets before execution

Attack at minimum:
- whether 8 Mpc/h is genuinely licensed by Band-L sampling rather than convenience;
- whether material patch means erase the relational information being tested;
- whether normalized eigenshape change is a meaningful nonleaky modal endpoint;
- whether full marginal spectra really subsume the strongest standard tidal baseline;
- whether 2x2x2 octant folds are sufficiently independent for a development screen;
- whether the full 511-shift null is valid under periodic long-wavelength fields;
- whether OLS with the frozen relation block creates unstable multicollinearity;
- whether temporal derivative output density is sufficient at z~2,1,0.5;
- whether any standard-dynamics identity makes the added-value test tautological.

## 18. Bounded APQ stopping rule

Execution may begin only when no unresolved BLOCKER remains and every MATERIAL objection is either repaired prospectively, converted into an explicit limitation/sensitivity, or assigned NEED_MORE_INFO semantics.

## 19. Exploration firewall

No outcome closes:
- modal P0-D exploration;
- Conglomerate/System;
- joint Scalar + Modal + Conglomerate;
- Stability Inheritance;
- additional architecture-component search.
