# Atlas Foundation and Review Validators

## Scope

These bounded Python tools verify accepted Atlas contracts, deterministic fixtures, machine attestations, reviewer handoffs, returned submission consistency, and explicit review-record admission decisions.

They do **not** decide scientific truth, assign confidence, rewrite authored content, grant `reviewed` status, create human accountability, perform real-world identity checks, resolve findings, commit returned reviews automatically, or define the future Atlas runtime.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r tools/foundation-validator/requirements.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Foundation validator

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
```

The active authored corpus is English-only. Translation identity and staleness are tested through neutral synthetic fixtures.

## Review gate

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/<record>.json
```

The gate enforces reviewer kind, qualification, independence, accountability, conflicts, horizon, findings, exact revision, and lifecycle requirements.

## Coverage reporter

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report phase1-coverage.md
```

Coverage reports required, satisfied, and missing review classes plus dependency impact. It never promotes content.

## Review backlog

```bash
python tools/foundation-validator/phase1_review_backlog.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --json-out phase1-backlog.json \
  --report phase1-backlog.md
```

The backlog separates automation-eligible and human-required tasks. It does not assign reviewers or count as completed review.

## Machine attestations

```bash
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

The generator is limited to structural conformance and explicitly permitted fully specified recurrence reproduction. Every generated record is machine-only, non-accountable, and unable to permit promotion.

## Human review handoff

```bash
python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir phase1-reports/human-review-handoff \
  --expect-task-count 25 \
  --expect-track-count 5
```

The package contains `atlas-review-handoff/0.1`, five qualification-track bundles, all 25 human tasks exactly once, ten exact Markdown snapshots, paths and SHA-256 digests, blockers and dependents, and no reviewer assignment.

## Review submission intake

Validate a returned `atlas-review-submission/0.1` envelope:

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Extract the proposed nested record with intake lineage:

```bash
python tools/foundation-validator/phase1_review_intake.py extract \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/extracted-review.json
```

Intake verifies active task identity, exact entity revision and snapshot digest, review type, human accountability, required independence, qualification, conflicts, nested review validity, AI-assistance disclosure, and date order.

The extracted record adds `metadata.intake`. The tool never writes to `content/reviews/records/` automatically and does not accept authority.

## Explicit review admission

Validate an `atlas-review-admission/0.1` decision:

```bash
python tools/foundation-validator/phase1_review_admission.py validate \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Write a deterministic receipt:

```bash
python tools/foundation-validator/phase1_review_admission.py receipt \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/admission-receipt.json
```

Prepare a record after an explicit `accept` decision:

```bash
python tools/foundation-validator/phase1_review_admission.py prepare \
  admission.json \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --records-dir content/reviews/records \
  --out phase1-reports/proposed-admitted-review.json
```

Admission validates:

- an accountable human decider declaration;
- `accept`, `request-changes`, or `reject` decision semantics;
- admission and submission date order;
- declared external checks for reviewer identity, qualification, independence, and conflicts;
- non-empty decision rationale;
- duplicate canonical review-ID prevention;
- intake and admission lineage preservation.

Only `accept` may prepare a record. Preparation writes solely to `--out` and never to the canonical review directory.

A `changes-required` record or record with open major findings may be admitted so criticism is preserved. Admission does not change its outcome, remove findings, or promote knowledge.

Synthetic admissions set `test_fixture: true`; their prepared records are forced to `permits_promotion: false`.

## Run all tests

```bash
python -m unittest discover -s tools/foundation-validator/tests -v
```

The suite covers corpus validation, deterministic diagnostics, migrations, identity, synthetic translation staleness, review authority, lifecycle transitions, coverage, backlog generation, machine-attestation drift, handoff uniqueness, snapshot integrity, blocker preservation, return-envelope matching, human authority, independence, AI disclosure, intake lineage, admission decisions, duplicate prevention, finding preservation, fixture promotion suppression, and no automatic repository writes.

## Migration and identity fixtures

```bash
python tools/foundation-validator/atlas_foundation_validator.py migration \
  content/fixtures/migrations/mechanical-0.1-to-0.2.json

python tools/foundation-validator/atlas_foundation_validator.py migration \
  content/fixtures/migrations/semantic-claim-split.json

python tools/foundation-validator/atlas_foundation_validator.py identity \
  content/fixtures/identity/alias-rename-federation.json

python tools/foundation-validator/atlas_foundation_validator.py translation-staleness \
  content/fixtures/translation/stale-source-revision.json
```

The last command must return `possibly-stale` for the synthetic fixture.

## Diagnostic contract

Diagnostics contain severity, stable code, path, and deterministic message. Tools report safely independent findings in one pass and never edit authored meaning.

## Authority boundary

When tool behavior conflicts with an accepted foundation decision, the tool is wrong. Update implementation and fixtures through review; do not weaken the authored contract merely to make a test pass.

Machine conformance, arithmetic reproduction, backlogs, reviewer bundles, valid submissions, intake records, admission receipts, and prepared records are bounded governance artifacts. They are not scientific, editorial, methodological, source, legal, ethical, reviewer-identity, or lifecycle authority.
