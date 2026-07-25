# Initial Relation Vocabulary

## Status

Provisional controlled vocabulary for Phase 0. Each relation has one direction and meaning. New types require examples, counterexamples, allowed entity pairs, and migration analysis.

## General rules

- The subject is the entity containing the relation.
- The `target` is the object of the relation.
- Direction is defined here and is not inferred from wording alone.
- Inverse relations may be generated for navigation but are not independently authored unless listed.
- Symmetric relations are explicitly marked.
- A relation does not replace explanatory prose or evidence appraisal.
- Initial pairs use only canonical entity types: source, evidence, claim, concept, model, question, synthesis, and revisioned versions of those entities.

## Structural relations

### `part-of`

**Meaning:** the subject is a constituent or bounded component of the target.

**Initial pairs:** concept → concept; model → model.

**Counterexample:** a topic merely discussed near another topic.

### `instance-of`

**Meaning:** the subject is a concrete or narrower instance of the target category.

**Initial pairs:** concept → concept; model → concept.

**Counterexample:** two concepts that are only similar.

### `prerequisite-of`

**Meaning:** understanding the subject is materially required to understand or use the target at the stated level.

**Initial pairs:** concept → concept; model → model.

**Counterexample:** the subject is only helpful background.

## Epistemic relations

### `supports`

**Meaning:** the subject provides evidence that increases reason to accept the target claim within a stated scope.

**Initial pairs:** evidence → claim.

**Required note:** why the evidence is relevant and what limitations remain.

### `challenges`

**Meaning:** the subject weakens, narrows, or raises a material problem for the target claim without necessarily asserting its direct opposite.

**Initial pairs:** evidence → claim; claim → claim.

### `contradicts`

**Meaning:** the subject and target cannot both hold under materially comparable definitions, scope, and conditions.

**Initial pairs:** claim ↔ claim.

**Symmetry:** semantically symmetric; one authored edge may generate the reverse view.

**Required check:** confirm the apparent conflict is not caused only by different scope, terminology, timeframe, or method.

### `contextualizes`

**Meaning:** the subject provides relevant background or interpretation but does not directly support or challenge the target.

**Initial pairs:** evidence → claim; concept → claim; source → synthesis.

### `illustrates`

**Meaning:** the subject is an example that makes the target easier to understand but is not sufficient evidence for it.

**Initial pairs:** evidence → concept; concept → concept.

### `motivates`

**Meaning:** the subject explains why the target question is worth investigating, without by itself answering the question.

**Initial pairs:** source → question; evidence → question; claim → question; concept → question.

### `replicates`

**Meaning:** the subject independently reproduces a material result represented by the target evidence or claim.

**Initial pairs:** evidence → evidence; evidence → claim.

### `fails-to-replicate`

**Meaning:** the subject reports a relevant attempt that did not reproduce the target result under stated conditions.

**Initial pairs:** evidence → evidence; evidence → claim.

## Explanatory and inferential relations

### `explains`

**Meaning:** the subject provides a mechanism, account, or framework that makes the target intelligible.

**Initial pairs:** concept → concept; model → claim; model → concept; claim → concept.

**Counterexample:** simple correlation or chronological order.

### `derived-from`

**Meaning:** the subject was produced through a stated transformation, inference, calculation, or integration using the target.

**Initial pairs:** claim → model; synthesis → claim; evidence → source; evidence → model.

**Required note:** derivation method or transformation reference.

### `refines`

**Meaning:** the subject makes the target more precise, scoped, or detailed while preserving a meaningful core.

**Initial pairs:** claim → claim; concept → concept; model → model; question → question; synthesis → synthesis.

### `supersedes`

**Meaning:** the subject replaces the target as the current item for the stated purpose while preserving the target for history.

**Initial pairs:** source → source; evidence → evidence; claim → claim; concept → concept; model → model; question → question; synthesis → synthesis.

**Required note:** reason and effective revision.

## Causal and empirical relations

### `causes`

**Meaning:** the subject contributes causally to the target under stated conditions and supported reasoning.

**Initial pairs:** concept → concept; claim → claim.

**Required caution:** this relation requires stronger justification than temporal order or association.

### `correlates-with`

**Meaning:** the subject and target vary together under a stated measurement and scope without asserting causation.

**Initial pairs:** concept ↔ concept; claim ↔ claim.

**Symmetry:** semantically symmetric.

### `measured-by`

**Meaning:** the subject is operationalized, estimated, or observed using the target model or measurement representation.

**Initial pairs:** concept → model; claim → model.

### `applies-to`

**Meaning:** the subject can be validly used, interpreted, or instantiated in the target context under stated conditions.

**Initial pairs:** model → concept; concept → concept; synthesis → question.

### `analogous-to`

**Meaning:** the subject and target share a stated structural similarity useful for understanding.

**Initial pairs:** concept ↔ concept; model ↔ model.

**Symmetry:** semantically symmetric.

**Required caution:** analogy does not provide evidence that mechanisms or conclusions transfer.

## Relations not yet accepted

The following tempting labels are not accepted without further definition:

- `related-to`
- `associated-with`
- `depends-on`
- `influences`
- `uses`
- `contains`
- `similar-to`

They are too broad or overlap with existing semantics. Authors should choose a precise accepted relation or explain the connection in prose until the vocabulary is revised.

## Compatibility validation

A validator should reject:

- unknown relation types;
- disallowed subject-target entity pairs;
- self-relations unless explicitly permitted;
- duplicate authored edges with the same semantic key;
- missing notes for relations that require rationale;
- reversed directions such as a claim `supports` evidence;
- `causes` where the rationale establishes only correlation;
- `analogous-to` used as supporting evidence;
- `illustrates` treated as sufficient support;
- `motivates` treated as an answer to a question.

## Vocabulary revision procedure

To add or change a relation:

1. identify a real fixture that existing relations cannot express;
2. define subject, target, direction, and meaning;
3. provide positive examples and counterexamples;
4. identify overlap with current types;
5. define inverse or symmetry behavior;
6. specify validation rules;
7. analyze migration impact;
8. update fixtures, contracts, and affected syntheses;
9. record the decision in the decision register or an ADR.
