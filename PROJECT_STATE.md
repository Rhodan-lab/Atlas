# Atlas Project State

## Current status

**Phase 0 — Knowledge Foundation (closure candidate)**

The Phase 0 foundation specification and executable fixture system are mechanically complete for `atlas-content/0.1`. Final transition to Phase 1 requires:

1. final green checks on PR #3;
2. maintainer acceptance through merge.

Canonical example content remains `draft`. Foundation closure does not grant scientific, legal, ethical, or translation authority to those examples.

The existing C++, Rust, Python ingestion, TypeScript, SQL, and UI work remains an **experimental prototype**. It is tested for regression but is not the approved product architecture.

## Authority order

1. `PROJECT_STATE.md`
2. `docs/foundation/`
3. accepted ADRs
4. reviewed canonical content and fixtures
5. implementation code and generated artifacts

When code conflicts with the accepted foundation, the code is provisional.

## Phase 0 foundation completed

### Product and ontology

- product charter and explicit non-goals;
- canonical source, evidence, claim, concept, relation, model, question, synthesis, and revision meanings;
- stable language-specific `id` and language-neutral `work` identity;
- claim granularity, scope, kind, confidence rationale, and embedded argument structure;
- controlled relation vocabulary, direction, and entity compatibility.

### Evidence and governance

- claim-level evidence and provenance;
- evidence access, copyright, restricted-source, unit, dataset, and transformation-lineage rules;
- lifecycle, review roles, reviewer conflicts, disagreement, and revision impact;
- staleness states and dependency propagation;
- explicit normative values and inference boundaries;
- AI-assisted work remains `draft` and cannot grant authority.

### Contract and architecture

- versioned `atlas-content/0.1` Markdown contract;
- contract migration and rollback invariants;
- architecture and language-admission policy;
- accepted ADR-0001 for the minimum Phase 0 validator;
- experimental prototype audit and feature freeze.

### Canonical fixtures

- 34 English canonical entity files across three vertical slices;
- 8 Indonesian translated entities forming one complete vertical path;
- 24 invalid diagnostic scenarios;
- mechanical and semantic migration fixtures;
- alias, rename, collision, and federation fixture;
- stale-translation fixture;
- reproducible delayed-feedback model output.

## Validation status

Foundation Contract workflow run `30169791668` passed on:

- Python 3.11;
- Python 3.13.

Results:

- 30 tests passed;
- 0 tests failed;
- canonical and translated corpus produced 0 errors and 0 warnings;
- migration fixtures passed;
- identity fixture passed;
- translation mismatch produced `possibly-stale`;
- the experimental prototype regression suite remained green across its tested languages and operating systems.

Validation records:

- `docs/reviews/phase-0-structural-validation.md`
- `docs/reviews/phase-0-source-verification.md`
- `docs/reviews/phase-0-review-register.md`
- `docs/foundation/18-phase-0-closure-report.md`

## Foundation versus content review

Phase 0 closes the **knowledge contract, governance model, and executable fixture architecture**.

Phase 1 owns **revision-specific review of the reference corpus**. Pending independent reviews include:

- biochemistry and assay methodology;
- control-systems terminology;
- recommender-system and political-communication methodology;
- ethical and legal context;
- Indonesian translation equivalence.

These reviews block promotion of specific entities from `draft`; they do not invalidate the mechanically proven Phase 0 foundation.

Any Phase 1 review that exposes an ontology failure may reopen the relevant Phase 0 decision with preserved history.

## Phase 0 closure gate

| Gate | Result |
|---|---|
| product purpose and non-goals explicit | passed |
| canonical entities and invariants explicit | passed |
| claim-level provenance representable | passed |
| relation direction and compatibility executable | passed |
| canonical records split and valid | passed |
| multilingual identity and translation lineage demonstrated | passed |
| migration, alias, federation, and staleness demonstrated | passed |
| invalid behavior deterministic | passed |
| minimum validator selected through ADR | passed |
| closure report recommends Phase 1 | passed |
| final PR checks and maintainer merge | pending |

## Work allowed before merge

- correct closure-report or fixture defects;
- resolve final CI failures;
- improve review documentation without changing accepted meaning;
- keep the prototype regression suite healthy.

Do not add product features, services, UI expansion, plugins, synchronization, new languages, or AI synthesis during closure.

## Phase 1 entry scope

After PR #3 is merged:

1. independently review exact canonical revisions;
2. record findings and conflicts;
3. promote only entities that pass their required review types;
4. harden the reference validator without turning it into the product runtime;
5. expand fixtures only when review reveals a real contract gap;
6. keep broader product engineering frozen until Phase 1 exit criteria justify it.

**Phase 0 is no longer conceptually incomplete. It is awaiting final acceptance of an executable, versioned foundation.**
