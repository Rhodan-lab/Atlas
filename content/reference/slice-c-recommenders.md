# Reference Slice C — Recommendation Systems, Exposure, and User Choice

## Slice metadata

```yaml
contract: atlas-content/0.1
id: synthesis:en:recommender-exposure-and-autonomy-slice
work: work:recommender-exposure-and-autonomy-slice
type: synthesis
title: Recommendation systems can shape exposure, but policy conclusions require explicit values
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
```

## Question record

```yaml
id: question:en:how-do-recommenders-influence-user-choice
type: question
status: draft
state: contested
```

**Question:** How can recommendation systems influence what users encounter, and which transparency or choice requirements are justified by the evidence and stated values?

## Source records

### Source 1 — Facebook observational study

```yaml
id: src:bakshy-messing-adamic-2015-diverse-news
type: source
status: draft
source:
  kind: primary-research
  authors:
    - Eytan Bakshy
    - Solomon Messing
    - Lada A. Adamic
  title: Exposure to ideologically diverse news and opinion on Facebook
  container: Science
  volume: 348
  issue: 6239
  pages: 1130-1132
  published: 2015-06-05
  doi: 10.1126/science.aaa1160
  locator: https://doi.org/10.1126/science.aaa1160
access:
  class: public-locator
conflicts:
  - authors included Facebook employees and the work used platform-controlled data
```

### Source 2 — Twitter randomized experiment

```yaml
id: src:huszar-et-al-2022-algorithmic-amplification
type: source
status: draft
source:
  kind: primary-research
  authors:
    - Ferenc Huszar
    - Sofia Ira Ktena
    - Conor O'Brien
    - Luca Belli
    - Andrew Schlaikjer
    - Moritz Hardt
  title: Algorithmic amplification of politics on Twitter
  container: Proceedings of the National Academy of Sciences
  volume: 119
  issue: 1
  article: e2025334119
  published: 2022-01-04
  doi: 10.1073/pnas.2025334119
  locator: https://pubmed.ncbi.nlm.nih.gov/34934011/
access:
  class: open
conflicts:
  - several authors worked on Twitter's machine-learning ethics and accountability team
```

### Source 3 — European Union regulation

```yaml
id: src:eu-2022-digital-services-act
type: source
status: draft
source:
  kind: legal-policy-document
  issuing_body: European Parliament and Council of the European Union
  title: Regulation (EU) 2022/2065 — Digital Services Act
  published: 2022-10-27
  locator: https://eur-lex.europa.eu/eli/reg/2022/2065/oj
  version: official-journal
access:
  class: open
```

## Evidence records

### Evidence 1 — observational exposure pathway

```yaml
id: evidence:en:facebook-study-network-ranking-and-click-path
type: evidence
status: draft
source: src:bakshy-messing-adamic-2015-diverse-news
locator:
  kind: abstract
  value: article abstract and summary
relations:
  - type: supports
    target: claim:en:platform-exposure-reflects-network-ranking-and-user-selection
```

**Description:** The study examined deidentified behavior of 10.1 million U.S. Facebook users who self-reported political affiliation and compared potential cross-cutting exposure from social networks, content encountered after News Feed ranking, and clicked content. The authors reported that user choices played a stronger role than ranking in limiting cross-cutting exposure in that setting.

**Limitations:** observational platform-specific design, selected user population, historical product state, platform-controlled data, and limited independent reproducibility.

### Evidence 2 — randomized comparison of ranked and chronological feeds

```yaml
id: evidence:en:twitter-randomized-amplification-comparison
type: evidence
status: draft
source: src:huszar-et-al-2022-algorithmic-amplification
locator:
  kind: abstract
  value: article abstract
relations:
  - type: supports
    target: claim:en:ranking-can-change-relative-political-exposure
```

**Description:** The study used a long-running randomized control group of nearly two million daily active accounts receiving a reverse-chronological feed and compared amplification of political content under algorithmic ranking.

**Limitations:** platform- and period-specific outcomes, operational definitions of political groups and amplification, and author employment connections.

### Evidence 3 — transparency and user-option requirements

```yaml
id: evidence:en:dsa-recommender-transparency-and-choice-rules
type: evidence
status: draft
source: src:eu-2022-digital-services-act
locator:
  kind: section
  value: Articles 27 and 38
relations:
  - type: contextualizes
    target: claim:en:transparency-and-user-control-are-recognized-governance-responses
```

**Description:** Article 27 requires online platforms using recommender systems to describe main parameters and user influence options in clear terms. Article 38 adds a non-profiling recommender option requirement for very large online platforms and search engines within its scope.

**Interpretation limit:** a legal requirement demonstrates a governance choice, not empirical proof that the requirement fully protects autonomy or produces better outcomes.

## Claim records

### Claim 1

```yaml
id: claim:en:platform-exposure-reflects-network-ranking-and-user-selection
type: claim
status: draft
claim:
  kind: descriptive
  statement: In the studied Facebook setting, cross-cutting political-news exposure reflected the composition of social connections, algorithmic ranking, and users' click choices.
  scope:
    platform: Facebook
    population: U.S. users self-reporting political affiliation
    period: study period reported in the 2015 article
  confidence: well-supported
```

### Claim 2

```yaml
id: claim:en:ranking-can-change-relative-political-exposure
type: claim
status: draft
claim:
  kind: causal
  statement: In the Twitter experiment, algorithmic timeline ranking changed the relative amplification of political content compared with a reverse-chronological control feed.
  scope:
    platform: Twitter
    design: randomized platform experiment
    outcome: relative algorithmic amplification as defined by the study
  confidence: well-supported
```

