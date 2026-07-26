# Phase 1 Machine Attestations

## Purpose

This work package completes every review task that the accepted Phase 1 authority policy permits a machine to satisfy for the complete English delayed-feedback vertical slice.

It does not perform human review, grant accountability, resolve domain or methodological findings, permit promotion, or change lifecycle status.

## Exact scope

The complete slice contains ten exact revision-1 entities. Each receives one structural machine attestation:

1. research question;
2. authoritative feedback reference;
3. generated model-run source;
4. generated periodic-sequence evidence;
5. model-derived oscillation claim;
6. model-to-world inference-boundary claim;
7. feedback concept;
8. oscillation concept;
9. delayed-correction recurrence model;
10. delayed-feedback synthesis.

Three entities also receive a reproducibility machine attestation because the manifest marks them `fully-specified-reproducibility`:

- `claim:en:stated-delayed-recurrence-oscillates@1`;
- `evidence:en:delayed-feedback-periodic-sequence@1`;
- `model:en:delayed-correction-recurrence@1`.

Total: **13 machine attestations**.

## Authority boundary

Every generated record:

- uses `contract: atlas-review/0.1`;
- targets one exact entity ID and revision;
- sets reviewer kind to `machine`;
- sets independence to `not-applicable`;
- sets `accountable: false`;
- sets `permits_promotion: false`;
- records no authority beyond the named deterministic procedure;
- remains distinguishable from human judgment.

The records cannot satisfy:

- source interpretation;
- final editorial accountability;
- domain terminology or scientific adequacy;
- methodological or model-to-world inference review;
- ethical or legal-context review;
- human reproducibility review where the computation is not fully specified;
- any lifecycle acceptance decision.

## Structural procedure

Structural records refer to:

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
```

A structural pass establishes only that the exact authored corpus conforms to the accepted content contract and deterministic relationship checks.

It does not establish that definitions are scientifically optimal, claims are true, evidence is sufficient, or conclusions are appropriate.

## Reproducibility procedure

The bounded arithmetic fixture recalculates:

```text
x[t+1] = x[t] - x[t-1]
x[0] = 1
x[1] = 0
```

The first eight values are:

```text
1, 0, -1, -1, 0, 1, 1, 0
```

This verifies the stated recurrence calculation for the exact parameters and initial values.

It does not establish:

- that the word `oscillation` is the best terminology;
- a general theorem for all gains, delays, or initial conditions;
- stability or instability of every delayed system;
- adequacy of the recurrence for a real system;
- empirical evidence about physical, biological, economic, or organizational behavior.

## Deterministic generator

Generate records:

```bash
python tools/foundation-validator/phase1_machine_attestations.py generate \
  --records-dir content/reviews/records
```

Verify committed records:

```bash
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

CI fails when:

- a required record is missing;
- a committed record differs from deterministic output;
- the recurrence output changes unexpectedly;
- a record violates `atlas-review/0.1`;
- a machine record claims accountability or permission to promote.

## Resulting backlog

Before this work package:

- 38 gate tasks;
- 13 automation-eligible;
- 25 human-required.

After the committed attestations are counted:

- 25 gate tasks;
- 0 automation-eligible;
- 25 human-required;
- 0 advisory-only.

The slice remains `blocked`. This is the correct result.

## Principia & Atlas implication

A future Principia experience may rely on the structural integrity and reproducibility of an Atlas model fixture. It may not present those machine attestations as scientific review or evidence that the model applies to a real system.

Atlas preserves the authority boundary so Principia can expose both:

- what the formal model demonstrably computes;
- what still requires accountable human judgment before broader interpretation.
