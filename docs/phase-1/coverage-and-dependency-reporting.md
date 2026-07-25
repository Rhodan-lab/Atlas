# Phase 1 Coverage and Dependency Reporting

## Purpose

`atlas-review-coverage/0.1` answers a question that an entity-by-entity promotion decision cannot answer by itself:

> Does a bounded review packet or vertical slice have sufficient exact-revision review coverage, what remains missing, and which dependents would be affected by a change?

The coverage reporter is governance infrastructure. It does not judge truth, perform review, change lifecycle state, or promote content.

## Contracts

- review records: `atlas-review/0.1`;
- lifecycle decisions: `atlas-promotion/0.1`;
- packet and slice coverage: `atlas-review-coverage/0.1`.

A coverage manifest names exact entity revisions, their role in the bounded scope, required review classes, internal dependencies, and optional external dependents.

## Coverage policies

### `all`

Every listed entity is required for the coverage decision. Use this for a tightly bounded review packet.

### `load-bearing`

Only entities marked `load-bearing` determine the overall decision. Supporting and context entities are still reported, but their incomplete state does not falsely block a deliberately narrower gate.

This policy must not be used to hide a load-bearing claim by labeling it as context.

## Entity roles

- `load-bearing` — a conclusion, model, evidence item, or definition whose failure changes the bounded synthesis or application;
- `supporting` — materially useful but replaceable without changing the principal conclusion;
- `context` — included for navigation or interpretation rather than authority.

Roles are local to the manifest. They do not modify the canonical entity.

## Exact-revision coverage

A review counts only when:

1. the review record validates;
2. its entity ID and revision match exactly;
3. its outcome passes;
4. no unresolved critical or major finding blocks it;
5. its review horizon is current at the decision date;
6. reviewer authority satisfies the required review type;
7. an accountable human review permits promotion where human authority is required.

AI-assisted records remain visible as preparation and challenge material, but cannot satisfy independent authority.

## Required review types

The reporter uses the same requirement function as the promotion gate. A manifest may add stricter explicit requirements but cannot remove the automatic minimum.

A methodological claim requires structural, editorial, source, domain, and methodological review. This prevents claims about measurement or inference practice from being promoted through domain and source review alone.

A legal-descriptive claim may explicitly add `legal-context` when its canonical semantics require current legal interpretation even if the generic descriptive-claim profile would not infer that requirement from the entity fields alone.

## Dependency impact

### Internal dependents

An entity may list `depends_on` IDs. The report reverses those links and shows which in-scope entities would require inspection after a revision, deprecation, or retraction.

### External dependents

`external_dependents` are opaque references supplied by another repository. Atlas validates only the reference structure and the targeted in-scope Atlas IDs.

Example future reference:

```json
{
  "id": "principia:system-dossier:refrigerator",
  "kind": "principia-artifact",
  "repository": "Rhodan-lab/principle-to-system",
  "revision": 3,
  "role": "load-bearing",
  "depends_on": [
    "model:en:delayed-correction-recurrence"
  ]
}
```

This creates a safe future boundary for **Principia & Atlas**:

- Atlas owns knowledge identity, evidence, review, lifecycle, and staleness;
- Principia owns explanation, pedagogy, pathways, systems, investigations, and design experiences;
- Atlas may report that a Principia artifact is affected;
- Atlas does not validate Principia's pedagogical status;
- Principia does not inherit Atlas review status automatically;
- Atlas does not import or require the Principia repository to validate its own corpus.

No current coverage manifest declares a live Principia dependency. The field is implemented now so later bridge work does not require changing Atlas's review semantics.

## Commands

Validate coverage manifests:

```bash
python tools/foundation-validator/phase1_coverage_report.py validate-manifest \
  content/reviews/coverage/*.json
```

Generate a report:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/catalase-methodology.json \
  --records-dir content/reviews/records \
  --report phase1-reports/catalase-methodology.md
```

The current packet manifests are intentionally expected to be blocked because accountable independent review is still missing:

```bash
python tools/foundation-validator/phase1_coverage_report.py coverage \
  content/reviews/coverage/catalase-methodology.json \
  --records-dir content/reviews/records \
  --expect blocked
```

`--expect blocked` confirms that known blockers remain visible. It does not turn a blocked result into a pass.

## Current bounded manifests

- catalase assay methodology;
- delayed-feedback domain terminology and formal result;
- recommender legal-context governance;
- English–Indonesian delayed-feedback translation.

These manifests cover the target entities of the existing reviewer packets. They are not yet complete vertical-slice closure manifests.

## Phase 1 implications

This work satisfies the infrastructure part of deterministic coverage reporting. Phase 1 remains incomplete until:

- accountable human reviews are recorded;
- at least one complete vertical slice is represented by a coverage manifest;
- every required entity in that slice has sufficient exact-revision review;
- open major findings are resolved or the affected entity remains blocked;
- a completion report recommends or rejects entry to Phase 2.
