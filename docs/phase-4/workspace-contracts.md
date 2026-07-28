# Phase 4 Workstream 3 — First Workspace Contract Candidate

## Status

```yaml
phase: 4
workstream: 3
state: workspace-contract-candidate
workspace_authority: ephemeral-research-only
entries: 5
candidates: 2
principia_references: 1
warnings: 1
negative_cases: 10
deterministic_export_required: true
browser_slice_included: false
production_frontend_architecture_selected: false
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Candidate contracts

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

These contracts remain candidates until accepted through an immutable-head merge.

## Pinned evidence

Python 3.11 and Python 3.13 produced byte-identical substantive artifacts.

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

The workflow regenerates every artifact twice per Python version, compares the complete directories byte-for-byte, then enforces the pinned baseline record.

## Composition source

The candidate composes only accepted evidence:

- Phase 3 structured-field retrieval baseline;
- Phase 3 recommender research trail with five exact-revision decisions;
- one accepted contradiction candidate assessed as likely scope difference;
- one accepted duplicate candidate assessed as related but not duplicate;
- one Phase 4 fixture-only Principia reference with separate draft status;
- one explicit unavailable-revision impact warning.

It does not rerank the corpus, invent a new candidate, copy canonical body text, or infer cross-repository status.

## Bounded workspace

```yaml
workspace_id: workspace:en:recommender-cross-platform-effect-review
workspace_revision: 1
query_id: query:retrieval:recommender-cross-platform-generalization
filter_id: filter:en:recommender-claims-and-synthesis
filter_revision: 1
trail_id: trail:en:recommender-cross-platform-generalization
trail_revision: 1
```

The ordered decisions are:

1. include the context-dependent scope claim;
2. include the recommender exposure and governance synthesis;
3. contextualize the Twitter randomized comparison;
4. exclude the explanation-and-choice policy claim from the narrower effect-size question;
5. contextualize the Facebook observational exposure pathway.

The export derives visible title, type, lifecycle, review, staleness, and provenance metadata from the exact canonical revisions. It does not export canonical body fields.

## Advisory candidates

The workspace references:

```yaml
contradiction:
  id: candidate:contradiction:facebook-twitter-exposure-effects
  assessment: scope-difference-likely
  resolution: unresolved
duplicate:
  id: candidate:duplicate:recommender-context-claim-and-synthesis
  assessment: related-not-duplicate
  resolution: unresolved
```

Both remain advisory. The workspace cannot resolve, merge, redirect, supersede, deprecate, promote, or alter either side.

## Principia boundary

The fixture-only envelope `principia-reference:feedback:period-six@1` is included solely to prove that a workspace can carry a pinned offline cross-repository reference while keeping Principia status separate.

```yaml
principia_status: draft
principia_status_separate: true
fixture_only: true
implicit_latest: false
live: false
automatic_status_inheritance: false
```

The Principia reference does not inherit Atlas lifecycle state, and Atlas does not inherit Principia readiness.

## Deterministic artifacts

Each run produces:

- `workspace-export.json` — exact references, research decisions, visible metadata, advisory candidates, warnings, limitations, and authority boundaries;
- `workspace-manifest.json` — byte count, SHA-256, semantic digest, replaceability, and non-mutation boundaries;
- `workspace-report.json` — validation counts, negative-case outcomes, upstream and child digests, and candidate status.

The export contains references and visible metadata rather than copied canonical body authority. Generated artifacts are replaceable and require no account, cloud service, external request, or live dependency.

## Required rejection cases

The candidate rejects:

```text
E-WORKSPACE-LATEST
E-WORKSPACE-DUPLICATE-ENTRY
E-WORKSPACE-COPIED-AUTHORITY
E-WORKSPACE-CANDIDATE-AUTHORITY
E-WORKSPACE-UNAVAILABLE-REVISION
E-WORKSPACE-LIFECYCLE-MUTATION
E-WORKSPACE-PRINCIPIA-STATUS
E-WORKSPACE-DETERMINISM
E-WORKSPACE-NETWORK
E-WORKSPACE-NON-GRAPH
```

Every negative case records that the previous valid workspace remains preserved. No failure may silently substitute `latest`, reorder entries, merge records, inherit status, or write repository state.

## Authority boundary

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

## Non-goals

This candidate does not add a browser workspace, product UI, account, cloud persistence, collaboration, live Principia synchronization, canonical editing, production architecture, semantic infrastructure, accessibility certification, or a production retrieval-quality claim.
