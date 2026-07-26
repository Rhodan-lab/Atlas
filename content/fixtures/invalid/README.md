# Invalid `atlas-content/0.1` Fixtures

## Purpose

These compact examples define content that a validator must reject or flag. They are intentionally invalid and must never be imported as canonical knowledge.

The active authored corpus is English-only. Translation examples in this catalog are neutral synthetic contract fixtures.

| ID | Invalid pattern | Expected diagnostic |
|---|---|---|
| F001 | missing contract version | `E-CONTRACT-MISSING` |
| F002 | unsupported contract version | `E-CONTRACT-UNSUPPORTED` |
| F003 | duplicate durable identity | `E-ID-DUPLICATE` |
| F004 | numeric or file-order identity | `E-ID-NONCANONICAL` |
| F005 | evidence without a source | `E-EVIDENCE-SOURCE-MISSING` |
| F006 | evidence with an unstructured locator | `E-LOCATOR-STRUCTURE` |
| F007 | reversed `supports` relation | `E-RELATION-PAIR` |
| F008 | unknown vague relation | `E-RELATION-UNKNOWN` |
| F009 | reviewed status without review record | `E-REVIEW-RECORD-MISSING` |
| F010 | review targets another revision | `E-REVIEW-REVISION-MISMATCH` |
| F011 | synthetic translation inherits status or uses machine output as reviewed authorship | `E-TRANSLATION-REVIEW-MISSING`, `W-AI-ASSISTED-DRAFT-REQUIRED` |
| F012 | normative claim hides values | `E-NORMATIVE-VALUES-MISSING` |
| F013 | prediction lacks horizon and evaluation | `E-PREDICTION-HORIZON-MISSING`, `E-PREDICTION-EVALUATION-MISSING` |
| F014 | correlational claim uses causal wording | `W-CLAIM-KIND-LANGUAGE-CONFLICT` |
| F015 | numeric evidence lacks unit | `E-MEASUREMENT-UNIT-MISSING` |
| F016 | converted value loses original lineage | `E-CONVERSION-LINEAGE-MISSING` |
| F017 | derived evidence lacks input lineage | `E-TRANSFORMATION-INPUT-MISSING` |
| F018 | model-derived claim lacks model | `E-MODEL-REFERENCE-MISSING` |
| F019 | argument premise points directly to source | `E-ARGUMENT-PREMISE-TYPE` |
| F020 | normative argument hides empirical boundary | `W-NORMATIVE-INFERENCE-HIDDEN` |
| F021 | long restricted excerpt in public fixture | `E-RESTRICTED-CONTENT-PUBLIC` |
| F022 | hash presented as semantic truth proof | `W-INTEGRITY-SEMANTIC-OVERREACH` |
| F023 | silent claim merge or split without mapping | `E-MIGRATION-IDENTITY-MAPPING-MISSING` |
| F024 | unsupported field silently ignored | `E-FIELD-UNKNOWN` |

## Representative synthetic translation fixture

```yaml
---
contract: atlas-content/0.1
id: claim:fr:synthetic-translated-claim
work: work:synthetic-translated-claim
type: claim
title: Synthetic translated claim
status: reviewed
revision: 1
language: fr
translation_of: claim:en:synthetic-translated-claim
translation:
  source_revision: 2
  method: machine
---
```

Expected:

- `E-TRANSLATION-REVIEW-MISSING`;
- `W-AI-ASSISTED-DRAFT-REQUIRED`.

This fixture tests contract behavior only. It does not create an active authored language or supported product locale.

## Diagnostic principles

- Report all safe independent errors in one pass.
- Include path, entity ID when available, and field location.
- Separate structural errors from semantic or editorial warnings.
- Never auto-correct authored meaning.
- A warning cannot promote or demote lifecycle status by itself.
- Diagnostics must remain deterministic for identical input.
