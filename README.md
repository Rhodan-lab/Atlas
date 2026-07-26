# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)
[![Foundation Contract](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml)
[![Phase 1 Review Gate](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml)

> **Current status: Phase 1 — English Reference Corpus and Accountable Exact-Revision Review**
>
> Phase 0 established the knowledge contract. Phase 1 proves review coverage, bounded machine authority, accountable-human handoff, exact-snapshot return provenance, explicit review-record admission, lifecycle integrity, and dependency impact before product expansion.

## What Atlas is

Atlas is a local-first knowledge and governance environment for an independent learner, researcher, or builder. It makes reasoning inspectable:

- what a claim states and where it applies;
- what evidence supports, challenges, or contextualizes it;
- which model, assumptions, argument, or values lead to a conclusion;
- how certain, limited, contested, stale, deprecated, or retracted an item is;
- how a synthesis traces to original sources;
- what was reviewed, by whom or by which deterministic procedure, for which revision, and with which unresolved findings;
- which exact content snapshot was handed to a reviewer and returned;
- who admitted a returned review record into Atlas history and which external checks were declared;
- why knowledge changed through revision.

Atlas is not merely a notes app, graph visualization, textbook, course platform, or chatbot.

## Future Principia & Atlas role

Atlas is being built as the knowledge and governance layer of a future **Principia & Atlas** system.

- **Atlas** owns canonical knowledge identity, sources, evidence, claims, models, provenance, review, revision, lifecycle, and staleness.
- **Principia** will own causal explanation, pathways, investigations, simulations, system dossiers, failure analysis, and design experiences.
- Principia may depend on Atlas entities without inheriting authority automatically.
- Atlas may report which Principia artifacts are affected by upstream knowledge changes without taking ownership of pedagogical release status.

No live cross-repository dependency exists during Phase 1.

## Authority order

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. accepted foundation documents in [`docs/foundation/`](docs/foundation/)
3. accepted ADRs
4. canonical authored content and committed exact-revision review records
5. generated reports, manifests, backlogs, handoff bundles, intake artifacts, and admission receipts
6. experimental implementation code

Tools may establish bounded conformance, arithmetic reproduction, task-to-snapshot integrity, submission consistency, or admission-declaration consistency. They cannot establish scientific truth, source interpretation, model applicability, reviewer identity, reviewer qualification, reviewer independence, legal correctness, ethical acceptability, editorial quality, or lifecycle authority by themselves.

## Language scope

The active authored and review corpus is **English-only**.

Atlas retains language-neutral translation semantics—shared `work` identity, source-revision pinning, independent lifecycle, and stale-translation detection—but they are exercised only by neutral synthetic fixtures during the current phase.

There is no active translated vertical slice, language-specific review packet, bilingual terminology program, or supported authored language beyond English.

## Executable English corpus

`content/canonical/` contains **34 entity files** across three vertical slices:

1. **Catalase and assay conditions** — empirical evidence, measurement proxies, assay scope, and methodological limitations.
2. **Delayed feedback and oscillation** — formal model, reproducible derived evidence, assumptions, and model-to-world limits.
3. **Recommendation systems and user choice** — observational and randomized evidence, legal context, conflicts, and explicit normative reasoning.

Each slice supports:

```text
question → source → evidence → claim → concept/model → synthesis → revision trigger
```

## Phase 1 contracts

- `atlas-review/0.1` — exact-revision review records;
- `atlas-promotion/0.1` — deterministic lifecycle decisions;
- `atlas-review-coverage/0.1` — packet and complete-slice coverage;
- `atlas-review-backlog/0.1` — deterministic missing-review tasks;
- `atlas-review-handoff/0.1` — generated accountable-human review bundles;
- `atlas-review-submission/0.1` — exact-task and exact-snapshot return envelopes;
- `atlas-review-admission/0.1` — explicit human-maintainer decisions about entry into review history.

The promotion gate blocks AI-only or machine-only authority where humans are required, wrong-revision reviews, expired reviews, unresolved serious findings, hidden conflicts, and incomplete lifecycle transitions.

## Active complete slice

The first complete English review scope is:

`content/reviews/coverage/feedback-complete-vertical-slice.json`

It contains ten exact revision-1 entities and keeps both the formal result and model-to-world inference boundary load-bearing.

### Completed machine work

The repository commits and verifies:

- 10 structural machine attestations;
- 3 fully specified recurrence-reproducibility attestations.

Every machine record is non-accountable and sets `permits_promotion: false`.

### Remaining human work

- 25 gate tasks remain;
- 0 tasks remain automation-eligible;
- all 25 tasks require accountable humans.

They group into 7 domain, 7 editorial, 5 methods, 5 source/provenance, and 1 independent reproducibility task. The slice remains `draft` and `blocked`.

## Accountable-human handoff

```bash
python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir phase1-reports/human-review-handoff \
  --expect-task-count 25 \
  --expect-track-count 5
```

The output contains five qualification-track bundles, all 25 tasks exactly once, ten byte-for-byte canonical snapshots, original paths and SHA-256 digests, existing blockers and dependents, acceptance criteria, and no reviewer assignment.

## Exact-snapshot review return

Validate a returned submission:

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Extract a proposed review record with intake lineage:

```bash
python tools/foundation-validator/phase1_review_intake.py extract \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/extracted-review.json
```

Intake verifies the active task, exact revision and snapshot digest, review type, human accountability, required independence, qualification, conflicts, dates, and AI-assistance disclosure.

A passing envelope or extracted record is not accepted automatically and is never written to `content/reviews/records/` by the tool.

## Explicit review admission

Validate an accountable maintainer decision:

```bash
python tools/foundation-validator/phase1_review_admission.py validate \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Prepare an accepted review record for normal repository review:

```bash
python tools/foundation-validator/phase1_review_admission.py prepare \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --records-dir content/reviews/records \
  --out phase1-reports/proposed-admitted-review.json
```

Admission records whether a review record may enter Atlas history. It does **not** accept the reviewed knowledge.

A legitimate `changes-required` review or review with major findings may be admitted so criticism is preserved. The outcome and findings remain unchanged, and the promotion gate continues to block the knowledge where appropriate.

The tool rejects duplicate review IDs, requires explicit external-verification declarations for `accept`, preserves intake and admission lineage, and writes only to the explicit output path.

Synthetic admissions force `permits_promotion: false`.

## Validation

```bash
python -m pip install -r tools/foundation-validator/requirements.txt
python -m unittest discover -s tools/foundation-validator/tests -v
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

These commands produce conformance, planning, evidence-transfer, intake-consistency, or admission-consistency output only. They never edit lifecycle status automatically.

## Reading path

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/README.md`](docs/foundation/README.md)
3. [`docs/phase-1/README.md`](docs/phase-1/README.md)
4. [`docs/phase-1/review-protocol.md`](docs/phase-1/review-protocol.md)
5. [`docs/phase-1/machine-attestations.md`](docs/phase-1/machine-attestations.md)
6. [`docs/phase-1/human-review-handoff.md`](docs/phase-1/human-review-handoff.md)
7. [`docs/phase-1/review-intake.md`](docs/phase-1/review-intake.md)
8. [`docs/phase-1/review-admission.md`](docs/phase-1/review-admission.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Still frozen during Phase 1

- product UI expansion;
- new services or programming languages;
- specialized retrieval architecture;
- plugins and synchronization;
- active translated corpus or language-specific review programs;
- AI-generated authoritative content;
- automatic reviewer assignment, external verification, admission, or review-record commitment;
- direct Principia integration or repository merger;
- promotion of experimental runtime structures as canonical.

## Phase boundary

Phase 1 closes only when the complete English delayed-feedback slice has sufficient accountable exact-revision review coverage, no required critical or major finding remains unresolved, lifecycle transitions preserve history, dishonest authority paths fail, and a completion report recommends entry into Phase 2.

Passing validators, generating handoffs, validating intake, or preparing an admitted record never turns a draft into authoritative knowledge by itself.

## License

MIT
