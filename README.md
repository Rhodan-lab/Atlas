# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)
[![Foundation Contract](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml)
[![Phase 1 Review Gate](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml)

> **Current status: Phase 1 — Reference Corpus and Review Gate**
>
> Phase 0 was accepted through merged PR #3. The active work is exact-revision review, reviewer-ready packets, deterministic promotion gating, and lifecycle integrity. Product feature expansion remains frozen.

## What Atlas is

Atlas is a local-first knowledge environment for an independent learner, researcher, or builder. It is designed to make reasoning inspectable:

- what a claim states and where it applies;
- what evidence supports, challenges, or contextualizes it;
- which model, assumptions, argument, or values lead to a conclusion;
- how certain, limited, contested, translated, stale, deprecated, or retracted an item is;
- how a synthesis traces back to original sources;
- what was reviewed, by whom, for which revision, and with which unresolved findings;
- why knowledge changed through revision.

Atlas is not merely a notes app, graph visualization, textbook, course platform, or chatbot.

## Authority order

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. accepted foundation documents in [`docs/foundation/`](docs/foundation/)
3. accepted ADRs
4. canonical authored content and revision-specific review records
5. generated reports and indexes
6. experimental implementation code

Machine validation can establish conformance. It cannot establish scientific truth, legal correctness, ethical acceptability, or translation equivalence.

## Accepted Phase 0 foundation

The accepted `atlas-content/0.1` foundation defines:

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

Arguments remain structured blocks in `0.1`; they do not become independent entities until fixtures demonstrate that separate identity and lifecycle are necessary.

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

### Foundation boundary fixtures

`content/fixtures/` contains:

- 24 invalid diagnostic scenarios;
- mechanical and semantic migration cases;
- alias, rename, collision, and federation behavior;
- stale-translation behavior.

## Phase 1 review system

Phase 1 adds `atlas-review/0.1` and `atlas-promotion/0.1` governance.

The review system records:

- exact entity ID and revision;
- review type;
- reviewer kind, independence, qualification, accountability, and conflicts;
- outcome and review horizon;
- findings with severity and resolution status;
- whether the bounded review recommends promotion.

The promotion gate independently evaluates coverage and authority. It blocks:

- AI-only or machine-only authority where accountable human review is required;
- wrong-revision reviews;
- stale translations;
- expired time-sensitive reviews;
- unresolved critical or major findings;
- hidden conflicts;
- incomplete contested, deprecated, or retracted transitions.

Review records are in `content/reviews/records/`. Lifecycle and promotion fixtures are in `content/reviews/fixtures/`.

## Reviewer packets

Reviewer-ready scopes are in [`docs/phase-1/packets/`](docs/phase-1/packets/):

- catalase and assay methodology;
- delayed-feedback mathematics and terminology;
- recommender evidence, DSA context, and ethical governance;
- English–Indonesian feedback translation equivalence.

AI-assisted findings remain internal review preparation and cannot grant authority.

## Validation

Install the pinned dependency and run all tests:

```bash
python -m pip install -r tools/foundation-validator/requirements.txt
python -m unittest discover -s tools/foundation-validator/tests -v
```

Validate authored content:

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical content/translations
```

Validate a review record:

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/feedback-domain-ai-assisted.json
```

Evaluate a promotion fixture and generate a report:

```bash
python tools/foundation-validator/phase1_review_gate.py promotion \
  content/reviews/fixtures/valid-normative-promotion.json \
  --report phase1-report.md
```

The command produces governance output only. It never edits lifecycle status automatically.

## Reading path

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/README.md`](docs/foundation/README.md)
3. [`docs/foundation/18-phase-0-closure-report.md`](docs/foundation/18-phase-0-closure-report.md)
4. [`docs/phase-1/README.md`](docs/phase-1/README.md)
5. [`docs/phase-1/review-protocol.md`](docs/phase-1/review-protocol.md)
6. [`docs/phase-1/promotion-policy.md`](docs/phase-1/promotion-policy.md)
7. [`docs/phase-1/packets/README.md`](docs/phase-1/packets/README.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Repository map

```text
Atlas/
├── PROJECT_STATE.md
├── docs/foundation/            # accepted knowledge and governance foundation
├── docs/phase-1/               # review protocol, promotion policy, and packets
├── docs/adr/                   # accepted and proposed architecture decisions
├── docs/reviews/               # Phase 0 validation and review records
├── content/canonical/          # split canonical English fixtures
├── content/translations/       # first-class multilingual fixtures
├── content/fixtures/           # contract, migration, identity, and staleness tests
├── content/reviews/            # Phase 1 review records and lifecycle fixtures
├── tools/foundation-validator/ # bounded content and review validators
├── engine/cpp/                 # experimental prototype
├── services/search-rs/         # experimental prototype
├── tools/ingest-py/            # experimental prototype
├── apps/api-ts/                # experimental prototype
├── contracts/                  # provisional derived-format work
└── storage/                    # provisional persistence work
```

## Still frozen during Phase 1

- product UI expansion;
- new services or programming languages;
- specialized retrieval architecture;
- plugins and synchronization;
- AI-generated authoritative content;
- promotion of `.atlas`, SQL, or prototype runtime structures as canonical;
- optimization without accepted requirements and measurements.

## Phase boundary

Phase 1 closes only when review records and promotion decisions are executable, lifecycle transitions preserve history, dishonest authority paths fail, reviewer packets are usable without code knowledge, and at least one complete vertical slice has sufficient revision-specific review coverage for its intended state.

Passing a validator confirms only the checks it performs. It never turns a draft into authoritative knowledge by itself.

## License

MIT
