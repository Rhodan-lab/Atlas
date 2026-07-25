# Atlas Foundation Index

## Status

This directory is the authoritative Phase 0 foundation. Atlas is now a **verification-ready mature draft**, not a completed phase. Documents are binding or provisional according to their stated status and the decision register.

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
| 8 | [`13-claim-scope-and-argument-policy.md`](13-claim-scope-and-argument-policy.md) | Claim atomicity, kinds, scope, and embedded argument structure. |
| 9 | [`14-evidence-data-and-restricted-source-policy.md`](14-evidence-data-and-restricted-source-policy.md) | Access classes, copyright, units, datasets, private evidence, and lineage. |
| 10 | [`15-review-governance-and-disagreement.md`](15-review-governance-and-disagreement.md) | Reviewer roles, conflicts, findings, disagreement, and review staleness. |
| 11 | [`16-revision-impact-and-staleness.md`](16-revision-impact-and-staleness.md) | Dependency impact, stale states, propagation, and human judgment boundary. |

## Governance and delivery

| Document | Purpose |
|---|---|
| [`04-language-and-architecture-policy.md`](04-language-and-architecture-policy.md) | How implementation and language choices earn approval. |
| [`05-phase-gates.md`](05-phase-gates.md) | Evidence required before later phases. |
| [`06-current-prototype-audit.md`](06-current-prototype-audit.md) | Evaluation of existing software without architectural lock-in. |
| [`07-decision-register.md`](07-decision-register.md) | Accepted, provisional, open, and rejected decisions. |
| [`08-reference-slice-plan.md`](08-reference-slice-plan.md) | Scope of the three ontology tests. |
| [`09-validation-matrix.md`](09-validation-matrix.md) | Rules mapped to fixtures, diagnostics, review, and phase gates. |
| [`17-phase-0-maturity-assessment.md`](17-phase-0-maturity-assessment.md) | Current maturity, blockers, and completion work packages. |

Repository-level rules are in [`../../PROJECT_STATE.md`](../../PROJECT_STATE.md), [`../../AGENTS.md`](../../AGENTS.md), and [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Evidence corpus

- [`../../content/reference/README.md`](../../content/reference/README.md) — corpus status and conventions
- [`../../content/reference/slice-a-catalase.md`](../../content/reference/slice-a-catalase.md) — empirical biology and assay scope
- [`../../content/reference/slice-b-feedback.md`](../../content/reference/slice-b-feedback.md) — formal model and reproducible derivation
- [`../../content/reference/slice-c-recommenders.md`](../../content/reference/slice-c-recommenders.md) — socio-technical evidence and normative reasoning
- [`../../content/fixtures/invalid/README.md`](../../content/fixtures/invalid/README.md) — invalid cases and expected diagnostic codes

All reference content is `draft` until independently reviewed.

## Authority and conflict handling

- `PROJECT_STATE.md` defines the active phase and freeze.
- This directory defines product and knowledge semantics.
- The decision register identifies which policies are accepted or provisional.
- Accepted ADRs define implementation decisions after foundation requirements exist.
- Reviewed canonical content outranks prototype examples.
- Prototype code is experimental evidence, not semantic authority.
- Conflicts between documents are recorded and resolved before implementation depends on them.

## Maturity rule

A foundation rule advances only when:

- terminology is consistent;
- at least one representative fixture uses it;
- invalid behavior and expected diagnostics are specified;
- reviewers can apply it without reading code;
- migration and revision consequences are understood;
- unresolved issues remain visible.

A long document without fixtures is only defined. A fixture without review is only exercised.

## Current work sequence

1. Split bundled slices into canonical entity files.
2. Add multilingual, migration, identity, and staleness fixtures.
3. Verify source metadata and evidence locators.
4. Record independent review findings.
5. Compare Phase 1 validator options through the ADR template.
6. Implement only the selected validator.
7. Produce the Phase 0 completion report.

## Change rule

Substantive changes state:

- the fixture, review finding, or decision exposing the problem;
- affected invariants and documents;
- compatibility, migration, and review impact;
- unresolved consequences;
- validation performed.

Do not change a semantic definition merely to preserve prototype code or make parsing easier.
