# Phase 4 — Principia & Atlas Interactive Experience

## Status

Active after accepted Phase 3 closure evidence.

```yaml
phase: 4
mode: interactive-experience-foundation
active_workstream: 1
workstream_name: interaction-contract-and-reference-shell
atlas_semantics_authoritative: true
principia_status_separate: true
exact_cross_repository_references: true
preferred_bounded_retrieval: structured-field-baseline
retrieval_authority: advisory-only
local_first: true
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Purpose

Build a unified user experience over proven Atlas and Principia semantics without erasing repository ownership, lifecycle status, provenance, revision identity, or authority boundaries.

Phase 4 is an experience phase. It may expose accepted semantics, but it may not redefine them.

## Entry evidence

Phase 4 entry is authorized by the accepted Phase 3 completion baseline:

```yaml
completion_contract: atlas-phase3-completion-report/0.1
completion_baseline_contract: atlas-phase3-completion-baseline/0.1
accepted_pr: 40
accepted_merge_commit: 52f51558a9188f049f4b4b838bc6acfd1a991e96
decision: proceed-phase4-interactive-experience
accepted_workstreams: [1, 2, 3, 5]
preferred_bounded_retrieval: structured-field-baseline
semantic_infrastructure_decision: defer-until-broader-benchmark-and-architecture-approval
```

## Workstream 1 — interaction contract and reference shell

### Objective

Define the smallest versioned interaction model and local reference shell that can exercise the accepted knowledge, retrieval, trail, candidate, and bridge semantics.

### Required contracts

Workstream 1 must define at least:

```yaml
interaction_state_contract: atlas-interaction-state/0.1
view_result_contract: atlas-interaction-view/0.1
principia_reference_contract: atlas-principia-reference-envelope/0.1
impact_warning_contract: atlas-cross-repository-impact-warning/0.1
failure_state_contract: atlas-interaction-failure/0.1
```

Contract names are candidates until executable fixtures and CI evidence are accepted.

### Interaction-state invariants

Every state must:

- identify the active view and stable state version;
- reference Atlas entities by exact ID and revision;
- expose canonical status, review level, staleness, and provenance where applicable;
- identify generated retrieval, filter, trail, or candidate evidence by exact contract and digest;
- distinguish Atlas state from Principia state;
- expose whether a Principia reference is available, stale, unavailable, or fixture-only;
- preserve deterministic back, forward, and deep-link behavior;
- remain disposable and reconstructible from canonical content and accepted fixtures;
- remain `live: false` and `repository_mutation: false` during Workstream 1.

### Reference workflows

The first fixture set must cover:

1. **Atlas entity inspection** — open a question, source, evidence, claim, model, concept, or synthesis at an exact revision.
2. **Provenance trace** — move from synthesis or claim to evidence and source locators without hiding lifecycle or review metadata.
3. **Explainable retrieval** — run the accepted structured baseline and inspect matched fields, score explanation, provenance, review, lifecycle, and staleness.
4. **Deterministic filtering** — apply entity-type, status, domain, date, and evidence-role filters while preserving exact revisions.
5. **Research trail** — save include, exclude, and context decisions as exact-revision references rather than copied canonical knowledge.
6. **Candidate inspection** — inspect contradiction and duplicate candidates without presenting them as confirmed or resolved.
7. **Principia bridge envelope** — follow a pinned offline reference that names an exact Atlas revision and preserves separate Principia readiness.
8. **Impact warning** — show an explicit warning when an Atlas revision is unavailable, stale, superseded in a fixture, or referenced by a Principia artifact with a different status.

### Required failure fixtures

Workstream 1 must include deterministic states for:

- malformed interaction state;
- unknown view type;
- missing Atlas entity;
- unavailable exact revision;
- stale review or staleness warning;
- missing provenance target;
- malformed retrieval or filter artifact;
- unavailable Principia reference;
- Principia status mismatch;
- offline package missing a generated artifact;
- attempted canonical or lifecycle mutation from interface state.

No failure state may silently substitute `latest`, hide authority metadata, or mutate canonical content.

## Reference shell boundary

The reference shell may be implemented only after the interaction contracts and fixtures are executable.

The first shell should be deliberately minimal:

- local-first and static-start capable;
- no mandatory account, cloud database, or external API;
- keyboard-accessible navigation;
- semantic HTML or equivalent accessible structure;
- graph visualization optional, never required for core navigation;
- deterministic URLs or local state identifiers;
- visible loading, empty, warning, error, and offline states;
- no design-system or animation expansion before contract acceptance.

A polished product interface is not a Workstream 1 requirement.

## Atlas views

Allowed Atlas views include:

- entity identity and exact revision;
- source and locator details;
- evidence appraisal and limitations;
- claim scope and disagreement;
- concept and model relations;
- synthesis provenance;
- review level, findings, lifecycle, and staleness;
- dependency and revision-impact warnings;
- structured retrieval explanations;
- filters, research trails, and advisory candidates.

Every visual relation must map to an accepted relation, provenance, dependency, review, lifecycle, retrieval, or trail semantic.

## Principia reference boundary

Principia remains a separate repository and authority domain.

A Phase 4 Principia reference envelope may contain:

```yaml
principia_artifact_id: required
principia_artifact_revision: required
principia_status: required
atlas_references:
  - atlas_id: required
    atlas_revision: required
