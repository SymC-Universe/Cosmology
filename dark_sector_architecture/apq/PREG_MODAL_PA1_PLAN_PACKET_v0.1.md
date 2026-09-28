# PREG-MODAL-PA-1 APQ-3 PLAN PACKET v0.1

**Project:** Cosmic Stability Architecture
**Stage:** pre-P1 residual freeze / APQ-3
**Status:** PLAN_DRAFT, NOT QUALIFIED, NOT FROZEN FOR P1
**Date:** 2026-09-27
**Parent:** PARTIAL_ARCHITECTURE_PREREG_CANDIDATES.md
**Representation qualification:** Development 011, NATIVE_FIXED_BAND_QUALIFIED_P0Q

## 1. Native scientific question

After subtracting established density, tidal-anisotropy, T-web/V-web, shear, electric-Weyl, and nonlinear tide-shear results, is there a genuinely unresolved standalone modal question that can be tested prospectively, or should the qualified modal representation be used only as an input to Conglomerate/System and joint Scalar + Modal + Conglomerate tests?

## 2. Prior-art subtraction already established

The following are not available as new standalone claims:

- tidal anisotropy/eigenstructure adds information beyond scalar overdensity in halo assembly/environment studies;
- velocity-shear eigenvalues/eigenvectors organize nonlinear cosmic-web structure and halo alignments;
- T-web and V-web coincide in the linear regime and depart in the nonlinear regime;
- tidal and velocity-shear tensors are nonlinearly coupled;
- the electric Weyl tensor reduces to the Newtonian tidal tensor in the Newtonian/weak-field limit;
- shear and electric Weyl are coupled by standard covariant propagation equations;
- in irrotational purely-electric/silent limits, shear and electric Weyl share an eigenframe and their commutator vanishes;
- generic nonlinear evolution is nonlocal and cannot be promoted to a new SymC mechanism merely because a local/silent approximation fails.

Therefore the candidate cannot be 'modes matter', 'tidal structure beats density', 'Weyl is extra relativistic information', 'T-web differs from V-web', or 'shear and Weyl interact'.

## 3. Smallest live residual candidate

Candidate residual:

> In a qualified late-time weak-field relativistic large-scale-structure representation, the joint relational state of the native electric-Weyl tensor E_ij and velocity-shear tensor sigma_ij contains reproducible information about subsequent modal reorganization that is not contained in scalar state variables or in the marginal spectra/invariants of E_ij and sigma_ij considered separately.

This candidate is intentionally relational. It does not claim a new degree of freedom, new substance, new force, or specifically relativistic effect.

## 4. Material alternatives

- H0 / EQUIVALENT: the joint relation adds no information once scalar state and the two tensors' marginal spectra are included.
- H1 / MODAL_ADDS: a prospectively frozen joint relational descriptor improves untouched prediction of later modal state beyond the strongest marginal-tensor comparator.
- H2 / STANDARD_DYNAMICS_ONLY: an effect exists but is fully explained by established Newtonian/cosmic-web dynamics and therefore does not support a distinct SymC modal claim.
- H3 / TOOL_ONLY: a relational descriptor is reproducible and useful as a measurement/compression tool but does not support a standalone physical S-class claim.
- H4 / NOT_ACTIVATED: prior art and native equations leave no scientifically worthwhile standalone modal residual; modal objects proceed only as qualified inputs to Conglomerate and joint tests.
- REFUSED: the relational state is non-identifiable, degenerate, representation-unstable, or algebraically/circularly tied to the proposed endpoint.

## 5. Current evidence class and claim ceiling

Available evidence:
- P0-N/A0 literature conglomeration;
- P0-Q native tensor/eigensystem known truth;
- P0-Q real gevolution field qualification;
- P0-Q native LATfield2 operator qualification;
- P0-Q N32/N64/N128 fixed-band convergence;
- already-viewed early-epoch pilot results.

Current ceiling:
- modal representation is qualified for measurement;
- no standalone modal physical P1 claim is active;
- no chi or Chi formula is licensed;
- no dark-matter or dark-energy replacement claim is permitted.

## 6. Candidate native relational observables

Primary candidate invariant:

\[
\kappa_{E\sigma}
=
\frac{\|[E,\sigma]\|_F}
{\|E\|_F\,\|\sigma\|_F},
\]

evaluated only where both tensor norms are numerically identifiable under prospectively frozen qualification rules.

Supporting relational observables:
- absolute eigenframe alignment matrix |e_i^E dot e_j^sigma|;
- ordered principal-angle/eigenframe summary where eigengaps permit directional interpretation;
- mixed rotational invariants such as tr(E sigma), tr(E^2 sigma), and tr(E sigma^2) only if redundancy analysis shows they add non-duplicative information;
- marginal E and sigma eigenvalues/invariants are comparators, not relational features.

Important theoretical caveat:
`kappa_Esigma = 0` is already linked to simultaneous diagonalization/aligned silent limits. Nonzero kappa must not be interpreted as a new degree of freedom or as proof of relativistic physics.

## 7. Strongest comparator family

The comparator must be stronger than density-only or scalar-only baselines.

