# Atlas Project State

## Current status

**Phase 3 — Retrieval Evaluation (active)**

Phase 1 is complete under an explicitly **AI-reviewed** policy. Phase 2 is complete under deterministic kernel, compatibility, failure, scale, replay, replaceability, and rollback evidence. Phase 3 Workstreams 1, 2, and 3 are accepted. Workstream 4 — bounded comparative retrieval experiments — is active.

No human or expert verification is claimed, no live Principia dependency is active, and retrieval has advisory authority only.

## Accepted history

- Phase 0 foundation — PR #3, commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- review and promotion experiments — PR #4, commit `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency reporting — PR #5, commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- delayed-feedback readiness — PR #6, commit `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only authored corpus — PR #7, commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations — PR #8, commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- optional human handoff — PR #9, commit `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`;
- optional exact-snapshot intake — PR #10, commit `9809bcb523954770e87c78154cdb124f37aadf46`;
- optional admission boundary — PR #17, commit `01feffc696cc207305ef74c92d600f37f1e240a4`;
- Phase 1 AI review and Phase 2 activation — PR #18, commit `f90fa53f99ec9780451c9c50c57625759ba3b2b5`;
- first Phase 2 kernel and bridge receiver — PR #19, commit `8f1e473578d9086a73dae44f0b6001b246cfbc20`;
- Principia v0.2 importer implementation — PR #20, commit `1cc4aec6908a8703a7f505478329c633a23b4ef9`;
- accepted Principia importer governance baseline — PR #21, commit `9370cc746e9756e433ac3772d56d079c9803b144`;
- offline multi-artifact and lifecycle-protocol audit — PR #22, commit `1096a2176eb50e1921081bb3f46eeac8b13bd2c3`;
- accepted offline protocol governance record — PR #23, commit `ec666b59c4834c9a716006be9f9830d20178af34`;
- runtime hardening and failure semantics — PR #24, commit `7596e4fbae099304d64a5b2371c0fb4a2e55ffc4`;
- accepted runtime-hardening governance record — PR #25, commit `e66975a9a2e74f97fcd799ee80b47483a8390f0d`;
- scale, replay, and recovery validation — PR #26, commit `dd0c64447fb70727d260362f9877ffc6be560c3c`;
- accepted scale and replay governance record — PR #27, commit `fae9fc301a6d6d4bb91d8939c7d9a7fd6b48374b`;
- Phase 2 closure and retrieval-entry evidence — PR #28, commit `99b5c4db514da8ac1f6f30740fae66d42e242a74`;
- Phase 2 governance closure and Phase 3 activation — PR #29, commit `9374db0359b19366bd32fe5ea65980bab67068c0`;
- retrieval evaluation contracts and judgments — PR #30, commit `973827e6e7644f79437f3705c73f9e6d83e9a477`;
- accepted retrieval-contract governance record — PR #31, commit `bbf8f3e79518473fc929b0d1f9363484146205db`;
- deterministic lexical retrieval baseline — PR #32, commit `444011821969285da78e6c7fc4ceadec1efca322`;
- accepted lexical-baseline governance record — PR #33, commit `c3fee229dd5c0e6e3d006dd50d4004dff84923e0`;
- deterministic structured-field retrieval baseline — PR #34, commit `a8212512261ed3d718ee14c1fa40e30277f62b75`.

## Language policy

The active authored and review corpus is English-only.

Language-neutral translation identity, revision lineage, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent an active translated corpus.

## Review policy

Atlas distinguishes review levels instead of presenting all review as equivalent.

### AI-reviewed

An AI-reviewed artifact has an identified AI reviewer and model family, explicit non-human status, exact entity revisions, source-use checks, reproducibility or mathematical checks where applicable, recorded findings and corrections, explicit limitations, and `human_verified: false`.

AI review is sufficient for current Atlas development and is not human verification.

### Human-verified

Human verification remains an optional stronger layer. Historical handoff, intake, admission, coverage, and promotion tools remain available, but they are not active Phase 3 gates.

Atlas must never convert an AI review into a human review or invent reviewer identity, credentials, independence, or accountability.

## Phase 1 completion

The delayed-feedback slice is accepted at `ai-reviewed` with:

```yaml
reviewer: GPT-5.6 Thinking
reviewer_kind: ai
human_verified: false
human_review_required: false
overall_outcome: pass
entity_count: 10
```

For `x[t+1] = x[t] - x[t-1]`, `x0 = 1`, and `x1 = 0`, the exact orbit is bounded and periodic with period 6. This is a formal result for one recurrence and initial history. It is not empirical evidence about a real system and not a general theorem that delay causes instability.

## Phase 2 completion

