# SUPPLEMENTAL RECOVERY LITERATURE SUBTRACTION - PRESERVED, NON-AUTHORITATIVE

This file was created during timeout recovery. Its prior-art subtraction is retained as useful Stage A evidence, but it does not override the authoritative APQ-3 / APQ-2 material-lineage design.

---
# PREG-MODAL-PA-1 Stage A Residual and Literature Adjudication

**Project:** Cosmic Stability Architecture  
**Stage:** Stage A prior-art subtraction before P1-M activation  
**Status:** RESIDUAL SURVIVES CURRENT ADMITTED CORPUS / NOT A CLAIM OF EXHAUSTIVE NOVELTY  
**Date:** 2026-09-28

## Frozen question entering the literature gate

After the modal representation itself qualified at P0-Q, the broad candidate was:

> Does native cosmological modal structure add predictive information beyond scalar state?

That question is too broad and is refused as a novel residual.

## Literature-native known world

### Electric Weyl is not automatically a new relativistic observable

[Ehl09] shows that the electric part of the Weyl tensor has a well-defined Newtonian limit corresponding to the tidal field. A claim that electric-Weyl eigenstructure is generically extra relativistic information beyond the standard tidal tensor is therefore refused.

### Tidal anisotropy already adds information beyond density

[Ram19], [Mus17], and [Bor16] show that anisotropic tidal environment carries information about halo assembly, accretion, formation, and clustering beyond mass or local scalar density.

Therefore the following candidate is refused as non-novel:

> tensor/tidal anisotropy predicts structure evolution beyond density.

### Modal/eigenvector evolution is already established territory

[Lib13] studies the redshift and scale evolution of velocity-shear eigenvectors and vorticity. Tidal-torque and cosmic-web studies such as [Por01] also use tensor alignment/misalignment to understand later evolution.

Therefore the following candidate is refused as too broad:

> eigenvectors or their time evolution matter.

### Static cosmic-web classifier disagreement/information content is known

[Lec16] compares cosmic-web classifiers using information theory and explicitly considers predictive utility for later or unused observables.

Therefore the following candidate is refused:

> T-web/V-web or modal classifier disagreement contains additional information.

### Shear-electric-Weyl alignment has an established covariant theoretical role

In irrotational dust, [Bru94], [Els96b], [Les94], and [Maa98c] show that the shear tensor and electric Weyl tensor share an eigenframe in the silent/purely electric restriction. The covariant constraint can be written as the vanishing of the antisymmetric shear-Weyl product or equivalent commutator. A nonzero commutator is therefore not a new mathematical object.

In particular,

\[
D^b H_{ab}=-\epsilon_{abc}\sigma^b{}_d E^{cd}
\]

in the irrotational-dust covariant system [Maa98c].

This does not mean the commutator directly measures H_ab. It means the relational state has a known theoretical connection to departure from the silent aligned limit.

## Subtraction

The current modal preregistration may not claim novelty for any of the following:

- electric Weyl as a tidal tensor;
- tidal anisotropy beyond density;
- shear or tidal eigenvectors;
- generic eigenframe evolution;
- generic T-web/V-web disagreement;
- the mathematical fact that [sigma,E]=0 defines simultaneous diagonalization/alignment;
- the theoretical silent-universe role of shear-Weyl alignment.

## Surviving residual

No paper in the admitted corpus was found that performs the following complete test:

1. reconstruct the native velocity-shear tensor and full first-order electric-Weyl tensor from a relativistic cosmological simulation;
2. construct a bounded continuous noncommutativity observable from [sigma,E];
3. control for present scalar state;
4. control for the complete separate eigenvalue spectra of both tensors;
5. additionally control for a simpler static tensor-alignment scalar;
6. ask whether the commutator adds out-of-sample predictive information for subsequent field-level nonlinear shear reorganization;
7. test that added information on untouched independent initial-condition realizations;
8. include an independent higher-resolution holdout on the same physical Fourier band.

The residual is therefore:

> Does the local noncommutativity of the native velocity-shear and electric-Weyl tensors carry predictive information about subsequent nonlinear shear reorganization that is not already contained in scalar state, the separate tensor spectra, or a simple static tensor-alignment scalar?

