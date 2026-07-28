# Phase 4 Workstream 3 — Read-Only Research Workspace Composition

## Status

```yaml
phase: 4
workstream: 3
mode: interactive-experience-foundation
state: active
active_slice: 2
slice_name: local-browser-workspace-composition
slice_1: accepted
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

Workstream 3 is a composition and evidence workstream. It does not authorize a production frontend architecture, live synchronization, accounts, cloud persistence, canonical editing, or automatic candidate resolution.

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

## Slice 2 — active local browser workspace composition

### Purpose

Expose the accepted Slice 1 export and manifest through a small, replaceable static local experience. The browser layer is a deterministic reader and navigator, not a second workspace engine.

The browser may not:

- recompute retrieval rankings;
- create, remove, reorder, or reinterpret accepted entries;
- change include, exclude, or context decisions;
- resolve advisory candidates;
- infer Atlas status from Principia or Principia status from Atlas;
- change canonical, review, lifecycle, merge, release, or repository state;
- select a production frontend framework or deployment architecture.

### Accepted input authority

```yaml
input_export_contract: atlas-research-workspace-export/0.1
input_export_sha256: 43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a
input_export_digest: 82f08c18ae76b4b4d091fe0d8be7d54cf5d10d989443132a26e550056af3f56a
input_manifest_contract: atlas-research-workspace-manifest/0.1
input_manifest_sha256: 8240d78b29f610cb7c566dfad50432473949c5a63b9de9c522ab28751d80fd09
input_manifest_digest: 9aefaf24b130718f284eecb5502b3c1dd144347f6fdcfc85b47d8ec6ce3fda68
input_authority: accepted-workspace-export-only
```

The package builder must regenerate those accepted artifacts from canonical and pinned fixture inputs, verify the accepted baseline, and copy the exact bytes into the static package. It may not maintain a manually edited duplicate export.

### Required static views

The bounded package must expose deterministic, exact routes for:

1. workspace overview and authority;
2. five ordered entry decisions;
3. unresolved contradiction and duplicate candidates;
4. the fixture-only Principia reference with separate status;
5. the impact warning;
6. open questions;
7. limitations and non-goals;
8. accepted export and manifest identities;
9. a complete text-only or non-graph summary.

A graph view is optional and is not required for acceptance. No route may use implicit `latest` or silently fall back to a different entry.

### Browser state boundary

Browser state must remain ephemeral and non-authoritative.

Allowed state:

- the current deterministic route;
- the currently focused or expanded read-only section;
- a bounded in-memory navigation position;
- a URL hash or query representation containing only accepted route identifiers.

Forbidden state:

- canonical or lifecycle state;
- edited decisions or reordered entries;
- candidate resolution;
- Principia status inheritance;
- hidden persistence that becomes authority;
- account, cloud, analytics, or external-service state;
- credentials or repository write tokens.

If local or session storage is used at all, it must be proven disposable, non-authoritative, and unnecessary for exact reload. The preferred first implementation uses URL and in-memory state only.

### Local export action

The browser may offer one local download action only when it reproduces the accepted `workspace-export.json` bytes exactly.

The action must:

- use the accepted filename or a deterministic equivalent;
- preserve byte identity and SHA-256;
- require no network request;
- create no Atlas or Principia write;
- make its research-only authority visible;
- remain optional to navigation and inspection.

### Required browser evidence

The first browser candidate must use the accepted pinned browser toolchain unless separately amended:

```yaml
engine: chromium
engine_version: 151.0.7922.34
playwright_version: 1.62.0
viewports:
  - desktop: 1440x1000
  - mobile: 390x844
external_request_count: 0
human_verified: false
accessibility_certified: false
```

Evidence must prove:

1. skip navigation, landmarks, heading hierarchy, names, labels, and live/error regions;
2. complete keyboard operation and visible focus;
3. exact entry order, decisions, revisions, and digests;
4. deterministic deep links, reload, back, and forward behavior;
5. complete non-graph and text-equivalent navigation;
6. unresolved candidate status and separate Principia status;
7. warning, limitation, and non-mutation authority visibility;
8. reduced-motion and bounded desktop/mobile behavior;
9. zero external requests after local boot;
10. local download byte identity with the accepted export;
11. failure preservation for unknown routes and unavailable artifacts;
12. no account, cloud service, live dependency, canonical write, or production architecture.

Evidence directories must be generated twice and compared byte-for-byte. Independent validation must verify all child hashes and semantic digests.

### Candidate browser contracts

Contract names remain candidates until executable evidence is built. Expected families include:

```yaml
workspace_shell_data: atlas-workspace-shell-data/0.1
workspace_shell_build_report: atlas-workspace-shell-build-report/0.1
workspace_browser_workflow: atlas-workspace-browser-workflow-evidence/0.1
workspace_browser_accessibility: atlas-workspace-browser-accessibility-report/0.1
workspace_browser_network: atlas-workspace-browser-network-report/0.1
workspace_browser_failure: atlas-workspace-browser-failure-evidence/0.1
workspace_browser_manifest: atlas-phase4-workspace-browser-manifest/0.1
workspace_browser_report: atlas-phase4-workspace-browser-report/0.1
```

These names are not accepted contracts until exact fixtures, negative cases, repeatability evidence, and immutable-head CI pass.

## Workspace authority

A workspace is an ephemeral research artifact. It may:

- reference exact Atlas entity revisions;
- reference pinned offline Principia envelopes with separate Principia status;
- include accepted retrieval results, filters, research trails, warnings, and advisory candidates;
- record questions, rationales, and bounded include, exclude, or context decisions in accepted fixtures;
- produce deterministic read-only exports;
- expose accepted artifacts through a bounded local browser package;
- preserve provenance, review level, lifecycle, staleness, and authority labels from referenced records.

A workspace may not:

- copy itself into canonical authority;
- edit canonical entities, evidence, claims, models, sources, or relations;
- change review level, lifecycle, staleness, promotion, merge, release, or Principia readiness;
- resolve contradiction, duplicate, or bridge candidates automatically;
- replace exact revisions with implicit `latest`;
- infer that a workspace decision is an Atlas governance decision;
- write to the repository, require an account, or depend on cloud persistence;
- activate live Principia synchronization or external semantic services.

## Workstream 3 exit criteria

Workstream 3 closes only when:

- the accepted Slice 1 contracts and artifacts remain pinned;
- the bounded local browser package is deterministic and replaceable;
- browser routes preserve exact revisions, entry order, decisions, candidates, warnings, and authority;
- keyboard and non-graph multi-step operation pass in the pinned browser;
- local download reproduces the accepted export bytes;
- repeated browser evidence is byte-identical;
- no workspace or browser action can mutate canonical, review, lifecycle, merge, release, Principia, or repository state;
- the workspace operates locally without accounts, cloud services, or external network access;
- a completion report recommends or rejects broader workspace implementation.

## Immediate implementation sequence

1. generate the accepted export and manifest into a replaceable static package;
2. create the smallest semantic HTML, CSS, and JavaScript reader for the required routes;
3. add explicit unknown-route and missing-artifact failures that preserve the prior valid view;
4. add deterministic route, history, keyboard, focus, non-graph, reduced-motion, and mobile tests;
5. intercept and reject all external browser requests;
6. verify local download byte identity with the accepted export;
7. pin shell and browser evidence across repeated runs;
8. keep production architecture, live synchronization, accounts, cloud persistence, canonical writes, and automatic authority frozen.
