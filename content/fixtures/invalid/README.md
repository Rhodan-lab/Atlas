# Invalid `atlas-content/0.1` Fixtures

## Purpose

These compact fixtures define content that a Phase 1 validator must reject or flag. They are intentionally invalid and must never be imported as canonical knowledge.

Diagnostic codes are provisional but stable enough to test error specificity.

## F001 — Missing contract version

```yaml
---
id: claim:en:no-contract
type: claim
title: Missing contract
status: draft
revision: 1
language: en
---
```

Expected: `E-CONTRACT-MISSING`.

## F002 — Unsupported contract version

```yaml
---
contract: atlas-content/99.0
id: concept:en:future-format
type: concept
title: Future format
status: draft
revision: 1
language: en
---
```

Expected: `E-CONTRACT-UNSUPPORTED`.

## F003 — Duplicate durable identity

Two files declare:

```yaml
id: claim:en:duplicate-id
```

Expected: `E-ID-DUPLICATE` with both file locations.

## F004 — File-order numeric identity

```yaml
---
contract: atlas-content/0.1
id: 17
type: claim
title: Numeric-only identity
status: draft
revision: 1
language: en
---
```

Expected: `E-ID-NONCANONICAL`.

## F005 — Evidence without source

```yaml
---
contract: atlas-content/0.1
id: evidence:en:no-source
type: evidence
title: Evidence without origin
status: draft
revision: 1
language: en
locator:
  kind: page
  value: 4
---
```

Expected: `E-EVIDENCE-SOURCE-MISSING`.

## F006 — Evidence with imprecise locator

```yaml
---
contract: atlas-content/0.1
id: evidence:en:vague-location
type: evidence
title: Vague evidence
status: draft
revision: 1
language: en
source: src:example
locator: somewhere in the paper
---
```

Expected: `E-LOCATOR-STRUCTURE`; editorial follow-up may add `W-LOCATOR-IMPRECISE`.

## F007 — Reversed support relation

```yaml
---
contract: atlas-content/0.1
id: claim:en:reversed-support
type: claim
title: Reversed support
status: draft
revision: 1
language: en
relations:
  - type: supports
    target: evidence:en:some-result
---
```

Expected: `E-RELATION-PAIR`; `supports` is evidence → claim.

## F008 — Unknown vague relation

```yaml
relations:
  - type: related-to
    target: concept:en:another-concept
```

Expected: `E-RELATION-UNKNOWN`.

## F009 — Reviewed without review record

```yaml
---
contract: atlas-content/0.1
id: claim:en:unreviewed-reviewed
work: work:unreviewed-reviewed
type: claim
title: Unsupported review status
status: reviewed
revision: 1
language: en
claim:
  kind: descriptive
  statement: This item claims reviewed status without a review record.
---
```

Expected: `E-REVIEW-RECORD-MISSING`.

## F010 — Review targets another revision

```yaml
status: reviewed
revision: 3
review:
  entity_revision: 2
  status: reviewed
```

Expected: `E-REVIEW-REVISION-MISMATCH`.

## F011 — Translation inherits status

```yaml
---
contract: atlas-content/0.1
id: claim:id:translated-claim
work: work:translated-claim
type: claim
title: Klaim terjemahan
status: reviewed
revision: 1
language: id
translation_of: claim:en:translated-claim
translation:
  source_revision: 2
  method: machine
---
```

Expected: `E-TRANSLATION-REVIEW-MISSING` and `W-AI-ASSISTED-DRAFT-REQUIRED`.

## F012 — Normative claim hides values

```yaml
claim:
  kind: normative
  statement: Platforms must always use chronological feeds.
```

Expected: `E-NORMATIVE-VALUES-MISSING`.

## F013 — Prediction lacks horizon

```yaml
claim:
  kind: predictive
  statement: This intervention will reduce harmful exposure.
```

Expected: `E-PREDICTION-HORIZON-MISSING` and `E-PREDICTION-EVALUATION-MISSING`.

## F014 — Causal wording on correlational claim

```yaml
claim:
  kind: correlational
  statement: Increased recommendation frequency causes stronger belief.
```

Expected: `W-CLAIM-KIND-LANGUAGE-CONFLICT`; requires editorial and methodological review rather than automatic rewriting.

## F015 — Numeric evidence lacks unit

```yaml
measurement:
  quantity: temperature
  value: 37
```

Expected: `E-MEASUREMENT-UNIT-MISSING`.

## F016 — Converted value loses original

```yaml
measurement:
  quantity: length
  value: 10
  unit: cm
  transformation: converted
```

Expected: `E-CONVERSION-LINEAGE-MISSING`.

## F017 — Derived evidence lacks input lineage

```yaml
transformation:
  procedure: analysis:summary-v1
  parameters:
    aggregation: mean
```

Expected: `E-TRANSFORMATION-INPUT-MISSING`.

## F018 — Model-derived claim lacks model

```yaml
claim:
  kind: model-derived
  statement: The sequence is periodic.
```

Expected: `E-MODEL-REFERENCE-MISSING`.

## F019 — Argument premise points directly to source

```yaml
argument:
  mode: inductive
  premises:
    - src:paper-1
  conclusion: claim:en:conclusion
```

Expected: `E-ARGUMENT-PREMISE-TYPE`; premises reference claims.

## F020 — Normative argument hides empirical boundary

```yaml
argument:
  mode: deductive
  premises:
    - claim:en:ranking-changes-exposure
  conclusion: claim:en:platforms-should-be-banned
```

Expected: `W-NORMATIVE-INFERENCE-HIDDEN`; the conclusion needs a normative mode and explicit value premises.

## F021 — Long restricted excerpt in public fixture

```yaml
access:
  class: licensed
excerpt: <full copyrighted chapter>
```

Expected: `E-RESTRICTED-CONTENT-PUBLIC`; validators may detect metadata but human review is required for actual content length and rights.

## F022 — Hash presented as authenticity proof

```yaml
integrity:
  algorithm: sha256
  digest: abc123
claim:
  statement: The digest proves that the source is true.
```

Expected: `W-INTEGRITY-SEMANTIC-OVERREACH`.

## F023 — Silent claim merge during migration

Migration output combines two input claim IDs into one ID without a mapping record.

Expected: `E-MIGRATION-IDENTITY-MAPPING-MISSING`.

## F024 — Unsupported field silently ignored

```yaml
magic_truth_score: 0.98
```

Expected: `E-FIELD-UNKNOWN`; the validator must not discard it silently.

## Diagnostic principles

- Report all safe independent errors in one pass.
- Include path, entity ID when available, and field location.
- Separate structural errors from semantic or editorial warnings.
- Never auto-correct authored meaning.
- A warning cannot promote or demote lifecycle status by itself.
- Diagnostics must remain deterministic for identical input.
