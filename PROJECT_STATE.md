# Atlas Project State

## Current status

**Phase 1 — English Reference Corpus and Accountable Vertical-Slice Review (active)**

Phase 0 was accepted through merged PR #3 at commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`. It established `atlas-content/0.1`, canonical entity semantics, provenance, revision identity, migrations, federation fixtures, and deterministic conformance validation.

The initial Phase 1 review and promotion infrastructure was merged through PR #4 at commit `09488b76c43fdbe46f94fcb14a27637472adfa38`.

Coverage and dependency reporting was merged through PR #5 at commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`.

Complete delayed-feedback vertical-slice readiness and deterministic backlog generation were merged through PR #6 at commit `786bdaf4141be032554fe1b73439dfacb67c806d`.

The English-only authored and review corpus policy was merged through PR #7 at commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`.

Current work records the complete set of machine-authorized structural and fully specified reproducibility attestations for the English delayed-feedback slice. Human-required review remains blocked and cannot be replaced by machine or AI-assisted work.

All canonical reference entities remain `draft`. No validator pass, machine attestation, AI-assisted record, coverage report, readiness manifest, generated backlog, or synthetic fixture grants scientific, methodological, editorial, source, legal, ethical, or human authority.

## Authority order

1. `PROJECT_STATE.md`
2. accepted foundation documents in `docs/foundation/`
3. accepted ADRs
4. canonical authored content and exact-revision review records
5. generated reports, indexes, coverage manifests, and backlogs
6. experimental prototype code

A validator can establish bounded conformance or a fully specified calculation. It cannot establish scientific truth, domain adequacy, model applicability, source interpretation, legal correctness, ethical acceptability, editorial quality, reviewer accountability, or translation equivalence.

## Language policy

The active authored corpus and review program are English-only.

Language-neutral translation identity, source-revision lineage, independent lifecycle, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent a supported authored language or active review queue.

## Phase 0 accepted baseline

- `atlas-content/0.1` authored Markdown contract;
- canonical source, evidence, claim, concept, relation, model, question, synthesis, and revision semantics;
- claim-level provenance, scope, uncertainty, and normative-value boundaries;
- controlled relation vocabulary and compatibility;
- language-neutral work identity and dormant translation-lineage semantics;
- mechanical and semantic migration rules;
- alias, rename, collision, and federation fixtures;
- deterministic validator and test suite;
- source-verification, structural-validation, review-register, and closure records.

Phase 0 may be reopened only when representative review, migration, lifecycle behavior, or a future multilingual reopening demonstrates a real contract failure.

## Phase 1 implemented baseline

### Review and lifecycle

- `atlas-review/0.1` exact-revision review records;
- `atlas-promotion/0.1` deterministic lifecycle decisions;
- reviewer kind, qualification, independence, accountability, and conflict fields;
- critical and major finding blockers;
- review horizons and expiration behavior;
- AI and machine authority boundaries;
- contested, deprecated, and retracted transition fixtures;
- reviewer-ready English packets and submission templates.

### Coverage and provenance

- `atlas-review-coverage/0.1` packet and complete-slice manifests;
- `all` and `load-bearing` coverage policies;
- exact-revision required, satisfied, and missing review classes;
- internal reverse-dependency impact;
- optional opaque external dependents;
- deterministic Markdown and JSON reports;
- CI proof that known gaps remain blocked rather than masquerading as passes.

### Review backlog

- `atlas-review-backlog/0.1` deterministic task generation;
- exact entity and revision targeting;
- gate-blocking versus advisory classification;
- automation-eligible versus human-required execution mode;
- reviewer qualification, independence, and accountability requirements;
- priority and dependency-impact reporting;
- no automatic assignment, review, finding resolution, or promotion.

## Active review scopes

### Bounded packets

1. catalase assay methodology;
2. delayed-feedback mathematics, terminology, and inference limits;
3. recommender evidence, legal context, and governance.

These packet scopes remain intentionally blocked pending accountable review.

### Complete English delayed-feedback vertical slice

`content/reviews/coverage/feedback-complete-vertical-slice.json` includes the exact revision-1:

- question;
- authoritative and generated sources;
- reproducible evidence;
- formal and methodological claims;
- concepts;
- model;
- synthesis.

The manifest uses `coverage_requirement: all`. Every listed entity must obtain acceptable exact-revision coverage before the slice can become coverage-complete.

The formal recurrence result and the model-to-world inference boundary are both load-bearing. A future Principia explanation, investigation, simulation, or system dossier must not consume the formal result while hiding its limitation.

## Machine attestations

`tools/foundation-validator/phase1_machine_attestations.py` deterministically generates and checks exactly 13 machine review records:

- 10 structural attestations, one for every entity in the complete slice;
- 3 reproducibility attestations for the formal claim, generated evidence, and executable model marked `fully-specified-reproducibility`.

Every machine attestation:

- targets one exact entity revision;
- uses reviewer kind `machine`;
- uses independence `not-applicable`;
- sets `accountable: false`;
- sets `permits_promotion: false`;
- has no authority beyond its declared bounded procedure;
- is checked against deterministic generator output in CI.

The recurrence check recalculates:

```text
x[t+1] = x[t] - x[t-1]
x[0] = 1
x[1] = 0
```

