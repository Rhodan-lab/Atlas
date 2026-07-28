# Atlas Project State

## Current status

**Phase 4 — Principia & Atlas Interactive Experience (active)**

Phase 0 established the knowledge foundation. Phase 1 accepted the bounded English reference corpus under an explicitly AI-reviewed, non-human policy. Phase 2 accepted the deterministic read-only knowledge kernel. Phase 3 accepted bounded retrieval and research-trail foundations.

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 1
workstream_name: interaction-contract-and-reference-shell
atlas_semantics_authoritative: true
principia_status_separate: true
exact_cross_repository_references: true
preferred_bounded_retrieval: structured-field-baseline
retrieval_authority: advisory-only
local_first: true
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

No human or expert verification is claimed. No production retrieval-quality claim, vector database, live Principia synchronization, autonomous knowledge mutation, or automatic lifecycle authority is active.

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
- accepted structured-baseline governance record — PR #35, commit `0dd8c8d73db279aae04076a6b3ad1e2e59fa4f9c`;
- evaluated and rejected reciprocal-rank-fusion candidate — PR #36, commit `e6010893112b10362a15392d8635a0297b055267`;
- rejected-candidate governance and Workstream 5 activation — PR #37, commit `9614541ba35570a888f50005d2602cccc24bd4d4`;
- research trails and candidate-discovery contracts — PR #38, commit `12cb0e218dbbc1101253e8f070d4cf77111a7500`;
- Phase 3 closure and Phase 4 recommendation — PR #40, commit `52f51558a9188f049f4b4b838bc6acfd1a991e96`.

PR #39 was a superseded, unmerged closure draft and is not accepted history.

## Language policy

The active authored and review corpus is English-only.

Language-neutral translation identity, revision lineage, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent an active translated corpus.

## Review policy

Atlas distinguishes review levels instead of presenting all review as equivalent.

### AI-reviewed

An AI-reviewed artifact has an identified AI reviewer and model family, explicit non-human status, exact entity revisions, source-use checks, reproducibility or mathematical checks where applicable, recorded findings and corrections, explicit limitations, and `human_verified: false`.

AI review is sufficient for the current bounded development program. It is not human verification.

### Human-verified

Human verification remains an optional stronger layer. Atlas must never convert AI review into human review or invent reviewer identity, credentials, independence, or accountability.

## Authority order

1. `PROJECT_STATE.md`;
2. accepted foundation documents in `docs/foundation/`;
3. accepted phase completion reports and ADRs;
4. canonical authored content;
5. identified review records and reports, with review level visible;
6. generated manifests and operational artifacts;
7. experimental runtime, retrieval, bridge, and interface code.

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

## Phase 3 completion

Phase 3 established bounded, explainable retrieval and research workflows without granting retrieval any canonical or lifecycle authority.

```yaml
completion_contract: atlas-phase3-completion-report/0.1
completion_baseline_contract: atlas-phase3-completion-baseline/0.1
state: accepted
accepted_pr: 40
tested_head: 4f69697065f66ecb8f797616523673d39c8976e1
accepted_merge_commit: 52f51558a9188f049f4b4b838bc6acfd1a991e96
accepted_workstreams: [1, 2, 3, 5]
evaluated_rejected_workstream_4_candidate: equal-weight-reciprocal-rank-fusion
source_digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
entity_count: 34
query_count: 13
positive_judgment_count: 26
preferred_bounded_retrieval: structured-field-baseline
semantic_infrastructure_decision: defer-until-broader-benchmark-and-architecture-approval
retrieval_authority: advisory-only
exact_revision_required: true
replaceable: true
external_services: false
embeddings: false
vector_database: false
live: false
repository_mutation: false
```

### Accepted retrieval evidence

```yaml
lexical:
  precision_at_5: 0.3
  recall_at_5: 0.708333333333
  mean_reciprocal_rank: 0.652777777778
  ndcg_at_5: 0.589071924873
structured:
  precision_at_5: 0.366666666667
  recall_at_5: 0.854166666667
  mean_reciprocal_rank: 0.770833333333
  ndcg_at_5: 0.754777384811
rank_fusion:
  decision: rejected
  recommendation: reject-candidate-no-quality-gain-over-structured
```

