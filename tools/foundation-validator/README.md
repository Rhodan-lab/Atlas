# Atlas Foundation and Review Validators

## Scope

These bounded Python tools verify accepted Atlas contracts, deterministic fixtures, machine attestations, reviewer handoffs, and returned submission consistency.

They do **not** decide scientific truth, assign confidence, rewrite authored content, grant `reviewed` status, create or assign human accountability, resolve findings, accept returned reviews automatically, or define the future Atlas runtime.

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

The package contains `atlas-review-handoff/0.1`, five qualification-track bundles, all 25 human tasks exactly once, ten exact Markdown snapshots, original paths and SHA-256 digests, blockers and dependents, and no reviewer assignment.

## Review submission intake

Validate a returned `atlas-review-submission/0.1` envelope:

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Extract the proposed nested review record with intake lineage:

```bash
python tools/foundation-validator/phase1_review_intake.py extract \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/extracted-review.json
```

Intake verifies:

- active coverage and task identity;
- exact entity revision and snapshot SHA-256;
- matching review type;
- human reviewer kind and accountability;
- required independence;
- qualification and conflicts;
- nested `atlas-review/0.1` validity;
- AI-assistance disclosure;
- completion and submission date order.

The extracted record adds `metadata.intake` provenance. The tool never writes to `content/reviews/records/` automatically and does not accept the review into authority.

## Run all tests

```bash
python -m unittest discover -s tools/foundation-validator/tests -v
```

The suite covers corpus validation, deterministic diagnostics, migrations, identity, synthetic translation staleness, review authority, lifecycle transitions, coverage, backlog generation, machine-attestation drift, handoff task uniqueness, snapshot integrity, blocker preservation, return-envelope matching, human authority, independence, AI disclosure, intake lineage, and no automatic repository writes.

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

Machine conformance, arithmetic reproduction, backlogs, reviewer bundles, valid submission envelopes, and extracted proposed records are bounded evidence-transfer or planning artifacts. They are not scientific, editorial, methodological, source, legal, ethical, human, or lifecycle authority.
