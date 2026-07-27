# Phase 3 Deterministic Lexical Baseline

## Status

```yaml
phase: 3
workstream: 2
mode: retrieval-evaluation
state: candidate
index_contract: atlas-lexical-index/0.1
scoring_contract: atlas-bm25f-scoring/0.1
retrieval_authority: advisory-only
live: false
repository_mutation: false
```

This workstream creates the first ranking baseline against the accepted Phase 3 query set. It does not establish production retrieval quality, select a vector database, activate external services, change judgments, alter canonical content, or grant ranking output lifecycle authority.

## Method

The baseline indexes four transparent fields from every exact canonical entity revision:

```yaml
body: 1.0
id: 1.5
title: 3.0
type: 0.75
```

The tokenizer uses:

- Unicode NFKC normalization;
- case folding;
- the explicit pattern `[a-z0-9]+`;
- a fixed public English stopword list;
- no stemming;
- no query expansion;
- no hidden synonyms;
- no learned normalization.

Scoring uses deterministic BM25F with:

```yaml
k1: 1.2
b: 0.75
tie_break: exact-key-ascending
```

The field weights are declared before evaluation and are not optimized against individual judgments.

## Index contract

```text
atlas-lexical-index/0.1
```

The generated index contains:

- the canonical source contract and source digest;
- all 34 exact entity revisions;
- canonical identity, title, type, lifecycle, review, path, and source-hash fields;
- normalized lexical tokens and field lengths;
- average field lengths;
- exact document frequencies;
- tokenizer and scoring configuration;
- a deterministic build digest;
- `replaceable: true`;
- `canonical_mutation: false`;
- `live: false`.

The index is generated operational state, not canonical knowledge.

## Result evidence

The baseline emits the accepted:

```text
atlas-retrieval-result-set/0.1
```

Every ranked result carries:

- exact ID and positive revision;
- rank and finite BM25F score;
- canonical type, title, status, staleness, and review level;
- sorted matched fields;
- a deterministic scoring explanation;
- exact-revision provenance sources where available;
- the lexical index contract, build digest, and canonical source digest.

Equal scores are ordered by ascending exact entity key.

The unavailable-revision fixture is resolved through exact repository admission and returns the deterministic `E-REVISION-MISSING` response. The harness does not substitute an implicit latest revision.

## Metric evidence

The baseline evaluates the unchanged accepted query set at cutoff 5 and emits:

```text
atlas-retrieval-metric-report/0.1
```

Reported metrics are:

- precision at 5;
- recall at 5;
- mean reciprocal rank;
- nDCG at 5;
- zero-result rate;
- unavailable-revision success rate;
- deterministic tie count.

The metrics describe only the pinned 34-entity, 13-query English reference fixture. They are not production quality estimates.

## Replaceability and rollback

Two independent index builds must be byte-identical. Tests also:

1. write the generated index;
2. delete it;
3. rebuild from canonical Markdown;
4. require byte-identical restored output.

A malformed build digest, changed canonical metadata, inconsistent field length, altered corpus statistic, live authority, or canonical mutation declaration is rejected.

## Explicit exclusions

```yaml
external_services: false
embeddings: false
vector_database: false
learned_ranking: false
query_expansion: false
judgment_specific_tuning: false
canonical_writes: false
lifecycle_mutation: false
principia_live_sync: false
```

## Acceptance boundary

The candidate may be accepted only after:

- lexical tests pass on Python 3.11 and 3.13;
- the exact query set remains unchanged and validates;
- the generated index, result set, metric report, and baseline report validate;
- index deletion and byte-identical rebuild pass;
- exact metrics and digests are pinned on the exact candidate head;
- Foundation, Phase 2, Phase 3 contract, Atlas platform, and end-to-end regressions pass.

Workstream 3 structured retrieval must use the same accepted query-set version and compare against this lexical evidence without rewriting judgments.
