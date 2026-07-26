# Atlas Project State

## Current status

**Phase 1 — English Reference Corpus and Accountable Vertical-Slice Review (active)**

Accepted history:

- Phase 0 foundation — PR #3, commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- Phase 1 review and promotion gate — PR #4, commit `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency reporting — PR #5, commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- complete delayed-feedback readiness and backlog — PR #6, commit `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only authored and review corpus — PR #7, commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations — PR #8, commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- accountable-human handoff bundles — PR #9, commit `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`.

All machine-authorized structural and fully specified reproducibility work for the complete English delayed-feedback slice is complete. The remaining 25 gate tasks require accountable humans.

Current work validates returned human-review submissions against one active handoff task and the exact canonical snapshot supplied to the reviewer. Intake validation does not accept the review, resolve findings, permit promotion, assign authority, or change lifecycle status.

All canonical reference entities remain `draft`. No validator pass, machine attestation, AI-assisted record, coverage report, backlog, handoff bundle, submission envelope, extracted record, or synthetic fixture grants scientific, methodological, editorial, source, legal, ethical, or human authority.

## Authority order

1. `PROJECT_STATE.md`
2. accepted foundation documents in `docs/foundation/`
3. accepted ADRs
4. canonical authored content and committed exact-revision review records
5. generated reports, manifests, backlogs, handoff bundles, and intake artifacts
6. experimental prototype code

A tool may establish bounded conformance, arithmetic reproduction, task-to-snapshot integrity, or submission consistency. It cannot establish scientific truth, domain adequacy, model applicability, source interpretation, legal correctness, ethical acceptability, editorial quality, reviewer identity, reviewer qualification, or lifecycle authority by itself.

## Language policy

The active authored corpus and review program are English-only.

Language-neutral translation identity, source-revision lineage, independent lifecycle, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent a supported authored language or active review queue.

## Accepted foundation and governance contracts

### Phase 0

- `atlas-content/0.1` authored Markdown contract;
- canonical source, evidence, claim, concept, relation, model, question, synthesis, and revision semantics;
- claim-level provenance, scope, uncertainty, and normative-value boundaries;
- controlled relation vocabulary and compatibility;
- mechanical and semantic migration rules;
- alias, rename, collision, federation, and synthetic translation fixtures;
- deterministic validation and closure records.

### Phase 1

- `atlas-review/0.1` — exact-revision review records;
- `atlas-promotion/0.1` — deterministic lifecycle decisions;
- `atlas-review-coverage/0.1` — packet and complete-slice coverage;
- `atlas-review-backlog/0.1` — deterministic missing-review tasks;
- deterministic machine-attestation generation and drift checks;
- `atlas-review-handoff/0.1` — self-contained accountable-human reviewer bundles;
- `atlas-review-submission/0.1` — exact-task and exact-snapshot return envelope.

## Active review scope

### Complete English delayed-feedback vertical slice

`content/reviews/coverage/feedback-complete-vertical-slice.json` includes exact revision 1 of:

- the research question;
- authoritative and generated sources;
- reproducible evidence;
- formal and methodological claims;
- feedback and oscillation concepts;
- the delayed-correction recurrence model;
- the synthesis.

The manifest uses `coverage_requirement: all`. Every listed entity must obtain acceptable exact-revision coverage before the slice can become coverage-complete.

The formal recurrence result and the model-to-world inference boundary are both load-bearing. A future Principia explanation, investigation, simulation, or system dossier must not consume the formal result while hiding its limitation.

## Completed machine authority

The repository commits and deterministically verifies:

- 10 structural machine records, one for each complete-slice entity;
- 3 fully specified recurrence-reproducibility machine records.

Every machine record:

- targets an exact entity revision;
- uses reviewer kind `machine`;
- uses independence `not-applicable`;
- sets `accountable: false`;
- sets `permits_promotion: false`;
- remains bounded to its declared procedure.

## Remaining human-required backlog

The complete slice remains `blocked` with:

- 25 gate tasks;
- 0 automation-eligible tasks;
- 25 human-required tasks;
- 0 advisory-only tasks.

Qualification tracks:

| Track | Tasks | Minimum authority |
|---|---:|---|
| Domain authority | 7 | independent control-systems, dynamical-systems, or difference-equation expertise |
| Editorial and scope | 7 | accountable human technical editing and scope review |
| Methods and inference | 5 | independent mathematical-modeling or scientific-inference expertise |
| Source and provenance | 5 | accountable source, locator, and provenance review |
| Independent reproducibility | 1 | independent human reproduction of the generated source procedure |

These are exact entity/review-type tasks, not a required number of distinct people.

## Accountable-human handoff baseline

`tools/foundation-validator/phase1_human_review_handoff.py` generates a self-contained package containing:

- all 25 tasks exactly once;
- five JSON and Markdown qualification-track bundles;
- byte-for-byte snapshots of all ten canonical Markdown entities;
- original repository paths and SHA-256 digests;
- existing non-satisfying records, blockers, and dependents;
- task-specific acceptance criteria and submission worksheets;
- `reviewer_assignment: null`.

