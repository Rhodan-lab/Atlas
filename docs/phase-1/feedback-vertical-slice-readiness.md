# Delayed-Feedback Vertical-Slice Readiness

## Purpose

This package defines the first **complete English vertical-slice review scope** for Atlas Phase 1.

It does not claim that the slice is reviewed. It establishes the exact entity boundary, dependency graph, completed machine work, remaining human-review backlog, and authority requirements needed before lifecycle promotion can be considered.

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

The manifest uses `coverage_requirement: all`. Every listed entity must have acceptable exact-revision coverage before the slice can become coverage-complete.

## Load-bearing reasoning boundary

The formal result and methodological limitation are both load-bearing:

1. the stated recurrence produces the stated repeating sequence;
2. that result does not establish that a real system follows the model or will oscillate.

A future Principia explanation, investigation, simulation, or system dossier must not present the first statement while hiding the second.

## Language scope

The active authored scope is English-only.

Atlas retains language-neutral translation contracts and stale-source behavior as dormant infrastructure tested only through neutral synthetic fixtures. No active translated slice or language-specific review backlog exists.

## Dependency semantics

The manifest records `depends_on` links for governance impact, not runtime execution.

- periodic-sequence evidence depends on the generated source and model;
- the formal claim depends on evidence, model, and oscillation concept;
- the methodological claim depends on the reference, model, and conceptual boundary;
- the synthesis depends on the complete provenance path.

A revision, deprecation, or retraction of an upstream entity therefore exposes downstream items requiring inspection.

## Completed machine work

The accepted authority policy permits machines to satisfy only:

- structural conformance;
- fully specified reproducibility where the exact procedure is explicit.

`tools/foundation-validator/phase1_machine_attestations.py` generates and checks:

- 10 structural records, one for every exact entity revision in the slice;
- 3 reproducibility records for the formal claim, generated evidence, and recurrence model.

Every record is non-accountable and cannot permit promotion.

See [`machine-attestations.md`](machine-attestations.md).

## Reproducibility boundary

The recurrence procedure recalculates:

```text
x[t+1] = x[t] - x[t-1]
x[0] = 1
x[1] = 0
```

and confirms:

```text
1, 0, -1, -1, 0, 1, 1, 0
```

This establishes exact arithmetic reproduction only. It does not establish the best domain terminology, a general stability result, model adequacy, or real-system behavior.

## Generated reviewer backlog

`tools/foundation-validator/phase1_review_backlog.py` converts coverage into deterministic missing-review tasks recording:

- exact entity ID and revision;
- entity role and gate effect;
- execution mode;
- reviewer track and priority;
- allowed reviewer kinds and independence;
- accountability and qualification requirements;
- existing records and unresolved blockers;
- dependents;
- acceptance criteria.

The backlog does not assign a real person, perform review, resolve findings, or change lifecycle state.

## Current backlog

Before machine attestations:

- 38 gate tasks;
- 13 automation-eligible;
- 25 human-required.

After machine attestations:

- 25 gate tasks;
- 0 automation-eligible;
- 25 human-required;
- 0 advisory-only.

The remaining tasks group into:

- 7 domain-authority tasks;
- 7 editorial-and-scope tasks;
- 5 methods-and-inference tasks;
- 5 source-and-provenance tasks;
- 1 independent reproducibility task for the generated source.

See [`feedback-human-review-plan.md`](feedback-human-review-plan.md).

## Known major finding

The existing AI-assisted domain record for the formal claim has outcome `changes-required` and preserves the open major finding:

`finding:feedback:periodicity-proof`

The slice cannot advance until accountable review resolves the finding with an exact argument or keeps the affected entity blocked.

## Authority boundary

- machine checks satisfy only their declared structural or arithmetic scope;
- AI-assisted work may identify defects and prepare reviewer questions;
- machine and AI-assisted records set `accountable: false`;
- neither can permit promotion;
- source, editorial, domain, methods, and remaining reproducibility tasks require accountable humans under policy;
- no coverage or backlog report changes `draft` status;
- no synthetic translation fixture establishes a supported authored language.

## Future Principia boundary

The complete slice is the kind of Atlas knowledge unit that Principia may later consume.

Atlas can report when upstream revisions affect a Principia explanation, investigation, simulation, or system dossier. Principia still owns pedagogical design and release status, while Atlas owns knowledge identity, provenance, review, lifecycle, and staleness.

No live Principia dependency is introduced in Phase 1.

## Commands

Verify machine records:

```bash
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

Generate remaining backlog:

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

The slice remains `blocked` because 25 accountable human-review tasks remain. Phase 1 still requires real exact-revision reviews, resolution or preservation of every major finding, coverage regeneration, and a completion report before entry into Phase 2.
