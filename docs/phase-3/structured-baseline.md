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
external_services: false
embeddings: false
vector_database: false
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

## Comparison rule

The structured baseline must use the unchanged accepted query set and compare its metrics directly with `content/fixtures/phase3_retrieval/lexical-baseline.json`.

Metrics:

- precision@5;
- recall@5;
- mean reciprocal rank;
- nDCG@5;
- zero-result rate;
- unavailable-revision rate;
- deterministic tie count.

A metric regression must be reported, not concealed. No query judgment may be rewritten after observing either method.

## Replaceability

The structured index is generated and disposable. CI builds it twice, validates exact canonical agreement, deletes generated output, and requires a byte-identical rebuild from canonical Markdown and accepted fixtures.

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
