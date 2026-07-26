# Atlas Foundation and Review Validators

## Active scope

The active validation path checks:

- the English authored-content contract;
- deterministic migration, identity, and synthetic staleness fixtures;
- the comprehensive delayed-feedback AI review;
- the exact period-six recurrence proof;
- exact reviewed entity revisions;
- explicit non-human review labeling;
- `human_review_required: false`.

Human handoff, intake, admission, backlog, and promotion tools remain available as optional historical governance experiments. They are not active Phase 1 duties or Phase 2 blockers.

## Setup

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r tools/foundation-validator/requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## Foundation validator

```bash
python tools/foundation-validator/atlas_foundation_validator.py validate \
  content/canonical
```

The active authored corpus is English-only. Translation identity and staleness are tested only through neutral synthetic fixtures.

## Phase 1 AI review validator

```bash
python tools/foundation-validator/phase1_ai_review.py \
  content/reviews/ai/feedback-delayed-comprehensive.json \
  --canonical-root content/canonical
```

Expected output:

```text
ai-review=pass; entities=10; exact-period=6; human-review-required=false
```

The validator checks:

- contract `atlas-ai-review/0.1`;
- canonical AI-review ID;
- reviewer kind `ai`;
- `human_verified: false`;
- reviewer limitations;
- authoritative source locator and matched metadata;
- exact recurrence sequence;
- ordered state-pair return;
- exact period 6;
- all ten canonical entity IDs and revisions;
- review dimensions and outcomes;
- required resolved findings;
- no open critical or major finding;
- overall `pass`;
- review level `ai-reviewed`;
- `human_review_required: false`.

The validator does not claim human identity, credentials, professional accountability, or empirical system testing.

## Active tests

```bash
python -m unittest discover \
  -s tools/foundation-validator/tests \
  -p 'test_phase1_ai_review.py' \
  -v
```

The active tests reject:

- a false human-verification claim;
- reintroduction of a mandatory human-review duty;
- an incorrect sequence;
- an incorrect period;
- missing entities;
- wrong reviewed revisions;
- open major findings;
- an unrecognized source locator.

## Optional human verification tools

The following tools are preserved but inactive:

### Exact-revision review records

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/<record>.json
```

### Coverage and backlog

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --expect blocked \
  --report optional-human-coverage.md
```

### Human handoff

```bash
python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir optional-human-handoff
```

### Intake and admission

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff optional-human-handoff/handoff.json

python tools/foundation-validator/phase1_review_admission.py validate \
  admission.json \
  reviewer-submission.json \
  --handoff optional-human-handoff/handoff.json
```

These tools must not be described as required work. A future human review must remain separately labeled and may not overwrite the AI review identity.

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

The final command must return `possibly-stale` for the synthetic fixture.

## Authority boundary

Machine validation and AI review can provide bounded evidence for structure, mathematics, reproducibility, source metadata, internal consistency, and explicit inference limits.

They do not become human professional verification merely because they are detailed. Atlas must always display the actual review kind and review level.
