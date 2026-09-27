# WORKING_INVESTIGATION

**Project:** Cosmic Stability Architecture  
**Branch:** `dark-sector-stability-architecture`  
**Current stage:** P0-Q modal representation/convergence qualification; gevolution real-field smoke and Q-R2/Q-R3 ladders complete; full electric-Weyl representation gate active  
**Current scientific state:** The bounded nonperturbative/additional-architecture pass is complete. The full no-dark-substance route is UNSUPPORTED_AT_CURRENT_STAGE under the frozen literature rules, not falsified. The active branch is now the partial architecture; the full route remains open only in P0-D for genuinely new future candidates.

## Frozen objects

- **PREG-LIT-COSMO-v1.0** frozen at GitHub commit `383747c6a713e6a518b913635b2ace423fafff0d`.
- Literature adjudication semantics are frozen for the current controlled P0-Q pass.
- P0-D exploration remains open by rule and is not bounded by refusal outcomes.
- No P1 claim is activated yet. PREG-SCALAR-PA-0 is explicitly NOT_ACTIVATED; modal/conglomerate/joint candidates are defined but remain unfrozen pending qualification.

## Frozen hypothesis scope

The investigation tests whether phenomena conventionally assigned to dark matter and dark energy can arise, in whole or in part, from the native cosmological stability architecture without introducing a dark fluid, hidden medium, new force, or new dark substance.

No outcome is presumed.

Scalar, Vector/Modal, and Conglomerate/System are starting representations only. They do not exhaust (Chi), and additional architecture components remain open to discovery.

## Current Stage A literature state

### Admitted foundations
- dark-sector ontology neutrality / dark degeneracy;
- standard primordial and Einstein-Boltzmann modal organization;
- matrix-valued primordial mode correlation structure;
- averaged-GR coupling among expansion variance, shear, backreaction, and curvature;
- two-way multiscale coupling in several GR formalisms;
- formal history/memory under coarse graining;
- limited late-time DM-like and DE-like functional analogies.

### Admitted counterevidence / limits
- known radiation-era and perturbative backreaction terms are too small or have the wrong scaling to supply the standard pre-recombination pressureless gravitational function;
- large backreaction can be gauge/slicing sensitive and is restricted by strong adversarial frameworks;
- apparent acceleration alone is insufficient if observed growth suppression fails;
- ordinary linear GR does not contain a hidden independent scalar gravitational propagating mode.

## Scientific developments to date

1. **Early-universe constraint:** known late structure-generated backreaction does not supply the pre-recombination CDM-like function.
2. **Primordial carrier:** conserved curvature variables provide a real scalar inheritance carrier but not an independent gravitational source.
3. **Three-layer inheritance:** primordial organization is scalar, modal, and conglomerate/correlation based; (zeta/mathcal R) is one projection, not the whole architecture.
4. **Direct modal narrowing:** ordinary linear GR does not supply an overlooked scalar replacement mode; nonlinear scalar/vector/tensor and Weyl couplings are real but have not demonstrated the required function.
5. **Known conglomerate insufficiency:** nonlinear generated modes, covariant correlation sectors, averaging corrections, and memory kernels are real but no admitted construction demonstrates the complete pre-recombination CDM-like function.
6. **Bounded full-route narrowing:** nonlocal, geon, edge-mode, field-self-interaction, exact-inhomogeneous, and additional-geometry candidates were examined. None satisfies the frozen full CMB-to-late standard-GR burden. The full route is therefore UNSUPPORTED_AT_CURRENT_STAGE, while the partial architecture becomes the active research branch.
7. **Native modal basis identified:** relativistic shear/Weyl tensor eigenstructure is the primary modal representation; scalar invariants, modal eigenstructure, and conglomerate spatial organization can now be tested separately and jointly.

Detailed stop records: `WORKING_SCIENTIFIC_DEVELOPMENTS.md`.

## Current claim ceiling

Supported:
- inherited primordial organization exists;
- modal and conglomerate transfer structure exists;
- nonlinear and multiscale GR coupling exists;
- late structure/curvature feedback has legitimate literature precedents.

Not supported:
- complete dark-matter replacement;
- complete dark-energy replacement;
- one demonstrated architecture spanning recombination through late acceleration;
- a direct elementary GR mode replacing the pre-recombination CDM function;
- a licensed cosmological lower-case (chi) beyond previously published/model-specific scalar constructions.

Stage-A disposition:
- FULL_NO_DARK_SUBSTANCE: UNSUPPORTED_AT_CURRENT_STAGE;
- PARTIAL_ARCHITECTURE: ACTIVE;
- FULL_ROUTE_P0D_EXPLORATION: OPEN.

## Active exploration branches

