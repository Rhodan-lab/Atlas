# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)
[![Foundation Contract](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml)
[![Phase 1 AI Review](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml)

> **Current status: Phase 2 — Minimal Knowledge Kernel**
>
> Phase 0 established the authored knowledge contract. Phase 1 completed an explicitly labeled AI review of the English delayed-feedback slice, corrected its formal proof and inference boundaries, and removed the former mandatory human-review queue. Human verification remains optional and separately labeled.

## What Atlas is

Atlas is a local-first knowledge and governance environment for inspectable reasoning:

- what a claim states and where it applies;
- what evidence supports or challenges it;
- which model, assumptions, argument, or values lead to a conclusion;
- how a synthesis traces to sources;
- which exact revision was reviewed;
- whether the review was machine, AI, or human;
- which findings remain open;
- which dependents are affected when knowledge changes.

Atlas is not merely a notes app, graph visualization, textbook, course platform, or chatbot.

## Future Principia & Atlas role

Atlas is being built as the knowledge and governance layer of a future **Principia & Atlas** system.

- **Atlas** owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- **Principia** will own causal explanation, pathways, investigations, simulations, system dossiers, failure analysis, and design experiences.
- Principia may reference exact Atlas revisions without inheriting status automatically.
- Atlas may report which Principia artifacts are affected by upstream changes.

No live cross-repository dependency exists at the start of Phase 2.

## Language scope

The active authored and review corpus is **English-only**.

Language-neutral translation identity and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures.

## Review levels

### AI-reviewed

The active Phase 1 review level is `ai-reviewed`.

An AI-reviewed artifact records:

- AI reviewer identity and model family;
- exact canonical revisions;
- source checks;
- mathematical or reproducibility checks where applicable;
- findings and corrections;
- explicit limitations;
- `human_verified: false`.

AI review is sufficient for current Atlas development.

### Human-verified

Human verification is an optional stronger layer. Historical handoff, intake, admission, coverage, and promotion tools remain available, but they are not active duties and do not block Phase 2.

Atlas must never describe an AI review as human verification or invent identity, qualifications, independence, or accountability.

## English reference corpus

`content/canonical/` contains 34 entity files across three vertical slices:

1. **Catalase and assay conditions**
2. **Delayed feedback and oscillation**
3. **Recommendation systems and user choice**

The delayed-feedback slice is the completed Phase 1 review reference.

## Completed delayed-feedback review

Machine-readable record:

`content/reviews/ai/feedback-delayed-comprehensive.json`

Readable report:

[`docs/phase-1/ai-review-report.md`](docs/phase-1/ai-review-report.md)

The review covers all ten entities and records `overall_outcome: pass`, `review_level: ai-reviewed`, and `human_review_required: false`.

### Corrected mathematical result

For:

```text
x[t+1] = x[t] - x[t-1]
x0 = 1
x1 = 0
```

the sequence is:

```text
1, 0, -1, -1, 0, 1, 1, 0, ...
```

The ordered pair `(x1, x0) = (0, 1)` returns as `(x7, x6) = (0, 1)`. Since the recurrence is deterministic in that ordered pair, the sequence repeats. Periods 1, 2, and 3 are excluded by the first six states, so the exact period is 6.

The orbit is bounded and periodic. This does not prove instability and does not establish behavior in a real system.

### Resolved findings

- insufficient periodicity proof;
- ambiguity between oscillation and instability;
- unclear boundary between the textbook reference and the independently derived recurrence result.

## Validate the AI review

```bash
python -m pip install -r tools/foundation-validator/requirements.txt
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
python tools/foundation-validator/phase1_ai_review.py \
  content/reviews/ai/feedback-delayed-comprehensive.json \
  --canonical-root content/canonical
```

The validator confirms the explicit AI identity, exact entity set and revisions, source locator, recurrence sequence, period-six proof, resolved serious findings, and absence of a mandatory human-review duty.

## Optional human verification tooling

The following remain available as optional governance experiments:

- `phase1_review_gate.py`
- `phase1_coverage_report.py`
- `phase1_review_backlog.py`
- `phase1_human_review_handoff.py`
- `phase1_review_intake.py`
- `phase1_review_admission.py`

They are not run as active Phase 1 gates and do not define project progress.

## Phase 2 — Minimal Knowledge Kernel

Phase 2 implements only the dependable runtime needed by the authored contract:

- canonical-to-runtime compilation;
- exact-revision read-only lookup;
- typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- deterministic command or library interface;
- compatibility and failure tests;
- representative performance measurements.

The kernel must remain replaceable without changing authored Markdown.

## Reading path

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/README.md`](docs/foundation/README.md)
3. [`docs/phase-1/ai-review-report.md`](docs/phase-1/ai-review-report.md)
4. [`docs/roadmap.md`](docs/roadmap.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Still frozen

- polished product UI;
- specialized retrieval and ranking;
- synchronization and plugins;
- active translated corpus;
- hidden AI authority claims;
- automatic conversion of AI review into human verification;
- direct Principia repository merger;
- promotion of prototype runtime formats before Phase 2 evaluation.

## License

MIT
