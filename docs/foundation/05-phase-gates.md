# Atlas Phase Gates

## Why gates replace a feature checklist

A roadmap can create the illusion of progress by counting components. Atlas uses phase gates: each phase must prove that its contracts, examples, failure behavior, and authority boundaries are stable enough for the next layer.

A buildable component is not automatically a mature knowledge system. A machine-valid content file is not automatically reviewed knowledge.

## Phase 0 — Knowledge foundation

**Status: closure candidate for `atlas-content/0.1`**

### Purpose

Define the product, ontology, evidence model, editorial lifecycle, authored-content contract, migration rules, and architecture decision policy before product implementation expands.

### Required outputs

- foundation charter and non-goals;
- canonical entity definitions and invariants;
- evidence, disagreement, review, revision, and staleness policy;
- versioned Markdown authoring contract;
- controlled relation vocabulary;
- multilingual identity and translation policy;
- migration and rollback policy;
- current-prototype audit;
- architecture and language decision policy;
- accepted minimum validator ADR;
- decision register;
- representative valid and invalid fixtures;
- closure report.

### Required vertical slices

At least three bounded draft trails exercise materially different knowledge structures:

```text
question
→ source
→ evidence
→ claim
→ concept or model
→ synthesis
→ limitation or revision trigger
```

The Phase 0 reference domains are:

- empirical biology and assay interpretation;
- formal feedback modeling and model-to-world inference;
- socio-technical recommender evidence, legal context, and normative reasoning.

The slices must be individually traceable and mechanically valid. They are ontology fixtures, not automatically reviewed educational content.

### Exit criteria

- every canonical entity has stable identity, required meaning, and lifecycle rules;
- claim-level provenance, disagreement, and normative boundaries are representable;
- malformed and semantically invalid content is rejected predictably;
- reviewed items are distinguishable from drafts and review is revision-specific;
- language-specific IDs, shared work identity, translation lineage, and staleness are demonstrated;
- mechanical and semantic migrations preserve identity and meaning through explicit mappings;
- alias, rename, collision, and federation behavior have representative fixtures;
- derived tools can be replaced without losing authored meaning;
- the minimum validator scope is approved through ADR;
- canonical and translated fixtures pass the supported environment matrix;
- a closure report recommends entry into Phase 1;
- no unresolved critical or major **foundation-definition** issue blocks the reference-review phase.

### Acceptance boundary

Phase 0 acceptance stabilizes the knowledge contract and executable fixture architecture.

It does not promote fixture content from `draft`. Independent domain, methodological, ethical, legal-context, and translation review belong to Phase 1 and remain revision-specific.

### Forbidden expansion

No product UI expansion, retrieval service, plugin system, AI synthesis workflow, synchronization layer, new language boundary, or canonical runtime storage design.

## Phase 1 — Reviewed reference corpus and validator hardening

### Purpose

Test the accepted foundation through independent review of real canonical revisions and harden the smallest validator without turning it into the product runtime.

### Scope

- conduct source, editorial, domain, methodological, reproducibility, ethical, legal-context, conflict, and translation review as applicable;
- preserve reviewer disagreement and conflicts;
- promote only exact revisions that pass their required review types;
- test confidence vocabulary and domain-native uncertainty;
- add contradiction, deprecation, retraction, and revision-impact cases;
- expand migration and identity fixtures when real review exposes gaps;
- improve diagnostics and provenance reports;
- document where `atlas-content/0.1` is too rigid or too vague;
- reopen Phase 0 decisions when fixture or review evidence demonstrates semantic failure.

### Architecture posture

Use the ADR-0001 Python validator as a bounded reference baseline. Do not reuse it as product architecture by default. One semantic owner and versioned fixtures remain mandatory.

### Exit criteria

- required independent reviews are recorded for the reference corpus;
- no reviewed item has unresolved critical or major findings;
- reviewer conflicts and disagreement are visible;
- source-to-synthesis provenance reports are usable without reading implementation code;
- contradiction, deprecation, retraction, and staleness workflows are demonstrated;
- confidence and uncertainty language receives reviewer calibration;
- migration and identity behavior survives representative contract evolution;
- canonical IDs survive file reordering and generated-storage changes;
- validator results are deterministic across supported environments;
- the first minimal knowledge-kernel requirements are derived from reviewed workflows rather than the prototype.

### Non-scope

- polished knowledge interface;
- specialized search service;
- autonomous synthesis;
- cloud synchronization;
- plugin marketplace;
- broad product implementation.

## Phase 2 — Minimal knowledge kernel

### Purpose

Build the smallest dependable runtime that can load, query, and traverse the accepted and reviewed model.

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
- performance and resource behavior are measured on representative reviewed corpora;
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
- implementation pressure distorts the contract;
- new evidence invalidates a central assumption.

Reopening a foundation decision is responsible versioned development, not failure.
