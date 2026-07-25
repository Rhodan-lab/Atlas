# Foundation Decision Register

## Purpose

This register separates accepted constraints from unresolved questions. Unresolved items must not be silently decided by implementation details.

## Decision states

- `accepted` — binding until explicitly revised;
- `provisional` — current working assumption requiring fixture or review evidence;
- `open` — not yet decided;
- `rejected` — considered and excluded for the stated reason;
- `superseded` — replaced by a later decision with preserved history.

## Accepted decisions

### FND-001 — Foundation before feature development

**State:** accepted

Atlas remains in Phase 0 until the knowledge and editorial contracts pass their gate. Existing code is experimental and feature-frozen.

### FND-002 — Markdown is the authored source of truth

**State:** accepted

Databases, binary formats, indexes, and API representations are derived and reproducible. They cannot become the only location of canonical meaning or review history.

### FND-003 — Claim-level provenance is required

**State:** accepted

Sources and evidence must connect to individually inspectable claims. Concept-level citations alone are insufficient.

### FND-004 — Draft is the default lifecycle state

**State:** accepted

All new knowledge modules and generated material remain `draft` until the required review types are completed.

### FND-005 — Local ownership is a core constraint

**State:** accepted

Authoritative content must remain inspectable and exportable without a mandatory cloud account.

### FND-006 — Polyglot requires evidence

**State:** accepted

Multiple languages are allowed only through the architecture decision policy. Existing language assignments are candidates, not binding decisions.

### FND-007 — AI cannot grant authority

**State:** accepted

AI-assisted extraction or synthesis may create drafts, but cannot create reviewed status or replace source verification.

### FND-008 — No global truth score

**State:** accepted

Atlas preserves domain-appropriate uncertainty measures and written appraisal. It does not collapse all credibility into one universal number.

## Provisional decisions

### FND-101 — Initial canonical entity set

**State:** provisional

The current set is source, evidence, claim, concept, relation, model, question, synthesis, and revision. Fixtures must demonstrate that each entity is necessary and that no critical entity is missing.

### FND-102 — Controlled initial relation vocabulary

**State:** provisional

The relation set in `01-knowledge-model.md` is a starting vocabulary. It must be tested for ambiguity, overlap, inverse semantics, and entity compatibility.

### FND-103 — Human-readable canonical identifiers

**State:** provisional

Stable prefixed identifiers are preferred. Collision handling, renaming, aliases, multilingual titles, and repository federation remain to be tested.

### FND-104 — Qualitative confidence vocabulary

**State:** provisional

`uncertain`, `plausible`, `well-supported`, and `strongly-supported` may be used only with rationale. The vocabulary must be tested across scientific, formal, historical, and normative material.

### FND-105 — Independent learner as primary initial user

**State:** provisional

The first product framing serves an independent learner or researcher exploring connected knowledge without a rigid course sequence. Later collaborative or institutional needs must not distort the first foundation prematurely.

## Open decisions

### FND-201 — Authoring language policy

Questions:

- Is English the canonical authoring language, Indonesian, or multilingual from the beginning?
- Are translations separate entities, revisions, or localized views of one entity?
- Which fields are language-neutral?

This must be resolved before the reference corpus becomes large.

### FND-202 — Evidence excerpt storage

Questions:

- When should Atlas store a short excerpt, structured observation, hash, or locator only?
- How are copyright, access restrictions, and private sources handled?
- How can a reviewer verify evidence that cannot be redistributed?

### FND-203 — Claim granularity

Questions:

- How atomic must claims be?
- How are compound claims detected and represented?
- When does splitting reduce readability without improving review?

### FND-204 — Argument representation

Questions:

- Are premises and conclusions represented as claims plus relations, or is a separate argument entity required?
- How are deductive, inductive, abductive, causal, and normative arguments distinguished?

### FND-205 — Dataset and quantitative evidence model

Questions:

- How are tables, variables, units, transformations, missing data, and analysis scripts linked to claims?
- Which metadata is canonical versus domain-specific?

### FND-206 — Review authority and trust

Questions:

- How are reviewer roles and conflicts of interest represented?
- Can review be distributed, and how are disagreements between reviewers preserved?
- Which review types are required for different entity kinds?

### FND-207 — Revision impact propagation

Questions:

- Which dependencies trigger automatic stale flags?
- How are downstream syntheses re-reviewed?
- What can be automated without implying that semantic impact has been fully understood?

### FND-208 — First reference corpus

Questions:

- Which three vertical slices best stress the ontology?
- Which domains expose quantitative, formal, interpretive, and ethical differences?
- What content size is enough to evaluate the model without becoming a content-production project?

### FND-209 — First reference implementation

Questions:

- What is the smallest runtime required after Phase 0?
- Which single-language baseline should be tested first?
- Which prototype components should be retained, merged, rewritten, or removed?

### FND-210 — Repository structure after Phase 0

Questions:

- Should the current prototype move under `prototypes/`?
- Should canonical content and implementation remain in one repository?
- How should generated artifacts be separated from authored material?

## Rejected decisions

### FND-301 — Treat the current polyglot stack as final

**State:** rejected

Reason: the stack predates the canonical ontology, reference corpus, performance targets, and language decision evidence.

### FND-302 — Use concepts as the only knowledge entity

**State:** rejected

Reason: this prevents claim-level provenance, disagreement, model assumptions, open questions, and inspectable synthesis.

### FND-303 — Build the polished UI before representative content

**State:** rejected

Reason: interface behavior would solidify incomplete semantics and create misleading signs of product maturity.

## Decision procedure

To resolve an open decision:

1. state the concrete problem and affected invariants;
2. create representative valid and invalid examples;
3. compare alternatives and failure modes;
4. record the decision and rationale;
5. update affected contracts and phase gates;
6. add migration notes if any authored or generated material changes;
7. retain the previous decision history.
