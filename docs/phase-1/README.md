# Phase 1 — Reference Corpus, Review Gate, and Coverage

## Status

Active after Phase 0 acceptance at merge commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16` and the initial Phase 1 review-gate merge at `09488b76c43fdbe46f94fcb14a27637472adfa38`.

Phase 1 turns the accepted knowledge contract into a trustworthy review workflow. It does not build the general Atlas product and does not promote example content merely because it parses.

## Core question

Can Atlas prove, for an exact authored revision:

- what was reviewed;
- by whom and with what authority;
- which conflicts were disclosed;
- what findings remain open;
- whether the review is still current;
- which review classes remain missing;
- which internal or external dependents may be affected;
- which lifecycle transition is permitted;
- why promotion or slice closure is blocked?

## Workstreams

| Workstream | Output |
|---|---|
| Review contract | `atlas-review/0.1` schema and validation |
| Promotion gate | deterministic lifecycle decision with reasons |
| Coverage contract | `atlas-review-coverage/0.1` packet and slice reporting |
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
- summarize source limitations.

AI-assisted review may not independently satisfy:

- domain review;
- methodological review of empirical inference;
- ethical review;
- legal-context review;
- translation equivalence review;
- final editorial accountability.

Those reviews require accountable human judgment under the promotion policy.

## Phase 1 artifacts

```text
content/reviews/
  records/            # revision-specific review records
  fixtures/           # promotion and lifecycle test cases
  coverage/           # packet and future vertical-slice manifests

docs/phase-1/
  review-protocol.md
  promotion-policy.md
  coverage-and-dependency-reporting.md
  reviewer-submission-guide.md
  templates/          # reviewer submission example
  packets/            # reviewer-ready bounded packets
  reports/            # generated or signed review reports

tools/foundation-validator/
  phase1_review_gate.py
  phase1_coverage_report.py
  tests/test_phase1_review_gate.py
  tests/test_phase1_coverage_report.py
```

## Initial review packets

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

Each packet now has a coverage manifest for its target entity. The current manifests are expected to remain `blocked` until sufficient accountable human reviews are recorded. They are not complete vertical-slice manifests.

## Coverage commands

Validate manifests:

```bash
python tools/foundation-validator/phase1_coverage_report.py validate-manifest \
  content/reviews/coverage/*.json
```

Generate an honest current-state report:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-domain.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report phase1-reports/feedback-domain.md
```

`--expect blocked` verifies that known gaps remain visible. It does not grant a pass or change lifecycle state.

## Future Principia & Atlas compatibility

Coverage manifests can represent external dependents as opaque references. A future Principia artifact may therefore be listed as affected by an Atlas entity revision without making Atlas import, validate, or inherit Principia's pedagogical status.

No live Principia dependency is declared during Phase 1. The current work prepares a stable boundary only.

## Exit evidence

Phase 1 does not close because several review files or reports exist. It closes when:

- the review, promotion, and coverage contracts are executable;
- promotion and coverage decisions are deterministic and explainable;
- dishonest authority paths fail fixtures;
- lifecycle transitions preserve history;
- reviewer packets and submission templates are usable without code knowledge;
- at least one complete vertical slice reaches its intended lifecycle state through valid records;
- dependency impact is visible;
- all remaining gaps are visible and correctly scoped.

## Non-goals

- broad content production;
- a polished UI;
- search or retrieval redesign;
- autonomous review approval;
- replacing domain experts with AI;
- direct Principia integration or repository merger;
- selecting the final runtime architecture.
