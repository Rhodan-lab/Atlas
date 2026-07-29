# Atlas Project State

## Current authority

**Phase 4 — Principia & Atlas Interactive Experience (active)**

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 4
workstream_name: bounded-workspace-fixture-generalization
active_slice: 2
slice_name: catalase-static-reader-reuse-evaluation
workstream_1: accepted
workstream_2: accepted
workstream_3: accepted
workstream_4_slice_1: accepted
fixture_count_authorized: 1
previous_fixture_domain: recommender-systems
active_fixture_domain: catalase-assay-methodology
cross_domain_required: true
existing_canonical_revisions_only: true
new_canonical_authoring_authorized: false
accepted_contract_reuse_required: true
existing_static_reader_reuse_authorized: true
browser_implementation_scope: existing-static-reader-reuse-only
browser_evidence_authorized: true
new_frontend_architecture_authorized: false
production_implementation_authorized: false
workspace_authority: ephemeral-research-only
browser_state_authority: ephemeral-only
atlas_semantics_authoritative: true
principia_status_separate: true
exact_cross_repository_references: true
retrieval_authority: advisory-only
local_first: true
deterministic_export_required: true
canonical_copy_authority: false
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
automatic_merge_or_resolution: false
account_required: false
cloud_required: false
external_network_required: false
production_frontend_architecture_selected: false
live_principia_dependency: false
repository_mutation: false
```

No human or expert verification is claimed. Automated Chromium evidence is not accessibility certification. No production retrieval-quality claim, new frontend architecture, deployment architecture, vector database, live Principia synchronization, autonomous knowledge mutation, account system, cloud persistence, or automatic lifecycle authority is active.

## Authority order

1. `PROJECT_STATE.md`;
2. accepted foundation documents in `docs/foundation/`;
3. accepted phase, workstream, completion, and governance records;
4. canonical authored content;
5. identified review records, with review level visible;
6. generated manifests and operational evidence;
7. experimental runtime, retrieval, bridge, workspace, browser, and interface code.

## Language and review policy

The active authored and review corpus is English-only. AI review is sufficient for this bounded development program but is not human verification. Human verification remains an optional stronger layer and must never be inferred. Browser automation remains distinct from human usability review, assistive-technology user review, and accessibility certification.

## Accepted development history

The repository preserves granular history through the merged pull requests and phase records. The accepted sequence is:

```yaml
phase_0_and_phase_1:
  accepted_prs: [3, 4, 5, 6, 7, 8, 9, 10, 17, 18]
