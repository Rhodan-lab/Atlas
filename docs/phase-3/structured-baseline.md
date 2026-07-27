# Phase 3 Workstream 3 — Structured-Field Retrieval Baseline

## Status

Candidate for bounded retrieval evaluation.

```yaml
phase: 3
workstream: 3
mode: retrieval-evaluation
state: structured-baseline-candidate
retrieval_authority: advisory-only
exact_revision_required: true
canonical_body_indexed: false
accepted_judgments_unchanged: true
external_services: false
embeddings: false
vector_database: false
judgment_specific_tuning: false
live: false
repository_mutation: false
```

## Purpose

Measure whether authored structure and graph context improve retrieval over the accepted lexical baseline without changing the query set, judgments, canonical content, or authority boundaries.

## Indexed fields

The index contains only deterministic, inspectable fields derived from canonical front matter and the compiled graph:

- stable entity ID;
- title;
- entity type;
- substantive authored metadata values and keys;
- lifecycle, confidence, state, staleness, and visible review fields;
- exact outbound references and relations with target identities and titles;
- exact inbound dependent identities and titles;
- provenance-linked source identities, titles, and authored source records.

Canonical Markdown body text is explicitly excluded. This prevents Workstream 3 from becoming a second lexical body index under a different name.

## Scoring

```yaml
algorithm: BM25F
k1: 1.2
b: 0.75
field_weights:
  graph: 1.25
  id: 1.5
  lifecycle: 0.25
  primary: 2.5
  provenance: 1.0
  title: 3.0
  type: 0.75
tie_break: exact-key-ascending
```

The method uses the accepted English tokenizer. It does not use stemming, synonyms, query expansion, embeddings, learned weights, external services, or per-query tuning.

## Pinned evidence

The exact evidence is pinned in `content/fixtures/phase3_retrieval/structured-baseline.json`.

```yaml
index_contract: atlas-structured-index/0.1
scoring_contract: atlas-structured-bm25f-scoring/0.1
entity_count: 34
term_count: 868
cutoff: 5
result_limit: 10
index_build_digest: 91af098baa9bdb6dd6fc55f58f579b6b3be01637562f5797ec1c948a65c748f2
result_set_sha256: 45f215c726e03aa6bfbb1d701291a4a575dd7dc20f435741ec57eb97c939f77c
tie_count: 0
python_evidence_artifacts_byte_identical: true
rebuild_verified: true
replaceable: true
```

Python 3.11 and Python 3.13 produced byte-identical index, result, metric, and report artifacts.

## Metrics

The structured baseline uses the unchanged accepted 13-query fixture: 12 ranked queries and one unavailable-revision error case.

| Metric | Lexical | Structured | Delta |
|---|---:|---:|---:|
| Precision@5 | 0.300000000000 | 0.366666666667 | +0.066666666667 |
| Recall@5 | 0.708333333333 | 0.854166666667 | +0.145833333334 |
| Mean reciprocal rank | 0.652777777778 | 0.770833333333 | +0.118055555555 |
| nDCG@5 | 0.589071924873 | 0.754777384811 | +0.165705459938 |
| Zero-result rate | 0.000000000000 | 0.000000000000 | 0.000000000000 |
| Unavailable-revision rate | 1.000000000000 | 1.000000000000 | 0.000000000000 |

These results show that authored metadata, graph context, and provenance materially improve the bounded reference fixture. They do not establish production search quality or generalization to a larger corpus.

## Preserved limitations

The candidate does not hide unresolved ranking failures:

1. Specific fluorescent-assay evidence still outranks the methodological catalase scope claim for the direct optimum query.
2. The foam-proxy query can rank the question and broad catalase concept above the observation model.
3. Randomized Twitter evidence can outrank the causal claim even when the claim is the more direct answer target.
4. The cross-slice scope query still misses the recommender context-dependent claim within the top-five cutoff.

These limitations become comparison targets for later hybrid or semantic experiments. They are not reasons to alter the accepted judgments after seeing the scores.

## Comparison rule

The structured baseline uses the unchanged accepted query set and compares directly with `content/fixtures/phase3_retrieval/lexical-baseline.json`. A regression must be reported rather than concealed. No query judgment may be rewritten after observing either method.

## Replaceability and validation

The structured index is generated and disposable. Validation reconstructs every indexed field from the canonical runtime, verifies exact identity and metadata, checks graph and provenance content, validates the build digest, rejects authority escalation, and requires deterministic exact-key ordering.

CI builds the index repeatedly, deletes generated output, and requires a byte-identical rebuild from canonical Markdown and accepted fixtures.

## Non-goals

This candidate does not:

- claim production retrieval quality;
- index canonical body text;
- replace canonical authority;
- write lifecycle or review state;
- select a vector database;
- activate live Principia synchronization;
- implement embeddings, hybrid ranking, or learned reranking;
- alter the accepted lexical baseline or relevance judgments.
