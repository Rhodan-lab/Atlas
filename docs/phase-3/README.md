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

## Active candidate

Workstream 1 defines the retrieval evaluation boundary before ranking implementation begins.

```yaml
workstream: 1
mode: retrieval-evaluation
state: candidate
query_set_contract: atlas-retrieval-query-set/0.1
result_set_contract: atlas-retrieval-result-set/0.1
metric_report_contract: atlas-retrieval-metric-report/0.1
query_count: 13
entity_count: 34
live: false
repository_mutation: false
```

The candidate includes direct, compositional, ambiguous, cross-slice, and unavailable-revision cases. It does not implement retrieval or claim quality. See [`evaluation-contract.md`](evaluation-contract.md).

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

Phase 3 must define a machine-readable fixture contract containing:

- stable query ID;
- query text;
- language;
- intended information need;
- exact relevant entity IDs and revisions;
- graded or binary relevance judgment;
- rationale;
- slice and difficulty metadata;
- ambiguity or disagreement notes.

Judgments are evaluation fixtures, not new canonical scientific claims.

### Baselines before infrastructure commitments

The first accepted retrieval candidates must include:

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

Embedding, vector, or learned-ranking experiments may begin only after these baselines exist and use the same judgment set.

### Evaluation metrics

The phase must define and report appropriate deterministic metrics, including at minimum:

- precision at a declared cutoff;
- recall at a declared cutoff;
- mean reciprocal rank or an explicitly justified alternative;
- normalized discounted cumulative gain when graded judgments are used;
- zero-result and unavailable-revision rates;
- deterministic tie counts and tie-breaking behavior.

Metrics must be reported with the fixture version and exact index implementation.

### Result contract

Every retrieval result must expose:

- exact entity ID;
- positive revision;
- entity type and title;
- deterministic score and rank;
- matched fields or explanation evidence;
- provenance or source path where applicable;
- review level;
- lifecycle and staleness visibility;
- index contract and build digest.

A result may not silently substitute another revision or an implicit `latest` entity.

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

### Workstream 1 — evaluation contract and fixtures

Candidate scope:

- define query, judgment, result, and metric contracts;
- create a bounded fixture set spanning catalase, delayed feedback, and recommendation systems;
- include straightforward, compositional, ambiguous, cross-slice, and unavailable-revision cases;
- treat every unlisted exact entity as grade 0 over the pinned corpus;
- record explicit fixture limitations;
- reject unversioned results, mismatched metadata, nondeterministic ties, malformed metrics, and live authority.

Acceptance requires exact-head Phase 3 contract CI and the complete Atlas regression suite.

### Workstream 2 — lexical baseline

- tokenize and normalize deterministically;
- index canonical exact revisions;
- implement transparent scoring;
- define deterministic tie-breaking;
- emit inspectable match evidence;
- validate deletion and rebuild.

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