- EXP-003 nonlinear collective gravitational mode;
- EXP-004 Weyl/shear/tidal modal channel;
- EXP-005 additional architecture component beyond S/M/C;
- EXP-006 Green-Wald applicability boundary;
- EXP-007 gauge/slicing invariant architecture;
- EXP-008 partial architecture branch;
- EXP-009 no-CDM primordial modal architecture;
- EXP-010 conglomerate source emergence after direct modal refusal;
- EXP-011 nonlinear Weyl/tidal inheritance;
- EXP-012 additional architecture component search.

See `LITERATURE_EXPLORATION_QUEUE.md`.

## Active holds / promotion debt

- Any new component proposed because of the early-universe or direct-modal failures is post-result and cannot retroactively rescue those failures.
- No literature-derived residual may be called confirmatory.
- PREG-S/M/C/J activation is held until controlled literature adjudication identifies the irreducible residual claim set.
- Full-system claims are held until scalar/modal/conglomerate/joint gates are separately defined and passed where applicable.

## Latest scientific development

**Development 008: fixed-band convergence separates the scalar-Weyl and shear qualification states.**

The gevolution infrastructure gate is now passed with the canonical gevolution 1.3 / LATfield2 v1.1 CPU stack and the canonical historical `sc1_crystal.dat` particle template. Durable real-field HDF5 outputs and modal extraction summaries exist.

A synchronized high-resolution ladder at (N=32,64,128), common seed, common box, common epoch (z\simeq98.9976), and fixed physical Fourier support shows a representation-dependent convergence pattern:

- (64\rightarrow128) potential RMS error / reference RMS: (5.93\times10^{-4});
- scalar-Weyl-shape median relative tensor-operator error: (1.48\times10^{-2}), with q95 (3.15\times10^{-2});
- scalar-Weyl eigenframe median diagonal alignments: (0.999978, 0.999952, 0.999979);
- scalar-Weyl median tensor-error/eigengap direction diagnostics: approximately (0.0171) and (0.0170);
- velocity-shear median relative tensor-operator error: (0.174), with q95 (0.351);
- velocity-shear eigenframe median diagonal alignments: (0.9983, 0.9961, 0.9983), but q05 remains approximately (0.970, 0.931, 0.967);
- velocity-shear median tensor-error/eigengap diagnostics remain approximately (0.201).

The gevolution scalar slip correction is tiny at this early development epoch:
- `chi_gev_rms / phi_rms` is approximately (6.84\times10^{-6}) at (N=128);
- replacing `phi` by the scalar Weyl/lensing potential changes the scalar-Weyl tensor by a median relative operator amount of approximately (1.41\times10^{-6});
- corresponding eigenframes are essentially unchanged at this epoch.

Interpretation:
- scalar potential convergence does not license a modal convergence claim;
- the scalar-Weyl shape is numerically much better conditioned on the frozen high-resolution physical band than the velocity-shear modal object;
- shear/modal convergence is improving materially with resolution but is not collapsed into a binary PASS threshold;
- the scalar-slip result is epoch- and scalar-sector-specific and does not license calling the current object the full electric Weyl tensor;
- the full vector/tensor (B_i,h_{ij}) electric-Weyl contribution and temporal derivative terms remain an open representation gate.

This is a scientific-development stop because the numerical qualification state differs materially by representation. It strengthens, rather than closes, the requirement to investigate scalar, modal, conglomerate, and their joint meaning separately.

Detailed stop record: `WORKING_SCIENTIFIC_DEVELOPMENTS.md`.

## Next exact action

Continue the **modal representation gate**, not another scalar-only ladder:

1. freeze the exact first-order convention map between gevolution `Phi`, `chi_gev = Phi-Psi`, `B_i`, `h_ij` and the covariant electric/magnetic Weyl variables;
2. build a three-snapshot matched-epoch pilot so vector/tensor temporal derivatives can be reconstructed rather than assumed;
3. qualify centered first- and second-time derivatives at two temporal spacings;
4. reconstruct scalar + vector + tensor electric-Weyl contributions under the frozen convention, preserving scalar-only and full objects separately;
5. quantify whether (B_i) and (h_{ij}) materially alter eigenvalues/eigenframes relative to the scalar-Weyl shape;
6. keep the velocity-shear channel separate and continue its convergence accounting rather than using scalar-Weyl convergence as a proxy;
7. only after the electric-Weyl representation gate and shear uncertainty route are qualified should `PREG-MODAL-PA-1` be considered for activation;
8. after modal qualification, return to `PREG-CONGLOMERATE-PA-1` and `PREG-JOINT-PA-1/2` so the investigation does not collapse into a scalar-only result.

No universal numerical threshold is frozen by Development 008.

## Resume pointers

- `PREG_LIT_COSMO_V1_FREEZE.md`
- `COSMOLOGY_PREREGISTRATION_ARCHITECTURE.md`
- `LITERATURE_ADJUDICATION_PROTOCOL.md`
- `LITERATURE_ADJUDICATION_MATRIX.md`
- `LITERATURE_EXPLORATION_QUEUE.md`
- `WORKING_SCIENTIFIC_DEVELOPMENTS.md`
- `STAGE_A_PRIMORDIAL_MODAL_CONGLOMERATE_SYNTHESIS.md`


