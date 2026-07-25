# Phase 1 — Reference Corpus, Review Gate, Coverage, and Readiness

## Status

Active after:

- Phase 0 acceptance at `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- initial Phase 1 review-gate merge at `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency-reporting merge at `c67457ae2c369d57b00b1cd22f454245ebf6ac13`.

Phase 1 turns the accepted knowledge contract into a trustworthy review workflow. It does not build the general Atlas product and does not promote example content merely because it parses or generates a report.

## Core question

Can Atlas prove, for an exact authored revision:

- what was reviewed;
- by whom and with what authority;
- which conflicts were disclosed;
- what findings remain open;
- whether the review is still current;
- which review classes remain missing;
- which human-review tasks must happen next;
- which internal or external dependents may be affected;
- which lifecycle transition is permitted;
- why promotion or slice closure is blocked?

## Workstreams

| Workstream | Output |
|---|---|
| Review contract | `atlas-review/0.1` schema and validation |
| Promotion gate | deterministic lifecycle decision with reasons |
| Coverage contract | `atlas-review-coverage/0.1` packet and slice reporting |
| Review backlog | `atlas-review-backlog/0.1` deterministic missing-review tasks |
| Review packets | bounded domain and translation packets |
| Review records | exact-revision internal, AI-assisted, and independent records |
| Reviewer submission | code-independent guide and JSON example |
| Lifecycle fixtures | reviewed, contested, deprecated, retracted, and stale cases |
| Dependency impact | internal reverse links and optional opaque external dependents |
| Contract challenge | reopen Phase 0 only when a real fixture fails |

## Review authority boundary

Machine validation may satisfy structural conformance and reproducibility checks where the computation is fully specified.

AI-assisted review may:

- identify candidate issues;
- compare terminology;
- draft questions;
- flag missing evidence;
- summarize source limitations;
- generate a review backlog.

AI-assisted review may not independently satisfy:

- domain review;
- methodological review of empirical or model-to-world inference;
- ethical review;
- legal-context review;
- translation equivalence review;
- final editorial accountability.

Those reviews require accountable human judgment under the promotion policy. A generated backlog is not a review record.

## Phase 1 artifacts

```text
content/reviews/
  records/            # revision-specific review records
  fixtures/           # promotion and lifecycle test cases
  coverage/           # packet, complete-slice, and translation-overlay manifests

docs/phase-1/
  review-protocol.md
  promotion-policy.md
  coverage-and-dependency-reporting.md
  reviewer-submission-guide.md
  feedback-vertical-slice-readiness.md
  templates/          # reviewer submission example
  packets/            # reviewer-ready bounded packets
  reports/            # generated or signed review reports

tools/foundation-validator/
  phase1_review_gate.py
  phase1_coverage_report.py
  phase1_review_backlog.py
  tests/test_phase1_review_gate.py
  tests/test_phase1_coverage_report.py
  tests/test_phase1_review_backlog.py
```

## Bounded review packets

1. **Catalase and assay conditions**
   - enzyme-source and assay-scope terminology;
   - proxy measurement limits;
   - pH and temperature generalization;
   - distinction between reaction rate and thermal stability.

2. **Delayed feedback and oscillation**
   - recurrence arithmetic;
   - oscillation and stability terminology;
   - boundedness versus convergence;
   - model-to-world inference boundary.

3. **Recommender exposure and governance**
   - observational versus randomized evidence;
   - platform and timeframe dependence;
   - DSA Articles 27 and 38;
   - legal updates and review horizon;
   - autonomy, accountability, accessibility, safety, and feasibility trade-offs.

4. **Indonesian translation equivalence**
   - mathematical meaning;
   - control-systems terminology;
   - qualifier preservation;
   - stale-source behavior.

Each bounded packet has a coverage manifest for its target entity. Those manifests remain expected `blocked` until sufficient accountable human review exists.

## First complete vertical-slice readiness scope

The delayed-feedback slice is the first complete readiness scope because it combines a question, source provenance, generated evidence, a formal model, model-derived and methodological claims, concepts, synthesis, and an Indonesian translation path.

### English complete slice

`content/reviews/coverage/feedback-complete-vertical-slice.json`

- contains all ten split English entities;
- uses `coverage_requirement: all`;
- records the complete governance dependency graph;
- remains `draft` and expected `blocked`.

### Indonesian translation overlay

`content/reviews/coverage/feedback-id-translation-overlay.json`

- contains all eight translated entities;
- retains shared English sources as context;
- treats every translated entity as load-bearing;
- requires independent translation and domain authority;
- remains independently blocked even if English coverage later passes.

See [`feedback-vertical-slice-readiness.md`](feedback-vertical-slice-readiness.md).

## Coverage commands

Validate manifests:

```bash
python tools/foundation-validator/phase1_coverage_report.py validate-manifest \
  content/reviews/coverage/*.json
```

Generate an honest current-state report:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report phase1-reports/feedback-complete-vertical-slice.md
```

`--expect blocked` verifies that known gaps remain visible. It does not grant a pass or change lifecycle state.

## Review backlog commands

Generate the English complete-slice backlog:

```bash
python tools/foundation-validator/phase1_review_backlog.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --json-out phase1-reports/backlog-feedback-en.json \
  --report phase1-reports/backlog-feedback-en.md
```

Generate the Indonesian translation backlog:

```bash
python tools/foundation-validator/phase1_review_backlog.py \
  content/reviews/coverage/feedback-id-translation-overlay.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --json-out phase1-reports/backlog-feedback-id.json \
  --report phase1-reports/backlog-feedback-id.md
```

The backlog records exact revision, missing review type, reviewer authority, priority, blockers, dependents, and acceptance criteria. It does not assign a person or count as completed review.

## Future Principia & Atlas compatibility

Coverage manifests can represent external dependents as opaque references. A future Principia artifact may therefore be listed as affected by an Atlas entity revision without making Atlas import, validate, or inherit Principia's pedagogical status.

The complete delayed-feedback slice demonstrates the future boundary:

- Atlas owns knowledge identity, evidence, provenance, review, lifecycle, and staleness;
- Principia may depend on a model, claim, concept, or synthesis;
- Atlas reports upstream knowledge impact;
- Principia owns explanation, investigation, simulation, pedagogy, and release status;
- neither system inherits authority automatically.

No live Principia dependency is declared during Phase 1.

## Exit evidence

Phase 1 does not close because several review files, complete manifests, or backlogs exist. It closes when:

- the review, promotion, coverage, and backlog semantics are executable;
- promotion and coverage decisions are deterministic and explainable;
- dishonest authority paths fail fixtures;
- lifecycle transitions preserve history;
- reviewer packets and submission templates are usable without code knowledge;
- at least one complete vertical slice reaches its intended lifecycle state through valid accountable records;
- translated status is independently justified;
- dependency impact is visible;
- all remaining gaps are visible and correctly scoped;
- a completion report recommends or rejects Phase 2.

## Non-goals

- broad content production;
- a polished UI;
- search or retrieval redesign;
- autonomous review approval;
- replacing domain experts with AI;
- direct Principia integration or repository merger;
- selecting the final runtime architecture.
