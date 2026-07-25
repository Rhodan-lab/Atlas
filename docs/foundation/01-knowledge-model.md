# Canonical Knowledge Model

## Status

Draft ontology for Phase 0. It defines the meaning Atlas must preserve before storage schemas, APIs, or programming-language models are finalized.

## Why a concept graph is not enough

A graph containing only concepts, broad source references, and edges cannot reliably answer:

- which exact statement a source supports;
- which passage, observation, or measurement counts as evidence;
- whether a statement is disputed or limited in scope;
- which assumptions belong to a model;
- how a synthesis was formed;
- what must be reconsidered when knowledge changes.

Atlas therefore requires distinct knowledge units. They may share storage mechanisms later, but they must not be collapsed semantically.

## Canonical entities

### 1. Source

A source is an identifiable origin of information: a paper, book, dataset, interview, standard, webpage, experiment record, archival document, or other citable object.

A source record preserves:

- stable identity;
- title or human-readable label;
- creator or issuing body when known;
- publication or observation date when known;
- locator and access information;
- source type;
- edition or version when relevant.

A source does not automatically support a claim. Support is established through evidence.

### 2. Evidence

Evidence identifies the specific material taken from a source and the context in which it is used.

Examples include:

- a page range or limited excerpt;
- a table, figure, or dataset slice;
- an experimental observation;
- a measured result;
- an interview segment;
- a reproducible calculation or model output.

Evidence records preserve:

- source identity;
- precise locator or observation context;
- excerpt summary, observation, or structured value when appropriate;
- surrounding context needed to avoid distortion;
- collection, extraction, or transformation method;
- limitations;
- explicit relation to the claims or questions for which it is relevant.

### 3. Claim

A claim is the smallest meaningful statement that can be evaluated, qualified, supported, challenged, revised, or deprecated.

A good claim is:

- clear enough to inspect independently;
- scoped by population, place, time, conditions, or definitions where needed;
- separated from its supporting argument;
- not overloaded with unrelated assertions;
- linked to evidence or explicitly marked as an assumption, interpretation, value judgment, prediction, or open hypothesis.

Claim kinds may include factual, causal, definitional, methodological, interpretive, predictive, normative, and hypothetical. These kinds do not require identical evidence or review.

### 4. Concept

A concept is an explanatory unit that organizes meaning around a term, mechanism, pattern, principle, or phenomenon.

A concept may link to:

- a concise definition;
- boundaries and common confusions;
- prerequisite concepts;
- important claims;
- examples and counterexamples;
- models;
- applications;
- disputes and open questions.

A concept does not own truth. It provides structure around individually traceable claims.

### 5. Relation

A relation is a typed, directed connection between compatible entities. Its direction, meaning, allowed entity pairs, and validation rules must be explicit.

The single authoritative provisional vocabulary is [`10-relation-vocabulary.md`](10-relation-vocabulary.md). Other foundation documents may show relation examples but must not maintain independent competing lists.

New relation types require:

- a real fixture that existing relations cannot express;
- definition and direction;
- allowed subject-target pairs;
- examples and counterexamples;
- inverse or symmetry behavior;
- validation requirements;
- overlap analysis;
- migration consequences.

### 6. Model

A model is a structured representation used to explain, calculate, simulate, classify, or predict.

A model record distinguishes:

- purpose;
- inputs and outputs;
- assumptions;
- scope of validity;
- mechanism or formal structure;
- calibration or parameter sources;
- validation evidence;
- known failure modes;
- claims derived from using the model.

Equations, diagrams, statistical models, simulations, conceptual frameworks, and taxonomies can all be models, but their validation requirements differ.

### 7. Question

A question records a knowledge need rather than pretending the answer is already settled.

Question states may include:

- open;
- partially answered;
- blocked by missing evidence;
- contested;
- resolved for a stated scope;
- superseded by a better question.

Questions connect research activity, concepts, claims, models, evidence, and syntheses.

### 8. Synthesis

A synthesis is a reasoned integration of claims, evidence, models, and unresolved tensions for a defined question and scope.

A synthesis exposes:

- the question and intended audience;
- included and excluded scope;
- supporting and challenging claims;
- evidence selection rationale;
- models and assumptions used;
- disagreements and uncertainty;
- conclusions;
- open questions;
- revision history and trigger conditions.

A synthesis is derived knowledge. It must never become an untraceable replacement for its supporting structure.

### 9. Revision

A revision records meaningful change to an authoritative knowledge unit.

It states:

- what changed;
- why it changed;
- evidence or decision that triggered the change;
- who or what performed the change;
- review status;
- which earlier version it supersedes;
- known downstream items that may require re-evaluation.

Version history is part of knowledge provenance, not merely repository history.

## Core invariants

1. Every canonical entity has a stable identifier not derived solely from its title or file order.
2. Generated numeric IDs may exist internally but are never the sole durable identity.
3. Evidence always points to a source and a precise locator or observation context.
4. Reviewed factual claims have evidence or an explicit reason direct evidence is unavailable.
5. Claims preserve scope and qualifiers; summaries do not silently remove them.
6. Support, challenge, and contradiction occur primarily at claim level, not only concept level.
7. Every relation type has one documented semantic meaning and direction.
8. A synthesis identifies all claims that materially support or challenge its conclusion.
9. Models expose assumptions, scope, and failure modes.
10. Revisions preserve prior versions and reasons for change.
11. Generated files can be deleted and rebuilt without losing authored meaning.
12. No interface or implementation language may introduce hidden canonical fields.
13. Review status belongs to an entity revision, not merely to a folder or interface view.
14. Credible disagreement remains visible until it is resolved for an explicit scope.

## Identity model

Canonical IDs should be human-inspectable and stable, for example:

```text
src:doe-2025-system-models
evidence:doe-2025-delay-result
claim:feedback-loops-can-amplify-change
concept:feedback-loop
model:basic-stock-flow
question:when-does-local-feedback-create-instability
synthesis:feedback-and-stability-v1
```

Titles may change without changing identity. When meaning changes so substantially that continuity would mislead, create a new entity and connect it through the accepted revision or refinement semantics.

## Layer separation

The canonical flow is not strictly linear, but the distinctions remain visible:

```text
Source → Evidence → Claim → Concept or Model → Synthesis
                    ↘          ↑             ↗
                       Question
```

Concepts organize claims. Models transform assumptions and inputs. Questions expose needs and gaps. Syntheses integrate the current state. None is a universal replacement for the others.

## Open ontology tests

Phase 0 must still test:

- the minimum required fields for each entity type;
- how evidence fragments are stored without violating copyright or access restrictions;
- how qualitative and quantitative evidence share a common core;
- whether argument requires its own entity type;
- how normative claims remain distinct from empirical claims;
- which relation types are essential for the reference corpus;
- how review applies when a synthesis depends on mixed-status material;
- how multilingual versions share identity and revision history.
