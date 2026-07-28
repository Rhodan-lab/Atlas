# Phase 4 Workstream 3 — Read-Only Research Workspace Composition

## Status

```yaml
phase: 4
workstream: 3
mode: interactive-experience-foundation
state: active
workspace_authority: ephemeral-research-only
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

## Required contracts

The first candidate must define versioned contracts for:

```yaml
workspace_contract: atlas-research-workspace/0.1
workspace_entry_contract: atlas-research-workspace-entry/0.1
workspace_decision_contract: atlas-research-workspace-decision/0.1
workspace_export_contract: atlas-research-workspace-export/0.1
workspace_manifest_contract: atlas-research-workspace-manifest/0.1
workspace_failure_contract: atlas-research-workspace-failure/0.1
```

Contract names remain candidates until executable fixtures, validation, deterministic exports, and CI evidence are accepted.

## Workspace authority

A workspace is an ephemeral research artifact. It may:

- reference exact Atlas entity revisions;
- reference pinned offline Principia envelopes with separate Principia status;
- include accepted retrieval results, filters, research trails, warnings, and advisory candidates;
- record user-authored questions, notes, rationales, and bounded include, exclude, or context decisions;
- produce deterministic read-only exports;
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

## First bounded fixture

The first fixture should compose the accepted research-trail evidence into one exact-revision workspace containing:

- five ordered include, exclude, or context decisions;
- two advisory contradiction or duplicate candidates;
- one pinned offline Principia reference;
- explicit rationales and open questions;
- one deterministic export and manifest;
- machine-readable authority and limitation metadata.

The fixture must remain small enough for complete human inspection and deterministic test coverage. It is not a production corpus or production workspace claim.

## Required failure cases

The first validator must reject at least:

1. an implicit `latest` reference;
2. a duplicate workspace entry identifier;
3. a copied canonical-authority claim;
4. automatic contradiction or duplicate resolution;
5. an unavailable exact revision without an explicit failure record;
6. lifecycle, review, merge, release, or repository mutation;
7. a live or unpinned Principia dependency;
8. a nondeterministic export field such as an uncontrolled timestamp;
9. an external-network or cloud requirement;
10. missing non-graph or text-equivalent workflow information.

## Deterministic export

A workspace export must:

- use a versioned contract;
- preserve stable ordering;
- include exact revision keys and source digests;
- include the workspace authority and limitations;
- include all decision rationales and open questions;
- include the separate status of pinned Principia references;
- include no uncontrolled timestamps, random identifiers, machine-specific paths, credentials, or mutable URLs;
- reproduce byte-identically from the same accepted inputs.

## Browser evidence boundary

A later browser slice may expose the workspace through the accepted local shell, but only after the data and export contracts are accepted. Browser evidence must retain keyboard operation, non-graph equivalence, visible focus, explicit failures, zero external requests, and non-mutating authority.

The workspace implementation must not select a production framework or deployment architecture. A framework decision requires separate architecture evidence and governance approval.

## Exit criteria

Workstream 3 closes only when:

- all workspace contracts are versioned and executable;
- the bounded exact-revision fixture validates;
- all required negative cases are rejected deterministically;
- workspace order, decisions, references, warnings, and candidates remain explicit;
- deterministic exports reproduce byte-identically across supported Python versions;
- no workspace action can mutate canonical, review, lifecycle, merge, release, Principia, or repository state;
- the workspace operates locally without accounts, cloud services, or external network access;
- a browser evidence slice proves keyboard and non-graph multi-step operation, if a browser slice is implemented;
- a completion report recommends or rejects broader workspace implementation.

## Immediate implementation sequence

1. define the workspace, entry, decision, export, manifest, and failure schemas;
2. construct the first bounded exact-revision fixture from accepted research-trail evidence;
3. implement deterministic validation and export;
4. add negative fixtures for every authority and determinism boundary;
5. pin Python 3.11 and 3.13 substantive artifact identities;
6. only then add a bounded browser composition over the accepted local shell;
7. keep production architecture, live synchronization, accounts, cloud persistence, canonical writes, and automatic authority frozen.
