# Phase 3 — Retrieval Evaluation

## Status

```yaml
phase: 3
mode: retrieval-evaluation
accepted_workstreams: [1, 2, 3]
workstream_4_candidate_1: evaluated-rejected
active_workstream: 5
preferred_bounded_ranking: structured-field-baseline
retrieval_authority: advisory-only
exact_revision_required: true
live: false
canonical_mutation: false
```

Phase 3 is not a production-search launch. It is a bounded evidence phase over a 34-entity English reference corpus.

## Workstream 1 — accepted evaluation contract

PR #30 established the retrieval evaluation boundary, and PR #31 finalized its governance record.

```yaml
query_set_contract: atlas-retrieval-query-set/0.1
result_set_contract: atlas-retrieval-result-set/0.1
metric_report_contract: atlas-retrieval-metric-report/0.1
query_set_id: retrieval-query-set:phase3-reference-en-v1
query_set_version: 1
query_count: 13
ranked_query_count: 12
expected_error_query_count: 1
entity_count: 34
positive_judgment_count: 26
implicit_grade_zero_judgment_count: 382
state: accepted
```

The fixture includes direct, compositional, ambiguous, cross-slice, contested-normative, and exact-revision-error cases. See [`evaluation-contract.md`](evaluation-contract.md).

## Workstream 2 — accepted lexical baseline

PR #32 established the lexical baseline, and PR #33 finalized its governance record.

```yaml
index_contract: atlas-lexical-index/0.1
tokenizer_contract: atlas-english-tokenizer/0.1
scoring_contract: atlas-bm25f-scoring/0.1
state: accepted
accepted_pr: 32
tested_head: 2fb6a5cb31cc98b9daac942a1745a9bd9effe9ff
accepted_merge_commit: 444011821969285da78e6c7fc4ceadec1efca322
entity_count: 34
term_count: 424
precision_at_5: 0.3
recall_at_5: 0.708333333333
mean_reciprocal_rank: 0.652777777778
ndcg_at_5: 0.589071924873
zero_result_rate: 0.0
unavailable_revision_rate: 1.0
tie_count: 0
replaceable: true
rebuild_verified: true
quality_claim: bounded-reference-fixture-only
```

The tokenizer uses NFKC case folding, `[a-z0-9]+`, a fixed English stopword list, no stemming, and no query expansion. BM25F scores body, stable ID, title, and type with fixed public weights.

Evidence: `content/fixtures/phase3_retrieval/lexical-baseline.json` and [`lexical-baseline.md`](lexical-baseline.md).

## Workstream 3 — accepted structured-field baseline

PR #34 established the structured baseline, and PR #35 finalized its governance record.

```yaml
index_contract: atlas-structured-index/0.1
scoring_contract: atlas-structured-bm25f-scoring/0.1
state: accepted
accepted_pr: 34
tested_head: d7b7c10338ff68121f7fb7532f3799adfa72c404
accepted_merge_commit: a8212512261ed3d718ee14c1fa40e30277f62b75
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
replaceable: true
rebuild_verified: true
quality_claim: bounded-reference-fixture-only
```

The structured index scores stable identity, title, type, substantive front-matter values, lifecycle and review fields, outbound graph references and relations, inbound dependents, and provenance-linked source identity. Canonical body text is excluded.

This is the preferred accepted ranking baseline for the current fixture. It is not a production-quality claim.

Evidence: `content/fixtures/phase3_retrieval/structured-baseline.json` and [`structured-baseline.md`](structured-baseline.md).

## Workstream 4 candidate 1 — reciprocal-rank fusion — evaluated and rejected

PR #36 evaluated the method declared before scoring:

```yaml
method: reciprocal-rank-fusion
rrf_k: 60
lexical_weight: 1.0
structured_weight: 1.0
input_limit: 10
output_limit: 10
raw_score_blending: false
query_set: unchanged
judgments: unchanged
tie_break: exact-key-ascending
```

Pinned result:

```yaml
state: evaluated-rejected
tested_head: cec57a7a090dbdc8238a19a21f9d84e38a836917
evidence_merge_commit: e6010893112b10362a15392d8635a0297b055267
recommendation: reject-candidate-no-quality-gain-over-structured
manifest_build_digest: 1ad4dbab8ab538d44a3e09e263b9c116687c9d4cfb5d4254ca88305565b64d6e
result_set_sha256: 7193a359331d06205695798716452b91955029f5cd904181ea1f96913b1aef1c
precision_at_5: 0.35
recall_at_5: 0.791666666667
mean_reciprocal_rank: 0.736111111111
ndcg_at_5: 0.678019431236
zero_result_rate: 0.0
unavailable_revision_rate: 1.0
tie_count: 9
precision_delta_from_structured: -0.016666666667
recall_delta_from_structured: -0.0625
mrr_delta_from_structured: -0.034722222222
ndcg_delta_from_structured: -0.076757953575
query_gains_vs_structured: 2
query_mixed_vs_structured: 1
query_regressions_vs_structured: 7
query_unchanged_vs_structured: 2
additional_index_documents: 0
additional_index_terms: 0
python_evidence_artifacts_byte_identical: true
```

