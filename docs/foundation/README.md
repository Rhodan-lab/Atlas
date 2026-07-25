# Atlas Foundation Index

## Status

This directory is the authoritative Phase 0 foundation for `atlas-content/0.1`.

**Current state:** closure candidate. The specification, canonical fixtures, migrations, multilingual lineage, and validator matrix are mechanically complete. Final acceptance requires green PR #3 checks and maintainer merge.

Canonical example content remains `draft`. Phase 0 acceptance does not substitute machine validation for expert review.

## Core reading order

| Order | Document | Purpose |
|---:|---|---|
| 1 | [`00-charter.md`](00-charter.md) | Product purpose, users, principles, and non-goals. |
| 2 | [`01-knowledge-model.md`](01-knowledge-model.md) | Canonical entities and invariants. |
| 3 | [`02-evidence-and-editorial-policy.md`](02-evidence-and-editorial-policy.md) | Lifecycle, evidence appraisal, uncertainty, disagreement, and AI limits. |
| 4 | [`03-content-contract.md`](03-content-contract.md) | `atlas-content/0.1` authored Markdown structure. |
| 5 | [`10-relation-vocabulary.md`](10-relation-vocabulary.md) | Relation meaning, direction, allowed pairs, and validation. |
| 6 | [`11-contract-versioning-and-migrations.md`](11-contract-versioning-and-migrations.md) | Contract versions, compatibility, migration, and rollback. |
| 7 | [`12-authoring-language-and-translation-policy.md`](12-authoring-language-and-translation-policy.md) | Multilingual identity, terminology, translation, and review. |
| 8 | [`13-claim-scope-and-argument-policy.md`](13-claim-scope-and-argument-policy.md) | Claim atomicity, kinds, scope, and embedded arguments. |
| 9 | [`14-evidence-data-and-restricted-source-policy.md`](14-evidence-data-and-restricted-source-policy.md) | Access classes, copyright, units, datasets, private evidence, and lineage. |
| 10 | [`15-review-governance-and-disagreement.md`](15-review-governance-and-disagreement.md) | Reviewer roles, conflicts, findings, disagreement, and review staleness. |
| 11 | [`16-revision-impact-and-staleness.md`](16-revision-impact-and-staleness.md) | Dependency impact, stale states, propagation, and human judgment boundary. |
| 12 | [`18-phase-0-closure-report.md`](18-phase-0-closure-report.md) | Gate evidence, closure interpretation, and Phase 1 recommendation. |

## Governance and delivery

| Document | Purpose |
|---|---|
| [`04-language-and-architecture-policy.md`](04-language-and-architecture-policy.md) | How implementation and language choices earn approval. |
| [`05-phase-gates.md`](05-phase-gates.md) | Phase 0 closure and later phase evidence requirements. |
| [`06-current-prototype-audit.md`](06-current-prototype-audit.md) | Evaluation of existing software without architectural lock-in. |
| [`07-decision-register.md`](07-decision-register.md) | Accepted, provisional, superseded, open, and rejected decisions. |
| [`08-reference-slice-plan.md`](08-reference-slice-plan.md) | Scope of the three ontology stress tests. |
| [`09-validation-matrix.md`](09-validation-matrix.md) | Rules mapped to fixtures, diagnostics, review, and gates. |
| [`17-phase-0-maturity-assessment.md`](17-phase-0-maturity-assessment.md) | Pre-closure assessment retained as historical state. |

Repository-level rules are in [`../../PROJECT_STATE.md`](../../PROJECT_STATE.md), [`../../AGENTS.md`](../../AGENTS.md), and [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Executable corpus

### Canonical English records

- [`../../content/canonical/catalase/`](../../content/canonical/catalase/) — empirical biology, measurement proxy, and assay scope;
- [`../../content/canonical/feedback/`](../../content/canonical/feedback/) — formal model, reproducible derivation, and model-to-world limits;
- [`../../content/canonical/recommenders/`](../../content/canonical/recommenders/) — observational and randomized evidence, legal context, conflicts, and normative reasoning.

Total: 34 split canonical entity files.

### Indonesian translation path

- [`../../content/translations/id/feedback/`](../../content/translations/id/feedback/) — complete question, evidence, claim, concept, model, and synthesis path.

Total: 8 translated entity files with independent lifecycle and staleness.

### Boundary fixtures

- [`../../content/fixtures/invalid/README.md`](../../content/fixtures/invalid/README.md) — 24 required diagnostic scenarios;
- [`../../content/fixtures/migrations/`](../../content/fixtures/migrations/) — mechanical preservation and semantic claim split;
- [`../../content/fixtures/identity/`](../../content/fixtures/identity/) — alias, rename, collision, and federation behavior;
- [`../../content/fixtures/translation/`](../../content/fixtures/translation/) — source-revision mismatch and stale translation.

Bundled files in `content/reference/` remain historical drafting artifacts. Executable validation uses the split canonical and translation directories.

## Validator and ADR

- [`../adr/0001-phase-0-validator-baseline.md`](../adr/0001-phase-0-validator-baseline.md) — accepted minimum validator decision;
- [`../../tools/foundation-validator/`](../../tools/foundation-validator/) — bounded Python reference validator and 30-test suite;
- [`../../.github/workflows/foundation.yml`](../../.github/workflows/foundation.yml) — Python 3.11 and 3.13 matrix.

The validator checks conformance only. It cannot judge truth or grant review status.

## Review records

- [`../reviews/phase-0-structural-validation.md`](../reviews/phase-0-structural-validation.md) — machine conformance and reproducibility result;
- [`../reviews/phase-0-source-verification.md`](../reviews/phase-0-source-verification.md) — bibliographic and locator verification ledger;
- [`../reviews/phase-0-review-register.md`](../reviews/phase-0-review-register.md) — completed machine/internal checks and pending independent reviews.

All reference content remains `draft` until exact revisions pass required Phase 1 reviews.

## Authority and conflict handling

- `PROJECT_STATE.md` defines active phase and freeze.
- This directory defines product and knowledge semantics.
- The decision register identifies accepted and provisional policies.
- Accepted ADRs define bounded implementation decisions after requirements exist.
- Reviewed canonical revisions outrank drafts and prototype examples.
- Prototype code is experimental evidence, not semantic authority.
- Conflicts are recorded and resolved before implementation depends on them.

## Maturity rule

A foundation rule is mature only when:

- terminology is consistent;
- representative valid fixtures use it;
- invalid behavior has deterministic diagnostics;
- identity, migration, revision, and review consequences are explicit;
- it remains understandable without implementation code;
- unresolved questions remain visible.

A fixture passing validation means its structure conforms. It does not mean its claims are reviewed or true.

## Phase transition

### Before PR #3 merge

- keep product feature development frozen;
- resolve only closure defects and final CI failures;
- do not promote canonical content.

### After Phase 0 acceptance

Phase 1 performs independent review of the reference corpus, confidence calibration, contradiction/deprecation/retraction exercises, and validator hardening. Broader product engineering remains outside scope until Phase 1 exit criteria are met.

## Change rule

Substantive changes state:

- the fixture, review finding, or decision exposing the problem;
- affected invariants and documents;
- compatibility, migration, and review impact;
- unresolved consequences;
- validation performed.

Do not change a semantic definition merely to preserve prototype code or make parsing easier.
