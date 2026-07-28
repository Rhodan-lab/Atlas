# Phase 4 Workstream 4 — Bounded Workspace Fixture Generalization

## Status

```yaml
phase: 4
workstream: 4
state: active
active_slice: 1
slice_name: catalase-fixture-selection-and-contract-reuse
fixture_count_authorized: 1
previous_fixture_domain: recommender-systems
candidate_fixture_domain: catalase-assay-methodology
cross_domain_required: true
existing_canonical_revisions_only: true
new_canonical_authoring_authorized: false
accepted_contract_reuse_required: true
browser_implementation_authorized: false
production_implementation_authorized: false
workspace_authority: ephemeral-research-only
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
repository_mutation: false
production_frontend_architecture_selected: false
live_principia_dependency: false
```

## Authorization source

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

This governance record supplies that separate authorization. It permits exactly one non-production fixture evaluation and nothing broader.

## Objective

Test whether the accepted Workstream 3 workspace contracts can represent a materially different subject without contract changes, canonical authoring, hidden fallback, or authority expansion.

The candidate question is:

> Under what assay conditions may catalase activity be compared without treating one reported optimum as universal?

The Catalase domain is selected because the accepted corpus already contains enough exact-revision records for a bounded cross-domain test.

## Candidate exact-revision source pool

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

The source pool is not itself a workspace. Slice 1 must select and justify exactly five ordered workspace entries from these records.

## Required contract reuse

Slice 1 must reuse these accepted contracts unchanged:

```yaml
workspace: atlas-research-workspace/0.1
entry: atlas-research-workspace-entry/0.1
decision: atlas-research-workspace-decision/0.1
export: atlas-research-workspace-export/0.1
manifest: atlas-research-workspace-manifest/0.1
failure: atlas-research-workspace-failure/0.1
```

The candidate may define new fixture identifiers and research-only records, but it may not change accepted contract names, required authority fields, exact-revision semantics, export determinism, or failure behavior.

## Required bounded fixture

The candidate must contain:

- one exact five-entry trail using include, exclude, or context decisions;
- two unresolved advisory candidates, including at least one scope-difference assessment;
- one fixture-only pinned offline Principia envelope with separate Principia status;
- one explicit unavailable-revision warning;
- explicit rationales and open questions;
- a complete non-graph summary;
- deterministic fixture, report, export, and manifest artifacts;
- machine-readable authority and limitation fields.

Every candidate, decision, warning, and Principia reference remains non-authoritative and non-mutating.

## Slice 1 acceptance gates

Slice 1 passes only if:

1. all referenced canonical records exist at exact revision 1;
2. no recommender-system entity is reused as a workspace entry;
3. exactly five ordered entries are selected from the Catalase source pool;
4. accepted workspace contracts validate without modification;
5. two candidates remain unresolved and advisory;
6. Principia status remains fixture-only, separate, and non-live;
7. unavailable revisions fail visibly without substitution;
8. the non-graph summary covers every entry;
9. fixture, report, export, and manifest artifacts are deterministic;
10. Python 3.11 and 3.13 produce byte-identical substantive artifacts;
11. no account, cloud service, credential, or external network is required;
12. no canonical, review, lifecycle, candidate-resolution, release, or repository authority is introduced;
13. one bounded recommendation is issued without implementing it.

## Required negative cases

The validator must reject at least:

- an implicit `latest` reference;
- a non-Catalase workspace entry;
- a duplicate entry or reordered accepted trail;
- an unavailable exact revision;
- a modified accepted contract name;
- copied canonical authority;
- candidate auto-resolution or automatic merge;
- inherited or live Principia status;
- missing non-graph coverage;
- nondeterministic fields;
- account, cloud, credential, or external-network requirements;
- canonical, review, lifecycle, release, or repository mutation;
- browser implementation or production architecture selection.

Every failure preserves the accepted Workstream 3 workspace as the previous valid state.

## Allowed Slice 1 recommendation

Exactly one decision may be issued:

```yaml
allowed_decisions:
  - proceed-static-reader-reuse-evaluation
  - hold-for-contract-review
  - reject-catalase-generalization
```

A proceed decision authorizes only a separate governance proposal for static-reader reuse. It does not authorize browser code, Chromium evidence, deployment, production architecture, accounts, cloud persistence, live synchronization, or canonical editing.

## Immediate implementation sequence

1. define the Catalase fixture and validation bundle;
2. bind the eight candidate exact revisions;
3. create and justify the five-entry trail;
4. create two unresolved advisory candidates;
5. create one pinned offline Principia envelope and one unavailable-revision warning;
6. build deterministic export and manifest artifacts using accepted contracts;
7. add positive and negative tests;
8. run Python 3.11 and 3.13 repeated-build evidence;
9. pin exact artifact identities;
10. produce one bounded Slice 1 recommendation.

## Frozen boundaries

Workstream 4 does not authorize new canonical content, a second active fixture, replacement of the accepted recommender workspace, browser implementation, production claims, deployment, accounts, cloud state, collaboration, live Principia synchronization, automatic candidate resolution, embeddings, vector databases, learned ranking, human-verification claims, or accessibility certification.
