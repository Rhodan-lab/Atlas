# Atlas Phase Gates

## Why gates replace a feature checklist

A roadmap can create the illusion of progress by counting components. Atlas instead uses phase gates: each phase must prove that its foundation is stable enough for the next layer. A phase is not complete because code exists; it is complete when its contracts, examples, review rules, and failure behavior are demonstrated.

## Phase 0 — Knowledge foundation

**Status: active**

### Purpose

Define the product, ontology, evidence model, editorial lifecycle, authoring contract, and architecture decision rules.

### Required outputs

- foundation charter and non-goals;
- canonical entity definitions and invariants;
- evidence, disagreement, review, and revision policy;
- versioned Markdown authoring contract;
- controlled relation vocabulary;
- current-prototype audit;
- architecture and language decision policy;
- unresolved decision register;
- representative content fixtures.

### Required vertical slices

At least three carefully reviewed trails must exercise the full structure:

```text
question
→ source
→ evidence
→ claim
→ concept or model
→ relation to another domain
→ synthesis
→ open limitation or revision trigger
```

The slices should differ materially, for example:

- an empirical scientific topic with quantitative evidence;
- a formal or computational topic involving definitions and a model;
- a human, social, strategic, or ethical topic containing interpretation and disagreement.

### Exit criteria

- every canonical entity has stable identity, required meaning, and lifecycle rules;
- claim-level provenance and contradiction are representable;
- malformed and semantically invalid content can be rejected predictably;
- reviewed items are distinguishable from drafts;
- derived artifacts can be rebuilt without losing authored meaning;
- the first implementation scope is small and explicitly approved;
- no unresolved issue blocks a reference implementation.

### Forbidden expansion

No new UI, search service, plugin system, AI workflow, synchronization layer, or language boundary.

## Phase 1 — Reference corpus and validator

### Purpose

Prove the knowledge model using real content before building a general product.

### Scope

- author representative entities in Markdown;
- build structural and semantic validation;
- generate provenance and review reports;
- test controlled vocabularies and relation compatibility;
- test revision, deprecation, and contradiction;
- document where the contract is too rigid or too vague.

### Architecture posture

Use the simplest implementation capable of validating the contract. A single language is preferred unless the Phase 0 decision policy demonstrates otherwise.

### Exit criteria

- all Phase 0 fixtures validate correctly;
- invalid fixtures fail with specific diagnostics;
- three vertical slices can be reviewed without relying on internal code knowledge;
- canonical IDs survive file reordering and generated-storage changes;
- the contract has a documented version and migration policy;
- editorial reviewers can use the reports effectively.

## Phase 2 — Minimal knowledge kernel

### Purpose

Build the smallest dependable runtime that can load, query, and traverse the accepted model.

### Scope

- canonical-to-runtime compiler;
- read-only repository or index;
- entity lookup and typed relation traversal;
- provenance queries from synthesis to source;
- dependency and revision-impact queries;
- deterministic command or library interface;
- contract and compatibility tests.

### Non-scope

- polished visual explorer;
- autonomous synthesis;
- broad plugin architecture;
- cloud synchronization;
- optimization without measured need.

### Exit criteria

- runtime results match authoritative fixtures;
- no domain rule is duplicated across components;
- invalid generated inputs fail atomically;
- performance and resource behavior are measured on representative corpora;
- the runtime can be replaced without changing authored knowledge.

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
- optional specialized index only after benchmark approval.

### Exit criteria

- relevance is evaluated on a documented test collection;
- search never hides review status or provenance;
- ranking behavior is explainable;
- specialized language or service boundaries pass the architecture policy;
- failure of retrieval does not corrupt authoritative knowledge.

## Phase 4 — Interactive atlas

### Purpose

Provide useful views over a proven knowledge system.

### Scope

- long-form reading;
- evidence and claim inspection;
- concept and prerequisite navigation;
- graph, timeline, scale, and system views where they improve understanding;
- accessibility and typography controls;
- local-first packaging.

### Exit criteria

- every visual relation maps to canonical semantics;
- no interface element implies false confidence or review status;
- key workflows work without a graph visualization;
- navigation supports exploration rather than a rigid course sequence;
- accessibility and failure-state tests pass.

## Phase 5 — Assisted synthesis and domain extensions

### Purpose

Add advanced analysis only after governance and provenance are dependable.

Possible scope:

- assisted claim extraction;
- citation-aware synthesis drafts;
- model and simulation adapters;
- domain-specific validators;
- synchronization;
- optional plugins;
- local AI assistance.

### Mandatory constraints

- AI output remains draft until reviewed;
- source and evidence locators are independently checked;
- extensions cannot bypass canonical contracts;
- synchronization preserves local ownership and revision history;
- plugin permissions and failure isolation are explicit.

## Reopening a completed phase

A phase can be reopened when:

- representative content exposes an ontology failure;
- review reveals a provenance or uncertainty gap;
- a migration loses meaning;
- implementation pressure is distorting the contract;
- new evidence invalidates a central assumption.

Reopening a foundation decision is a sign of responsible development, not failure.
