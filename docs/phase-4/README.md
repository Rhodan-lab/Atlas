# Phase 4 — Principia & Atlas Interactive Experience

## Status

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 3
workstream_name: read-only-research-workspace-composition
active_slice: 3
slice_name: workstream-3-closure-and-recommendation
workstream_1: accepted
workstream_2: accepted
workstream_3_slice_1: accepted
workstream_3_slice_2: accepted
workspace_authority: ephemeral-research-only
browser_state_authority: ephemeral-only
atlas_semantics_authoritative: true
principia_status_separate: true
exact_cross_repository_references: true
preferred_bounded_retrieval: structured-field-baseline
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

Phase 4 builds a unified experience over proven Atlas and Principia semantics without erasing repository ownership, lifecycle status, provenance, revision identity, or authority boundaries. It may expose and compose accepted semantics but may not redefine them.

## Entry evidence

Phase 4 entry was authorized by the accepted Phase 3 completion evidence:

```yaml
completion_contract: atlas-phase3-completion-report/0.1
completion_baseline_contract: atlas-phase3-completion-baseline/0.1
accepted_pr: 40
accepted_merge_commit: 52f51558a9188f049f4b4b838bc6acfd1a991e96
decision: proceed-phase4-interactive-experience
preferred_bounded_retrieval: structured-field-baseline
```

## Workstream 1 — accepted interaction contract and reference shell

Workstream 1 defined the smallest versioned interaction model and local reference shell capable of exercising accepted knowledge, retrieval, trail, candidate, and bridge semantics.

### Accepted contracts

```yaml
interaction_state_contract: atlas-interaction-state/0.1
view_result_contract: atlas-interaction-view/0.1
principia_reference_contract: atlas-principia-reference-envelope/0.1
impact_warning_contract: atlas-cross-repository-impact-warning/0.1
failure_state_contract: atlas-interaction-failure/0.1
shell_data_contract: atlas-reference-shell-data/0.1
shell_build_report_contract: atlas-reference-shell-build-report/0.1
completion_contract: atlas-phase4-workstream1-completion-report/0.1
completion_baseline_contract: atlas-phase4-workstream1-completion-baseline/0.1
```

### Accepted evidence

```yaml
interaction_contracts:
  accepted_pr: 42
  accepted_merge_commit: 1f15cee1f0ed86c5a85750659b4d35e1d535564f
reference_shell:
  accepted_pr: 43
  accepted_merge_commit: 4992d0caa0eb37db5b58158a9dd53a8ca10f1405
closure:
  accepted_pr: 44
  tested_head: 265c44d3b39091bf6dcf1263b9cb3092d3ea4568
  accepted_merge_commit: 37b013ce1b3c8c45230feaf4c1cd6bfd0ba48735
  report_artifact_sha256: 03ba1f02d7ca2cfb7432919c7bdca110edbd497fc8c2be2c2216b099abe0cb23
  report_digest: a3167ee2dc7a02c47468a1b850e15b495f3ed6058399205fc2cdf906d922aaa3
  exit_gate_count: 10
  decision: proceed-workstream2-browser-accessibility-evidence
```

Accepted capabilities include exact-revision views, deterministic routes, visible authority and provenance, separate Principia status, explicit warnings and failures, keyboard and non-graph requirements, replaceable local artifacts, and negative tests preventing hidden fallback or authority escalation.

See [`interaction-contract.md`](interaction-contract.md), [`reference-shell.md`](reference-shell.md), and [`workstream-1-completion.md`](workstream-1-completion.md).

## Workstream 2 — accepted browser accessibility and workflow evidence

Workstream 2 used one pinned Chromium engine as a controlled test instrument over the accepted local shell. It established deterministic machine-readable evidence without selecting a production browser, frontend framework, hosting platform, or product architecture.

### Accepted contracts

```yaml
browser_workflow_contract: atlas-browser-workflow-evidence/0.1
browser_accessibility_contract: atlas-browser-accessibility-report/0.1
browser_network_contract: atlas-browser-network-report/0.1
browser_failure_contract: atlas-browser-failure-evidence/0.1
browser_evidence_manifest: atlas-phase4-browser-evidence-manifest/0.1
browser_evidence_report: atlas-phase4-browser-evidence-report/0.1
browser_evidence_baseline: atlas-phase4-browser-evidence-baseline/0.1
completion_contract: atlas-phase4-workstream2-completion-report/0.1
completion_baseline_contract: atlas-phase4-workstream2-completion-baseline/0.1
```

### Accepted browser evidence and closure

