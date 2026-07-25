# Authoritative Content Contract

## Status

**Provisional contract: `atlas-content/0.1`.** Markdown is authoritative. Database rows, `.atlas` files, indexes, JSON, and interface views are derived artifacts.

This document defines the common authored structure. Detailed rules live in the linked foundation policies.

## Contract goals

Canonical content must be:

- readable without Atlas software;
- version-controllable with meaningful diffs;
- strict enough to validate identity, provenance, review, and relations;
- expressive enough for scope, uncertainty, disagreement, translation, and revision;
- independent of one programming language or database;
- reproducibly compilable into disposable runtime formats.

## Proposed canonical layout

```text
content/
├── sources/
├── evidence/
├── claims/
├── concepts/
├── models/
├── questions/
├── syntheses/
├── translations/
└── vocabularies/
```

Folders separate semantic roles but do not define navigation. Derived views may organize the same entities by question, topic, prerequisite, time, scale, model, or relation.

## Common metadata

Every canonical entity begins with front matter:

```yaml
---
contract: atlas-content/0.1
id: concept:en:feedback-loop
work: work:feedback-loop
type: concept
title: Feedback loop
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
tags:
  - systems
  - causality
---
```

### Required common fields

- `contract` — supported authoring-contract version;
- `id` — stable identity for this language-specific authored entity;
- `work` — language-neutral identity shared by valid translations;
- `type` — one accepted entity type;
- `title` — human-readable label;
- `status` — lifecycle state from the editorial policy;
- `revision` — monotonic authored revision number;
- `created` and `updated` — ISO dates;
- `language` — BCP 47 language tag.

`tags` are optional descriptors and are not canonical relations.

### Identity rules

- IDs are not based only on file order or title.
- Renaming a title does not automatically change identity.
- Meaningful semantic replacement creates a new ID and a traceable supersession record.
- Two translations share `work`, not `id`.
- Generated numeric IDs are allowed only as disposable runtime identifiers.

See [`12-authoring-language-and-translation-policy.md`](12-authoring-language-and-translation-policy.md).

## Review metadata

Review applies to one exact revision:

```yaml
review:
  entity_revision: 2
  status: reviewed
  completed_at: 2026-08-10
  types:
    structural: pass
    source: pass
    domain: pass-with-notes
  reviewers:
    - reviewer:example-domain-01
  findings:
    - finding:scope-limited-to-stated-assay
  unresolved: []
```

A later material edit does not inherit this review automatically. See [`15-review-governance-and-disagreement.md`](15-review-governance-and-disagreement.md).

## Source record

```yaml
---
contract: atlas-content/0.1
id: src:en:example-feedback-paper
work: work:example-feedback-paper
type: source
title: Example Feedback Paper
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
source:
  kind: primary-research
  authors:
    - Example Author
  published: 2025-04-12
  locator: https://example.org/paper
  version: published
access:
  class: public-locator
---
```

A source identifies an origin. It does not automatically support any claim.

Recommended body sections:

1. Source description
2. Relevance
3. Access and version notes
4. Conflicts or limitations
5. Related evidence records

## Evidence record

```yaml
---
contract: atlas-content/0.1
id: evidence:en:example-result-1
work: work:example-result-1
type: evidence
title: Example result under delayed correction
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
source: src:en:example-feedback-paper
locator:
  kind: page-range
  value: pp. 14-16
extraction:
  method: manual
  checked: false
relations:
  - type: supports
    target: claim:en:delayed-feedback-can-oscillate
    note: The reported result is relevant within the stated model and protocol.
---
```

The body records:

- relevant observation, result, excerpt summary, or value;
- context needed to avoid distortion;
- extraction, collection, or transformation method;
- evidence appraisal and limitations;
- rationale for its relation role.

Long copyrighted material is not copied. Restricted and quantitative evidence follow [`14-evidence-data-and-restricted-source-policy.md`](14-evidence-data-and-restricted-source-policy.md).

## Claim record

```yaml
---
contract: atlas-content/0.1
id: claim:en:delayed-feedback-can-oscillate
work: work:delayed-feedback-can-oscillate
type: claim
title: Delayed feedback can produce oscillation in a stated model
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
claim:
  kind: model-derived
  statement: For the stated recurrence and parameter values, the state follows an oscillatory sequence.
  scope:
    model: model:en:delayed-correction-recurrence
  confidence: strongly-supported
  confidence_rationale: The sequence can be recalculated exactly for the stated values.
model: model:en:delayed-correction-recurrence
---
```

The body records definitions, reasoning, limitations, alternatives, and relevant links. Material qualifiers remain inside the statement or structured scope.

Claim kinds and argument blocks follow [`13-claim-scope-and-argument-policy.md`](13-claim-scope-and-argument-policy.md).

## Concept record

```yaml
---
contract: atlas-content/0.1
id: concept:en:feedback-loop
work: work:feedback-loop
type: concept
title: Feedback loop
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
claims:
  - claim:en:delayed-feedback-can-oscillate
relations:
  - type: prerequisite-of
    target: concept:en:closed-loop-stability
---
```

Recommended body sections:

1. Working definition
2. Boundaries and non-examples
3. Why it matters
4. Prerequisites
5. Key claims
6. Models
7. Examples and counterexamples
8. Misconceptions
9. Applications
10. Disputes and limitations
11. Open questions
12. Revision notes

