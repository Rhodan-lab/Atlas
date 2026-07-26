# Reviewer Submission and Admission Guide

## Purpose

This guide allows an accountable reviewer to return an exact-revision review without understanding Atlas validator implementation, and allows a maintainer to preserve an explicit decision about whether that review record may enter Atlas history.

The workflow is:

```text
handoff task
  → exact-snapshot submission
  → intake validation
  → external human verification
  → admission decision
  → normal pull-request commitment
  → coverage and promotion evaluation
```

No step automatically approves knowledge or changes lifecycle status.

## Before reviewing

Begin with the generated `atlas-review-handoff/0.1` package. Confirm:

1. the exact task ID;
2. the canonical entity ID and revision;
3. the original repository path;
4. the SHA-256 digest of the copied Markdown snapshot;
5. the bounded review type;
6. relevant sources, assumptions, limitations, blockers, and dependents;
7. required qualification and independence;
8. conflicts;
9. whether the review needs a horizon.

A review of revision 1 does not authorize revision 2. A review of one type does not satisfy another type.

## Reviewer identity and accountability

Use the reviewer's real display name or a stable accountable organizational identity. Do not invent credentials, independence, or conflicts.

- `kind: human` is required;
- `accountable: true` means responsibility for the bounded judgment;
- independent authority is required where the handoff task says so;
- editorial and source review may be internal only when the task permits;
- `qualification` must explain competence for the exact task;
- `conflicts` must disclose relevant authorship, employment, funding, ownership, data access, or other interests;
- use an explicit empty list only when no relevant conflict is known.

AI may assist preparation, comparison, or wording. Its role must be disclosed and does not replace the accountable reviewer.

## Outcomes and findings

Outcomes:

- `pass` — no open findings remain;
- `pass-with-minor-findings` — only open minor or informational findings remain;
- `changes-required` — revision is required;
- `blocked` — the reviewer cannot support the bounded use;
- `not-applicable` — the requested review class does not apply, with rationale.

`permits_promotion: true` is valid only for a passing accountable human review with no unresolved critical or major finding. It applies only to the exact revision and review type.

Each finding needs a canonical ID, severity, status, summary, rationale, affected fields, suggested action, references when needed, and a resolution note for resolved major or critical findings.

The existing major finding `finding:feedback:periodicity-proof` must remain visible until an accountable review resolves it or keeps the formal claim blocked.

## Prepare the return envelope

Start from [`templates/reviewer-submission-envelope.json.example`](templates/reviewer-submission-envelope.json.example).

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

## Validate intake

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

A passing result means only that the return package is consistent with the active handoff.

Extract a proposed record:

```bash
python tools/foundation-validator/phase1_review_intake.py extract \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/extracted-review.json
```

The extracted record adds `metadata.intake`. Extraction never writes to `content/reviews/records/` automatically.

## Perform real external verification

Before an `accept` admission decision, an accountable human maintainer must actually check:

- reviewer identity;
- qualification for the exact task;
- independence declaration;
- conflict disclosure.

The admission validator can verify that the maintainer declares these checks complete. It cannot perform them.

Do not set a check to `true` unless it occurred.

## Record the admission decision

Start from [`templates/review-admission.json.example`](templates/review-admission.json.example).

Available decisions:

- `accept` — the record may be prepared for normal repository review;
- `request-changes` — preserve the decision receipt but prepare no record;
- `reject` — preserve the decision receipt but prepare no record.

Validate and print a receipt:

```bash
python tools/foundation-validator/phase1_review_admission.py validate \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Write the receipt:

```bash
python tools/foundation-validator/phase1_review_admission.py receipt \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/admission-receipt.json
```

A receipt preserves the submission and proposed-record digests, decision, date, and boundary statement.

## Prepare an accepted record

Only `decision: accept` may prepare a record:

```bash
python tools/foundation-validator/phase1_review_admission.py prepare \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --records-dir content/reviews/records \
  --out phase1-reports/proposed-admitted-review.json
```

The prepared record:

- preserves `metadata.intake`;
- adds `metadata.admission`;
- preserves the outcome and every finding;
- rejects a review ID already present in the canonical records directory;
- writes only to the explicit output path.

Admission can accept a `changes-required` review or a review with major findings into history. This preserves criticism and does not approve the knowledge.

Synthetic admissions set `test_fixture: true`; prepared fixture records are forced to `permits_promotion: false`.

## Commit through normal repository review

After preparation, a maintainer must still:

1. inspect the prepared record and both lineage blocks;
2. confirm the admission declarations match the real checks performed;
3. confirm findings and outcome are unchanged;
4. open a normal pull request adding the record under `content/reviews/records/`;
5. let CI validate the record and regenerate coverage;
6. preserve unresolved findings;
7. create a new canonical revision when findings require content changes;
8. use the promotion gate separately.

Admission is not an automatic commitment mechanism.

## Regenerate governance outputs

After a real record is merged:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report phase1-reports/feedback-coverage.md

python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir phase1-reports/human-review-handoff
```

A task disappears only when an acceptable committed exact-revision record satisfies coverage. A valid envelope, receipt, or prepared file never makes that decision by itself.

## Prohibited shortcuts

Do not:

- reuse a review for another task, entity, revision, or review type;
- modify a snapshot digest to make a different review fit;
- mark AI or a machine as human or accountable;
- claim identity, independence, qualifications, conflicts, or external checks that do not exist;
- hide AI assistance, blockers, disagreements, or findings;
- convert `changes-required` into `pass` during admission;
- remove or resolve findings during admission;
- set `permits_promotion` while serious findings remain;
- copy prepared records automatically into the canonical review directory;
- treat intake or admission validation as scientific, editorial, methodological, legal, ethical, or lifecycle approval;
- fabricate or automatically assign a reviewer or maintainer;
- use an Atlas review to approve a Principia explanation, lesson, simulation, investigation, or system dossier automatically.
