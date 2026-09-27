# Cosmology Qualification Results Index

**Project:** Cosmic Stability Architecture  
**Branch:** `dark-sector-stability-architecture`  
**Stage:** P0-Q modal/representation qualification  
**Updated:** 2026-09-27

## Modal eigensystem known-truth suite

Path:
`dark_sector_architecture/qualification/results/modal_known_truth_report.json`

Status:
**GENERATED / DURABLE**

Cases:
KT-01 through KT-12.

Interpretation:
- exact degeneracy refuses unique direction;
- rotation covariance passes;
- scalar-matched/modal-different known truth passes;
- near-degeneracy is tracked continuously through eigengap/conditioning;
- known-bad nonsymmetric tensor is refused;
- no scientific eigengap threshold is frozen.

## Weak-field comparator reconstruction suite

Path:
`dark_sector_architecture/qualification/results/weak_field_known_truth_report.json`

Status:
**GENERATED / DURABLE**

Cases:
WF-01 through WF-04.

Interpretation:
- periodic continuum spectral Hessian recovery passes;
- trace-free scalar tidal construction passes;
- velocity divergence/shear recovery passes;
- off-diagonal shear recovery passes;
- these objects are retained as comparator representations and are not relabeled as the native LATfield2 electric-Weyl tensor.

## gevolution real-field extraction

Durable outputs:
- `qualification/results/gevolution_modal_pilot_metadata.json`
- `qualification/results/gevolution_modal_pilot_manifest.txt`
- `qualification/results/gevolution_modal_extraction_summary.json`

Status:
**GENERATED / DURABLE**

The canonical CPU pairing is:
- gevolution `0cca42e51a824002ae4fb602cbd79d671e8ffe60`;
- LATfield2 `2d8c737ab6adc965a1d2718c209f5085af27b09c`.

The canonical historical `sc1_crystal.dat` particle template is used for real-field qualification.

## Continuum fixed-band resolution chain

Durable outputs include:
- `qualification/results/q_r2_n8_n16_resolution_pair.json`
- `qualification/results/q_r2_n16_n32_resolution_pair.json`
- `qualification/results/q_r2_n32_n64_resolution_pair.json`
- `qualification/results/q_r2_highres_n32_n64.json`
- `qualification/results/q_r2_highres_n64_n128.json`
- `qualification/results/q_r3_fixed_band_n32_n64_n128.json`
- `qualification/results/highres_scalar_weyl_slip_n32.json`
- `qualification/results/highres_scalar_weyl_slip_n64.json`
- `qualification/results/highres_scalar_weyl_slip_n128.json`

Status:
**GENERATED / DURABLE / COMPARATOR-REPRESENTATION**

Interpretation:
- fixed physical support sharply improves scalar-Weyl convergence with resolution;
- velocity-shear converges more slowly;
- Development 010 shows that continuum FFT and native LATfield2 Weyl reconstructions differ materially on the full N64 grid;
- therefore these continuum resolution results remain valid within their representation but do not by themselves qualify the native gevolution Weyl representation.

## Electric-Weyl sector algebra

Path:
`qualification/results/electric_weyl_known_truth_report.json`

Status:
**GENERATED / DURABLE**

Cases:
EW-01 through EW-04.

Interpretation:
- scalar limit passes;
- transverse vector coefficient/sign passes;
- pure TT vacuum-wave coefficient/sign passes;
- mixed scalar/vector/tensor linear superposition passes;
- this qualifies the frozen algebra, not real-snapshot temporal derivatives by itself.

## Temporal derivative known truth

Path:
`qualification/results/temporal_derivative_known_truth_report.json`

Status:
**GENERATED / DURABLE**

Cases:
TD-01 through TD-04.

Interpretation:
- arbitrary nonuniform conformal-time derivative weights pass;
- nested inner/outer centered stencils pass;
- no equal-spacing assumption is required;
- the real temporal pilot uses full-precision actual `tau/boxsize`.

## LATfield2/gevolution native operator known truth

Path:
`qualification/results/latfield2_native_operator_known_truth_report.json`

Status:
**GENERATED / DURABLE**

Cases:
NL-01 through NL-04.

Interpretation:
- native backward/forward derivatives reproduce direct periodic finite differences;
- native lattice Laplacian reproduces the gevolution `gridk2` operator;
- vector divergence and staggered symmetric gradient reproduce gevolution conventions;
- tensor divergence and Laplacian reproduce gevolution staggering;
- scalar native STF Hessian reproduces the gradient-then-staggered-gradient construction.

## Real five-snapshot native electric-Weyl temporal pilot

Paths:
- `qualification/results/electric_weyl_temporal_snapshot_metadata.json`
- `qualification/results/electric_weyl_temporal_pilot.json`

Workflow:
`36357082516` **SUCCESS**

