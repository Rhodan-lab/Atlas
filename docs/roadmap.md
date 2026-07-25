# Atlas Roadmap

## Roadmap status

Atlas uses **evidence-based phase gates**, not a feature checklist. The authoritative gate definitions are in [`docs/foundation/05-phase-gates.md`](foundation/05-phase-gates.md).

The earlier roadmap incorrectly described the C++ and polyglot prototypes as completed foundation phases. They are now recorded as experiments that revealed useful engineering possibilities and important semantic gaps.

## Experimental work already present

The repository currently demonstrates:

- a C++ concept-graph engine and CLI;
- a provisional `.atlas` file format;
- Python Markdown ingestion;
- a Rust lexical search process;
- a TypeScript API and browser explorer;
- a preliminary SQL schema;
- per-language and integration CI.

This work remains valuable for comparison and regression testing. It does not satisfy the new Phase 0 exit criteria because the prototype predates the claim, evidence, review, uncertainty, model, synthesis, and revision contracts.

## Phase 0 — Knowledge foundation

**Status: active**

Primary work:

- finalize the Atlas charter and non-goals;
- test the canonical entity set;
- define claim-level provenance;
- define editorial and scientific review;
- define uncertainty, disagreement, revision, and dependency impact;
- stabilize the authoritative Markdown contract;
- create three complete reference vertical slices;
- close or explicitly defer blocking foundation decisions;
- reassess implementation choices through ADRs.

No feature expansion is permitted during this phase.

## Phase 1 — Reference corpus and validator

Build a small, rigorous body of canonical Markdown content and the simplest validator needed to test it.

Expected outcomes:

- valid and invalid fixtures for every entity type;
- deterministic canonical identity;
- structural, semantic, editorial, and reproducibility checks;
- provenance and review reports;
- tested contradiction, deprecation, and revision behavior;
- versioned content contract and migration rules.

## Phase 2 — Minimal knowledge kernel

Implement only the dependable runtime needed to load and query the accepted model.

Expected outcomes:

- canonical-to-runtime compilation;
- entity lookup and typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- measured behavior on representative corpora;
- one clear owner for each semantic invariant.

The first baseline should use the smallest reasonable architecture. Polyglot extraction requires separate approval.

## Phase 3 — Retrieval and research trails

Add inspectable retrieval after the knowledge kernel is reliable.

Expected outcomes:

- lexical baseline and documented relevance tests;
- field- and status-aware ranking;
- filters and saved research trails;
- contradiction and duplicate candidates;
- ranking explanations;
- specialized indexing only when benchmarks demonstrate the need.

## Phase 4 — Interactive atlas

Build interfaces over proven semantics.

Expected outcomes:

- long-form reading and evidence inspection;
- concept, claim, prerequisite, timeline, scale, and system views;
- accessible exploration without a mandatory graph visualization;
- visible review status, uncertainty, and provenance;
- local-first packaging.

## Phase 5 — Assisted synthesis and extensions

Introduce advanced assistance only after authority and governance are dependable.

Possible outcomes:

- AI-assisted draft extraction and synthesis;
- citation-aware research workflows;
- domain-specific validators and model adapters;
- synchronization that preserves local ownership;
- carefully permissioned plugins.

AI output remains draft until reviewed and cannot bypass source verification.

## Global non-goals until their prerequisites exist

- autonomous rewriting of authoritative user knowledge;
- opaque vector-only retrieval;
- mandatory cloud accounts;
- polished visual design before representative content;
- plugin marketplaces before versioned contracts;
- adding languages without an independently useful, benchmarked boundary;
- describing internal consistency as scientific validity.

## Progress rule

A phase is complete only when its exit criteria are demonstrated with reviewed examples, fixtures, and failure cases. Code quantity, language count, screenshots, or build success are not sufficient measures of maturity.
