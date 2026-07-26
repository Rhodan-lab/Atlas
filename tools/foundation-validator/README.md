# Atlas Foundation and Review Validators

## Scope

These bounded Python tools verify accepted Atlas contracts and deterministic fixtures.

They do **not**:

- decide whether a scientific claim is true;
- decide whether a source interpretation is adequate;
- assign confidence automatically;
- rewrite authored content;
- grant `reviewed` status;
- create human accountability;
- define the future Atlas runtime.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r tools/foundation-validator/requirements.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Foundation validator

Validate the English canonical corpus:

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
```

Warnings remain visible but do not fail the command unless `--warnings-as-errors` is supplied.

The active authored corpus is English-only. Translation identity and staleness are tested through neutral synthetic fixtures, not authored files under `content/translations/`.

## Review gate

Validate one exact-revision review record:

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/feedback-domain-ai-assisted.json
```

Evaluate a bounded promotion fixture:

```bash
python tools/foundation-validator/phase1_review_gate.py promotion \
  content/reviews/fixtures/valid-normative-promotion.json
```

The review gate enforces reviewer kind, qualification, independence, accountability, conflicts, review horizon, findings, exact revision, and lifecycle requirements.

## Coverage reporter

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report phase1-coverage.md
```

Coverage reports required, satisfied, and missing review classes plus dependency impact. They never promote content.

## Review backlog

```bash
python tools/foundation-validator/phase1_review_backlog.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --json-out phase1-backlog.json \
  --report phase1-backlog.md
```

The backlog separates automation-eligible and human-required tasks and records qualification requirements. It does not assign reviewers or count as completed review.

## Machine attestations

Generate the exact permitted machine records:

```bash
python tools/foundation-validator/phase1_machine_attestations.py generate \
  --records-dir content/reviews/records
```

Verify committed records against deterministic output:

```bash
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

The generator is intentionally limited to:

- structural conformance for all ten entities in the complete delayed-feedback slice;
- fully specified recurrence reproducibility for the formal claim, generated evidence, and model.

Every generated record is machine-only, non-accountable, and unable to permit promotion.

## Run all tests

```bash
python -m unittest discover -s tools/foundation-validator/tests -v
```

The suite covers valid corpus behavior, deterministic diagnostics, migrations, identity, synthetic translation staleness, review authority, lifecycle transitions, coverage, backlog generation, and machine-attestation drift.

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

Diagnostics contain:

- severity;
- stable code;
- path;
- deterministic message.

They are sorted by path, code, and message. Validators report safely independent findings in one pass and never edit authored meaning.

## Authority boundary

When validator behavior conflicts with an accepted foundation decision, the validator is wrong. Update implementation and fixtures through review; do not weaken the authored contract merely to make a test pass.

Machine conformance and arithmetic reproduction are evidence about bounded procedures. They are not scientific, editorial, methodological, legal, ethical, or lifecycle authority.
