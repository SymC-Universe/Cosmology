# Material-Patch Tensor Interpolation Qualification Plan v0.1

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q material representation qualification
**Status:** FROZEN BEFORE REAL LATE-TIME PATCH OUTCOME INSPECTION
**Date:** 2026-09-27
**Dependencies:** Development 013 centered velocity shear; Development 014 particle lineage; Development 016 co-located local electric-Weyl eigensystem
**P1 status:** CLOSED

## Purpose

Qualify the deterministic machinery needed to evaluate vertex-centered modal tensors at the same tracked material locations and aggregate them into reproducible Lagrangian material patches.

This gate does not choose the scientific patch scale and does not test E-sigma predictive added value.

## Coordinate convention

gevolution particle positions are dimensionless periodic box coordinates in [0,1).

Vertex grid index i along an N-point axis represents x=i/N.

Finite particle positions are interpreted periodically with x -> x mod 1.

## Frozen grid-to-particle interpolation

Use periodic trilinear interpolation of tensor **components**, never eigenvalues or eigenvectors.

For each particle position x, define

\[
u_a=N x_a,\qquad i_a=\lfloor u_a\rfloor,\qquad f_a=u_a-i_a.
\]

The particle tensor is the weighted sum of the eight periodic neighboring vertex tensors with weights

\[
w(d_x,d_y,d_z)=\prod_a [d_a f_a+(1-d_a)(1-f_a)]
\]

for d_a in {0,1}.

Local eigensystems are computed only after tensor-component interpolation.

## Frozen material-patch semantics

Patch membership is Lagrangian and ID-frozen:
1. choose a reference snapshot before outcome inspection;
2. assign each unique particle ID to exactly one patch from its reference position and a prospectively supplied periodic patch-grid shape;
3. retain that ID->patch map at every later epoch;
4. do not reassign a particle when it crosses an Eulerian patch boundary.

The patch-grid shape is an input to the generic method and is **not chosen by this qualification gate**.

For equal-mass CDM particles, the primary patch tensor is the arithmetic particle mean of the interpolated tensor samples. This is a material-mass-weighted patch state, not a volume average.

Empty patch IDs are omitted/reported as empty. They are never represented by zero tensors.

## Frozen known-truth cases

### MP-01 Vertex exactness
Particle positions exactly on vertices recover the original vertex tensor components.

### MP-02 Constant field
Any finite constant tensor field is recovered exactly at arbitrary particle positions.

### MP-03 Periodic wrap
Positions x, x+n for integer vector n produce identical interpolated tensors, including boundary-crossing cases.

### MP-04 Linearity
Interpolation commutes with finite linear combinations.

### MP-05 symmetry and trace structure
Symmetric inputs remain symmetric after interpolation. Trace-free inputs remain trace-free to floating-point accuracy because interpolation is componentwise linear.

### MP-06 smooth periodic convergence
For a frozen smooth periodic analytic tensor and frozen physical sample points, interpolation error decreases at second order under N=16,32,64 refinement.

### MP-07 particle reorder invariance
Changing HDF5/array record order while preserving IDs and positions does not change ID-keyed interpolated results.

### MP-08 deterministic reference partition
For unique IDs and finite reference positions, a supplied patch-grid shape assigns every ID to exactly one periodic patch with no overlaps or duplicates.

### MP-09 frozen material membership
After particles move across Eulerian patch boundaries, later aggregation still uses their frozen reference-patch membership.

### MP-10 patch mean known truth
For a constant tensor over all particles in a patch, the patch arithmetic mean recovers that tensor exactly and is invariant to particle order.

### MP-11 patch modal recovery
For patches populated by prospectively constructed nondegenerate constant/controlled tensors, aggregate-then-diagonalize recovers the known patch eigensystem; exactly degenerate controls retain the existing modal refusal/subspace semantics.

### MP-12 fail-closed lineage/data semantics
Refuse duplicate IDs, missing reference IDs, non-finite positions/tensors, invalid tensor shape, invalid patch-grid shape, or materially nonsymmetric tensor samples.

## Acceptance

`MATERIAL_PATCH_INTERPOLATION_QUALIFIED_P0Q` only if MP-01 through MP-12 pass with no outcome-dependent modification.

## Need more information

`MATERIAL_PATCH_INTERPOLATION_NEED_MORE_INFO` if interpolation is numerically valid but patch eigensystem semantics or lineage matching cannot be reconciled prospectively.

## Refusal

`MATERIAL_PATCH_INTERPOLATION_REFUSED` if periodic interpolation, ID-frozen membership, symmetry preservation, expected convergence, or fail-closed lineage behavior fails.

## Downstream development rule

If qualified, a separate APQ/freeze must choose:
- reference epoch;
- patch-grid scale(s);
- primary Band L filtering;
- modal features/endpoints;
- persistence/autoregressive comparator;
- development stopping rule.

Only then may seed 424242 be used for z~2 -> z~1 -> z~0.5 P0-Q development.

Untouched P1 remains prohibited.

## Exploration firewall

Failure of this material representation does not invalidate qualified grid fields or close Conglomerate/System, joint, inheritance, or P0-D exploration.
