# Phase 3 Workstream 4 — Reciprocal-Rank Fusion Candidate

## Decision

**Rejected as the preferred retrieval method for this fixture.**

```yaml
phase: 3
workstream: 4
mode: retrieval-evaluation
state: evaluated-rejected
method: reciprocal-rank-fusion
rrf_k: 60
lexical_weight: 1.0
structured_weight: 1.0
recommendation: reject-candidate-no-quality-gain-over-structured
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

The rejected decision follows the rule declared before evaluation: reject when every core metric is no better than the accepted structured baseline. No value of `k`, component weight, query judgment, or input ranking was changed after observing results.

## Purpose

Test whether combining the accepted lexical and structured rank positions improves the unchanged Phase 3 benchmark enough to justify an extra fusion layer before any embedding or vector experiment.

## Method

For each exact entity ranked by either accepted method:

```text
score(entity) = 1 / (60 + lexical_rank) + 1 / (60 + structured_rank)
```

A missing component contributes zero. Raw BM25 scores are not blended because lexical and structured scores have different scales.

The candidate used:

- accepted lexical ranking, top 10;
- accepted structured ranking, top 10;
- equal weights fixed before evaluation;
- `k = 60` fixed before evaluation;
- exact-key ascending tie handling;
- the unchanged accepted query set and judgments.

## Pinned evidence

Exact evidence is pinned in `content/fixtures/phase3_retrieval/rank-fusion.json`.

```yaml
manifest_contract: atlas-rank-fusion-manifest/0.1
scoring_contract: atlas-reciprocal-rank-fusion/0.1
entity_count: 34
query_count: 13
ranked_query_count: 12
cutoff: 5
result_limit: 10
manifest_build_digest: 1ad4dbab8ab538d44a3e09e263b9c116687c9d4cfb5d4254ca88305565b64d6e
result_set_sha256: 7193a359331d06205695798716452b91955029f5cd904181ea1f96913b1aef1c
tie_count: 9
python_evidence_artifacts_byte_identical: true
additional_index_documents: 0
additional_index_terms: 0
embedding_dimensions: 0
external_calls: 0
replaceable: true
```

Python 3.11 and Python 3.13 produced byte-identical manifest, result, metric, and report artifacts.

## Aggregate comparison

| Metric | Lexical | Structured | Fusion | Fusion vs lexical | Fusion vs structured |
|---|---:|---:|---:|---:|---:|
| Precision@5 | 0.300000000000 | 0.366666666667 | 0.350000000000 | +0.050000000000 | -0.016666666667 |
| Recall@5 | 0.708333333333 | 0.854166666667 | 0.791666666667 | +0.083333333334 | -0.062500000000 |
| Mean reciprocal rank | 0.652777777778 | 0.770833333333 | 0.736111111111 | +0.083333333333 | -0.034722222222 |
| nDCG@5 | 0.589071924873 | 0.754777384811 | 0.678019431236 | +0.088947506363 | -0.076757953575 |
| Zero-result rate | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 | 0.000000000000 |
| Unavailable-revision rate | 1.000000000000 | 1.000000000000 | 1.000000000000 | 0.000000000000 | 0.000000000000 |

Fusion improves all four core metrics over lexical retrieval, but loses all four to structured retrieval. The extra layer therefore does not become the preferred baseline.

## Query-level findings

Against lexical retrieval:

```yaml
gain: 7
unchanged: 4
mixed: 0
regression: 1
```

Against structured retrieval:

```yaml
gain: 2
unchanged: 2
mixed: 1
regression: 7
```

The two gains over structured retrieval are:

- `query:retrieval:catalase-foam-proxy`;
- `query:retrieval:recommender-twitter-causal`.

The structured baseline remains stronger on seven queries, especially those requiring methodological scope, model-to-world boundaries, full exposure pathways, explanation-and-choice context, and cross-domain abstraction.

The cross-platform recommender query is mixed: fusion retrieves all four relevant targets inside the cutoff, improving recall over structured retrieval, but orders them less effectively and therefore reduces nDCG.

## Inspectability

Every fused result exposes:

- exact entity ID and revision;
- canonical metadata and provenance;
- lexical component rank and contribution when present;
- structured component rank and contribution when present;
- source-prefixed matched fields;
- total deterministic RRF score.

## Complexity and failure behavior

```yaml
input_ranked_items: 230
output_ranked_items: 118
manifest_bytes: 1855
result_set_bytes: 106273
metric_report_bytes: 633
additional_index_documents: 0
additional_index_terms: 0
embedding_dimensions: 0
external_calls: 0
```

The candidate creates no searchable index, embeddings, learned model, external call, or vector infrastructure. It still adds a fusion manifest, a large fused result artifact, a comparison report, and nine deterministic score ties.

Validation rejects:

- changed accepted baseline identities or build digests;
- changed `k`, weights, input limit, output limit, or tie rule;
- manifest digest mismatch;
- unavailable-revision disagreement between inputs;
- authority escalation or repository mutation.

## Interpretation

The negative result is useful. Lexical evidence can repair particular structured failures, but equal-weight global rank fusion dilutes the structured method’s stronger performance on more queries. This suggests that later work should not merely combine methods uniformly.

Any later semantic, hybrid, or reranking candidate must be separately predeclared and compared against the accepted structured baseline. This result does not justify a vector database commitment.

## Non-goals

This evaluated candidate does not:

- claim production retrieval quality;
- change either accepted baseline;
- alter query judgments;
- train or tune weights;
- use embeddings or a vector database;
- write canonical or lifecycle state;
- activate live Principia synchronization.
