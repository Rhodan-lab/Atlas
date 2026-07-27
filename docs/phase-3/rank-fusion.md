# Phase 3 Workstream 4 — Reciprocal-Rank Fusion Candidate

## Status

Bounded comparative candidate.

```yaml
phase: 3
workstream: 4
mode: retrieval-evaluation
state: rank-fusion-candidate
method: reciprocal-rank-fusion
rrf_k: 60
lexical_weight: 1.0
structured_weight: 1.0
retrieval_authority: advisory-only
exact_revision_required: true
external_services: false
embeddings: false
vector_database: false
learned_weights: false
judgment_specific_tuning: false
live: false
repository_mutation: false
```

## Purpose

Test whether combining the accepted lexical and structured rank positions improves the unchanged Phase 3 benchmark enough to justify the added comparison layer before any embedding or vector experiment.

## Method

For each exact entity ranked by either accepted method:

```text
score(entity) = 1 / (60 + lexical_rank) + 1 / (60 + structured_rank)
```

A missing component contributes zero. The method does not blend raw BM25 scores because the lexical and structured score scales are not directly comparable.

The candidate uses:

- accepted lexical ranking, top 10;
- accepted structured ranking, top 10;
- equal weights fixed before evaluation;
- `k = 60` fixed before evaluation;
- exact-key ascending tie handling;
- the unchanged accepted query set and judgments.

## Inspectability

Every fused result exposes:

- exact entity ID and revision;
- canonical metadata and provenance;
- lexical component rank and contribution when present;
- structured component rank and contribution when present;
- source-prefixed matched fields;
- total deterministic RRF score.

## Complexity boundary

The candidate creates no new searchable index, terms, embeddings, learned model, external calls, or vector infrastructure. It produces only a replaceable manifest, result set, metric report, and comparison report.

## Evaluation

The candidate must report:

- precision@5;
- recall@5;
- mean reciprocal rank;
- nDCG@5;
- zero-result and unavailable-revision rates;
- deterministic tie count;
- deltas from lexical and structured baselines;
- per-query gains, regressions, mixed results, and unchanged results;
- deterministic artifact sizes and input/output ranking work;
- failure and inspectability behavior.

## Decision rule

The candidate is not automatically accepted because it combines two methods.

- Retain when it improves or matches all core structured metrics and improves at least one.
- Reject when every core metric is no better than the accepted structured baseline.
- Require query-level review when aggregate results are mixed.

The decision remains bounded to the 34-entity, 13-query reference fixture.

## Non-goals

This candidate does not:

- claim production retrieval quality;
- change either accepted baseline;
- alter query judgments;
- train or tune weights;
- use embeddings or a vector database;
- write canonical or lifecycle state;
- activate live Principia synchronization.
