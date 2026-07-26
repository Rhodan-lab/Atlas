# Atlas Phase Gates

## Why gates replace a feature checklist

Atlas measures maturity through evidence, not component count. Each phase must prove that its contracts, fixtures, failure behavior, and authority boundaries are stable enough for the next layer.

A buildable component is not automatically a mature knowledge system. A machine-valid file is not automatically reviewed knowledge.

## Phase 0 — Knowledge foundation

**Status: accepted for `atlas-content/0.1`**

Accepted through merged PR #3 at commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`.

### Purpose

Define the product, ontology, evidence model, editorial lifecycle, authored-content contract, migration rules, and architecture policy before product implementation expands.

### Required outputs

- foundation charter and non-goals;
- canonical entity definitions and invariants;
- evidence, disagreement, review, revision, and staleness policy;
- versioned Markdown authoring contract;
- controlled relation vocabulary;
- language-qualified identity and dormant translation semantics;
- migration and rollback policy;
- current-prototype audit;
- architecture and programming-language decision policy;
- accepted minimum validator ADR;
- decision register;
- representative valid and invalid fixtures;
- closure report.

### Required vertical slices

At least three bounded draft trails exercise materially different structures:

```text
question
→ source
→ evidence
→ claim
→ concept or model
→ synthesis
→ limitation or revision trigger
```

Reference domains:

- empirical biology and assay interpretation;
- formal feedback modeling and model-to-world inference;
- socio-technical recommender evidence, legal context, and normative reasoning.

The slices are ontology fixtures, not automatically reviewed educational content.

### Exit criteria

- canonical entities have stable identity, meaning, and lifecycle rules;
- claim-level provenance, disagreement, and normative boundaries are representable;
- malformed and semantically invalid content is rejected predictably;
- reviewed items are distinguishable from drafts and review is revision-specific;
- language-qualified IDs, shared work identity, source-revision lineage, and staleness are representable;
- mechanical and semantic migrations preserve identity and meaning through explicit mappings;
- alias, rename, collision, and federation behavior have representative fixtures;
- derived tools can be replaced without losing authored meaning;
- the minimum validator scope is approved through ADR;
- the canonical corpus and synthetic boundary fixtures pass the supported environment matrix;
- a closure report recommends entry into Phase 1;
- no unresolved critical or major foundation-definition issue blocks review work.

Passing these gates did not promote reference content beyond `draft`.

### Language amendment

The active authored corpus is English-only. Translation semantics remain covered through neutral synthetic fixtures. Multilingual authoring requires a future explicit reopening decision.

### Reopening rule

Phase 0 may be reopened only when a representative review, migration, lifecycle fixture, or future multilingual reopening demonstrates a real contract or ontology failure. Implementation convenience alone is insufficient.

## Phase 1 — English reference corpus and review gate

**Status: active**

### Purpose

Test the accepted foundation through exact-revision review of canonical English content and harden bounded validators without turning them into product runtime.

### Accepted contracts

- `atlas-review/0.1` — exact-revision review records;
- `atlas-promotion/0.1` — deterministic lifecycle decisions;
- `atlas-review-coverage/0.1` — packet and complete-slice coverage;
- `atlas-review-backlog/0.1` — deterministic review tasks.

These contracts preserve reviewer kind, independence, qualification, accountability, conflicts, outcomes, findings, horizons, dependency impact, and transition history.

### Scope

- conduct source, editorial, domain, methodological, reproducibility, ethical, legal-context, and conflict review as applicable;
- preserve reviewer disagreement and conflicts;
- promote only exact revisions that pass required review types;
- reject machine-only or AI-only authority where accountable human judgment is required;
- generate reviewer-ready packets, coverage reports, and review backlogs;
- distinguish automation-eligible tasks from human-required tasks;
- test confidence vocabulary and domain-native uncertainty;
- exercise contested, deprecation, retraction, and revision-impact cases;
- expand migration and identity fixtures when real review exposes gaps;
- document where `atlas-content/0.1` is too rigid or vague;
- reopen Phase 0 only when evidence demonstrates semantic failure.

### Active review scopes

- catalase and assay methodology;
- delayed-feedback mathematics, terminology, and inference limits;
- recommender evidence, current legal context, and ethical governance;
- complete English delayed-feedback vertical slice.

### Architecture posture

Use the bounded Python validators as reference baselines. They do not become product architecture by implication.

