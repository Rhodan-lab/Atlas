# Phase 4 — Principia & Atlas Interactive Experience

## Status

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 3
workstream_name: read-only-research-workspace-composition
workstream_1: accepted
workstream_2: accepted
atlas_semantics_authoritative: true
workspace_authority: ephemeral-research-only
principia_status_separate: true
exact_cross_repository_references: true
preferred_bounded_retrieval: structured-field-baseline
retrieval_authority: advisory-only
local_first: true
deterministic_export_required: true
production_frontend_architecture_selected: false
live_principia_dependency: false
canonical_mutation: false
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

## Workstream 1 — accepted interaction contracts and reference shell

Workstream 1 defined the smallest versioned interaction model and local reference shell capable of exercising accepted knowledge, retrieval, trail, candidate, and bridge semantics.

```yaml
interaction_contracts_pr: 42
reference_shell_pr: 43
closure_pr: 44
closure_merge_commit: 37b013ce1b3c8c45230feaf4c1cd6bfd0ba48735
completion_contract: atlas-phase4-workstream1-completion-report/0.1
completion_baseline_contract: atlas-phase4-workstream1-completion-baseline/0.1
report_artifact_sha256: 03ba1f02d7ca2cfb7432919c7bdca110edbd497fc8c2be2c2216b099abe0cb23
report_digest: a3167ee2dc7a02c47468a1b850e15b495f3ed6058399205fc2cdf906d922aaa3
exit_gate_count: 10
```

Accepted capabilities include exact-revision workflow views, deterministic routes, visible authority metadata, separate Atlas and Principia status, explicit failures, keyboard and non-graph navigation, and a static local package requiring no account, API, cloud service, or graph view.

See [`interaction-contract.md`](interaction-contract.md), [`reference-shell.md`](reference-shell.md), and [`workstream-1-completion.md`](workstream-1-completion.md).

## Workstream 2 — accepted browser accessibility and workflow evidence

Workstream 2 used a pinned real browser against the accepted static package and established bounded automated evidence for workflow operation, accessibility foundations, deterministic routing, local operation, and authority isolation.

```yaml
browser_evidence_pr: 46
browser_evidence_merge_commit: d5577d9664a16b89d4c2597229f418a7f4a8f849
closure_pr: 47
closure_tested_head: f15e085317ed898cfca545f1492f53b4882e4045
closure_merge_commit: dca6dd1bf8b8445bb4101ad7a3503dd79a57ea74
completion_contract: atlas-phase4-workstream2-completion-report/0.1
completion_baseline_contract: atlas-phase4-workstream2-completion-baseline/0.1
report_artifact_bytes: 4070
report_artifact_sha256: 4cccee425316ed329979cb9f5eb900a7a7ee3656c72822ecffa8f4f15ef76786
report_digest: 926eb576fb216fca2d1f5a52d11f977f7c743c058d9a8a31d81ffc265f2d9913
exit_gate_count: 12
python_substantive_artifacts_byte_identical: true
decision: proceed-workstream3-read-only-research-workspace
```

### Accepted browser evidence

```yaml
engine: chromium
engine_version: 151.0.7922.34
playwright_version: 1.62.0
workflow_count: 8
keyboard_workflow_count: 9
viewport_count: 2
external_request_count: 0
repeated_run_byte_identical: true
human_verified: false
accessibility_certified: false
```

Accepted evidence covers keyboard traversal, visible focus, skip navigation, landmarks, headings, labels, status and error semantics, exact-revision deep links, reload and history behavior, complete non-graph paths, warnings and failures, reduced motion, bounded responsive behavior, local operation, and zero external requests.

This remains automated evidence. It does not establish human accessibility, assistive-technology usability, broad browser compatibility, or production readiness.

See [`browser-evidence.md`](browser-evidence.md) and [`workstream-2-completion.md`](workstream-2-completion.md).

## Workstream 3 — active read-only research workspace composition

### Objective

Compose accepted exact-revision views into a complete, deterministic, local research workflow while preserving Atlas and Principia authority boundaries.

A researcher should be able to:

