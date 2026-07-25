# Atlas Review Records and Fixtures

## Contracts

- Review records: `atlas-review/0.1`
- Promotion manifests: `atlas-promotion/0.1`

The contracts are defined in:

- `docs/phase-1/review-protocol.md`
- `docs/phase-1/promotion-policy.md`

## Records

`records/` contains revision-specific review work.

Current records are AI-assisted internal challenge scans. They:

- identify exact entity revisions;
- disclose that they are AI-assisted and internal;
- record conflicts and qualifications;
- retain open findings;
- set `permits_promotion` to `false`.

They are not independent reviews and must never be counted as domain, legal, ethical, or translation authority.

## Fixtures

`fixtures/` proves governance behavior.

### Expected eligible

- `valid-normative-promotion.json`
- `valid-contested-transition.json`
- `valid-deprecation-transition.json`
- `valid-retraction-transition.json`

### Expected blocked

- `invalid-ai-only-domain-promotion.json`
- `invalid-stale-translation-promotion.json`
- `invalid-open-major-finding.json`

A blocked fixture is successful only when the promotion command exits non-zero for the expected governance reasons.

## Commands

Validate a review record:

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/feedback-domain-ai-assisted.json
```

Evaluate a promotion manifest:

```bash
python tools/foundation-validator/phase1_review_gate.py promotion \
  content/reviews/fixtures/valid-normative-promotion.json
```

Generate a deterministic Markdown report:

```bash
python tools/foundation-validator/phase1_review_gate.py promotion \
  content/reviews/fixtures/invalid-open-major-finding.json \
  --report blocked-report.md
```

The report explains eligibility or blockers. It never edits canonical content or lifecycle status.
