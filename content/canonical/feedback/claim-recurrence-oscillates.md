---
contract: atlas-content/0.1
id: claim:en:stated-delayed-recurrence-oscillates
work: work:stated-delayed-recurrence-oscillates
type: claim
title: The stated delayed recurrence has an oscillatory sequence
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
claim:
  kind: model-derived
  statement: For x[t+1] = x[t] - x[t-1] with x0 = 1 and x1 = 0, the first states form the repeating sequence 1, 0, -1, -1, 0, 1, 1, 0.
  scope:
    model: model:en:delayed-correction-recurrence
    gain: 1
    delay_steps: 1
    initial_state:
      x0: 1
      x1: 0
  confidence: strongly-supported
model: model:en:delayed-correction-recurrence
confidence_rationale: The result follows by direct arithmetic and is recalculated by the validator test suite.
limitations:
  - confidence applies only to the stated recurrence, parameters, initial values, and exact arithmetic
---

This claim is formal and reproducible. It is not empirical evidence that a particular real system oscillates.
