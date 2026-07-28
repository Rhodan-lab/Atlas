# Phase 4 — Principia & Atlas Interactive Experience

## Status

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 2
workstream_name: browser-accessibility-and-workflow-evidence
workstream_1: accepted
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

Phase 4 builds a unified experience over proven Atlas and Principia semantics without erasing repository ownership, lifecycle status, provenance, revision identity, or authority boundaries. It may expose accepted semantics but may not redefine them.

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
workstream_1_closure:
  accepted_pr: 44
  tested_head: 265c44d3b39091bf6dcf1263b9cb3092d3ea4568
  accepted_merge_commit: 37b013ce1b3c8c45230feaf4c1cd6bfd0ba48735
  completion_contract: atlas-phase4-workstream1-completion-report/0.1
  completion_baseline_contract: atlas-phase4-workstream1-completion-baseline/0.1
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

## Workstream 2 — active browser accessibility and workflow evidence

### Objective

Use a real browser against the accepted static shell to determine whether the required workflows are genuinely operable, perceivable, deterministic, offline-capable, and authority-safe.

Workstream 2 is an evidence phase. It is not permission for broad visual redesign, productization, deployment architecture selection, or live repository integration.

### Candidate evidence contracts

```yaml
browser_workflow_contract: atlas-browser-workflow-evidence/0.1
browser_accessibility_contract: atlas-browser-accessibility-report/0.1
browser_network_contract: atlas-browser-network-report/0.1
browser_failure_contract: atlas-browser-failure-evidence/0.1
browser_evidence_manifest: atlas-phase4-browser-evidence-manifest/0.1
```

These names remain candidates until executable fixtures and CI evidence are accepted.

### Required browser workflows

A pinned browser harness must exercise:

1. loading the local shell and reaching the primary content through the skip link;
2. traversing the workflow selector and every workflow by keyboard;
3. opening exact-revision deep links and preserving them through reload;
4. using browser back and forward navigation deterministically;
5. inspecting entity, provenance, retrieval, filter, research-trail, candidate, Principia-reference, and impact-warning views;
6. reaching equivalent list or text routes without graph visualization;
7. exposing authority metadata and separate Atlas and Principia status;
8. displaying warnings and all accepted failure categories;
9. operating from the generated local package with no external network request;
10. proving that browser interactions cannot write canonical, review, lifecycle, merge, or release state.

### Accessibility evidence

The browser report must inspect:

- keyboard reachability and deterministic focus order;
- visible focus indication;
- skip-link operation;
- main, navigation, header, and footer landmarks;
- heading hierarchy;
- accessible names and labels for interactive controls;
- live status and error announcements where required;
- text equivalents for relation and graph-capable workflows;
- information that remains understandable without color, hover, position, or motion;
- reduced-motion compatibility;
- viewport behavior at a bounded desktop and mobile size.

Automated accessibility evidence is necessary but not equivalent to human accessibility certification.

### Network and offline evidence

The harness must:

- start from a deterministically generated shell package;
- serve only from loopback;
- record every browser request;
- reject any non-loopback request;
- require no account, credential, API key, remote font, image, stylesheet, script, analytics endpoint, or cloud service;
- verify that the package remains usable after the test server is isolated from external networking.

### Browser boundary

The first candidate may use one pinned Chromium engine as a controlled test instrument. This does not select a production browser or frontend architecture. Additional engines are justified only if they affect a documented decision.

Screenshots may assist debugging but are not authoritative evidence. The accepted evidence must be deterministic, machine-readable records of workflows, focus, semantics, requests, failures, and decisions.

## Atlas and Principia authority boundary

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns explanation, pathways, investigations, simulations, dossiers, failure analysis, design experiences, and its own readiness.
- Principia may reference exact Atlas revisions.
- Neither repository inherits the other repository's status.
- Browser state and offline fixtures have no canonical or lifecycle authority.
- No live cross-repository dependency is active.

## Phase 4 boundary

Allowed:

- local-first interaction contracts, static shells, and bounded browser evidence harnesses;
- exact-revision Atlas views and pinned offline Principia references;
- deterministic keyboard, focus, semantic, deep-link, history, warning, failure, offline, responsive, and network-isolation tests;
- accessibility corrections required by evidence, provided accepted semantics and authority remain unchanged;
- optional graph visualization only with complete equivalent non-graph navigation.

Still frozen:

- production retrieval-quality claims;
- vector database commitment, embeddings, or learned ranking;
- implicit `latest` references;
- live Principia synchronization;
- canonical writes from browser, interface, retrieval, trail, or candidate state;
- automatic review, lifecycle, promotion, merge, or release mutation;
- synthetic bridge events as canonical lifecycle history;
- accounts, permissions, cloud synchronization, plugins, or autonomous agents;
- active multilingual authoring;
- automatic conversion of AI review into human verification;
- production frontend, hosting, or deployment architecture selection from bounded evidence.

## Workstream 2 exit criteria

Workstream 2 closes only when:

- browser evidence contracts and fixtures are versioned and executable;
- required workflows pass in the pinned browser environment;
- keyboard traversal, focus visibility, landmarks, headings, labels, and announcements are recorded;
- exact-revision deep links and browser history are deterministic;
- every workflow has a non-graph route;
- warnings and failure states remain visible and authority-safe;
- no external request occurs;
- local and offline package behavior is recorded;
- generated evidence is deterministic, replaceable, and pinned;
- a completion report recommends or rejects broader interface implementation.

## Immediate next actions

1. define the browser evidence manifest and report contracts;
2. add a pinned Chromium harness against the generated local package;
3. execute keyboard, focus, landmark, heading, label, live-region, and error-summary checks;
4. execute exact-route reload and history checks;
5. execute every non-graph workflow and failure-state path;
6. block and record external requests;
7. emit deterministic machine-readable evidence;
8. keep production architecture, live synchronization, canonical writes, and automatic authority frozen.

**Phase 4 Workstream 1 is accepted. Workstream 2 — Browser Accessibility and Workflow Evidence — is active.**
