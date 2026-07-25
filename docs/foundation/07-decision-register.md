# Foundation Decision Register

## Purpose

This register separates accepted constraints from provisional assumptions and future decisions. Implementation must not silently decide semantic questions.

## Decision states

- `accepted` — binding for the stated contract version until explicitly revised;
- `provisional` — usable but still requires calibration or broader evidence;
- `open` — unresolved for a future phase;
- `rejected` — considered and excluded for the stated reason;
- `superseded` — replaced with preserved history.

## Accepted decisions

### FND-001 — Foundation before feature development

Atlas defines and tests its knowledge foundation before expanding product features. Existing software remains experimental until later architecture gates justify it.

### FND-002 — Markdown is the authored source of truth

Databases, portable files, indexes, JSON, and interfaces are derived and reproducible.

### FND-003 — Claim-level provenance is required

Evidence supports, challenges, or contextualizes individually inspectable claims. Concept-level citations alone are insufficient.

### FND-004 — Draft is the default lifecycle state

New knowledge and generated transformations remain `draft` until required review types are completed.

### FND-005 — Local ownership is a core constraint

Authoritative content remains inspectable and exportable without a mandatory cloud account.

### FND-006 — Polyglot requires evidence

A language or process boundary requires a stable responsibility, baseline comparison, measurable advantage, versioned contract, and maintenance analysis.

### FND-007 — AI cannot grant authority

AI may assist draft transformation but cannot create reviewed status or replace source verification.

### FND-008 — No global truth score

Atlas preserves domain-appropriate uncertainty and written rationale rather than one universal credibility number.

### FND-009 — Initial contract is `atlas-content/0.1`

Authoring, derived-data, and application versions are separate. Contract changes follow `11-contract-versioning-and-migrations.md`.

### FND-010 — Multilingual authored knowledge with language-neutral structure

Canonical structural tokens remain English technical identifiers. Human-readable knowledge may use any declared language. Translations are separate entities sharing a `work` identity and require their own review.

### FND-011 — Claim atomicity is semantic, not sentence length

A claim is split when its clauses can differ in evidence, scope, confidence, lifecycle, contradiction, or revision.

### FND-012 — Argument is embedded structure in `0.1`

Arguments use structured premise, assumption, conclusion, alternative, and inference blocks. They are not canonical entities until fixtures demonstrate a need for independent identity and lifecycle.

### FND-013 — Evidence storage follows minimum-necessary provenance

Atlas stores source identity, precise locator, context, method, limitations, access class, and evidence role. It does not assume full-source redistribution.

### FND-014 — Quantitative evidence has lineage

Values include quantities, units, uncertainty or its absence, methods, transformations, inputs, and missing-data behavior where applicable.

### FND-015 — Review is revision-specific and role-specific

Review records exact entity revision, review types, reviewers, conflicts, findings, and unresolved issues. Reviewer disagreement remains visible.

### FND-016 — Three reference domains define the Phase 0 stress test

The canonical corpus tests empirical biology, formal feedback modeling, and socio-technical recommender governance. The slices are bounded ontology tests, not a general content-production program.

### FND-017 — Invalid fixtures are part of the contract

The validator reports specific deterministic structural and semantic diagnostics and never silently repairs authored meaning.

### FND-018 — Revision impact uses bounded automatic staleness

Material dependency changes may mark downstream items `possibly-stale` or `review-required`. Automation identifies candidates; human review determines semantic impact. Translation source-revision mismatch is demonstrated by fixture.

### FND-019 — Canonical entity set is sufficient for `0.1`

Source, evidence, claim, concept, relation, model, question, synthesis, and revision are sufficient for the three split canonical slices. Argument remains embedded. A future contract may add an entity only after fixtures show independent identity and lifecycle are necessary.

### FND-020 — Relation vocabulary is executable for `0.1`

`10-relation-vocabulary.md` is the single source of truth. The validator checks relation names, directions, entity pairs, duplicate edges, and missing targets.

### FND-021 — Language-specific IDs and shared work identity are accepted

Canonical entity IDs are language-specific. Equivalent language versions share a language-neutral `work` identifier. Alias, rename, collision, federation, and translation behavior are demonstrated by fixtures.

### FND-022 — Python is the minimum Phase 0 validator baseline

