# Authoritative Content Contract

## Status

Draft authoring contract for Phase 0. Markdown remains authoritative; database rows, `.atlas` files, indexes, JSON, and UI views are derived artifacts.

## Contract goals

The content format must be:

- readable and editable without Atlas software;
- version-controllable with meaningful diffs;
- strict enough to validate identity, provenance, review, and relations;
- expressive enough for uncertainty and disagreement;
- independent of a specific programming language or database;
- reproducibly compilable into runtime formats.

## Proposed source layout

```text
content/
├── sources/
├── evidence/
├── claims/
├── concepts/
├── models/
├── questions/
├── syntheses/
└── vocabularies/
```

The folders separate semantic roles. They are not the only navigation structure; derived views may reorganize the same entities by topic, question, prerequisite, scale, timeline, or relation.

## Common metadata

Every canonical item begins with front matter:

```yaml
---
id: concept:feedback-loop
type: concept
title: Feedback loop
status: draft
revision: 1
created: 2026-07-25
updated: 2026-07-25
language: en
tags:
  - systems
  - causality
---
```

Required common fields:

- `id` — stable canonical identifier;
- `type` — one accepted entity type;
- `title` — readable title;
- `status` — lifecycle state defined by the editorial policy;
- `revision` — monotonic authored revision number;
- `created` and `updated` — ISO dates;
- `language` — language of the authored item;
- `tags` — optional controlled or provisional descriptors.

Review information is added only when review has occurred:

```yaml
review:
  version: 1
  status: reviewed
  types:
    - structural
    - source
    - domain
  reviewed_at: 2026-08-10
  reviewers:
    - role: domain-reviewer
      name: Example Reviewer
```

The review record applies to one explicit revision. Later material changes return affected material to the appropriate review state.

## Source record

A source record identifies a citable object. It does not contain extracted claims as if they were properties of the source.

```yaml
---
id: src:example-2025-feedback
type: source
title: Feedback and Stability in Dynamic Systems
status: draft
revision: 1
created: 2026-07-25
updated: 2026-07-25
language: en
source:
  kind: primary-research
  authors:
    - Example Author
  published: 2025-04-12
  locator: https://example.org/paper
  version: published
---
```

Recommended body sections:

1. Source description
2. Relevance
3. Access and version notes
4. Known limitations or conflicts of interest
5. Related evidence records

## Evidence record

Evidence identifies the relevant material and context from a source. Evidence-to-claim relations point from the evidence toward the claim because the evidence performs the supporting, challenging, or contextualizing role.

```yaml
---
id: evidence:example-feedback-result-1
type: evidence
title: Amplification result under delayed correction
status: draft
revision: 1
created: 2026-07-25
updated: 2026-07-25
language: en
source: src:example-2025-feedback
locator:
  kind: page-range
  value: pp. 14–16
extraction:
  method: manual
  checked: false
relations:
  - type: supports
    target: claim:delayed-negative-feedback-can-oscillate
---
```

The body explains:

- the observation, measurement, excerpt summary, or structured value;
- surrounding context needed to avoid distortion;
- extraction or collection method;
- limitations;
- why the stated evidence role is appropriate.

Long copyrighted passages should not be copied into the repository. Store a precise locator and a limited lawful excerpt or summary when appropriate.

## Claim record

```yaml
---
id: claim:delayed-negative-feedback-can-oscillate
type: claim
title: Delayed negative feedback can produce oscillation
status: draft
revision: 1
created: 2026-07-25
updated: 2026-07-25
language: en
claim:
  kind: causal
  statement: Under specified response delays and gain conditions, negative feedback can produce oscillatory behavior.
  scope: Dynamic systems represented by the stated model assumptions.
  confidence: plausible
---
```

The body contains:

- definitions needed to interpret the statement;
- reasoning;
- confidence rationale;
- limitations and alternative explanations;
- links to relevant evidence, concepts, models, and competing claims.

The statement must preserve qualifiers. A claim that contains several independently disputable assertions should be split.

## Concept record

