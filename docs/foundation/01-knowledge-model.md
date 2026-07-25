# Canonical Knowledge Model

## Status

Draft ontology for Phase 0. It defines the meaning Atlas must preserve before storage schemas, APIs, or programming-language models are finalized.

## Why the current concept graph is insufficient

A graph containing only concepts, broad source references, and relations cannot reliably answer:

- which exact statement a source supports;
- which passage or observation counts as evidence;
- whether a statement is disputed or limited in scope;
- how a synthesis was formed;
- what must be reconsidered when a source, claim, or model changes.

Atlas therefore requires several distinct knowledge units. They may later share storage mechanisms, but they must not be collapsed semantically.

## Canonical entities

### 1. Source

A source is an identifiable origin of information: a paper, book, dataset, interview, standard, webpage, experiment record, archival document, or other citable object.

Required meaning:

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

- a page range or quoted passage;
- a table, figure, or dataset slice;
- an experimental observation;
- a measured result;
- an interview segment;
- a reproducible calculation.

Evidence records must preserve:

- source identity;
- precise locator;
- excerpt, observation, or structured value when legally and practically appropriate;
- surrounding context needed to avoid distortion;
- collection or extraction method;
- limitations;
- which claims the evidence supports, challenges, or merely contextualizes.

### 3. Claim

A claim is the smallest meaningful statement that can be evaluated, qualified, supported, challenged, revised, or deprecated.

A good claim is:

- clear enough to inspect independently;
- scoped by population, place, time, conditions, or definitions where needed;
- separated from its supporting argument;
- not overloaded with several unrelated assertions;
- linked to evidence or explicitly marked as an assumption, interpretation, or open hypothesis.

Claim kinds may include factual, causal, definitional, methodological, interpretive, predictive, normative, and hypothetical. These kinds must not be treated as if they require identical evidence.

### 4. Concept

A concept is an explanatory unit that organizes meaning around a term, mechanism, pattern, principle, or phenomenon.

A concept may contain or link to:

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

A relation is a typed, directed connection between compatible entities. Direction and meaning must be explicit.

The initial controlled relation set is intentionally small:

- `prerequisite-of`
- `part-of`
- `instance-of`
- `explains`
- `supports`
- `challenges`
- `contradicts`
- `refines`
- `causes`
- `correlates-with`
- `measured-by`
- `applies-to`
- `analogous-to`
- `derived-from`
- `supersedes`

New relation types require a definition, allowed entity pairs, direction, examples, counterexamples, and migration consequences.

### 6. Model

A model is a structured representation used to explain, calculate, simulate, classify, or predict.

A model record must distinguish:

- purpose;
- inputs and outputs;
- assumptions;
- scope of validity;
- mechanism or formal structure;
- calibration or parameter source;
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

Questions can connect research activity, concepts, claims, models, and syntheses.

### 8. Synthesis

A synthesis is a reasoned integration of claims, evidence, models, and unresolved tensions for a defined question and scope.

A synthesis must expose:

- the question and intended audience;
- included and excluded scope;
- supporting and challenging claims;
- evidence selection rationale;
- disagreements and uncertainty;
- conclusions;
- open questions;
- revision history.

A synthesis is derived knowledge. It must never become an untraceable replacement for its supporting structure.

### 9. Revision

A revision records meaningful change to an authoritative knowledge unit.

It must state:

- what changed;
- why it changed;
- evidence or decision that triggered the change;
- who or what performed the change;
- review status;
- which earlier version it supersedes;
- known downstream items that may require re-evaluation.

Version history is part of knowledge provenance, not merely repository history.

## Core invariants

1. Every canonical entity has a stable identifier that is not derived solely from its title.
2. Generated numeric IDs may exist internally but are never the sole durable identity.
3. Evidence always points to a source and a precise locator or observation context.
4. Reviewed factual claims must have evidence or an explicit reason why direct evidence is unavailable.
5. Claims preserve scope and qualifiers; summaries must not silently remove them.
6. Support and contradiction occur primarily at claim level, not only concept level.
7. A relation type has one documented semantic meaning across the project.
8. A synthesis identifies all claims that materially support its conclusion.
9. Revisions preserve prior versions and the reason for change.
10. Generated files can be deleted and rebuilt without losing authored meaning.
11. No interface or implementation language may introduce hidden canonical fields.
12. Review status belongs to the knowledge item and its revision, not merely to a folder.

## Identity model

Canonical IDs should be human-inspectable and stable, for example:

```text
src:doe-2025-system-models
claim:feedback-loops-can-amplify-change
concept:feedback-loop
model:basic-stock-flow
question:when-does-local-feedback-create-instability
synthesis:feedback-and-stability-v1
```

Titles may change without changing identity. When meaning changes so substantially that continuity would mislead, create a new entity and connect it with `supersedes`, `refines`, or another accepted relation.

## Layer separation

The canonical flow is not strictly linear, but this separation must remain visible:

```text
Source → Evidence → Claim → Concept/Model → Synthesis
                    ↘ Question ↗
```

Concepts organize claims. Models transform assumptions and inputs. Questions expose gaps. Syntheses integrate the current state. None of these should be used as a universal replacement for the others.

## What remains open

Phase 0 must still test:

- the minimum required fields for each entity type;
- how evidence fragments are stored without violating copyright restrictions;
- how qualitative and quantitative evidence share a contract;
- how normative claims are separated from empirical claims;
- which relation types are essential for the first reference corpus;
- how review applies when a synthesis contains items with different statuses.
