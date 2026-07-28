# Phase 3 — Retrieval and Research Trails

## Status

**Accepted and closed through PR #40.**

```yaml
phase: 3
mode: retrieval-evaluation
state: accepted
accepted_pr: 40
tested_head: 4f69697065f66ecb8f797616523673d39c8976e1
accepted_merge_commit: 52f51558a9188f049f4b4b838bc6acfd1a991e96
accepted_workstreams: [1, 2, 3, 5]
evaluated_rejected_workstream_4_candidate: equal-weight-reciprocal-rank-fusion
preferred_bounded_retrieval: structured-field-baseline
semantic_infrastructure_decision: defer-until-broader-benchmark-and-architecture-approval
retrieval_authority: advisory-only
exact_revision_required: true
replaceable: true
live: false
repository_mutation: false
```

Phase 3 was a bounded evidence phase over a 34-entity English reference corpus. It did not launch production search.

## Accepted Workstream 1 — evaluation contract

PR #30 established the query, result, and metric contracts; PR #31 finalized their governance record.

```yaml
query_set_contract: atlas-retrieval-query-set/0.1
result_set_contract: atlas-retrieval-result-set/0.1
metric_report_contract: atlas-retrieval-metric-report/0.1
query_set_id: retrieval-query-set:phase3-reference-en-v1
query_set_version: 1
entity_count: 34
query_count: 13
ranked_query_count: 12
expected_error_query_count: 1
positive_judgment_count: 26
implicit_grade_zero_judgment_count: 382
judgment_authority: evaluation-only
```

The fixture includes direct, compositional, ambiguous, cross-slice, contested-normative, and unavailable-revision cases.

## Accepted Workstream 2 — lexical baseline

PR #32 established deterministic lexical BM25F retrieval; PR #33 finalized the accepted record.

```yaml
index_contract: atlas-lexical-index/0.1
tokenizer_contract: atlas-english-tokenizer/0.1
scoring_contract: atlas-bm25f-scoring/0.1
entity_count: 34
term_count: 424
precision_at_5: 0.3
recall_at_5: 0.708333333333
mean_reciprocal_rank: 0.652777777778
ndcg_at_5: 0.589071924873
zero_result_rate: 0.0
unavailable_revision_rate: 1.0
tie_count: 0
rebuild_verified: true
replaceable: true
external_services: false
embeddings: false
vector_database: false
```

## Accepted Workstream 3 — structured-field baseline

PR #34 established deterministic structured-field BM25F retrieval; PR #35 finalized the accepted record.

```yaml
index_contract: atlas-structured-index/0.1
scoring_contract: atlas-structured-bm25f-scoring/0.1
entity_count: 34
term_count: 868
canonical_body_indexed: false
precision_at_5: 0.366666666667
recall_at_5: 0.854166666667
mean_reciprocal_rank: 0.770833333333
ndcg_at_5: 0.754777384811
zero_result_rate: 0.0
unavailable_revision_rate: 1.0
tie_count: 0
precision_delta_from_lexical: 0.066666666667
recall_delta_from_lexical: 0.145833333334
mrr_delta_from_lexical: 0.118055555555
ndcg_delta_from_lexical: 0.165705459938
rebuild_verified: true
replaceable: true
```

The structured method indexes identity, title, type, substantive metadata, lifecycle and review fields, graph neighborhood, and provenance-linked source identity. Canonical body text is excluded.

It is the preferred bounded method for the accepted fixture. This is not a production-quality claim.

## Workstream 4 candidate 1 — evaluated and rejected

PR #36 evaluated equal-weight reciprocal-rank fusion over the accepted lexical and structured rankings. PR #37 recorded the rejection and activated Workstream 5.

```yaml
method: reciprocal-rank-fusion
rrf_k: 60
lexical_weight: 1.0
structured_weight: 1.0
state: evaluated-rejected
precision_at_5: 0.35
recall_at_5: 0.791666666667
mean_reciprocal_rank: 0.736111111111
ndcg_at_5: 0.678019431236
precision_delta_from_structured: -0.016666666667
recall_delta_from_structured: -0.0625
mrr_delta_from_structured: -0.034722222222
ndcg_delta_from_structured: -0.076757953575
query_gains_vs_structured: 2
query_mixed_vs_structured: 1
query_regressions_vs_structured: 7
query_unchanged_vs_structured: 2
recommendation: reject-candidate-no-quality-gain-over-structured
```

