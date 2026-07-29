# Phase 4 — Principia & Atlas Interactive Experience

## Status

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
active_fixture_domain: catalase-assay-methodology
new_canonical_authoring_authorized: false
existing_static_reader_reuse_authorized: true
browser_implementation_scope: existing-static-reader-reuse-only
new_frontend_architecture_authorized: false
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

## Workstream 4 — bounded cross-domain fixture generalization

Workstream 4 supplies separate governance for exactly one additional non-production fixture in a materially different domain.

### Accepted Slice 1 — Catalase fixture selection and contract reuse

```yaml
state: accepted
accepted_pr: 58
accepted_candidate_head: 4b25e0ac7e5b31f05629b19cef6388ca823ad9fa
accepted_merge_commit: a7e04f377389cb003aec8faadcd3eccdfd78ba2b
evidence_baseline_contract: atlas-phase4-workspace-generalization-baseline/0.1
fixture_id: generalization-fixture:phase4-catalase-en-v1
fixture_domain: catalase-assay-methodology
canonical_source_pool: 8
workspace_entries: 5
unresolved_candidates: 2
total_negative_cases: 24
acceptance_gates: 13
python_3_11_and_3_13_byte_identical: true
recommendation: proceed-static-reader-reuse-evaluation
```

Slice 1 reused the accepted Workstream 3 workspace, entry, decision, export, manifest, and failure contracts unchanged. It preserved two unresolved advisory candidates, one fixture-only non-live Principia envelope with separate status, one unavailable-revision warning, complete non-graph coverage, and deterministic artifacts.

Pinned identities are stored in [`catalase-generalization-baseline.json`](../../content/fixtures/phase4_workspace_generalization/catalase-generalization-baseline.json). The governance decision is recorded in [`workstream-4-slice-1-governance.md`](workstream-4-slice-1-governance.md).

### Active Slice 2 — Catalase static reader reuse evaluation

```yaml
state: active
fixture_count_authorized: 1
fixture_id: generalization-fixture:phase4-catalase-en-v1
accepted_slice_1_baseline_required: true
existing_static_reader_reuse_authorized: true
new_static_reader_authorized: false
new_frontend_architecture_authorized: false
browser_evidence_authorized: true
production_implementation_authorized: false
```

Slice 2 may reuse only the existing accepted static reader. It must preserve the recommender-system workspace, accepted contracts, exact revisions, visible warnings and failures, keyboard and non-graph behavior, disposable state, exact local-download identity, and zero-network boundary.

Required Slice 2 evidence:

1. generate the accepted Catalase fixture and export from the pinned Slice 1 baseline;
2. package the Catalase artifacts through the existing reader contract;
3. prove no regression to the accepted recommender-system reader;
4. render all five entries, two unresolved candidates, Principia status, warning, open questions, and non-graph summary;
5. test routes, deep links, history, keyboard, focus, responsive behavior, downloads, and explicit failures;
6. run pinned Chromium evidence twice and prove zero external requests;
7. reject implicit latest, hidden fallback, accounts, cloud, credentials, mutation, and authority escalation;
8. issue one bounded recommendation without authorizing production.

Allowed Slice 2 decisions:

```yaml
allowed_decisions:
  - proceed-workstream4-closure-evaluation
  - hold-static-reader-reuse
  - reject-static-reader-reuse
```

See [`workstream-4.md`](workstream-4.md).

## Phase 4 boundaries

### Allowed

- exact-revision Atlas views and pinned offline Principia references;
- deterministic local fixtures, exports, manifests, reports, shells, and browser evidence;
- keyboard, focus, semantic, deep-link, history, warning, failure, responsive, export, and network-isolation tests;
- fixture-only research questions, rationales, and include, exclude, or context decisions;
- accessibility fixes required by evidence when semantic and authority contracts remain unchanged;
- exactly one accepted Catalase generalization fixture;
- reuse evaluation of the existing static reader under Workstream 4 Slice 2.

### Still frozen

- new canonical authoring for the Workstream 4 fixture;
- a second additional fixture;
- replacement or mutation of the accepted recommender workspace;
- a new static reader or frontend architecture;
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

1. add deterministic Catalase package selection to the existing static-reader build path;
2. preserve the accepted recommender package and prove regression safety;
3. add Catalase routes without changing accepted workspace contracts;
4. validate all visible entries, candidates, Principia status, warning, open questions, and non-graph content;
5. prove exact local-download bytes and explicit failure states;
6. generate repeated pinned Chromium evidence with zero external requests;
7. pin Slice 2 identities and issue one bounded recommendation;
8. keep every production and authority boundary frozen.
