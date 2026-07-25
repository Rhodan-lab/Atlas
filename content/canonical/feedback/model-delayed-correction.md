---
contract: atlas-content/0.1
id: model:en:delayed-correction-recurrence
work: work:delayed-correction-recurrence
type: model
title: Delayed corrective recurrence
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
purpose: Demonstrate how a one-step delay changes a simple corrective feedback recurrence.
formal_structure: x[t+1] = x[t] - k*x[t-d]
inputs:
  - state history
outputs:
  - next state
parameters:
  - gain k
  - delay d
assumptions:
  - discrete time
  - scalar state
  - linear correction
  - fixed gain and delay
  - exact arithmetic
  - no noise, saturation, or external input
validation:
  - hand calculation and unit test for k=1, d=1, x0=1, x1=0
failure_modes:
  - nonlinear or multidimensional dynamics
  - changing parameters
  - saturation or bounded control
  - measurement delay differing from actuation delay
  - external inputs or noise
---

The model is intentionally small enough to reproduce manually. It illustrates one mechanism, not a general theorem about every delayed system.
