# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)

> **Current status: Phase 0 — Knowledge Foundation, verification-ready mature draft**
>
> Product feature development remains frozen. The current work is canonical fixture splitting, independent review, multilingual and migration testing, and selection of the smallest Phase 1 validator.

## What Atlas is

Atlas is a local-first knowledge environment for an independent learner, researcher, or builder. It is designed to make reasoning inspectable:

- what a claim states and where it applies;
- what evidence supports, challenges, or contextualizes it;
- which model or assumptions produce a conclusion;
- how certain, limited, contested, or stale an item is;
- how concepts and questions connect across domains;
- how a synthesis can be traced back to original sources;
- why knowledge changed through revision.

Atlas is not merely a notes app, graph visualization, textbook, course platform, or chatbot.

## Why the project is still in Phase 0

The repository contains an experimental C++, Rust, Python, TypeScript, SQL, and browser prototype. It proves several engineering ideas are possible, but it was created before the knowledge model and review governance were mature.

The prototype is preserved for testing and comparison. It does not own the ontology, dictate the final languages, or count as a completed product foundation.

## Authority order

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/`](docs/foundation/)
3. accepted architecture decision records
4. reviewed canonical content and fixtures
5. implementation code and generated artifacts

When code conflicts with the foundation, code is provisional.

## Canonical knowledge units

Atlas currently distinguishes:

- **Source** — identifiable origin of information
- **Evidence** — the relevant passage, observation, measurement, data subset, or derived result
- **Claim** — one evaluable and qualified statement
- **Concept** — an explanatory structure organizing meaning and claims
- **Relation** — a governed typed and directed connection
- **Model** — a representation used to explain, calculate, simulate, classify, or predict
- **Question** — an explicit knowledge need or unresolved problem
- **Synthesis** — a scoped integration of claims, evidence, models, disagreement, and values
- **Revision** — a traceable change and its downstream consequences

Arguments are structured blocks in `atlas-content/0.1`, not independent entities unless later fixtures prove that independent identity is necessary.

## Contract and governance now defined

The mature draft includes:

- `atlas-content/0.1` authored Markdown contract;
- multilingual `id` and shared language-neutral `work` identities;
- claim-level provenance and scoped confidence rationale;
- controlled relation vocabulary and entity compatibility;
- evidence access, copyright, private-source, unit, dataset, and transformation-lineage rules;
- structural, editorial, source, domain, methodological, reproducibility, ethics, and translation review;
- reviewer conflict and disagreement handling;
- contract migration and rollback invariants;
- dependency impact and staleness propagation;
- invalid fixtures with deterministic expected diagnostics;
- architecture policy preventing premature polyglot expansion.

## Reference corpus

Three bundled draft slices now test the ontology:

1. [`Catalase and assay conditions`](content/reference/slice-a-catalase.md) — empirical evidence, synthetic observation, measurement proxies, and biological scope.
2. [`Delayed feedback and oscillation`](content/reference/slice-b-feedback.md) — formal model, exact derived evidence, assumptions, and analogy limits.
3. [`Recommendation systems, exposure, and user choice`](content/reference/slice-c-recommenders.md) — observational and randomized evidence, legal context, conflicts, and normative reasoning.

The corpus index is [`content/reference/README.md`](content/reference/README.md). Invalid contract examples are in [`content/fixtures/invalid/README.md`](content/fixtures/invalid/README.md).

All reference material remains `draft`. It is ontology evidence, not reviewed educational content.

## Foundation reading path

Start with:

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/README.md`](docs/foundation/README.md)
3. [`docs/foundation/00-charter.md`](docs/foundation/00-charter.md)
4. [`docs/foundation/01-knowledge-model.md`](docs/foundation/01-knowledge-model.md)
5. [`docs/foundation/03-content-contract.md`](docs/foundation/03-content-contract.md)
6. [`docs/foundation/07-decision-register.md`](docs/foundation/07-decision-register.md)
7. [`docs/foundation/17-phase-0-maturity-assessment.md`](docs/foundation/17-phase-0-maturity-assessment.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Current repository map

```text
Atlas/
├── PROJECT_STATE.md
├── AGENTS.md
├── docs/foundation/       # authoritative Phase 0 semantics and governance
├── docs/adr/              # architecture decision process
├── content/reference/     # bundled draft vertical slices
├── content/fixtures/      # valid/invalid contract evidence
├── engine/cpp/            # experimental prototype
├── services/search-rs/    # experimental prototype
├── tools/ingest-py/       # experimental prototype
├── apps/api-ts/           # experimental prototype
├── contracts/             # provisional derived-format work
├── storage/               # provisional persistence work
└── scripts/               # prototype checks
```

## What is allowed now

- split bundled slices into canonical entity files;
- verify sources and locators;
- record independent review findings;
- add Indonesian translation and stale-translation fixtures;
- add migration, identity, and dependency-impact fixtures;
- compare validator implementation options through an ADR;
- fix prototype defects needed for inspection.

## What remains frozen

- product UI expansion;
- additional services or languages;
- plugin and synchronization systems;
- AI-generated authoritative content;
- promotion of `.atlas`, SQL, or runtime structures as canonical;
- optimization without accepted requirements and measurements.

## Phase 0 completion condition

Phase 0 is not complete until canonical fixtures are split, reviewed, migrated, translated, and validated; no critical or major review issue remains; and the smallest Phase 1 validator is selected through an accepted ADR.

See [`docs/foundation/17-phase-0-maturity-assessment.md`](docs/foundation/17-phase-0-maturity-assessment.md) for the current gate assessment.

## Prototype validation

The experimental prototype remains available for comparison:

```bash
./scripts/check.sh
```

Passing prototype tests means the experiment is internally consistent. It does not certify the knowledge foundation or reference content.

## License

MIT
