# Dark Sector Stability Architecture

**Status:** Stage A null-model reconstruction  
**Branch:** `dark-sector-stability-architecture`  
**Scientific rule:** foundations first; no new dark-fluid model before the ΛCDM null architecture is reconstructed.

## Foundation stack

### Published SymC anchor
The Scientific Reports paper *Exceptional-point stability boundaries from quantum dissipation to cosmological acceleration* is the program anchor. Only its scope-limited published results are inherited:

- the ordinary positive-curvature second-order damping coordinate (chi=gamma/(2omega)) and its (chi=1) repeated-root boundary;
- the flat-(Lambda)CDM synchronization (chi_delta=1 Longleftrightarrow q=0);
- the extension-offset prediction (Delta z=z_{q=0}-z_{chi_delta=1});
- the interpretation of the cosmological identity as a structural reformulation within the assumed model, not a new gravitational law.

The project does not inherit substrate inheritance as established mechanism, a universal scalar (chi), or the old mechanical-EP reading of the native negative-curvature density-growth equation.

### External foundations
- **Kunz:** dark degeneracy; gravity constrains total dark-sector stress-energy rather than a unique DM/DE split.
- **Nadkarni-Ghosh & Refregier:** first-order non-autonomous Einstein-Boltzmann generator and (k)-(a) spectral mapping.
- **Battye, Moss & Pearson:** coupled matter/DE normal modes, scale/time-dependent eigenstructure, and observable projections.
- **Kou & Lewis; Jiménez et al.; Hashim & El-Zant; Pérez et al.:** strongest current unified-dark-sector comparators.
- **You, Cai & Yang:** expansion-plus-growth degeneracy breaking and explicit (Lambda)CDM null testing.

## Research question

> Does the total dark sector possess a gauge-robust dynamical architecture whose evolving modal content naturally reproduces the two observational roles conventionally labeled dark matter and dark energy: clustering/structure support and accelerated-expansion/growth suppression?

The answer is not assumed to be yes.

## Competing hypotheses

### H0
Standard two-component (Lambda)CDM is sufficient. Any apparent complementarity is simply the standard model written in modal language.

### H1
A single conserved dark-sector architecture supports distinct modes/regimes whose observable functions become DM-like and DE-like.

### H2
Two distinguishable dark-sector modes exist inside one internally coupled conserved architecture; the usual split is an effective basis, not necessarily the unique ontology.

## Stage A

No new unified-dark-sector Lagrangian is introduced.

1. Build the scalar perturbation system using gauge-invariant variables wherever possible.
2. Derive
   [
   rac{dmathbf X}{dln a}=mathbf A(k,a)mathbf X.
   ]
3. Audit time-dependent basis/gauge transformations:
   [
   mathbf A_Y=mathbf Smathbf A_Xmathbf S^{-1}
   +rac{dmathbf S}{dln a}mathbf S^{-1}.
   ]
   Instantaneous eigenvalues are not automatically physical invariants.
4. Map over a preregistered ((k,a)) domain:
   - eigenvalue trajectories;
   - spectral gaps;
   - real/complex transitions;
   - modal participation/eigenvector rotation;
   - non-normality;
   - adiabaticity;
   - projections onto growth, lensing, and metric potentials.
5. Mark the published (q=0)/(chi_delta=1) epoch without treating it as a native generator EP.
6. Test whether any independent gauge-robust spectral/modal reorganization occurs near that epoch.

## Stage A falsifier

If no gauge-robust spectral or modal feature occurs near the acceleration transition beyond the known background change, the stronger dark-sector architecture hypothesis is not supported by ordinary (Lambda)CDM. Preserve that as a negative result.

## Novelty ceiling

Do not claim first dark-sector unification, first unified fluid, first eigenmode analysis, first stability analysis, first (k)-(a) spectral map, or first joint expansion-growth test.

The novelty target is the integration of total-dark-sector ontology neutrality, gauge-robust generator-first spectral reconstruction, an emergence test for DM-like versus DE-like functions, joint local-modal (chi)/broader (Chi) interpretation where licensed, and observational falsification with (Lambda)CDM retained as a null.

## First computational deliverable

A reproducible Stage A implementation that reconstructs the standard (Lambda)CDM perturbation generator, validates it against known growth solutions, and produces the first gauge-robust (k)-(a) modal map.
