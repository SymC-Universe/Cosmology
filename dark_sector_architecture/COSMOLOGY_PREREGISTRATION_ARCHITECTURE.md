# Cosmology Preregistration Architecture

**Project:** Cosmic Stability Architecture  
**Status:** Working protocol to be frozen before controlled literature adjudication and before any P1 confirmation  
**GOM basis:** v0.8.7

## Purpose

The cosmology project uses two distinct preregistration layers.

The first freezes how existing literature will be adjudicated. The second freezes only the residual scientific claims that remain after the literature has been conglomerated and adjudicated.

The literature stage does not confirm claims about nature. It determines what is already established, contradicted, unresolved, or unavailable and prevents known prior work from being rediscovered as if novel.

## Preregistration sequence

[
	ext{PREG-LIT}
ightarrow
	ext{controlled literature adjudication}
ightarrow
	ext{residual claim set}
ightarrow
	ext{PREG-S/M/C/J}
ightarrow
	ext{untouched P1 confirmation}.
]

### PREG-LIT: literature adjudication preregistration

Scientific status: **P0-Q / controlled foundation qualification**, not empirical confirmation.

Freeze before applying the adjudication rules to the remaining/unseen literature corpus:

- exact cosmology hypothesis and scope;
- no-dark-substance/no-new-force ontology constraint;
- scalar, vector/modal, conglomerate/system, and joint-meaning questions;
- inclusion/exclusion rules for papers and claim components;
- evidence classes;
- compatibility tests;
- admission/refusal/indeterminate rules;
- shared-premise/common-source rules;
- search boundaries and stopping conditions;
- extraction schema;
- residual-question rule.

Previously viewed literature remains discovery/foundation material. Freezing PREG-LIT does not retroactively convert it into untouched evidence.

### PREG-S: scalar claim preregistration

Used only for a material scalar claim.

A scalar object must retain its native name unless it qualifies as lower-case (chi) under the GOM licensing rules.

Each activated PREG-S record receives its own complete MFR-14.

### PREG-M: modal/vector claim preregistration

Used for a modal, eigenspace, subspace, transfer, participation, or mode-function claim.

Each activated PREG-M record receives its own complete MFR-14.

A modal claim can survive or fail independently of scalar or conglomerate claims.

### PREG-C: conglomerate/system claim preregistration

Used for a claim about coupled organization, feedback, multiscale closure, emergent collective behavior, or system architecture.

Each activated PREG-C record receives its own complete MFR-14.

A conglomerate claim cannot inherit a PASS merely because scalar or modal components look favorable.

### PREG-J: joint-meaning / inheritance claim preregistration

Used when the claim concerns the relationship among scalar, modal, and conglomerate layers, including inheritance across epochs.

Each activated PREG-J record receives its own complete MFR-14.

The joint claim must specify what information is preserved, transformed, lost, or newly created across the mapping.

## Claim-family structure

The current cosmology confirmatory family is expected to contain at least four separately adjudicated layers:

| Claim family | Question |
|---|---|
| S | What scalar/local quantities are licensed and what do they retain or lose? |
| M | What modal/subspace organization exists and what functions do its modes carry? |
| C | What coupled/conglomerate organization emerges from the full system? |
| J | What do S, M, and C mean together, especially across inheritance and feedback? |

Additional layers may be added only as post-result discoveries under the GOM and cannot retroactively absorb a failure.

## Minimum MFR-14 implementation

Every activated P1 scientific claim will contain all fourteen fields separately.

### MFR-01 Frozen claim
- claim_id;
- exact claim text;
- scope;
- frozen task;
- value axis if applicable;
- version.

### MFR-02 Provenance
One or more of:
- DOMAIN_THEORY;
- EXTERNAL_THEORY;
- FRAMEWORK_DERIVED;
- DATA_DERIVED;
- CROSS_DOMAIN_TRANSFER.

### MFR-03 Target native object
Specify the exact measurable or formal object capable of contradicting the claim.

### MFR-04 Representation and validity regime
Specify native model, reduction, conditions, exclusions, units/conventions, and refusal conditions.

### MFR-05 Strongest native comparator
Freeze the strongest fair comparator for the same question, or record NO_NATIVE_COMPARATOR with the search record.

### MFR-06 Null/competing explanation
At least one competing explanation capable of producing the result if the SymC interpretation is wrong.

### MFR-07 Expected response
Freeze the expected direction, class, ordering, trajectory, invariance, transition, or other response.

### MFR-08 Decision rule
Freeze the categorical, interval, numerical, ordinal, or blinded adjudication rule.

### MFR-09 Uncertainty / tolerance / indeterminate zone
Define uncertainty and the conditions producing INDETERMINATE.

### MFR-10 Independence / leakage map
Record shared data, labels, source tables, simulations, fitted parameters, thresholds, literature, or outcome construction.

### MFR-11 Multiplicity / search space
Freeze the family of modes, endpoints, scales, windows, models, thresholds, or subgroups that can affect the claim.

### MFR-12 Freeze identity and decisive test
Record commit/hash/timestamp, model version, and untouched test.

### MFR-13 Explicit falsifier
State what result counts against the claim.

### MFR-14 Failure consequence
State in advance whether failure:
- falsifies;
- narrows;
- retires the representation in-regime;
- returns NO_ADDED_SYMC_VALUE;
- returns DOMAIN_LIMITED;
- or blocks promotion.

## Cosmology-specific additions

Every activated cosmology preregistration additionally records:

- epoch/domain: primordial, radiation, equality, recombination, matter, nonlinear structure, acceleration;
- scale domain in (k) and/or physical scale;
- gauge/covariant representation;
- cosmological SVT sector where relevant;
- SymC layer: scalar, modal/vector, conglomerate/system, joint;
- transfer/inheritance map if relevant;
- whether a quantity is a physical mode, constrained response, correlation term, effective rewriting, or system-level function;
- relation to CMB, lensing, growth, BAO, BBN, galaxies, clusters, or distances;
- whether CDM and/or (Lambda) are included in the native comparator;
- whether an effective-fluid rewrite is only bookkeeping or is being granted physical ontology;
- Function Map target;
- Limit Map target;
- refusal conditions.

## Frozen interpretation rule

No confirmatory outcome may be summarized as a full-system success unless the specific system-level claim passed its own gate.

Examples:

[
	ext{scalar support} + 	ext{modal support} + 	ext{failed conglomerate gate}

eq
	ext{full architecture support}.
]

Likewise,

[
	ext{inheritance carrier found}

eq
	ext{dark-sector function established}.
]

## Activation rule

The schema may be frozen now.

The exact S/M/C/J claim texts are frozen only after PREG-LIT adjudication identifies the irreducible residual questions. This prevents premature preregistration of a claim that the literature already settles or makes incoherent.

## Current preregistration status

- PREG-LIT schema: READY TO FREEZE.
- PREG-S: schema defined, claim not yet activated.
- PREG-M: schema defined, claim not yet activated.
- PREG-C: schema defined, claim not yet activated.
- PREG-J: schema defined, claim not yet activated.

The next action after freezing PREG-LIT is controlled adjudication of the literature corpus under the companion protocol.
