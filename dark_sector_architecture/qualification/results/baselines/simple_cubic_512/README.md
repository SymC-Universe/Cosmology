# Simple-Cubic 512-Particle Smoke Baseline

**Stage:** P0-Q  
**Run:** 36350705742  
**Head:** `fe0269cf5241a523e439eaad81fb575af2b804ce`  
**Persistence commit:** `0603f4ba22a4b29731b0b40f59617eb1c2f6979d`  
**Artifact ID:** 10941723946  
**Artifact digest:** `sha256:106920f81c6dce5560f2ce843fcd3205793ab80ec0590bed8402d017ffa4fb92`  
**Artifact expiry:** 2026-12-26T21:10:09Z

This is the first durable gevolution smoke in the current qualification chain with:

- canonical CPU source pairing;
- valid 2x2 MPI layout;
- fail-closed shell behavior;
- Ngrid = 8;
- one deterministic simple-cubic template particle tiled 8 times per axis, yielding 512 CDM particles;
- finite HDF5 phi and velocity fields;
- successful weak-field tidal/shear extraction and eigensystem summary.

It is an infrastructure/development baseline only. It does not activate a cosmological claim or a scientific acceptance threshold.

The raw development arrays remain in the GitHub Actions artifact. The durable generic summary and metadata at persistence commit `0603f4...` are copied into this baseline directory so later smoke variants cannot erase the record.
