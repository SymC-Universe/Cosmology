# Stage A R1 Compatibility Map

Status: P0-D foundation conglomeration

The current residual closure problem is whether resolved cosmological structure and averaged geometry can be placed in one gauge-robust state description without converting geometrical bookkeeping into a new physical substance.

A provisional common state scaffold is

[
X_{mathcal D}(k,t)
=
left[
mathcal B_{mathcal D}(t),
mathcal P(k,t),
mathcal M(t)
ight],
]

with domain-level background/geometry

[
mathcal B_{mathcal D}
=
{
a_{mathcal D},
H_{mathcal D},
langleepsilonangle_{mathcal D},
langle pangle_{mathcal D},
Q_{mathcal D},
P_{mathcal D},
langlemathcal Rangle_{mathcal D}
},
]

resolved gauge-invariant/covariant perturbations (mathcal P(k,t)), and a history block (mathcal M) admitted only if non-Markovian closure is required by derivation.

The desired architecture has the schematic form

[
dot{mathcal B}_{mathcal D}
=
F_B
left(
mathcal B_{mathcal D},
mathcal C[mathcal P],
mathcal M
ight),
]

[
dot{mathcal P}
=
F_P
left(
k,
mathcal B_{mathcal D},
mathcal P
ight),
]

with an additional memory evolution or convolution only where licensed.

The unresolved object is the closure operator (mathcal C[mathcal P]): the map from resolved matter/radiation/metric structure into the averaged geometrical state. It must avoid double counting, gauge artifacts, and outcome-fitted effective-fluid assumptions.

## Compatibility results

- Standard Einstein-Boltzmann generators establish perturbation evolution on FLRW backgrounds, but cannot simply be reused unchanged on an averaged non-FLRW background.
- Buchert dust averaging gives (Q_{mathcal D})-curvature coupling but is insufficient for recombination-era physics.
- Perfect/general-fluid averaging admits pressure, radiation, vorticity, lapse/acceleration, and dynamical backreaction (P_{mathcal D}), but the resulting averaged system is explicitly unclosed.
- Averaged-background perturbation work supplies the background-to-perturbation direction but does not yet close the perturbation-to-background return path at the same approximation order.
- Mori-Zwanzig projection proves that history-dependent closure is formally possible, but does not establish a physical SymC inheritance carrier.
- Radiation-inclusive lattice backreaction shows radiation can be incorporated and tends to reduce backreaction, but it retains conventional cold matter and does not solve the no-dark-substance CMB problem.

## R1 residual

The first preregisterable residual target is:

> Derive or identify a covariant/gauge-robust closure operator that maps resolved matter/radiation/metric structure into the averaged geometrical state while the averaged state governs subsequent perturbation evolution, and show that the resulting loop is mathematically well posed before asking whether it carries DM-like or DE-like phenomenology.

## Current claim ceiling

A cosmological architecture scaffold is supported. Opposite-sign shear and expansion-variance roles are supported within averaged-GR models. Formal history dependence is supported under coarse graining.

A complete feedback closure, SymC inheritance, or replacement of dark matter/dark energy is not established. The architecture has also not yet met the early CMB burden.

The remaining Stage A task is to determine whether an existing covariant closure or projection formalism already supplies the missing (mathcal C[mathcal P]). If not, that missing closure becomes the Stage B derivation target.
