# Reviewer Submission Guide

## Purpose

This guide allows an accountable reviewer to return a revision-specific review without understanding the validator implementation.

Start from [`templates/reviewer-submission.json.example`](templates/reviewer-submission.json.example). Submit one record per entity revision and review type.

## Before reviewing

Confirm all of the following:

1. the exact canonical entity ID;
2. the exact revision reviewed;
3. the bounded review type requested by the packet;
4. the sources, evidence, assumptions, and limitations included in scope;
5. whether any relevant conflict affects independence;
6. whether the review has a time horizon.

A review of revision 1 does not authorize revision 2.

## Reviewer identity and accountability

Use the reviewer's real display name or a stable accountable organizational identity. Do not invent credentials or independence.

- `kind: human` is required for accountable review;
- `accountable: true` means the reviewer accepts responsibility for the bounded judgment recorded;
- `independence: independent` is required for domain, methodological, ethical, translation, legal-context, and normally reproducibility authority;
- `qualification` must describe why the reviewer is competent for this exact review;
- `conflicts` must disclose relevant authorship, employment, funding, project ownership, data access, or other interests.

AI may assist preparation, comparison, or wording. AI assistance must be disclosed and does not replace the accountable reviewer.

## Outcomes

- `pass` — no open findings remain;
- `pass-with-minor-findings` — only open minor or informational findings remain;
- `changes-required` — the entity needs revision before this review can permit promotion;
- `blocked` — the reviewer cannot support the bounded use;
- `not-applicable` — the requested review class does not apply, with rationale.

`permits_promotion: true` is valid only for a passing accountable human review with no unresolved critical or major finding.

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

## Review horizon

Use `null` only when the review is not meaningfully time-sensitive. Legal context, current policy, safety guidance, software behavior, and rapidly changing evidence commonly need an explicit horizon.

Expiration does not delete the review. It prevents the expired record from satisfying a later promotion decision.

## Submission workflow

1. Copy the example file.
2. Replace every placeholder.
3. Save it under `content/reviews/records/`.
4. Validate it:

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/<record>.json
```

5. Regenerate the relevant coverage report:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/<manifest>.json \
  --records-dir content/reviews/records \
  --report phase1-reports/<manifest>.md
```

6. Resolve findings through a new canonical revision when content changes.
7. Do not edit lifecycle status merely because one review passes. The promotion gate evaluates the complete required set separately.

## Prohibited shortcuts

Do not:

- reuse a review for another revision;
- mark an AI or machine as accountable;
- hide conflicts;
- claim independent status for project authors reviewing their own work;
- set `permits_promotion` when serious findings remain;
- treat a validator pass as scientific, legal, ethical, or translation approval;
- fabricate a reviewer to make a coverage report green.
