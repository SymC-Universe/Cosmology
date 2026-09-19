# SymC Cosmology - Current Scientific Status

**Current research notice: 19 September 2026**

This repository preserves historical SymC cosmology and cross-scale stability work. Its older landing text and manuscripts were written before the current generator-first domain-licensing rules in SymC GOM v0.8.0 were established.

The repository is therefore **under scientific reconstruction**. Historical files remain public for provenance, but broader claims in them are not automatically current claims.

## Current domain-licensing rule

A normalized ratio may be useful without being a mechanical damping ratio.

For an ordinary passive positive-curvature second-order mode,

```math
\ddot q + \gamma \dot q + \Omega^2 q = 0
```

the conventional damping ratio

```math
\chi = \frac{\gamma}{2\Omega}
```

has a true repeated-root boundary at `chi = 1`.

That interpretation does **not** transfer automatically to equations with negative curvature, growth terms, first-order relaxation, spectral widths, or open-system generators of a different form.

## Cosmological density growth

The flat-Lambda-CDM density-growth equation can be written schematically as

```math
\ddot\delta + 2H\dot\delta - 4\pi G\rho_m\delta = 0.
```

Its characteristic discriminant is

```math
\Delta = 4H^2 + 16\pi G\rho_m,
```

which is positive for positive `H` and `rho_m`. The ordinary critical-damping repeated-root construction therefore does not occur in this growth equation.

A normalized balance coordinate may still satisfy a relation equivalent to `q = 0` in flat Lambda-CDM. Under the current framework that relation is treated as a **balance/kinematic synchronization**, not by itself as a mechanical critical-damping EP of the density-growth generator.

## Open-quantum-system caution

Historical derivations that rewrite simple amplitude-damped oscillator first moments into an approximate second-order form must preserve the approximation regime. An exceptional-point claim requires coalescence and defectiveness of the relevant full generator, not merely a scalar rewriting or an extrapolation of a weak-damping approximation to a non-weak-damping boundary.

## Current claim ceiling

This repository does not presently treat the following as established merely because they appeared in an earlier manuscript:

- one universal scalar chi across cosmology, quantum dynamics, particles, biology, or other domains;
- a cosmological density-growth EP at the ordinary mechanical chi=1 boundary;
- a universal information-efficiency maximum at chi=1;
- particle-width ratios as mechanical damping ratios without a licensed generator;
- cross-scale recurrence as proof of one physical mechanism;
- substrate inheritance as established merely from mathematical resemblance.

Historical PDFs and TeX sources remain valuable for derivations, hypotheses, and provenance. They must be reclassified claim by claim before reuse in a new release.

## Relationship to current Foundations

The current SymC Foundations program is generator-first and explicitly separates:

- positive-curvature mechanical damping;
- negative-curvature/barrier coordinates;
- cosmological balance coordinates;
- particle spectral-width ratios;
- non-Markovian pole conditions;
- full-generator exceptional-point evidence.

Future cosmology work should inherit those distinctions rather than preserve a broad universal-chi narrative.

## Repository status

`main` is currently an archival/public research branch, not a GOM-v0.8.0-complete rebuilt cosmology program.

A new release should not be prepared until the current manuscript, supplemental derivations, figures, and claim map have been re-audited under the present generator-first rules. Negative or narrowed conclusions are valid outcomes of that reconstruction.
