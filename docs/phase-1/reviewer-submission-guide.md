# Reviewer Submission Guide

## Purpose

This guide allows an accountable reviewer to return an exact-revision review without understanding Atlas validator implementation.

Begin with the generated `atlas-review-handoff/0.1` package. Return one `atlas-review-submission/0.1` envelope per active task. The envelope contains one proposed `atlas-review/0.1` record and binds it to the exact task and canonical snapshot reviewed.

## Before reviewing

Confirm:

1. the handoff contract is `atlas-review-handoff/0.1`;
2. the exact task ID;
3. the canonical entity ID and revision;
4. the original repository path;
5. the SHA-256 digest of the copied Markdown snapshot;
6. the bounded review type;
7. relevant sources, evidence, assumptions, limitations, and dependents;
8. existing review records and unresolved blockers;
9. qualification, independence, and conflicts;
10. whether the review needs a time horizon.

A review of revision 1 does not authorize revision 2. A review of one type does not silently satisfy another type.

## Reviewer identity and accountability

Use the reviewer's real display name or a stable accountable organizational identity. Do not invent credentials, independence, or conflicts.

- `kind: human` is required;
- `accountable: true` means responsibility for the bounded judgment;
- independent authority is required where the handoff task says so;
- editorial and source review may be internal when the task permits;
- `qualification` must explain competence for the exact task;
- `conflicts` must disclose relevant authorship, employment, funding, ownership, data access, or other interests;
- use an explicit empty list only when no relevant conflict is known.

AI may assist preparation, comparison, or wording. Its role must be disclosed in the submission envelope and does not replace the accountable reviewer.

## Outcomes

- `pass` — no open findings remain;
- `pass-with-minor-findings` — only open minor or informational findings remain;
- `changes-required` — revision is required before promotion permission;
- `blocked` — the reviewer cannot support the bounded use;
- `not-applicable` — the requested review class does not apply, with rationale.

`permits_promotion: true` is valid only for a passing accountable human review with no unresolved critical or major finding. It applies only to the exact entity revision and review type.

## Findings

Each finding needs:

- canonical finding ID;
- severity and status;
- concise summary and rationale;
- affected fields;
- suggested action;
- references when needed;
- resolution note for resolved major or critical findings.

The existing major finding `finding:feedback:periodicity-proof` must remain visible until an accountable review resolves it or keeps the formal claim blocked.

## Prepare the return envelope

Start from:

[`templates/reviewer-submission-envelope.json.example`](templates/reviewer-submission-envelope.json.example)

Copy the exact values from the selected handoff task:

- `coverage_id`;
- `task_id`;
- snapshot entity ID;
- snapshot revision;
- snapshot SHA-256;
- review type;
- required independence.

Set `reviewed_exact_snapshot: true` only after reviewing the copied canonical snapshot identified by that digest.

Disclose AI assistance explicitly:

```json
{
  "used": true,
  "description": "AI compared terminology; the accountable human made the final judgment."
}
```

Use `used: false` and `description: null` when no AI assistance was used.

## Validate the return package

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Validation checks the active task, exact snapshot, nested review record, reviewer authority, independence, qualification, conflicts, dates, and AI disclosure.

A passing result means only that the return package is consistent with the active handoff. It does not accept the review.

## Extract the proposed review record

```bash
python tools/foundation-validator/phase1_review_intake.py extract \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/extracted-review.json
```

The extracted record adds `metadata.intake` containing the task, snapshot, date, and AI-assistance lineage. Extraction does not write to `content/reviews/records/` automatically.

Validate the extracted record separately:

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  phase1-reports/extracted-review.json
```

## Maintainer acceptance workflow

1. Validate the submission envelope.
2. Inspect the real reviewer identity, qualification, independence, and conflicts.
3. Confirm findings and promotion permission are bounded honestly.
4. Compare the extracted record with the original envelope.
5. Commit an acceptable record under `content/reviews/records/` through normal review.
6. Regenerate coverage, backlog, and handoff.
7. Create a new canonical revision when findings require content changes.
8. Do not edit lifecycle status merely because one review passes.

## Regenerate handoff

```bash
python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir phase1-reports/human-review-handoff
```

A task disappears only when an acceptable committed exact-revision record satisfies coverage. A valid envelope or extracted file never makes that decision by itself.

## Prohibited shortcuts

Do not:

- reuse a review for another task, entity, revision, or review type;
- modify the snapshot digest to make a different review fit;
- mark AI or a machine as human or accountable;
- claim independence or qualifications that do not exist;
- hide conflicts, AI assistance, or existing blockers;
- set `permits_promotion` while serious findings remain;
- copy extracted records automatically into the canonical review directory;
- treat intake validation as scientific, editorial, methodological, legal, ethical, or human approval;
- fabricate or automatically assign a reviewer;
- use an Atlas review to approve a future Principia explanation, lesson, simulation, or system dossier automatically.
