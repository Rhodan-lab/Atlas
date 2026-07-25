# Evidence and Editorial Policy

## Status

Draft governance policy for Phase 0. It defines how Atlas distinguishes authored material, evidence, review, uncertainty, disagreement, and revision.

## Editorial objective

Atlas must help a reader judge knowledge rather than merely consume it. That requires visible provenance, scope, uncertainty, disagreement, and review history.

The system must avoid two opposite failures:

- presenting unreviewed notes with the authority of established knowledge;
- hiding real uncertainty behind vague disclaimers that cannot be inspected.

## Item lifecycle

Every canonical knowledge item has an explicit status.

### `draft`

The item is being authored or modeled. It may be incomplete, weakly sourced, or structurally unstable.

Rules:

- all newly created modules begin as `draft`;
- drafts must not be described as scientifically reviewed;
- missing evidence and unresolved questions remain visible;
- derived views clearly distinguish drafts.

### `in-review`

The item is undergoing one or more defined review types.

Rules:

- review scope and reviewer identity or role are recorded;
- material changes return the affected portion to review;
- unresolved review comments are not silently discarded.

### `reviewed`

The item has passed the required review for its type, version, and scope.

Reviewed means adequately supported, scoped, and presented under the current policy. It does **not** mean permanently or universally true.

Required:

- review date;
- review types;
- reviewer or review authority;
- exact version reviewed;
- evidence and limitations checked;
- remaining uncertainty recorded.

### `contested`

Credible, materially different interpretations or findings remain unresolved.

Rules:

- competing claims and evidence remain visible;
- the source of disagreement is explained;
- contested status is not hidden as a defect;
- a synthesis may still be reviewed if it represents the dispute honestly.

### `deprecated`

The item is no longer recommended as current because it is obsolete, misleading, duplicated, or replaced.

Rules:

- retain it for provenance;
- link to the replacement when available;
- record reason and effective date;
- identify dependent items requiring review.

### `retracted`

The item contains a serious error or integrity problem and must not support current conclusions.

Rules:

- retain the historical record;
- state the reason clearly;
- propagate review flags to dependent claims and syntheses.

## Review types

Review is not one universal action. Atlas distinguishes:

- **structural review** — contract completeness, identifiers, links, and syntax;
- **editorial review** — clarity, scope, terminology, and faithful summarization;
- **source review** — citation identity, locator accuracy, and contextual use;
- **domain review** — subject-matter accuracy and important omissions;
- **methodological review** — design, measurement, statistics, and inference;
- **reproducibility review** — calculations, transformations, or code can be repeated;
- **ethical review** — risks, affected groups, consent, power, and responsible use where relevant.

An item records which review types it has passed. One review type does not imply the others.

## Epistemic relation roles

The governed relation vocabulary is defined in [`10-relation-vocabulary.md`](10-relation-vocabulary.md). Important editorial distinctions include:

### Evidence to claim

- `supports` — increases reason to accept the target claim within a defined scope;
- `challenges` — weakens, narrows, or raises a material problem for the target claim;
- `contextualizes` — adds relevant background without directly testing the claim;
- `replicates` — independently reproduces a material result;
- `fails-to-replicate` — records a relevant non-replication.

### Claim to claim

- `challenges` — one claim weakens or limits another without being its direct opposite;
- `contradicts` — two claims cannot both hold under comparable definitions, scope, and conditions;
- `refines` — one claim makes another more precise while preserving a meaningful core.

### Evidence or concept to concept

- `illustrates` — provides an example useful for understanding but not sufficient proof.

### Source, evidence, claim, or concept to question

- `motivates` — explains why the question is worth investigating without answering it.

These relations are authored judgments. Their direction, rationale, and compatibility can themselves be reviewed and revised.

## Source classification

Source type is descriptive, not an automatic quality score. Initial types may include:

- primary research;
- systematic review or meta-analysis;
- dataset;
- standard or official specification;
- legal or policy document;
- archival record;
- textbook or reference work;
- expert commentary;
- journalism;
- interview or testimony;
- user observation;
- model or simulation output;
- generated analysis.

Atlas must not infer truth solely from type, prestige, or citation count.

## Evidence appraisal

Evidence appraisal is structured but not reduced to one universal number. Relevant dimensions include:

- directness to the claim;
- methodological fit;
- measurement validity;
- sample or observation coverage;
- independence from other evidence;
- reproducibility;
- recency where time sensitivity matters;
- consistency with comparable evidence;
- risk of bias or conflict of interest;
- applicability to the stated scope;
- uncertainty and missing data.

Each appraisal records a concise rationale. Numeric measures may be used inside domain-specific models, but Atlas does not present one global truth score.

## Confidence language

Claims and syntheses may use qualitative confidence labels only with a written rationale:

- `uncertain`
- `plausible`
- `well-supported`
- `strongly-supported`

These labels describe the current evidence state for a defined scope. They are not permanent properties.

Where a domain has accepted statistical, formal, or measurement uncertainty, preserve those measures rather than replacing them with a vague label.

## Claim requirements

A reviewed empirical claim includes:

- statement;
- claim kind;
- scope and qualifiers;
- applicable definitions;
- supporting and challenging evidence;
- confidence rationale;
- limitations;
- review record;
- revision history.

A normative claim additionally identifies the values or ethical principles involved. Empirical evidence may inform a recommendation but cannot alone logically determine what ought to be done.

A prediction states its time horizon, conditions, model or reasoning basis, and evaluation criterion.

## Contradiction handling

Atlas does not merge conflicting claims into an artificial compromise.

When credible conflict appears:

1. confirm that terms, populations, timeframes, and methods are comparable;
2. preserve each claim and its evidence;
3. record the appropriate `contradicts` or `challenges` relation;
4. identify possible reasons for divergence;
5. mark affected syntheses for review;
6. update synthesis only after the disagreement is represented honestly.

## Revision and dependency impact

A material revision should trigger review of dependent items when it changes:

- a central definition;
- the scope or polarity of a claim;
- evidence validity;
- a model assumption or parameter;
- the status of a source;
- a conclusion used in a synthesis.

Automated dependency detection may assist later, but final editorial status remains explicit and reviewable.

## AI-assisted work

AI-generated extraction, classification, summaries, relations, or syntheses are provisional transformations.

Requirements:

- generated material begins as `draft`;
- the model and prompt or procedure are recorded when practical;
- source locators are independently checked;
- AI output cannot create reviewed status;
- generated claims do not cite the AI as evidence when the underlying source is available;
- uncertainty and disagreement are not silently normalized away.

## Minimum review gate for publication

A module is not eligible for a reviewed public view unless:

- all material factual claims meet their evidence requirements;
- citations and locators have been checked;
- scope and limitations are visible;
- unresolved credible disagreement is represented;
- required review types are recorded;
- the reviewed version is immutable or reproducibly versioned;
- later changes return affected material to the appropriate review state.
