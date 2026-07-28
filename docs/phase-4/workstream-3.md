# Phase 4 Workstream 3 — Read-Only Research Workspace Composition

## Status

```yaml
phase: 4
workstream: 3
state: active-governance-boundary
workspace_authority: ephemeral-research-only
exact_revision_required: true
deterministic_export_required: true
canonical_copy_authority: false
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
automatic_merge_or_resolution: false
production_frontend_architecture_selected: false
live_principia_dependency: false
repository_mutation: false
```

## Purpose

Workstream 3 composes the accepted retrieval, filter, research-trail, candidate, Atlas-view, Principia-reference, warning, failure, and browser foundations into one complete read-only research workflow.

The workspace is a temporary analytical arrangement of exact references and researcher decisions. It is not a canonical knowledge record, review record, lifecycle event, merge instruction, or release action.

## Authorized workflow

The first bounded workflow may:

1. start from a pinned structured-field retrieval result or exact Atlas revision;
2. apply accepted deterministic filters;
3. inspect provenance, review level, lifecycle, and staleness;
4. create an ordered workspace entry for an exact revision;
5. assign one decision: `include`, `exclude`, or `context`;
6. record an ordered rationale and open questions;
7. attach advisory contradiction or duplicate candidates without resolving them;
8. attach a pinned offline Principia reference while preserving separate status;
9. expose stale, unavailable-revision, mismatch, duplicate-entry, and impact warnings;
10. export a deterministic research package and manifest.

## Candidate contracts

The first implementation should propose and test the following families:

```yaml
workspace_contract: atlas-research-workspace/0.1
workspace_entry_contract: atlas-research-workspace-entry/0.1
workspace_decision_contract: atlas-research-workspace-decision/0.1
workspace_export_contract: atlas-research-workspace-export/0.1
workspace_manifest_contract: atlas-research-workspace-manifest/0.1
workspace_failure_contract: atlas-research-workspace-failure/0.1
```

These names are candidates, not accepted contracts, until executable fixtures, negative tests, deterministic exports, and exact-head CI evidence pass.

## Required workspace identity

A workspace must expose:

- a stable workspace ID and explicit revision;
- mode and schema contract;
- source corpus digest;
- exact upstream fixture and report identities;
- ordered entry IDs;
- ordered rationale and open-question IDs;
- an explicit authority block;
- a deterministic workspace digest.

Timestamps, random identifiers, environment-dependent paths, and implicit current-state lookups are not permitted in substantive evidence.

## Required entry semantics

Each entry must contain:

- a stable entry ID;
- an exact Atlas entity ID and revision;
- a decision of `include`, `exclude`, or `context`;
- an explicit position;
- a rationale reference;
- visible provenance, review level, lifecycle, and staleness metadata;
- pinned retrieval, filter, or trail evidence identities where applicable;
- advisory candidate references where applicable;
- an authority block stating that the entry cannot mutate canonical state.

Entries must be unique by exact entity revision. Duplicate exact entries must fail explicitly rather than merge silently.

## Principia reference boundary

A Principia attachment must:

- use a pinned offline fixture or exact external revision identity;
- expose Principia status separately from Atlas status;
- state that no live dependency is active;
- reject implicit `latest`;
- refuse to infer publication readiness, review state, or lifecycle state across repositories;
- remain optional to the Atlas workspace export.

## Candidate and warning boundary

Contradiction, duplicate, and impact records remain advisory.

The workspace may record:

- the candidate identity;
- exact compared revisions;
- evidence and explanation references;
- confidence or score already present in accepted upstream evidence;
- the researcher’s `include`, `exclude`, or `context` decision;
- an unresolved status.

It may not automatically resolve a contradiction, merge a duplicate, change an entity, promote a review level, alter lifecycle status, or create a repository event.

## Deterministic export

The export package must contain references and decisions, not copied canonical authority.

Required export contents:

- workspace identity and revision;
- source and upstream evidence digests;
- ordered exact-revision entries;
- ordered decisions and rationales;
- open questions;
- advisory candidate references;
- optional pinned Principia reference envelopes;
- warnings and limitations;
- explicit authority and non-mutation statements;
- child-file SHA-256 values;
- a parent manifest digest.

The export must be generated twice in the same run and compared byte-for-byte. Python 3.11 and 3.13 substantive artifacts must also be byte-identical before acceptance.

## Required negative cases

The first implementation must reject at least:

```text
E-WORKSPACE-CONTRACT
E-WORKSPACE-REVISION
E-WORKSPACE-LATEST
E-WORKSPACE-DUPLICATE-ENTRY
E-WORKSPACE-UNAVAILABLE-REVISION
E-WORKSPACE-COPIED-AUTHORITY
E-WORKSPACE-DECISION
E-WORKSPACE-CANDIDATE-AUTHORITY
E-WORKSPACE-PRINCIPIA-STATUS
E-WORKSPACE-LIFECYCLE-MUTATION
E-WORKSPACE-DIGEST
E-WORKSPACE-MANIFEST
```

A failed operation must preserve the previous valid workspace and must not silently substitute, remove, reorder, merge, or mutate entries.

## Initial fixture target

The first deterministic fixture should include:

- five exact Atlas revisions with a mixture of include, exclude, and context decisions;
- one accepted structured retrieval identity;
- one deterministic filter identity;
- one accepted research-trail identity;
- two advisory candidate references, such as one contradiction and one duplicate candidate;
- one pinned offline Principia reference;
- ordered rationales and open questions;
- explicit warnings for unavailable revision and cross-repository impact;
- a deterministic export and manifest.

The fixture should reuse accepted upstream records instead of inventing new production claims.

## Browser scope

Browser work is not required for the first contract slice. When browser composition is added, it must:

- remain local-first;
- restore only ephemeral workspace state;
- expose a complete keyboard and non-graph path;
- preserve exact revisions and entry order;
- make save/export authority explicit;
- perform no canonical, review, lifecycle, merge, release, or repository write;
- preserve zero-external-request behavior unless a separately approved boundary changes.

## Acceptance gates

Workstream 3 cannot close until evidence proves:

1. versioned workspace contracts are executable;
2. all entries use exact revisions;
3. entry order and uniqueness are deterministic;
4. decisions remain advisory and non-mutating;
5. provenance, review, lifecycle, and staleness remain visible;
6. Principia status remains separate;
7. candidates remain unresolved and advisory;
8. unavailable and malformed references fail explicitly;
9. copied canonical authority is rejected;
10. deterministic export and manifest digests are valid;
11. repeated and cross-Python substantive artifacts are byte-identical;
12. generated artifacts are replaceable;
13. no account, cloud service, external network, live dependency, or production architecture is required;
14. a completion report recommends or rejects broader workspace implementation.

## Still frozen

- canonical, review, lifecycle, merge, or release writes;
- automatic contradiction resolution or duplicate merge;
- copied canonical body text becoming workspace authority;
- implicit `latest` references;
- live Principia synchronization;
- production retrieval-quality claims;
- vector databases, embeddings, learned ranking, or external semantic services;
- accounts, cloud synchronization, analytics, plugins, collaboration, and autonomous agents;
- production frontend, hosting, or deployment architecture selection;
- accessibility certification or human usability claims;
- screenshots as authority.