A concept organizes claims; it does not turn a page of prose into one untraceable assertion.

## Model record

```yaml
---
contract: atlas-content/0.1
id: model:en:delayed-correction-recurrence
work: work:delayed-correction-recurrence
type: model
title: Delayed correction recurrence
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
purpose: Demonstrate how a delayed state enters a corrective recurrence.
formal_structure: x[t+1] = x[t] - k*x[t-d]
inputs:
  - state history
parameters:
  - gain k
  - delay d
outputs:
  - next state
assumptions:
  - scalar state
  - discrete time
  - fixed parameters
validation:
  - evidence:en:delayed-recurrence-sequence
failure_modes:
  - nonlinear response
  - changing parameters
  - saturation
---
```

Models expose purpose, assumptions, inputs, outputs, formal or conceptual structure, parameters, validation, and failure modes.

## Question record

```yaml
---
contract: atlas-content/0.1
id: question:en:when-can-delayed-correction-oscillate
work: work:when-can-delayed-correction-oscillate
type: question
title: When can delayed correction oscillate?
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
state: partially-answered
resolution_criteria:
  - formal conditions are stated
  - real-system applicability is separated from model behavior
---
```

Questions record scope, motivation, state, blockers, related entities, and resolution criteria.

## Synthesis record

```yaml
---
contract: atlas-content/0.1
id: synthesis:en:delayed-feedback-synthesis
work: work:delayed-feedback-synthesis
type: synthesis
title: Delayed feedback and oscillation
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
question: question:en:when-can-delayed-correction-oscillate
material_claims:
  - claim:en:delayed-feedback-can-oscillate
relations:
  - type: derived-from
    target: claim:en:delayed-feedback-can-oscillate
---
```

A synthesis records audience, scope, evidence-selection method, claims, models, disagreement, conclusion, confidence rationale, open questions, and revision triggers. It never replaces its dependencies.

## Revision record

Revision is represented by entity history plus explicit change metadata:

```yaml
revision_note:
  previous_revision: 1
  change_kind: scope-change
  reason: New evidence showed the conclusion applies only to one assay protocol.
  triggered_by:
    - evidence:en:new-assay-comparison
  downstream_review:
    - synthesis:en:catalase-assay-synthesis
```

Supersession across durable IDs uses the governed relation vocabulary. Staleness and dependency behavior follow [`16-revision-impact-and-staleness.md`](16-revision-impact-and-staleness.md).

## Argument block

Arguments remain embedded in `0.1`:

```yaml
argument:
  mode: inductive
  premises:
    - claim:en:premise-one
    - claim:en:premise-two
  assumptions:
    - claim:en:scope-matches
  conclusion: claim:en:conclusion
  alternatives:
    - claim:en:alternative-explanation
```

Premises reference claims, not raw source URLs.

## Relation representation

```yaml
relations:
  - type: explains
    target: concept:en:oscillation
    note: Identifies the stated mechanism under the model assumptions.
```

Relation direction and compatible pairs come only from [`10-relation-vocabulary.md`](10-relation-vocabulary.md). A prose link is not automatically a canonical relation.

## Canonical body links

```text
See [[concept:en:feedback-loop]] and [[claim:en:delayed-feedback-can-oscillate]].
```

A renderer may create localized human-friendly URLs later.

## Deterministic compilation

A compiler may:

- validate metadata and controlled vocabularies;
- resolve IDs and build reverse links;
- generate numeric runtime IDs;
- emit graph, database, index, API, review, provenance, and staleness artifacts.

A compiler must not:

- invent evidence;
- alter claim meaning or remove qualifiers;
- promote review status;
- infer normative values;
- silently translate content;
- ignore unknown fields;
- overwrite authoritative Markdown from derived output;
- assign durable identity from file order;
- decide that a semantic revision is unaffected without a recorded rule or review.

## Validation levels

### Structural

Syntax, contract version, common fields, identity, dates, references, and field types.

### Semantic

Entity compatibility, relation direction, claim kind, scope, evidence role, translation, lifecycle, revision, and staleness rules.

### Editorial

Claim atomicity, qualifier preservation, confidence rationale, citation completeness, required sections, and unresolved placeholders.

### Reproducibility

Clean rebuild and deterministic comparison of derived artifacts, transformations, diagnostics, and provenance reports.

## Invalid fixtures

Invalid examples live in [`../../content/fixtures/invalid/README.md`](../../content/fixtures/invalid/README.md) with expected diagnostics. Validators report errors rather than silently repairing authored semantics.

## Compatibility

Versioning and migration follow [`11-contract-versioning-and-migrations.md`](11-contract-versioning-and-migrations.md). A migration preserves identity, meaning, provenance, evidence roles, review, uncertainty, and revision history.

## Phase 0 evidence

The bundled reference slices in [`../../content/reference/`](../../content/reference/) exercise:

- empirical and synthetic observation;
- formal model-derived evidence;
- observational and randomized platform evidence;
- legal context;
- descriptive, causal, methodological, interpretive, and normative claims;
- argument blocks;
- uncertainty and scope;
- source conflict disclosure;
- revision triggers.

They remain draft until split, validated, and independently reviewed.
