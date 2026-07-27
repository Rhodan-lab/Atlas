# Phase 3 — Retrieval Evaluation

## Status

Active after accepted Phase 2 closure evidence.

```yaml
phase: 3
mode: retrieval-evaluation
retrieval_authority: advisory-only
exact_revision_required: true
live: false
canonical_mutation: false
```

## Accepted workstream 1

PR #30 established the retrieval evaluation boundary before ranking implementation.

```yaml
workstream: 1
mode: retrieval-evaluation
state: accepted
query_set_contract: atlas-retrieval-query-set/0.1
result_set_contract: atlas-retrieval-result-set/0.1
metric_report_contract: atlas-retrieval-metric-report/0.1
query_set_id: retrieval-query-set:phase3-reference-en-v1
query_set_version: 1
query_count: 13
entity_count: 34
accepted_pr: 30
tested_head: 3cd4c103da12c140e1a4d0b7bf2bdb8cca5e9727
accepted_merge_commit: 973827e6e7644f79437f3705c73f9e6d83e9a477
live: false
repository_mutation: false
```

The accepted fixture contains 12 ranked queries and one unavailable-revision error, with 26 positive graded targets and 382 implicit grade-0 judgments over the pinned corpus. It includes direct, compositional, ambiguous, cross-slice, contested-normative, and exact-revision-error cases. See [`evaluation-contract.md`](evaluation-contract.md).

## Goal

Evaluate whether Atlas can retrieve relevant, inspectable, versioned knowledge while preserving canonical authority, exact revisions, provenance, review level, lifecycle visibility, deterministic behavior, and index replaceability.

Phase 3 is not a production-search launch. It is a bounded evidence phase.

## Why retrieval begins now

Phase 2 established that the Atlas kernel is deterministic, strictly admitted, safely failing, measurable at larger scale, replay-safe, replaceable, and reproducible from canonical Markdown. Its accepted completion report recommends:

```text
proceed-bounded-retrieval-evaluation
```

That recommendation permits comparative retrieval experiments. It does not permit production claims, live synchronization, canonical writes, unversioned lookup, or automatic lifecycle action.

## Required evidence

### Query and judgment contract

Workstream 1 now provides a machine-readable contract containing:

- stable query-set and query IDs;
- query text and intended information need;
- exact relevant entity IDs and revisions;
- graded relevance judgments and rationales;
- slice and difficulty metadata;
- ambiguity and disagreement notes;
- an exhaustive grade-0 policy over the pinned corpus.

Judgments are evaluation fixtures, not new canonical scientific claims.

### Baselines before infrastructure commitments

The next accepted retrieval candidates must include:

1. a deterministic lexical baseline;
2. a deterministic structured-field baseline.

The structured baseline may use authored and compiled fields such as:

- title;
- entity type;
- canonical metadata;
- claims and questions;
- relations;
- provenance-linked source identity;
- status, staleness, confidence, and review level.

Embedding, vector, or learned-ranking experiments may begin only after these baselines exist and use the same accepted judgment set.

### Evaluation metrics

The accepted metric contract requires:

- precision at a declared cutoff;
- recall at a declared cutoff;
- mean reciprocal rank;
- normalized discounted cumulative gain at the cutoff;
- zero-result and unavailable-revision rates;
- deterministic tie counts and tie-breaking behavior.

Metrics must be reported with the exact fixture version, result-set digest, and index implementation. Workstream 1 defines the fields but does not establish a quality threshold.

### Result contract

Every retrieval result must expose:

- exact entity ID;
- positive revision;
- entity type and title;
- deterministic score and rank;
- matched fields and explanation evidence;
- provenance where applicable;
- review level;
- lifecycle and staleness visibility;
- index contract and build digest.

A result may not silently substitute another revision or an implicit `latest` entity. Equal-score ties use ascending exact entity keys.

### Replaceability and rollback

Every generated retrieval index must be:

- reproducible from canonical Markdown and accepted operational fixtures;
- disposable without knowledge loss;
- validated before query use;
- rebuildable deterministically;
- removable without changing canonical content;
- comparable against the accepted lexical and structured baselines.

Rollback means deleting the generated index and rebuilding it. Mutable index state is never knowledge authority.

## Initial workstreams

### Workstream 1 — evaluation contract and fixtures — accepted

Accepted evidence:

- `content/fixtures/phase3_retrieval/reference-query-set.v01.json`;
- `content/fixtures/phase3_retrieval/contract-baseline.json`;
- `tools/phase3_retrieval/contracts.py`;
- `tools/phase3_retrieval/tests/test_contracts.py`;
- `.github/workflows/phase3-retrieval-contract.yml`;
- `docs/phase-3/evaluation-contract.md`.

The workstream rejects duplicate queries, unavailable positive targets, mismatched revision errors, unversioned results, canonical metadata drift, malformed ranks, increasing scores, nondeterministic ties, malformed metrics, non-replaceable indexes, live authority, and repository mutation.

### Workstream 2 — lexical baseline — next

- use the accepted query set unchanged;
- tokenize and normalize deterministically;
- index canonical exact revisions;
- implement transparent scoring;
- define deterministic tie-breaking;
- emit contract-valid matched-field and provenance evidence;
- compute the accepted metrics;
- validate deletion and byte-identical rebuild;
- record quality limitations without production claims.

### Workstream 3 — structured baseline

- score declared canonical fields and graph relationships;
- preserve exact revisions and provenance;
- compare against lexical results on the same fixture set;
- report gains, regressions, and unresolved query classes.

### Workstream 4 — comparative retrieval experiments

Only after Workstreams 1–3 are accepted:

- test embedding, vector, hybrid, or reranking candidates;
- keep external services optional and replaceable;
- compare quality, determinism, latency, storage, failure behavior, and inspectability;
- reject infrastructure commitment when evidence does not justify it.

## Non-goals

Still out of scope:

- production search quality claims;
- polished search UI;
- personalized ranking;
- user profiling;
- autonomous agents changing knowledge state;
- live Principia synchronization;
- retrieval-generated canonical content;
- automatic review, lifecycle, promotion, or release mutation;
- active multilingual retrieval;
- choosing a vector database by popularity rather than evidence.

## Authority boundary

```yaml
canonical_authority: content/canonical/**/*.md
retrieval_index: generated-and-replaceable
retrieval_result: advisory-only
exact_revision_required: true
principia_live_dependency: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

## Exit criteria

Phase 3 closes only when:

- the query-and-judgment set is versioned and validated;
- lexical and structured baselines are accepted;
- results preserve exact revisions and visible provenance;
- deterministic metrics and tie behavior are recorded;
- malformed indexes and unavailable revisions fail safely;
- index deletion and canonical rebuild are tested;
- any vector or learned candidate is compared against accepted baselines;
- the completion report recommends or rejects broader retrieval work;
- no retrieval result is granted canonical or lifecycle authority.
