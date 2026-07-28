# Phase 4 Workstream 2 — Browser Accessibility and Workflow Evidence

## Status

Active governance scope after accepted Workstream 1 closure.

```yaml
phase: 4
workstream: 2
mode: interactive-experience-foundation
state: active
purpose: collect-real-browser-evidence
production_frontend_architecture_selected: false
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Decision question

Does the accepted static reference shell expose the required Atlas and Principia workflows in a real browser with deterministic keyboard operation, visible focus, semantic structure, exact-revision navigation, explicit failures, complete non-graph routes, offline operation, and zero external network dependency?

Workstream 2 must answer this with executable evidence. It may identify defects and authorize bounded accessibility fixes, but it may not infer product maturity from a passing static shell.

## Source authority

The browser harness consumes only:

- accepted canonical Atlas Markdown through deterministic generated shell data;
- accepted Phase 4 interaction fixtures;
- accepted Workstream 1 completion evidence;
- static files under `apps/reference-shell/`;
- a loopback HTTP origin created by the test harness.

Browser observations are generated evidence. They do not become canonical knowledge, review records, lifecycle history, or Principia publication status.

## Candidate contracts

### Browser evidence manifest

`atlas-phase4-browser-evidence-manifest/0.1` should bind:

```yaml
engine_name: required
engine_version: required
engine_source: required
operating_system: required
viewport_matrix: required
shell_baseline_sha256: required
shell_build_digest: required
interaction_report_digest: required
workstream1_completion_digest: required
workflow_fixture_revision: required
network_policy_revision: required
accessibility_policy_revision: required
external_network_allowed: false
live: false
repository_mutation: false
```

### Workflow evidence

`atlas-browser-workflow-evidence/0.1` should record, for each workflow:

```yaml
workflow_id: required
workflow_revision: required
start_route: required
input_sequence: required
focus_sequence: required
expected_route_sequence: required
observed_route_sequence: required
expected_view_kind: required
observed_view_kind: required
exact_entity_references: required
non_graph_route_exercised: required
warnings_observed: required
failure_state_observed: optional
decision: pass-or-fail
```

Input and focus sequences must be semantic records, not timing-sensitive event dumps.

### Accessibility report

`atlas-browser-accessibility-report/0.1` should record:

- document language and title;
- landmark counts and accessible names;
- heading order;
- labeled interactive controls;
- skip-link target and operation;
- keyboard-reachable controls;
- focus sequence and visible focus checks;
- live-region and status-message checks;
- error-summary visibility;
- reduced-motion evaluation;
- desktop and mobile viewport results;
- deterministic rule identifiers for any violations;
- limitations of automated testing;
- `human_verified: false`.

### Network report

`atlas-browser-network-report/0.1` should record:

```yaml
loopback_origin: required
request_count: required
loopback_request_count: required
external_request_count: 0
blocked_external_request_count: required
request_records: deterministic-sorted
credentials_used: false
remote_assets_used: false
analytics_used: false
cloud_service_used: false
```

### Failure evidence

`atlas-browser-failure-evidence/0.1` should prove browser-visible outcomes for:

- malformed generated data;
- missing generated data;
- unknown route or view;
- unavailable exact Atlas revision;
- stale or mismatched Principia reference;
- explicit offline state;
- attempted non-loopback request;
- attempted implicit `latest` route;
- attempted authority mutation.

A failure record must preserve the previous valid state where declared, expose a readable error or warning, forbid silent fallback, and remain non-mutating.

## Pinned test instrument

The first implementation may use a single pinned Chromium engine in CI.

The engine is a measurement instrument, not an architecture decision. The manifest must record the exact browser version and installation source. A second engine should be added only if it tests a specific compatibility risk or changes a decision.

## Required workflow matrix

### 1. Shell entry and skip navigation

- load the local shell;
- confirm the document title and language;
- use keyboard input to reveal and activate the skip link;
- verify focus arrives at the main content target;
- confirm no mouse or pointer input is necessary.

### 2. Workflow navigation

- traverse the named workflow selector by keyboard;
- open each of the eight accepted workflow kinds;
- verify visible focus before activation;
- verify the selected workflow and detail view are programmatically identifiable.

### 3. Exact-revision deep links

- open a pinned route directly;
- verify the route contains an exact ID and positive revision;
- reload and confirm the same view;
- reject any route containing implicit `latest`;
- verify unavailable revisions show explicit warning or failure evidence.

### 4. Browser history

- navigate between at least three distinct workflow routes;
- use browser back and forward actions;
- compare observed route and view sequences against the pinned expectation;
- ensure history does not silently substitute another revision.

### 5. Authority inspection

For every workflow kind, verify visible or programmatically available:

- exact Atlas ID and revision;
- lifecycle status;
- review level;
- staleness;
- provenance or source identity where applicable;
- advisory retrieval or candidate authority;
- separate Principia status where applicable.

### 6. Non-graph equivalence

- complete every relation, dependency, provenance, candidate, and impact workflow through list or text navigation;
- verify graph visualization is absent or optional;
- fail the evidence gate if essential information is available only through geometry, hover, or visual position.

### 7. Warnings and failures

- open the impact-warning workflow;
- exercise all accepted failure categories;
- verify readable category, code, summary, and recovery information where present;
- verify warnings and errors are not distinguished only by color;
- verify no failure mutates canonical or lifecycle state.

### 8. Offline and network isolation

- generate the shell package deterministically;
- serve it on loopback;
- intercept every request;
- allow only loopback requests required by the static package;
- fail on any external request attempt;
- verify the core workflow matrix remains operable without external connectivity.

### 9. Responsive bounded viewports

The first evidence matrix should include one desktop viewport and one narrow mobile viewport. The report must record:

- viewport dimensions;
- horizontal overflow checks;
- reachable controls;
- readable detail content;
- focus visibility;
- preservation of semantic order.

This is bounded evidence, not full device certification.

## Determinism policy

Authoritative evidence must exclude:

- timestamps that vary between equivalent runs;
- animation frame counts;
- raw performance timings unless a threshold decision requires them;
- screenshots as semantic proof;
- unordered network or DOM records;
- browser-generated opaque IDs;
- absolute temporary filesystem paths.

Records should use stable workflow IDs, semantic focus locators, normalized routes, sorted request entries, pinned browser identity, and canonical JSON rendering.

Repeated runs in the same pinned environment must produce byte-identical substantive JSON evidence. Logs and diagnostic screenshots may differ and are non-authoritative.

## Accessibility evidence limitations

Automated browser checks can establish machine-testable properties. They cannot prove that every user with a disability can use the interface, certify conformance, or replace human assistive-technology review.

Every report must state:

```yaml
human_verified: false
accessibility_certified: false
assistive_technology_user_reviewed: false
```

## Allowed corrections

Evidence may authorize narrowly scoped changes to:

- missing labels or accessible names;
- invalid heading or landmark structure;
- broken skip navigation;
- invisible or obscured focus;
- keyboard traps or unreachable controls;
- missing live status or error summaries;
- color-only warnings;
- overflow that blocks bounded mobile workflows;
- nondeterministic history or route behavior;
- unexpected external requests.

Corrections must not alter canonical knowledge, accepted interaction semantics, retrieval judgments, Principia status, or lifecycle authority.

## Non-goals

Workstream 2 does not:

- design a polished product interface;
- choose React, Next.js, another framework, hosting, or deployment architecture;
- add accounts, personalization, analytics, collaboration, plugins, or cloud synchronization;
- activate live Principia integration;
- grant browser state write authority;
- claim production search quality;
- add semantic retrieval infrastructure;
- certify WCAG conformance or human accessibility verification;
- treat screenshots or browser output as canonical knowledge.

## Acceptance gates

Workstream 2 may close only when:

1. the browser manifest and evidence contracts are versioned;
2. the pinned engine and environment are recorded;
3. all required workflows pass by keyboard;
4. focus, landmarks, headings, labels, announcements, and errors are recorded;
5. deep links, reload, back, and forward behavior are deterministic;
6. every workflow has a non-graph equivalent;
7. warnings and failure states remain explicit and non-mutating;
8. external request count is zero;
9. desktop and mobile bounded viewports pass;
10. substantive evidence is byte-identical across repeated runs;
11. limitations and non-human review status are explicit;
12. a completion report recommends or rejects broader interface implementation.

## Immediate implementation sequence

1. create a pinned browser-test package and lockfile;
2. define stable workflow fixtures independent of browser timing;
3. build the accepted static package in CI;
4. start an isolated loopback server;
5. run the browser workflow and accessibility matrix;
6. normalize evidence into deterministic JSON contracts;
7. add negative tests for external requests, implicit `latest`, and authority mutation;
8. pin the first evidence only after repeated-run equivalence;
9. keep the PR draft until the exact final head passes the complete Atlas regression matrix.
