---
contract: atlas-content/0.1
id: claim:en:stated-delayed-recurrence-oscillates
work: work:stated-delayed-recurrence-oscillates
type: claim
title: The stated delayed recurrence has an exact period-six orbit
status: draft
revision: 2
created: 2026-07-26
updated: 2026-07-26
language: en
claim:
  kind: model-derived
  statement: "For x[t+1] = x[t] - x[t-1] with x0 = 1 and x1 = 0, the state sequence is periodic with exact period 6: 1, 0, -1, -1, 0, 1, then repetition."
  scope:
    model: model:en:delayed-correction-recurrence
    gain: 1
    delay_steps: 1
    initial_state:
      x0: 1
      x1: 0
  confidence: strongly-supported
model: model:en:delayed-correction-recurrence
confidence_rationale: Direct substitution gives the six-state cycle, and the ordered state pair returns after six steps; determinism then proves indefinite repetition. Periods 1, 2, and 3 are excluded by the observed six-state block.
limitations:
  - confidence applies only to the stated recurrence, parameters, initial values, and exact arithmetic
  - the result does not imply instability, because the orbit is bounded
  - the result does not establish behavior for other gains, delays, or initial histories
review:
  level: ai-reviewed
  record: ai-review:feedback-delayed-comprehensive
  reviewed_at: 2026-07-26
  human_verified: false
---

This is a formal result about one deterministic recurrence. It establishes a bounded periodic orbit, not empirical oscillation in a physical system and not a general claim that delay causes instability.