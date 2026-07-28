# Phase 4 Workstream 3 — Read-Only Research Workspace Composition

## Status

```yaml
phase: 4
workstream: 3
mode: interactive-experience-foundation
state: active
active_slice: 3
slice_name: workstream-3-closure-and-recommendation
slice_1: accepted
slice_2: accepted
workspace_authority: ephemeral-research-only
browser_state_authority: ephemeral-only
exact_revision_required: true
principia_status_separate: true
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

## Objective

Compose accepted exact-revision Atlas views and pinned offline Principia references into a deterministic, read-only, multi-step research workspace. The workspace may organize evidence, questions, decisions, candidates, comparisons, and exports, but it has no canonical, review, lifecycle, merge, release, or repository authority.

Workstream 3 is a composition and evidence workstream. It does not authorize a production frontend architecture, live synchronization, accounts, cloud persistence, canonical editing, automatic candidate resolution, or inherited Principia status.

## Slice 1 — accepted workspace data and export contracts

### Accepted contracts

```yaml
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

### Accepted evidence

```yaml
accepted_pr: 50
tested_head: 6d556bde6c24a8313bece3074f6c5fc56c4c4ccd
accepted_merge_commit: 86c1f9f779172aa47d450022fc40357a93f2302f
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

### Accepted bounded fixture

The accepted fixture composes the Phase 3 research trail into one exact-revision workspace containing:

- five ordered decisions: two include, one exclude, and two context;
- two unresolved advisory candidates;
- one fixture-only pinned Principia reference with separate draft status;
- one explicit unavailable-revision impact warning;
- two open questions;
- deterministic export and manifest artifacts;
- machine-readable authority and limitation metadata.

The export derives visible title, type, lifecycle, review, staleness, and provenance metadata from exact canonical revisions. It contains references and metadata rather than canonical body authority.

### Accepted failure semantics

The validator rejects:

1. implicit `latest` references — `E-WORKSPACE-LATEST`;
2. duplicate workspace entries — `E-WORKSPACE-DUPLICATE-ENTRY`;
3. copied canonical authority — `E-WORKSPACE-COPIED-AUTHORITY`;
4. automatic candidate resolution — `E-WORKSPACE-CANDIDATE-AUTHORITY`;
5. unavailable revisions — `E-WORKSPACE-UNAVAILABLE-REVISION`;
6. lifecycle mutation — `E-WORKSPACE-LIFECYCLE-MUTATION`;
7. live or status-inheriting Principia references — `E-WORKSPACE-PRINCIPIA-STATUS`;
8. nondeterministic fields — `E-WORKSPACE-DETERMINISM`;
9. external-network requirements — `E-WORKSPACE-NETWORK`;
10. missing non-graph equivalents — `E-WORKSPACE-NON-GRAPH`.

Every rejected operation records that the previous valid workspace remains preserved. No failure silently substitutes a revision, reorders entries, merges candidates, inherits status, or writes repository state.

## Slice 2 — accepted local browser workspace composition

### Accepted static shell

```yaml
state: accepted
accepted_pr: 52
tested_head: f273c79b26d9b943a9b57a259645c8b0c6a5de48
accepted_merge_commit: dcad8aaedbf9b212ed926c09bbb50690c8fae19b
shell_data_contract: atlas-workspace-shell-data/0.1
shell_validation_contract: atlas-workspace-shell-validation/0.1
shell_build_report_contract: atlas-workspace-shell-build-report/0.1
shell_baseline_contract: atlas-phase4-workspace-shell-baseline/0.1
route_count: 13
entry_route_count: 5
shell_data_bytes: 5955
shell_data_sha256: a2dd3979c35cee4d081511cadf98499e325dfd22d814cae097cfd3e98f3f5c0c
shell_build_digest: b4aa3fab14ecc66ee602c9c40dc88b10add23d3391915a72c31968c681edcaee
shell_report_bytes: 1448
shell_report_sha256: b8b29a61495ecfc420de9324006b6f8efac455905c7b2b69f03639d995e7f932
shell_report_digest: f1b13c7c202f93a1682d9366fcbef5265a7ae36f335d4e10ddff71ce216e955b
python_substantive_artifacts_byte_identical: true
```

The shell is a replaceable static reader over the accepted Slice 1 export and manifest. It provides deterministic routes for overview, five ordered entries, candidates, Principia, warnings, questions, limitations, evidence, and a complete text summary. It uses URL and in-memory state only and does not maintain an editable duplicate workspace model.

### Accepted browser contracts

```yaml
workspace_browser_workflow: atlas-workspace-browser-workflow-evidence/0.1
workspace_browser_accessibility: atlas-workspace-browser-accessibility-report/0.1
workspace_browser_network: atlas-workspace-browser-network-report/0.1
workspace_browser_failure: atlas-workspace-browser-failure-evidence/0.1
workspace_browser_manifest: atlas-phase4-workspace-browser-manifest/0.1
workspace_browser_report: atlas-phase4-workspace-browser-report/0.1
workspace_browser_validation: atlas-phase4-workspace-browser-validation/0.1
workspace_browser_baseline: atlas-phase4-workspace-browser-baseline/0.1
```

### Accepted browser evidence

```yaml
state: accepted
accepted_pr: 54
tested_head: f2a9eb6f4dce8ee770024127c795598e37335921
accepted_merge_commit: 6fb5932c4a6dbe26aa005da280d80bac1e61ad18
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

