---
contract: atlas-content/0.1
id: synthesis:en:catalase-assay-conditions
work: work:catalase-assay-conditions
type: synthesis
title: Catalase results must be interpreted within assay conditions
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
question: question:en:how-assay-conditions-affect-catalase
claims:
  - claim:en:catalase-optimum-requires-assay-scope
models:
  - model:en:catalase-assay-observation
evidence_selection: Use an established catalase-method reference and one assay paper whose abstract states a scoped pH optimum; do not infer a universal optimum.
conclusion: Reported catalase activity or stability values belong to defined enzyme preparations, conditions, and measurement methods. A classroom-visible reaction can illustrate condition sensitivity but must not be treated as purified-enzyme kinetics without calibration.
confidence: plausible
confidence_rationale: The methodological boundary is clear, but this small fixture is not a systematic review and remains pending domain and methodological review.
disagreements:
  - different enzyme sources and assays may produce different response profiles
open_questions:
  - which protocol fields should become mandatory in a later contract?
  - when should a protocol become its own canonical entity?
revision_triggers:
  - full-text review changes the assay interpretation
  - a systematic comparison of methods is added
  - the contract introduces a protocol entity
---

## Provenance path

`question:en:how-assay-conditions-affect-catalase` → `src:wu-lin-wolfbeis-2003-catalase-assay` → `evidence:en:fluorescent-catalase-assay-neutral-ph` → `claim:en:catalase-optimum-requires-assay-scope` → `concept:en:catalase` and `model:en:catalase-assay-observation` → this synthesis.

## Limitation

The synthesis is a contract fixture, not reviewed instructional content.