This is narrower than modes matter, tidal anisotropy matters, or misalignment matters.

## Primary relational observable

For nonzero traceless symmetric tensors sigma and E,

\[
C_{\sigma E}
=
\frac{\|[\sigma,E]\|_F}
{\sqrt{2}\,\|\sigma\|_F\,\|E\|_F}.
\]

By the Böttcher-Wenzel commutator bound,

\[0\le C_{\sigma E}\le 1.\]

Properties:

- C_sigmaE = 0 when the tensors commute/share an eigenframe;
- it is invariant under a common spatial rotation;
- it is independent of the overall amplitude of either tensor;
- it is not determined by the two separate eigenvalue spectra alone.

If either tensor has exactly zero Frobenius norm, the relational orientation is undefined. Such cells are reported as undefined rather than assigned zero. No nonzero amplitude threshold is introduced.

## Strong non-relational/static baseline

The baseline is deliberately stronger than a density-only or tidal-anisotropy baseline.

At the prediction epoch it contains:

- normalized energy-density contrast from gevolution T00;
- native velocity divergence theta;
- Phi;
- chi_gev;
- electric-Weyl amplitude ||E||_F;
- complete trace-free electric-Weyl spectral shape q_E = 3 sqrt(6) det(E) / [tr(E^2)]^(3/2);
- shear amplitude ||sigma||_F;
- complete trace-free shear spectral shape q_sigma = 3 sqrt(6) det(sigma) / [tr(sigma^2)]^(3/2);
- static tensor cosine A_sigmaE = tr(sigma E) / (||sigma||_F ||E||_F).

For a trace-free symmetric 3x3 tensor, amplitude plus the normalized cubic invariant determines the unordered eigenvalue spectrum. The baseline therefore contains the separate spectra of both tensors and one simple static cross-tensor alignment scalar before C_sigmaE is added.

## Primary future target

The primary target is same-coordinate Eulerian shear reorganization over the frozen interval:

\[
R_\sigma(t_0,t_1)
=
\frac{\|\sigma(t_1)-\sigma(t_0)\|_F}
{\|\sigma(t_1)\|_F+\|\sigma(t_0)\|_F}.
\]

This lies in [0,1] when the denominator is nonzero.

The target is intentionally field-level. It does not claim a Lagrangian particle-history interpretation. Advection is part of the evolution being predicted and affects baseline and augmented models equally.

## Secondary non-gating target

A secondary target is local energy-density growth:

\[
G_\rho
=
\ln\left[
\frac{1+\delta_{T00}(t_1)}
{1+\delta_{T00}(t_0)}
\right].
\]

It is reported for functional relevance but cannot determine the primary ACCEPT/REFUSE outcome in v1.

## Literature adjudication

**Current outcome:** RESIDUAL_SURVIVES_STAGE_A.

Meaning:

- the broad modal claims were substantially reduced by prior art;
- the commutator itself is theoretically known;
- the admitted corpus did not reveal the complete predictive test defined above;
- novelty remains a falsifiable working status, not a declaration that no prior paper exists anywhere.

If a direct prior test is found before untouched P1-M evidence is opened, the preregistration must be revised and re-frozen.

If a direct prior is found only after P1-M is opened, the empirical result is preserved but the novelty claim ceiling is reduced.

## Key admitted sources

- [Ehl09] DOI 10.1007/s10714-009-0855-1
- [Bru94] DOI 10.1086/175755
- [Els96b] DOI 10.1088/0264-9381/14/5/018
- [Les94] DOI 10.1103/PhysRevD.52.3406
- [Maa98c] DOI 10.1088/0264-9381/15/4/021
- [Lib13] DOI 10.1093/mnras/stu629
- [Ram19] DOI 10.1093/mnras/stz2344
- [Mus17] DOI 10.1093/mnras/sty191
- [Bor16] DOI 10.1093/mnras/stx873
- [Lec16] DOI 10.1088/1475-7516/2016/08/027
- [Por01] DOI 10.1046/j.1365-8711.2002.05306.x
