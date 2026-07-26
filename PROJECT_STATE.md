# Atlas Project State

## Current status

**Phase 1 — Reference Corpus, Coverage, and Vertical-Slice Readiness (active)**

Phase 0 was accepted through merged PR #3 at commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`. The versioned `atlas-content/0.1` foundation, canonical corpus, multilingual lineage, migration fixtures, identity rules, and deterministic conformance validator are the accepted baseline.

The initial Phase 1 review and promotion infrastructure was merged through PR #4 at commit `09488b76c43fdbe46f94fcb14a27637472adfa38`.

Phase 1 coverage and dependency reporting was merged through PR #5 at commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`. It established `atlas-review-coverage/0.1`, deterministic packet coverage, dependency impact, reviewer submission guidance, and a one-way future Principia compatibility boundary.

Current work expands the delayed-feedback packet into the first complete English vertical-slice readiness scope, a complete Indonesian translation overlay, and a deterministic missing-review backlog.

All reference entities remain `draft`. No AI-assisted record, validator pass, coverage report, readiness manifest, or generated backlog grants scientific, methodological, legal, ethical, editorial, or translation authority.

## Authority order

1. `PROJECT_STATE.md`
2. accepted foundation documents in `docs/foundation/`
3. accepted ADRs
4. canonical authored content and revision-specific review records
5. generated reports, indexes, coverage manifests, and backlogs
6. experimental prototype code

A validator can establish conformance. It cannot establish scientific truth, legal correctness, ethical acceptability, translation equivalence, or reviewer accountability.

## Phase 0 accepted baseline

- `atlas-content/0.1` authored Markdown contract;
- canonical source, evidence, claim, concept, relation, model, question, synthesis, and revision semantics;
- claim-level provenance, scope, uncertainty, and normative-value boundaries;
- controlled relation vocabulary and compatibility;
- multilingual IDs, shared `work` identity, translation lineage, and staleness;
- mechanical and semantic migration rules;
- alias, rename, collision, and federation fixtures;
- deterministic validator and 30-test Phase 0 suite;
- source-verification, structural-validation, review-register, and closure records.

Phase 0 may be reopened only when a representative review, migration, or lifecycle fixture exposes an actual ontology or contract failure.

## Phase 1 implemented baseline

### Review and lifecycle

- `atlas-review/0.1` exact-revision review records;
- `atlas-promotion/0.1` deterministic lifecycle decisions;
- accountable reviewer, qualification, independence, and conflict fields;
- critical and major finding blockers;
- review horizons and expiration behavior;
- AI and machine authority boundaries;
- contested, deprecated, and retracted transition fixtures;
- reviewer-ready packets and submission templates.

### Coverage and provenance

- `atlas-review-coverage/0.1` packet and slice manifests;
- `all` and `load-bearing` coverage policies;
- exact-revision required, satisfied, and missing review classes;
- internal reverse-dependency impact;
- optional opaque external dependents;
- deterministic Markdown and JSON reporting;
- CI proof that known gaps remain blocked rather than masquerading as passes.

### Current bounded packet manifests

1. catalase assay methodology;
2. delayed-feedback domain review;
3. recommender legal context;
4. English–Indonesian feedback translation.

These target individual packet entities and remain intentionally blocked pending accountable review.

## Current vertical-slice readiness work

### Complete English delayed-feedback slice

`content/reviews/coverage/feedback-complete-vertical-slice.json` includes the exact revision-1 question, sources, evidence, claims, concepts, model, and synthesis.

The manifest uses `coverage_requirement: all`; every listed entity must have acceptable coverage before the scope can become coverage-complete.

### Complete Indonesian translation overlay

`content/reviews/coverage/feedback-id-translation-overlay.json` includes every translated delayed-feedback entity and the shared English source context.

The translated entities are load-bearing. Translation approval remains independent from English status and requires accountable bilingual domain authority.

### Deterministic review backlog

`tools/foundation-validator/phase1_review_backlog.py` converts missing coverage into structured tasks that record:

- exact entity ID and revision;
- reviewer track and priority;
- whether the task blocks the selected gate;
- allowed reviewer kinds and independence;
- accountability and qualification requirements;
- existing non-satisfying review records and blockers;
- internal and external dependents;
- task-specific acceptance criteria.

