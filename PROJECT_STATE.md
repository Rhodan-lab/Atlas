# Atlas Project State

## Current status

**Phase 3 — Retrieval Evaluation (active)**

Phase 1 is complete under an explicitly **AI-reviewed** policy. Phase 2 is complete under deterministic kernel, compatibility, failure, scale, replay, replaceability, and rollback evidence. Phase 3 Workstreams 1 and 2 are accepted. No human or expert verification is claimed, no live Principia dependency is active, and retrieval has advisory authority only.

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
- Phase 2 closure, replaceability, and retrieval-entry evidence — PR #28, commit `99b5c4db514da8ac1f6f30740fae66d42e242a74`;
- Phase 2 closure governance and Phase 3 activation — PR #29, commit `9374db0359b19366bd32fe5ea65980bab67068c0`;
- Phase 3 retrieval evaluation contracts and judgments — PR #30, commit `973827e6e7644f79437f3705c73f9e6d83e9a477`;
- accepted retrieval-contract governance record — PR #31, commit `bbf8f3e79518473fc929b0d1f9363484146205db`;
- deterministic lexical retrieval baseline — PR #32, commit `444011821969285da78e6c7fc4ceadec1efca322`.

## Language policy

The active authored and review corpus is English-only.

Language-neutral translation identity, revision lineage, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent an active translated corpus.

## Review policy

Atlas distinguishes review levels instead of presenting all review as equivalent.

### AI-reviewed

An AI-reviewed artifact has:

- an identified AI reviewer and model family;
- explicit non-human status;
- exact entity revisions;
- source-use checks;
- reproducibility or mathematical checks where applicable;
- recorded findings and corrections;
- explicit limitations;
- `human_verified: false`.

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

Active evidence:

- `content/reviews/ai/feedback-delayed-comprehensive.json`;
- `docs/phase-1/ai-review-report.md`;
- `tools/foundation-validator/phase1_ai_review.py`.

## Phase 2 completion

Phase 2 established the smallest dependable, deterministic, read-only kernel over canonical `atlas-content/0.1` Markdown.

Accepted capabilities include deterministic compilation, strict runtime admission, exact-revision lookup, typed relation and provenance traversal, reverse-dependency impact, safe failures, non-live Principia compatibility, atomic offline protocol validation, lifecycle escalation reporting, scaled measurements, receipt replay and recovery, portable snapshots, independent query-engine equivalence, and deterministic migration and rollback.

### Accepted closure evidence

```yaml
completion_contract: atlas-phase2-completion-report/0.1
portable_contract: atlas-kernel-portable-snapshot/0.1
mode: phase2-closure-candidate
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
2. deterministic lexical retrieval baseline;
3. deterministic structured-field retrieval baseline;
4. explicit relevance metrics and deterministic tie handling;
5. exact entity ID and revision in every result;
6. visible provenance, review level, lifecycle, and staleness in every result;
7. safe failures for unavailable revisions and malformed indexes;
8. deletion and canonical rebuild tests for every generated index;
9. comparative evidence before any embedding or vector-store commitment;
10. a Phase 3 completion report recommending or rejecting broader retrieval work.

## Phase 3 workstream 1 — accepted

PR #30 established the retrieval evaluation boundary before ranking implementation. PR #31 finalized the accepted governance record.

```yaml
query_set_contract: atlas-retrieval-query-set/0.1
result_set_contract: atlas-retrieval-result-set/0.1
metric_report_contract: atlas-retrieval-metric-report/0.1
mode: retrieval-evaluation
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

For each ranked query, every unlisted exact entity in the pinned corpus receives grade 0. Listed exact targets receive grades 1–3 with explicit rationales. The judgments are evaluation fixtures, not canonical scientific claims or human relevance consensus.

## Phase 3 workstream 2 — accepted

PR #32 established the first transparent ranking baseline against the unchanged Workstream 1 fixture.

```yaml
index_contract: atlas-lexical-index/0.1
tokenizer_contract: atlas-english-tokenizer/0.1
scoring_contract: atlas-bm25f-scoring/0.1
baseline_contract: atlas-phase3-lexical-baseline/0.1
mode: retrieval-evaluation
state: accepted
accepted_pr: 32
tested_head: 2fb6a5cb31cc98b9daac942a1745a9bd9effe9ff
accepted_merge_commit: 444011821969285da78e6c7fc4ceadec1efca322
query_set_id: retrieval-query-set:phase3-reference-en-v1
query_set_version: 1
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

The tokenizer uses NFKC case folding, `[a-z0-9]+`, a fixed stopword list, no stemming, and no query expansion. BM25F scores canonical body, stable ID, title, and type with public fixed weights and exact-key ascending ties.

The evidence is intentionally not described as strong production quality. It shows moderate graded ranking performance and exposes concrete weaknesses:

- specific assay evidence can outrank methodological scope;
- the exact formal model can rank below related prose records;
- cross-platform context can lose to named study records;
- cross-slice methodological abstraction is incomplete.

These are comparison targets for Workstream 3 rather than reasons to rewrite the accepted judgments or tune the lexical baseline after seeing results.

## Phase 3 entry boundary

Allowed:

- bounded lexical and structured retrieval experiments;
- versioned query and relevance fixtures;
- deterministic ranking and tie-breaking;
- advisory result sets with exact revisions and provenance;
- replaceable generated indexes;
- comparative embedding or vector experiments only after lexical and structured baselines are accepted.

Still frozen:

- production retrieval-quality claims;
- vector database commitment before comparative evaluation;
- unversioned or implicit `latest` lookup;
- retrieval-generated writes to canonical content;
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

1. implement a deterministic structured-field baseline against the unchanged query-set version;
2. declare field and graph weights before evaluation and avoid judgment-specific tuning;
3. score canonical metadata, titles, types, exact relations, and provenance-linked source identity transparently;
4. emit contract-valid results and metrics with exact revisions and visible provenance;
5. compare every metric and query-level gain or regression against the accepted lexical evidence;
6. prove index deletion and byte-identical canonical rebuild;
7. keep embeddings, vector infrastructure, live synchronization, canonical writes, and automatic authority frozen until a separate comparative decision.

**Phase 1 and Phase 2 are complete. Phase 3 Workstreams 1 and 2 are accepted. Workstream 3 — deterministic structured-field retrieval — is next. Retrieval remains bounded, advisory, exact-revision, provenance-visible, replaceable, and `live: false`.**
