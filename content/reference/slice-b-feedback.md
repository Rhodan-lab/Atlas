# Reference Slice B — Delayed Feedback and Oscillation

## Status

- Language: English
- Review level: `ai-reviewed`
- Human verified: false
- Human review required: false
- Comprehensive record: `content/reviews/ai/feedback-delayed-comprehensive.json`
- Review report: `docs/phase-1/ai-review-report.md`

This reference slice summarizes the split canonical entities. The split files under `content/canonical/feedback/` remain authoritative for exact revisions.

## Question

Under which assumptions can delayed corrective feedback produce oscillation, and what may be inferred about real systems from that formal result?

The scope is a discrete scalar recurrence. The question is not answered by claiming that every delayed system oscillates.

## Authoritative source context

**Karl J. Åström and Richard M. Murray, _Feedback Systems: An Introduction for Scientists and Engineers_, Princeton University Press, 2008.**

Authoritative locator:

`https://authors.library.caltech.edu/records/yzs24-xsx88`

The source supports established feedback, dynamic-behavior, and stability terminology. It does not contain or prove the exact Atlas recurrence result below.

## Model

```text
x[t+1] = x[t] - k*x[t-d]
```

For the reviewed example:

```text
k = 1
d = 1
x0 = 1
x1 = 0
```

Assumptions:

- discrete time;
- scalar state;
- linear correction;
- fixed gain and delay;
- sufficient initial history;
- exact arithmetic;
- no noise, saturation, or external input.

## Generated evidence

Direct substitution gives:

```text
x0..x7 = 1, 0, -1, -1, 0, 1, 1, 0
```

The recurrence is deterministic in the ordered state pair `(x[t], x[t-1])`.

```text
(x1, x0) = (0, 1)
(x7, x6) = (0, 1)
```

The pair returns after six steps, so all later states repeat with period dividing 6. The first six states exclude periods 1, 2, and 3. Therefore the orbit has exact period 6.

This is generated model evidence, not an empirical measurement.

## Claims

### Exact model-derived claim

For `x[t+1] = x[t] - x[t-1]` with `x0 = 1` and `x1 = 0`, the orbit is bounded and periodic with exact period 6:

```text
1, 0, -1, -1, 0, 1, then repetition
```

### Inference-boundary claim

Oscillation in a simplified delayed-feedback model does not by itself establish that a real system follows the model or will oscillate.

Applying the result to a real system requires separate evidence for model structure, parameters, measurements, initial conditions, external inputs, and operating conditions.

## Concepts

### Feedback

A process in which information about system behavior influences later input, action, or state.

### Oscillation

Repeated variation of a state or output over time. In this slice the formal behavior is an exact bounded periodic orbit.

Periodicity is not automatically instability. One periodic solution also does not establish behavior for every parameter or initial history.

## Synthesis

One specified delayed corrective recurrence has an exact bounded period-six orbit for one gain, delay, and initial history. The result demonstrates one formal mechanism by which delayed correction can produce oscillatory behavior.

It does not establish that:

- delay always causes oscillation;
- oscillation implies instability;
- every real feedback system follows this recurrence;
- a real observed oscillation was caused by delay;
- parameters or interventions transfer across domains.

## Resolved AI-review findings

1. Eight displayed states alone did not prove indefinite periodicity. The ordered-state return now provides the proof.
2. The slice needed to distinguish bounded oscillation from instability. The revised result does so explicitly.
3. The textbook source and independently derived recurrence result needed a clearer boundary. The source-use scope is now explicit.

## Revision triggers

- the recurrence or initial conditions change;
- the ordered-state proof is challenged;
- empirical system applications are added;
- another stability definition becomes relevant;
- a formal-expression contract is introduced.

## Optional human verification

Historical human handoff, intake, and admission tools remain available as an optional stronger review path. They are not active duties and do not block Phase 2.
