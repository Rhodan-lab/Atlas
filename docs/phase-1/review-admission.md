# Review Admission — `atlas-review-admission/0.1`

## Purpose

Review intake proves that a returned submission targets one active human-required task and the exact canonical snapshot supplied to the reviewer.

Admission is the separate maintainer decision about whether that proposed review record may enter Atlas review history through normal repository review.

Admission does **not** decide that the reviewed knowledge is correct. It does not resolve findings, edit canonical content, permit a lifecycle transition, or approve any Principia artifact.

## Why admission is separate

A structurally valid submission can still require human inspection of facts that software cannot establish:

- whether the reviewer is a real person or stable accountable organization;
- whether the claimed qualification is genuine and relevant;
- whether the claimed independence is accurate;
- whether conflicts are complete;
- whether the review appears authentic and internally coherent;
- whether the returned record should be preserved as review history.

Intake validates declarations and exact-snapshot consistency. Admission records the accountable maintainer decision after external checks.

## Decisions

### `accept`

The proposed review record may be prepared for normal repository review.

Acceptance requires all external verification checks to be explicitly complete. It does not automatically commit the record and does not imply that the review outcome is `pass`.

A review with `changes-required`, `blocked`, or an open major finding may be admitted because preserving criticism is part of trustworthy knowledge governance.

### `request-changes`

The submission is not ready to enter review history. The receipt preserves the decision and rationale, but no admitted record may be prepared.

### `reject`

The submission is unsuitable for admission. The receipt preserves the rejection and rationale, but no admitted record may be prepared.

## Contract

```json
{
  "contract": "atlas-review-admission/0.1",
  "id": "admission:feedback-editorial:2026-07-26",
  "decision": "accept",
  "decided_at": "2026-07-26",
  "decider": {
    "display_name": "Accountable maintainer name or stable role",
    "kind": "human",
    "role": "Atlas review-record maintainer",
    "accountable": true,
    "conflicts": []
  },
  "external_verification": {
    "reviewer_identity_checked": true,
    "qualification_checked": true,
    "independence_checked": true,
    "conflicts_checked": true,
    "method": "Describe the external checks performed."
  },
  "rationale": "Why this submission should enter Atlas review history.",
  "test_fixture": false
}
```

Start from [`templates/review-admission.json.example`](templates/review-admission.json.example).

## External verification boundary

The validator can confirm that verification fields are present and that an `accept` decision marks every required check as complete.

It cannot perform the real-world verification itself. The human decider remains responsible for the truth of the declaration.

Required checks for `accept`:

- reviewer identity checked;
- qualification checked;
- independence checked;
- conflicts checked;
- verification method recorded.

## Commands

Validate and print a deterministic receipt:

```bash
python tools/foundation-validator/phase1_review_admission.py validate \
  admission.json \
  submission.json \
  --handoff human-review-handoff/handoff.json
```

Write a receipt to an explicit output path:

```bash
python tools/foundation-validator/phase1_review_admission.py receipt \
  admission.json \
  submission.json \
  --handoff human-review-handoff/handoff.json \
  --out admission-receipt.json
```

Prepare an admitted review record after an `accept` decision:

```bash
python tools/foundation-validator/phase1_review_admission.py prepare \
  admission.json \
  submission.json \
  --handoff human-review-handoff/handoff.json \
  --records-dir content/reviews/records \
  --out proposed-admitted-review.json
```

The `prepare` command:

- revalidates the submission and admission;
- rejects duplicate canonical review IDs;
- preserves `metadata.intake` lineage;
- adds `metadata.admission` lineage;
- writes only to the explicit `--out` path;
- never writes to `content/reviews/records/` automatically.

The prepared file must still be inspected and committed through normal pull-request review.

## Test fixtures

Synthetic admission fixtures set:

```json
"test_fixture": true
```

Prepared fixture records are forcibly changed to:

```json
"permits_promotion": false
```

A synthetic fixture cannot grant real review authority even when it uses structurally human-shaped declarations.

## Findings and lifecycle

Admission preserves the submitted outcome and findings. It must not convert:

- `changes-required` into `pass`;
- an open finding into `resolved`;
- `permits_promotion: false` into `true`;
- a draft entity into a reviewed entity.

After a real admitted record is committed, Atlas regenerates coverage and the backlog. The promotion gate remains the only mechanism that evaluates whether the complete review set permits a lifecycle transition.

## Future Principia & Atlas boundary

Admission concerns Atlas review history only. It cannot approve a Principia explanation, lesson, simulation, investigation, system dossier, or release. Principia and Atlas retain separate authority and status.