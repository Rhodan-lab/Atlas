# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)
[![Foundation Contract](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/foundation.yml)
[![Phase 1 AI Review](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase1-review.yml)
[![Phase 2 Closure](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase2-closure.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/phase2-closure.yml)

> **Current status: Phase 3 — Retrieval Evaluation**
>
> Phase 1 completed an explicitly labeled AI review of the English delayed-feedback slice. Phase 2 completed the deterministic, read-only, replaceable knowledge kernel and accepted bounded entry into retrieval evaluation. Human verification remains optional and separately labeled. Retrieval remains advisory, exact-revision, provenance-visible, replaceable, and `live: false`.

## What Atlas is

Atlas is a local-first knowledge and governance environment for inspectable reasoning:

- what a claim states and where it applies;
- what evidence supports or challenges it;
- which model, assumptions, argument, or values lead to a conclusion;
- how a synthesis traces to sources;
- which exact revision was reviewed or retrieved;
- whether the review was machine, AI, or human;
- which findings remain open;
- which dependents are affected when knowledge changes.

Atlas is not merely a notes app, graph visualization, textbook, course platform, search box, or chatbot.

## Principia & Atlas role

Atlas is the knowledge and governance layer of a future **Principia & Atlas** system.

- **Atlas** owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- **Principia** owns causal explanation, pathways, investigations, simulations, system dossiers, failure analysis, design experiences, and its own publication readiness.
- Principia may reference exact Atlas revisions without inheriting status automatically.
- Atlas may report which Principia artifacts are affected by upstream changes.

No live cross-repository dependency is active. Phase 3 does not change that boundary.

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

AI review is sufficient for current Atlas development. It is not human verification.

### Human-verified

Human verification is an optional stronger layer. Historical handoff, intake, admission, coverage, and promotion tools remain available, but they are not active Phase 3 duties.

Atlas must never describe an AI review as human verification or invent identity, qualifications, independence, or accountability.

## English reference corpus

`content/canonical/` contains 34 exact entity revisions across three vertical slices:

1. **Catalase and assay conditions**
2. **Delayed feedback and oscillation**
3. **Recommendation systems and user choice**

The delayed-feedback slice is the completed Phase 1 review reference.

## Phase 1 — AI-reviewed reference slice

Machine-readable record:

`content/reviews/ai/feedback-delayed-comprehensive.json`

Readable report:

[`docs/phase-1/ai-review-report.md`](docs/phase-1/ai-review-report.md)

For:

```text
x[t+1] = x[t] - x[t-1]
x0 = 1
x1 = 0
```

the ordered state returns after six steps, so the exact orbit is bounded and periodic with period 6. This does not prove instability and does not establish behavior in a real system.

## Phase 2 — completed minimal knowledge kernel

Phase 2 established:

- deterministic canonical-to-runtime compilation;
- strict serialized-runtime admission;
- exact-revision read-only lookup;
- typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- safe deterministic failures;
- exact-revision non-live Principia compatibility;
- atomic offline protocol validation;
- representative and 1,026-entity scaled measurements;
- receipt replay, idempotency, and recovery semantics;
- an independent portable query engine;
- 136 query-equivalence checks over all 34 canonical revisions;
- deterministic migration and rollback rebuilding.

Completion report:

[`docs/phase-2/completion-report.md`](docs/phase-2/completion-report.md)

Accepted Phase 2 decision:

```yaml
completion: accepted
retrieval_entry: proceed-bounded-retrieval-evaluation
live: false
repository_mutation: false
```

Generated runtimes and indexes remain disposable. Canonical Markdown remains authoritative.

## Phase 3 — Retrieval Evaluation

Phase 3 evaluates retrieval quality without weakening identity, provenance, lifecycle, review, or replaceability guarantees.

Initial required work:

- define versioned query-and-judgment fixtures;
- implement deterministic lexical retrieval;
- implement deterministic structured-field retrieval;
- define relevance metrics and tie-breaking;
- preserve exact IDs, revisions, provenance, review level, lifecycle, and staleness in every result;
- test index deletion and canonical rebuild;
- compare embedding or vector candidates only after accepted baselines exist.

Phase plan:

[`docs/phase-3/README.md`](docs/phase-3/README.md)

## Validation

```bash
python -m pip install -r tools/foundation-validator/requirements.txt
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
python tools/foundation-validator/phase1_ai_review.py \
  content/reviews/ai/feedback-delayed-comprehensive.json \
  --canonical-root content/canonical
python -m tools.phase2_kernel.closure \
  --output phase2-completion-report.json
```

## Reading path

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/README.md`](docs/foundation/README.md)
3. [`docs/phase-1/ai-review-report.md`](docs/phase-1/ai-review-report.md)
4. [`docs/phase-2/completion-report.md`](docs/phase-2/completion-report.md)
5. [`docs/phase-3/README.md`](docs/phase-3/README.md)
6. [`docs/roadmap.md`](docs/roadmap.md)

Contributors and agents must follow [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Still frozen

- production retrieval-quality claims;
- polished product UI;
- vector database commitment before comparative evaluation;
- unversioned or implicit `latest` lookup;
- retrieval-generated canonical writes;
- automatic review, lifecycle, promotion, or release mutation;
- live Principia synchronization;
- plugins and autonomous synchronization;
- active translated corpus;
- hidden AI authority claims;
- automatic conversion of AI review into human verification;
- direct Principia repository merger.

## License

MIT
