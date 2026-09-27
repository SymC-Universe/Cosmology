# Cosmology Literature Adjudication Protocol

**Project:** Cosmic Stability Architecture  
**Protocol ID:** PREG-LIT  
**Status:** Working protocol to be frozen before controlled adjudication

## Governing principle

The unit of adjudication is a **paper-specific claim component**, not an entire paper and not whether the paper agrees with the SymC hypothesis.

Supportive and contradictory evidence are equally eligible for admission.

The protocol governs whether a claim component may enter the **current qualified foundation and promotion path**. It does not determine what may be explored.

## Frozen literature questions

Each admitted result is tested against one or more of the following questions:

1. **Scalar:** What native scalar/local quantities are established, under what conditions, and what information do they retain or destroy?
2. **Modal:** What modes, subspaces, transfer structures, participation patterns, or reorganizations are established?
3. **Conglomerate:** What coupled, feedback, correlation, multiscale, or system-level organization is established?
4. **Joint meaning:** What relationships among scalar, modal, and conglomerate representations are established, contradicted, or unresolved?
5. **Inheritance:** What structure is demonstrably carried, transformed, lost, or created across cosmic transitions?
6. **Functional dark-sector burden:** What DM-like or DE-like observational function is actually reproduced, on what scales and epochs, and with what assumptions?

## Adjudication outputs

The primary operational statuses are:

### ADMITTED
The claim component is sufficiently specified, relevant, and supported to enter the foundation conglomeration at its earned epistemic level.

Admission does not mean the claim is true universally or supports SymC.

### PARTIAL_ADMISSION
A narrower portion is admissible, but the broader interpretation is not.

The admitted subclaim and refused extension must be written separately.

### COUNTEREVIDENCE_ADMITTED
The result is sufficiently supported and materially conflicts with, limits, or falsifies part of the working hypothesis.

Counterevidence is a first-class foundation object, not a failed literature hit.

### INDETERMINATE_NEED_MORE_INFO
The component is relevant but cannot yet be adjudicated because a material item is missing.

Required reason codes include one or more of:
- FULL_TEXT_NEEDED;
- EQUATION_CONTEXT_NEEDED;
- PARAMETER_OR_REGIME_UNCLEAR;
- GAUGE_OR_CONVENTION_UNCLEAR;
- DATA_PROVENANCE_UNCLEAR;
- MODEL_DEPENDENCY_UNCLEAR;
- UNCERTAINTY_UNCLEAR;
- SOURCE_CONFLICT;
- REPLICATION_OR_INDEPENDENCE_UNCLEAR.

This is the operational "need more info" state. Canonically it maps to GOM `INDETERMINATE`.

### REFUSED
The proposed interpretation is not admissible for the frozen question.

Refusal reason codes include:
- MODEL_NOT_APPLICABLE;
- WRONG_EPOCH_OR_SCALE;
- UNSUPPORTED_EXTRAPOLATION;
- NO_ADMISSIBLE_MODAL_OBJECT;
- NO_CONGLOMERATE_OBJECT;
- SCALAR_REDUCTION_NOT_LICENSED;
- GAUGE_OR_SLICING_ARTIFACT_RISK;
- EFFECTIVE_REWRITE_ONLY;
- ONTOLOGY_MISMATCH;
- CIRCULAR_WITH_TARGET_CLAIM;
- EVIDENCE_TOO_WEAK;
- CLAIM_EXCEEDS_SOURCE;
- INCOMPATIBLE_FOUNDATION_ASSUMPTIONS.

Refusal applies to the interpretation or use, not to the existence of the paper.

A refusal never means "do not investigate further." It means only that the proposed use is not admissible for the frozen question under the current evidence and representation.

Every refused record may carry an independent exploration disposition:
- `NO_FOLLOWUP_REQUIRED`;
- `P0D_OPEN`;
- `POST_RESULT_DISCOVERY`;
- `NEW_COMPONENT_CANDIDATE`;
- `ALTERNATIVE_REPRESENTATION_CANDIDATE`;
- `NATIVE_MODEL_REVIEW`;
- `QUALIFICATION_NEEDED`.

The exploration disposition does not change the refusal status.

### NOT_APPLICABLE
The paper may be scientifically sound but does not bear on the frozen question or layer.

## Mandatory extraction record

Every literature claim component receives:

- literature_record_id;
- cite key / DOI / stable identifier;
- exact result/equation/finding;
- source location;
- scientific layer: scalar / modal / conglomerate / joint / inheritance / functional burden;
- native model;
- matter/energy content;
- epoch;
- scale;
- gauge/foliation/covariant status;
- evidence class: mathematical / simulation / observational / inferential / review / speculative;
- assumptions;
- uncertainty/tolerance if available;
- what is established;
- what is not established;
- compatibility dependencies;
- competing interpretation;
- shared-data/shared-premise risks;
- adjudication status;
- reason code;
- information needed if indeterminate;
- downstream claim(s) affected;
- exploration_disposition;
- exploratory question generated, if any;
- post-result/promotion-debt status where applicable.

## Admission gates

A component may be ADMITTED only when all applicable gates pass:

1. **Identity gate:** the exact object/result is identifiable.
2. **Relevance gate:** it bears directly on a frozen literature question.
3. **Native-model gate:** the result is interpreted within the model that generated it.
4. **Regime gate:** epoch, scale, matter content, and validity regime are specified.
5. **Representation gate:** scalar/modal/conglomerate classification is actually licensed.
6. **Provenance gate:** the evidence route/source is identifiable.
7. **Claim-ceiling gate:** the proposed use does not exceed what the source establishes.
8. **Compatibility gate:** combining it with another foundation does not silently change either model's assumptions.
9. **Independence gate:** shared evidence or common premises are visible and not misrepresented as independent confirmation.
10. **Friction gate:** a serious contrary interpretation is preserved where one exists.

Failure of a required gate yields REFUSED or INDETERMINATE, not forced admission.

Gate failure restricts qualification only. It may simultaneously generate a P0-D question about why the gate failed, whether another representation is required, whether a boundary has been found, or whether an additional architecture component exists.

## Need-more-info test

A record enters INDETERMINATE_NEED_MORE_INFO only if the missing information could plausibly change admission status.

The record must state:

[
	ext{missing information}
ightarrow
	ext{specific resolving action}
ightarrow
	ext{possible status change}.
]

If no obtainable information could make the interpretation admissible, use REFUSED instead of NEED_MORE_INFO.

If the question does not apply, use NOT_APPLICABLE.

## Partial-admission rule

A source may support one layer and fail another.

Examples:

- scalar result ADMITTED;
- modal interpretation INDETERMINATE;
- conglomerate mechanism REFUSED.

No averaging of validity is permitted.

## Contradiction rule

A credible result that contradicts the hypothesis is never REFUSED merely for contradiction.

Use COUNTEREVIDENCE_ADMITTED and map the affected residual claim.

If two admitted foundations conflict, both remain admitted and the relationship receives:

`CONFLICTING_FOUNDATIONS`

until a discriminating test resolves them.

## Conglomeration rule

Only admitted components may enter the literature-native architecture.

Connections between admitted components receive one of:

- EXPLICITLY_ESTABLISHED;
- ALGEBRAICALLY_IMPLIED;
- MODEL_CONDITIONAL;
- SYNTHESIS_DERIVED;
- CONFLICTING;
- UNRESOLVED;
- INCOMPATIBLE.

A SYNTHESIS_DERIVED connection is a new hypothesis candidate, not an established literature fact.

## Exploration-preservation rule

Controlled adjudication and open exploration are intentionally asymmetric.

The P0-Q literature pass asks whether the current evidence is admissible for a frozen question. P0-D is allowed to ask new questions that arise from any outcome, including refusal, contradiction, anomaly, or failed reduction.

A new exploratory branch:
- must preserve the original adjudication outcome;
- must state the trigger that opened the branch;
- is labeled post-result when generated after inspecting the relevant result;
- may introduce a new representation or architecture component when native science supports doing so;
- cannot be counted as evidence that the original frozen claim survived.

This ensures that the gate on **promotion** can close while the gate on **exploration** remains open.

## Stop rule for the controlled Stage A literature adjudication lane

Stop expanding the literature corpus when all three conditions hold:

1. every active residual question has at least one admitted foundation and one serious comparator/counterevidence route where such literature exists;
2. two successive bounded search passes add no new claim class, mechanism class, or material contradiction;
3. remaining NEED_MORE_INFO records cannot plausibly change the residual claim family without new primary evidence.

The stopping condition is about saturation of the **current controlled adjudication question**, not a fixed paper count and not closure of the scientific architecture.

Meeting the stop rule ends that P0-Q pass only. It does not:
- prohibit new literature searches;
- prohibit revisiting refused or indeterminate records;
- prohibit new scalar/modal/conglomerate/additional components;
- declare the field saturated permanently;
- or prevent a new PREG-LIT version when a scientifically material discovery changes the residual-question architecture.

Literature found after the controlled stop enters P0-D first. If it materially changes the qualified residual question, a new controlled adjudication version is frozen rather than silently editing the completed one.

## Residual-question output

After adjudication, classify every material working statement as:

- ALREADY_ESTABLISHED;
- PARTIALLY_ESTABLISHED;
- COUNTEREVIDENCE_PRESENT;
- CONFLICTING_FOUNDATIONS;
- SUPPORTED_ONLY_WITH_ADDITIONAL_ASSUMPTION;
- CONTRADICTED_IN_TESTED_REGIME;
- INDETERMINATE;
- UNRESOLVED;
- NOT_APPLICABLE.

Only UNRESOLVED or properly scoped synthesis-derived relationships from the controlled lane can become immediate new PREG-S, PREG-M, PREG-C, or PREG-J claim candidates.

Any adjudication outcome, including REFUSED, COUNTEREVIDENCE_ADMITTED, INDETERMINATE, or NOT_APPLICABLE, may still generate a separate P0-D exploratory hypothesis. Such a hypothesis must enter through its own provenance and promotion path and cannot inherit confirmatory status from the record that generated it.

## Literature adjudication is not confirmation

A literature component used to formulate a residual prediction cannot later be counted as untouched confirmation of that same prediction.

The literature protocol determines:
- prior art;
- foundation admissibility;
- claim ceiling;
- conflicts;
- and residual questions.

Confirmation about nature requires a separately frozen P1 test under MFR-14.