```yaml
browser_evidence:
  accepted_pr: 46
  tested_head: 05e829dcf0c331188f4e75a7ffe8e9b1434b2aab
  accepted_merge_commit: d5577d9664a16b89d4c2597229f418a7f4a8f849
  engine: chromium
  engine_version: 151.0.7922.34
  playwright_version: 1.62.0
  workflow_count: 8
  keyboard_workflow_count: 9
  viewport_count: 2
  external_request_count: 0
  human_verified: false
  accessibility_certified: false
closure:
  accepted_pr: 47
  tested_head: f15e085317ed898cfca545f1492f53b4882e4045
  accepted_merge_commit: dca6dd1bf8b8445bb4101ad7a3503dd79a57ea74
  report_artifact_sha256: 4cccee425316ed329979cb9f5eb900a7a7ee3656c72822ecffa8f4f15ef76786
  report_digest: 926eb576fb216fca2d1f5a52d11f977f7c743c058d9a8a31d81ffc265f2d9913
  exit_gate_count: 12
  decision: proceed-workstream3-read-only-research-workspace
```

Automated browser evidence is necessary but is not human accessibility certification, assistive-technology user review, or broad usability validation.

See [`browser-evidence.md`](browser-evidence.md) and [`workstream-2-completion.md`](workstream-2-completion.md).

## Workstream 3 — active closure of the read-only research workspace

### Objective

Compose accepted exact-revision Atlas views and pinned offline Principia references into a deterministic read-only multi-step research workspace. The workspace may organize evidence, questions, decisions, candidates, comparisons, and exports, but has no canonical, review, lifecycle, merge, release, or repository authority.

### Slice 1 — accepted workspace data and export contracts

```yaml
state: accepted
accepted_pr: 50
tested_head: 6d556bde6c24a8313bece3074f6c5fc56c4c4ccd
accepted_merge_commit: 86c1f9f779172aa47d450022fc40357a93f2302f
fixture_contract: atlas-phase4-workspace-fixtures/0.1
workspace_contract: atlas-research-workspace/0.1
workspace_entry_contract: atlas-research-workspace-entry/0.1
workspace_decision_contract: atlas-research-workspace-decision/0.1
workspace_export_contract: atlas-research-workspace-export/0.1
workspace_manifest_contract: atlas-research-workspace-manifest/0.1
workspace_failure_contract: atlas-research-workspace-failure/0.1
workspace_report_contract: atlas-phase4-workspace-contract-report/0.1
workspace_baseline_contract: atlas-phase4-workspace-contract-baseline/0.1
```

```yaml
fixture:
  artifact_bytes: 8961
  artifact_sha256: 3493c963163a2ba52d6de92fdf8193f9c7f9d7eb967211d7e13ef7b596b24f86
report:
  artifact_bytes: 4186
  artifact_sha256: 41d555a077e63b47da5159e48a5aa37d93bc6cbd149b86baf372ff932b7e5a94
  report_digest: 6aec854b297b51b0dde2e65a944453d7af2a8e36b77bd78302cbb0e2f405b402
export:
  artifact_bytes: 11347
  artifact_sha256: 43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a
  report_digest: 82f08c18ae76b4b4d091fe0d8be7d54cf5d10d989443132a26e550056af3f56a
manifest:
  artifact_bytes: 1094
  artifact_sha256: 8240d78b29f610cb7c566dfad50432473949c5a63b9de9c522ab28751d80fd09
  report_digest: 9aefaf24b130718f284eecb5502b3c1dd144347f6fdcfc85b47d8ec6ce3fda68
python_substantive_artifacts_byte_identical: true
```

The accepted fixture contains five ordered decisions, two unresolved advisory candidates, one fixture-only Principia reference with separate status, one explicit warning, two open questions, and deterministic export and manifest artifacts. The export contains exact references and visible metadata rather than copied canonical body authority.

See [`workspace-contracts.md`](workspace-contracts.md).

### Slice 2 — accepted static workspace and pinned browser evidence

#### Accepted shell

```yaml
state: accepted
accepted_pr: 52
tested_head: f273c79b26d9b943a9b57a259645c8b0c6a5de48
accepted_merge_commit: dcad8aaedbf9b212ed926c09bbb50690c8fae19b
shell_baseline_contract: atlas-phase4-workspace-shell-baseline/0.1
route_count: 13
entry_route_count: 5
shell_data_sha256: a2dd3979c35cee4d081511cadf98499e325dfd22d814cae097cfd3e98f3f5c0c
shell_build_digest: b4aa3fab14ecc66ee602c9c40dc88b10add23d3391915a72c31968c681edcaee
shell_report_sha256: b8b29a61495ecfc420de9324006b6f8efac455905c7b2b69f03639d995e7f932
shell_report_digest: f1b13c7c202f93a1682d9366fcbef5265a7ae36f335d4e10ddff71ce216e955b
python_substantive_artifacts_byte_identical: true
```