## Active hypothesis branch after Stage A narrowing

**PARTIAL_ARCHITECTURE**

Working question:

> Which late-time phenomena conventionally assigned to dark matter and dark energy are actually generated, reorganized, or conditioned by GR-native multiscale structure, modal organization, geometry, feedback, edge/boundary effects, and inheritance, and what does the scalar-modal-conglomerate joint architecture explain beyond the strongest native baseline?

This does not presume that the early dark gravitational component is architectural or absent.


## Partial-architecture preregistration candidates

- `PREG-SCALAR-PA-0`: NOT_ACTIVATED.
- `PREG-MODAL-PA-1`: CANDIDATE, native shear/Weyl/tidal eigenstructure.
- `PREG-CONGLOMERATE-PA-1`: CANDIDATE, single-rule late-time dual-function architecture.
- `PREG-JOINT-PA-1`: CANDIDATE, scalar insufficiency conditioned by modal/conglomerate organization.
- `PREG-JOINT-PA-2`: CANDIDATE, modal-to-conglomerate Stability Inheritance.

See `PARTIAL_ARCHITECTURE_PREREG_CANDIDATES.md`.


## Current modal P0-Q implementation commits

- tensor extractor: `11b815a202cb67019ae52c920fb80506c49d7301`
- known-truth tests: `aa2f20cb600f4688b5d8fb6400bc5dad16bfc18b`
- machine-readable runner: `ca7003616b2d96fc1c9d0b4ee8fc12d6aad8b3ae`
- known-truth workflow: `42c06d232259bf3166df29feabbdf8c5c6e8cbdd`
- independent validation checkpoint: `3974ad5c1fb453db10d57a6a3c7e6b4cd10b0c9f`
- frozen gevolution pilot settings: `721ef700df28d5f778bdaf2d05759ef1aef05230`
- pinned gevolution pilot workflow: `4b3902c6cb327a6743aace71289a3e2de7e05f98`


## Durable modal qualification outputs

- `qualification/results/modal_known_truth_report.json`: GENERATED / durable.
- `qualification/results/weak_field_known_truth_report.json`: GENERATED / durable.
- latest integrated modal qualification CI observed PASS: run `36350444568`.

The modal qualification workflow now persists generated JSON reports back to the branch.

## gevolution infrastructure chain

Canonical CPU source pairing:
- gevolution `0cca42e51a824002ae4fb602cbd79d671e8ffe60`;
- UZH LATfield2 v1.1 `2d8c737ab6adc965a1d2718c209f5085af27b09c`.

Preserved failure classes are recorded in `GEVOLUTION_PILOT_FAILURE_LEDGER.md`.

Validated mechanical milestones:
- canonical CPU backend fetches and compiles;
- deterministic Gadget-2 template generator validates its binary structure;
- 2x2 MPI layout is required for the smoke and uses hosted-runner oversubscription;
- fail-closed pipeline handling is active;
- LATfield2 HDF5 loader is qualified against the exact array-datatype schema;
- weak-field tidal/shear transform and end-to-end synthetic extraction are qualified;
- modal convergence utilities and tests are committed.

Current active smoke:
- run `36350573345`;
- head `49a4a9648a51cf3d9c931675d000097f8fe5b2e4`;
- template tiling changed to 8 so the 8^3 mesh receives 512 homogeneous template particles;
- this repair follows run `36350469640`, whose sparse 8-particle IC produced an invalid cycle-0 NaN and was classified INVALID_INPUT rather than scientific evidence.

Pending durable gevolution outputs:
- `qualification/results/gevolution_modal_pilot_metadata.json`;
- `qualification/results/gevolution_modal_pilot_manifest.txt`;
- `qualification/results/gevolution_modal_extraction_summary.json`.


## Durable convergence outputs added after Development 007

- `qualification/results/gevolution_modal_extraction_summary.json`
- `qualification/results/q_r2_n8_n16_resolution_pair.json`
- `qualification/results/q_r2_n16_n32_resolution_pair.json`
- `qualification/results/q_r2_n32_n64_resolution_pair.json`
- `qualification/results/q_r2_highres_n32_n64.json`
- `qualification/results/q_r2_highres_n64_n128.json`
- `qualification/results/q_r3_fixed_band_n32_n64_n128.json`
- `qualification/results/highres_scalar_weyl_slip_n32.json`
- `qualification/results/highres_scalar_weyl_slip_n64.json`
- `qualification/results/highres_scalar_weyl_slip_n128.json`

Latest observed high-resolution scalar-Weyl ladder workflow: run `36354573737`, PASS.
Latest integrated modal known-truth workflow: run `36354573739`, PASS.
