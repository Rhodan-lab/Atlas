# Delayed-Feedback Vertical-Slice Readiness

## Purpose

This package turns the delayed-feedback reference material from a collection of reviewed targets into the first **complete vertical-slice readiness scope** for Atlas Phase 1.

It does not claim that the slice is reviewed. It establishes the exact entity boundary, dependency graph, translation overlay, missing-review backlog, and reviewer-authority requirements needed before any lifecycle promotion can be considered.

## Why this slice

Delayed feedback exercises several foundation requirements at once:

- a formal and reproducible model;
- generated evidence with explicit provenance;
- a model-derived claim;
- a methodological claim limiting model-to-world transfer;
- controlled scientific terminology;
- synthesis-level provenance;
- English–Indonesian translation lineage;
- future dependency impact for Principia artifacts.

A slice that contains only a factual claim would not stress these boundaries as strongly.

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

## Indonesian translation overlay

`content/reviews/coverage/feedback-id-translation-overlay.json` represents the complete Indonesian translation path while retaining the two English sources as context.

The overlay uses `coverage_requirement: load-bearing`:

- every translated entity is load-bearing;
- shared English source records are context;
- translation status remains independent from English lifecycle status;
- a current English source revision is necessary but not sufficient for translation approval.

The translation path requires bilingual technical review. Structural similarity and machine comparison cannot establish equivalence for terms such as feedback, state, recurrence, gain, delay, oscillation, periodicity, and stability.

## Dependency semantics

The manifests record `depends_on` links for governance impact, not runtime execution.

Examples:

- the periodic-sequence evidence depends on the generated source and model;
- the formal claim depends on the evidence, model, and oscillation concept;
- the methodological claim depends on the model and conceptual boundary;
- the synthesis depends on the complete provenance path;
- translated claims depend on translated evidence, model, and concepts.

A revision, deprecation, or retraction of an upstream entity therefore exposes the downstream items that require inspection.

## Generated reviewer backlog

`tools/foundation-validator/phase1_review_backlog.py` converts a coverage result into deterministic review tasks.

For every missing review type, it records:

- exact entity ID and revision;
- entity role and whether the task blocks the selected gate;
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
7. translation equivalence;
8. independence and conflicts when required.

A single qualified reviewer may cover more than one track only when the review record honestly documents qualification, independence, accountability, and conflicts for each review type.

## Authority boundary

- machine checks may satisfy structural review;
- machine checks may satisfy fully specified reproducibility where allowed by policy;
- AI-assisted work may identify defects and create reviewer questions;
- AI-assisted work cannot satisfy accountable domain, methodological, translation, ethical, legal-context, or final editorial authority;
- no generated backlog task counts as a completed review;
- no coverage report changes `draft` status.

## Future Principia boundary

The complete slice is the kind of Atlas knowledge unit that Principia may later consume.

A Principia explanation, investigation, simulation, or system dossier may depend on the model, claims, or synthesis. Atlas can report that such an artifact requires impact inspection when an upstream revision changes. Principia still owns pedagogical design and release status, while Atlas owns knowledge identity, provenance, review, lifecycle, and staleness.

No live Principia dependency is introduced in Phase 1.

## Commands

Generate the English backlog:

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

`--expect blocked` verifies that missing authority remains visible. It does not convert the result into a pass.

## Current honest status

Both manifests are expected to remain `blocked` because sufficient accountable human review records do not yet exist.

This package completes the **readiness infrastructure** for one vertical slice. Phase 1 still requires real reviews, resolution or preservation of major findings, coverage regeneration, and a completion report before entry into Phase 2.
