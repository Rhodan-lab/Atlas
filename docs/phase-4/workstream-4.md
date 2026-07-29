# Phase 4 Workstream 4 — Bounded Workspace Fixture Generalization

## Status

```yaml
phase: 4
workstream: 4
state: active
active_slice: 2
slice_name: catalase-static-reader-reuse-evaluation
fixture_count_authorized: 1
previous_fixture_domain: recommender-systems
active_fixture_domain: catalase-assay-methodology
cross_domain_required: true
existing_canonical_revisions_only: true
new_canonical_authoring_authorized: false
accepted_contract_reuse_required: true
workstream_4_slice_1: accepted
existing_static_reader_reuse_authorized: true
browser_implementation_scope: existing-static-reader-reuse-only
browser_evidence_authorized: true
new_frontend_architecture_authorized: false
production_implementation_authorized: false
workspace_authority: ephemeral-research-only
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
repository_mutation: false
production_frontend_architecture_selected: false
live_principia_dependency: false
```

## Authorization chain

Workstream 3 closed through PR #56 with thirteen passing gates and the bounded recommendation `proceed-bounded-workspace-fixture-evaluation`.

```yaml
accepted_workstream_3_pr: 56
accepted_workstream_3_tested_head: f24777d4f52ca4dd8e9829fc929f3fb2c88d0115
accepted_workstream_3_merge_commit: b9e30959e3b9387c5132c804cccf9c1391a9ada6
completion_contract: atlas-phase4-workstream3-completion-report/0.1
completion_baseline_contract: atlas-phase4-workstream3-completion-baseline/0.1
completion_report_sha256: fe4798f27ed31f6a180c9cb7ec5df31ddc77b440585f0d26dd3cd82d26e23353
completion_report_digest: 3f13809d1aba31a15af77ea7afae1062bac5b4a4274ec3794d9f6be389e3ecde
recommendation: proceed-bounded-workspace-fixture-evaluation
implementation_authorized_by_report: false
separate_governance_required: true
```

The original Workstream 4 governance record authorized exactly one non-production Catalase fixture evaluation and nothing broader.

## Accepted Slice 1 — Catalase fixture selection and contract reuse

### Objective

Test whether the accepted Workstream 3 workspace contracts can represent a materially different subject without contract changes, canonical authoring, hidden fallback, or authority expansion.

The evaluated question was:

> Under what assay conditions may catalase activity be compared without treating one reported optimum as universal?

### Accepted exact-revision source pool

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

### Reused contracts

Slice 1 reused these accepted contracts unchanged:

```yaml
workspace: atlas-research-workspace/0.1
entry: atlas-research-workspace-entry/0.1
decision: atlas-research-workspace-decision/0.1
export: atlas-research-workspace-export/0.1
manifest: atlas-research-workspace-manifest/0.1
failure: atlas-research-workspace-failure/0.1
```

No accepted contract name, authority field, exact-revision semantic, export rule, or failure behavior was changed.

### Accepted bounded fixture

The accepted fixture contains:

- one exact five-entry trail using include, exclude, and context decisions;
- two unresolved advisory candidates, including a scope-difference assessment;
- one fixture-only pinned offline Principia envelope with separate status;
- one explicit unavailable-revision warning;
- explicit rationales and open questions;
- a complete non-graph summary;
- deterministic fixture, report, export, and manifest artifacts;
- machine-readable authority and limitation fields.

Every candidate, decision, warning, and Principia reference remains non-authoritative and non-mutating.

### Acceptance result