The backlog never assigns a real reviewer, performs review, resolves findings, or changes lifecycle status.

## Phase 1 work packages

### A. Review contract — implemented baseline

- review identity and exact target revision;
- review type, reviewer role, independence, and conflicts;
- outcome and promotion effect;
- structured findings with severity and resolution state;
- reviewed-at date and review horizon;
- evidence or rationale for each decision.

### B. Promotion gate — implemented baseline

- calculate required review types;
- reject wrong-revision records;
- reject unresolved critical or major findings;
- reject authority derived only from AI or machine review;
- reject stale translations and expired time-sensitive reviews;
- preserve disagreement and conflicts;
- require explicit transition records for reviewed, contested, deprecated, and retracted states.

### C. Reviewer packets and submission — implemented baseline

- bounded packets for catalase, delayed feedback, recommender governance, and Indonesian translation;
- code-independent reviewer guide and JSON example;
- explicit prohibition on fabricated reviewers or hidden AI authority.

### D. Coverage and dependency reporting — implemented baseline

- packet and slice coverage manifests;
- deterministic missing-review reports;
- internal reverse-dependency impact;
- optional external impact references;
- future-safe boundary for Principia artifacts.

### E. Complete vertical-slice readiness — implementation in review

- complete English delayed-feedback manifest;
- complete Indonesian translation overlay;
- deterministic review backlog generation;
- reviewer-track and priority grouping;
- CI artifacts for coverage and backlog reports;
- no lifecycle promotion.

## Future Principia & Atlas boundary

Atlas is being prepared to serve as the knowledge and governance layer of a future **Principia & Atlas** product without becoming dependent on the Principia repository.

- Atlas owns canonical knowledge identity, evidence, provenance, revision, review, lifecycle, and staleness.
- Principia will own causal explanation, pedagogy, pathways, systems, investigations, and design experiences.
- A future Principia artifact may appear as an opaque external dependent of an Atlas entity.
- Atlas may report that an external artifact is affected by an Atlas revision, deprecation, or retraction.
- Atlas does not validate or inherit Principia's pedagogical or release status.
- Principia does not inherit Atlas review status automatically.
- No live Principia dependency is declared during Phase 1.

This is compatibility preparation, not repository merger or product UI work.

## Phase 1 exit gate

Phase 1 is complete only when:

- `atlas-review/0.1`, `atlas-promotion/0.1`, coverage semantics, and backlog semantics are explicit;
- review records, coverage manifests, and generated plans validate deterministically;
- promotion cannot occur from machine or AI review alone where human authority is required;
- review coverage, blockers, and human-review work can be generated without reading validator code;
- contradiction, contested, deprecation, retraction, stale-review, and dependency-impact fixtures pass;
- at least one complete vertical slice has sufficient accountable exact-revision review coverage for its intended lifecycle state;
- translated lifecycle status remains independently justified;
- remaining review gaps are visible and do not masquerade as passes;
- no critical or major contract defect remains;
- a Phase 1 completion report recommends or rejects entry to Phase 2.

## Current restrictions

Still frozen:

- product UI expansion;
- retrieval and ranking architecture;
- synchronization and plugins;
- additional implementation languages;
- autonomous or authoritative AI synthesis;
- direct Principia integration or repository merger;
- promotion of the experimental `.atlas`, SQL, C++, Rust, or TypeScript structures as the final runtime.

Allowed:

- review-contract, promotion, coverage, provenance, backlog, and validator work;
- reviewer packets, submission templates, and reports;
- source and literature challenge scans;
- accountable domain, methodological, ethical, legal-context, editorial, and translation review records;
- fixture-driven corrections to accepted content or foundation decisions;
- compatibility boundaries that do not create a live cross-repository dependency;
- prototype regression maintenance.

## Immediate next actions

1. verify complete-slice manifests, backlog generation, and CI on Python 3.11 and 3.13;
2. merge the readiness implementation only after all repository checks are green;
3. use generated backlogs to obtain real accountable human reviews;
4. record submissions against exact revisions and regenerate coverage;
5. resolve or preserve every major finding honestly;
6. determine whether the English slice can reach `reviewed` while the translation overlay remains independently blocked;
7. produce a Phase 1 completion report before entering Phase 2.

**Phase 1 is active. The goal is a trustworthy, reviewable knowledge authority that Principia can later depend on without inheriting false certainty.**
