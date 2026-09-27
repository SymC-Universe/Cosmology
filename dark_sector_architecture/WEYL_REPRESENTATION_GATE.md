# Electric-Weyl Representation Gate

**Project:** Cosmic Stability Architecture  
**Stage:** P0-Q representation qualification  
**Status:** OPEN  
**Updated:** 2026-09-27

## Purpose

Determine what tensor object can be reconstructed defensibly from gevolution
outputs and prevent the current scalar weak-field tidal Hessian from being
silently relabeled as the full electric part of the Weyl tensor.

This gate is independent of the numerical resolution ladder.

A numerically converged scalar Hessian does not, by itself, establish a
numerically converged electric-Weyl tensor.

## Native gevolution metric

Adamek et al. use Poisson gauge

[
ds^2=a^2(	au)left[
-(1+2Psi)d	au^2
-2B_i dx^i d	au
+(1-2Phi)delta_{ij}dx^i dx^j
+h_{ij}dx^i dx^j
ight],
]

with

[
partial_iB^i=0,qquad
h^i{}_i=0,qquad
partial^jh_{ij}=0.
]

gevolution defines the gravitational slip variable

[
chi_{m gev}equivPhi-Psi.
]

This symbol is gevolution's native variable and must never be confused with
SymC scalar chi.

Reference:
Adamek J, Daverio D, Durrer R, Kunz M.
*gevolution: a cosmological N-body code based on General Relativity*.
JCAP 2016(07)053.
DOI: 10.1088/1475-7516/2016/07/053.
arXiv:1604.06065.

## Scalar electric-Weyl sector

At first order about FLRW, the scalar electric Weyl tensor is the
symmetric trace-free Hessian of the Weyl/lensing potential,

[
E^{(S)}_{ij}
propto
left(
partial_ipartial_j
-rac13delta_{ij}
abla^2
ight)
rac{Phi+Psi}{2},
]

up to the chosen physical/conformal index normalization and Weyl sign
convention.

Using gevolution's native slip,

[
rac{Phi+Psi}{2}
=
Phi-rac{chi_{m gev}}{2}.
]

Therefore the current development tensor

[
T^{m dev}_{ij}
=
operatorname{STF}left[partial_ipartial_jPhiight]
]

is the scalar electric-Weyl shape only in the negligible-slip limit.

The immediate scalar correction is prospectively

[
T^{(S)}_{ij}
=
operatorname{STF}
left[
partial_ipartial_j
left(Phi-rac{chi_{m gev}}2ight)
ight].
]

The overall (a^{-2}) physical normalization is irrelevant for
eigenvectors at one epoch but is required before comparing physical
eigenvalue magnitudes across epochs.

Supporting references:
- Vitenti SDP, Falciano FT, Pinto-Neto N.
  *Covariant Bardeen Perturbation Formalism*.
  Phys. Rev. D 89, 103538 (2014).
  DOI: 10.1103/PhysRevD.89.103538.
  arXiv:1311.6730.
- Ip HY, Schmidt F.
  *Large-Scale Tides in General Relativity*.
  JCAP 2017(02)025.
  DOI: 10.1088/1475-7516/2017/02/025.
  arXiv:1610.01059.
- Ehlers J, Buchert T.
  *On the Newtonian limit of the Weyl tensor*.
  Gen. Rel. Grav. 41, 2153-2158 (2009).
  DOI: 10.1007/s10714-009-0855-1.
  arXiv:0907.2645.

## Why one snapshot is not enough for the full tensor

Vitenti et al. give the first-order decomposition

[
E_{mu
u}
=
-rac12left(T_{mu
u}+J_{mu
u}ight).
]

For flat FLRW, their vector/tensor terms contain, schematically,

[
D_{(i}S_{j)},qquad
D_{(i}dot S_{j)},qquad
D^2W_{ij},qquad
dot W_{ij},qquad
ddot W_{ij},
]

in addition to the scalar trace-free Hessian.

In Poisson gauge these gauge-invariant vector/tensor degrees map to the
shift/frame-dragging sector and the transverse-traceless spatial metric
sector, subject to convention and scale-factor mapping that must be frozen
explicitly before implementation.

Consequently, a single gevolution snapshot containing

[
{Phi,chi_{m gev},B_i,h_{ij}}
]

does not by itself supply all temporal derivative information required by
the general first-order electric-Weyl reconstruction.

This is a representation limitation, not a negative scientific result.

## Multi-snapshot qualification requirement

Before any object is labeled full electric Weyl:

1. freeze the exact convention map between gevolution
   ({Phi,Psi,B_i,h_{ij}}) and the covariant perturbation variables;
2. output at least three closely spaced snapshots at matched epochs;
3. reconstruct (chi_{m gev}), (B_i), and (h_{ij}) on identical grids;
4. use centered finite differences for first derivatives and a controlled
   second-derivative stencil where required;
5. repeat with at least two temporal spacings;
6. verify derivative convergence;
7. compare the scalar-only object to the scalar+vector+tensor object;
8. preserve the magnetic Weyl sector as a diagnostic rather than assuming
   it vanishes outside the Newtonian/scalar limit;
9. verify symmetry, trace-free character, transversality constraints where
   applicable, and coordinate-rotation covariance;
10. only then assess whether full-Weyl eigenstructure is stable enough for a
    modal claim.

## Immediate development objects

Three labels are now required:

### 1. `weak_field_tidal_tensor`

Current legacy development object

[
operatorname{STF}[partial_ipartial_jPhi].
]

Interpretation:
Newtonian/negligible-slip scalar tidal approximation only.

### 2. `scalar_weyl_shape_tensor`

Next qualified scalar object

[
operatorname{STF}
left[
partial_ipartial_j
left(Phi-chi_{m gev}/2ight)
ight].
]

Interpretation:
first-order scalar electric-Weyl spatial shape, before physical (a^{-2})
normalization.

### 3. `electric_weyl_tensor`

Reserved name.

It may not be used until the full scalar+vector+tensor reconstruction,
observer/foliation convention, temporal derivatives, and normalization are
qualified.

## Claim consequence

PREG-MODAL-PA-1 remains **CANDIDATE / NOT ACTIVATED** even if the current
scalar tidal representation converges numerically.

Activation requires both:

- admissible numerical resolution/convergence; and
- an explicitly licensed tensor representation for the intended claim.

## Next exact actions

1. add and known-truth-test `scalar_weyl_shape_tensor(phi, chi_gev)`;
2. quantify the slip correction on a real gevolution development output;
3. complete the N32-N64 scalar-tidal resolution rung;
4. design a three-snapshot temporal derivative pilot;
5. map the vector/tensor convention exactly before coding the full
   electric-Weyl expression.