ADR-0001 selects Python 3.11+ with pinned PyYAML for contract verification. The validator is replaceable infrastructure and is not the future product runtime or semantic authority.

### FND-023 — Foundation acceptance is distinct from content review

Phase 0 accepts the versioned knowledge contract, governance, and executable fixture architecture. Phase 1 performs revision-specific independent review of reference content. Machine conformance cannot promote content from `draft`.

### FND-024 — Canonical files replace bundled slices as executable fixtures

The bundled vertical-slice documents remain historical drafting artifacts. Canonical validation uses one file per entity under `content/canonical/` and `content/translations/`.

## Provisional decisions

### FND-101 — Qualitative confidence vocabulary

**State:** provisional

`uncertain`, `plausible`, `well-supported`, and `strongly-supported` require rationale and scope. The fixtures demonstrate useful distinctions, but independent reviewer calibration remains a Phase 1 task.

### FND-102 — Independent learner and researcher as initial user

**State:** provisional

The foundation optimizes for inspectable personal or small-team knowledge. Institutional workflow requirements remain deferred.

## Superseded decisions

### FND-106 — Bundled vertical slices before canonical file split

**State:** superseded by FND-024

Bundled documents were useful for initial reasoning review. The executable contract now uses split canonical records.

### FND-207 — Revision impact propagation remained the main semantic blocker

**State:** superseded by FND-018

Material and navigational dependencies, staleness states, translation mismatch, and human impact review are now defined and demonstrated.

### FND-209 — First reference implementation remained blocked

**State:** superseded by FND-022

The minimum Phase 0 validator was selected through ADR-0001 and passes the fixture matrix on Python 3.11 and 3.13.

## Open Phase 1 decisions

These do not block Phase 0 foundation acceptance.

### FND-210 — Repository structure after Phase 0

- Should prototype code move beneath `prototypes/`?
- Should canonical content and product software remain in one repository?
- Where should generated artifacts live?

### FND-211 — Formal expressions and executable models

- Does a later contract need typed equations or a formal-expression subtype?
- How are symbolic derivations, simulations, and notebooks compared?
- Which executable artifacts are reproducibility inputs rather than canonical knowledge?

### FND-212 — Protocol and method representation

- Are experimental protocols sources, models, or a future method entity?
- How are protocol deviations and instrument calibration represented?

### FND-213 — Legal and policy interpretation lifecycle

- How are authoritative guidance, amendments, and case law linked to legal claims?
- Which changes trigger review of normative syntheses?

### FND-214 — Confidence calibration

- How do reviewers apply qualitative confidence consistently across domains?
- When should a domain-native uncertainty representation replace a qualitative label?

### FND-215 — Operational federation

- How are identifiers exchanged across repositories?
- Which authority controls aliases and collision resolution?
- How are trust and access boundaries represented?

## Rejected decisions

### FND-301 — Treat the current polyglot stack as final

Rejected because it predates the canonical ontology, corpus, workload, and operational evidence.

### FND-302 — Use concepts as the only knowledge entity

Rejected because it prevents claim-level provenance, disagreement, model assumptions, questions, and synthesis.

### FND-303 — Build polished UI before representative content

Rejected because interface behavior would solidify incomplete semantics.

### FND-304 — Make English the only authored knowledge language

Rejected because it would make Indonesian and other serious authored knowledge secondary display material rather than reviewable first-class content.

### FND-305 — Promote translations automatically

Rejected because translation can alter meaning, scope, terminology, and ambiguity.

### FND-306 — Introduce argument as an entity before evidence

Rejected for `0.1`; embedded argument structure is sufficient until reuse and independent lifecycle are demonstrated.

### FND-307 — Require reviewed example content before accepting the foundation contract

Rejected because it conflates two authorities. Phase 0 must prove that reviewable content can be represented and validated; Phase 1 must perform and record the independent reviews before promoting particular revisions.

## Decision procedure

1. State the concrete problem and affected invariants.
2. Create representative valid and invalid examples.
3. Compare alternatives and failure modes.
4. Record the decision and rationale.
5. Update contracts, policies, vocabulary, and gates together.
6. Add migration notes for authored or generated content.
7. Retain previous decision history.
8. Reopen an accepted decision when fixtures or review demonstrate semantic failure.
