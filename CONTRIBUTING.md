# Contributing to Atlas

## Current contribution mode

Atlas is in **Phase 0 — Knowledge Foundation**. Feature development is frozen. Contributions should improve the product charter, ontology, evidence governance, authoring contract, reference fixtures, validation criteria, or documented decisions.

The existing polyglot code is an experimental prototype. Its current component boundaries are not final ownership rules.

## Before making a change

Read, in order:

1. `PROJECT_STATE.md`
2. `AGENTS.md`
3. `docs/foundation/00-charter.md`
4. `docs/foundation/01-knowledge-model.md`
5. `docs/foundation/02-evidence-and-editorial-policy.md`
6. `docs/foundation/03-content-contract.md`
7. the remaining files in `docs/foundation/`
8. any accepted ADR relevant to the change

Do not infer product requirements from the prototype alone.

## Contributions encouraged during Phase 0

- clearer entity definitions and invariants;
- valid and invalid content fixtures;
- complete source-to-synthesis vertical slices;
- citation and evidence-locator rules;
- disagreement, uncertainty, revision, and review examples;
- controlled vocabulary analysis;
- architecture alternatives and measured baselines;
- documentation consistency and contradiction checks;
- bug fixes that keep the prototype inspectable and testable.

## Contributions not accepted during Phase 0

- new UI features;
- new product services;
- additional programming languages;
- plugin systems;
- AI-generated authoritative content;
- cloud synchronization;
- premature performance optimization;
- expansion of `.atlas` or SQL as if either were canonical;
- changes that promote draft content without its required review.

## Knowledge contribution requirements

A knowledge change should identify:

- canonical entity type;
- stable identifier;
- status and revision;
- scope and qualifiers;
- relevant sources and evidence;
- supporting or challenging relationships;
- uncertainty and limitations;
- required review types;
- downstream material that may be affected.

All new modules begin as `draft`.

## Architecture contribution requirements

A proposed implementation or language boundary must follow `docs/foundation/04-language-and-architecture-policy.md`.

A proposal should include:

- concrete requirement;
- responsibility and non-responsibilities;
- alternatives;
- representative fixtures or workload;
- measurable acceptance criteria;
- maintenance and operational cost;
- compatibility and failure behavior;
- rollback or replacement plan.

“Best language,” “faster,” or “safer” without a representative comparison is not sufficient.

## Prototype checks

When a change touches existing prototype code, run the relevant checks:

```bash
./scripts/check.sh
```

Available component targets include:

```bash
make cpp
make python
make rust
make api
make integration
```

Passing prototype tests confirms internal consistency only. It does not grant foundation or scientific approval.

## Pull requests

Keep each pull request bounded to one foundation purpose. Include:

- foundation problem being solved;
- affected invariant, decision, or phase-gate criterion;
- authoritative contracts changed;
- fixtures or examples added;
- validation performed;
- unresolved questions and follow-up work;
- whether any material must return to review.

Substantial changes should update `PROJECT_STATE.md` or the decision register when appropriate.
