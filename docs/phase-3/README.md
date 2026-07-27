# Phase 3 — Retrieval Evaluation

## Status

Active after accepted Phase 2 closure evidence.

```yaml
phase: 3
mode: retrieval-evaluation
accepted_workstreams: [1, 2, 3]
active_workstream: 4
retrieval_authority: advisory-only
exact_revision_required: true
live: false
canonical_mutation: false
```

## Accepted Workstream 1 — evaluation contract

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
live: false
repository_mutation: false
```

The accepted fixture includes direct, compositional, ambiguous, cross-slice, contested-normative, and exact-revision-error cases. See [`evaluation-contract.md`](evaluation-contract.md).

## Accepted Workstream 2 — lexical baseline

PR #32 established the first transparent ranking baseline, and PR #33 finalized its governance record.

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
cutoff: 5
result_limit: 10
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
external_services: false
embeddings: false
vector_database: false
live: false
repository_mutation: false
```

The tokenizer uses NFKC case folding, `[a-z0-9]+`, a fixed English stopword list, no stemming, and no query expansion. BM25F scores body, stable ID, title, and type with fixed public weights and exact-key ascending ties.

The exact evidence is pinned in `content/fixtures/phase3_retrieval/lexical-baseline.json`. See [`lexical-baseline.md`](lexical-baseline.md).

## Accepted Workstream 3 — structured-field baseline

PR #34 established the structured-field baseline over the unchanged accepted query set.

```yaml
index_contract: atlas-structured-index/0.1
scoring_contract: atlas-structured-bm25f-scoring/0.1
state: accepted
accepted_pr: 34
tested_head: d7b7c10338ff68121f7fb7532f3799adfa72c404
accepted_merge_commit: a8212512261ed3d718ee14c1fa40e30277f62b75
entity_count: 34
term_count: 868
cutoff: 5
result_limit: 10
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
canonical_body_indexed: false
accepted_judgments_unchanged: true
python_evidence_artifacts_byte_identical: true
replaceable: true
rebuild_verified: true
quality_claim: bounded-reference-fixture-only
external_services: false
embeddings: false
vector_database: false
judgment_specific_tuning: false
live: false
repository_mutation: false
```

The structured index scores stable identity, title, type, substantive front-matter values, lifecycle and review fields, outbound graph references and relations, inbound dependents, and provenance-linked source identity. Canonical Markdown body text is excluded and validation reconstructs every field from the canonical runtime.

The exact evidence is pinned in `content/fixtures/phase3_retrieval/structured-baseline.json`. See [`structured-baseline.md`](structured-baseline.md).

The aggregate improvement is accepted as bounded fixture evidence, not a production estimate. Remaining failures are preserved: evidence can outrank methodological or causal claims, and the cross-slice query still misses one context-dependent target inside the top five.

## Active Workstream 4 — comparative retrieval experiments

The first candidate is declared before evaluation:

```yaml
candidate: deterministic-rank-fusion
method: reciprocal-rank-fusion
rrf_k: 60
lexical_weight: 1.0
structured_weight: 1.0
inputs: accepted-exact-result-rankings
query_set: unchanged
judgments: unchanged
tie_break: exact-key-ascending
external_services: false
embeddings: false
vector_database: false
learned_weights: false
judgment_specific_tuning: false
retrieval_authority: advisory-only
live: false
repository_mutation: false
```

This bounded hybrid must compare against both accepted baselines, preserve exact revisions and provenance, report aggregate and query-level gains and regressions, and justify its added complexity. It must be rejected when evidence does not support it.

Embedding or vector experiments remain separate later candidates. No vector database is selected by Workstream 4 entry.

## Goal

Evaluate whether Atlas can retrieve relevant, inspectable, versioned knowledge while preserving canonical authority, exact revisions, provenance, review level, lifecycle visibility, deterministic behavior, and index replaceability.

Phase 3 is not a production-search launch. It is a bounded evidence phase.

## Accepted evidence requirements

### Query and judgment contract

Workstream 1 provides stable query and query-set IDs, exact graded targets, explicit ambiguity records, and an exhaustive grade-0 policy over the pinned corpus. Judgments are evaluation fixtures rather than canonical scientific claims.

### Result contract

Every result must expose exact ID and revision, deterministic score and rank, canonical metadata, matched fields, explanation evidence, provenance, review level, lifecycle, staleness, index contract, build digest, and canonical source digest.

A result may not substitute an implicit `latest` revision. Equal scores use ascending exact keys.

### Metric contract

Reports bind the exact query-set version and result-set digest and expose precision, recall, MRR, nDCG, zero-result rate, unavailable-revision rate, and deterministic tie count.

### Replaceability

Every index and comparison artifact must be reproducible, disposable, validated before query use, byte-identically rebuildable, removable without canonical mutation, and comparable against accepted baselines.

## Evidence files

### Workstream 1 — accepted

- `content/fixtures/phase3_retrieval/reference-query-set.v01.json`;
- `content/fixtures/phase3_retrieval/contract-baseline.json`;
- `tools/phase3_retrieval/contracts.py`;
- `tools/phase3_retrieval/tests/test_contracts.py`;
- `.github/workflows/phase3-retrieval-contract.yml`;
- `docs/phase-3/evaluation-contract.md`.

### Workstream 2 — accepted

- `content/fixtures/phase3_retrieval/lexical-baseline.json`;
- `tools/phase3_retrieval/lexical.py`;
- `tools/phase3_retrieval/tests/test_lexical.py`;
- `.github/workflows/phase3-lexical-baseline.yml`;
- `docs/phase-3/lexical-baseline.md`.

### Workstream 3 — accepted

- `content/fixtures/phase3_retrieval/structured-baseline.json`;
- `tools/phase3_retrieval/structured.py`;
- `tools/phase3_retrieval/tests/test_structured.py`;
- `.github/workflows/phase3-structured-baseline.yml`;
- `docs/phase-3/structured-baseline.md`.

## Non-goals

Still out of scope:

- production search-quality claims;
- polished search UI;
- personalized ranking or user profiling;
- autonomous agents changing knowledge state;
- live Principia synchronization;
- retrieval-generated canonical content;
- automatic review, lifecycle, promotion, or release mutation;
- active multilingual retrieval;
- vector database selection before comparative evidence.

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
- comparative candidates are measured against both accepted baselines;
- results preserve exact revisions and visible provenance;
- deterministic metrics and tie behavior are recorded;
- malformed indexes and unavailable revisions fail safely;
- deletion and canonical rebuild are tested;
- any vector or learned candidate is compared against accepted baselines;
- the completion report recommends or rejects broader retrieval work;
- no retrieval result is granted canonical or lifecycle authority.