and confirms the eight-state sequence:

```text
1, 0, -1, -1, 0, 1, 1, 0
```

This establishes arithmetic reproducibility only. It does not establish periodicity terminology, stability classification, model adequacy, or behavior of any real system.

## Current English backlog

After the 13 machine attestations are counted, the complete delayed-feedback slice remains `blocked` with:

- 25 gate tasks;
- 0 automation-eligible tasks;
- 25 human-required tasks;
- 0 advisory-only tasks.

These are exact entity/review-type tasks, not a required number of distinct people. A qualified reviewer may cover several tasks only when each exact-revision judgment, qualification, independence state, conflict, finding, and promotion recommendation is recorded separately.

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
- reject machine or AI authority where accountable human judgment is required;
- reject stale synthetic translation fixtures and expired time-sensitive reviews;
- preserve disagreement and conflicts;
- require explicit transition records for reviewed, contested, deprecated, and retracted states.

### C. Reviewer packets and submission — implemented baseline

- bounded English packets for catalase, delayed feedback, and recommender governance;
- code-independent reviewer guide and JSON example;
- explicit prohibition on fabricated reviewers or hidden AI authority.

### D. Coverage and dependency reporting — implemented baseline

- packet and complete-slice coverage manifests;
- deterministic missing-review reports;
- internal reverse-dependency impact;
- optional external impact references;
- future-safe boundary for Principia artifacts.

### E. Complete English vertical-slice readiness — implemented baseline

- complete delayed-feedback manifest;
- deterministic review backlog generation;
- reviewer-track and priority grouping;
- automation-versus-human classification;
- CI artifacts for coverage and backlog reports;
- no lifecycle promotion.

### F. Machine attestations — implementation in review

- deterministic generator and exact committed outputs;
- ten structural records;
- three fully specified reproducibility records;
- generator drift detection in CI;
- post-attestation backlog assertion;
- no human authority or lifecycle promotion.

### G. Accountable human review — next work

- consolidate the 25 tasks into reviewer qualification tracks;
- prepare source/provenance, editorial/scope, domain, and methods/inference packets;
- obtain accountable exact-revision reviews;
- preserve conflicts, disagreements, and findings;
- resolve or retain every major finding honestly;
- regenerate coverage without weakening requirements;
- keep the slice blocked until every required review class passes.

## Future Principia & Atlas boundary

Atlas is being prepared to serve as the knowledge and governance layer of a future **Principia & Atlas** product without becoming dependent on the Principia repository.

- Atlas owns canonical knowledge identity, evidence, provenance, revision, review, lifecycle, and staleness.
- Principia will own causal explanation, pedagogy, pathways, systems, investigations, simulations, and design experiences.
- A future Principia artifact may appear as an opaque external dependent of an Atlas entity.
- Atlas may report that a Principia artifact is affected by revision, deprecation, or retraction.
- Atlas does not validate or inherit Principia's pedagogical or release status.
- Principia does not inherit Atlas review status automatically.
- No live Principia dependency is declared during Phase 1.

This is compatibility preparation, not repository merger or product UI work.

## Phase 1 exit gate

Phase 1 is complete only when:

- review, promotion, coverage, backlog, and attestation semantics are explicit and executable;
- review records, coverage manifests, committed attestations, and generated plans validate deterministically;
- promotion cannot occur from machine or AI review alone where human authority is required;
- review coverage, blockers, and reviewer work can be generated without reading validator code;
- contradiction, contested, deprecation, retraction, stale-review, and dependency-impact fixtures pass;
- the complete English delayed-feedback slice has sufficient accountable exact-revision review coverage for its intended lifecycle state;
- remaining review gaps are visible and do not masquerade as passes;
- no critical or major contract defect remains;
- a Phase 1 completion report recommends or rejects entry to Phase 2.

## Current restrictions

Still frozen:

- product UI expansion;
- retrieval and ranking architecture;
- synchronization and plugins;
- additional implementation languages;
- active translated corpus or language-specific review programs;
- autonomous or authoritative AI synthesis;
- direct Principia integration or repository merger;
- promotion of experimental `.atlas`, SQL, C++, Rust, or TypeScript structures as the final runtime.

Allowed:

- review-contract, promotion, coverage, provenance, backlog, attestation, and validator work;
- English reviewer packets, submission templates, and reports;
- source and literature challenge scans;
- accountable domain, methodological, ethical, legal-context, source, and editorial review records;
- synthetic translation fixtures testing language-neutral contracts only;
- fixture-driven corrections to accepted foundation decisions;
- compatibility boundaries that do not create a live cross-repository dependency;
- prototype regression maintenance.

## Immediate next actions

1. verify all 13 machine attestations against deterministic generator output;
2. confirm the remaining backlog is exactly 25 human-required gate tasks;
3. consolidate those tasks into bounded qualification tracks;
4. obtain accountable source, editorial, domain, and methodological reviews;
5. record findings against exact revisions;
6. resolve or preserve every major finding honestly;
7. regenerate coverage and determine whether the English slice can reach `reviewed`;
8. produce a Phase 1 completion report before entering Phase 2.

**Phase 1 is active. The goal is a trustworthy English knowledge authority that Principia can later depend on without inheriting false certainty.**
