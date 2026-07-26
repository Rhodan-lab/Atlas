# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)
[![Foundation Contract](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml)
[![Phase 1 Review Gate](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml)

> **Current status: Phase 1 — English Reference Corpus and Exact-Revision Review**
>
> Phase 0 established the knowledge contract. Phase 1 proves review coverage, lifecycle integrity, dependency impact, and reviewer authority before product expansion.

## What Atlas is

Atlas is a local-first knowledge and governance environment for an independent learner, researcher, or builder. It is designed to make reasoning inspectable:

- what a claim states and where it applies;
- what evidence supports, challenges, or contextualizes it;
- which model, assumptions, argument, or values lead to a conclusion;
- how certain, limited, contested, stale, deprecated, or retracted an item is;
- how a synthesis traces back to original sources;
- what was reviewed, by whom, for which revision, and with which unresolved findings;
- why knowledge changed through revision.

Atlas is not merely a notes app, graph visualization, textbook, course platform, or chatbot.

## Future Principia & Atlas role

Atlas is being built as the knowledge and governance layer of a future **Principia & Atlas** system.

- **Atlas** owns canonical knowledge identity, sources, evidence, claims, models, provenance, review, revision, lifecycle, and staleness.
- **Principia** will own causal explanation, pathways, investigations, simulations, system dossiers, failure analysis, and design experiences.
- Principia may depend on Atlas entities without inheriting authority automatically.
- Atlas may report which Principia artifacts are affected by an upstream knowledge change without taking ownership of pedagogical release status.

No live cross-repository dependency exists during Phase 1.

## Authority order

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. accepted foundation documents in [`docs/foundation/`](docs/foundation/)
3. accepted ADRs
4. canonical authored content and exact-revision review records
5. generated reports, coverage manifests, and backlogs
6. experimental implementation code

Machine validation can establish conformance. It cannot establish scientific truth, legal correctness, ethical acceptability, editorial quality, reviewer accountability, or translation equivalence.

## Language scope

The active authored corpus is **English-only**.

Atlas still retains language-neutral translation semantics—shared `work` identity, source-revision pinning, independent lifecycle, and stale-translation detection—but those semantics are exercised only by synthetic fixtures during the current phase.

There is no active translated vertical slice, language-specific review packet, bilingual terminology program, or supported product language beyond English.

## Accepted Phase 0 foundation

The accepted `atlas-content/0.1` foundation defines:

- source, evidence, claim, concept, relation, model, question, synthesis, and revision semantics;
- stable language-qualified `id` and shared language-neutral `work` identity;
- claim-level provenance, scope, confidence rationale, and explicit normative values;
- controlled relation vocabulary, direction, and entity compatibility;
- source access, copyright, private evidence, measurement, unit, and transformation lineage;
- review roles, reviewer conflicts, disagreement, lifecycle, dependency impact, and staleness;
- dormant translation lineage and independent translation-review semantics;
- mechanical and semantic migration rules;
- architecture policy preventing premature implementation expansion;
- deterministic invalid-fixture diagnostics.

Arguments remain structured blocks in `0.1`; they do not become independent entities until fixtures demonstrate that separate identity and lifecycle are necessary.

## Executable English reference corpus

`content/canonical/` contains **34 entity files** across three vertical slices:

1. **Catalase and assay conditions** — empirical evidence, measurement proxies, assay scope, and methodological limitations.
2. **Delayed feedback and oscillation** — formal model, reproducible derived evidence, assumptions, and model-to-world limits.
3. **Recommendation systems and user choice** — observational and randomized evidence, legal context, conflicts, and explicit normative reasoning.

Each slice supports:

```text
question → source → evidence → claim → concept/model → synthesis → revision trigger
```

## Foundation boundary fixtures

`content/fixtures/` contains:

- invalid diagnostic scenarios;
- mechanical and semantic migration cases;
- alias, rename, collision, and federation behavior;
- synthetic stale-translation behavior.

Synthetic translation fixtures test contract behavior only. They are not authored reference content.

## Phase 1 review system

Phase 1 adds:

- `atlas-review/0.1` exact-revision review records;
- `atlas-promotion/0.1` deterministic lifecycle decisions;
- `atlas-review-coverage/0.1` packet and complete-slice coverage;
- `atlas-review-backlog/0.1` deterministic missing-review tasks.

The review system records:

- exact entity ID and revision;
- review type;
- reviewer kind, independence, qualification, accountability, and conflicts;
- outcome and review horizon;
- findings with severity and resolution status;
- whether the bounded review permits promotion.

The promotion gate blocks:

- AI-only or machine-only authority where accountable human review is required;
- wrong-revision reviews;
- expired time-sensitive reviews;
- stale synthetic translation fixtures;
- unresolved critical or major findings;
- hidden conflicts;
- incomplete contested, deprecated, or retracted transitions.

## Active review scopes

Reviewer-ready scopes are in [`docs/phase-1/packets/`](docs/phase-1/packets/):

- catalase and assay methodology;
- delayed-feedback mathematics, terminology, and inference limits;
- recommender evidence, DSA context, and ethical governance.

The first complete English slice is:

`content/reviews/coverage/feedback-complete-vertical-slice.json`

Its current generated backlog contains:

- 38 gate tasks;
- 13 automation-eligible tasks;
- 25 human-required tasks.

AI-assisted findings remain review preparation and cannot grant authority.

## Validation

Install the pinned dependency and run all tests:

```bash
python -m pip install -r tools/foundation-validator/requirements.txt
python -m unittest discover -s tools/foundation-validator/tests -v
```

Validate authored English content:

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
```

Validate a review record:

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/feedback-domain-ai-assisted.json
```

Generate complete-slice coverage:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report phase1-coverage.md
```

Generate the review backlog:

```bash
python tools/foundation-validator/phase1_review_backlog.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --json-out phase1-backlog.json \
  --report phase1-backlog.md
```

These commands produce governance output only. They never edit lifecycle status automatically.

## Reading path

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/README.md`](docs/foundation/README.md)
3. [`docs/foundation/18-phase-0-closure-report.md`](docs/foundation/18-phase-0-closure-report.md)
4. [`docs/phase-1/README.md`](docs/phase-1/README.md)
5. [`docs/phase-1/review-protocol.md`](docs/phase-1/review-protocol.md)
6. [`docs/phase-1/promotion-policy.md`](docs/phase-1/promotion-policy.md)
7. [`docs/phase-1/feedback-vertical-slice-readiness.md`](docs/phase-1/feedback-vertical-slice-readiness.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Repository map

```text
Atlas/
├── PROJECT_STATE.md
├── docs/foundation/            # accepted knowledge and governance foundation
├── docs/phase-1/               # review, coverage, backlog, and reviewer packets
├── docs/adr/                   # accepted and proposed architecture decisions
├── docs/reviews/               # Phase 0 validation and review records
├── content/canonical/          # active English reference corpus
├── content/fixtures/           # contract, migration, identity, and synthetic tests
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
- active translated corpus or language-specific review programs;
- AI-generated authoritative content;
- direct Principia integration or repository merger;
- promotion of `.atlas`, SQL, or prototype runtime structures as canonical;
- optimization without accepted requirements and measurements.

## Phase boundary

Phase 1 closes only when review records and promotion decisions are executable, lifecycle transitions preserve history, dishonest authority paths fail, reviewer packets are usable without code knowledge, and the complete English delayed-feedback slice has sufficient revision-specific review coverage for its intended state.

Passing a validator confirms only the checks it performs. It never turns a draft into authoritative knowledge by itself.

## License

MIT
