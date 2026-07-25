# ADR-0001 — Use Python for the Phase 0 contract validator

- **Status:** accepted for Phase 0 verification
- **Date:** 2026-07-26
- **Decision owners:** Atlas foundation maintainers
- **Foundation decisions affected:** FND-002, FND-006, FND-011, FND-012
- **Phase-gate criterion affected:** executable structural and semantic validation

## Context

Atlas Phase 0 requires deterministic validation of authored Markdown, canonical identity, relation direction, translation lineage, migration mappings, and invalid fixtures. The validator is verification infrastructure, not the future Atlas runtime. It must remain small enough to replace after Phase 0 and must not make its implementation language authoritative over the content contract.

## Requirements

The baseline must:

- parse YAML front matter from Markdown;
- reject duplicate YAML keys;
- validate `atlas-content/0.1` records;
- report deterministic diagnostic codes, paths, and messages;
- validate the canonical reference corpus as a connected set;
- execute the invalid-fixture catalog;
- verify identity, translation-staleness, and migration fixtures;
- avoid rewriting authored meaning;
- run on Linux, macOS, and Windows in CI;
- remain independently replaceable.

## Non-requirements

The baseline does not provide:

- product search or graph traversal;
- a database or runtime storage format;
- editorial correction;
- domain or scientific review;
- automatic review promotion;
- UI, API, synchronization, plugins, or AI workflows.

## Options considered

### Option A — Python 3.11+ with PyYAML

Strengths:

- concise implementation for content validation;
- mature YAML parser and straightforward duplicate-key protection;
- strong standard-library support for paths, JSON fixtures, testing, and deterministic sorting;
- matches the existing research and ingestion ecosystem without requiring reuse of the provisional ingestion ontology;
- low cost for maintainers to inspect or replace.

Costs:

- one runtime and one pinned dependency;
- dynamic typing requires disciplined tests and explicit checks;
- Python must not become the owner of canonical semantics outside the versioned contract and fixtures.

### Option B — TypeScript on Node.js

Strengths:

- accessible tooling and good JSON/schema ecosystem;
- could later share types with a browser application.

Costs:

- browser reuse is not a Phase 0 requirement;
- package and module configuration would be larger than the validator itself;
- risks making future UI concerns influence the authoring contract.

### Option C — Rust

Strengths:

- strong type system and deterministic native executable;
- suitable for a future high-performance indexer.

Costs:

- larger implementation and contributor setup for a small contract checker;
- compile time and ownership complexity provide no demonstrated Phase 0 advantage;
- would prematurely reinforce the existing polyglot prototype.

### Option D — Extend the current Python ingestion prototype

Strengths:

- reuses existing code.

Costs:

- the ingestion tool implements the earlier concept-only contract;
- reuse would risk importing provisional ontology assumptions;
- foundation validation needs a clean semantic boundary and independent fixtures.

## Decision

Use **Python 3.11+ with pinned PyYAML** for a small, standalone Phase 0 validator under `tools/foundation-validator/`.

The validator is authoritative only about whether authored files conform to the published `atlas-content/0.1` rules and fixture expectations. The Markdown contract, foundation policies, and accepted decisions remain authoritative over the validator.

## Boundary

### Responsibilities

- parse front matter without silently repairing it;
- produce deterministic structural and semantic diagnostics;
- resolve canonical IDs across a corpus;
- validate controlled relation types and subject-target pairs;
- verify translation and migration fixtures;
- execute invalid cases and snapshot expected diagnostic codes.

### Non-responsibilities

- judging scientific truth;
- assigning confidence labels;
- deciding whether a source is credible;
- granting `reviewed` status;
- compiling the product runtime;
- mutating authored files.

### Inputs

- UTF-8 Markdown with YAML front matter;
- JSON fixture manifests for invalid, migration, identity, and translation cases.

### Outputs

- sorted diagnostics in human-readable or JSON form;
- nonzero exit status when errors occur or fixture expectations fail.

### Error behavior

The validator reports all safely independent findings in one pass. It never changes files. Diagnostics are sorted by path, code, and message.

## Acceptance criteria

- every canonical entity file parses and receives no error diagnostics;
- all 24 invalid fixture cases produce their expected codes;
- duplicate ID, alias, rename, collision, and federation cases are deterministic;
- mechanical migration preserves ID, work, status, revision history, and provenance;
- semantic claim split has an explicit one-to-many identity mapping;
- translation source revision changes mark the translation stale in the fixture result;
- unit tests run with one command and in GitHub Actions;
- removing the validator does not remove authored meaning.

## Consequences

### Positive

- Phase 0 rules become executable rather than aspirational;
- diagnostics can stabilize before product architecture resumes;
- the implementation remains small and disposable.

### Negative

- contributors need Python and one dependency;
- semantic rules are still procedural rather than generated from a formal schema;
- human review remains necessary for meaning and evidence quality.

### New risks

- validator code could drift from foundation documents;
- future contributors might treat passing validation as scientific approval.

Mitigation: fixtures, the completion report, and repository guidance explicitly distinguish conformance from truth and review.

## Migration plan

No canonical content meaning changes. Existing bundled slices remain historical drafting artifacts while canonical entity files become the executable reference corpus.

## Rollback or replacement plan

A replacement validator must pass the same canonical corpus, invalid cases, migration fixtures, and diagnostic snapshots. Python-specific state is not stored in authored content.

## Validation

Before this ADR is considered implemented:

- add the validator and pinned dependency;
- add canonical and invalid fixtures;
- add unit and CI tests;
- publish an execution report in the Phase 0 completion document.

## Decision history

- 2026-07-26: accepted for Phase 0 verification after comparing Python, TypeScript, Rust, and reuse of the provisional ingestion tool.
