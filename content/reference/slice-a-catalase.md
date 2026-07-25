# Reference Slice A — Catalase Activity and Assay Conditions

## Slice metadata

```yaml
contract: atlas-content/0.1
id: synthesis:en:catalase-assay-conditions-slice
work: work:catalase-assay-conditions-slice
type: synthesis
title: Catalase activity depends on enzyme source and assay conditions
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
```

## Question record

```yaml
id: question:en:how-do-ph-and-temperature-affect-catalase-assays
work: work:how-do-ph-and-temperature-affect-catalase-assays
type: question
status: draft
state: partially-answered
scope:
  process: catalase-catalyzed-hydrogen-peroxide-decomposition
  settings:
    - in-vitro enzyme assays
    - classroom tissue assays
```

**Question:** How do pH and temperature affect measured catalase activity, and which conclusions can be generalized across enzyme sources and assay methods?

**Resolution criterion:** distinguish direct published findings, general mechanistic interpretation, and limitations of classroom proxy measurements.

## Source records

### Source 1

```yaml
id: src:aebi-1984-catalase-in-vitro
type: source
status: draft
source:
  kind: methodological-reference
  authors:
    - Hugo Aebi
  title: Catalase in vitro
  container: Methods in Enzymology
  volume: 105
  pages: 121-126
  published: 1984
  doi: 10.1016/S0076-6879(84)05016-3
  locator: https://pubmed.ncbi.nlm.nih.gov/6727660/
access:
  class: public-locator
```

**Use in this slice:** establishes an identifiable laboratory-method reference for catalase activity measurement. This fixture does not reproduce the article text.

### Source 2

```yaml
id: src:romantsev-prozorovskii-1984-catalase-thermostability
type: source
status: draft
source:
  kind: primary-research
  authors:
    - F. E. Romantsev
    - V. N. Prozorovskii
  title: Proteolytic resistance and thermostability of catalase and histidine decarboxylase from Micrococcus sp.
  published: 1984-04
  pmid: 6722300
  locator: https://pubmed.ncbi.nlm.nih.gov/6722300/
access:
  class: public-locator
limitations:
  - article language differs from this authored fixture
  - organism-specific result
```

### Source 3

```yaml
id: src:mueller-2003-fluorescent-catalase-assay
type: source
status: draft
source:
  kind: primary-research
  title: Determination of the activity of catalase using a europium(III)-tetracycline-derived fluorescent substrate
  published: 2003
  pmid: 12895476
  locator: https://pubmed.ncbi.nlm.nih.gov/12895476/
access:
  class: public-locator
limitations:
  - assay-specific optimum
```

## Evidence records

### Evidence 1 — organism-specific heat and pH result

```yaml
id: evidence:en:micrococcus-catalase-retained-activity-near-optimal-ph
type: evidence
status: draft
source: src:romantsev-prozorovskii-1984-catalase-thermostability
locator:
  kind: abstract
  value: PubMed abstract
relations:
  - type: supports
    target: claim:en:catalase-temperature-response-depends-on-ph-and-source
```

**Evidence description:** The abstract reports that the studied catalase retained substantial activity after a short high-temperature treatment only near the enzyme preparation’s reported optimal pH.

**Appraisal:** relevant to interaction between pH and thermal stability, but limited to a particular microbial enzyme preparation and protocol.

### Evidence 2 — assay-specific neutral-pH optimum

```yaml
id: evidence:en:fluorescent-assay-reported-neutral-ph-optimum
type: evidence
status: draft
source: src:mueller-2003-fluorescent-catalase-assay
locator:
  kind: abstract
  value: PubMed abstract
relations:
  - type: supports
    target: claim:en:catalase-optimum-is-not-universal-without-assay-scope
```

**Evidence description:** The abstract reports best performance near neutral pH for the described fluorescent catalase assay.

**Appraisal:** supports a scoped assay result, not a universal optimum for every catalase source or measurement method.

### Evidence 3 — synthetic classroom observation fixture

```yaml
id: evidence:en:synthetic-classroom-foam-observation
type: evidence
status: draft
source: src:synthetic-classroom-catalase-log
access:
  class: open
locator:
  kind: observation-log
  value: fixture-run-001
measurement:
  quantity: foam-height-after-60-seconds
  values:
    - condition: chilled
      value: 1.8
      unit: cm
    - condition: room-temperature
      value: 4.1
      unit: cm
    - condition: heated
      value: 0.7
      unit: cm
  repeats: 1
relations:
  - type: illustrates
    target: concept:en:enzyme-activity
```