### Claim 3

```yaml
id: claim:en:recommender-effects-are-context-dependent
type: claim
status: draft
claim:
  kind: interpretive
  statement: The direction and magnitude of recommender-system effects should not be generalized across platforms, populations, outcomes, and time periods without additional evidence.
  confidence: well-supported
```

### Claim 4

```yaml
id: claim:en:transparency-and-user-control-are-recognized-governance-responses
type: claim
status: draft
claim:
  kind: descriptive
  statement: Recommender transparency and user influence or non-profiling options are recognized governance responses in the European Union Digital Services Act.
  scope:
    jurisdiction: European Union
    law: Regulation EU 2022/2065
  confidence: strongly-supported
```

### Claim 5 — normative

```yaml
id: claim:en:users-should-receive-meaningful-recommender-explanation-and-choice
type: claim
status: draft
claim:
  kind: normative
  statement: Users should receive understandable information about major recommender parameters and meaningful options to influence or avoid profiling-based ranking where feasible.
  confidence: plausible
values:
  - autonomy
  - procedural fairness
  - accountability
  - accessibility
```

This claim is not logically produced by empirical evidence alone. It depends on stated values and must be ethically reviewed.

## Concept records

```yaml
id: concept:en:recommender-system
type: concept
status: draft
definition: A system that selects or orders items for a recipient using specified signals, objectives, and constraints.
```

```yaml
id: concept:en:exposure
type: concept
status: draft
definition: The opportunity for a user to encounter information, distinguished from attention, engagement, belief, and behavior.
```

```yaml
id: concept:en:user-autonomy
type: concept
status: draft
definition: A contested normative concept concerning meaningful agency, understanding, and freedom from unacceptable manipulation or constraint.
```

## Model record

```yaml
id: model:en:recommender-exposure-loop
type: model
status: draft
purpose: Separate stages that can influence observed exposure and action.
stages:
  - available content
  - social or subscription network
  - eligibility and moderation
  - ranking
  - presentation
  - user attention
  - selection or click
  - feedback signals used by later ranking
assumptions:
  - stages can be analytically distinguished
  - platform logs imperfectly represent human understanding or preference
failure_modes:
  - hidden platform interventions
  - changing objectives
  - multiple devices or accounts
  - unobserved offline influences
  - feedback between user adaptation and ranking
```

## Argument blocks

### Empirical argument

```yaml
argument:
  mode: inductive
  premises:
    - claim:en:platform-exposure-reflects-network-ranking-and-user-selection
    - claim:en:ranking-can-change-relative-political-exposure
  conclusion: claim:en:recommender-systems-can-shape-information-exposure
  vulnerabilities:
    - platform specificity
    - outcome-definition differences
    - historical product changes
```

### Normative argument

```yaml
argument:
  mode: normative
  premises:
    - claim:en:recommender-systems-can-shape-information-exposure
    - claim:en:users-often-cannot-observe-ranking-logic-directly
  values:
    - autonomy
    - accountability
  conclusion: claim:en:users-should-receive-meaningful-recommender-explanation-and-choice
  alternatives:
    - independent auditing without individual controls
    - default chronological feed
    - outcome-based safety requirements
```

## Synthesis

The evidence supports a bounded conclusion: recommendation and ranking systems can change which political content users encounter, but the pathway also includes social networks, available content, user selection, platform rules, and feedback from prior behavior. The two platform studies use different designs and outcomes, so they should not be merged into one universal effect estimate. The Digital Services Act shows that transparency and user-choice mechanisms are recognized regulatory responses, while not proving that those measures are sufficient.

A mature synthesis therefore distinguishes three layers:

1. **Empirical:** ranking can affect exposure under specific platform conditions.
2. **Interpretive:** effect direction and size are context-dependent and entangled with user and network behavior.
3. **Normative:** transparency and meaningful choice may be justified by autonomy and accountability values, but alternative governance designs remain contestable.

## Challenging material and disagreement

- User choice can matter more than ranking for some measured outcomes.
- Platform experiments may not generalize to other platforms or later product versions.
- Transparency can overwhelm users or reveal little about actual system behavior.
- A non-profiling option may not eliminate other ranking or selection effects.
- Greater user control can conflict with safety, usability, or collective-risk objectives.
- Employment and platform-data access create conflicts that require disclosure and independent scrutiny.

## Open questions

- Which explanations are understandable and actionable rather than merely formal compliance?
- How should autonomy be operationalized without reducing it to click behavior?
- What outcomes should recommender audits measure?
- How should Atlas represent legal claims whose interpretation changes through guidance or case law?
- When should a policy recommendation be represented as a normative claim versus a synthesis conclusion?

## Revision triggers

- corrected or retracted study findings;
- major platform-design changes affecting applicability;
- legal amendment or authoritative interpretation of the DSA;
- stronger independent replication evidence;
- ontology change introducing a first-class policy or argument entity.

## Review matrix

| Review | Status | Reason |
|---|---|---|
| structural | pending | bundled fixture not machine-validated |
| source | pending | article and legal locators require verification |
| editorial | pending | empirical and normative separation requires review |
| domain | pending | recommender-systems and political communication review required |
| methodological | pending | study-design and generalization review required |
| ethical | pending | autonomy and governance values require review |
| conflict review | pending | platform employment and data-access limits must be assessed |