The existing major finding `finding:feedback:periodicity-proof` remains visible in the domain packet.

The handoff assigns no reviewer, performs no review, resolves no finding, permits no promotion, and changes no lifecycle state.

## Review submission intake

`tools/foundation-validator/phase1_review_intake.py` validates `atlas-review-submission/0.1` envelopes against a generated handoff.

A submission must bind:

- the active coverage ID;
- one active human-required task ID;
- the exact entity ID and revision;
- the exact handoff snapshot SHA-256;
- `reviewed_exact_snapshot: true`;
- submission date;
- explicit AI-assistance disclosure;
- one proposed `atlas-review/0.1` record.

Intake validation checks:

- task and coverage identity;
- exact snapshot identity and digest;
- exact review entity, revision, and review type;
- human reviewer kind and accountability;
- required independence;
- qualification and conflicts;
- review-record contract validity;
- AI-assistance disclosure;
- completion and submission date order.

A successful intake may extract a normalized review record with `metadata.intake` lineage. Extraction writes only to an explicitly requested output path and never modifies `content/reviews/records/` automatically.

Maintainers must still inspect the real reviewer, commit the record through normal review, regenerate coverage, and preserve any unresolved finding.

## Phase 1 work packages

### Implemented baseline

- review and promotion contracts;
- lifecycle and dishonest-authority fixtures;
- coverage and dependency reporting;
- deterministic backlog generation;
- complete English delayed-feedback readiness scope;
- bounded machine attestations;
- accountable-human handoff bundles.

### Review intake — implementation in review

- `atlas-review-submission/0.1` envelope;
- active-task and exact-snapshot binding;
- human accountability and independence checks;
- AI-assistance disclosure;
- normalized intake lineage extraction;
- proof that intake does not write to the canonical review directory;
- synthetic CI fixtures only, with no real review authority.

### Accountable human review execution — external next work

- identify real qualified reviewers outside the generator;
- provide the relevant exact-snapshot track bundles;
- receive and validate submission envelopes;
- inspect and commit acceptable exact-revision review records;
- preserve disagreements and findings;
- resolve content defects through new canonical revisions;
- regenerate coverage, backlog, and handoff;
- keep the slice blocked until every required review class passes.

## Future Principia & Atlas boundary

Atlas is being prepared to serve as the knowledge and governance layer of a future **Principia & Atlas** product without becoming dependent on the Principia repository.

- Atlas owns canonical knowledge identity, evidence, provenance, revision, review, lifecycle, and staleness.
- Principia will own causal explanation, pedagogy, pathways, systems, investigations, simulations, and design experiences.
- Atlas may report that a Principia artifact is affected by revision, deprecation, or retraction.
- Atlas does not inherit Principia pedagogical status.
- Principia does not inherit Atlas review status automatically.
- No live Principia dependency is declared during Phase 1.

Handoff and intake validate Atlas review provenance only. They cannot approve a future Principia explanation, lesson, simulation, investigation, or system dossier.

## Phase 1 exit gate

Phase 1 is complete only when:

- review, promotion, coverage, backlog, attestation, handoff, and intake semantics are explicit and executable;
- review records, manifests, committed attestations, generated bundles, and return envelopes validate deterministically;
- promotion cannot occur from machine or AI review alone where human authority is required;
- every remaining task is tied to an exact entity revision, exact snapshot, and accountable authority requirement;
- contradiction, contested, deprecation, retraction, stale-review, and dependency-impact fixtures pass;
- the complete English delayed-feedback slice has sufficient accountable exact-revision review coverage;
- remaining review gaps remain visible and do not masquerade as passes;
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
- automatic reviewer assignment;
- automatic commitment or acceptance of extracted review records;
- direct Principia integration or repository merger;
- promotion of experimental `.atlas`, SQL, C++, Rust, or TypeScript structures as the final runtime.

Allowed:

- review-contract, promotion, coverage, provenance, backlog, attestation, handoff, intake, and validator work;
- English reviewer packets, submission templates, and reports;
- source and literature challenge scans;
- accountable review records supplied by real reviewers;
- synthetic CI submissions that clearly grant no real authority;
- synthetic translation fixtures testing language-neutral contracts only;
- fixture-driven corrections to accepted foundation decisions;
- compatibility boundaries that do not create a live cross-repository dependency;
- prototype regression maintenance.

## Immediate next actions

1. verify synthetic intake validation and extraction on Python 3.11 and 3.13;
2. prove exact-snapshot lineage is preserved and no automatic repository write occurs;
3. publish the intake template and documentation;
4. identify real qualified reviewers outside Atlas automation;
5. receive and inspect exact-snapshot submissions;
6. commit only acceptable exact-revision records through normal review;
7. resolve or preserve every major finding honestly;
8. regenerate coverage and determine whether the English slice can reach `reviewed`;
9. produce a Phase 1 completion report before entering Phase 2.

**Phase 1 is active. The goal is a trustworthy English knowledge authority that Principia can later depend on without inheriting false certainty.**