1. start from a bounded retrieval result or exact Atlas revision;
2. inspect provenance, review level, lifecycle, and staleness;
3. apply accepted deterministic filters;
4. include, exclude, or contextualize exact revisions in an ephemeral workspace;
5. record ordered rationales and open questions;
6. inspect advisory contradiction and duplicate candidates without resolving them automatically;
7. attach pinned offline Principia references without inheriting status;
8. surface unavailable-revision and cross-repository impact warnings;
9. export a deterministic package containing references and decisions, not copied canonical authority.

### Entry boundary

```yaml
workspace_authority: ephemeral-research-only
canonical_copy_authority: false
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
automatic_merge_or_resolution: false
exact_revision_required: true
principia_status_separate: true
non_graph_workflow_required: true
local_first: true
deterministic_export_required: true
account_required: false
cloud_required: false
external_network_required: false
production_frontend_architecture_selected: false
live_principia_dependency: false
repository_mutation: false
```

### Candidate contract families

The first executable slice should define:

- workspace identity and revision;
- ordered exact-revision workspace entries;
- include, exclude, and context decisions;
- workspace rationales and open questions;
- pinned query, filter, research-trail, and candidate identities;
- offline Principia references with separate status;
- deterministic export package and manifest;
- explicit stale, unavailable, mismatch, duplicate-entry, copied-authority, and mutation failures;
- browser-state restoration without canonical persistence.

Contract names remain candidates until executable fixtures and deterministic evidence are accepted.

### Required evidence

Workstream 3 must prove:

- all references use exact revisions and reject implicit `latest`;
- workspace entries are ordered and unique;
- include, exclude, and context decisions remain advisory and non-mutating;
- canonical body text is not copied as workspace authority;
- candidate contradictions and duplicates are not automatically resolved;
- Principia status remains separate;
- deterministic export and manifest records are byte-identical across repeated runs;
- parent-child digests and accepted upstream evidence identities are preserved;
- explicit failures retain the prior valid workspace state;
- browser restoration, if added, persists only ephemeral workspace state;
- no account, cloud service, external request, live dependency, or production architecture is required.

See [`workstream-3.md`](workstream-3.md).

## Atlas and Principia authority boundary

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns explanation, pathways, investigations, simulations, dossiers, failure analysis, design experiences, and its own readiness.
- Principia may reference exact Atlas revisions.
- Neither repository inherits the other repository's status.
- Browser and workspace state have no canonical, review, lifecycle, merge, or release authority.
- No live cross-repository dependency is active.

## Phase 4 boundary

Allowed:

- local-first interaction contracts, static shells, browser evidence harnesses, and read-only workspace contracts;
- exact-revision Atlas views and pinned offline Principia references;
- deterministic keyboard, focus, semantic, route, history, warning, failure, offline, responsive, export, and network-isolation evidence;
- accessibility corrections required by evidence, provided accepted semantics and authority remain unchanged;
- optional graph visualization only with complete equivalent non-graph navigation.

Still frozen:

- production retrieval-quality claims;
- vector databases, embeddings, learned ranking, or external semantic services;
- implicit `latest` references;
- live Principia synchronization;
- canonical, review, lifecycle, merge, or release writes from browser or workspace state;
- automatic contradiction resolution or duplicate merge;
- accounts, permissions, cloud sync, analytics, plugins, collaboration, or autonomous agents;
- active multilingual authoring;
- automatic conversion of AI review into human verification;
- production frontend, hosting, or deployment architecture selection;
- accessibility certification or human usability claims;
- screenshots as authority.

## Immediate next actions

1. define workspace, entry, decision, export, manifest, and failure contracts;
2. create one deterministic exact-revision fixture spanning retrieval, filtering, research-trail decisions, advisory candidates, and a pinned offline Principia reference;
3. reject implicit `latest`, duplicate entries, unavailable revisions, copied authority, automatic candidate resolution, and lifecycle mutation;
4. generate the export twice and require byte identity;
5. independently validate every digest and authority boundary;
6. keep production architecture, live synchronization, canonical writes, accounts, cloud services, and automatic authority frozen.

**Phase 4 Workstreams 1 and 2 are accepted. Workstream 3 — Read-Only Research Workspace Composition — is active.**
