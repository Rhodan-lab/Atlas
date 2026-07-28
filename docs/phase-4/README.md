# Phase 4 — Principia & Atlas Interactive Experience

## Status

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 3
workstream_name: read-only-research-workspace-composition
active_slice: 2
slice_name: local-browser-workspace-composition
workstream_1: accepted
workstream_2: accepted
workstream_3_slice_1: accepted
workspace_authority: ephemeral-research-only
atlas_semantics_authoritative: true
principia_status_separate: true
exact_cross_repository_references: true
preferred_bounded_retrieval: structured-field-baseline
retrieval_authority: advisory-only
local_first: true
deterministic_export_required: true
browser_state_authority: ephemeral-only
canonical_copy_authority: false
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
automatic_merge_or_resolution: false
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
  tested_head: 8172a46cd400fbcf0bce225ca908275c0d1edfdf
  accepted_merge_commit: 1f15cee1f0ed86c5a85750659b4d35e1d535564f
  report_digest: 9cbaa5f4675d995a183a6be5bee0b364eb7b6ae1da2ab9affc59b6d5fc452296
reference_shell:
  accepted_pr: 43
  tested_head: ae6e662656c40c2108c0ef52dd2c1d7f0e2f1c0f
  accepted_merge_commit: 4992d0caa0eb37db5b58158a9dd53a8ca10f1405
  shell_build_digest: ebc90a5781b7e974fe30034898364d87ebb5ed00ac05ce6cf0c27d6ded32b223
  shell_report_digest: cfa4e37b07ed95337bb1fd1cb9e795656da78020d31b46eaf19828332c74d696
closure:
  accepted_pr: 44
  tested_head: 265c44d3b39091bf6dcf1263b9cb3092d3ea4568
  accepted_merge_commit: 37b013ce1b3c8c45230feaf4c1cd6bfd0ba48735
  report_artifact_sha256: 03ba1f02d7ca2cfb7432919c7bdca110edbd497fc8c2be2c2216b099abe0cb23
  report_digest: a3167ee2dc7a02c47468a1b850e15b495f3ed6058399205fc2cdf906d922aaa3
  exit_gate_count: 10
  decision: proceed-workstream2-browser-accessibility-evidence
