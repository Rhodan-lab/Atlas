# Reference Slice B — Delayed Feedback and Oscillation

## Slice metadata

```yaml
contract: atlas-content/0.1
id: synthesis:en:delayed-feedback-and-oscillation-slice
work: work:delayed-feedback-and-oscillation-slice
type: synthesis
title: Delay can change the stability of a feedback model
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
```

## Question record

```yaml
id: question:en:when-can-delayed-correction-oscillate
type: question
status: draft
state: partially-answered
```

**Question:** Under which assumptions can delayed corrective feedback produce oscillation or instability, and what may be inferred about real systems from that formal result?

## Source record

```yaml
id: src:astrom-murray-2008-feedback-systems
type: source
status: draft
source:
  kind: textbook-reference
  authors:
    - Karl J. Astrom
    - Richard M. Murray
  title: Feedback Systems: An Introduction for Scientists and Engineers
  publisher: Princeton University Press
  published: 2008
  locator: https://authors.library.caltech.edu/records/yzs24-xsx88
access:
  class: public-locator
```

**Use in this slice:** provides an established conceptual and mathematical reference for feedback, dynamic behavior, and stability. The fixture paraphrases rather than reproduces the book.

## Evidence records

### Evidence 1 — source structure

```yaml
id: evidence:en:feedback-book-covers-dynamic-behavior-and-stability
type: evidence
status: draft
source: src:astrom-murray-2008-feedback-systems
locator:
  kind: section
  value: Chapter 4, Dynamic Behavior, including Stability
relations:
  - type: contextualizes
    target: claim:en:feedback-performance-and-stability-are-distinct
```

**Description:** The source organizes dynamic behavior and stability as explicit subjects in the study of feedback systems.

### Evidence 2 — reproducible sequence generated from a model

```yaml
id: evidence:en:delayed-difference-equation-periodic-sequence
type: evidence
status: draft
source: src:synthetic-model-run-delay-one-gain-one
access:
  class: open
locator:
  kind: observation-log
  value: hand-calculation-v1
transformation:
  procedure: model:en:delayed-correction-difference-equation
  parameters:
    gain: 1
    delay_steps: 1
    initial_state:
      x0: 1
      x1: 0
measurement:
  quantity: state-sequence
  values: [1, 0, -1, -1, 0, 1, 1, 0]
  unit: unitless
relations:
  - type: supports
    target: claim:en:one-delayed-feedback-model-can-oscillate
```

**Reproduction:** apply `x[t+1] = x[t] - x[t-1]` repeatedly from `x0 = 1` and `x1 = 0`.

**Appraisal:** this is exact model-derived evidence for one parameterized equation. It is not empirical evidence about a physical, biological, economic, or social system.

## Claim records

### Claim 1

```yaml
id: claim:en:feedback-performance-and-stability-are-distinct
type: claim
status: draft
claim:
  kind: definitional
  statement: Evaluating a feedback system requires distinguishing desired correction or performance from the stability of its resulting dynamics.
  confidence: plausible
```

### Claim 2

```yaml
id: claim:en:one-delayed-feedback-model-can-oscillate
type: claim
status: draft
claim:
  kind: model-derived
  statement: For the recurrence x[t+1] = x[t] - x[t-1] with x0 = 1 and x1 = 0, the state follows a repeating oscillatory sequence.
  scope:
    model: model:en:delayed-correction-difference-equation
    gain: 1
    delay_steps: 1
  confidence: strongly-supported
model: model:en:delayed-correction-difference-equation
```

The strong confidence refers only to the arithmetic result for the stated recurrence and initial values.

### Claim 3

```yaml
id: claim:en:model-oscillation-does-not-prove-real-system-oscillation
type: claim
status: draft
claim:
  kind: methodological
  statement: Oscillation in a simplified feedback model does not by itself establish that a real system will oscillate.
  confidence: well-supported
```

### Claim 4

```yaml
id: claim:en:delay-can-be-a-stability-relevant-assumption
type: claim
status: draft
claim:
  kind: interpretive
  statement: Delay is a stability-relevant modeling assumption because it changes which past state contributes to the current correction.
  scope:
    model_family: discrete feedback recurrences
  confidence: plausible
```

## Concept records

```yaml
id: concept:en:feedback
type: concept
status: draft
definition: A process in which information about system behavior influences later input or action.
relations:
  - type: prerequisite-of
    target: concept:en:closed-loop-stability
```

```yaml
id: concept:en:oscillation
type: concept
status: draft
definition: Repeated variation of a state or output over time; its exact meaning depends on the mathematical or empirical context.
```

```yaml
id: concept:en:closed-loop-stability
type: concept
status: draft
definition: A property concerning whether the behavior of a feedback-connected system remains bounded or approaches an accepted state under stated conditions.
```

## Model record

```yaml
id: model:en:delayed-correction-difference-equation
type: model
status: draft
purpose: Demonstrate how one-step delay changes a simple corrective recurrence.
formal_structure: x[t+1] = x[t] - k*x[t-d]
inputs:
  - state history
parameters:
  - gain k
  - delay d
outputs:
  - next state
assumptions:
  - discrete time
  - scalar state
  - linear correction
  - exact arithmetic
  - fixed gain and delay
  - no noise, saturation, or external input
validation:
  - hand-calculated fixture for k=1 and d=1
failure_modes:
  - nonlinear response
  - changing parameters
  - multidimensional dynamics
  - measurement delay differing from actuation delay
  - saturation or bounded controls
```

## Argument block

```yaml
argument:
  mode: deductive
  premises:
    - claim:en:one-delayed-feedback-model-can-oscillate
  assumptions:
    - the recurrence and initial values are applied exactly
  conclusion: claim:en:the-stated-recurrence-has-an-oscillatory-solution
```

A separate abductive argument would be required to use an observed real-world oscillation as evidence for delayed feedback. The formal result alone cannot identify the mechanism in a real system.

## Synthesis

The slice demonstrates a clean separation between formal and empirical knowledge. A simple delayed corrective recurrence can produce a repeating sequence for a particular gain, delay, and initial condition. That result is reproducible and strongly supported within the model. It does not establish that delay always destabilizes feedback, that every oscillation is caused by feedback, or that any specific real system follows the equation. The responsible use of the model is explanatory and hypothesis-generating: it shows one mechanism by which delayed correction can create oscillatory behavior and clarifies which assumptions must be tested before applying the conclusion elsewhere.

## Cross-domain analogy limits

The same diagram may resemble regulation in biology, engineering, economics, or organizations. `analogous-to` may connect those models only when the shared structure is named. The analogy cannot be used as evidence that parameters, causal mechanisms, stability thresholds, or interventions transfer.

## Open questions

- Does `atlas-content/0.1` need a first-class equation object, or is a model field sufficient?
- How should exact symbolic derivation differ from numerical simulation evidence?
- When should model parameter ranges become separate evidence records?
- Which stability definition is appropriate for each model class?

## Revision triggers

- arithmetic fixture is found incorrect;
- the recurrence definition changes;
- a separate argument entity becomes necessary;
- the contract adopts formal-expression or executable-model subcontracts;
- domain examples are added and require application-specific evidence.

## Review matrix

| Review | Status | Reason |
|---|---|---|
| structural | pending | bundled fixture not machine-validated |
| source | pending | book metadata and locator verification required |
| editorial | pending | definition and scope review required |
| domain | pending | control-systems review required |
| methodological | pending | inference boundary review required |
| reproducibility | pending | sequence should be independently recalculated |
