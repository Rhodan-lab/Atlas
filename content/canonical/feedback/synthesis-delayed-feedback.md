---
contract: atlas-content/0.1
id: synthesis:en:delayed-feedback-and-oscillation
work: work:delayed-feedback-and-oscillation
type: synthesis
title: A delayed corrective recurrence can oscillate under stated assumptions
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
question: question:en:when-delayed-correction-can-oscillate
claims:
  - claim:en:stated-delayed-recurrence-oscillates
  - claim:en:model-oscillation-does-not-prove-real-system
models:
  - model:en:delayed-correction-recurrence
evidence_selection: Use the authoritative feedback reference for terminology and a reproducible generated sequence for the exact recurrence; do not treat model output as empirical observation.
conclusion: The stated one-step delayed corrective recurrence produces a repeating sequence for the stated gain and initial values. This demonstrates one mechanism by which delayed correction can produce oscillatory behavior, but applying the result to a real system requires separate evidence for model adequacy.
confidence: well-supported
confidence_rationale: The formal sequence is exact and reproducible; the broader interpretation is deliberately limited to a methodological boundary.
disagreements:
  - other gains, delays, nonlinearities, and stability definitions can produce different behavior
open_questions:
  - should formal expressions receive their own contract subtype?
  - which stability definition is appropriate for each model class?
revision_triggers:
  - the arithmetic fixture changes
  - the recurrence or assumptions change
  - a formal-expression contract is introduced
---

## Provenance path

`question:en:when-delayed-correction-can-oscillate` → `src:synthetic-feedback-run-delay-one-gain-one` → `evidence:en:delayed-feedback-periodic-sequence` → `claim:en:stated-delayed-recurrence-oscillates` → `model:en:delayed-correction-recurrence` and `concept:en:feedback` → this synthesis.

## Inference boundary

The exact sequence is not evidence that delay always destabilizes feedback or that any observed real-world oscillation has this mechanism.
