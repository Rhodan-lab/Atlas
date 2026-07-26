# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)
[![Foundation Contract](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml)
[![Phase 1 Review Gate](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml)

> **Current status: Phase 1 — English Reference Corpus and Accountable Exact-Revision Review**
>
> Phase 0 established the knowledge contract. Phase 1 proves review coverage, bounded machine authority, human accountability, lifecycle integrity, and dependency impact before product expansion.

## What Atlas is

Atlas is a local-first knowledge and governance environment for an independent learner, researcher, or builder. It makes reasoning inspectable:

- what a claim states and where it applies;
- what evidence supports, challenges, or contextualizes it;
- which model, assumptions, argument, or values lead to a conclusion;
- how certain, limited, contested, stale, deprecated, or retracted an item is;
- how a synthesis traces to original sources;
- what was reviewed, by whom or by which deterministic procedure, for which revision, and with which unresolved findings;
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

Machine validation can establish bounded conformance or a fully specified calculation. It cannot establish scientific truth, source interpretation, model applicability, legal correctness, ethical acceptability, editorial quality, or human accountability.

## Language scope

The active authored and review corpus is **English-only**.

Atlas retains language-neutral translation semantics—shared `work` identity, source-revision pinning, independent lifecycle, and stale-translation detection—but they are exercised only by neutral synthetic fixtures during the current phase.

There is no active translated vertical slice, language-specific review packet, bilingual terminology program, or supported authored language beyond English.

## Accepted foundation

The accepted `atlas-content/0.1` foundation defines:

- source, evidence, claim, concept, relation, model, question, synthesis, and revision semantics;
- stable language-qualified `id` and shared language-neutral `work` identity;
- claim-level provenance, scope, confidence rationale, and explicit normative values;
- controlled relation vocabulary, direction, and entity compatibility;
- source access, measurement, units, transformations, and lineage;
- review roles, conflicts, disagreement, lifecycle, dependency impact, and staleness;
- dormant translation lineage and independent translation-review semantics;
- mechanical and semantic migration rules;
- deterministic invalid-fixture diagnostics;
- architecture restraint before product expansion.

## Executable English corpus

`content/canonical/` contains **34 entity files** across three vertical slices:

1. **Catalase and assay conditions** — empirical evidence, measurement proxies, assay scope, and methodological limitations.
2. **Delayed feedback and oscillation** — formal model, reproducible derived evidence, assumptions, and model-to-world limits.
3. **Recommendation systems and user choice** — observational and randomized evidence, legal context, conflicts, and explicit normative reasoning.

Each slice supports:

```text
question → source → evidence → claim → concept/model → synthesis → revision trigger
```

## Phase 1 review system

Phase 1 adds:

- `atlas-review/0.1` exact-revision review records;
- `atlas-promotion/0.1` deterministic lifecycle decisions;
- `atlas-review-coverage/0.1` packet and complete-slice coverage;
- `atlas-review-backlog/0.1` deterministic missing-review tasks;
- deterministic structural and fully specified reproducibility attestations.

The promotion gate blocks:

- AI-only or machine-only authority where accountable human review is required;
- wrong-revision reviews;
- expired time-sensitive reviews;
- stale synthetic translation fixtures;
- unresolved critical or major findings;
- hidden conflicts;
- incomplete contested, deprecated, or retracted transitions.

## Active complete slice

The first complete English review scope is:

`content/reviews/coverage/feedback-complete-vertical-slice.json`

It contains ten exact revision-1 entities and keeps both the formal result and model-to-world inference boundary load-bearing.

### Completed machine work

The repository commits and verifies exactly:

- 10 structural machine attestations;
- 3 fully specified recurrence-reproducibility attestations.

Every machine record is non-accountable and sets `permits_promotion: false`.

### Remaining human work

After machine attestations:

- 25 gate tasks remain;
- 0 tasks remain automation-eligible;
- all 25 remaining tasks require accountable humans.

They group into:

- 7 domain-authority tasks;
- 7 editorial-and-scope tasks;
- 5 methods-and-inference tasks;
- 5 source-and-provenance tasks;
- 1 independent reproducibility task for the generated source.

The slice remains `draft` and `blocked`.

## Validation

Install dependencies and run tests:

```bash
python -m pip install -r tools/foundation-validator/requirements.txt
python -m unittest discover -s tools/foundation-validator/tests -v
```

Validate authored content:

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
```

Verify deterministic machine records:

```bash
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

Generate complete-slice coverage:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report phase1-coverage.md
```

Generate the remaining review backlog:

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
3. [`docs/phase-1/README.md`](docs/phase-1/README.md)
4. [`docs/phase-1/review-protocol.md`](docs/phase-1/review-protocol.md)
5. [`docs/phase-1/machine-attestations.md`](docs/phase-1/machine-attestations.md)
6. [`docs/phase-1/feedback-human-review-plan.md`](docs/phase-1/feedback-human-review-plan.md)
7. [`docs/phase-1/feedback-vertical-slice-readiness.md`](docs/phase-1/feedback-vertical-slice-readiness.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

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

Phase 1 closes only when the complete English delayed-feedback slice has sufficient accountable exact-revision review coverage, no required critical or major finding remains unresolved, lifecycle transitions preserve history, dishonest authority paths fail, and a completion report recommends entry into Phase 2.

Passing a validator confirms only the checks it performs. It never turns a draft into authoritative knowledge by itself.

## License

MIT