The structured index excludes canonical body text and uses stable identity, title, type, substantive metadata, lifecycle and review fields, graph neighborhood, and provenance-linked source identity. It is the preferred bounded baseline for the accepted fixture, not a production-quality claim.

### Accepted research foundations

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
research_report_digest: 733aeb28a3147a36d1cc7d3406ab98fa81522cb4b4e87e3aa792aaf54893a394
canonical_copy_authority: false
automatic_merge_or_resolution: false
```

The contradiction candidate is assessed `scope-difference-likely`; the duplicate candidate is assessed `related-not-duplicate`. Candidate discovery remains a request for inspection, not a forced assertion.

### Phase 3 exit gates

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

## Phase 4 objective

Phase 4 builds a unified interactive experience over proven Atlas and Principia semantics without erasing repository ownership, lifecycle status, or authority boundaries.

Phase 4 is not permission to redesign the ontology, claim production search quality, or activate live synchronization.

## Phase 4 Workstream 1 — active interaction contract and reference shell

Workstream 1 must define the smallest interface contract and local reference shell capable of exercising the accepted semantics.

Required outcomes:

1. a versioned interaction-state contract;
2. exact Atlas entity-revision references in every knowledge view;
3. a non-live Principia reference envelope with separate Principia status;
4. visible provenance, review level, lifecycle, staleness, and retrieval explanation;
5. explicit impact warnings for stale or unavailable cross-repository references;
6. keyboard-accessible, non-graph-dependent navigation;
7. deterministic loading, empty, malformed, unavailable-revision, and offline failure states;
8. local-first packaging with no required cloud service;
9. tests proving that interface state cannot mutate canonical knowledge;
10. a Workstream 1 report recommending or rejecting implementation expansion.

Reference workflows:

- inspect an Atlas question, source, evidence, claim, model, or synthesis at an exact revision;
- trace claim-to-source provenance;
- run the accepted structured retrieval and inspect why a result ranked;
- apply accepted deterministic filters;
- open and revise a research trail as references and decisions only;
- inspect contradiction or duplicate candidates without treating them as resolved;
- follow a bounded Principia reference envelope while preserving separate status and unavailable-reference warnings.

## Phase 4 boundary

Allowed:

- local-first interaction contracts and reference shells;
- Atlas evidence, claim, model, provenance, review, revision, retrieval, filter, trail, and candidate views;
- offline Principia bridge fixtures with exact Atlas references;
- concept, prerequisite, timeline, scale, and system views where canonical semantics support them;
- optional graph visualization with equivalent non-graph navigation;
- accessibility, typography, and deterministic failure-state testing.

Still frozen:

- production retrieval-quality claims;
- vector database commitment;
- implicit `latest` cross-repository references;
- live Principia synchronization;
- canonical writes from interface or retrieval state;
- automatic review, lifecycle, promotion, merge, or release mutation;
- accepting synthetic bridge events as canonical lifecycle history;
- autonomous agents changing knowledge state;
- plugins or permissionless extensions;
- active multilingual authoring;
- automatic conversion of AI review into human verification.

## Principia & Atlas boundary

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns causal explanation, pathways, investigations, simulations, system dossiers, failure analysis, design experiences, and its own publication readiness.
- Principia may reference exact Atlas revisions.
- Neither repository inherits the other repository's status automatically.
- Phase 4 may demonstrate the bridge through pinned offline fixtures, but no live cross-repository dependency is active.

## Immediate next actions

1. define `atlas-interaction-state/0.1` and the exact view-state invariants;
2. define the non-live Principia reference envelope and impact-warning contract;
3. create reference workflows and negative interface fixtures;
4. implement a minimal local shell only after the contracts are executable;
5. test keyboard navigation, non-graph alternatives, offline behavior, and authority isolation;
6. keep semantic infrastructure, live synchronization, canonical writes, and automatic authority frozen.

**Phase 0, Phase 1, Phase 2, and Phase 3 are complete. Phase 4 — Principia & Atlas Interactive Experience — is active at Workstream 1.**
