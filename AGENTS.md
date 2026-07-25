# Atlas Contributor and Agent Rules

These rules apply to humans, coding agents, research agents, and automated tools working in this repository.

## Start here

Before making changes, read:

1. `PROJECT_STATE.md`
2. every file in `docs/foundation/`
3. relevant accepted architecture decision records
4. the contract or content file being changed

Do not infer project direction from the current prototype alone.

## Foundation-first rule

Atlas is currently in Phase 0. Work must strengthen the knowledge foundation before expanding software.

Allowed work:

- clarify product boundaries;
- improve the ontology and content contract;
- model representative knowledge examples;
- define evidence, review, revision, and provenance rules;
- add validation tests for accepted contracts;
- repair defects that block verification.

Disallowed work during Phase 0:

- new UI features;
- new services or plugins;
- adding a language because it seems suitable;
- premature optimization;
- opaque AI-generated content pipelines;
- treating generated data as the editorial source of truth.

## Knowledge rules

- Markdown is authoritative for authored knowledge and governance documents.
- A source is not evidence by itself; an evidence record identifies the relevant part and context.
- A concept is not a bag of facts. Claims must remain individually traceable.
- Relationships must use an accepted type and explicit direction.
- Contradictory credible claims must coexist visibly until resolved; do not silently overwrite them.
- Uncertainty must be stated with a rationale, not hidden behind a score.
- All new modules remain `draft` until the required editorial or scientific review is complete.
- Reviewed does not mean eternally true; revisions and superseded material must remain traceable.

## Architecture rules

- Prefer the smallest architecture that satisfies an accepted requirement.
- A new language requires an ADR with a concrete boundary, alternatives, operational cost, and measurable acceptance criteria.
- Do not implement the same parser, validation rule, or domain invariant independently in multiple languages.
- Cross-process contracts require versioning, fixtures, and compatibility tests.
- Generated formats must be reproducible from authoritative inputs.
- The current polyglot implementation is a prototype candidate, not a binding decision.

## Change discipline

Every substantial change must state:

- which foundation problem it solves;
- which invariant or phase-gate criterion it advances;
- what remains unresolved;
- whether it changes an authoritative contract;
- how the change was validated.

Update `PROJECT_STATE.md` whenever the active phase, authority order, accepted decisions, or blockers change.

## Definition of done

A change is not done merely because it builds. It is done when its meaning, evidence, boundaries, failure behavior, and place in the phase plan are clear and testable.
