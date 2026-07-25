# Phase 1 — Reference Corpus and Review Gate

## Status

Active after Phase 0 acceptance at merge commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`.

Phase 1 turns the accepted knowledge contract into a trustworthy review workflow. It does not build the general Atlas product and does not promote example content merely because it parses.

## Core question

Can Atlas prove, for an exact authored revision:

- what was reviewed;
- by whom and with what authority;
- which conflicts were disclosed;
- what findings remain open;
- whether the review is still current;
- which lifecycle transition is permitted;
- why promotion is blocked when requirements are not met?

## Workstreams

| Workstream | Output |
|---|---|
| Review contract | `atlas-review/0.1` schema and validation |
| Promotion gate | deterministic decision with reasons |
| Review packets | bounded domain and translation packets |
| Review records | exact-revision internal, AI-assisted, and independent records |
| Lifecycle fixtures | reviewed, contested, deprecated, retracted, and stale cases |
| Coverage report | human-readable missing-review and blocker report |
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

docs/phase-1/
  review-protocol.md
  promotion-policy.md
  packets/            # reviewer-ready bounded packets
  reports/            # generated or signed review reports

tools/foundation-validator/
  phase1_review_gate.py
  tests/test_phase1_review_gate.py
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

## Exit evidence

Phase 1 does not close because several review files exist. It closes when:

- the review contract is executable;
- promotion decisions are deterministic and explainable;
- dishonest authority paths fail fixtures;
- lifecycle transitions preserve history;
- reviewer packets are usable without code knowledge;
- at least one vertical slice reaches its intended lifecycle state through valid records;
- all remaining gaps are visible and correctly scoped.

## Non-goals

- broad content production;
- a polished UI;
- search or retrieval redesign;
- autonomous review approval;
- replacing domain experts with AI;
- selecting the final runtime architecture.