#### Accepted browser evidence

```yaml
state: accepted
accepted_pr: 54
tested_head: f2a9eb6f4dce8ee770024127c795598e37335921
accepted_merge_commit: 6fb5932c4a6dbe26aa005da280d80bac1e61ad18
baseline_contract: atlas-phase4-workspace-browser-baseline/0.1
engine: chromium
engine_version: 151.0.7922.34
playwright_version: 1.62.0
route_count: 13
keyboard_route_count: 13
entry_count: 5
candidate_count: 2
principia_reference_count: 1
warning_count: 1
viewport_count: 2
request_count: 120
external_request_count: 0
repeated_run_substantive_artifacts_byte_identical: true
report_artifact_bytes: 2281
report_artifact_sha256: a1f259d1cbfc40d87311a5955e6fe77f932e652b3e8ccfad19d12f629c5103f2
report_digest: 971c44ef7863d313dceffc7356187b94a15d6543e346654cbf6eadc116213311
human_verified: false
accessibility_certified: false
```

Accepted Slice 2 proves route-safe skip navigation, keyboard-only access to all thirteen routes, visible focus, exact order and revisions, read-only decisions, unresolved candidates, separate Principia status, warnings, non-graph coverage, deep links, reload and history, explicit route and package failures, local export byte identity, reduced-motion and mobile behavior, deterministic repeated evidence, independent validation, tamper rejection, and zero external requests.

The route-safe skip patch changes only the static target and focus marker. It preserves shell data, workspace export, workspace manifest, interaction semantics, and all authority boundaries.

See [`workspace-shell.md`](workspace-shell.md), [`workspace-browser-evidence.md`](workspace-browser-evidence.md), and [`workstream-3.md`](workstream-3.md).

### Slice 3 — active Workstream 3 closure and recommendation

```yaml
state: active
completion_report_candidate: atlas-phase4-workstream3-completion-report/0.1
completion_baseline_candidate: atlas-phase4-workstream3-completion-baseline/0.1
input_authority: accepted-slice-1-and-slice-2-evidence-only
closure_authority: evidence-and-recommendation-only
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
repository_mutation: false
production_frontend_architecture_selected: false
live_principia_dependency: false
```

Slice 3 must bind every accepted Slice 1 and Slice 2 identity, map all Workstream 3 exit criteria to executable gates, prove replaceability and disposable browser state, define migration and rollback boundaries, reject authority escalation, reproduce completion artifacts byte-identically across Python 3.11 and 3.13, and issue exactly one bounded recommendation.

Allowed recommendation values are:

```yaml
allowed_decisions:
  - proceed-bounded-workspace-fixture-evaluation
  - hold-accepted-bounded-workspace
  - reject-broader-workspace-implementation
```

A proceed decision authorizes only another non-production fixture evaluation under separate governance. It does not authorize production architecture, deployment, accounts, cloud persistence, live synchronization, canonical editing, or automatic authority.

## Phase 4 boundaries

### Allowed

- exact-revision Atlas views and pinned offline Principia references;
- local-first deterministic shells, workspace fixtures, exports, manifests, and browser evidence;
- keyboard, focus, semantic, deep-link, history, warning, failure, responsive, export, and network-isolation tests;
- ephemeral research questions, rationales, and include, exclude, or context decisions;
- optional graph visualization only when equivalent non-graph navigation is complete;
- accessibility fixes required by evidence when semantic and authority contracts remain unchanged;
- deterministic Workstream 3 closure evidence and a bounded recommendation.

### Still frozen

- production retrieval-quality claims;
- vector database commitment, embeddings, or learned ranking;
- implicit `latest` references;
- live Principia synchronization;
- canonical writes from browser, interface, workspace, retrieval, trail, or candidate state;
- automatic candidate resolution, review, lifecycle, promotion, merge, or release mutation;
- autonomous agents changing knowledge state;
- accounts, permissions, cloud sync, plugins, or permissionless extensions;
- active multilingual authoring;
- automatic conversion of AI review into human verification;
- accessibility certification without qualified human evidence;
- production frontend, hosting, or deployment architecture selection.

## Immediate next actions

1. define Workstream 3 completion-report and completion-baseline contracts;
2. bind accepted Slice 1 and Slice 2 identities without reinterpretation;
3. create executable closure gates and negative authority tests;
4. document replaceability, migration, rollback, and failure preservation;
5. reproduce completion evidence on Python 3.11 and 3.13;
6. issue one bounded recommendation without implementing it;
7. keep every frozen boundary unchanged.

**Phase 4 Workstreams 1 and 2 and Workstream 3 Slices 1 and 2 are accepted. Workstream 3 Slice 3 — Closure and Recommendation — is active.**