The negative result is retained. No post-hoc tuning was accepted.

## Accepted Workstream 5 — research trails and candidate discovery

PR #38 established the remaining research-foundation contracts.

```yaml
filter_contract: atlas-retrieval-filter/0.1
filtered_result_contract: atlas-filtered-result-set/0.1
research_trail_contract: atlas-research-trail/0.1
contradiction_candidate_contract: atlas-contradiction-candidate/0.1
duplicate_candidate_contract: atlas-duplicate-candidate/0.1
filters: 4
filter_result_items: 9
trails: 1
trail_entries: 5
contradiction_candidates: 1
duplicate_candidates: 1
negative_cases: 5
report_digest: 733aeb28a3147a36d1cc7d3406ab98fa81522cb4b4e87e3aa792aaf54893a394
exact_revision_preserved: true
provenance_visible: true
review_and_staleness_visible: true
canonical_copy_authority: false
automatic_merge_or_resolution: false
```

The contradiction candidate is assessed `scope-difference-likely`; the duplicate candidate is assessed `related-not-duplicate`. Candidate output remains advisory and never resolves or mutates canonical knowledge automatically.

## Closure evidence

PR #40 added the deterministic completion report and pinned baseline.

```yaml
completion_contract: atlas-phase3-completion-report/0.1
completion_baseline_contract: atlas-phase3-completion-baseline/0.1
source_digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
decision: proceed-phase4-interactive-experience
accepted_workstreams: [1, 2, 3, 5]
preferred_bounded_retrieval: structured-field-baseline
semantic_infrastructure_decision: defer-until-broader-benchmark-and-architecture-approval
```

Passed exit gates:

```yaml
documented_relevance_collection: true
review_status_and_provenance_visible: true
ranking_behavior_explainable: true
specialized_boundaries_pass_policy: true
retrieval_failure_cannot_corrupt_authority: true
filters_and_research_trails_operational: true
candidate_discovery_advisory: true
generated_artifacts_replaceable: true
```

## Authority boundary

```yaml
canonical_authority: content/canonical/**/*.md
retrieval_indexes: generated-and-replaceable
retrieval_results: advisory-only
research_trails: exact-revision-references-not-canonical-copies
candidate_discovery: advisory-only
exact_revision_required: true
principia_live_dependency: false
automatic_status_change: false
automatic_merge_or_resolution: false
automatic_release_action: false
repository_mutation: false
```

## Deferred work

Phase 3 did not justify:

- production retrieval-quality claims;
- embeddings or learned ranking;
- a vector database;
- external semantic services;
- post-hoc judgment tuning;
- live Principia synchronization;
- retrieval-generated canonical writes;
- automatic lifecycle or review mutation;
- a polished product UI.

A future semantic experiment requires a broader corpus, more queries, hard negatives, candidate-discovery benchmarks, and a separate architecture decision.

## Evidence files

- `content/fixtures/phase3_retrieval/reference-query-set.v01.json`;
- `content/fixtures/phase3_retrieval/contract-baseline.json`;
- `content/fixtures/phase3_retrieval/lexical-baseline.json`;
- `content/fixtures/phase3_retrieval/structured-baseline.json`;
- `content/fixtures/phase3_retrieval/rank-fusion.json`;
- `content/fixtures/phase3_retrieval/research-foundations.v01.json`;
- `content/fixtures/phase3_retrieval/research-foundations-baseline.json`;
- `content/fixtures/phase3_retrieval/phase3-completion-baseline.json`;
- `tools/phase3_retrieval/`;
- `.github/workflows/phase3-*.yml`;
- `docs/phase-3/completion-report.md`.

**Phase 3 is complete. Phase 4 may expose the accepted semantics through a local-first, accessible, failure-visible interactive experience while keeping Atlas and Principia status separate.**
