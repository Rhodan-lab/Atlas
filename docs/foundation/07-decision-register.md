# Foundation Decision Register

## Purpose

This register separates accepted constraints from provisional assumptions and unresolved decisions. Implementation must not silently decide open semantic questions.

## Decision states

- `accepted` — binding until explicitly revised;
- `provisional` — usable for fixtures but still under evaluation;
- `open` — unresolved and potentially blocking;
- `rejected` — considered and excluded for the stated reason;
- `superseded` — replaced with preserved history.

## Accepted decisions

### FND-001 — Foundation before feature development

Atlas remains in Phase 0 until knowledge, evidence, editorial, fixture, and migration gates are met. Existing software is experimental and feature-frozen.

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

Canonical structural tokens remain English technical identifiers. Human-readable knowledge may use any declared language. Translations are separate entities sharing a `work` identity and require their own review. See `12-authoring-language-and-translation-policy.md`.

### FND-011 — Claim atomicity is semantic, not sentence length

A claim is split when its clauses can differ in evidence, scope, confidence, lifecycle, contradiction, or revision. See `13-claim-scope-and-argument-policy.md`.

### FND-012 — Argument is embedded structure in `0.1`

Arguments use structured premise, assumption, conclusion, alternative, and inference blocks. They are not canonical entities until fixtures demonstrate a need for independent identity and lifecycle.

### FND-013 — Evidence storage follows minimum-necessary provenance

Atlas stores source identity, precise locator, context, method, limitations, access class, and evidence role. It does not assume full-source redistribution. See `14-evidence-data-and-restricted-source-policy.md`.

### FND-014 — Quantitative evidence has lineage

Values include quantities, units, uncertainty or its absence, methods, transformations, inputs, and missing-data behavior where applicable.

### FND-015 — Review is revision-specific and role-specific

Review records exact entity revision, review types, reviewers, conflicts, findings, and unresolved issues. Reviewer disagreement remains visible. See `15-review-governance-and-disagreement.md`.

### FND-016 — Three reference domains are fixed for Phase 0

The reference corpus tests empirical biology, formal feedback modeling, and socio-technical recommender governance. The slices are bounded ontology tests, not a general content-production program.

### FND-017 — Invalid fixtures are part of the contract

The validator must report specific deterministic structural and semantic diagnostics and must never silently repair authored meaning.

## Provisional decisions

### FND-101 — Canonical entity set

**State:** provisional

Source, evidence, claim, concept, relation, model, question, synthesis, and revision remain sufficient across the first three bundled slices. Argument stays embedded. The entity set is promoted only after the slices are split into canonical files and reviewed.

### FND-102 — Controlled relation vocabulary

**State:** provisional

The vocabulary in `10-relation-vocabulary.md` is now the single source of truth and is exercised by the reference slices. Pair compatibility and ambiguous cases still need validator fixtures.

### FND-103 — Human-readable canonical identifiers

**State:** provisional

Language-specific entity IDs plus shared language-neutral `work` identity are adopted for `0.1`. Alias, rename, federation, and collision behavior still need dedicated fixtures.

### FND-104 — Qualitative confidence vocabulary

**State:** provisional

`uncertain`, `plausible`, `well-supported`, and `strongly-supported` require rationale and scope. The three slices show useful distinctions, but reviewer calibration remains untested.

### FND-105 — Independent learner and researcher as initial user

**State:** provisional

The foundation optimizes for inspectable personal or small-team knowledge. Institutional workflow requirements are deferred.

### FND-106 — Bundled vertical slices before canonical file split

**State:** provisional

Phase 0 uses one document per slice so reviewers can inspect the entire reasoning chain. Phase 1 should split records mechanically only after the contract passes review.

## Open decisions

### FND-207 — Revision impact propagation

- Which relation types automatically mark dependents stale?
- How are downstream syntheses re-reviewed?
- Which warnings can be generated without claiming semantic impact is fully understood?

This is the main remaining semantic blocker.

### FND-209 — First reference implementation

- What is the smallest validator and compiler baseline?
- Which language minimizes semantic duplication and setup cost?
- Which prototype components should be retained, compared, or retired?

This remains intentionally blocked until Phase 0 fixtures and completion assessment are reviewed.

### FND-210 — Repository structure after Phase 0

- Should prototype code move beneath `prototypes/`?
- Should canonical content and software remain in one repository?
- Where should generated artifacts live?

This is not blocking the current bundled-fixture review.

### FND-211 — Formal expressions and executable models

- Does `0.1` need typed equations or a separate formal-expression contract?
- How are symbolic derivations, simulations, and notebooks compared?
- Which executable artifacts are reproducibility inputs rather than canonical knowledge?

The feedback slice exposes this question without requiring immediate expansion.

### FND-212 — Protocol and method representation

- Are experimental protocols sources, models, or a future method entity?
- How are protocol deviations and instrument calibration represented?

The catalase slice exposes this question.

### FND-213 — Legal and policy interpretation lifecycle

- How are authoritative guidance, amendments, and case law linked to legal claims?
- Which changes trigger review of normative syntheses?

The recommender slice exposes this question.

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

## Decision procedure

1. State the concrete problem and affected invariants.
2. Create representative valid and invalid examples.
3. Compare alternatives and failure modes.
4. Record the decision and rationale.
5. Update contracts, policies, vocabulary, and gates together.
6. Add migration notes for authored or generated content.
7. Retain previous decision history.
8. Reopen an accepted decision when fixtures demonstrate semantic failure.
