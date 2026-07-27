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

## Accepted workstream 1 — evaluation contract

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

## Accepted workstream 2 — lexical baseline

PR #32 established the first transparent ranking baseline over the unchanged accepted query set.

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

The tokenizer uses NFKC case folding, `[a-z0-9]+`, a fixed English stopword list, no stemming, and no query expansion. The BM25F baseline scores body, stable ID, title, and entity type with public fixed weights and exact-key ascending tie handling.

The exact evidence is pinned in `content/fixtures/phase3_retrieval/lexical-baseline.json`. Full method, digests, metrics, and limitations are recorded in [`lexical-baseline.md`](lexical-baseline.md).

The accepted metrics are not production quality estimates. The baseline exposes moderate ranking quality and specific weaknesses in methodological scope, formal-model prioritization, cross-platform context, and cross-slice abstraction.

## Goal

Evaluate whether Atlas can retrieve relevant, inspectable, versioned knowledge while preserving canonical authority, exact revisions, provenance, review level, lifecycle visibility, deterministic behavior, and index replaceability.

Phase 3 is not a production-search launch. It is a bounded evidence phase.

## Accepted evidence requirements

### Query and judgment contract

Workstream 1 provides stable query-set and query IDs, exact graded targets, explicit ambiguity records, and an exhaustive grade-0 policy over the pinned corpus. Judgments are evaluation fixtures rather than canonical scientific claims.

### Result contract

Every result must expose exact ID and revision, deterministic score and rank, canonical metadata, matched fields, explanation evidence, provenance, review level, lifecycle, staleness, index contract, build digest, and canonical source digest.

A result may not substitute an implicit `latest` revision. Equal scores use ascending exact keys.

### Metric contract

Reports bind the exact query-set version and result-set digest and expose precision, recall, MRR, nDCG, zero-result rate, unavailable-revision rate, and deterministic tie count.

### Replaceability

Every index must be reproducible, disposable, validated before query use, byte-identically rebuildable, removable without canonical mutation, and comparable against accepted baselines.

## Workstreams

### Workstream 1 — evaluation contract and fixtures — accepted

Accepted evidence:

- `content/fixtures/phase3_retrieval/reference-query-set.v01.json`;
- `content/fixtures/phase3_retrieval/contract-baseline.json`;
- `tools/phase3_retrieval/contracts.py`;
- `tools/phase3_retrieval/tests/test_contracts.py`;
- `.github/workflows/phase3-retrieval-contract.yml`;
- `docs/phase-3/evaluation-contract.md`.

### Workstream 2 — deterministic lexical baseline — accepted

Accepted evidence:

- `content/fixtures/phase3_retrieval/lexical-baseline.json`;
- `tools/phase3_retrieval/lexical.py`;
- `tools/phase3_retrieval/tests/test_lexical.py`;
- `.github/workflows/phase3-lexical-baseline.yml`;
- `docs/phase-3/lexical-baseline.md`.

The index is byte-identical across repeated builds and Python 3.11/3.13 evidence runs. Deletion and canonical rebuild are verified. No external services, embeddings, vectors, learned ranking, query expansion, or judgment-specific tuning are used.

### Workstream 3 — structured-field baseline — next

The next candidate must:

- use the exact accepted query-set version unchanged;
- declare field and graph weights before evaluation;
- score canonical titles, types, metadata, relations, and provenance transparently;
- preserve exact revisions, canonical metadata, lifecycle, review level, and provenance;
- emit accepted result and metric contracts;
- compare aggregate and query-level results against the lexical baseline;
- report gains, regressions, and unresolved cases honestly;
- validate deletion and byte-identical rebuild;
- avoid embeddings, vector infrastructure, learned weights, and judgment-specific tuning.

### Workstream 4 — comparative retrieval experiments

Only after Workstreams 1–3 are accepted:

- test embedding, vector, hybrid, or reranking candidates;
- keep external services optional and replaceable;
- compare quality, determinism, latency, storage, failure behavior, and inspectability;
- reject infrastructure commitment when evidence does not justify it.

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
- results preserve exact revisions and visible provenance;
- deterministic metrics and tie behavior are recorded;
- malformed indexes and unavailable revisions fail safely;
- index deletion and canonical rebuild are tested;
- any vector or learned candidate is compared against accepted baselines;
- the completion report recommends or rejects broader retrieval work;
- no retrieval result is granted canonical or lifecycle authority.