Minimum comparator content:
- density contrast / matter state;
- expansion or velocity-divergence scalar;
- scalar shear norm;
- complete marginal ordered eigenvalue spectra or equivalent rotational invariants of E and sigma separately;
- standard tidal-anisotropy information;
- T-web/V-web class or equivalent eigenvalue-sign information if not redundant with the spectra;
- redshift and fixed cosmological parameters.

A relational claim can receive ADDS only beyond this comparator.

## 8. Candidate decisive endpoint

The candidate endpoint is **later modal state**, not halo mass, galaxy property, lensing, backreaction, or other Conglomerate/System behavior.

Candidate later-modal endpoints:
- later ordered sigma eigenvalue spectrum;
- later ordered E eigenvalue spectrum;
- later E-sigma eigenframe relation / kappa_Esigma;
- a prespecified multivariate modal-state distance built without later outcomes.

The endpoint must be tied to the same material/comoving region or a defensible domain-tracking construction. A fixed Eulerian-cell comparison is not automatically admissible because advection can mimic reorganization.

## 9. Candidate P1-M data route if the residual survives APQ

Untouched evidence would be generated only after final plan freeze.

Candidate system:
- gevolution, canonical qualified CPU stack;
- N = 128;
- box size candidate 128 Mpc/h;
- multiple new deterministic seeds generated from the final preregistration file hash rather than hand selected;
- late-time outputs sufficient to define a pre-outcome state and later modal endpoint;
- no pilot or qualification seed may count as confirmation.

Exact redshift windows, spatial/domain tracking, physical band, and number of seeds are not yet frozen in v0.1 because they are APQ attack targets.

## 10. Candidate estimator architecture

Primary comparison:
- baseline model B0 uses scalar state + marginal E and sigma information;
- relational model B1 = B0 + frozen joint E-sigma relational descriptor family;
- training and evaluation split by simulation realization/volume, never random cells from the same realization;
- outcome metrics must be out-of-sample and prespecified;
- spatial autocorrelation requires block/volume-level uncertainty rather than treating cells as independent samples.

Preferred estimator family:
- low-flexibility regularized regression or another interpretable nested model where the incremental contribution of relational features is identifiable;
- a flexible nonlinear model may be a sensitivity analysis, not the sole primary evidence.

No numerical effect-size threshold is invented at this stage.

## 11. Candidate outcome architecture

ACCEPT / MODAL_ADDS only if:
- the relational feature family is prospectively frozen and identifiable;
- B1 improves untouched later-modal prediction over B0 across held-out realizations;
- the improvement survives uncertainty, resolution, and allowed representation checks;
- the result is not explained by leakage, advection mismatch, or a weaker omitted standard comparator;
- the result is not merely a restatement of a standard propagation identity.

EQUIVALENT if:
- B1 does not add reproducible held-out information beyond B0 within the declared uncertainty/equivalence logic.

SUBTRACTS if:
- B1 reproducibly worsens held-out performance relative to B0.

NEED_MORE_INFO if:
- relational variables are measurable but sample variance, tracking uncertainty, degeneracy, or finite volume prevents adjudication.

REFUSED if:
- modal directions are non-identifiable under eigengap/representation checks;
- E-sigma relation is algebraically determined by variables already in B0 for the tested regime;
- endpoint construction leaks future information;
- region tracking cannot distinguish physical reorganization from transport;
- the result requires post-outcome filtering, thresholding, or comparator deletion.

NOT_ACTIVATED if:
- APQ/P0-N concludes that the candidate residual is already established, tautological under the native equations, scientifically uninteresting as a standalone claim, or inseparable from the later Conglomerate/joint question.

## 12. Dependency structure

Foundational dependencies:
1. novelty survives prior-art subtraction;
2. relational observable is not a disguised standard scalar/tidal-anisotropy quantity;
3. endpoint is not tautologically linked to the relational feature by the same algebra used to construct it;
4. region/domain tracking is physically defensible;
5. strongest standard comparator is included;
6. untouched realization-level independence is preserved.

If 1-3 fail, standalone PREG-MODAL-PA-1 does not activate.
If 4-6 fail but are repairable, PLAN_HOLD / NEED_MORE_INFO.
Conglomerate/System and joint branches remain independently open regardless.

## 13. APQ-3 review coverage required

Isolated review routes must cover:
- novelty/prior-art attack;
- covariant GR/domain-theory attack;
- method/statistics/leakage attack;
- standard cosmic-web/alternative-model attack;
- falsification/refusal attack;
- reproducibility and untouched-evidence attack.

## 14. APQ bounded stopping rule

APQ closes only when:
- no unresolved BLOCKER remains;
- every MATERIAL objection is resolved by evidence, a discriminating test, claim limitation, or explicit hold;
- the plan retains genuine EQUIVALENT, SUBTRACTS, REFUSED, NEED_MORE_INFO, and NOT_ACTIVATED paths;
- untouched P1 outcomes remain unexposed;
- further review produces no new material dependency.

## 15. Exploration firewall

No disposition of PREG-MODAL-PA-1 may close:
- modal P0-D exploration;
- Conglomerate/System exploration;
- joint Scalar + Modal + Conglomerate investigation;
- Stability Inheritance investigation;
- additional architecture-component search.

A standalone modal refusal is evidence about that claim, not about the entire architecture program.
