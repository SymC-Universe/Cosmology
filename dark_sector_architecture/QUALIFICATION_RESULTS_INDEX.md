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

Status:
**SIGNIFICANT DEVELOPMENT / FIXED-BAND FOLLOW-UP REQUIRED**

On the full N64 grid:
- scalar native-versus-continuum median relative tensor difference: approximately (0.562);
- full native-versus-continuum median relative tensor difference: approximately (0.562);
- vector median relative tensor difference: approximately (0.488);
- tensor median relative tensor difference: approximately (0.0168).

Interpretation:
- continuum and native lattice reconstructions are not interchangeable on the full grid;
- the discrepancy has not yet been decomposed into UV/staggering versus persistent common-band representation effects;
- a native-lattice fixed-physical-band (N=32,64,128) ladder is required before modal preregistration activation.

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

## Qualification status

Qualified at P0-Q:
- modal eigensystem machinery;
- LATfield2 HDF5 semantics;
- electric-Weyl sector algebra;
- nonuniform temporal derivative machinery;
- LATfield2/gevolution native spatial operators;
- native full electric-Weyl representation at the tested early N64 epoch.

Still held:
- native fixed-band resolution convergence;
- universal or later-epoch scalar-dominance statements;
- `PREG-MODAL-PA-1` activation;
- Conglomerate/System promotion;
- joint Scalar + Modal + Conglomerate promotion;
- any P1 dark-sector claim.

No P1 claim is activated by any result in this index.
