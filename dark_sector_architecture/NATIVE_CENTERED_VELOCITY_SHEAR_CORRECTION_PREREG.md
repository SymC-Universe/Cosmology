# Native Centered Velocity-Shear Correction Preregistration

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q representation correction
**Status:** FROZEN BEFORE CORRECTED REAL-FIELD SHEAR RESULT
**Date:** 2026-09-27
**Parent development:** Development 012
**Parent fixed-band gate:** NATIVE_FIXED_BAND_WEYL_RESOLUTION_PREREG.md

## Purpose

Correct and requalify only the gevolution coarse-grained peculiar-velocity shear object after source audit established that exported `vi` is vertex-centered and uses a centered lattice derivative rather than the staggered metric-vector operator.

Electric-Weyl qualification is outside this corrective gate and is not rerun.

## Frozen source semantics

gevolution constructs exported velocity through:

1. `projection_Ti0_project` onto the scalar/vertex lattice;
2. `vertexProjectionCIC_comm`;
3. `compute_vi_rescaled`, with `vi = Ti0/source/a` where source is nonzero.

gevolution's own velocity Fourier diagnostics use

\[
k_i^{(v)}=N\sin(2\pi n_i/N)
\]

in `projectFTtheta` and `projectFTomega`.

The corrected shear is therefore

\[
\sigma_{ij}^{(v)}
=
\frac12(D_i^{(v)}v_j+D_j^{(v)}v_i)
-\frac13\delta_{ij}D_k^{(v)}v_k.
\]

## Frozen simulation family

- gevolution commit `0cca42e51a824002ae4fb602cbd79d671e8ffe60`;
- LATfield2 commit `2d8c737ab6adc965a1d2718c209f5085af27b09c`;
- canonical crystal template blob `d4de9a5400ef58f6a0181fbe61f18056b233a425`;
- seed 424242;
- L = 64 Mpc/h;
- N = 32, 64, 128;
- tiling = 8, 16, 32;
- one central requested snapshot at a = 0.010000 (approximately z=99);
- time-step limit 0.0005;
- exported field `v` only is sufficient for this correction.

## Frozen physical support

Use exactly the Development 011 support:

\[
\mathcal K_{32}=\{\mathbf n:0<|\mathbf n|<15,\ |n_i|<15\}.
\]

Reconstruct shear with each grid's own centered native operator first, then project the shear tensor onto the common K32 support and 32^3 comparison grid.

Restricting velocity first and differentiating second is prohibited for the primary convergence result.

## Required diagnostics

For N32, N64, N128 record:

- actual snapshot redshift and tau/L with full precision;
- centered-native shear Frobenius RMS;
- centered-native divergence RMS;
- centered-native vorticity RMS;
- trace residual of corrected shear;
- corrected-centered versus prior-staggered shear difference;
- corrected-centered versus continuum-spectral shear difference on K32.

For 32->64 and 64->128 corrected-native comparisons record:

- median and q95 relative tensor-operator error;
- eigenvalue errors;
- eigengap errors;
- eigenframe diagonal alignment quantiles;
- error/eigengap direction diagnostics.

## Outcome A: CENTERED_VELOCITY_SHEAR_QUALIFIED_P0Q

Use only if:

1. the three actual central epochs are aligned closely enough that epoch mismatch cannot compete with the measured resolution difference;
2. all velocity/shear/vorticity fields are finite;
3. shear is numerically symmetric and trace-free;
4. N64->N128 median relative operator error is lower than N32->N64;
5. N64->N128 q95 relative operator error is lower than N32->N64;
6. eigenframe and error/eigengap diagnostics improve or remain consistent with refinement;
7. no post-result mode deletion, smoothing retuning, or derivative substitution is used.

## Outcome B: NEED_MORE_INFO

Use if the corrected object is valid but convergence evidence is mixed, epoch mismatch competes with the trend, or identifiable-axis statistics remain dominated by degeneracy.

## Outcome C: REFUSED

Use if the centered native shear cannot be stably reconstructed, native-resolution error systematically worsens from 32->64 to 64->128, or the result requires post hoc changes to the frozen support/operator.

## Prior representation handling

The Development 011 staggered-operator shear values remain preserved. They are labeled `PRIOR_STAGGERED_VELOCITY_REPRESENTATION` and may be compared with the corrected centered result, but they cannot count toward native shear qualification.

## Consequence

If Outcome A passes, Development 012 is mechanically repaired and the APQ-3 late-time E-sigma development plan may resume.

If Outcome B or C occurs, PREG-MODAL-PA-1 must narrow or refuse its shear-dependent relational claim without affecting the independently qualified electric-Weyl branch.

## Exploration firewall

This correction cannot close modal P0-D, Conglomerate/System, or joint Scalar + Modal + Conglomerate exploration.
