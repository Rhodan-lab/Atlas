# Atlas Foundation Index

## Status

This directory is the authoritative Phase 0 foundation. Documents are drafts unless their own status and review record state otherwise.

## Reading order

| Order | Document | Purpose |
|---:|---|---|
| 1 | [`00-charter.md`](00-charter.md) | Defines what Atlas is, who it serves, its principles, and non-goals. |
| 2 | [`01-knowledge-model.md`](01-knowledge-model.md) | Defines canonical entities and invariants. |
| 3 | [`02-evidence-and-editorial-policy.md`](02-evidence-and-editorial-policy.md) | Defines lifecycle, review, evidence appraisal, disagreement, and revision. |
| 4 | [`03-content-contract.md`](03-content-contract.md) | Defines authoritative Markdown records and compilation limits. |
| 5 | [`10-relation-vocabulary.md`](10-relation-vocabulary.md) | Defines relation meanings, direction, compatibility, and validation. |
| 6 | [`04-language-and-architecture-policy.md`](04-language-and-architecture-policy.md) | Defines how implementation and language choices earn approval. |
| 7 | [`05-phase-gates.md`](05-phase-gates.md) | Defines evidence required before moving to later phases. |
| 8 | [`06-current-prototype-audit.md`](06-current-prototype-audit.md) | Evaluates existing software without treating it as final. |
| 9 | [`07-decision-register.md`](07-decision-register.md) | Separates accepted, provisional, open, and rejected decisions. |
| 10 | [`08-reference-slice-plan.md`](08-reference-slice-plan.md) | Defines the three representative ontology tests. |
| 11 | [`09-validation-matrix.md`](09-validation-matrix.md) | Maps foundation rules to positive fixtures, negative fixtures, and review. |

Repository-level rules are in [`../../PROJECT_STATE.md`](../../PROJECT_STATE.md), [`../../AGENTS.md`](../../AGENTS.md), and [`../../CONTRIBUTING.md`](../../CONTRIBUTING.md).

## Authority and conflict handling

- `PROJECT_STATE.md` defines the active phase and development freeze.
- This directory defines product and knowledge semantics.
- Accepted ADRs define approved implementation decisions.
- Prototype code demonstrates experiments but is not semantically authoritative.
- When two foundation documents conflict, record the conflict in the decision register and resolve it before implementation depends on either interpretation.

## Document maturity

A foundation document is not mature because it is long or detailed. It advances only when:

- terminology is consistent with the other documents;
- representative positive and negative fixtures exist;
- reviewers can apply the rule without reading implementation code;
- failure behavior is defined;
- unresolved decisions are visible;
- changes preserve decision history and migration consequences.

## Phase 0 working sequence

1. Run cross-document consistency review.
2. Resolve blocking open decisions for the reference corpus.
3. Author the three vertical slices as `draft` content.
4. Create valid and invalid fixtures.
5. Apply the validation matrix.
6. Revise ontology and contracts based on actual failures.
7. Produce a Phase 0 completion report.
8. Select the smallest Phase 1 validator implementation.

## Change rule

Substantive changes must identify:

- the problem exposed by a fixture, review, or decision;
- affected invariants and documents;
- compatibility or migration impact;
- unresolved consequences;
- validation used.

Do not change a definition merely to make the existing prototype easier to preserve.