```yaml
---
id: concept:feedback-loop
type: concept
title: Feedback loop
status: draft
revision: 1
created: 2026-07-25
updated: 2026-07-25
language: en
claims:
  - claim:delayed-negative-feedback-can-oscillate
relations:
  - type: prerequisite-of
    target: concept:dynamic-stability
---
```

Recommended body sections:

1. Working definition
2. Boundaries and non-examples
3. Why it matters
4. Prerequisites
5. Key claims
6. Models and representations
7. Examples and counterexamples
8. Misconceptions
9. Applications
10. Disputes and limitations
11. Open questions
12. Revision notes

A concept organizes claims; it does not convert all prose into one untraceable assertion.

## Model record

A model record identifies:

- purpose;
- assumptions;
- inputs and outputs;
- formal or conceptual structure;
- parameters and their sources;
- validation evidence;
- known failure modes;
- claims derived from using the model.

Executable files may accompany the model, but the Markdown record remains the explanation and provenance authority.

## Question record

A question includes:

- scope;
- motivation;
- current state;
- related concepts, claims, evidence, and models;
- blockers;
- criteria for considering the question resolved within its scope.

## Synthesis record

A synthesis identifies:

- the question it addresses;
- intended audience;
- included and excluded scope;
- material claims;
- evidence selection method;
- models used;
- supporting and challenging material;
- disagreements;
- conclusion and confidence rationale;
- unresolved questions;
- revision trigger conditions.

A synthesis is derived knowledge and must expose its dependencies.

## Relation representation

Relations use canonical IDs and an accepted vocabulary:

```yaml
relations:
  - type: explains
    target: concept:oscillation
    note: Explains how repeated correction can create periodic behavior.
```

Direction is semantic. For example:

- evidence `supports` a claim;
- one claim `contradicts` another claim;
- one concept is `prerequisite-of` another concept;
- a synthesis is `derived-from` material claims.

A link in prose does not automatically create a canonical relation.

## Body links

Canonical links use stable IDs rather than relative filenames in authored semantics:

```text
See [[concept:feedback-loop]] and [[claim:delayed-negative-feedback-can-oscillate]].
```

A renderer may later create human-friendly URLs.

## Invalid fixture example

Malformed content belongs in a dedicated invalid-fixture directory and must be clearly marked. It must never be presented beside valid authoring examples without a label.

```yaml
# INVALID: missing stable id and unsupported status
---
type: claim
title: An invalid fixture
status: finished
revision: 1
---
```

A validator should report each violated rule specifically rather than silently repairing the file.

## Deterministic compilation

A compiler may:

- validate front matter and controlled vocabularies;
- resolve stable IDs;
- build reverse links;
- generate numeric internal IDs;
- emit graph, database, search-index, and API artifacts;
- produce review and provenance reports.

A compiler must not:

- invent missing evidence;
- change claim meaning;
- remove qualifiers;
- promote review status;
- discard unknown fields without error;
- overwrite authoritative Markdown from a derived artifact;
- assign canonical identity based only on file order.

## Validation levels

### Structural validation

Checks syntax, required fields, unique IDs, valid entity types, dates, and references.

### Semantic validation

Checks relation compatibility, direction, claim scope, evidence roles, lifecycle rules, and revision consistency.

### Editorial validation

Checks required sections, unresolved placeholders, citation completeness, confidence rationale, and review records.

### Reproducibility validation

Rebuilds derived artifacts from a clean checkout and compares deterministic output and provenance.

## Compatibility principle

The authoring contract is versioned separately from any database or binary format. Migrations must preserve identity, meaning, provenance, review, and revision history. Storage optimization is never sufficient reason to weaken the authored contract.

## Phase 0 fixtures

Before implementation is approved, the contract must be tested with:

- valid minimal records for every entity type;
- a complete source-to-synthesis vertical slice;
- contradictory claims from credible sources;
- a model with assumptions and failure modes;
- a revised and superseded claim;
- multilingual metadata or content behavior;
- malformed examples that validators must reject;
- content whose generated order changes while canonical identity remains stable.
