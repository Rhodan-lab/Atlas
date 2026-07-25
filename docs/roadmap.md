# Atlas Roadmap

## Roadmap status

Atlas uses **evidence-based phase gates**, not a feature checklist. Authoritative definitions are in [`docs/foundation/05-phase-gates.md`](foundation/05-phase-gates.md).

The C++, Rust, Python ingestion, TypeScript, SQL, `.atlas`, and browser work remains an experimental prototype. It is maintained for regression and comparison, not counted as completed product architecture.

## Phase 0 — Knowledge foundation

**Status: closure candidate for `atlas-content/0.1`**

Completed foundation outputs:

- charter and non-goals;
- canonical entity model and invariants;
- claim-level evidence and provenance;
- evidence, review, disagreement, revision, translation, migration, and staleness governance;
- governed relation vocabulary;
- multilingual identity with shared work IDs;
- versioned authored Markdown contract;
- three split canonical vertical slices;
- complete Indonesian translation path;
- invalid, migration, identity, federation, and stale-translation fixtures;
- accepted minimum validator ADR;
- deterministic Python 3.11/3.13 validation matrix;
- source-verification and review registers;
- closure report.

Closure condition:

- final PR #3 checks remain green;
- maintainer accepts the versioned foundation through merge.

Phase 0 acceptance stabilizes the foundation. It does not promote example content from `draft`.

## Phase 1 — Reviewed reference corpus and validator hardening

**Status: next after Phase 0 acceptance**

Primary work:

- conduct revision-specific source, editorial, domain, methodological, reproducibility, ethical, legal-context, conflict, and translation reviews;
- preserve reviewer disagreement and conflicts;
- promote only entities that pass required review types;
- calibrate confidence and domain-native uncertainty;
- exercise contradiction, deprecation, retraction, and revision impact;
- harden deterministic diagnostics and provenance reports;
- expand migration and identity fixtures when review exposes real gaps;
- reopen Phase 0 decisions when evidence demonstrates ontology failure;
- derive minimal knowledge-kernel requirements from reviewed workflows.

Non-scope:

- product UI expansion;
- specialized search architecture;
- synchronization or plugins;
- autonomous synthesis;
- new programming-language boundaries.

## Phase 2 — Minimal knowledge kernel

Implement only the dependable runtime required by reviewed Phase 1 workflows.

Expected outcomes:

- canonical-to-runtime compilation;
- read-only entity repository;
- typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- deterministic command or library interface;
- compatibility and failure tests;
- representative performance measurements.

The kernel must remain replaceable without changing authored Markdown.

## Phase 3 — Retrieval and research trails

Add inspectable retrieval after the knowledge kernel is dependable.

Expected outcomes:

- lexical baseline and documented relevance tests;
- field-, status-, and evidence-aware ranking;
- filters and saved research trails;
- contradiction and duplicate candidates;
- ranking explanations;
- specialized indexing only after benchmark approval.

## Phase 4 — Interactive atlas

Build interfaces over proven semantics.

Expected outcomes:

- long-form reading and evidence inspection;
- concept, claim, prerequisite, timeline, scale, and system views;
- accessible exploration without mandatory graph visualization;
- visible review status, uncertainty, provenance, and staleness;
- local-first packaging.

## Phase 5 — Assisted synthesis and extensions

Introduce advanced assistance only after authority and governance are dependable.

Possible outcomes:

- AI-assisted draft extraction and synthesis;
- citation-aware research workflows;
- domain-specific validators and model adapters;
- synchronization preserving local ownership;
- permissioned plugins.

AI output remains draft until reviewed and cannot bypass source verification.

## Global non-goals until prerequisites exist

- autonomous rewriting of authoritative knowledge;
- opaque vector-only retrieval;
- mandatory cloud accounts;
- polished visual design before reviewed workflows;
- plugin marketplaces before versioned contracts and permissions;
- adding languages without an independently useful, measured boundary;
- describing machine conformance as scientific validity.

## Progress rule

A phase is complete only when its own authority boundary and exit criteria are demonstrated. Code quantity, language count, screenshots, or build success are not sufficient measures of maturity.
