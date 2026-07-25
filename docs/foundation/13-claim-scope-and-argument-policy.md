# Claim Scope and Argument Policy

## Status

**Accepted for `atlas-content/0.1`.** Argument remains a structured authored block rather than a new canonical entity until fixtures demonstrate a need for independent identity and lifecycle.

## Claim granularity decision

A claim is atomic when a reviewer can reasonably evaluate its truth, scope, evidence, and revision as one unit.

Atomic does not mean grammatically short. It means the statement does not combine assertions that could differ in:

- evidence;
- confidence;
- scope;
- lifecycle status;
- revision trigger;
- contradiction relationship.

## Split test

Split a candidate statement when any of these questions has different answers for its clauses:

1. Could one clause be supported while another is unsupported?
2. Could one clause be true in a narrower scope?
3. Could credible evidence contradict only one clause?
4. Would a revision alter only part of the statement?
5. Do the clauses use different claim kinds?
6. Does one clause describe evidence while another interprets it?

Example requiring separation:

> Higher temperature increased the observed catalase reaction and therefore heat always improves enzyme activity.

This combines an observation, an interpretation, and an overgeneralized universal claim. They require separate records.

## Claim statement requirements

A claim statement should:

- assert one evaluable proposition;
- include material qualifiers;
- avoid citation prose inside the statement;
- avoid words such as “proves” unless the applicable logic genuinely warrants them;
- distinguish observation, association, causal inference, prediction, interpretation, and recommendation;
- remain understandable when shown outside its original page.

## Scope object

Claims use a structured scope where relevant:

```yaml
scope:
  population: potato tissue catalase preparation
  setting: classroom hydrogen-peroxide assay
  conditions:
    - equal sample mass
    - fixed hydrogen-peroxide concentration
  time: single experimental session
  exclusions:
    - purified catalase kinetics
```

Not every field is mandatory. Authors include dimensions that materially affect interpretation.

## Claim kinds

Initial controlled kinds:

- `observational` — describes what was observed or measured;
- `descriptive` — describes a pattern or property;
- `definitional` — states how a term is used;
- `correlational` — states association without causation;
- `causal` — states a causal contribution under conditions;
- `mechanistic` — states how a process produces an outcome;
- `methodological` — states how a method behaves or should be applied;
- `model-derived` — follows from a model and its assumptions;
- `predictive` — states a future or out-of-sample expectation;
- `interpretive` — offers a reasoned reading of evidence or meaning;
- `normative` — states what ought to be valued or done;
- `hypothetical` — proposes an explanation or possibility for testing.

A claim has one primary kind and may list secondary characteristics. Choosing a kind does not establish that the claim is valid.

## Arguments in `0.1`

An argument is represented as a structured block within a claim, question, or synthesis record:

```yaml
argument:
  mode: abductive
  premises:
    - claim:en:observed-delay-precedes-oscillation
    - claim:en:model-predicts-delay-instability
  assumptions:
    - claim:en:experimental-system-matches-model-scope
  conclusion: claim:en:delay-contributed-to-oscillation
  alternatives:
    - claim:en:measurement-noise-explains-pattern
```

Initial modes:

- `deductive`
- `inductive`
- `abductive`
- `causal`
- `analogical`
- `normative`

The argument block records reasoning structure but does not become an independent graph entity in `0.1`.

## Why argument is not yet a canonical entity

The reference corpus has not shown that arguments require:

- independent titles;
- independent review lifecycle;
- reuse across many syntheses;
- separate version identity;
- argument-to-argument relations.

Adding an entity before demonstrating those needs would increase ontology complexity. The decision must be reopened if vertical slices require independent argument identity or if embedding creates duplication.

## Premise requirements

- Premises reference claims, not raw source URLs.
- Evidence supports or challenges premise claims separately.
- Hidden assumptions are listed explicitly where material.
- Normative conclusions identify value premises.
- Model-derived arguments name the model and applicable assumptions.
- Analogical reasoning states which structure is shared and which properties do not transfer.

## Inference strength

An argument records a rationale appropriate to its mode. It does not use one universal validity score.

Possible fields:

```yaml
inference:
  status: provisional
  rationale: The model and observation agree, but alternative explanations were not independently excluded.
  vulnerabilities:
    - model mismatch
    - uncontrolled temperature variation
```

## Compound and linked claims

A readable concept or synthesis may present several claims together in prose, but each material claim keeps its own ID. Prose composition is not canonical claim merging.

A derived view may group claims by:

- shared scope;
- evidence set;
- model;
- question;
- argument;
- concept;
- disagreement cluster.

## Revision behavior

When a claim is split:

- retain the original claim as deprecated or superseded;
- create new claim IDs;
- record a split mapping;
- move evidence relations only after item-level review;
- flag dependent arguments and syntheses;
- do not automatically inherit reviewed status.

When claims are merged, the same provenance and review protections apply.

## Validation rules

A validator can detect structural problems but cannot fully determine semantic atomicity.

It should reject or flag:

- missing primary claim kind;
- causal language on a `correlational` claim without explanation;
- prediction without horizon or evaluation criterion;
- normative claim without value assumptions;
- argument conclusion not listed among material claims;
- premises referencing sources instead of claims;
- argument cycles without an explicit recursive or dialectical model;
- model-derived claim without model reference;
- a scope object that contradicts the written statement.

Editorial and domain review remain necessary for claim granularity and inference quality.
