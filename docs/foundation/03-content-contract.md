# Authoritative Content Contract

## Status

Draft authoring contract for Phase 0. Markdown remains authoritative; database rows, `.atlas` files, indexes, JSON, and UI views are derived artifacts.

## Contract goals

The content format must be:

- readable and editable without Atlas software;
- version-controllable with meaningful diffs;
- strict enough to validate identities, provenance, and relations;
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

This structure separates semantic roles. It is not intended to become the only navigation model; derived views may reorganize the same entities by topic, question, prerequisite, scale, timeline, or relation.

## Common metadata

Every canonical item begins with YAML-compatible front matter containing at least:

```yaml
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
```

Required common fields:

- `id` — stable canonical identifier;
- `type` — one accepted entity type;
- `title` — readable title;
- `status` — lifecycle state defined by editorial policy;
- `revision` — monotonic authored revision number;
- `created` and `updated` — ISO dates;
- `language` — language of the authored item;
- `tags` — optional controlled or provisional descriptors.

Review fields are added when applicable:

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

## Source record

A source record identifies the citable object and must not contain extracted claims as if they were the source itself.

```yaml
id: src:example-2025-feedback
 type: source
```

The leading space above is intentionally invalid and must be rejected by future fixtures; validators should detect malformed metadata rather than silently repair it.

A valid source should include fields such as:

```yaml
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
```

## Evidence record

Evidence points to a source and a precise context.

```yaml
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
```

The body explains the relevant observation, surrounding context, limitations, and legal handling of any excerpt. Long copyrighted passages should not be copied into the repository.

## Claim record

```yaml
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
relations:
  - type: supported-by
    target: evidence:example-feedback-result-1
```

The body contains definitions, reasoning, limitations, alternative explanations, and a confidence rationale. The statement must preserve qualifiers.

## Concept record

```yaml
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

Sections may be omitted only when genuinely inapplicable, not because the material has not been investigated.

## Model record

A model record identifies assumptions, formal structure, inputs, outputs, validation, and failure modes. Executable files may accompany it, but the Markdown record remains the explanation and provenance authority.

## Question record

A question includes its scope, motivation, current state, related concepts, relevant claims, blockers, and criteria for considering it resolved.

## Synthesis record

A synthesis identifies:

- the question it addresses;
- intended audience;
- included and excluded scope;
- material claims;
- evidence selection method;
- models used;
- disagreements;
- conclusion and confidence rationale;
- unresolved questions;
- revision trigger conditions.

## Relation representation

Relations use canonical IDs and accepted types:

```yaml
relations:
  - type: explains
    target: concept:oscillation
    note: Explains how repeated correction can create periodic behavior.
```

A relation must not be inferred as canonical merely because two pages link to each other in prose.

## Body links

Canonical links use stable IDs rather than relative filenames in authored semantics. A renderer may create human-friendly URLs later.

Example:

```text
See [[concept:feedback-loop]] and [[claim:delayed-negative-feedback-can-oscillate]].
```

## Deterministic compilation

A compiler may:

- validate front matter and controlled vocabularies;
- resolve stable IDs;
- build reverse links;
- generate numeric internal IDs;
- emit graph, database, search-index, and API artifacts;
- produce review and provenance reports.

A compiler must not:

- silently invent missing evidence;
- change claim meaning;
- promote review status;
- discard unknown fields without error;
- overwrite authoritative Markdown from a derived artifact;
- assign canonical identity based only on file order.

## Validation levels

### Structural validation

Checks syntax, required fields, unique IDs, valid entity types, dates, and references.

### Semantic validation

Checks relation compatibility, claim scope, evidence roles, lifecycle rules, and revision consistency.

### Editorial validation

Checks required sections, unresolved placeholders, citation completeness, and review records.

### Reproducibility validation

Rebuilds derived artifacts from a clean checkout and compares deterministic outputs.

## Compatibility principle

The authoring contract is versioned separately from any database or binary format. Migrations must preserve meaning and provenance. A storage optimization is never sufficient reason to weaken the authored contract.

## Phase 0 fixtures

Before implementation is approved, the contract must be tested with:

- valid minimal records for every entity type;
- a complete source-to-synthesis vertical slice;
- contradictory claims from credible sources;
- a model with assumptions and failure modes;
- a revised and superseded claim;
- multilingual metadata or content behavior;
- malformed examples that validators must reject;
- content whose generated order changes but canonical identity does not.
