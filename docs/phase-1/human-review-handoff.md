# Phase 1 Human Review Handoff

## Purpose

The human-review handoff converts the live complete-slice backlog into a self-contained package for accountable reviewers.

It does not assign a reviewer, perform review, resolve findings, permit promotion, or change lifecycle status.

## Generated contract

The handoff output uses:

```text
atlas-review-handoff/0.1
```

It is a generated planning and evidence-transfer artifact, not a canonical knowledge contract.

## Inputs

The generator reads:

- `content/reviews/coverage/feedback-complete-vertical-slice.json`;
- all valid exact-revision records under `content/reviews/records/`;
- canonical English Markdown under `content/canonical/`.

It therefore reflects the current coverage state rather than a manually maintained checklist.

## Preconditions

Generation fails when:

- the coverage scope is no longer blocked;
- automation-eligible tasks remain;
- advisory-only tasks are mixed into the gate handoff;
- a human task permits nonhuman authority;
- accountability is not required;
- an exact canonical entity revision cannot be located;
- a task appears more than once;
- an unsupported qualification track appears.

The current package is valid only after all 13 permitted machine attestations are present.

## Output structure

```text
human-review-handoff/
├── README.md
├── handoff.json
├── tracks/
│   ├── domain-authority.json
│   ├── domain-authority.md
│   ├── editorial-and-scope.json
│   ├── editorial-and-scope.md
│   ├── methods-and-inference.json
│   ├── methods-and-inference.md
│   ├── source-and-provenance.json
│   ├── source-and-provenance.md
│   ├── reproducibility.json
│   └── reproducibility.md
└── entities/
    └── content/canonical/feedback/
        └── exact Markdown snapshots
```

## Exact snapshot integrity

For every referenced entity, `handoff.json` records:

- exact entity ID;
- exact revision;
- title and entity type;
- original canonical repository path;
- SHA-256 digest.

The `entities/` directory contains a byte-for-byte copy of each canonical Markdown file. This allows a reviewer to inspect the exact material tied to the requested review even when the repository later changes.

A review still targets the recorded entity revision, not merely the copied filename.

## Qualification tracks

The current handoff contains 25 tasks in five tracks:

| Track | Tasks | Minimum authority |
|---|---:|---|
| Domain authority | 7 | independent control-systems, dynamical-systems, or difference-equation expertise |
| Editorial and scope | 7 | accountable human technical editor; internal or independent as policy permits |
| Methods and inference | 5 | independent mathematical-modeling or scientific-inference expertise |
| Source and provenance | 5 | accountable human source, locator, and provenance review |
| Independent reproducibility | 1 | independent human reproduction of the generated source procedure |

The handoff assigns no person to any track.

## Task contents

Each task records:

- canonical task ID;
- exact entity and revision;
- review type and qualification track;
- priority and gate status;
- required reviewer kind, independence, qualification, and accountability;
- exact canonical file and digest;
- existing records that do not yet satisfy coverage;
- unresolved blockers;
- internal and external dependents;
- acceptance criteria;
- a submission worksheet.

The existing major periodicity-proof finding remains visible in the domain-authority packet.

## Generate the package

```bash
python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir phase1-reports/human-review-handoff \
  --expect-task-count 25 \
  --expect-track-count 5
```

The command prints a deterministic directory digest. CI generates the package on Python 3.11 and 3.13 and uploads it with the other Phase 1 reports.

## Reviewer workflow

1. Open the relevant track Markdown file.
2. Confirm the requested review is within the reviewer's qualification.
3. Verify the exact entity ID, revision, canonical path, and SHA-256 digest.
4. Read the copied canonical entity and relevant dependents or sources.
5. Disclose independence and conflicts before making a judgment.
6. Record findings with severity, status, rationale, affected fields, and proposed action.
7. Return one `atlas-review/0.1` record per entity revision and review type.
8. Validate each record.
9. Regenerate coverage and backlog.
10. Change canonical content through a new revision when findings require edits.
11. Never edit lifecycle status directly because one review passed.

## Submission validation

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/<record>.json
```

A valid record can still fail to satisfy coverage when:

- it targets another revision;
- independence or qualification is insufficient;
- its review horizon is expired;
- it does not permit promotion;
- critical or major findings remain unresolved;
- another required review class is missing.

## Prohibited shortcuts

Do not:

- invent a reviewer or credentials;
- assign a person automatically from the handoff generator;
- reuse one record for another entity, revision, or review type;
- convert machine or AI-assisted preparation into human authority;
- hide an existing blocker from a reviewer packet;
- replace exact snapshots with an unversioned summary;
- treat a signed broad approval letter as 25 exact task records;
- promote Atlas content or a future Principia artifact automatically.

## Principia & Atlas boundary

The handoff prepares Atlas knowledge for accountable authority. It does not review a Principia explanation, simulation, investigation, or system dossier.

When the Atlas slice eventually reaches an eligible state, Principia may pin exact reviewed revisions. Principia still requires its own pedagogical, simulation, safety, and release review, while Atlas retains ownership of knowledge provenance and lifecycle.