**Important:** This is synthetic data created only to test the contract. Foam height is an indirect proxy affected by gas capture, tissue geometry, reagent mixing, and measurement error. It must not support a real scientific conclusion.

## Claim records

### Claim 1

```yaml
id: claim:en:catalase-temperature-response-depends-on-ph-and-source
type: claim
status: draft
claim:
  kind: descriptive
  statement: Reported catalase thermal behavior depends on the enzyme source, pH, exposure duration, and assay protocol.
  scope:
    evidence_set: sources-in-this-slice
  confidence: plausible
```

**Rationale:** The sources describe different preparations and methods. The claim is intentionally comparative and does not assert one universal optimum.

### Claim 2

```yaml
id: claim:en:catalase-optimum-is-not-universal-without-assay-scope
type: claim
status: draft
claim:
  kind: methodological
  statement: A reported optimum pH or temperature for catalase should be interpreted together with the enzyme source and assay definition.
  confidence: well-supported
```

**Limitation:** confidence applies to the methodological caution, not to a specific optimum value.

### Claim 3

```yaml
id: claim:en:classroom-foam-is-a-reaction-proxy
type: claim
status: draft
claim:
  kind: methodological
  statement: Foam height in a tissue-hydrogen-peroxide classroom assay is an indirect reaction proxy rather than a direct measurement of purified catalase kinetics.
  confidence: plausible
```

**Evidence status:** requires domain and methodological review before promotion. The synthetic observation does not establish this claim by itself.

## Concept records

```yaml
id: concept:en:catalase
type: concept
status: draft
definition: An enzyme that catalyzes decomposition of hydrogen peroxide, with behavior dependent on molecular source and conditions.
```

```yaml
id: concept:en:enzyme-activity
type: concept
status: draft
definition: A measured rate or proxy for enzyme-catalyzed transformation under defined conditions.
relations:
  - type: measured-by
    target: model:en:catalase-assay-observation-model
```

## Model record

```yaml
id: model:en:catalase-assay-observation-model
type: model
status: draft
purpose: Separate catalytic activity from what a classroom observer records.
inputs:
  - enzyme source and amount
  - hydrogen-peroxide concentration
  - pH
  - temperature and exposure duration
  - mixing and vessel geometry
latent_variable:
  - catalytic reaction rate
observed_proxies:
  - oxygen evolution
  - absorbance change
  - fluorescence change
  - foam height
assumptions:
  - proxy changes monotonically with reaction over the selected range
failure_modes:
  - gas escape
  - foam instability
  - unequal tissue surface area
  - substrate depletion
  - temperature drift
```

## Argument block

```yaml
argument:
  mode: inductive
  premises:
    - claim:en:catalase-temperature-response-depends-on-ph-and-source
    - claim:en:catalase-optimum-is-not-universal-without-assay-scope
  assumptions:
    - source abstracts accurately summarize their reported assays
  conclusion: claim:en:classroom-results-require-scoped-interpretation
  vulnerabilities:
    - limited source set
    - no direct comparison using one standardized preparation
```

## Synthesis

The reference sources support a cautious conclusion: catalase activity and stability are condition-dependent, but values reported as “optimal” belong to particular enzyme preparations and assay methods. A classroom tissue experiment can illustrate condition sensitivity, yet a foam measurement is a proxy with several uncontrolled influences. Therefore, the responsible synthesis is not “catalase works best at one universal temperature and pH,” but “interpret every observed optimum within its source, protocol, measurement, and enzyme context.”

## Challenging and limiting material

- Different catalases and assay systems may show different profiles.
- The fixture does not include a systematic review.
- Synthetic classroom data cannot establish external factual claims.
- Published abstracts are not substitutes for full methodological review.
- Temperature can alter both immediate reaction rate and longer-term enzyme stability; these are different questions.

## Open questions

- Which minimal metadata is required to compare classroom catalase assays reproducibly?
- Should observation protocol be a model, source, or separate method entity in a later contract?
- How should Atlas distinguish instantaneous temperature-rate effects from irreversible thermal inactivation?

## Revision triggers

- full-text source review changes the interpretation;
- a standardized comparative dataset is added;
- the contract adds a separate protocol or method entity;
- a reviewer finds that one claim is still compound or insufficiently scoped.

## Review matrix

| Review | Status | Reason |
|---|---|---|
| structural | pending | bundled fixture not yet machine-validated |
| source | pending | bibliographic and locator verification required |
| editorial | pending | claim atomicity review required |
| domain | pending | biochemistry review required |
| methodological | pending | assay and proxy interpretation review required |
| reproducibility | not-applicable | synthetic values are not a claimed analysis |
