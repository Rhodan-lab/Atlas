# Atlas Project State

## Current status

**Phase 3 — Retrieval Evaluation (active)**

Phase 1 is complete under an explicitly **AI-reviewed** policy. Phase 2 is complete under deterministic kernel, compatibility, failure, scale, replay, replaceability, and rollback evidence.

Phase 3 status:

```yaml
workstream_1_evaluation_contract: accepted
workstream_2_lexical_baseline: accepted
workstream_3_structured_baseline: accepted
workstream_4_comparative_retrieval: first-candidate-evaluated-rejected
workstream_5_research_trails_and_candidate_discovery: active
retrieval_authority: advisory-only
exact_revision_required: true
live: false
repository_mutation: false
```

No human or expert verification is claimed. No live Principia dependency, vector database, production retrieval claim, or autonomous knowledge mutation is active.

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
- deterministic structured-field retrieval baseline — PR #34, commit `a8212512261ed3d718ee14c1fa40e30277f62b75`;
- accepted structured-baseline governance record and Workstream 4 activation — PR #35, commit `0dd8c8d73db279aae04076a6b3ad1e2e59fa4f9c`;
- evaluated and rejected reciprocal-rank-fusion candidate — PR #36, commit `e6010893112b10362a15392d8635a0297b055267`.

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

Accepted capabilities include deterministic compilation, strict runtime admission, exact-revision lookup, relation and provenance traversal, dependency impact, safe failures, non-live Principia compatibility, atomic offline protocol validation, lifecycle escalation reporting, scaled measurements, receipt replay and recovery, portable snapshots, independent query-engine equivalence, and deterministic migration and rollback.

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

Phase 3 helps users find relevant knowledge and inspect why it was retrieved without weakening identity, provenance, review, lifecycle, or replaceability guarantees.

Required outcomes include:

1. a versioned relevance test collection;
2. deterministic lexical and structured ranking baselines;
3. visible exact revisions, provenance, review, lifecycle, and staleness;
4. inspectable ranking explanations and safe failures;
5. filters by entity, status, domain, date, and evidence role;
6. saved exact-revision research trails;
7. advisory contradiction and duplicate candidates;
8. comparative evidence before specialized indexing, embedding, or vector-store commitment;
9. a Phase 3 completion report recommending or rejecting entry into Phase 4.

Phase 3 is an evaluation phase, not a production-search deployment phase.

## Workstream 1 — accepted evaluation contract

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

Every unlisted exact entity in the pinned corpus receives grade 0 for each ranked query. Listed targets receive grades 1–3 with explicit rationales. These judgments are evaluation fixtures, not canonical scientific claims or human relevance consensus.

## Workstream 2 — accepted lexical baseline

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

## Workstream 3 — accepted structured baseline

```yaml
index_contract: atlas-structured-index/0.1
scoring_contract: atlas-structured-bm25f-scoring/0.1
baseline_contract: atlas-phase3-structured-baseline/0.1
state: accepted
accepted_pr: 34
governance_pr: 35
tested_head: d7b7c10338ff68121f7fb7532f3799adfa72c404
accepted_merge_commit: a8212512261ed3d718ee14c1fa40e30277f62b75
governance_merge_commit: 0dd8c8d73db279aae04076a6b3ad1e2e59fa4f9c
entity_count: 34
term_count: 868
cutoff: 5
result_limit: 10
canonical_body_indexed: false
accepted_judgments_unchanged: true
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

The structured index excludes canonical body text and uses stable identity, title, type, substantive metadata, lifecycle and review fields, exact graph neighborhood, and provenance-linked source identity.

It is the preferred accepted ranking baseline for the current bounded fixture. This is not a production-quality claim.

## Workstream 4 — comparative retrieval candidate 1 evaluated and rejected

PR #36 evaluated the predeclared equal-weight reciprocal-rank-fusion candidate.

```yaml
candidate_contract: atlas-phase3-rank-fusion-candidate/0.1
manifest_contract: atlas-rank-fusion-manifest/0.1
scoring_contract: atlas-reciprocal-rank-fusion/0.1
state: evaluated-rejected
accepted_evidence_pr: 36
tested_head: cec57a7a090dbdc8238a19a21f9d84e38a836917
evidence_merge_commit: e6010893112b10362a15392d8635a0297b055267
rrf_k: 60
lexical_weight: 1.0
structured_weight: 1.0
input_limit: 10
output_limit: 10
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
recommendation: reject-candidate-no-quality-gain-over-structured
python_evidence_artifacts_byte_identical: true
additional_index_documents: 0
additional_index_terms: 0
external_services: false
embeddings: false
vector_database: false
learned_weights: false
judgment_specific_tuning: false
retrieval_authority: advisory-only
live: false
repository_mutation: false
```

Fusion improved all four core metrics over lexical retrieval but lost all four to the structured baseline. Under the rule declared before evaluation, the extra layer is rejected as the preferred method.

The negative evidence is retained. It demonstrates that global equal weighting can repair specific failures while diluting stronger structured rankings on more queries. It does not justify post-hoc weight tuning or a vector database commitment.

## Workstream 5 — active research trails and candidate discovery

Purpose: complete the remaining Phase 3 foundation scope before any semantic infrastructure decision.

Required contracts and fixtures:

```yaml
filter_contract:
  dimensions: [entity-type, status, domain, date, evidence-role]
  exact_revision_preserved: true
  hidden_authority: false