The 120 requests are bounded loopback requests produced by fresh keyboard traversals, direct-link and history checks, mobile evidence, and the explicit missing-artifact test. One loopback request is deliberately blocked by the test harness. No external request, remote asset, credential, analytics endpoint, or cloud service is used.

### Route-safe skip-navigation patch

Pinned browser evidence found that the original `#main-content` skip target conflicted with the hash router. The accepted compatibility patch moves the target to `#overview` and adds a focusable marker inside `<main>`.

```yaml
patched_index_html_bytes: 3232
patched_index_html_sha256: ae7eafc4dccae669f25ed4f6e6e5bc8e81bce8dcabcc81b5d585d4d09fb5e921
interaction_semantics_changed: false
workspace_data_changed: false
workspace_export_changed: false
workspace_manifest_changed: false
```

The patch changes no workspace decision, route set, accepted digest, lifecycle rule, review rule, Principia status, or repository authority.

### Accepted browser evidence coverage

The accepted evidence proves:

1. route-safe skip navigation, landmarks, heading hierarchy, accessible names, status, and alert regions;
2. keyboard-only operation and visible focus for all thirteen routes;
3. exact entry order, decisions, revisions, and digests;
4. deterministic deep links, reload, back, and forward behavior;
5. complete non-graph and text-equivalent navigation;
6. unresolved candidate status and separate Principia status;
7. warning, limitation, and non-mutation authority visibility;
8. reduced-motion and bounded desktop/mobile behavior;
9. zero external requests;
10. local download byte identity with the accepted export;
11. explicit unknown-route and missing-artifact failures without fallback or persistence;
12. no account, cloud service, live dependency, canonical write, or production architecture.

The complete evidence directory is generated twice and compared byte-for-byte. Independent validation verifies all child hashes and semantic digests. Resealed tamper tests reject external requests, download drift, false human-verification claims, and candidate resolution.

## Slice 3 — active Workstream 3 closure and recommendation

### Purpose

Close Workstream 3 without expanding its authority. Slice 3 may inspect and bind accepted Slice 1 and Slice 2 evidence, create deterministic closure artifacts, and recommend or reject one bounded next experiment. It may not implement the recommendation, select production architecture, or activate any frozen capability.

### Candidate closure contracts

```yaml
completion_report: atlas-phase4-workstream3-completion-report/0.1
completion_baseline: atlas-phase4-workstream3-completion-baseline/0.1
```

These names remain candidates until executable evidence, negative cases, repeated-run identity, and immutable-head CI pass.

### Required closure inputs

The completion report must bind:

- PR #50 Slice 1 tested head, merge commit, fixture, report, export, manifest, and baseline identities;
- PR #52 shell tested head, merge commit, static package identity, shell data, build report, and shell baseline;
- PR #54 browser tested head, merge commit, baseline, engine, workflow, accessibility, network, failure, manifest, report, and validation identities;
- the route-safe skip-navigation patch identity;
- all relevant authority and limitation fields.

It may not regenerate accepted decisions, modify evidence records, or reinterpret candidate status.

### Closure gates

Workstream 3 closes only when the completion evidence proves:

1. Slice 1 and Slice 2 accepted identities are exact and immutable;
2. the bounded local browser package is deterministic and replaceable;
3. routes preserve exact revisions, entry order, decisions, candidates, warnings, limitations, and authority;
4. keyboard and non-graph multi-step operation pass in the pinned browser;
5. local download reproduces the accepted export bytes;
6. repeated shell and browser evidence remains byte-identical;
7. generated browser state is disposable and unnecessary for exact reload;
8. unknown routes and unavailable artifacts fail visibly while preserving prior valid state;
9. no workspace or browser action can mutate canonical, review, lifecycle, merge, release, Principia, or repository state;
10. the workspace operates locally without accounts, cloud services, credentials, or external network access;
11. migration and rollback boundaries are explicit and do not choose production infrastructure;
12. completion artifacts reproduce byte-identically across Python 3.11 and 3.13;
13. one bounded recommendation is issued with limitations and evidence visible.

### Allowed closure decisions

Exactly one decision may be issued:

```yaml
allowed_decisions:
  - proceed-bounded-workspace-fixture-evaluation
  - hold-accepted-bounded-workspace
  - reject-broader-workspace-implementation
```

A `proceed` decision authorizes only another non-production, fixture-bound evaluation under separate governance. It does not authorize a production frontend, deployment, accounts, cloud persistence, live synchronization, semantic infrastructure, canonical editing, or automated authority.

### Required negative cases

The closure validator must reject at least:

- a mismatched accepted Slice 1 artifact or digest;
- a mismatched accepted Slice 2 shell artifact or digest;
- a mismatched browser engine or evidence artifact;
- a false human-verification or accessibility-certification claim;
- any production architecture selection;
- any live Principia dependency;
- any account, cloud, credential, or external-network requirement;
- any canonical, review, lifecycle, candidate-resolution, release, or repository mutation authority;
- any recommendation outside the allowed decision set;
- any missing replaceability, migration, rollback, or limitation evidence.

Every rejection must preserve the accepted Workstream 3 state.

## Workspace authority

A workspace is an ephemeral research artifact. It may:

- reference exact Atlas entity revisions;
- reference pinned offline Principia envelopes with separate Principia status;
- include accepted retrieval results, filters, research trails, warnings, and advisory candidates;
- record questions, rationales, and bounded include, exclude, or context decisions in accepted fixtures;
- produce deterministic read-only exports;
- expose accepted artifacts through a bounded local browser package;
- preserve provenance, review level, lifecycle, staleness, and authority labels from referenced records;
- produce deterministic closure evidence and a bounded recommendation.

A workspace may not:

- copy itself into canonical authority;
- edit canonical entities, evidence, claims, models, sources, or relations;
- change review level, lifecycle, staleness, promotion, merge, release, or Principia readiness;
- resolve contradiction, duplicate, or bridge candidates automatically;
- replace exact revisions with implicit `latest`;
- infer that a workspace decision is an Atlas governance decision;
- write to the repository, require an account, or depend on cloud persistence;
- activate live Principia synchronization or external semantic services;
- select a production frontend, hosting, or deployment architecture.

## Immediate implementation sequence

1. define the completion-report and completion-baseline schemas;
2. load and verify accepted Slice 1 and Slice 2 baselines and identities;
3. map all thirteen closure gates to deterministic executable evidence;
4. document replaceability, migration, rollback, and failure-preservation boundaries;
5. implement negative cases for identity drift and authority escalation;
6. build the completion report and baseline twice on Python 3.11 and 3.13;
7. require byte identity and immutable-head CI;
8. issue one bounded recommendation without implementing it;
9. keep production architecture, live synchronization, accounts, cloud persistence, canonical writes, and automatic authority frozen.
