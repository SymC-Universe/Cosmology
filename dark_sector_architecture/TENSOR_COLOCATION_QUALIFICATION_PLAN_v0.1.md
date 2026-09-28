# Native Tensor Vertex Co-location Qualification Plan v0.1

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q representation qualification
**Status:** FROZEN BEFORE CO-LOCATED OUTPUT INSPECTION
**Date:** 2026-09-27
**Trigger:** Development 015
**P1 status:** CLOSED

## Purpose

Qualify the deterministic mapping required to interpret gevolution/LATfield2 staggered symmetric tensor components as one local tensor on the scalar/vertex lattice.

This gate repairs representation semantics only. It does not test a cosmological physical claim.

## Source geometry

gevolution/LATfield2 places diagonal tensor components on vertices and off-diagonal component T_ij at the ij-plaquette center displaced by +Delta/2 along axes i and j from the vertex carrying the same lattice index.

Primary target location: scalar/vertex lattice.

## Frozen co-location operator

For diagonal components:

\[
T^V_{ii}(x)=T_{ii}(x).
\]

For off-diagonal components i != j:

\[
T^V_{ij}(x)=\frac14[
T_{ij}(x)+T_{ij}(x-\hat e_i)+T_{ij}(x-\hat e_j)+
T_{ij}(x-\hat e_i-\hat e_j)].
\]

Periodic boundaries are mandatory.

The symmetric pair T_ij and T_ji is co-located once and written identically to preserve matrix symmetry.

## Fourier meaning

For a Fourier mode the mapping removes the plaquette-center stagger phase and multiplies the vertex-centered mode by

\[
C_{ij}(\mathbf k)=
\cos(k_i\Delta/2)\cos(k_j\Delta/2).
\]

This factor is a second-order symmetric interpolation/filter. It is not inverted.

Near-Nyquist attenuation is therefore expected and must be reported as a Limit Map, not numerically undone.

## Frozen known-truth cases

### TC-01 Diagonal passthrough
Arbitrary finite diagonal component fields remain bitwise/equivalently unchanged.

### TC-02 Four-point periodic formula
Every off-diagonal component equals the explicit four-point periodic average, including wraparound cells.

### TC-03 Symmetry
A symmetric staggered tensor remains symmetric after co-location.

### TC-04 Single-mode Fourier transfer
For an analytic off-diagonal single Fourier mode sampled at the plaquette center, the co-located vertex Fourier coefficient has the expected zero phase relative to the vertex truth and the expected amplitude factor C_ij.

### TC-05 Smooth-field convergence
For a smooth periodic analytic tensor sampled on its native staggered locations, vertex co-location error decreases at second order under grid refinement. The test uses a frozen N sequence and reports the observed convergence ratio without fitting an empirical scientific threshold.

### TC-06 Nyquist filtering
A mode at the Nyquist frequency along either staggered axis is attenuated to numerical zero by the co-location operator. No inverse/reconstruction is attempted.

### TC-07 Linearity
Co-location of a linear combination equals the same linear combination of separately co-located tensors to floating-point precision.

### TC-08 refusal semantics
Refuse non-finite arrays, wrong terminal tensor shape, non-cubic/non-3D spatial grids where the downstream cosmology pipeline requires a cubic periodic grid, and materially nonsymmetric inputs rather than silently symmetrizing them.

## Acceptance

`TENSOR_COLOCATION_QUALIFIED_P0Q` only if TC-01 through TC-08 pass without post-result changes and the Fourier transfer agrees with the frozen geometry.

## Need more information

`TENSOR_COLOCATION_NEED_MORE_INFO` if the real-space and Fourier descriptions cannot be reconciled to floating-point/known-truth accuracy, or if source geometry is ambiguous enough to change the physical target point.

## Refusal

`TENSOR_COLOCATION_REFUSED` if the frozen operator fails periodicity, symmetry, phase removal, expected interpolation transfer, or second-order smooth-field recovery.

## Downstream gate if qualified

Run a focused N32/N64/N128 fixed-physical-band requalification of co-located electric-Weyl local tensors.

Only after co-location may downstream code compute:
- local Weyl eigenvalues/eigenframes;
- eigengaps and error/eigengap directional diagnostics;
- local matrix operator norms;
- native-versus-continuum local modal comparisons;
- E-sigma commutators/eigenframe relations.

## Exploration firewall

A failure of co-location or local Weyl eigensystem qualification does not close componentwise Weyl fields, corrected velocity shear, Conglomerate/System, joint, inheritance, or P0-D exploration.