research_trail_contract:
  entries: exact-entity-revisions
  query_and_filter_snapshot: required
  ranking_explanation_snapshot: required
  canonical_copy: forbidden
  lifecycle_authority: none
candidate_discovery_contracts:
  contradiction_candidate: advisory-only
  duplicate_candidate: advisory-only
  automatic_merge_or_resolution: forbidden
```

Workstream 5 must:

- define deterministic filter semantics over accepted runtime fields;
- preserve exact entity revisions, provenance, review, lifecycle, and staleness after filtering;
- define saved research trails as versioned references and decisions, not copied canonical knowledge;
- make query, filters, selected results, exclusions, notes, and timestamps inspectable;
- identify contradiction and duplicate candidates without asserting that a contradiction or duplicate is proven;
- require explicit rationale and evidence paths for every candidate;
- prevent automatic merge, deprecation, lifecycle, or canonical mutation;
- include valid, invalid, ambiguity, stale-revision, and unavailable-revision fixtures;
- evaluate deterministic behavior before expanding the relevance benchmark.

Embedding, vector, learned-ranking, and external semantic-service experiments remain deferred until Workstream 5 contracts exist and the test collection is broadened beyond the current 34-entity, 13-query reference fixture.

## Phase 3 boundary

Allowed:

- bounded lexical, structured, filtering, trail, and candidate-discovery evaluation;
- versioned query and relevance fixtures;
- deterministic ranking, filtering, and tie-breaking;
- advisory result sets with exact revisions and provenance;
- replaceable generated indexes and comparison artifacts;
- separately proposed semantic experiments only after broader evidence and explicit architecture approval.

Still frozen:

- production retrieval-quality claims;
- vector database commitment;
- post-hoc tuning against the accepted judgment set;
- unversioned or implicit `latest` lookup;
- retrieval-generated canonical writes;
- retrieval-driven lifecycle, review, promotion, merge, or release mutation;
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

1. define the versioned retrieval-filter contract and deterministic field semantics;
2. define the saved research-trail contract with exact-revision entries and inspectable decisions;
3. define advisory contradiction-candidate and duplicate-candidate contracts;
4. create bounded valid, invalid, ambiguity, stale, and unavailable-revision fixtures;
5. add machine validation and Python 3.11/3.13 evidence;
6. keep the accepted structured method as the preferred bounded ranking baseline;
7. keep embeddings, vector infrastructure, live synchronization, canonical writes, and automatic authority frozen.

**Phase 1 and Phase 2 are complete. Phase 3 Workstreams 1–3 are accepted. Workstream 4 candidate 1 is evaluated and rejected. Workstream 5 — Research Trails and Candidate Discovery — is active. Retrieval remains advisory, exact-revision, provenance-visible, replaceable, and `live: false`.**
