# Delayed-Feedback Vertical-Slice Readiness

## Purpose

This package turns the delayed-feedback reference material into the first **complete English vertical-slice readiness scope** for Atlas Phase 1.

It does not claim that the slice is reviewed. It establishes the exact entity boundary, dependency graph, missing-review backlog, automation boundary, and reviewer-authority requirements needed before any lifecycle promotion can be considered.

## Why this slice

Delayed feedback exercises several foundation requirements at once:

- a formal and reproducible model;
- generated evidence with explicit provenance;
- a model-derived claim;
- a methodological claim limiting model-to-world transfer;
- controlled scientific terminology;
- synthesis-level provenance;
- future dependency impact for Principia artifacts.

A slice containing only one factual claim would not stress these boundaries as strongly.

## Complete English scope

`content/reviews/coverage/feedback-complete-vertical-slice.json` includes the exact revision-1 entities for:

- the research question;
- the authoritative feedback reference;
- the generated model-run source;
- the periodic-sequence evidence;
- the formal oscillation claim;
- the model-to-world inference-boundary claim;
- feedback and oscillation concepts;
- the delayed-correction recurrence model;
- the synthesis.

The manifest uses `coverage_requirement: all`. Every listed entity must therefore have acceptable exact-revision review coverage before the slice can be described as coverage-complete.

## Load-bearing reasoning boundary

The formal result and the methodological limitation are both load-bearing:

1. the stated recurrence produces the stated repeating sequence;
2. that formal result does not establish that a real system follows the model or will oscillate.

A future Principia explanation or simulation must not present the first statement while hiding the second.

## Language scope

The active authored scope is English-only.

Atlas retains language-neutral translation contracts and stale-source behavior as dormant infrastructure, tested only through synthetic fixtures. There is no active translated slice, language-specific review packet, or translation backlog in Phase 1.

## Dependency semantics

The manifest records `depends_on` links for governance impact, not runtime execution.

Examples:

- the periodic-sequence evidence depends on the generated source and model;
- the formal claim depends on the evidence, model, and oscillation concept;
- the methodological claim depends on the model and conceptual boundary;
- the synthesis depends on the complete provenance path.

A revision, deprecation, or retraction of an upstream entity therefore exposes downstream items that require inspection.

## Generated reviewer backlog

`tools/foundation-validator/phase1_review_backlog.py` converts a coverage result into deterministic review tasks.

For every missing review type, it records:

- exact entity ID and revision;
- entity role and whether the task blocks the selected gate;
- execution mode: `automation-eligible` or `human-required`;
- reviewer track;
- task priority;
- allowed reviewer kinds;
- required independence;
- whether accountability is mandatory;
- existing review records that do not yet satisfy authority;
- unresolved blockers;
- internal and external dependents;
- acceptance criteria.

The backlog does not assign a real person. It does not perform review, resolve findings, or change lifecycle state.

## Reviewer tracks

The generated work is separated into bounded tracks:

1. contract conformance;
2. editorial and scope;
3. source and provenance;
4. domain authority;
5. methods and inference;
6. reproducibility;
7. independence and conflicts when required.

A single qualified reviewer may cover more than one track only when the review record honestly documents qualification, independence, accountability, and conflicts for each review type.

## Current backlog

The current complete English slice generates:

- 38 gate tasks;
- 13 automation-eligible tasks;
- 25 human-required tasks;
- no advisory-only tasks.

These are exact entity/review-type tasks, not a required number of distinct reviewers.

## Authority boundary

- machine checks may satisfy structural review;
- machine checks may satisfy fully specified reproducibility where allowed by policy;
- AI-assisted work may identify defects and create reviewer questions;
- AI-assisted work cannot satisfy accountable domain, methodological, ethical, legal-context, or final editorial authority;
- no generated backlog task counts as a completed review;
- no coverage report changes `draft` status;
- no synthetic translation fixture establishes a supported authored language.

## Future Principia boundary

The complete slice is the kind of Atlas knowledge unit that Principia may later consume.

A Principia explanation, investigation, simulation, or system dossier may depend on the model, claims, concepts, or synthesis. Atlas can report that such an artifact requires impact inspection when an upstream revision changes. Principia still owns pedagogical design and release status, while Atlas owns knowledge identity, provenance, review, lifecycle, and staleness.

No live Principia dependency is introduced in Phase 1.

## Command

```bash
python tools/foundation-validator/phase1_review_backlog.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --json-out phase1-reports/backlog-feedback-en.json \
  --report phase1-reports/backlog-feedback-en.md
```

`--expect blocked` verifies that missing authority remains visible. It does not convert the result into a pass.

## Current honest status

The manifest is expected to remain `blocked` because sufficient accountable human review records do not yet exist.

This package completes the **readiness infrastructure** for one English vertical slice. Phase 1 still requires valid machine attestations, real accountable reviews, resolution or preservation of major findings, coverage regeneration, and a completion report before entry into Phase 2.
