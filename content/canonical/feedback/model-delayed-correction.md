---
contract: atlas-content/0.1
id: model:en:delayed-correction-recurrence
work: work:delayed-correction-recurrence
type: model
title: Delayed corrective recurrence
status: draft
revision: 2
created: 2026-07-26
updated: 2026-07-26
language: en
purpose: Demonstrate how a one-step delayed correction can produce a periodic orbit in a simple scalar recurrence.
formal_structure: x[t+1] = x[t] - k*x[t-d]
inputs:
  - state history sufficient to evaluate x[t-d]
outputs:
  - next state
parameters:
  - gain k
  - nonnegative integer delay d
assumptions:
  - discrete time
  - scalar state
  - linear correction
  - fixed gain and delay
  - enough initial history is supplied for the selected delay
  - exact arithmetic
  - no noise, saturation, or external input
validation:
  - direct calculation for k=1, d=1, x0=1, x1=0
  - the ordered state pair (x7, x6) equals (x1, x0), proving repetition under the deterministic second-order recurrence
  - the first six states exclude periods 1, 2, and 3, so the orbit has exact period 6
failure_modes:
  - nonlinear or multidimensional dynamics
  - changing parameters
  - insufficient or inconsistent initial history
  - saturation or bounded control
  - measurement delay differing from actuation delay
  - external inputs or noise
review:
  level: ai-reviewed
  record: ai-review:feedback-delayed-comprehensive
  reviewed_at: 2026-07-26
  human_verified: false
---

For `k = 1` and `d = 1`, the recurrence becomes `x[t+1] = x[t] - x[t-1]`. Starting from `x0 = 1` and `x1 = 0`, it produces `1, 0, -1, -1, 0, 1, 1, 0, ...`. Because the ordered pair `(x7, x6) = (0, 1)` equals `(x1, x0) = (0, 1)`, determinism forces the subsequent sequence to repeat. The model illustrates one exact mechanism, not a general theorem about every delayed system.