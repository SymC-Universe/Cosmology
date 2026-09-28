# Co-located Weyl Fixed-Band Requalification Adjudication

**Project:** Cosmic Stability Architecture
**Stage:** P0-Q local modal representation requalification
**Date:** 2026-09-27
**Frozen plan:** COLOCATED_WEYL_FIXED_BAND_REQUALIFICATION_PLAN_v0.1.md
**Frozen plan commit:** 6acc0d4868d0574c4041eeaec53426efdfe3f290
**Decisive workflow:** 36365508065
**Workflow head:** 6b2aa0ff23edd66905fc9cd86a4d9af41d3d050b
**P1 exposed:** NO

## Adjudicated outcome

\[
\boxed{\text{COLOCATED\_LOCAL\_WEYL\_QUALIFIED\_P0Q}}
\]

Therefore:

\[
\boxed{\text{LOCAL\_WEYL\_EIGENSYSTEM\_P0Q = QUALIFIED}}.
\]

This is a representation qualification only.

## Tensor co-location dependency

The preceding frozen co-location gate TC-01 through TC-08 passed as
`TENSOR_COLOCATION_QUALIFIED_P0Q`.

Native staggered electric-Weyl sector fields were therefore reconstructed on
their LATfield2 locations, vertex-co-located with the frozen four-point
operator, and only then treated as local 3x3 matrices.

No co-location filter was inverted.

## Exact epoch and support

All three resolutions land at exactly the same recorded central epoch:

\[
z=98.99516176429084,\qquad \tau/L=14.141552190017416.
\]

Common support:

\[
0<|\mathbf n|<15,\qquad |n_i|<15,
\]

with 13,996 retained signed Fourier modes.

## Full-Weyl local resolution convergence

| Diagnostic | N32->N64 | N64->N128 |
| --- | ---: | ---: |
| Median relative tensor error | 0.2740 | **0.07671** |
| q95 relative tensor error | 0.5798 | **0.1504** |
| Median error/gap, lower pair | 0.3150 | **0.08724** |
| Median error/gap, upper pair | 0.3156 | **0.08697** |
| q95 error/gap, lower pair | 1.2267 | **0.3292** |
| q95 error/gap, upper pair | 1.2090 | **0.3219** |

Median eigenframe diagonal alignment improves:

\[
(0.99571,0.99043,0.99568)
\rightarrow
(0.999669,0.999277,0.999671).
\]

The q05 alignment improves much more strongly:

\[
(0.9163,0.8255,0.9213)
\rightarrow
(0.99424,0.98855,0.99465).
\]

Thus both central and lower-tail modal identifiability improve with refinement.

## Scalar-Weyl local convergence

Scalar-Weyl median relative error improves

\[
0.2740\rightarrow0.07671,
\]

and q95 improves

\[
0.5798\rightarrow0.1504.
\]

The full tensor is scalar-dominated at this early epoch, but vector and tensor
sectors remain independently reported rather than removed.

## Temporal uncertainty

Full-Weyl inner-versus-outer temporal-stencil median relative errors are:

- N32: 2.84e-9;
- N64: 2.04e-9;
- N128: 2.60e-9.

q95 remains below approximately 6.1e-9 at all three resolutions.

These are many orders of magnitude below the spatial-resolution differences
used in this gate.

## Native-versus-continuum representation comparison after co-location

Full/scalar median relative discrepancy:

\[
0.42873\rightarrow0.11027\rightarrow0.027578.
\]

At N128 this is below the native N64->N128 median resolution error of
0.07671, satisfying the frozen `COLLAPSES_ON_COMMON_BAND` rule.

Vector discrepancy also collapses:

\[
0.61527\rightarrow0.18592\rightarrow0.07216.
\]

### Tensor-sector exception

The tiny tensor sector is internally native-convergent:

\[
0.05870\rightarrow0.01737
\]

in adjacent median resolution error, with q95

\[
0.1454\rightarrow0.04221.
\]

However its native-versus-continuum median discrepancy is

\[
0.10588\rightarrow0.05254\rightarrow0.02629,
\]

which at N128 remains larger than its native N64->N128 resolution error
0.01737.

Therefore:

\[
\boxed{\text{TENSOR-SECTOR NATIVE-vs-CONTINUUM = NEED\_MORE\_INFO}}.
\]

This sector-specific hold does not invalidate the full/local Weyl gate because
the tensor sector is only about 1.6e-6 of the scalar-sector Frobenius RMS in
the tested regime and was never allowed to be hidden inside the total.

## Effect of the Development 015 repair

Co-location is materially consequential. At N128 the raw-to-co-located total
change has Frobenius RMS approximately 3.68e-4 while the raw-index tensor RMS
is approximately 8.68e-4.

The corrected local comparison also improves substantially relative to the
pre-co-location raw-index results. The prior local-matrix/eigenframe numbers
are therefore retained as historical evidence of the stagger-location error
but are superseded for local eigensystem interpretation.

Componentwise native Weyl field results were not invalidated by Development
015 and remain qualified.

## Claim ceiling

Supported:
- vertex-co-located local electric-Weyl matrices are operationally defined;
- full/scalar local eigensystems converge strongly on the frozen common band;
- local full-Weyl eigenframes are numerically identifiable at the tested early epoch under the qualified representation;
- native and continuum comparator full/scalar representations approach the same resolved-band limit.

Not supported:
- standalone tensor-sector native/continuum equivalence;
- universal eigenframe identifiability at all epochs/scales;
- late-time material-patch E-sigma predictive added value;
- observer-independent/full-GR modal claims;
- any P1 dark-sector or capital-Chi claim.

## Next licensed action

Resume the Development 014/015 material-lineage route:
1. freeze material-patch and grid-tensor interpolation qualification;
2. use stable particle IDs to define non-overlapping material patches;
3. interpolate co-located E and corrected centered sigma onto identical particle/material locations;
4. qualify patch averaging and eigensystem recovery on known truths;
5. use primary Band L `0<|n|<4` and preferred z~2 -> z~1 -> z~0.5 only after the interpolation machinery passes;
6. keep all resulting prediction work P0-Q development until parent APQ-3 and MFR freeze are complete.
