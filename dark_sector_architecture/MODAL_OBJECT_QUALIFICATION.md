# Modal Object Qualification for Partial Cosmology Architecture

**Stage:** P0-Q representation qualification  
**Parent:** PARTIAL_ARCHITECTURE_PREREG_CANDIDATES.md  
**Status:** NATIVE MODAL BASIS IDENTIFIED; computational qualification pending

## Qualification question

What is the strongest native cosmological modal/vector object that can support the partial-architecture preregistrations without replacing domain physics with PCA, DMD, or another convenience decomposition?

## Candidate representations adjudicated

### 1. Arbitrary covariance/PCA modes
**Status:** REFUSED as primary native modal object.

Useful diagnostically, but the decomposition is estimator-defined rather than the native dynamical object. It may remain an exploratory proxy.

### 2. Dynamic-mode decomposition of simulation outputs
**Status:** REFUSED as primary native modal object.

Potentially useful P0-D diagnostic, but mode identity depends on observable/state choice, time window, rank truncation, and algorithm.

### 3. Linear Einstein-Boltzmann generator eigenmodes
**Status:** ADMITTED in their native linear/non-autonomous regime.

Strength:
- directly derived from the governing linear system;
- scale- and time-dependent eigenstructure is established.

Limit:
- not by itself a complete nonlinear late-time modal representation.

Use:
- baseline and transfer comparator, not the sole nonlinear modal object.

### 4. Tidal and velocity-shear eigenstructure
**Status:** ADMITTED for nonlinear structure formation.

Native objects:
- gravitational tidal tensor;
- velocity-deformation/shear tensor;
- ordered eigenvalues/eigenvectors.

Strength:
- directly encode principal contraction/expansion directions;
- standard cosmic-web and anisotropic-collapse tools;
- preserve information lost by density, divergence, or shear-norm scalars.

Limit:
- common cosmic-web threshold classifications can introduce a tunable threshold.

Rule:
- primary analysis uses continuous eigenvalues/eigenvectors/invariants;
- categorical web labels are secondary and require a prospectively frozen threshold if used.

### 5. Relativistic shear-Weyl eigenstructure
**Status:** PRIMARY NATIVE MODAL CANDIDATE.

For covariant scalar perturbations, literature identifies the electric Weyl tensor (E_{ij}) and shear (sigma_{ij}) as a minimal closed set of observable variables.

Related native sector structure:
- scalar/irrotational: (E_{ij}), (sigma_{ij});
- vector: vorticity plus shear;
- tensor/gravitational-wave: electric and magnetic Weyl tensors (E_{ij},H_{ij}).

Nonlinear relativistic Lagrangian work shows that:
- shear and electric Weyl/tidal fields evolve beyond linear order;
- magnetic Weyl structure is dynamically generated and carries nonlocal relativistic information.

## Primary modal representation

The primary late-time modal object will therefore be the **eigenstructure of the relativistic shear and Weyl/tidal tensors**, not an arbitrary spectral decomposition of the data matrix.

For a symmetric trace-free tensor (S_{ij}), retain:
- ordered eigenvalues (lambda_1,lambda_2,lambda_3);
- eigenvectors/eigenframe;
- degeneracy status;
- frame alignment with the relevant Weyl/tidal tensor;
- uncertainty and numerical conditioning.

Scalar reductions such as

[
sigma^2 = rac12sigma_{ij}sigma^{ij}
]

or a Weyl invariant retain only part of this information.

This creates a direct scalar-modal test:

[
{	ext{same scalar invariant}}

otRightarrow
{	ext{same eigenvalue spectrum/eigenframe}}.
]

Whether that lost modal information changes realized cosmological behavior becomes an empirical/confirmatory question rather than an assumption.

## Conglomerate bridge

The modal objects enter the conglomerate architecture through:
- spatial distribution of modal eigenvalues/eigenframes;
- alignments and misalignments;
- expansion variance;
- shear contribution to (Q_{mathcal D});
- averaged curvature;
- domain connectivity/topology;
- boundary or edge organization where separately qualified.

Thus the current reconstruction path becomes

[
	ext{local scalar invariants}
ightarrow
	ext{shear/Weyl modal eigenstructure}
ightarrow
	ext{spatial/domain conglomeration}
ightarrow
	ext{realized growth/collapse/expansion}.
]

Every arrow remains testable and may fail.

## Consequence for PREG-MODAL-PA-1

Replace the generic primary target "mode/eigenspace participation from any convenient generator" with:

**Primary target:** shear/Weyl/tidal eigenvalue spectrum, eigenframe, and their evolution/alignment.

**Linear comparator:** Einstein-Boltzmann generator modes.

**Weak-field computational representation:** tidal/velocity-shear eigenstructure and Poisson-gauge metric sectors from gevolution.

**Full-GR robustness representation:** covariant/3+1 shear and electric/magnetic Weyl variables from Einstein Toolkit or another qualified full-GR implementation.

PCA/DMD may be reported only as exploratory secondary diagnostics.

## Consequence for PREG-JOINT-PA-1

The strongest scalar-vs-modal design is now explicit.

Construct matched states/domains with comparable:
- density/background state;
- expansion scalar;
- shear scalar/norm where appropriate;

but differing:
- ordered shear/tidal eigenvalue spectrum;
- eigenframe geometry;
- shear-Weyl alignment;
- modal spatial organization.

Test whether the differing modal organization predicts different later growth, collapse, lensing, or expansion outcomes.

## Consequence for PREG-JOINT-PA-2

The inheritance candidate becomes:

> Does earlier shear/Weyl/tidal eigenstructure retain predictive information about later conglomerate curvature/backreaction/system organization beyond earlier scalar invariants alone?

This is a native cosmological Stability Inheritance test.

## Refusal rules

Refuse modal interpretation when:
- eigenvalues/eigenvectors are not numerically identifiable;
- a near-degeneracy makes eigenframe direction meaningless;
- the claimed modal effect is only a thresholded web-label artifact;
- gauge/observer choice changes the physical interpretation without an invariant/covariant restatement;
- the tensor is reconstructed from the endpoint in a way that creates leakage;
- the modal variables are algebraically reducible to the scalar comparator in the tested case.

## Need-more-info state

Use `INDETERMINATE_NEED_MORE_INFO` when:
- the native tensor can be reconstructed but gauge/covariant correspondence is not yet validated;
- eigenframe uncertainty is unresolved;
- simulation output lacks one required metric/kinematic field;
- correspondence between weak-field and full-GR tensor definitions has not been qualified.

## Next qualification action

Build a small known-truth tensor suite before cosmological production runs:

1. isotropic expansion: degenerate modal state;
2. one-axis collapse;
3. two-axis collapse;
4. three-axis collapse;
5. matched shear scalar with different eigenvalue spectra;
6. matched expansion/density with different eigenframes;
7. near-degenerate eigenvalue controls;
8. coordinate-rotation invariance;
9. gauge/representation correspondence cases where available.

No empirical threshold is frozen until this suite establishes numerical identifiability and tolerance.