```

### Accepted capabilities

- eight exact-revision workflow views and deterministic routes;
- visible provenance, review level, lifecycle, staleness, and advisory authority;
- fixture-only Principia references with separate Principia status;
- explicit impact warnings and five deterministic failure categories;
- keyboard and non-graph navigation requirements;
- a static local package requiring no account, API, cloud service, or graph view;
- deterministic and replaceable generated artifacts;
- negative tests preventing implicit `latest`, hidden fallback, authority escalation, and canonical mutation.

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

### Accepted browser evidence

```yaml
accepted_pr: 46
tested_head: 05e829dcf0c331188f4e75a7ffe8e9b1434b2aab
accepted_merge_commit: d5577d9664a16b89d4c2597229f418a7f4a8f849
engine: chromium
engine_version: 151.0.7922.34
playwright_version: 1.62.0
workflow_count: 8
keyboard_workflow_count: 9
viewport_count: 2
request_count: 4
loopback_request_count: 4
external_request_count: 0
repeated_run_substantive_artifacts_byte_identical: true
human_verified: false
accessibility_certified: false
```

The accepted evidence records skip navigation, deterministic keyboard order, visible focus, landmarks, heading hierarchy, labels, live regions, exact-revision deep links, reload, browser history, non-graph equivalents, warnings, failures, reduced motion, bounded desktop and mobile viewports, local operation, and zero external requests.

### Accepted closure

```yaml
accepted_pr: 47
tested_head: f15e085317ed898cfca545f1492f53b4882e4045
accepted_merge_commit: dca6dd1bf8b8445bb4101ad7a3503dd79a57ea74
report_artifact_bytes: 4070
report_artifact_sha256: 4cccee425316ed329979cb9f5eb900a7a7ee3656c72822ecffa8f4f15ef76786
report_digest: 926eb576fb216fca2d1f5a52d11f977f7c743c058d9a8a31d81ffc265f2d9913
exit_gate_count: 12
python_substantive_artifacts_byte_identical: true
decision: proceed-workstream3-read-only-research-workspace
```

Automated browser evidence is necessary but not equivalent to human accessibility certification, assistive-technology user review, or broad usability validation.

See [`browser-evidence.md`](browser-evidence.md) and [`workstream-2-completion.md`](workstream-2-completion.md).

## Workstream 3 — active read-only research workspace composition

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

### Pinned Slice 1 evidence

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

The accepted fixture contains five ordered include, exclude, or context decisions; two unresolved advisory candidates; one fixture-only Principia reference with separate status; one explicit impact warning; two open questions; and complete authority and limitation metadata.

The accepted validator rejects implicit `latest`, duplicate entries, copied canonical authority, automatic candidate resolution, unavailable revisions, lifecycle mutation, live Principia dependency, nondeterministic export fields, external-network requirements, and missing non-graph equivalents. Every failure preserves the previous valid workspace.

The accepted export preserves exact revision keys, stable order, source and upstream digests, decisions, rationales, open questions, separate Principia status, warnings, limitations, and visible metadata. It contains no canonical body authority and reproduces byte-identically on Python 3.11 and 3.13.

See [`workspace-contracts.md`](workspace-contracts.md).

### Slice 2 — active local browser workspace composition

Slice 2 may expose the accepted export through a bounded static local experience. It may not reinterpret, reorder, mutate, or regenerate accepted workspace decisions in the browser.

```yaml
state: active
input_authority: accepted-workspace-export-only
browser_state_authority: ephemeral-only
exact_revision_required: true
entry_order_preserved: true
decisions_read_only: true
candidates_unresolved: true
principia_status_separate: true
warning_visibility_required: true
keyboard_workflow_required: true
non_graph_workflow_required: true
reduced_motion_required: true
zero_external_requests_required: true
local_export_allowed: true
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
repository_mutation: false
production_frontend_architecture_selected: false
```

The bounded browser package should expose deterministic routes for:

- workspace overview and authority;
- five ordered entry decisions with exact revision keys;
- unresolved contradiction and duplicate candidates;
- the separate-status fixture-only Principia reference;
- the explicit impact warning;
- open questions, limitations, provenance, review, lifecycle, and staleness;
- accepted export and manifest identities;
- a local download that reproduces the accepted export bytes.

Browser restoration may use only bounded URL or in-memory state. No local or session storage becomes authority, and no browser state may create canonical persistence.

### Browser evidence requirements

Slice 2 must prove:

1. complete keyboard operation and visible focus;
2. complete non-graph and text-equivalent navigation;
3. exact entry order, decisions, revisions, and digests;
4. deterministic deep links, reload, and back/forward behavior;
5. unresolved candidate and separate Principia status visibility;
6. explicit warnings, limitations, and non-mutation authority;
7. reduced-motion and bounded desktop/mobile behavior;
8. zero external requests after local boot;
9. local download byte identity with the accepted export;
10. no account, cloud service, live dependency, canonical write, or production architecture.

See [`workstream-3.md`](workstream-3.md).

## Atlas and Principia authority boundary

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns explanation, pathways, investigations, simulations, dossiers, failure analysis, design experiences, and its own readiness.
- Principia may reference exact Atlas revisions.
- Neither repository inherits the other repository's status.
- Browser and workspace state have no canonical or lifecycle authority.
- Pinned offline Principia fixtures are permitted, but no live cross-repository dependency is active.

## Phase 4 boundary

Allowed:

- local-first interaction contracts, static shells, bounded browser evidence harnesses, and read-only workspace fixtures;
- exact-revision Atlas views and pinned offline Principia references;
- deterministic keyboard, focus, semantic, deep-link, history, warning, failure, offline, responsive, export, and network-isolation tests;
- ephemeral research notes, questions, rationales, and include, exclude, or context decisions;
- deterministic read-only exports and bounded local views over accepted exports;
- accessibility corrections required by evidence, provided accepted semantics and authority remain unchanged;
- optional graph visualization only with complete equivalent non-graph navigation.

Still frozen:

- production retrieval-quality claims;
- vector database commitment, embeddings, or learned ranking;
- implicit `latest` references;
- live Principia synchronization;
- canonical writes from browser, interface, workspace, retrieval, trail, or candidate state;
- automatic candidate resolution, review, lifecycle, promotion, merge, or release mutation;
- synthetic bridge events as canonical lifecycle history;
- accounts, permissions, cloud synchronization, plugins, or autonomous agents;
- active multilingual authoring;
- automatic conversion of AI review into human verification;
- accessibility certification without qualified human evidence;
- production frontend, hosting, or deployment architecture selection.

## Workstream 3 exit criteria

Workstream 3 closes only when:

- all workspace contracts are versioned and executable;
- the bounded exact-revision fixture validates;
- all required negative cases are rejected deterministically;
- workspace order, decisions, references, warnings, and candidates remain explicit;
- deterministic exports reproduce byte-identically across supported Python versions;
- no workspace action can mutate canonical, review, lifecycle, merge, release, Principia, or repository state;
- the workspace operates locally without accounts, cloud services, or external network access;
- a browser evidence slice proves keyboard and non-graph multi-step operation;
- a completion report recommends or rejects broader workspace implementation.

## Immediate next actions

1. build a replaceable static workspace package from the accepted export and manifest;
2. expose deterministic overview, entry, candidate, Principia, warning, question, limitation, and export routes;
3. preserve exact revisions, order, decisions, and all accepted digests without browser-side reinterpretation;
4. add keyboard, visible-focus, non-graph, reduced-motion, deep-link, reload, and history evidence;
5. prove browser restoration remains ephemeral and non-canonical;
6. reject every external request and verify local download byte identity;
7. keep production architecture, live synchronization, accounts, cloud persistence, canonical writes, and automatic authority frozen.

**Phase 4 Workstreams 1 and 2 and Workstream 3 Slice 1 are accepted. Workstream 3 Slice 2 — Local Browser Workspace Composition — is active.**
