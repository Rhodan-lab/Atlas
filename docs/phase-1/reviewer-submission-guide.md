# Reviewer Submission Guide

## Purpose

This guide allows an accountable reviewer to return an exact-revision review without understanding the validator implementation.

For the complete delayed-feedback slice, begin with the generated `atlas-review-handoff/0.1` package. It contains the requested tasks, exact canonical snapshots, SHA-256 digests, existing blockers, dependents, and submission worksheets.

Submit one `atlas-review/0.1` record per entity revision and review type.

## Before reviewing

Confirm all of the following:

1. the handoff contract is `atlas-review-handoff/0.1`;
2. the exact canonical entity ID and revision;
3. the canonical repository path;
4. the SHA-256 digest of the copied Markdown snapshot;
5. the bounded review type requested by the track;
6. the sources, evidence, assumptions, limitations, and dependents included in scope;
7. existing review records and unresolved blockers;
8. whether any conflict affects independence;
9. whether the review needs a time horizon.

A review of revision 1 does not authorize revision 2. A review of one type does not silently satisfy another type.

## Reviewer identity and accountability

Use the reviewer's real display name or a stable accountable organizational identity. Do not invent credentials, independence, or conflicts.

- `kind: human` is required for accountable review;
- `accountable: true` means the reviewer accepts responsibility for the bounded judgment recorded;
- `independence: independent` is required for domain, methodological, ethical, legal-context, and normally human reproducibility authority;
- editorial and source review may be internal or independent when policy permits;
- `qualification` must explain competence for the exact review type and domain;
- `conflicts` must disclose authorship, employment, funding, project ownership, data access, or other relevant interests;
- use an explicit empty conflict list only when no relevant conflict is known.

AI may assist preparation, comparison, or wording. AI assistance must be disclosed and does not replace the accountable reviewer.

## Outcomes

- `pass` — no open findings remain;
- `pass-with-minor-findings` — only open minor or informational findings remain;
- `changes-required` — the entity needs revision before the review can permit promotion;
- `blocked` — the reviewer cannot support the bounded use;
- `not-applicable` — the requested review class does not apply, with rationale.

`permits_promotion: true` is valid only for a passing accountable human review with no unresolved critical or major finding. It applies only to the exact entity revision and review type.

## Findings

Each finding needs:

- a canonical finding ID;
- severity;
- status;
- concise summary;
- rationale;
- affected fields;
- suggested action;
- references when needed.

Critical findings cannot be accepted as risk. Resolved major or critical findings require a resolution note.

The existing major finding `finding:feedback:periodicity-proof` must remain visible until an accountable review resolves it or keeps the formal claim blocked.

## Review horizon

Use `null` only when the review is not meaningfully time-sensitive. Legal context, current policy, safety guidance, software behavior, and rapidly changing evidence commonly need an explicit horizon.

Expiration does not delete the review. It prevents the expired record from satisfying a later promotion decision.

## Submission workflow

1. Open the generated track Markdown file.
2. Confirm reviewer qualification for that track and task.
3. Verify the exact entity snapshot path and digest.
4. Complete the task worksheet.
5. Start from [`templates/reviewer-submission.json.example`](templates/reviewer-submission.json.example).
6. Replace every placeholder honestly.
7. Save one record under `content/reviews/records/`.
8. Validate it:

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/<record>.json
```

9. Regenerate the relevant coverage report:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --report phase1-reports/feedback-complete-vertical-slice.md
```

10. Regenerate the backlog and handoff to confirm which tasks remain.
11. Resolve findings through a new canonical revision when content changes.
12. Do not edit lifecycle status merely because one review passes. The promotion gate evaluates the complete required set separately.

## Handoff regeneration

```bash
python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir phase1-reports/human-review-handoff
```

A task disappears only when an acceptable exact-revision review record satisfies its coverage requirement. A generated bundle never makes that decision by itself.

## Prohibited shortcuts

Do not:

- reuse a review for another entity, revision, or review type;
- mark an AI or machine as accountable;
- hide conflicts or existing blockers;
- claim independent status for project authors reviewing their own work;
- set `permits_promotion` when serious findings remain;
- treat a validator pass, machine attestation, backlog, or handoff as scientific, legal, ethical, methodological, editorial, or human approval;
- replace an exact canonical snapshot with an unversioned summary;
- treat one broad approval letter as multiple exact records;
- fabricate or automatically assign a reviewer to make coverage green;
- use an Atlas review to approve a future Principia lesson, simulation, or system dossier automatically.