Fusion improves all four core metrics over lexical retrieval but loses all four to structured retrieval. Under the predeclared rule, the extra layer is rejected as the preferred method. No post-hoc weight or judgment change is permitted.

Evidence: `content/fixtures/phase3_retrieval/rank-fusion.json` and [`rank-fusion.md`](rank-fusion.md).

## Workstream 5 — active research trails and candidate discovery

The authoritative Phase 3 gate also requires filters, saved research trails, and contradiction or duplicate candidates. These foundations must exist before Phase 3 can close or semantic infrastructure can be justified.

### Filter contract

Required deterministic dimensions:

```yaml
filters:
  - entity-type
  - status
  - domain
  - date
  - evidence-role
exact_revision_preserved: true
provenance_visible: true
review_and_staleness_visible: true
implicit_latest: forbidden
```

Filtering may narrow advisory results. It may not rewrite ranks, hide status, replace revisions, or mutate canonical content.

### Saved research-trail contract

A trail is a versioned research record containing:

- stable trail ID and revision;
- query and filter snapshot;
- exact selected entity revisions;
- exclusions and rationale;
- ranking and explanation snapshot;
- notes, open questions, and decision state;
- provenance-visible references;
- created and updated timestamps.

A trail stores references and research decisions. It may not copy canonical knowledge into a new authority, promote lifecycle state, or silently follow `latest` revisions.

### Candidate-discovery contracts

Two advisory candidate types are required:

```yaml
contradiction_candidate:
  authority: advisory-only
  required: [exact-revisions, compared-statements, scope-analysis, evidence-paths, rationale]
  automatic_resolution: forbidden
duplicate_candidate:
  authority: advisory-only
  required: [exact-revisions, similarity-basis, semantic-differences, provenance, rationale]
  automatic_merge: forbidden
```

A candidate means “inspect this possible relationship,” not “a contradiction or duplicate has been proven.”

### Workstream 5 evidence

The workstream must include:

- valid filter, trail, contradiction-candidate, and duplicate-candidate fixtures;
- malformed, unavailable-revision, stale-revision, ambiguous-scope, and authority-escalation negatives;
- deterministic validation on Python 3.11 and 3.13;
- replaceable generated reports;
- no canonical, review, lifecycle, merge, or release mutation.

## Semantic infrastructure decision

Embedding, vector, learned-ranking, and external semantic-service experiments remain deferred until:

1. Workstream 5 contracts are accepted;
2. the relevance collection is broadened beyond 34 entities and 13 queries;
3. hard negatives and candidate-discovery cases are included;
4. the architecture decision compares quality, determinism, inspectability, storage, latency, failure behavior, and replaceability.

No vector database is selected by the current evidence.

## Evidence files

### Workstream 1 — accepted

- `content/fixtures/phase3_retrieval/reference-query-set.v01.json`;
- `content/fixtures/phase3_retrieval/contract-baseline.json`;
- `tools/phase3_retrieval/contracts.py`;
- `.github/workflows/phase3-retrieval-contract.yml`;
- `docs/phase-3/evaluation-contract.md`.

### Workstream 2 — accepted

- `content/fixtures/phase3_retrieval/lexical-baseline.json`;
- `tools/phase3_retrieval/lexical.py`;
- `.github/workflows/phase3-lexical-baseline.yml`;
- `docs/phase-3/lexical-baseline.md`.

### Workstream 3 — accepted

- `content/fixtures/phase3_retrieval/structured-baseline.json`;
- `tools/phase3_retrieval/structured.py`;
- `.github/workflows/phase3-structured-baseline.yml`;
- `docs/phase-3/structured-baseline.md`.

### Workstream 4 candidate 1 — evaluated and rejected

- `content/fixtures/phase3_retrieval/rank-fusion.json`;
- `tools/phase3_retrieval/fusion.py`;
- `.github/workflows/phase3-rank-fusion.yml`;
- `docs/phase-3/rank-fusion.md`.

## Non-goals

Still out of scope:

- production search-quality claims;
- polished search UI;
- personalized ranking or user profiling;
- autonomous agents changing knowledge state;
- live Principia synchronization;
- retrieval-generated canonical content;
- automatic review, lifecycle, promotion, merge, or release mutation;
- active multilingual retrieval;
- post-hoc tuning against accepted judgments;
- vector database selection without broader comparative evidence.

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

## Exit criteria

Phase 3 closes only when:

- the query-and-judgment set is versioned and validated;
- lexical and structured baselines are accepted;
- comparative candidates are measured against both accepted baselines;
- filtering preserves exact revisions and visible authority metadata;
- saved research trails are exact-revision and inspectable;
- contradiction and duplicate candidates remain advisory and evidence-linked;
- deterministic metrics, ties, failures, and rebuild behavior are recorded;
- the completion report recommends or rejects entry into Phase 4;
- no retrieval result, trail, or candidate is granted canonical or lifecycle authority.
