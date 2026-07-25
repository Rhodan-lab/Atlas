# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)
[![Foundation Contract](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml)

> **Current status: Phase 0 — Knowledge Foundation, closure candidate for `atlas-content/0.1`**
>
> The versioned foundation and executable fixtures are mechanically complete. Final acceptance requires green PR #3 checks and maintainer merge. Canonical example content remains `draft` pending revision-specific expert review in Phase 1.

## What Atlas is

Atlas is a local-first knowledge environment for an independent learner, researcher, or builder. It is designed to make reasoning inspectable:

- what a claim states and where it applies;
- what evidence supports, challenges, or contextualizes it;
- which model, assumptions, argument, or values lead to a conclusion;
- how certain, limited, contested, translated, or stale an item is;
- how a synthesis traces back to original sources;
- why knowledge changed through revision.

Atlas is not merely a notes app, graph visualization, textbook, course platform, or chatbot.

## Authority order

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/`](docs/foundation/)
3. accepted ADRs
4. reviewed canonical content and fixtures
5. implementation code and generated artifacts

When code conflicts with the accepted foundation, the code is provisional.

## Phase 0 foundation

The foundation now defines:

- versioned `atlas-content/0.1` authored Markdown;
- source, evidence, claim, concept, relation, model, question, synthesis, and revision semantics;
- stable language-specific `id` and shared language-neutral `work` identity;
- claim-level provenance, scope, confidence rationale, and explicit normative values;
- controlled relation vocabulary, direction, and entity compatibility;
- source access, copyright, private evidence, measurement, unit, and transformation lineage;
- review roles, reviewer conflicts, disagreement, lifecycle, dependency impact, and staleness;
- translation lineage and independent translation review;
- mechanical and semantic migration rules;
- architecture policy preventing premature polyglot expansion;
- deterministic invalid-fixture diagnostics.

Arguments remain structured blocks in `0.1`; they do not become independent entities until fixtures demonstrate that independent identity and lifecycle are necessary.

## Executable reference corpus

### Canonical English entities

`content/canonical/` contains **34 entity files** across three complete vertical slices:

1. **Catalase and assay conditions** — empirical evidence, measurement proxies, assay scope, and methodological limitations.
2. **Delayed feedback and oscillation** — formal model, reproducible derived evidence, assumptions, and model-to-world limits.
3. **Recommendation systems and user choice** — observational and randomized evidence, legal context, conflicts, and explicit normative reasoning.

Each slice supports:

```text
question → source → evidence → claim → concept/model → synthesis → revision trigger
```

### Indonesian translation path

`content/translations/id/feedback/` contains **8 translated entities** forming a complete delayed-feedback path. Every translation has:

- a language-specific canonical ID;
- shared `work` identity with the English entity;
- source entity and revision lineage;
- its own lifecycle and staleness;
- no inherited reviewed status.

### Boundary fixtures

`content/fixtures/` contains:

- 24 invalid diagnostic scenarios;
- mechanical and semantic migration cases;
- alias, rename, collision, and federation behavior;
- stale-translation behavior.

## Foundation validator

ADR-0001 selects a small Python 3.11+ validator solely for Phase 0 conformance. It does not judge truth, rewrite content, assign confidence, or promote review status.

```bash
python -m pip install -r tools/foundation-validator/requirements.txt
python -m unittest discover -s tools/foundation-validator/tests -v
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical content/translations
```

Validated matrix:

- Python 3.11: passed;
- Python 3.13: passed;
- 30 tests: passed;
- canonical and translated corpus: 0 errors, 0 warnings;
- migration, identity, and stale-translation fixtures: passed.

See [`docs/reviews/phase-0-structural-validation.md`](docs/reviews/phase-0-structural-validation.md).

## Foundation acceptance versus content review

Phase 0 accepts the **contract, governance, and executable fixture architecture**.

It does not claim that every example is independently reviewed knowledge. All example entities remain `draft`. Phase 1 performs revision-specific biochemical, methodological, control-systems, recommender, legal-context, ethical, editorial, and translation review.

Review status is tracked in [`docs/reviews/phase-0-review-register.md`](docs/reviews/phase-0-review-register.md).

## Reading path

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/README.md`](docs/foundation/README.md)
3. [`docs/foundation/00-charter.md`](docs/foundation/00-charter.md)
4. [`docs/foundation/01-knowledge-model.md`](docs/foundation/01-knowledge-model.md)
5. [`docs/foundation/03-content-contract.md`](docs/foundation/03-content-contract.md)
6. [`docs/foundation/05-phase-gates.md`](docs/foundation/05-phase-gates.md)
7. [`docs/foundation/07-decision-register.md`](docs/foundation/07-decision-register.md)
8. [`docs/foundation/18-phase-0-closure-report.md`](docs/foundation/18-phase-0-closure-report.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Repository map

```text
Atlas/
├── PROJECT_STATE.md
├── docs/foundation/            # authoritative knowledge and governance foundation
├── docs/adr/                   # accepted and proposed architecture decisions
├── docs/reviews/               # explicit machine, internal, and pending review records
├── content/canonical/          # split canonical English fixtures
├── content/translations/       # first-class multilingual fixtures
├── content/fixtures/           # invalid, migration, identity, and staleness tests
├── tools/foundation-validator/ # bounded Phase 0 reference validator
├── engine/cpp/                 # experimental prototype
├── services/search-rs/         # experimental prototype
├── tools/ingest-py/            # experimental prototype
├── apps/api-ts/                # experimental prototype
├── contracts/                  # provisional derived-format work
└── storage/                    # provisional persistence work
```

## Work remains frozen during closure

- product UI expansion;
- new services or programming languages;
- specialized retrieval architecture;
- plugins and synchronization;
- AI-generated authoritative content;
- promotion of `.atlas`, SQL, or prototype runtime structures as canonical;
- optimization without accepted requirements and measurements.

## Closure report

[`docs/foundation/18-phase-0-closure-report.md`](docs/foundation/18-phase-0-closure-report.md) recommends accepting the Phase 0 foundation after final green checks and merge of PR #3.

The experimental prototype remains available for regression comparison:

```bash
./scripts/check.sh
```

Passing prototype tests confirms only tested implementation behavior. It does not grant authority to content or architecture.

## License

MIT
