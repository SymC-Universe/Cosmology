# Canonical sc1 512-Particle Smoke Baseline

**Stage:** P0-Q  
**Run:** 36352785617  
**Head:** `b6bed7dfb79069689127bc245cfaa34d72f4b598`  
**Persistence commit:** `bb6373b05da0e638184c7192c2ef530f290d2c85`  
**Artifact ID:** 10942733438  
**Artifact digest:** `sha256:36423d553bb59a43cefe331c08e113346d190b3a8e1bea0c83c14e2c1c0d1fde`  
**Artifact expiry:** 2026-12-26T21:43:48Z

Canonical upstream particle template:
- source: `gevolution-code/gevolution-1.2/sc1_crystal.dat`;
- Git blob: `d4de9a5400ef58f6a0181fbe61f18056b233a425`;
- template particles: 64 CDM particles;
- tiling factor: 2;
- total smoke particles: 512.

Run diagnostics:
- maximum initial displacement: 0.0255257 lattice units;
- cycle-0 average T00: 0.312046;
- cycle-0 background model: 0.312046;
- finite phi/B/chi/hij/v outputs produced;
- weak-field modal extraction completed.

This is the canonical P0-Q infrastructure/development baseline. It does not activate PREG-MODAL-PA-1 or any cosmological claim.

## Cross-template identity

The complete NPZ arrays from this canonical run were compared against run 12, which used a one-particle deterministic simple-cubic template tiled eight times per axis for the same total 512 particles.

Every stored array is exactly equal:
- phi;
- velocity;
- tidal tensor;
- shear tensor;
- theta;
- tidal eigenvalues;
- shear eigenvalues;
- tidal eigengaps;
- shear eigengaps;
- shear-tidal alignment.

For every array:
- `numpy.array_equal = true`;
- maximum absolute difference = 0;
- mean absolute difference = 0.

Therefore, for this Ngrid=8 qualification configuration, the generated 512-particle lattice and canonical `sc1_crystal.dat` 512-particle lattice are representation-equivalent at the saved-field level.
