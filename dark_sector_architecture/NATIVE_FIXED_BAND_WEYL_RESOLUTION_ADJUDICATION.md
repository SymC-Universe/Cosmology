# Native Fixed-Band Electric-Weyl Resolution Adjudication

**Project:** Cosmic Stability Architecture  
**Stage:** P0-Q modal/representation qualification  
**Date:** 2026-09-27  
**Frozen preregistration:** NATIVE_FIXED_BAND_WEYL_RESOLUTION_PREREG.md  
**Frozen preregistration commit:** 8b570edd23896e6feb6418ba0bb01cbcbe7d7d28  
**Decisive workflow:** 36357943715  
**Workflow head:** 3c13306f0eae1f09636ca06bc833a7190095bf05

## Adjudicated outcome

\[
\boxed{\text{NATIVE\_FIXED\_BAND\_WEYL\_QUALIFIED\_P0Q}}
\]

**Development 012 correction:** the electric-Weyl qualification remains valid, but the velocity-shear line item is withdrawn from native qualification because gevolution's exported `vi` field uses a centered vertex-lattice derivative rather than the staggered metric-vector derivative used in the original shear reconstruction. Corrected shear status is `NEED_MORE_INFO` pending centered-operator requalification.

Independent representation-split classification:

\[
\boxed{\text{SPLIT\_COLLAPSES\_ON\_COMMON\_BAND}}
\]

These are representation-qualification outcomes only. They do not activate P1 and do not establish a dark-sector claim.

## Preregistration integrity

The preregistration was committed before the decisive workflow existed. Repository path history verifies commit 8b570edd23896e6feb6418ba0bb01cbcbe7d7d28 at 23:10:11 UTC. The decisive workflow was created at 23:13:09 UTC.

The first persisted result incorrectly wrote the workflow head into the preregistration-commit field because the workflow used a shallow checkout. The branch result was corrected after completion with an explicit provenance note. No scientific value was changed. The workflow was subsequently changed to full-history checkout for future runs.

## Frozen common band

The experiment retained the prospectively frozen N32 active-overlap sphere:

\[
0<|\mathbf n|<15,
\qquad |n_i|<15.
\]

Mode count: 13,996.

Each resolution was differentiated and reconstructed with its own native operator before any projection onto the common band.

## Epoch alignment

The central snapshots were exactly aligned in the logged evolution coordinates:

- N32: z = 98.99516176429084, tau/L = 14.141552190017416;
- N64: z = 98.99516176429084, tau/L = 14.141552190017416;
- N128: z = 98.99516176429084, tau/L = 14.141552190017416.

Thus cross-resolution epoch mismatch is zero in the recorded coordinates.

## Native field validity

All three simulations retained machine-small native constraint residuals.

At the central snapshot:

- N32 B divergence/curl = 1.41e-14; h divergence/norm = 1.43e-14; h trace/norm = 4.47e-16;
- N64 B divergence/curl = 1.20e-14; h divergence/norm = 3.00e-14; h trace/norm = 5.23e-16;
- N128 B divergence/curl = 9.37e-15; h divergence/norm = 7.01e-14; h trace/norm = 6.04e-16.

Independent Python native-lattice post-processing reproduced the same constraint scale.

## Temporal floor

Common-band full-Weyl inner-versus-outer median relative tensor differences were:

- N32: 3.08e-9;
- N64: 2.02e-9;
- N128: 2.59e-9.

The cross-resolution differences are many orders of magnitude larger, so the observed resolution trend is not set by the demonstrated temporal-stencil floor.

## Native resolution direction

| Family | N32->N64 median | N64->N128 median | N32->N64 q95 | N64->N128 q95 | Direction |
| --- | ---: | ---: | ---: | ---: | --- |
| Scalar Weyl | 0.3041 | 0.1428 | 0.7149 | 0.3468 | convergent |
| Vector Weyl | 0.7117 | 0.4384 | 1.0128 | 0.9310 | convergent |
| Tensor Weyl | 0.07594 | 0.03101 | 0.1826 | 0.07609 | convergent |
| Full Weyl | 0.3041 | 0.1428 | 0.7149 | 0.3468 | convergent |
| Prior shear representation | 0.4987 | 0.1925 | 1.0831 | 0.4221 | preserved but not native-gevolution shear after Development 012 |

All four electric-Weyl sector objects move in the refinement direction required by the preregistration. The prior shear line also converged numerically, but Development 012 found that its derivative staggering did not match gevolution's native velocity field; it is therefore preserved as representation-specific evidence and reclassified `NEED_MORE_INFO`.

