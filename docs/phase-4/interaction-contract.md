# Phase 4 Workstream 1 — Interaction Contract Candidate

## Status

Candidate evidence for the interaction semantics that must exist before a runnable reference shell.

```yaml
phase: 4
workstream: 1
mode: interactive-experience-foundation
state: interaction-contract-candidate
interface_implemented: false
atlas_semantics_authoritative: true
principia_status_separate: true
exact_revision_required: true
local_first: true
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Purpose

Define versioned, executable state contracts for future Atlas and Principia interaction without allowing interface state to become a new knowledge authority.

This candidate answers five questions:

1. What exact knowledge identity must every view carry?
2. How can navigation remain deterministic and reconstructible offline?
3. How can Principia references preserve separate status and exact Atlas revisions?
4. How must stale or unavailable references be shown?
5. How must failures preserve previous state and block silent authority changes?

## Contracts

```yaml
interaction_state_contract: atlas-interaction-state/0.1
interaction_view_contract: atlas-interaction-view/0.1
principia_reference_contract: atlas-principia-reference-envelope/0.1
impact_warning_contract: atlas-cross-repository-impact-warning/0.1
failure_state_contract: atlas-interaction-failure/0.1
fixture_contract: atlas-phase4-interaction-fixtures/0.1
report_contract: atlas-phase4-interaction-contract-report/0.1
```

## Interaction view contract

Every interaction view has:

- a stable view ID and positive revision;
- one declared view kind;
- at least one exact Atlas entity revision;
- a readable title;
- visible exact revision, provenance, review level, lifecycle, and staleness metadata;
- a keyboard path;
- an equivalent non-graph path;
- `graph_required: false`;
- explicit non-live and non-mutating authority fields.

Accepted candidate view kinds:

```text
entity
provenance
retrieval
filter
research-trail
candidate
principia-reference
impact-warning
```

Generated retrieval or research artifacts may be referenced only through accepted, replaceable, advisory contracts and exact source/build digests.

A view may not:

- hide the exact revision;
- present graph navigation as mandatory;
- remove review, lifecycle, staleness, or provenance visibility;
- use an unsupported generated artifact;
- grant canonical or lifecycle mutation authority.

## Interaction state contract

Every state binds:

- a stable state ID and revision;
- the exact Phase 4 mode;
- a deterministic route that does not contain implicit `latest`;
- an exact active view ID and revision;
- a deterministic, non-repeating history whose final entry is the active view;
- offline capability;
- explicit prohibition on canonical copying and mutation.

State is disposable navigation evidence. It is not canonical knowledge and cannot silently follow a newer entity revision.

## Principia reference envelope

The non-live reference envelope carries:

```yaml
principia_artifact_id: required
principia_artifact_revision: required
principia_status: required
atlas_references: exact-id-and-revision
reference_purpose: required
impact_state: required
fixture_only: true
principia_status_separate: true
implicit_latest: false
automatic_status_inheritance: false
live: false
```

The envelope proves navigation and warning semantics only. It does not activate synchronization and does not transfer Principia readiness into Atlas.

## Impact-warning contract

An impact warning names:

- a stable warning ID and revision;
- an impact state;
- severity;
- an exact requested Atlas target;
- the actual list of available revisions;
- a human-readable message;
- deterministic recovery actions;
- explicit prohibition on automatic updates or `latest` substitution.

The reference fixture requests `model:en:delayed-correction-recurrence@3`, while only revision 2 exists. The warning must remain blocking and must offer revision-aware recovery rather than silently opening revision 2.

## Failure-state contract

A failure state has:

- a stable failure ID and revision;
- a controlled category and error code;
- a concise summary;
- deterministic recovery actions;
- `preserve_previous_state: true`;
- `silent_fallback: false`;
- `implicit_latest: false`;
- `canonical_copy: false`;
- no mutation authority.

Reference failures cover:

- malformed interaction state;
- unavailable exact revision;
- missing offline generated artifact;
- Principia status mismatch;
- attempted authority escalation.

## Reference fixture set

The fixture manifest assembles four reviewable parts:

```text
reference-interactions.v01.json
views.v01.json
states.v01.json
bridge-failures.v01.json
negatives.v01.json
```

Positive coverage:

```yaml
views: 8
states: 8
principia_references: 1
impact_warnings: 1
failure_states: 5
workflow_kinds: 8
```

The views exercise:

1. exact Atlas entity inspection;
2. claim-to-evidence provenance;
3. accepted structured retrieval and explanation evidence;
4. deterministic evidence-role filtering;
5. exact-revision research trails;
6. advisory candidate inspection;
7. an offline Principia reference envelope;
8. an unavailable-revision impact warning.

## Negative boundaries

Six negative fixtures require exact error outcomes:

```yaml
- graph-only view: E-INTERACTION-ACCESSIBILITY
- live interaction state: E-INTERACTION-STATE-AUTHORITY
- Principia envelope without artifact revision: E-PRINCIPIA-REFERENCE
- automatic reference update: E-IMPACT-AUTHORITY
- failure state with canonical mutation: E-INTERACTION-FAILURE-AUTHORITY
- unknown view kind: E-INTERACTION-VIEW-KIND
```

Additional tests reject:

- implicit-`latest` routes;
- tampered canonical source digest;
- view-level canonical mutation;
- silent failure fallback.

## Accessibility boundary

Workstream 1 requires accessibility semantics before visual implementation.

Every reference view declares both:

- a deterministic keyboard path;
- a non-graph path conveying the same core information.

Graph visualization remains optional. A future shell must not encode information only through position, color, hover, or motion.

This contract does not claim full WCAG conformance. Browser-level accessibility testing begins only after a runnable shell exists.

## Determinism and replaceability

The manifest loader assembles the same semantic fixture from stable local parts. CI:

- compiles the canonical corpus;
- validates every exact reference;
- validates positive and negative fixtures;
- generates a deterministic assembled fixture artifact;
- generates a deterministic report;
- runs on Python 3.11 and 3.13;
- records fixture, artifact, and report digests;
- keeps all generated output disposable.

## Authority boundary

```yaml
canonical_authority: content/canonical/**/*.md
interaction_state: generated-and-disposable
interaction_views: advisory-presentation-state
principia_reference: fixture-only
principia_status_inheritance: false
implicit_latest: false
canonical_copy_authority: false
automatic_status_change: false
automatic_release_action: false
live_principia_dependency: false
external_services: false
embeddings: false
vector_database: false
live: false
repository_mutation: false
```

## Non-goals

This candidate does not:

- implement a user interface;
- define a visual design system;
- add accounts, cloud storage, collaboration, or plugins;
- select a frontend framework;
- claim production retrieval quality;
- add embeddings, learned ranking, or a vector database;
- activate live Principia synchronization;
- copy canonical knowledge into UI state;
- automate review, lifecycle, promotion, merge, or release decisions;
- certify human verification.

## Candidate decision rule

The contract candidate may be accepted only if:

- both Python versions produce valid deterministic evidence;
- every exact Atlas revision exists or produces an explicit warning/failure;
- all eight workflow kinds validate;
- keyboard and non-graph paths are present;
- all negative cases fail with the pinned error codes;
- generated artifacts remain advisory and replaceable;
- all Phase 0–3 and Atlas integration regressions remain green.

Acceptance authorizes a **minimal local reference shell candidate**, not a polished product interface.
