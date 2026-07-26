# Phase 1 Review Intake

## Purpose

`atlas-review-submission/0.1` verifies that a returned accountable-human review matches one active handoff task and the exact canonical snapshot supplied to the reviewer.

The intake validator does not accept the review into authority, resolve findings, permit promotion, or change lifecycle status. It verifies the return package before a maintainer decides whether to commit the extracted `atlas-review/0.1` record.

## Why an intake envelope is necessary

A structurally valid review record can still be unsuitable for the active review scope when it:

- targets the wrong task;
- reviews another entity revision;
- uses a different canonical snapshot;
- submits the wrong review type;
- comes from a nonhuman or nonaccountable reviewer;
- fails the independence requirement;
- omits qualification or conflicts;
- uses AI assistance without disclosure;
- was completed after the claimed submission date.

The intake envelope binds those facts together without changing the underlying review-record contract.

## Contract

```text
atlas-review-submission/0.1
```

Required fields:

- `coverage_id` — exact coverage scope from the generated handoff;
- `task_id` — exact active human task;
- `snapshot` — entity ID, revision, and SHA-256 supplied to the reviewer;
- `submitted_at` — ISO submission date;
- `reviewed_exact_snapshot: true`;
- `ai_assistance` — explicit use and description;
- `review_record` — one proposed `atlas-review/0.1` record.

Start from [`templates/reviewer-submission-envelope.json.example`](templates/reviewer-submission-envelope.json.example).

## Validation requirements

The validator checks that:

1. the handoff itself is valid;
2. the coverage ID matches;
3. the task is active, gate-blocking, and human-required;
4. the exact entity ID and revision match the task;
5. the snapshot digest matches the handoff;
6. the review type matches the task;
7. the nested review record passes `atlas-review/0.1` validation;
8. reviewer kind is `human`;
9. reviewer accountability is true;
10. independence satisfies the task;
11. qualification and conflicts are present;
12. AI assistance is disclosed;
13. submission date does not precede review completion.

## Validate a returned submission

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

A passing result means only that the return package is internally consistent with the active handoff task.

## Extract the normalized review record

```bash
python tools/foundation-validator/phase1_review_intake.py extract \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/extracted-review.json
```

The extracted record preserves the submitted `atlas-review/0.1` content and adds `metadata.intake` containing:

- submission contract;
- coverage ID;
- task ID;
- exact snapshot identity and digest;
- submission date;
- exact-snapshot attestation;
- AI-assistance disclosure.

Extraction does not write to `content/reviews/records/` automatically.

## Maintainer acceptance workflow

1. Validate the submission envelope.
2. Inspect the real reviewer identity, qualification, independence, and conflicts.
3. Confirm findings and promotion permission are bounded honestly.
4. Compare the extracted record with the original submission.
5. Commit the record under `content/reviews/records/` only through normal review.
6. Regenerate coverage, backlog, and handoff.
7. Revise canonical content through a new revision when findings require changes.
8. Do not remove an old finding or task merely because the envelope validates.

## AI-assistance disclosure

When AI assistance was used, `ai_assistance.used` must be true and `description` must explain its bounded role.

Examples of permitted disclosed assistance:

- terminology comparison;
- formatting a findings table;
- checking arithmetic already judged by the reviewer;
- drafting questions for human consideration.

The accountable human must still make the final bounded judgment. AI cannot become the reviewer or satisfy independence.

## Prohibited shortcuts

Do not:

- modify the task ID or digest to make a different review fit;
- review a later repository state while claiming the handoff snapshot;
- submit a machine or AI identity as human;
- claim independence that does not exist;
- omit conflicts or AI assistance;
- treat successful intake validation as accepted review authority;
- automatically copy extracted records into the canonical review directory;
- resolve the open periodicity finding without an accountable review and, when needed, a new canonical revision;
- use an Atlas intake result to approve a future Principia artifact automatically.

## Principia & Atlas boundary

Review intake establishes provenance for Atlas knowledge review only. A future Principia explanation, simulation, investigation, or system dossier requires its own pedagogical and release review even when it references a reviewed Atlas revision.