Full-Weyl median eigenframe alignments also improve from approximately (0.9915, 0.9794, 0.9913) for N32->N64 to (0.9980, 0.9954, 0.9979) for N64->N128. The corresponding q05 alignments improve from approximately (0.8134, 0.6265, 0.8153) to (0.9565, 0.9079, 0.9573). Error/eigengap direction diagnostics improve in the same direction.

Native shear shows the same qualitative improvement rather than remaining an unresolved side channel.

## Early-epoch sector amplitudes on the common band

Relative to scalar-Weyl Frobenius RMS:

| Grid | Vector/scalar | Tensor/scalar |
| --- | ---: | ---: |
| N32 | 2.35e-6 | 1.72e-6 |
| N64 | 9.72e-7 | 1.62e-6 |
| N128 | 8.25e-7 | 1.59e-6 |

The vector and tensor sectors remain tiny at this early epoch, but they were retained explicitly and independently throughout the qualification.

## Native-versus-continuum split

Median native-versus-continuum relative tensor error on the same frozen band:

| Family | N32 | N64 | N128 | Native N64->N128 resolution error | Classification |
| --- | ---: | ---: | ---: | ---: | --- |
| Scalar Weyl | 0.5803 | 0.2817 | 0.1397 | 0.1428 | collapses |
| Vector Weyl | 0.6912 | 0.2526 | 0.09610 | 0.4384 | collapses |
| Tensor Weyl | 0.03001 | 0.006993 | 0.001769 | 0.03101 | collapses |
| Full Weyl | 0.5803 | 0.2817 | 0.1397 | 0.1428 | collapses |
| Shear | 0.4051 | 0.2708 | 0.1439 | 0.1925 | collapses |

For every frozen family, native-versus-continuum disagreement decreases monotonically with refinement and by N128 is no larger than the corresponding native N64->N128 resolution uncertainty.

This satisfies the preregistered SPLIT_COLLAPSES_ON_COMMON_BAND rule.

## Scientific interpretation

The large native-versus-continuum disagreement seen on the unrestricted N64 grid does not persist as a stable representation split when the same physical Fourier support is held fixed and resolution is increased.

The result is consistent with the native and continuum constructions approaching a common resolved-band limit while differing substantially at finite resolution and near the grid-dependent ultraviolet end.

This does not license treating finite-resolution continuum tensors as identical to native gevolution tensors. Native-model-first remains the primary rule.

The earlier continuum fixed-band convergence chain is retained and gains stronger interpretive support as comparator evidence for the same resolved-band limit, rather than being promoted retroactively to native evidence.

## Consequence for the investigation

The native Weyl/shear modal representation has now passed:

1. algebraic known truth;
2. temporal-derivative known truth;
3. native LATfield2 operator known truth;
4. real-field native transversality/TT checks;
5. early-epoch full electric-Weyl temporal qualification;
6. prospectively frozen N32/N64/N128 fixed-band resolution qualification.

This is sufficient to reopen the exact residual definition and activation assessment for PREG-MODAL-PA-1.

It is not sufficient to activate that preregistration automatically. Its claim, strongest comparator, falsifier, indeterminate zone, untouched decisive evidence route, and relationship to Conglomerate/System and joint gates must now be frozen explicitly.

## Exploration firewall

No scalar, Conglomerate/System, joint-meaning, additional-component, or P0-D exploration gate is closed by this result.


## Development 012 correction

gevolution's exported `vi` field is vertex-centered and its native Fourier divergence/vorticity routines use the centered symbol (N\sin(2\pi n/N)). The prior shear line used the staggered (B_i) operator. This does not affect scalar/vector/tensor/full electric Weyl. The original preregistration explicitly allowed shear to remain `NEED_MORE_INFO` without invalidating the independent full-Weyl gate. A corrected shear-only qualification is required before E-sigma relational testing.


## Development 013 shear-resolution addendum

The Development 012 centered-velocity correction has now completed under a
separately frozen gate.

Corrected native centered velocity shear is
`CENTERED_VELOCITY_SHEAR_QUALIFIED_P0Q`.

Its common-band median relative resolution error improves
0.5094 -> 0.1656 and q95 improves 1.0681 -> 0.3158 from N32->N64 to
N64->N128. Eigenframe and error/eigengap diagnostics improve in the same
direction.

Accordingly, the original fixed-band program now has:
- native electric-Weyl: QUALIFIED_P0Q;
- corrected native coarse-grained velocity shear: QUALIFIED_P0Q.

The historical Development 011 staggered-shear numbers remain preserved but
are superseded for native velocity-shear semantics by the Development 013
centered result.
