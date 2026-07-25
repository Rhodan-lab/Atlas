# Evidence, Data, and Restricted Source Policy

## Status

**Accepted for `atlas-content/0.1`.** Domain extensions may add fields but may not weaken the common provenance core.

## Evidence storage principle

Atlas stores enough information to verify how evidence is used without assuming that every source can be copied into the repository.

The default is:

- stable source identity;
- precise locator;
- concise factual description or limited lawful excerpt;
- extraction or observation method;
- context and limitations;
- integrity information where useful;
- explicit evidence role.

The source itself remains authoritative for its content.

## Evidence access classes

Every evidence record declares one access class:

- `open` — source and relevant material can be redistributed under known terms;
- `public-locator` — publicly accessible, but Atlas stores only locator and limited notes;
- `licensed` — accessible under license; redistribution may be restricted;
- `private` — supplied by a user or organization and not publicly shareable;
- `sensitive` — access must be restricted because disclosure could create harm or violate duty;
- `unavailable` — source is known but currently inaccessible;
- `ephemeral` — source may change or disappear and requires capture metadata where lawful.

Access class does not determine evidence quality.

## Copyright and excerpt handling

- Prefer summaries and precise locators over copying long passages.
- Store only the minimum excerpt needed for review when lawful.
- Preserve quotation boundaries and do not present paraphrase as verbatim text.
- Record page, section, table, figure, timestamp, row range, or other locator.
- Do not bypass access controls.
- Do not commit licensed or private source files to a public repository.
- A public fixture may describe restricted evidence structure using synthetic content.

## Evidence locator object

```yaml
locator:
  kind: page-range
  value: pp. 121–126
  edition: Methods in Enzymology, vol. 105
```

Initial locator kinds:

- `page`
- `page-range`
- `section`
- `figure`
- `table`
- `paragraph`
- `timestamp`
- `record-id`
- `row-range`
- `cell-range`
- `commit`
- `version`
- `observation-log`
- `query`

A free-text locator is allowed only when no structured kind fits, and it must explain why.

## Integrity metadata

For local or changing material, evidence may include:

```yaml
integrity:
  algorithm: sha256
  digest: <hex>
  captured_at: 2026-07-26T10:00:00Z
  media_type: text/csv
```

A digest establishes byte identity, not truth or authenticity by itself.

## Quantitative evidence core

Quantitative evidence includes:

```yaml
measurement:
  quantity: reaction-rate-proxy
  value: 42
  unit: bubbles-per-minute
  uncertainty:
    kind: range
    lower: 38
    upper: 46
  method: manual-count
  repeats: 3
```

Required when applicable:

- quantity or variable identity;
- value and unit;
- uncertainty or explicit reason it is unavailable;
- population or sample;
- collection time and setting;
- method or instrument;
- transformations;
- missing-data handling;
- analysis or model producing a derived value.

## Units

- Prefer SI units where appropriate.
- Preserve source units when conversion could hide meaning.
- Record conversion formulas and original values.
- Unitless quantities must say why they are unitless.
- Informal classroom proxies, such as foam height, remain valid observations only when labeled as proxies rather than direct enzyme-rate measurements.

## Dataset record

A dataset remains a `source` with `source.kind: dataset`. Evidence points to a version, subset, query, or row range.

```yaml
source:
  kind: dataset
  version: 2026-01
  schema: dataset-schema-v3
  locator: https://example.org/data
```

Dataset-specific metadata may include:

- variables and definitions;
- units;
- coverage;
- sampling design;
- collection process;
- license;
- missing-value codes;
- update frequency;
- known quality issues;
- data-processing lineage.

## Transformations and analyses

Derived quantitative evidence records its lineage:

```yaml
transformation:
  input:
    - evidence:en:raw-catalase-observations
  procedure: analysis:catalase-rate-summary-v1
  software:
    name: python
    version: 3.12
  parameters:
    aggregation: median
  output_integrity:
    algorithm: sha256
    digest: <hex>
```

The procedure may reference code, a notebook, an equation, or a manual calculation. Parameters and exclusions must be explicit.

## Observation records

A direct observation is evidence only within its documented conditions.

Record:

- observer or instrument;
- date and setting;
- protocol version;
- material or subject description;
- controls;
- deviations;
- raw result;
- uncertainty and limitations.

An observation does not inherit general scientific authority because it is stored in Atlas.

## Private and sensitive evidence

Canonical public content may reference a protected evidence ID without revealing protected content.

```yaml
access:
  class: private
  repository: local-vault
  disclosure: metadata-only
```

Rules:

- public syntheses state when conclusions depend on unavailable evidence;
- reviewers must have appropriate authorization;
- exported views exclude protected fields by policy;
- redaction is recorded as a transformation;
- removing access does not delete provenance history;
- sensitive information is not used in public fixtures.

## Unavailable evidence

When evidence cannot be inspected:

- do not fabricate an excerpt;
- record the source, locator, and access problem;
- lower confidence or limit review as appropriate;
- distinguish “not found” from “not publicly accessible”;
- record previous verification if one occurred and by whom.

## Evidence quality and source status

A retracted, corrected, superseded, or disputed source remains in provenance but triggers review of dependent evidence and claims.

Evidence appraisal must consider:

- directness;
- methodological fit;
- measurement validity;
- independence;
- reproducibility;
- applicability;
- bias and conflicts;
- missing data;
- access limitations.

No access class or numeric appraisal becomes a universal truth score.

## Validation rules

Reject or flag:

- evidence without source;
- imprecise locator when a precise one is available;
- excerpt marked as verbatim without quotation provenance;
- numeric value without unit or explicit unitless status;
- converted value without original value and method;
- derived evidence without input lineage;
- public fixture containing private or licensed content;
- hash presented as proof of truth;
- evidence role unsupported by its rationale;
- direct observation generalized beyond its documented scope.
