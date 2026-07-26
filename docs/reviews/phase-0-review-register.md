# Phase 0 Review Register

## Purpose

This register prevents machine validation, AI-assisted verification, internal editorial work, and independent human review from being presented as equivalent.

No canonical reference item is promoted from `draft` by this register.

## Review status vocabulary

- **passed-machine** — deterministic validator or reproducibility check passed;
- **completed-internal** — maintainers completed a documented review, but it is not independent external sign-off;
- **verified-metadata** — bibliographic or locator identity matched an authoritative source;
- **pending-independent** — an appropriately qualified independent reviewer has not signed the revision;
- **not-applicable** — review type does not apply to the item;
- **blocked** — a known critical or major issue prevents review completion.

## Foundation-level reviews

| Review area | Status | Evidence | Limitation |
|---|---|---|---|
| contract structure | passed-machine | `phase-0-structural-validation.md` | conformance is not semantic truth |
| diagnostic specificity | passed-machine | invalid cases and validator suite | future contract versions require new snapshots |
| migration preservation | passed-machine | mechanical and semantic migration fixtures | only representative migrations tested |
| identity and federation | passed-machine | alias, rename, and federation fixture | operational federation not implemented |
| language-qualified identity | passed-machine | neutral synthetic translation and stale-source fixtures | no active translated corpus |
| source metadata and locators | verified-metadata | `phase-0-source-verification.md` | full-text and domain interpretation remain pending |
| cross-document editorial consistency | completed-internal | ontology, relation, evidence, migration, and staleness policies aligned | independent editorial calibration pending |
| architecture restraint | completed-internal | ADR-0001 and feature freeze | later architecture requires bounded evidence |

## Catalase slice

| Review type | Status | Notes |
|---|---|---|
| structural | passed-machine | all canonical files and references valid |
| source | verified-metadata | source records matched authoritative metadata |
| editorial | completed-internal | universal-optimum wording removed; assay scope explicit |
| domain | pending-independent | biochemistry reviewer required |
| methodological | pending-independent | assay, proxy, and generalization reviewer required |
| reproducibility | not-applicable | no empirical calculation is reproduced in this slice |
| ethical | not-applicable | no material ethical recommendation |

## Delayed-feedback slice

| Review type | Status | Notes |
|---|---|---|
| structural | passed-machine | all canonical files and references valid |
| source | verified-metadata | authoritative feedback-reference metadata matched |
| editorial | completed-internal | formal result separated from real-system inference |
| domain | pending-independent | control-systems terminology reviewer required |
| methodological | completed-internal | model-to-world inference boundary explicit |
| reproducibility | passed-machine | sequence independently recalculated in tests |
| ethical | not-applicable | no material ethical recommendation |

## Recommender slice

| Review type | Status | Notes |
|---|---|---|
| structural | passed-machine | all canonical files and references valid |
| source | verified-metadata | study and legal identifiers and locators matched |
| editorial | completed-internal | observational, causal, legal, interpretive, and normative layers separated |
| domain | pending-independent | recommender-systems and political-communication reviewers required |
| methodological | pending-independent | experiment, measurement, and generalization review required |
| reproducibility | pending-independent | published empirical results were not independently recomputed |
| ethical | pending-independent | autonomy, accountability, accessibility, safety, and feasibility trade-offs require review |
| legal context | pending-independent | legal interpretation requires qualified review and horizon monitoring |
| conflict | completed-internal | platform employment and data-access limitations are visible |

## English-only amendment

The active authored corpus and review program were narrowed to English during Phase 1.

- previously authored translated examples were removed;
- language-specific review work is no longer a blocking Phase 1 requirement;
- translation semantics remain tested only through neutral synthetic fixtures;
- multilingual authoring requires an explicit future reopening decision.

## Blocking findings

### Critical

None identified by machine and internal consistency reviews.

### Major

The following remain major for promoting reference content to `reviewed`, not for accepting the foundation architecture:

1. independent biochemical and assay-method review;
2. independent control-systems terminology review;
3. independent recommender-methodology and political-communication review;
4. independent ethical and legal-context review.

## Closure interpretation

The Phase 0 foundation specification and executable fixture system can be accepted when its mechanical gates pass and its remaining human-review requirements are explicitly preserved.

The reference content cannot be called reviewed until pending independent reviews are recorded for exact revisions.

This avoids two dishonest extremes:

- claiming content authority from passing a schema validator;
- preventing the foundation architecture from stabilizing until every example becomes publication-grade research.

## Next review action

Independent reviewers should submit revision-specific findings without changing lifecycle status until critical and major findings are resolved. Disagreement must remain visible under the review-governance policy.