Phase 2 established the smallest dependable, deterministic, read-only kernel over canonical `atlas-content/0.1` Markdown.

Accepted capabilities include deterministic compilation, strict runtime admission, exact-revision lookup, typed relation and provenance traversal, reverse-dependency impact, safe failures, non-live Principia compatibility, atomic offline protocol validation, lifecycle escalation reporting, scaled measurements, receipt replay and recovery, portable snapshots, independent query-engine equivalence, and deterministic migration and rollback.

```yaml
completion_contract: atlas-phase2-completion-report/0.1
portable_contract: atlas-kernel-portable-snapshot/0.1
state: accepted
accepted_pr: 28
tested_head: ad8bc4fa66eb894ca72b13f81be5e3c14bbd241a
accepted_merge_commit: 99b5c4db514da8ac1f6f30740fae66d42e242a74
entity_count: 34
query_equivalence_checks: 136
query_decision: equivalent
migration_decision: replaceable
retrieval_decision: proceed-bounded-retrieval-evaluation
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

Generated runtimes, indexes, caches, and portable snapshots remain disposable. Canonical Markdown and pinned external fixtures remain authoritative.

## Authority order

1. `PROJECT_STATE.md`;
2. accepted foundation documents in `docs/foundation/`;
3. accepted phase completion reports and ADRs;
4. canonical authored content;
5. identified review records and reports, with review level visible;
6. generated manifests and operational artifacts;
7. experimental runtime, retrieval, adapter, and index code.

## Phase 3 objective

Phase 3 evaluates whether Atlas can retrieve relevant, versioned knowledge without weakening identity, provenance, review, lifecycle, or replaceability guarantees.

Phase 3 is an evaluation phase, not a production-search deployment phase.

Required outcomes:

1. a versioned query-and-judgment fixture set;
2. deterministic lexical and structured baselines;
3. explicit relevance metrics and deterministic tie handling;
4. exact entity ID and revision in every result;
5. visible provenance, review level, lifecycle, and staleness in every result;
6. safe failures for unavailable revisions and malformed indexes;
7. deletion and canonical rebuild tests for every generated index;
8. comparative evidence before any embedding or vector-store commitment;
9. a Phase 3 completion report recommending or rejecting broader retrieval work.

## Phase 3 Workstream 1 — accepted evaluation contract

```yaml
query_set_contract: atlas-retrieval-query-set/0.1
result_set_contract: atlas-retrieval-result-set/0.1
metric_report_contract: atlas-retrieval-metric-report/0.1
state: accepted
accepted_pr: 30
governance_pr: 31
tested_head: 3cd4c103da12c140e1a4d0b7bf2bdb8cca5e9727
accepted_merge_commit: 973827e6e7644f79437f3705c73f9e6d83e9a477
governance_merge_commit: bbf8f3e79518473fc929b0d1f9363484146205db
query_set_id: retrieval-query-set:phase3-reference-en-v1
query_set_version: 1
entity_count: 34
query_count: 13
ranked_query_count: 12
expected_error_query_count: 1
positive_judgment_count: 26
implicit_grade_zero_judgment_count: 382
judgment_authority: evaluation-only
retrieval_authority: advisory-only
exact_revision_required: true
live: false
repository_mutation: false
```

For each ranked query, every unlisted exact entity in the pinned corpus receives grade 0. Listed exact targets receive grades 1–3 with explicit rationales. These are evaluation fixtures, not canonical scientific claims or human relevance consensus.

## Phase 3 Workstream 2 — accepted lexical baseline

```yaml
index_contract: atlas-lexical-index/0.1
tokenizer_contract: atlas-english-tokenizer/0.1
scoring_contract: atlas-bm25f-scoring/0.1
baseline_contract: atlas-phase3-lexical-baseline/0.1
state: accepted
accepted_pr: 32
governance_pr: 33
tested_head: 2fb6a5cb31cc98b9daac942a1745a9bd9effe9ff
accepted_merge_commit: 444011821969285da78e6c7fc4ceadec1efca322
governance_merge_commit: c3fee229dd5c0e6e3d006dd50d4004dff84923e0
entity_count: 34
term_count: 424
cutoff: 5
result_limit: 10
source_digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
index_build_digest: 4da6848c020458694db5d26d44be2ddc2580e9c0c41656ce7dcb44a75da82f16
result_set_sha256: 400adae2eb62e275a02bb5838fc93964ea8a541e498617527b543f4932c8196c
precision_at_5: 0.3
recall_at_5: 0.708333333333
mean_reciprocal_rank: 0.652777777778
ndcg_at_5: 0.589071924873
zero_result_rate: 0.0
unavailable_revision_rate: 1.0
tie_count: 0
deterministic_index: true
rebuild_verified: true
replaceable: true
quality_claim: bounded-reference-fixture-only
external_services: false
embeddings: false
vector_database: false
judgment_specific_tuning: false
retrieval_authority: advisory-only
live: false
repository_mutation: false
```

The evidence is intentionally not described as production quality. It exposes weaknesses in methodological scope, formal-model prioritization, cross-platform context, and cross-slice abstraction.

## Phase 3 Workstream 3 — accepted structured baseline

PR #34 established a deterministic structured-field baseline over the unchanged Workstream 1 query set and the accepted Workstream 2 comparison.

```yaml
index_contract: atlas-structured-index/0.1
scoring_contract: atlas-structured-bm25f-scoring/0.1
baseline_contract: atlas-phase3-structured-baseline/0.1
state: accepted
accepted_pr: 34
tested_head: d7b7c10338ff68121f7fb7532f3799adfa72c404
accepted_merge_commit: a8212512261ed3d718ee14c1fa40e30277f62b75
entity_count: 34
term_count: 868
cutoff: 5
result_limit: 10
canonical_body_indexed: false
accepted_judgments_unchanged: true
source_digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
index_build_digest: 91af098baa9bdb6dd6fc55f58f579b6b3be01637562f5797ec1c948a65c748f2
result_set_sha256: 45f215c726e03aa6bfbb1d701291a4a575dd7dc20f435741ec57eb97c939f77c
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
python_evidence_artifacts_byte_identical: true
deterministic_index: true
rebuild_verified: true
replaceable: true
quality_claim: bounded-reference-fixture-only
external_services: false
embeddings: false
vector_database: false
judgment_specific_tuning: false
retrieval_authority: advisory-only
live: false
repository_mutation: false
```

The index excludes canonical body text and uses stable identity, title, type, substantive authored metadata, lifecycle and review fields, exact graph neighborhood, and provenance-linked source identity.

The aggregate gains are accepted as bounded fixture evidence, not production estimates. Residual limitations remain visible:

- specific fluorescent-assay evidence can outrank the methodological catalase scope claim;
- the foam-proxy query can rank a question and broad concept above the observation model;
- randomized Twitter evidence can outrank the causal claim;
- the cross-slice scope query still misses the recommender context-dependent claim within the top-five cutoff.

## Phase 3 Workstream 4 — active comparative experiments

The first comparison is predeclared before evaluation:

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

This candidate must compare against both accepted baselines, preserve exact revisions and provenance, report query-level gains and regressions, prove deterministic rebuildability, and reject itself if it does not improve the evidence enough to justify added complexity.

Embedding or vector experiments may begin only after this no-infrastructure hybrid comparison is recorded. No vector database is selected by Workstream 4 entry.

## Phase 3 boundary

Allowed:

- bounded lexical, structured, and comparative retrieval experiments;
- versioned query and relevance fixtures;
- deterministic ranking and tie-breaking;
- advisory result sets with exact revisions and provenance;
- replaceable generated indexes and comparison artifacts;
- embedding or vector experiments only as separate, evidence-backed candidates after accepted baselines.

Still frozen:

- production retrieval-quality claims;
- vector database commitment before comparative evidence;
- unversioned or implicit `latest` lookup;
- retrieval-generated canonical writes;
- retrieval-driven lifecycle, review, promotion, or release mutation;
- live Principia synchronization;
- accepting external synthetic events as canonical lifecycle history;
- polished product UI;
- plugins and autonomous synchronization;
- active translated corpus;
- hidden or autonomous authority claims;
- automatic conversion of AI review into human verification.

## Principia & Atlas boundary

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns causal explanation, pathways, investigations, simulations, system dossiers, failure analysis, design experiences, and its own publication readiness.
- Principia may reference exact Atlas revisions.
- Neither repository inherits the other repository's status automatically.
- No live cross-repository dependency is activated by Phase 3 evaluation.

## Immediate next actions

1. implement equal-weight reciprocal-rank fusion over the accepted lexical and structured rankings;
2. keep the accepted query set, judgments, and baseline artifacts unchanged;
3. emit exact-revision, provenance-visible, contract-valid hybrid results and metrics;
4. compare aggregate and query-level results against both accepted baselines;
5. record added complexity, failure behavior, determinism, storage, and inspectability;
6. reject or accept the hybrid candidate using evidence rather than popularity;
7. keep embeddings, vector infrastructure, live synchronization, canonical writes, and automatic authority frozen until a separate decision.

**Phase 1 and Phase 2 are complete. Phase 3 Workstreams 1–3 are accepted. Workstream 4 — bounded comparative retrieval experiments — is active. Retrieval remains advisory, exact-revision, provenance-visible, replaceable, and `live: false`.**
