# Review Packet — Catalase and Assay Methodology

## Requested reviews

- domain: biochemistry or enzymology
- methodological: enzyme assay design and interpretation

## Exact primary target

- Entity: `claim:en:catalase-optimum-requires-assay-scope`
- Revision: `1`
- File: `content/canonical/catalase/claim-optimum-requires-assay-scope.md`
- Current status: `draft`

## Linked records in scope

- `src:aebi-1984-catalase-in-vitro`
- `src:wu-lin-wolfbeis-2003-catalase-assay`
- `evidence:en:fluorescent-assay-neutral-ph`
- `concept:en:catalase`
- `model:en:catalase-assay-observation-model`
- `synthesis:en:catalase-assay-conditions`
- `question:en:catalase-assay-conditions`

All are revision 1 unless the canonical file states otherwise. Stop review if any target revision has changed.

## Claim under review

> A reported optimum pH or temperature for catalase should be interpreted together with the enzyme source, assay definition, exposure duration, and measurement method.

The review concerns this methodological interpretation rule. It does not ask the reviewer to establish one universal catalase optimum.

## Source checks

### Aebi method reference

- Verify author, title, venue, year, pages, PMID, and DOI.
- Confirm that the record is used as a method reference, not as evidence for one universal optimum.
- Confirm whether the canonical limitations are sufficient given that the PubMed record has no abstract.

### Wu–Lin–Wolfbeis fluorescent assay

- Verify bibliographic metadata and exact assay description.
- Confirm the reported pH result and the scope of the measurement method.
- Confirm whether the current evidence wording distinguishes assay performance from a universal enzyme property.

## Methodological questions

1. Does the statement correctly distinguish enzyme source from assay definition?
2. Is `exposure duration` necessary and correctly placed?
3. Does the evidence support an interpretation rule, or is the confidence label too strong for the limited source set?
4. Are immediate temperature effects on reaction rate distinguished from retained activity after thermal exposure?
5. Does the classroom observation model distinguish oxygen production, foam formation, tissue geometry, mixing, and gas retention?
6. Are purified-enzyme kinetics and tissue-level proxy observations kept separate?
7. Would a protocol or method entity be required to review the assay faithfully, or is the current model sufficient?
8. Which fields must be added before comparing measurements across studies?

## Generalization challenge

The reviewer should actively test whether the current wording could be misread as:

- one universal optimal pH;
- one universal optimal temperature;
- direct equivalence between foam height and catalytic rate;
- equivalence between activity during exposure and thermal stability;
- evidence that all catalases behave similarly.

Any such reading is a material defect.

## Current AI-assisted findings

See:

`content/reviews/records/catalase-methodological-ai-assisted.json`

Open findings:

- major: accountable full-text assay review is missing;
- minor: reaction-rate effects and thermal stability require explicit separation.

These findings are prompts, not authoritative conclusions.

## Pass conditions

A passing methodological record should:

- target revision 1 exactly;
- verify the source-specific assay interpretation;
- confirm or narrow the claim statement;
- assess the `well-supported` confidence label;
- resolve every major finding;
- disclose reviewer conflicts;
- state whether the review permits promotion for the methodological review type.

## Required output

One `atlas-review/0.1` record for `methodological` review and, if the reviewer is qualified, a separate record for `domain` review.

The two review types must not be merged into one broad record.
