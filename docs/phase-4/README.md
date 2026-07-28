# Phase 4 — Principia & Atlas Interactive Experience

## Status

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 4
workstream_name: bounded-workspace-fixture-generalization
active_slice: 1
slice_name: catalase-fixture-selection-and-contract-reuse
workstream_1: accepted
workstream_2: accepted
workstream_3: accepted
fixture_count_authorized: 1
candidate_fixture_domain: catalase-assay-methodology
new_canonical_authoring_authorized: false
browser_implementation_authorized: false
production_frontend_architecture_selected: false
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

Phase 4 builds bounded interactive evidence over accepted Atlas and Principia semantics without erasing repository ownership, lifecycle status, provenance, revision identity, or authority boundaries.

## Accepted Workstream 1 — interaction contracts and reference shell

```yaml
interaction_pr: 42
reference_shell_pr: 43
completion_pr: 44
completion_contract: atlas-phase4-workstream1-completion-report/0.1
exit_gate_count: 10
state: accepted
```

Accepted capabilities include exact-revision views, deterministic routes, visible authority and provenance, separate Principia status, explicit warnings and failures, keyboard and non-graph requirements, replaceable local artifacts, and negative tests preventing hidden fallback or authority escalation.

## Accepted Workstream 2 — pinned browser evidence

```yaml
browser_pr: 46
completion_pr: 47
completion_contract: atlas-phase4-workstream2-completion-report/0.1
engine: chromium-151.0.7922.34
playwright: 1.62.0
external_request_count: 0
exit_gate_count: 12
human_verified: false
accessibility_certified: false
state: accepted
```

Automated browser evidence is necessary but is not human accessibility certification, assistive-technology user review, or broad usability validation.

## Accepted Workstream 3 — read-only research workspace

Workstream 3 established one deterministic, read-only research workspace over an accepted recommender-system fixture.

```yaml
workspace_contract_pr: 50
workspace_shell_pr: 52
workspace_browser_pr: 54
completion_pr: 56
completion_tested_head: f24777d4f52ca4dd8e9829fc929f3fb2c88d0115
completion_merge_commit: b9e30959e3b9387c5132c804cccf9c1391a9ada6
completion_contract: atlas-phase4-workstream3-completion-report/0.1
completion_validation_contract: atlas-phase4-workstream3-completion-validation/0.1
completion_baseline_contract: atlas-phase4-workstream3-completion-baseline/0.1
completion_report_bytes: 9098
completion_report_sha256: fe4798f27ed31f6a180c9cb7ec5df31ddc77b440585f0d26dd3cd82d26e23353
completion_report_digest: 3f13809d1aba31a15af77ea7afae1062bac5b4a4274ec3794d9f6be389e3ecde
exit_gate_count: 13
recommendation: proceed-bounded-workspace-fixture-evaluation
implementation_authorized_by_report: false
state: accepted
```

Accepted Workstream 3 evidence includes:

- five ordered exact-revision decisions;
- two unresolved advisory candidates;
- one fixture-only, non-live Principia reference with separate status;
- one explicit unavailable-revision warning;
- deterministic export and manifest artifacts;
- a replaceable static reader with thirteen routes;
- keyboard and non-graph operation;
- pinned Chromium evidence at desktop and mobile viewports;
- exact local-download byte identity;
- explicit unknown-route and missing-artifact failures;
- zero external requests;
- disposable browser state;
- migration and rollback boundaries;
- thirteen passing completion gates.

The Workstream 3 completion recommendation required separate governance and could not authorize implementation by itself.

## Active Workstream 4 — bounded cross-domain fixture generalization

Workstream 4 supplies the separate governance authorization for exactly one additional non-production fixture.

```yaml
state: active
active_slice: 1
fixture_count_authorized: 1
previous_fixture_domain: recommender-systems
candidate_fixture_domain: catalase-assay-methodology
cross_domain_required: true
existing_canonical_revisions_only: true
new_canonical_authoring_authorized: false
accepted_contract_reuse_required: true
browser_implementation_authorized: false
production_implementation_authorized: false
```

### Candidate question

> Under what assay conditions may catalase activity be compared without treating one reported optimum as universal?

### Candidate exact-revision source pool

```yaml
- question:en:how-assay-conditions-affect-catalase@1
- concept:en:catalase@1
- model:en:catalase-assay-observation@1
- evidence:en:fluorescent-catalase-assay-neutral-ph@1
- claim:en:catalase-optimum-requires-assay-scope@1
- synthesis:en:catalase-assay-conditions@1
- src:aebi-1984-catalase-in-vitro@1
- src:wu-lin-wolfbeis-2003-catalase-assay@1
```

The candidate must reuse the accepted Workstream 3 workspace, entry, decision, export, manifest, and failure contracts unchanged. It must select exactly five ordered entries, preserve two unresolved advisory candidates, carry one fixture-only Principia envelope and one explicit warning, provide complete non-graph coverage, and produce deterministic artifacts on Python 3.11 and 3.13.

If the contracts do not generalize unchanged, the candidate must fail visibly and preserve Workstream 3 as the accepted state. Contract modification, browser reuse, and production implementation each require separate governance.

See [`workstream-4.md`](workstream-4.md).

## Phase 4 boundaries

### Allowed

- exact-revision Atlas views and pinned offline Principia references;
- deterministic local fixtures, exports, manifests, reports, shells, and browser evidence;
- keyboard, focus, semantic, deep-link, history, warning, failure, responsive, export, and network-isolation tests;
- fixture-only research questions, rationales, and include, exclude, or context decisions;
- accessibility fixes required by evidence when semantic and authority contracts remain unchanged;
- exactly one Catalase contract-reuse evaluation under Workstream 4 Slice 1.

### Still frozen

- new canonical authoring for the Workstream 4 fixture;
- a second additional fixture;
- browser implementation before Slice 1 acceptance;
- production retrieval-quality claims;
- vector databases, embeddings, or learned ranking;
- implicit `latest` references;
- live Principia synchronization;
- canonical writes from browser, workspace, retrieval, trail, or candidate state;
- automatic candidate resolution, review, lifecycle, promotion, merge, or release mutation;
- accounts, permissions, cloud sync, plugins, or autonomous agents changing knowledge state;
- automatic conversion of AI review into human verification;
- accessibility certification without qualified human evidence;
- production frontend, hosting, deployment, or business-model selection.

## Immediate next actions

1. define the Catalase fixture-selection and contract-reuse evidence bundle;
2. validate the eight candidate exact revisions;
3. create one five-entry trail and two unresolved advisory candidates;
4. create one pinned offline Principia envelope and one unavailable-revision warning;
5. generate deterministic fixture, report, export, and manifest candidates;
6. run positive and negative tests on Python 3.11 and 3.13;
7. pin exact identities and issue one bounded recommendation;
8. keep browser implementation and every production boundary frozen.
