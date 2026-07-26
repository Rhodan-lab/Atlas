# Delayed-Feedback Human Review Plan

## Purpose

This document converts the remaining complete-slice backlog into bounded qualification tracks for accountable human reviewers.

It is a planning and handoff artifact. It is not a review record, does not assign a person, does not resolve findings, and does not change lifecycle status.

## Current state

After deterministic machine attestations:

- coverage decision: `blocked`;
- remaining gate tasks: `25`;
- automation-eligible tasks: `0`;
- human-required tasks: `25`;
- advisory tasks: `0`.

The remaining tasks are grouped by required competence rather than by file count.

## Track 1 — Domain authority

**Task count:** 7  
**Reviewer profile:** independent reviewer with demonstrable control-systems, dynamical-systems, or difference-equation expertise.

Exact targets:

- `claim:en:model-oscillation-does-not-prove-real-system@1`;
- `claim:en:stated-delayed-recurrence-oscillates@1`;
- `model:en:delayed-correction-recurrence@1`;
- `synthesis:en:delayed-feedback-and-oscillation@1`;
- `concept:en:feedback@1`;
- `concept:en:oscillation@1`;
- `question:en:when-delayed-correction-can-oscillate@1`.

Primary decisions:

- whether `oscillatory`, `periodic`, `bounded`, `convergent`, and `stable` are used correctly;
- whether the ordered state required by the recurrence is represented clearly;
- whether the formal claim is exactly scoped to its gain, delay, and initial conditions;
- whether the concept definitions preserve cross-domain boundaries;
- whether the synthesis overstates the formal result.

Known blocker:

`review:domain:feedback-oscillation-r1:2026-07-26` currently has outcome `changes-required` and an unresolved major finding:

`finding:feedback:periodicity-proof`

The finding must be resolved with an exact argument or the affected entity must remain blocked.

## Track 2 — Editorial and scope accountability

**Task count:** 7  
**Reviewer profile:** accountable human editor capable of checking technical scope, qualifiers, internal consistency, and reader-facing interpretation. Independence may be internal or independent under policy.

Exact targets:

- the same two claims;
- the recurrence model;
- the synthesis;
- both concepts;
- the research question.

Primary decisions:

- whether each entity has one inspectable purpose;
- whether qualifiers and limitations are visible rather than buried;
- whether the question, claims, model, and synthesis use consistent terminology;
- whether confidence wording matches the exact evidence;
- whether a reader could mistake formal evidence for real-world observation;
- whether future Principia material can quote the result without losing its boundary.

## Track 3 — Methods and inference

**Task count:** 5  
**Reviewer profile:** independent reviewer qualified in mathematical modeling, scientific inference, system identification, or a closely related methodology.

Exact targets:

- `claim:en:model-oscillation-does-not-prove-real-system@1`;
- `claim:en:stated-delayed-recurrence-oscillates@1`;
- `evidence:en:delayed-feedback-periodic-sequence@1`;
- `model:en:delayed-correction-recurrence@1`;
- `synthesis:en:delayed-feedback-and-oscillation@1`.

Primary decisions:

- whether the generated sequence is correctly classified as model-derived evidence;
- whether the evidence supports only the exact formal claim;
- whether assumptions and failure modes are sufficient;
- whether the model-to-world transfer limitation is methodologically correct;
- whether the synthesis distinguishes demonstration, explanation, identification, and empirical validation;
- whether any broader claim requires additional evidence or a narrower scope.

## Track 4 — Source and provenance

**Task count:** 5  
**Reviewer profile:** accountable human reviewer able to inspect bibliographic identity, source use, provenance paths, locators, and claim-source boundaries. Independence may be internal or independent under policy.

Exact targets:

- `src:astrom-murray-2008-feedback-systems@1`;
- `src:synthetic-feedback-run-delay-one-gain-one@1`;
- `evidence:en:delayed-feedback-periodic-sequence@1`;
- `claim:en:model-oscillation-does-not-prove-real-system@1`;
- `synthesis:en:delayed-feedback-and-oscillation@1`.

Primary decisions:

- whether the external reference metadata and locator are accurate;
- whether established terminology is attributed without implying that the exact fixture appears in the reference;
- whether the generated source records its origin and procedure honestly;
- whether the evidence transformation is reproducible and traceable;
- whether the synthesis provenance path is complete;
- whether source roles are kept separate from domain or methodological authority.

## Track 5 — Independent reproducibility of generated source

**Task count:** 1  
**Reviewer profile:** independent accountable human able to reproduce the generated model-run source and inspect the recorded procedure.

Exact target:

- `src:synthetic-feedback-run-delay-one-gain-one@1`.

Primary decisions:

- independently reproduce the generated output;
- confirm that the source record accurately describes the procedure;
- confirm that no hidden data or unstated step is required;
- verify that the generated source is not presented as empirical observation;
- state any limitation not captured by the machine calculation.

The existing machine reproduction of the claim, evidence, and model does not satisfy this human-required source-level reproducibility task.

## Review record requirements

Each completed task requires one `atlas-review/0.1` record with:

- exact entity ID and revision;
- one review type;
- reviewer identity or stable accountable role;
- qualification;
- independence;
- conflicts, including an explicit empty list when none are known;
- bounded outcome;
- structured findings;
- review date and horizon when applicable;
- a clear `permits_promotion` decision for that exact review type.

A reviewer may cover multiple tasks, but each task must remain independently inspectable. A broad letter or one generic approval cannot silently satisfy unrelated review types.

## Recommended execution order

1. Resolve the major periodicity-proof finding through domain and methods review.
2. Review the model, generated evidence, and formal claim as one coordinated formal bundle.
3. Review the model-to-world boundary and synthesis together.
4. Complete source/provenance review after any formal revisions settle.
5. Complete editorial review against the final exact revisions.
6. Regenerate coverage and backlog.
7. Consider lifecycle promotion only when no required review class remains missing and no major or critical finding remains open.

## Principia & Atlas handoff

This slice should become a reusable Atlas dependency only after its formal result and inference boundary are both reviewed.

A future Principia artifact may then reference:

- the recurrence model;
- the formal claim;
- the generated evidence;
- the methodological limitation;
- the synthesis.

Principia must still own how these are explained, simulated, explored, and connected to a real system. Atlas review does not automatically approve a Principia lesson or simulation, and Principia presentation does not upgrade Atlas authority.
