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

The field weights were declared before evaluation and were not optimized against individual judgments.

## Exact candidate evidence

The initial Python 3.11 and Python 3.13 runs produced byte-identical index, result, metric, and report artifacts.

```yaml
source_digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
entity_count: 34
term_count: 424
index_build_digest: 4da6848c020458694db5d26d44be2ddc2580e9c0c41656ce7dcb44a75da82f16
index_artifact_sha256: 4c37fc7e8c90f4a00c9c1f66f5f4472517aeec35547cac76ec0a6b0ad94e6640
result_set_sha256: 400adae2eb62e275a02bb5838fc93964ea8a541e498617527b543f4932c8196c
metric_artifact_sha256: c96a6ab51f06e316d87424f3381833b16563237a957f2a5af38730262e95d0f7
report_artifact_sha256: 6e41b67d303061363c2d6bb6eb7faa225c07feabce1fbc16caf4eceae8bf2d9c
cutoff: 5
limit: 10
tie_count: 0
```

The exact evidence is pinned in:

```text
content/fixtures/phase3_retrieval/lexical-baseline.json
```

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

Equal scores are ordered by ascending exact entity key. The current evidence has zero equal-score adjacent ties.

The unavailable-revision fixture is resolved through exact repository admission and returns the deterministic `E-REVISION-MISSING` response. The harness does not substitute an implicit latest revision.

## Metric evidence

The unchanged accepted query set was evaluated at cutoff 5.

```yaml
precision_at_5: 0.3
recall_at_5: 0.708333333333
mean_reciprocal_rank: 0.652777777778
ndcg_at_5: 0.589071924873
zero_result_rate: 0.0
unavailable_revision_rate: 1.0
tie_count: 0
```

Interpretation:

- the baseline returns at least one lexical result for every ranked query;
- it retrieves about 70.8% of positively judged exact entities within the cutoff on average;
- the first relevant item appears reasonably early on average, but not consistently at rank 1;
- graded ranking quality remains moderate rather than strong;
- the exact unavailable revision is rejected correctly;
- these values describe only the pinned 34-entity, 13-query English reference fixture.

They are not production quality estimates or evidence that lexical retrieval is sufficient.

## Observed limitations

The baseline intentionally preserves its weaknesses instead of tuning the accepted judgments around them.

### Specific evidence can outrank scope

For the catalase optimum-scope query, a specific neutral-pH assay evidence record ranks above the methodological claim explaining why optima require enzyme-source and assay scope.

This shows that surface overlap can favor a concrete example over the intended reasoning boundary.

### Formal models can rank below related prose

For the period-six conditions query, the exact recurrence model is relevant but can rank below the associated claim, evidence, and synthesis records.

Lexical matching recognizes shared terms but does not understand which artifact carries the formal definition.

### Cross-platform scope is weak

For the recommender cross-platform generalization query, the Facebook and Twitter study records rank strongly, while the context-dependence claim and synthesis can fall below the cutoff.

Surface overlap retrieves the named studies more easily than the abstraction limiting their combination.

### Cross-slice abstraction is incomplete

For the cross-domain scope query, the catalase scope target is retrieved, but the recommender context target can be missed within the cutoff.

A lexical baseline can retrieve domain terms while failing to identify a shared methodological structure across domains.

These limitations define concrete comparison targets for Workstream 3 structured retrieval.

## Replaceability and rollback

Two independent index builds are byte-identical. Tests also:

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
- exact metrics and all artifact digests match the pinned baseline on the final exact head;
- Foundation, Phase 2, Phase 3 contract, Atlas platform, and end-to-end regressions pass.

Workstream 3 structured retrieval must use the same accepted query-set version and compare against this lexical evidence without rewriting judgments.
