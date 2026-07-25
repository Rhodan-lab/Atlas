# Atlas Foundation Validator

## Scope

This is the minimum validator selected by ADR-0001 for Phase 0 verification. It checks whether authored files conform to `atlas-content/0.1` and whether fixture expectations are deterministic.

It does **not**:

- decide whether a scientific claim is true;
- decide whether a source is credible enough;
- assign confidence;
- rewrite content;
- grant `reviewed` status;
- define the future Atlas runtime.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r tools/foundation-validator/requirements.txt
```

On Windows PowerShell, activate with `.venv\Scripts\Activate.ps1`.

## Validate the canonical corpus

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical content/translations
```

Warnings remain visible but do not fail the command unless `--warnings-as-errors` is supplied.

## Run the diagnostic contract

```bash
python -m unittest discover -s tools/foundation-validator/tests -v
```

The test suite exercises the 24 invalid scenarios documented in `content/fixtures/invalid/README.md`, plus valid corpus, migration, identity, translation-staleness, and feedback-reproduction cases.

## Validate migration and identity fixtures

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

The last command must return `possibly-stale`.

## Diagnostic contract

Diagnostics contain:

- severity;
- stable code;
- path;
- deterministic message.

They are sorted by path, code, and message. The validator reports safely independent findings in one pass and never edits authored files.

## Authority boundary

When validator behavior conflicts with an accepted foundation decision, the validator is wrong. Update the implementation and fixtures through review; do not weaken the authored contract merely to make a test pass.
