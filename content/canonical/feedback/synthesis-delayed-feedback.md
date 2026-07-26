---
contract: atlas-content/0.1
id: synthesis:en:delayed-feedback-and-oscillation
work: work:delayed-feedback-and-oscillation
type: synthesis
title: A delayed corrective recurrence can have a bounded periodic orbit
status: draft
revision: 2
created: 2026-07-26
updated: 2026-07-26
language: en
question: question:en:when-delayed-correction-can-oscillate
claims:
  - claim:en:stated-delayed-recurrence-oscillates
  - claim:en:model-oscillation-does-not-prove-real-system
models:
  - model:en:delayed-correction-recurrence
evidence_selection: Use the authoritative feedback reference for terminology and stability context, and use the reproducible generated sequence plus ordered-state proof for the exact recurrence. Do not treat model output as empirical observation.
conclusion: For gain 1, one-step delay, and initial state x0=1 and x1=0, the recurrence x[t+1]=x[t]-x[t-1] has an exact bounded period-six orbit. This demonstrates one mechanism by which delayed correction can produce oscillatory behavior, but it does not establish instability and does not transfer to a real system without separate evidence for model adequacy.
confidence: well-supported
confidence_rationale: The period-six result follows from exact arithmetic and return of the deterministic ordered state pair. The model-to-world conclusion is deliberately limited and consistent with the cited control-systems reference.
disagreements:
  - other gains, delays, nonlinearities, initial histories, and stability definitions can produce different behavior
  - periodic behavior is not synonymous with instability because a periodic orbit may remain bounded
open_questions:
  - should formal expressions receive their own contract subtype?
  - which stability definition is appropriate for each model class?
revision_triggers:
  - the arithmetic or ordered-state proof changes
  - the recurrence or assumptions change
  - empirical applications are introduced
  - a formal-expression contract is introduced
review:
  level: ai-reviewed
  record: ai-review:feedback-delayed-comprehensive
  reviewed_at: 2026-07-26
  human_verified: false
---

## Provenance path

`question:en:when-delayed-correction-can-oscillate` → `src:synthetic-feedback-run-delay-one-gain-one` → `evidence:en:delayed-feedback-periodic-sequence` → `claim:en:stated-delayed-recurrence-oscillates` → `model:en:delayed-correction-recurrence` and `concept:en:feedback` → this synthesis.

## Exact result

The sequence is `1, 0, -1, -1, 0, 1` and then repeats. Equality of the ordered state pairs `(x7, x6)` and `(x1, x0)` proves indefinite repetition under the deterministic second-order recurrence. The orbit is bounded and has exact period 6.

## Inference boundary

The exact model result is not evidence that delay always destabilizes feedback, that every observed oscillation is caused by delayed correction, or that a particular real system follows this recurrence.