```yaml
state: accepted
accepted_pr: 58
accepted_candidate_head: 4b25e0ac7e5b31f05629b19cef6388ca823ad9fa
accepted_merge_commit: a7e04f377389cb003aec8faadcd3eccdfd78ba2b
evidence_baseline_contract: atlas-phase4-workspace-generalization-baseline/0.1
fixture_id: generalization-fixture:phase4-catalase-en-v1
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

All thirteen Slice 1 gates passed:

1. every canonical record resolved at the exact accepted revision;
2. no recommender-system entity became a Catalase workspace entry;
3. exactly five ordered Catalase entries were selected;
4. accepted workspace contracts validated unchanged;
5. both candidates remained unresolved and advisory;
6. Principia status remained fixture-only, separate, and non-live;
7. the unavailable revision failed visibly without substitution;
8. the non-graph summary covered every entry;
9. fixture, report, export, and manifest artifacts were deterministic;
10. Python 3.11 and 3.13 produced byte-identical substantive artifacts;
11. no account, cloud service, credential, or external network was required;
12. no canonical, review, lifecycle, candidate-resolution, release, or repository authority was introduced;
13. one bounded recommendation was issued without implementing it.

The validator rejected implicit latest, domain leakage, duplicate or reordered entries, unavailable revisions, contract drift, copied authority, candidate auto-resolution, live or inherited Principia status, missing non-graph coverage, nondeterminism, account or cloud requirements, credentials, external network access, mutation, a second fixture, browser implementation, and production architecture selection.

Pinned identities are stored in `content/fixtures/phase4_workspace_generalization/catalase-generalization-baseline.json`. The acceptance decision and Slice 2 scope are recorded in `docs/phase-4/workstream-4-slice-1-governance.md`.

## Active Slice 2 — Catalase static reader reuse evaluation

### Objective

Evaluate whether the existing accepted Workstream 3 static reader can render the accepted Catalase fixture without changing Atlas semantics, the accepted workspace contracts, or the reader’s authority model.

Slice 2 is a reuse evaluation, not a redesign. It may add only the minimum deterministic fixture-selection and packaging logic required to pass the accepted Catalase artifacts through the existing reader.

### Authorized implementation scope

Slice 2 may:

- generate the accepted Catalase fixture and export from the pinned Slice 1 baseline;
- reuse the existing static-reader route, view, export, warning, failure, and non-graph conventions;
- add local fixture-selection plumbing that is deterministic, replaceable, and read-only;
- preserve the existing recommender-system package as the regression baseline;
- run keyboard, focus, semantic, responsive, history, deep-link, download-identity, warning, failure, and zero-network evidence;
- run pinned Chromium automation twice at accepted desktop and mobile viewports;
- emit deterministic package, report, manifest, browser evidence, and validation artifacts.

Slice 2 may not:

- create a new reader or frontend architecture;
- alter any accepted workspace contract;
- add or edit canonical Atlas content;
- replace or mutate the accepted recommender-system workspace;
- add a second generalized fixture;
- resolve candidates automatically;
- add accounts, permissions, cloud state, collaboration, plugins, credentials, or external network dependencies;
- introduce live Principia synchronization or inherited cross-repository status;
- mutate review, lifecycle, promotion, merge, release, or repository state;
- claim production readiness, broad retrieval quality, universal contract generality, human verification, or accessibility certification.

### Required Slice 2 package

The reused reader must expose, at minimum:

1. a deterministic index or selector that distinguishes the accepted recommender package from the Catalase package without changing either fixture;
2. the five ordered Catalase entries with exact revisions, decisions, rationales, original ranks, and visible metadata;
3. both unresolved advisory candidates with their assessments and non-authoritative status;
4. the pinned non-live Principia reference and separate draft status;
5. the unavailable-revision warning with no fallback or implicit latest;
6. both open questions and the complete five-item non-graph summary;
7. the existing authority and limitation disclosures;
8. a local export whose downloaded bytes exactly match the generated Catalase export artifact;
9. explicit unknown-fixture, unknown-route, missing-artifact, and tampered-artifact failures;
10. a rollback path that restores the unchanged accepted Workstream 3 reader package.

### Slice 2 acceptance gates

Slice 2 passes only if:

1. the pinned Slice 1 baseline verifies before reader packaging;
2. the existing recommender reader package remains byte-identical or semantically identical under its accepted baseline;
3. the Catalase package is deterministic across repeated builds;
4. the same accepted reader contracts render both fixtures without semantic branching that changes authority;
5. all Catalase entries, candidates, warnings, Principia status, questions, and non-graph content are visible and correct;
6. exact routes, deep links, history, keyboard, focus, responsive layout, and explicit failures pass;
7. the downloaded Catalase export is byte-identical to the generated export;
8. browser state remains disposable and non-authoritative;
9. pinned Chromium evidence is repeatable at desktop and mobile viewports;
10. all substantive package and evidence artifacts are byte-identical across repeated runs;
11. external request count remains zero;
12. negative tests reject fallback, implicit latest, hidden resolution, credentials, network access, mutation, and authority escalation;
13. one bounded recommendation is issued without closing Workstream 4 or authorizing production.

### Required negative cases

The Slice 2 evaluator must reject at least:

- an unknown fixture selector that silently falls back to the recommender package;
- an unknown route that silently redirects to a valid entry;
- a missing or tampered Catalase fixture, export, report, or baseline;
- any revision substitution or implicit latest;
- any candidate resolution or status inheritance;
- any mismatch between visible download and generated export bytes;
- any external request, credential, account, cloud, or live synchronization requirement;
- any canonical, review, lifecycle, release, or repository mutation;
- any attempt to activate a second generalized fixture;
- any new production reader or frontend architecture.

Every failure must preserve the accepted Workstream 3 reader and accepted Slice 1 evidence as the previous valid states.

### Allowed Slice 2 recommendation

Exactly one decision may be issued:

```yaml
allowed_decisions:
  - proceed-workstream4-closure-evaluation
  - hold-static-reader-reuse
  - reject-static-reader-reuse
```

A proceed decision authorizes only a separate Workstream 4 closure proposal. It does not close the workstream or authorize deployment, production architecture, accounts, cloud persistence, live synchronization, canonical editing, or broader fixture generalization.

### Immediate implementation sequence

1. inspect the accepted Workstream 3 static-reader package and identify the minimum reusable seams;
2. generate and verify the pinned Catalase fixture, report, export, and manifest;
3. add deterministic fixture selection without altering accepted contracts;
4. package the Catalase artifacts through the existing reader;
5. preserve and regression-test the accepted recommender package;
6. add positive and negative reader tests;
7. generate repeated local browser evidence at accepted desktop and mobile viewports;
8. prove exact download identity, disposable state, and zero external requests;
9. pin Slice 2 artifact identities;
10. issue one bounded recommendation without implementing closure.

## Frozen boundaries

Workstream 4 does not authorize new canonical content, a second generalized fixture, replacement of the accepted recommender workspace, a new reader or frontend architecture, production claims, deployment, accounts, cloud state, collaboration, live Principia synchronization, automatic candidate resolution, embeddings, vector databases, learned ranking, human-verification claims, or accessibility certification.