phase_2:
  accepted_prs: [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
phase_3:
  accepted_prs: [30, 31, 32, 33, 34, 35, 36, 37, 38, 40, 41]
phase_4_workstream_1:
  accepted_prs: [42, 43, 44, 45]
phase_4_workstream_2:
  accepted_prs: [46, 47, 48]
phase_4_workstream_3:
  accepted_prs: [50, 51, 52, 54, 55, 56]
phase_4_workstream_4:
  accepted_prs: [58]
superseded_unmerged_prs: [39, 49, 53]
```

PR #39 was a superseded Phase 3 closure draft. PR #49 duplicated PR #48. PR #53 was superseded by the stronger pinned browser-evidence PR #54.

## Completed phases

### Phase 1 — bounded English corpus

```yaml
state: accepted
reviewer: GPT-5.6 Thinking
reviewer_kind: ai
human_verified: false
overall_outcome: pass
entity_count: 10
```

### Phase 2 — deterministic read-only knowledge kernel

```yaml
state: accepted
accepted_pr: 28
accepted_merge_commit: 99b5c4db514da8ac1f6f30740fae66d42e242a74
completion_contract: atlas-phase2-completion-report/0.1
entity_count: 34
query_equivalence_checks: 136
migration_decision: replaceable
retrieval_decision: proceed-bounded-retrieval-evaluation
live: false
repository_mutation: false
```

### Phase 3 — bounded retrieval and research foundations

```yaml
state: accepted
accepted_pr: 40
accepted_merge_commit: 52f51558a9188f049f4b4b838bc6acfd1a991e96
completion_contract: atlas-phase3-completion-report/0.1
preferred_bounded_retrieval: structured-field-baseline
semantic_infrastructure_decision: deferred
retrieval_authority: advisory-only
replaceable: true
live: false
repository_mutation: false
```

The accepted structured baseline is bounded fixture evidence, not a production retrieval-quality claim.

## Phase 4 accepted workstreams

### Workstream 1 — interaction contracts and reference shell

```yaml
state: accepted
completion_pr: 44
completion_merge_commit: 37b013ce1b3c8c45230feaf4c1cd6bfd0ba48735
completion_contract: atlas-phase4-workstream1-completion-report/0.1
exit_gate_count: 10
```

### Workstream 2 — pinned browser accessibility and workflow evidence

```yaml
state: accepted
browser_pr: 46
closure_pr: 47
completion_contract: atlas-phase4-workstream2-completion-report/0.1
engine: chromium-151.0.7922.34
playwright: 1.62.0
external_request_count: 0
exit_gate_count: 12
human_verified: false
accessibility_certified: false
```

### Workstream 3 — read-only research workspace composition

```yaml
state: accepted
workspace_contract_pr: 50
workspace_shell_pr: 52
workspace_browser_pr: 54
closure_pr: 56
closure_tested_head: f24777d4f52ca4dd8e9829fc929f3fb2c88d0115
closure_merge_commit: b9e30959e3b9387c5132c804cccf9c1391a9ada6
completion_contract: atlas-phase4-workstream3-completion-report/0.1
completion_validation_contract: atlas-phase4-workstream3-completion-validation/0.1
completion_baseline_contract: atlas-phase4-workstream3-completion-baseline/0.1
completion_report_bytes: 9098
completion_report_sha256: fe4798f27ed31f6a180c9cb7ec5df31ddc77b440585f0d26dd3cd82d26e23353
completion_report_digest: 3f13809d1aba31a15af77ea7afae1062bac5b4a4274ec3794d9f6be389e3ecde
completion_validation_bytes: 380
completion_validation_sha256: 8bd6947a0be923ea6a6f6167a11fe059fc117c55538241a84ce41442f3e7d974
exit_gate_count: 13
python_3_11_and_3_13_byte_identical: true
recommendation: proceed-bounded-workspace-fixture-evaluation
implementation_authorized_by_report: false
separate_governance_required: true
```

Workstream 3 proved deterministic exact-revision composition, read-only decisions, unresolved advisory candidates, separate Principia status, visible warnings and failures, complete keyboard and non-graph operation, byte-identical local export, disposable browser state, replaceability, explicit migration and rollback boundaries, and zero external requests.

The completion report could not authorize its own recommendation. This state record separately authorized Workstream 4.

### Workstream 4 Slice 1 — Catalase fixture contract generalization

```yaml
state: accepted
accepted_pr: 58
accepted_candidate_head: 4b25e0ac7e5b31f05629b19cef6388ca823ad9fa
accepted_merge_commit: a7e04f377389cb003aec8faadcd3eccdfd78ba2b
evidence_baseline_contract: atlas-phase4-workspace-generalization-baseline/0.1
fixture_id: generalization-fixture:phase4-catalase-en-v1
fixture_domain: catalase-assay-methodology
canonical_source_pool_count: 8
workspace_entry_count: 5
unresolved_candidate_count: 2
principia_reference_count: 1
unavailable_revision_warning_count: 1
acceptance_gate_count: 13
core_negative_case_count: 10
generalization_negative_case_count: 14
total_negative_case_count: 24
python_3_11_and_3_13_byte_identical: true
recommendation: proceed-static-reader-reuse-evaluation
implementation_authorized_by_report: false
separate_governance_required: true
```

Pinned Slice 1 artifact identities:

```yaml
catalase_fixture_sha256: 0a3c76134b72351b9e3c331d7058563f24cd9eef498af1053e60c4b96ef031cd
generalization_report_sha256: 9028a6a4aa7d3841201d9273b42466ad217b283df93e84192933792ed1d6f2f6
generalization_report_digest: 75e5b93d288bd459e7ccc4e134b042f50dc1ef4a4eab24889fdb29b0b7a67121
workspace_contract_report_sha256: 5a8c307e858b348bc695e7dcffe0c5a3577e4ccf83d282631a25f1b623facb91
workspace_contract_report_digest: 3390157fd3935cb3f17ea2519a006589e299bbb922d87e28315e13172dc8fc32
workspace_export_sha256: b05617cac685873cd472b157efde835365b36d846db5eecf941db3495cc79893
workspace_export_digest: d8280f4aa5cfbb5ba91569190ce7836676a5eabc22c113eccd4474ade6a25154
workspace_manifest_sha256: 170a943ceecd306eb02251c92a143137d8f3dc6b047d52d5f5efcc9facf13a5f
workspace_manifest_digest: 0e1d2ee3674457844740b17100be298924293f1a9f7b0fab93ecae478197ca21
```

Slice 1 demonstrated that the accepted Workstream 3 workspace contracts can represent one materially different domain without contract modification, hidden fallback, candidate resolution, or authority expansion. The result is bounded to the single Catalase fixture and is not a universal generality claim.

## Phase 4 Workstream 4 — active Slice 2 static reader reuse evaluation

### Objective

Evaluate whether the existing accepted static workspace reader can render the accepted Catalase fixture without changing Atlas semantics, the accepted workspace contracts, or the reader’s authority model.

### Active Slice 2

```yaml
state: active
fixture_count_authorized: 1
fixture_id: generalization-fixture:phase4-catalase-en-v1
fixture_domain: catalase-assay-methodology
accepted_slice_1_baseline_required: true
existing_static_reader_reuse_authorized: true
new_static_reader_authorized: false
new_frontend_architecture_authorized: false
browser_evidence_authorized: true
production_implementation_authorized: false
existing_canonical_revisions_only: true
new_canonical_authoring_authorized: false
```

Slice 2 may add only the minimum deterministic fixture-selection and packaging logic required to reuse the existing reader. It must preserve the accepted recommender-system reader behavior, exact routes, visible metadata, warnings, failures, keyboard operation, non-graph operation, local-download identity, disposable state, and zero-network boundary.

### Slice 2 required evidence

1. generate the accepted Catalase fixture and export from the pinned Slice 1 baseline;
2. package the fixture through the existing static-reader contract without changing accepted workspace semantics;
3. preserve the existing recommender-system package and prove no regression;
4. render the five Catalase entries, two unresolved candidates, pinned Principia status, unavailable-revision warning, open questions, and non-graph summary;
5. test deterministic routes, deep links, history, keyboard, focus, responsive behavior, explicit failures, and exact local-download bytes;
6. run pinned Chromium evidence twice with zero external requests;
7. reject hidden fallback, implicit latest, account, cloud, credential, network, mutation, and authority escalation;
8. issue a bounded Slice 2 recommendation without authorizing production.

### Slice 2 allowed decisions

```yaml
allowed_decisions:
  - proceed-workstream4-closure-evaluation
  - hold-static-reader-reuse
  - reject-static-reader-reuse
```

A proceed decision may recommend a separate Workstream 4 closure evaluation. It cannot close the workstream or authorize production by itself.

## Global frozen boundaries

Still frozen:

- new canonical authoring for the Workstream 4 fixture;
- a second additional fixture;
- replacement or mutation of the accepted recommender workspace;
- a new reader or frontend architecture;
- production retrieval, frontend, hosting, deployment, or business-model claims;
- vector databases, embeddings, or learned ranking;
- implicit `latest` references;
- live Principia synchronization or inherited cross-repository status;
- canonical, review, lifecycle, promotion, merge, release, or repository authority from workspace or browser state;
- automatic contradiction or duplicate resolution;
- accounts, permissions, cloud state, collaboration, plugins, or autonomous knowledge mutation;
- conversion of AI review into human verification;
- accessibility certification without qualified human evidence.

**Phase 0, Phase 1, Phase 2, and Phase 3 are complete. Phase 4 Workstreams 1, 2, and 3 are accepted. Workstream 4 Slice 1 is accepted. Workstream 4 Slice 2 — Catalase Static Reader Reuse Evaluation — is active.**
