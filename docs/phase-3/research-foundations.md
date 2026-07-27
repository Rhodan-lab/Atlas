# Phase 3 Workstream 5 — Research Trails and Candidate Discovery

## Status

Candidate foundation for the remaining Phase 3 research workflow.

```yaml
phase: 3
workstream: 5
mode: retrieval-evaluation
state: research-foundation-candidate
preferred_bounded_ranking: structured-field-baseline
retrieval_authority: advisory-only
exact_revision_required: true
canonical_copy_authority: false
automatic_merge_or_resolution: false
embeddings: false
vector_database: false
external_services: false
live: false
repository_mutation: false
```

## Purpose

Complete the research foundations required by the authoritative Phase 3 gate before any semantic-index or vector-database decision:

- deterministic retrieval filters;
- saved exact-revision research trails;
- advisory contradiction candidates;
- advisory duplicate candidates.

The workstream is contract-first. It does not add a product UI, autonomous agent, semantic model, or new knowledge authority.

## Filter contract

Contract: `atlas-retrieval-filter/0.1`.

Supported dimensions:

```yaml
entity_types: canonical entity type
statuses: canonical lifecycle status
domains: first canonical collection path segment
updated: inclusive ISO-date from/to range
evidence_roles: explicit authored relation type
```

The initial domain keys are the canonical collection directories:

- `catalase`;
- `feedback`;
- `recommenders`.

Evidence-role filtering is restricted to explicit relation vocabulary:

- `supports`;
- `derived-from`;
- `contextualizes`;
- `replicates`.

Filtering uses AND across dimensions and OR inside a dimension. It preserves canonical order, exact revisions, provenance, status, staleness, and review visibility. It may narrow advisory results; it may not silently substitute `latest`, rewrite ranking evidence, or mutate canonical content.

## Research-trail contract

Contract: `atlas-research-trail/0.1`.

A trail stores research references and decisions, not copied canonical knowledge. Each revision binds:

- stable trail ID and revision;
- accepted query ID and exact text snapshot;
- exact filter ID and revision;
- accepted structured-baseline contract, index digest, and result digest;
- exact selected entity revisions;
- original rank when available;
- action: `include`, `exclude`, or `context`;
- rationale for every action;
- open questions;
- created and updated dates.

Every trail entry must be inside the saved filter result. A trail cannot follow a newer revision automatically, change lifecycle status, or become canonical authority.

## Contradiction-candidate contract

Contract: `atlas-contradiction-candidate/0.1`.

A contradiction candidate requires:

- two different exact entity revisions;
- compared statements;
- scope analysis;
- evidence paths;
- rationale;
- an explicit assessment.

Initial assessments:

- `needs-review`;
- `scope-difference-likely`;
- `substantive-tension`.

A valid candidate means “inspect this possible tension.” It does not prove contradiction, resolve the issue, deprecate a claim, or alter review state. Automatic resolution is forbidden.

## Duplicate-candidate contract

Contract: `atlas-duplicate-candidate/0.1`.

A duplicate candidate requires:

- two different exact entity revisions;
- similarity basis;
- semantic differences;
- evidence paths;
- rationale;
- an explicit assessment.

Initial assessments:

- `needs-review`;
- `related-not-duplicate`;
- `probable-duplicate`.

A valid candidate does not prove duplication and cannot merge, redirect, supersede, or deprecate either entity automatically.

## Reference fixtures

`content/fixtures/phase3_retrieval/research-foundations.v01.json` contains:

- four deterministic filters;
- one saved cross-platform recommender research trail;
- one contradiction candidate assessed as likely scope difference;
- one duplicate candidate assessed as related but not duplicate;
- five negative identity, date, revision, pair, and authority cases.

The positive filters cover:

1. feedback draft models;
2. catalase evidence with explicit `supports` role;
3. recommender evidence with explicit `contextualizes` role;
4. recommender claims and synthesis records for a saved research trail.

## Validation and negative boundaries

Machine validation reconstructs filter results from the canonical runtime and rejects:

- unavailable domain or entity-type values;
- unsupported evidence roles;
- inverted or malformed date ranges;
- unavailable exact revisions;
- trail entries outside the saved filter snapshot;
- changed query text or accepted ranking identity;
- repeated exact entities inside one trail;
- contradiction candidates comparing the same exact entity;
- automatic contradiction resolution;
- automatic duplicate merging;
- canonical-copy or lifecycle authority escalation;
- live or repository-mutating records.

## Semantic-infrastructure boundary

This candidate does not justify embeddings or vector infrastructure. Those remain deferred until:

1. these research-foundation contracts are accepted;
2. the relevance collection expands beyond 34 entities and 13 queries;
3. hard negatives and candidate-discovery cases are included;
4. any semantic architecture is compared on quality, determinism, inspectability, storage, latency, failure behavior, and replaceability.

## Non-goals

This candidate does not:

- claim production retrieval quality;
- provide a polished research UI;
- copy canonical content into trails;
- prove contradictions or duplicates;
- merge, deprecate, promote, review, or release entities;
- use embeddings, learned ranking, external semantic services, or a vector database;
- activate live Principia synchronization.