reference_purpose: required
impact_state: required
fixture_only: true
live: false
```

The envelope may support navigation and impact warnings. It may not:

- import Principia publication status into Atlas;
- promote or deprecate Atlas entities;
- treat a synthetic bridge event as canonical history;
- silently follow newer Atlas revisions;
- activate live cross-repository synchronization.

## Accessibility and non-graph navigation

Workstream 1 acceptance requires:

- complete keyboard traversal of every reference workflow;
- visible focus state in the future shell;
- readable headings, landmarks, labels, and error summaries;
- a non-graph route for every relation or dependency workflow;
- no information encoded only by color, position, motion, or hover;
- reduced-motion compatibility if motion is later introduced;
- deterministic text alternatives for diagrams and graph views.

## Testing policy

The Workstream 1 matrix must include:

- contract and fixture validation on Python 3.11 and 3.13;
- exact-state digest checks;
- deterministic repeated builds;
- deletion and rebuild of generated interaction artifacts;
- authority-escalation negatives;
- offline and missing-artifact tests;
- accessibility fixture checks before shell expansion;
- complete Atlas CI and end-to-end regression.

Browser automation is not required until a runnable shell exists.

## Non-goals

Workstream 1 does not:

- claim production retrieval quality;
- select a vector database;
- add embeddings or learned ranking;
- activate live Principia synchronization;
- write canonical content from UI state;
- automate review, lifecycle, promotion, merge, or release decisions;
- create a public social or collaborative platform;
- implement accounts, permissions, cloud sync, or plugins;
- activate multilingual authoring;
- require graph visualization;
- certify human verification.

## Workstream 1 exit criteria

Workstream 1 closes only when:

- the interaction, view, Principia-reference, impact-warning, and failure contracts are versioned and executable;
- representative positive and negative workflows are pinned;
- every state preserves exact revisions and authority metadata;
- Atlas and Principia statuses remain separate;
- generated interaction artifacts are deterministic and replaceable;
- offline and missing-reference failures are explicit;
- interface state cannot mutate canonical or lifecycle authority;
- accessibility and non-graph requirements are machine-checkable where possible;
- a completion report recommends or rejects implementation of the minimal reference shell.

## Immediate next actions

1. implement `atlas-interaction-state/0.1` and `atlas-interaction-view/0.1`;
2. implement the offline Principia reference and impact-warning contracts;
3. create representative workflow and failure fixtures;
4. add deterministic validators and Python 3.11/3.13 CI;
5. produce a Workstream 1 evidence report;
6. keep UI implementation, live synchronization, semantic infrastructure, canonical writes, and automatic authority frozen until contract acceptance.

**Phase 4 is active, but implementation begins with interaction semantics and failure contracts—not visual polish.**
