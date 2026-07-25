# Review Governance and Reviewer Disagreement

## Status

**Accepted for `atlas-content/0.1`.** This policy defines review authority without pretending that one reviewer or institution owns truth.

## Review principle

Review is a recorded assessment of one entity revision against defined criteria. It is not a permanent badge attached to a title or file path.

A reviewer confirms only the review types and scope they actually evaluated.

## Reviewer roles

Initial roles:

- `structural-reviewer` — contract, identifiers, references, and validation;
- `editorial-reviewer` — clarity, terminology, scope, and faithful presentation;
- `source-reviewer` — source identity, locator, excerpt fidelity, and access handling;
- `domain-reviewer` — subject-matter accuracy and important omissions;
- `method-reviewer` — study design, measurement, analysis, and inference;
- `reproducibility-reviewer` — calculations, transformations, and executable procedures;
- `ethics-reviewer` — values, affected groups, risk, consent, power, and responsible use;
- `translation-reviewer` — fidelity and terminology across languages.

One person may hold several roles, but every role assessment remains explicit.

## Reviewer identity

A review record includes a stable reviewer identity or, when privacy requires it, a stable pseudonymous reviewer ID controlled by the project.

```yaml
reviewers:
  - id: reviewer:example-domain-01
    role: domain-reviewer
    affiliation: independent
    conflict_statement: none-declared
```

Public display may omit private contact information while preserving accountability and uniqueness.

## Required review record

```yaml
review:
  entity_revision: 3
  status: reviewed
  completed_at: 2026-07-26
  types:
    structural: pass
    source: pass
    domain: pass-with-notes
  reviewers:
    - reviewer:example-domain-01
  findings:
    - finding:scope-limited-to-classroom-assay
  unresolved:
    - finding:temperature-not-controlled-precisely
```

A later entity revision does not inherit this record automatically.

## Review outcomes

Each review type records one outcome:

- `pass`
- `pass-with-notes`
- `changes-required`
- `not-applicable`
- `unable-to-review`

`pass-with-notes` is acceptable only when remaining issues do not materially undermine the stated scope or confidence.

## Minimum review by entity type

### Source

Required for reviewed status:

- structural;
- source.

### Evidence

Required:

- structural;
- source;
- domain or methodological review when interpretation or measurement is material.

### Empirical claim

Required:

- structural;
- editorial;
- source;
- domain;
- methodological when inference depends on study design or analysis.

### Definitional or formal claim

Required:

- structural;
- editorial;
- domain;
- source when externally attributed.

### Model

Required:

- structural;
- editorial;
- domain;
- methodological;
- reproducibility when executable or computational.

### Normative claim or socio-technical synthesis

Required:

- structural;
- editorial;
- domain;
- source where factual premises are used;
- ethics;
- methodological when empirical inference is material.

### Translation

Required:

- structural;
- editorial;
- translation;
- domain when technical meaning may shift.

## Independence and conflicts

Review records disclose relevant conflicts, including:

- authorship of the reviewed item;
- employment or funding connection to a source or affected organization;
- direct competitive interest;
- personal relationship likely to affect judgment;
- advocacy role relevant to a contested normative conclusion;
- inability to access underlying evidence.

A conflict does not always disqualify a reviewer. It changes what additional independent review may be required.

## Self-review

Authors may perform structural checks and an explicit author self-review, but self-review alone cannot create `reviewed` status for material factual, methodological, or normative claims.

Small personal projects may use one person in several roles only if the limitation is visible and the status is `reviewed-limited`, not full `reviewed`. `reviewed-limited` is a presentation label derived from review coverage, not a canonical lifecycle state.

## Reviewer disagreement

Reviewer disagreement is preserved as review findings rather than overwritten by majority vote.

When reviewers disagree materially:

1. record each finding and rationale;
2. identify whether disagreement concerns fact, scope, method, interpretation, terminology, or values;
3. compare source access and definitions;
4. request targeted additional review where useful;
5. mark the entity `in-review` or `contested` when disagreement affects its conclusion;
6. allow a synthesis to state the unresolved review disagreement explicitly.

A numeric vote is insufficient for semantic resolution.

## Finding severity

- `critical` — loss of provenance, fabricated evidence, severe integrity issue, or dangerous misrepresentation;
- `major` — material error in scope, inference, evidence, or conclusion;
- `moderate` — meaningful ambiguity or omission that limits use;
- `minor` — clarity or consistency issue without material semantic effect;
- `note` — optional improvement or recorded context.

Critical and major findings block reviewed status.

## Review expiration and staleness

Review may become stale when:

- the entity changes materially;
- a supporting source is corrected, retracted, or superseded;
- evidence access or integrity changes;
- a model or dataset version changes;
- a dependent definition changes;
- a translation source revision changes;
- a time-sensitive claim exceeds its review horizon.

Time-sensitive entities may declare:

```yaml
review_horizon:
  kind: date
  value: 2027-01-01
```

Expiration triggers review; it does not automatically make the previous review dishonest.

## Review of AI-assisted material

Reviewers must know when extraction, classification, translation, relation generation, or synthesis was AI-assisted.

Required checks include:

- source locator verification;
- unsupported-claim detection;
- qualifier preservation;
- citation-to-claim alignment;
- disagreement preservation;
- prompt or procedure record where practical.

Review cannot consist solely of another AI system approving the output.

## Review packets

A later validator should generate a review packet containing:

- entity revision;
- rendered body;
- sources and evidence locators;
- supporting and challenging relations;
- dependencies;
- previous review findings;
- changes since the reviewed revision;
- unresolved questions;
- restricted-evidence access notes.

The packet assists review but does not replace reviewer judgment.

## Governance changes

Changes to required review types or lifecycle consequences are semantic contract changes. They require:

- decision rationale;
- affected entity classes;
- migration or stale-review rules;
- updated fixtures;
- review of previously reviewed material where applicable.