One semantic owner, versioned fixtures, deterministic diagnostics, and explicit migrations remain mandatory.

### Exit criteria

- review, promotion, coverage, and backlog contracts are explicit and executable;
- records and manifests validate deterministically across supported environments;
- machine and AI assistance cannot grant accountable authority where human review is required;
- exact-revision, conflict, review-horizon, and staleness rules are enforced;
- reviewer packets, coverage reports, and backlogs are usable without reading implementation code;
- contested, deprecation, retraction, and stale-review workflows are demonstrated;
- confidence and uncertainty language receives reviewer calibration;
- the complete English delayed-feedback slice has sufficient review coverage for its intended lifecycle state;
- no reviewed item has unresolved critical or major findings;
- remaining independent-review gaps remain visible and are not reported as passes;
- migration and identity behavior survives representative contract evolution;
- canonical IDs survive file reordering and generated-storage changes;
- minimal knowledge-kernel requirements are derived from reviewed workflows;
- a Phase 1 completion report recommends or rejects entry into Phase 2.

### Authority boundary

AI-assisted and machine records may identify defects and block promotion. They may not satisfy independent domain, methodological, ethical, legal-context, or final editorial authority.

Synthetic translation fixtures may demonstrate structural or staleness behavior only. They do not establish an active authored language or translation authority.

Canonical entities remain `draft` until acceptable review coverage exists and an accountable human accepts the exact lifecycle transition.

### Non-scope

- polished product interface;
- specialized search service;
- active translated corpus or language-specific review program;
- autonomous synthesis;
- cloud synchronization;
- plugin marketplace;
- live Principia integration;
- broad product implementation.

## Phase 2 — Minimal knowledge kernel

### Purpose

Build the smallest dependable runtime required by reviewed Phase 1 workflows.

### Scope

- canonical-to-runtime compiler;
- read-only repository or index;
- entity lookup and typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- deterministic command or library interface;
- contract and compatibility tests.

### Exit criteria

- runtime results match authoritative fixtures;
- no domain rule is duplicated across components;
- invalid generated inputs fail atomically;
- performance and resources are measured on representative reviewed corpora;
- runtime can be replaced without changing authored knowledge.

## Phase 3 — Retrieval and research trails

### Purpose

Help users find relevant knowledge and inspect why it was retrieved.

### Scope

- lexical search baseline;
- field-aware ranking;
- filters by entity, status, domain, date, and evidence role;
- saved research trails;
- contradiction and duplicate candidates;
- inspectable ranking explanations;
- specialized indexing only after benchmark approval.

### Exit criteria

- relevance is evaluated on a documented test collection;
- search never hides review status or provenance;
- ranking behavior is explainable;
- specialized boundaries pass architecture policy;
- retrieval failure cannot corrupt authoritative knowledge.

## Phase 4 — Principia & Atlas interactive experience

### Purpose

Build a unified user experience over proven semantics without erasing domain boundaries.

### Scope

- Atlas evidence, claim, model, provenance, review, and revision views;
- Principia explanations, pathways, investigations, simulations, system dossiers, and design challenges;
- explicit cross-repository bridge references and impact warnings;
- concept, prerequisite, timeline, scale, and system views where useful;
- accessibility and typography controls;
- local-first packaging.

### Exit criteria

- every visual relation maps to canonical semantics;
- no interface implies false confidence or review status;
- Principia and Atlas status remain separate;
- key workflows work without mandatory graph visualization;
- navigation supports exploration rather than a rigid course sequence;
- accessibility and failure-state tests pass.

## Phase 5 — Assisted synthesis and extensions

### Purpose

Add advanced assistance only after governance and provenance are dependable.

Possible scope:

- assisted claim extraction;
- citation-aware synthesis drafts;
- model and simulation adapters;
- domain-specific validators;
- synchronization;
- permissioned plugins;
- local AI assistance;
- multilingual authoring after an accepted reopening gate.

### Mandatory constraints

- AI output remains draft until reviewed;
- source and evidence locators are independently checked;
- extensions cannot bypass canonical contracts;
- synchronization preserves local ownership and revision history;
- plugin permissions and failure isolation are explicit.

## Reopening a completed phase

A phase may reopen when:

- representative content exposes an ontology failure;
- review reveals a provenance or uncertainty gap;
- a migration loses meaning;
- implementation pressure distorts the contract;
- new evidence invalidates a central assumption.

Reopening a foundation decision is responsible versioned development, not failure.
