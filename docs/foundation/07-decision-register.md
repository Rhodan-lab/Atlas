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

Atlas defines and tests its knowledge foundation before expanding product features. Existing software remains experimental until later gates justify it.

### FND-002 — Markdown is the authored source of truth

Databases, portable files, indexes, JSON, and interfaces are derived and reproducible.

### FND-003 — Claim-level provenance is required

Evidence supports, challenges, or contextualizes individually inspectable claims. Concept-level citations alone are insufficient.

### FND-004 — Draft is the default lifecycle state

New knowledge and generated transformations remain `draft` until required review types are completed.

### FND-005 — Local ownership is a core constraint

Authoritative content remains inspectable and exportable without a mandatory cloud account.

### FND-006 — Polyglot implementation requires evidence

A programming-language or process boundary requires stable responsibility, baseline comparison, measurable advantage, versioned contract, and maintenance analysis.

### FND-007 — AI cannot grant authority

AI may assist draft transformation but cannot create reviewed status or replace source verification.

### FND-008 — No global truth score

Atlas preserves domain-appropriate uncertainty and written rationale rather than one universal credibility number.

### FND-009 — Initial contract is `atlas-content/0.1`

Authoring, derived-data, and application versions are separate. Contract changes follow the migration policy.

### FND-010 — Language-qualified identity remains part of the contract

Canonical structural tokens remain English technical identifiers. The contract can represent separately reviewed language versions sharing a `work` identity. This is a capability decision, not an active corpus requirement.

### FND-011 — Claim atomicity is semantic, not sentence length

A claim is split when clauses can differ in evidence, scope, confidence, lifecycle, contradiction, or revision.

### FND-012 — Argument is embedded structure in `0.1`

Arguments use structured premise, assumption, conclusion, alternative, and inference blocks. They are not canonical entities until fixtures demonstrate independent identity and lifecycle.

### FND-013 — Evidence storage follows minimum-necessary provenance

Atlas stores source identity, precise locator, context, method, limitations, access class, and evidence role. It does not assume full-source redistribution.

### FND-014 — Quantitative evidence has lineage

Values include quantities, units, uncertainty or its absence, methods, transformations, inputs, and missing-data behavior where applicable.

### FND-015 — Review is revision-specific and role-specific

Review records exact entity revision, review types, reviewers, conflicts, findings, and unresolved issues. Reviewer disagreement remains visible.

### FND-016 — Three reference domains define the Phase 0 stress test

The canonical corpus tests empirical biology, formal feedback modeling, and socio-technical recommender governance. The slices are ontology tests, not a general content-production program.

### FND-017 — Invalid fixtures are part of the contract

The validator reports specific deterministic structural and semantic diagnostics and never silently repairs authored meaning.

### FND-018 — Revision impact uses bounded automatic staleness

Material dependency changes may mark downstream items `possibly-stale` or `review-required`. Automation identifies candidates; human review determines semantic impact. Translation source-revision mismatch is demonstrated by a synthetic fixture.

### FND-019 — Canonical entity set is sufficient for `0.1`

Source, evidence, claim, concept, relation, model, question, synthesis, and revision are sufficient for the reference slices. A future contract may add an entity only after fixtures show independent identity and lifecycle are necessary.

### FND-020 — Relation vocabulary is executable for `0.1`

The relation vocabulary is the single source of truth. The validator checks names, directions, entity pairs, duplicate edges, and missing targets.

### FND-021 — Language-qualified IDs and shared work identity are accepted

Equivalent language versions can share a language-neutral `work` identifier while retaining separate IDs, revisions, lifecycle, and review.

### FND-022 — Python is the minimum Phase 0 validator baseline

ADR-0001 selects Python 3.11+ with pinned dependencies for contract verification. The validator is replaceable infrastructure, not product runtime or semantic authority.

### FND-023 — Foundation acceptance is distinct from content review

Phase 0 accepts the versioned knowledge contract, governance, and executable fixture architecture. Phase 1 performs exact-revision independent review. Machine conformance cannot promote content from `draft`.

### FND-024 — Split canonical files replace bundled slices

Bundled vertical-slice documents remain historical drafting artifacts. Executable authored validation uses one file per entity under `content/canonical/`.

### FND-025 — Active authored corpus is English-only

**Accepted during Phase 1.**

The current authored corpus, review packets, coverage manifests, generated backlogs, and future Principia compatibility work use English only.

