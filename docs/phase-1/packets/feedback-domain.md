# Review Packet — Delayed Feedback and Oscillation

## Requested reviews

- domain: control systems, dynamical systems, or difference equations
- methodological: model-to-world inference
- reproducibility: recurrence calculation and periodicity

## Exact primary target

- Entity: `claim:en:stated-delayed-recurrence-oscillates`
- Revision: `1`
- File: `content/canonical/feedback/claim-recurrence-oscillates.md`
- Current status: `draft`

## Linked records in scope

- `src:astrom-murray-2008-feedback-systems`
- `src:synthetic-delayed-feedback-run`
- `evidence:en:delayed-recurrence-periodic-sequence`
- `model:en:delayed-correction-recurrence`
- `claim:en:model-oscillation-does-not-prove-real-system-oscillation`
- `concept:en:feedback`
- `concept:en:oscillation`
- `synthesis:en:delayed-feedback-and-oscillation`
- `question:en:delayed-correction-oscillation`

## Formal object

```text
x[t+1] = x[t] - x[t-1]
x[0] = 1
x[1] = 0
```

Recorded prefix:

```text
1, 0, -1, -1, 0, 1, 1, 0
```

## Required mathematical checks

1. Recalculate each state from the recurrence.
2. Identify the ordered state pair needed to determine the future trajectory.
3. Verify whether an ordered pair repeats.
4. State the resulting period, if periodicity is established.
5. Confirm that the claim wording does not rely only on visual inspection of a finite prefix.
6. Confirm the difference between periodic, oscillatory, bounded, convergent, asymptotically stable, and unstable behavior.
7. Determine whether the current confidence rationale is sufficient for the exact claim.

## Terminology questions

- Is “oscillatory sequence” appropriate for this recurrence and initial state?
- Does any concept definition imply that all repeated sign changes are equivalent?
- Does the slice accidentally equate lack of convergence with instability?
- Is `closed-loop stability` needed as a separate concept in the canonical split?
- Should the model declare the state as the ordered pair `(x[t], x[t-1])`?
- Is the gain/delay notation consistent with the specialized recurrence used by the fixture?

## Model-to-world boundary

The reviewer should verify that the slice does not infer any of the following without empirical evidence:

- a real oscillation is caused by delayed feedback;
- every delayed feedback system oscillates;
- every oscillation is unstable;
- parameters transfer across engineering, biological, economic, or organizational systems;
- one scalar linear recurrence represents a real system adequately.

## Reference use

The Åström–Murray source is used as an established reference for feedback, dynamic behavior, and stability terminology. The exact recurrence is a project fixture, not a worked example attributed to that book.

The review must preserve that distinction.

## Current AI-assisted findings

See:

`content/reviews/records/feedback-domain-ai-assisted.json`

Open findings:

- major: add or confirm an explicit periodicity argument based on a repeated state pair;
- minor: keep periodic bounded behavior separate from asymptotic stability.

## Pass conditions

A passing domain review should:

- target revision 1;
- confirm the recurrence and terminology;
- state whether the finite-prefix evidence is sufficient when combined with the recurrence;
- confirm or revise the claim title and statement;
- resolve the major periodicity finding;
- preserve the model-to-world limitation;
- disclose conflicts and qualifications.

## Translation handoff

Any accepted English terminology should be handed to the Indonesian translation packet before the translated entities are promoted.
