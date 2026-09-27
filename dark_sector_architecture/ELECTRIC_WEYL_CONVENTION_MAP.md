# Electric-Weyl Convention Map

**Project:** Cosmic Stability Architecture  
**Stage:** P0-Q modal representation qualification  
**Status:** CONVENTION FROZEN FOR IMPLEMENTATION / FULL REPRESENTATION NOT YET QUALIFIED  
**Date:** 2026-09-27

## Purpose

Freeze one explicit curvature, metric, observer, time, and normalization
convention before any gevolution vector or tensor output is combined with the
already-qualified scalar-Weyl shape.

This document freezes the representation convention. It does not activate
PREG-MODAL-PA-1 and does not claim that the full electric-Weyl reconstruction
is numerically qualified.

## 1. gevolution metric and native variables

The gevolution Poisson-gauge metric is

\[
ds^2=a^2(\tau)\left[
-(1+2\Psi)d\tau^2
-2B_i dx^i d\tau
+\left((1-2\Phi)\delta_{ij}+h_{ij}\right)dx^i dx^j
\right],
\]

with

\[
\partial_i B^i=0,\qquad
h^i{}_i=0,\qquad
\partial^j h_{ij}=0.
\]

gevolution defines

\[
\chi_{\rm gev}\equiv \Phi-\Psi,
\qquad
\Psi=\Phi-\chi_{\rm gev}.
\]

Therefore the scalar Weyl/lensing potential is

\[
W\equiv\frac{\Phi+\Psi}{2}
=\Phi-\frac{\chi_{\rm gev}}{2}.
\]

The label \(\chi_{\rm gev}\) is always retained. It is not SymC lower-case
\(\chi\).

Primary source:
Adamek J, Daverio D, Durrer R, Kunz M,
*gevolution: a cosmological N-body code based on General Relativity*,
JCAP 2016(07)053,
DOI: 10.1088/1475-7516/2016/07/053.

## 2. Project curvature sign convention

For this qualification program, define

\[
R^\rho{}_{\sigma\mu\nu}
=
\partial_\mu\Gamma^\rho_{\nu\sigma}
-\partial_\nu\Gamma^\rho_{\mu\sigma}
+\Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma}
-\Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}.
\]

The electric Weyl tensor relative to a timelike unit vector \(u^\mu\) is

\[
E_{\mu\nu}
=
C_{\mu\alpha\nu\beta}u^\alpha u^\beta.
\]

This convention is frozen so that an overall curvature-sign difference between
references cannot silently reverse the ordered modal spectrum.

Vitenti, Falciano, and Pinto-Neto use the opposite displayed sign for the
first-order scalar electric-Weyl expression. Their result is used as a
structural cross-check, with the sign-convention difference recorded rather
than mixed into the implementation.

Reference:
Vitenti SDP, Falciano FT, Pinto-Neto N,
*Covariant Bardeen Perturbation Formalism*,
Phys. Rev. D 89, 103538 (2014),
DOI: 10.1103/PhysRevD.89.103538.

## 3. Observer convention

The first-order representation is evaluated relative to the FLRW background
comoving normal

\[
u^\mu_{(0)}=a^{-1}(1,0,0,0).
\]

The FLRW background Weyl tensor vanishes. Consequently, changing the observer
by a first-order velocity perturbation changes the electric Weyl tensor only at
second order. The first-order object used here is therefore not made observer
dependent by an arbitrary first-order peculiar velocity choice.

This does not license an observer-independent nonlinear electric-Weyl claim.

## 4. Direct first-order derivation from the gevolution metric

Strip the common conformal factor and define

\[
\widetilde g_{\mu\nu}=a^{-2}g_{\mu\nu}.
\]

Because the Weyl tensor with one index raised is conformally invariant, the
first-order conformal-coordinate electric-Weyl shape can be derived directly
from \(\widetilde g_{\mu\nu}\).

For the gevolution perturbations

\[
\delta\widetilde g_{00}=-2\Psi,\qquad
\delta\widetilde g_{0i}=-B_i,\qquad
\delta\widetilde g_{ij}=-2\Phi\delta_{ij}+h_{ij},
\]

the trace-free part of \(C_{i0j0}\) is