Translation capability remains dormant language-neutral infrastructure exercised through neutral synthetic fixtures. No active translated corpus, language-specific review queue, or supported product language beyond English exists.

Multilingual authoring may return only through an explicit reopening decision covering scope, reviewer capacity, terminology governance, migration, staleness, and rollback.

### FND-026 — Atlas and Principia retain separate authority boundaries

Atlas owns canonical knowledge identity, evidence, provenance, review, revision, lifecycle, and staleness. Principia will own explanation, pathways, investigations, simulations, system dossiers, and design experiences.

A shared product identity must not create automatic review-status inheritance or circular repository dependency.

## Provisional decisions

### FND-101 — Qualitative confidence vocabulary

`uncertain`, `plausible`, `well-supported`, and `strongly-supported` require rationale and scope. Independent reviewer calibration remains a Phase 1 task.

### FND-102 — Independent learner and researcher as initial user

The foundation optimizes for inspectable personal or small-team knowledge. Institutional workflow requirements remain deferred.

## Superseded decisions

### FND-106 — Bundled vertical slices before canonical file split

Superseded by FND-024.

### FND-207 — Revision impact propagation remained the main semantic blocker

Superseded by FND-018.

### FND-209 — First reference implementation remained blocked

Superseded by FND-022.

### FND-304 — Reject an English-only authored corpus

**State:** superseded by FND-025.

The earlier decision favored immediate multilingual first-class authoring. Phase 1 scope analysis showed that active language expansion would dilute exact-revision review capacity before the English knowledge authority was mature.

The underlying language-neutral contract remains accepted; only the active corpus policy changed.

## Open Phase 1 decisions

### FND-210 — Repository structure after Phase 1

- Should prototype code move beneath `prototypes/`?
- Should canonical content and product software remain in one repository?
- Where should generated artifacts live?

### FND-211 — Formal expressions and executable models

- Does a later contract need typed equations or a formal-expression subtype?
- How are symbolic derivations, simulations, and notebooks compared?
- Which executable artifacts are reproducibility inputs rather than canonical knowledge?

### FND-212 — Protocol and method representation

- Are experimental protocols sources, models, or a future method entity?
- How are deviations and calibration represented?

### FND-213 — Legal and policy interpretation lifecycle

- How are authoritative guidance, amendments, and case law linked to legal claims?
- Which changes trigger review of normative syntheses?

### FND-214 — Confidence calibration

- How do reviewers apply qualitative confidence consistently across domains?
- When should domain-native uncertainty replace a qualitative label?

### FND-215 — Operational federation

- How are identifiers exchanged across repositories?
- Which authority controls aliases and collision resolution?
- How are trust and access boundaries represented?

### FND-216 — Principia bridge contract

- Which Atlas revisions may a Principia artifact pin?
- How are deprecated or retracted dependencies surfaced?
- Which generated impact reports cross repository boundaries?
- How is pedagogical status kept independent from knowledge status?

## Rejected decisions

### FND-301 — Treat the current polyglot stack as final

Rejected because it predates the canonical ontology, corpus, workload, and operational evidence.

### FND-302 — Use concepts as the only knowledge entity

Rejected because it prevents claim-level provenance, disagreement, model assumptions, questions, and synthesis.

### FND-303 — Build polished UI before representative content

Rejected because interface behavior would solidify incomplete semantics.

### FND-305 — Promote translations automatically

Rejected because translation can alter meaning, scope, terminology, and ambiguity.

### FND-306 — Introduce argument as an entity before evidence

Rejected for `0.1`; embedded argument structure is sufficient until reuse and independent lifecycle are demonstrated.

### FND-307 — Require reviewed example content before accepting the foundation contract

Rejected because it conflates foundation conformance with content authority.

### FND-308 — Merge Principia and Atlas repositories before bridge semantics stabilize

Rejected because premature consolidation would mix pedagogical status, knowledge authority, review lifecycle, and implementation history.

## Decision procedure

1. State the concrete problem and affected invariants.
2. Create representative valid and invalid examples.
3. Compare alternatives and failure modes.
4. Record the decision and rationale.
5. Update contracts, policies, vocabulary, and gates together.
6. Add migration notes for authored or generated content.
7. Retain previous decision history.
8. Reopen an accepted decision when fixtures or review demonstrate semantic failure.