Frozen gate:
`ELECTRIC_WEYL_TEMPORAL_QUALIFICATION_GATE.md`

Current outcome:
**REPRESENTATION_QUALIFIED_P0Q for the tested early N64 epoch**

Key native result at (z\simeq98.9952):
- vector/scalar Frobenius RMS: (8.66\times10^{-7});
- tensor/scalar Frobenius RMS: (1.31\times10^{-6});
- full-versus-scalar median relative tensor difference: (1.50\times10^{-6});
- inner-versus-outer temporal-stencil median relative tensor difference: (2.37\times10^{-9});
- native full-versus-scalar eigenframes are effectively identical at this epoch.

Native constraints at the center snapshot:
- (\max|\nabla\cdot B|/\max|\nabla\times B|\approx1.20\times10^{-14});
- (\max|\nabla\cdot h|/\max|h|\approx3.00\times10^{-14});
- (\max|\mathrm{tr}\,h|/\max|h|\approx5.23\times10^{-16}).

## Native versus continuum representation comparison

Full-grid N64 status from Development 010:
**FINITE-RESOLUTION REPRESENTATION SPLIT OBSERVED**

On the unrestricted N64 grid:
- scalar native-versus-continuum median relative tensor difference: approximately 0.562;
- full native-versus-continuum median relative tensor difference: approximately 0.562;
- vector median relative tensor difference: approximately 0.488;
- tensor median relative tensor difference: approximately 0.0168.

Development 011 resolves the required follow-up on the prospectively frozen common physical band:

**SPLIT_COLLAPSES_ON_COMMON_BAND**

At N32 -> N64 -> N128, native-versus-continuum median relative tensor error becomes:
- scalar/full Weyl: 0.5803 -> 0.2817 -> 0.1397;
- vector Weyl: 0.6912 -> 0.2526 -> 0.09610;
- tensor Weyl: 0.03001 -> 0.006993 -> 0.001769;
- shear: 0.4051 -> 0.2708 -> 0.1439.

At N128 each split is no larger than the corresponding native N64->N128
resolution uncertainty on the same band.

Interpretation:
- continuum and native lattice reconstructions are not interchangeable at finite full-grid resolution;
- the split does not persist as a stable common-band separation;
- the evidence is consistent with both representations approaching the same resolved-band limit;
- native-model-first remains the primary representation rule.

## Native fixed-band N32/N64/N128 qualification

Frozen preregistration:
`NATIVE_FIXED_BAND_WEYL_RESOLUTION_PREREG.md`

Adjudication:
`NATIVE_FIXED_BAND_WEYL_RESOLUTION_ADJUDICATION.md`

Durable outputs:
- `qualification/results/native_fixed_band_weyl_ladder.json`
- `qualification/results/native_fixed_band_n32_metadata.json`
- `qualification/results/native_fixed_band_n64_metadata.json`
- `qualification/results/native_fixed_band_n128_metadata.json`

Workflow:
`36357943715` **SUCCESS**

Outcome:
**NATIVE_FIXED_BAND_QUALIFIED_P0Q**

Median relative operator error improves from N32->N64 to N64->N128:
- scalar Weyl: 0.3041 -> 0.1428;
- vector Weyl: 0.7117 -> 0.4384;
- tensor Weyl: 0.07594 -> 0.03101;
- full Weyl: 0.3041 -> 0.1428;
- native shear: 0.4987 -> 0.1925.

The q95 error improves for all five families, and full-Weyl eigenframe and
error/eigengap diagnostics improve in the same direction.

The common-band temporal reconstruction floor remains about 2-3e-9 in median
relative full-Weyl tensor difference, far below the cross-resolution effects.

The three central epochs are exactly aligned in the recorded evolution
coordinates.

## Pipeline source files

Primary native representation:
- `qualification/latfield2_native_operators.py`
- `qualification/electric_weyl.py`
- `qualification/temporal_derivatives.py`
- `qualification/run_electric_weyl_temporal_pilot.py`

Comparator / supporting representation:
- `qualification/weak_field_tensors.py`
- `qualification/fourier_resolution.py`
- `qualification/run_fixed_band_convergence.py`
- `qualification/run_native_fixed_band_weyl_ladder.py`

## Qualification status

Qualified at P0-Q:
- modal eigensystem machinery;
- LATfield2 HDF5 semantics;
- electric-Weyl sector algebra;
- nonuniform temporal derivative machinery;
- LATfield2/gevolution native spatial operators;
- native full electric-Weyl representation at the tested early N64 epoch;
- native N32/N64/N128 fixed-band Weyl/shear resolution convergence.

Still held:
- universal or later-epoch scalar-dominance statements;
- `PREG-MODAL-PA-1` activation;
- Conglomerate/System promotion;
- joint Scalar + Modal + Conglomerate promotion;
- any P1 dark-sector claim.

No P1 claim is activated by any result in this index.