\[
\boxed{
\mathcal E^{\rm conf}_{ij}
=
D_{ij}W
-\frac12\partial_{(i}B'_{j)}
-\frac14\left(h''_{ij}+\nabla^2h_{ij}\right)
}
\]

where

\[
D_{ij}
\equiv
\partial_i\partial_j
-\frac13\delta_{ij}\nabla^2,
\]

prime denotes \(\partial/\partial\tau\), and

\[
\partial_{(i}B'_{j)}
\equiv
\frac12\left(\partial_iB'_j+\partial_jB'_i\right).
\]

Numerically, the complete sum is projected back to its symmetric trace-free
part before eigendecomposition. This catches finite-difference and interpolation
residuals without changing the analytic object.

## 5. Physical orthonormal normalization

The coordinate-index first-order object above is the convenient simulation
shape tensor. The physical orthonormal-frame electric Weyl tensor is

\[
\boxed{
E_{\hat i\hat j}
=
a^{-2}\mathcal E^{\rm conf}_{ij}
}
\]

at this order.

For one-epoch eigenframe comparisons the common positive \(a^{-2}\) factor does
not change eigenvectors. It must be included for physical eigenvalue comparisons
across epochs.

## 6. Required limit checks

### Scalar limit

Set

\[
B_i=0,\qquad h_{ij}=0.
\]

Then

\[
\mathcal E^{\rm conf}_{ij}
=
D_{ij}\frac{\Phi+\Psi}{2}.
\]

If gravitational slip is negligible, \(\Psi=\Phi\), so

\[
\mathcal E^{\rm conf}_{ij}=D_{ij}\Phi,
\]

which is the relativistic scalar tidal tensor in the project sign convention.

### Pure vector limit

Set scalar and tensor sectors to zero:

\[
\mathcal E^{(V)}_{ij}
=
-\frac12\partial_{(i}B'_{j)}.
\]

Because \(B_i\) is transverse, this term is analytically trace-free.

### Pure tensor limit

Set scalar and vector sectors to zero:

\[
\mathcal E^{(T)}_{ij}
=
-\frac14\left(h''_{ij}+\nabla^2h_{ij}\right).
\]

For a flat-background vacuum gravitational wave satisfying

\[
h''_{ij}-\nabla^2h_{ij}=0,
\]

this reduces to

\[
\mathcal E^{(T)}_{ij}
=
-\frac12h''_{ij},
\]

the standard tidal form in the frozen project convention.

## 7. Relation to the covariant perturbation literature

Vitenti et al. derive the first-order electric Weyl tensor from scalar, vector,
and tensor gauge-invariant variables. Their scalar sector is proportional to the
trace-free Hessian of \((\Phi+\Psi)/2\), while their vector and tensor sectors
contain first and second time derivatives. Their displayed overall electric
Weyl sign is opposite the project convention frozen above.

This agreement in sector content is the required literature cross-check:

- scalar: \(D_{ij}(\Phi+\Psi)/2\);
- vector: spatial derivative of a time-dependent transverse shift/shear mode;
- tensor: time and spatial second derivatives of the transverse-traceless mode.

The implementation is derived from the gevolution metric rather than by
copying coefficients across different time and tensor normalizations.

## 8. gevolution dynamics cross-check

gevolution's traceless spatial Einstein equation contains

\[
\frac12 h''_{ij}
+\mathcal H h'_{ij}
-\frac12\nabla^2h_{ij}
+B'_{(i,j)}
+2\mathcal H B_{(i,j)}
+\chi_{{\rm gev},ij}
+\cdots .
\]

Thus the vector and tensor sectors are genuinely dynamical and require temporal
information. A one-snapshot reconstruction cannot be promoted to the full
electric Weyl tensor.

## 9. Naming rule

The following names are now frozen.

### weak_field_tidal_tensor

\[
D_{ij}\Phi.
\]

Newtonian/negligible-slip scalar development object only.

### scalar_weyl_shape_tensor

\[
D_{ij}\left(\Phi-\chi_{\rm gev}/2\right).
\]

First-order scalar electric-Weyl spatial shape in the frozen project curvature
sign convention.

### electric_weyl_conformal_tensor

\[
D_{ij}W
-\frac12\partial_{(i}B'_j)
-\frac14(h''_{ij}+\nabla^2h_{ij}).
\]

Reserved for the complete first-order scalar+vector+tensor reconstruction after
temporal-derivative qualification.

### electric_weyl_physical_tensor

\[
a^{-2}E^{\rm conf}_{ij}.
\]

Reserved for cross-epoch physical eigenvalue comparisons after the scale-factor
and temporal reconstruction are qualified.

## 10. Refusal conditions

REFUSE full electric-Weyl interpretation if any of the following holds:

- \(B_i'\) cannot be reconstructed at the target epoch with demonstrated
  temporal convergence;
- \(h''_{ij}\) cannot be reconstructed with demonstrated temporal convergence;
- output epochs cannot be mapped to the required conformal times;
- vector transversality or tensor TT residuals are numerically uncontrolled;
- scalar, vector, and tensor fields cannot be put on the same physical grid;
- sign/normalization conventions are mixed across components;
- the full result is materially sensitive to the temporal stencil without an
  admissible uncertainty treatment.

## 11. Next qualification gate

1. implement the frozen algebra with derivative arrays supplied explicitly;
2. known-truth test scalar, pure-vector, pure-tensor, and mixed cases;
3. add five exact nearby output epochs around one frozen central epoch;
4. reconstruct \(B_i'\) and \(h_{ij}''\) using nested centered stencils;
5. compare the half-width and full-width derivative reconstructions;
6. only then apply the full tensor to real gevolution outputs;
7. quantify full-versus-scalar modal changes before any modal preregistration
   activation.

No scientific numerical threshold is frozen by this convention map.
