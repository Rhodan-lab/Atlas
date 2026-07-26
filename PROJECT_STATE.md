# Atlas Project State

## Current status

**Phase 1 — English Reference Corpus and Accountable Vertical-Slice Review (active)**

Phase 0 was accepted through merged PR #3 at commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`. It established `atlas-content/0.1`, canonical entity semantics, provenance, revision identity, migrations, federation fixtures, and deterministic conformance validation.

The initial Phase 1 review and promotion infrastructure was merged through PR #4 at commit `09488b76c43fdbe46f94fcb14a27637472adfa38`.

Coverage and dependency reporting was merged through PR #5 at commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`.

Complete delayed-feedback vertical-slice readiness and deterministic backlog generation were merged through PR #6 at commit `786bdaf4141be032554fe1b73439dfacb67c806d`.

The English-only authored and review corpus policy was merged through PR #7 at commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`.

Deterministic machine attestations were merged through PR #8 at commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`. All machine-authorized structural and fully specified reproducibility work for the complete English delayed-feedback slice is complete.

Current work generates a self-contained accountable-human review handoff from the live remaining backlog. The handoff assigns no reviewer, performs no review, resolves no finding, permits no promotion, and changes no lifecycle state.

All canonical reference entities remain `draft`. No validator pass, machine attestation, AI-assisted record, coverage report, readiness manifest, backlog, reviewer bundle, or synthetic fixture grants scientific, methodological, editorial, source, legal, ethical, or human authority.

## Authority order

1. `PROJECT_STATE.md`
2. accepted foundation documents in `docs/foundation/`
3. accepted ADRs
4. canonical authored content and exact-revision review records
5. generated reports, indexes, coverage manifests, backlogs, and handoff bundles
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

### Machine attestations

- deterministic generation and drift checking;
- 10 structural exact-revision records;
- 3 fully specified recurrence-reproducibility records;
- every record uses reviewer kind `machine`;
- every record sets `accountable: false` and `permits_promotion: false`;
- no authority outside the declared deterministic procedure.

## Active review scope

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

## Current human-required backlog

After the 13 machine attestations are counted, the complete delayed-feedback slice remains `blocked` with:

- 25 gate tasks;
- 0 automation-eligible tasks;
- 25 human-required tasks;
- 0 advisory-only tasks.

The 25 tasks are grouped into five qualification tracks:

| Track | Tasks | Required authority |
|---|---:|---|
| Domain authority | 7 | independent control-systems, dynamical-systems, or difference-equation expertise |
| Editorial and scope | 7 | accountable human technical editing and scope review |
| Methods and inference | 5 | independent mathematical-modeling or scientific-inference expertise |
| Source and provenance | 5 | accountable source, locator, and provenance review |
| Independent reproducibility | 1 | independent human reproduction of the generated source procedure |

These are exact entity/review-type tasks, not a required number of distinct people. One qualified reviewer may cover several tasks only when each exact-revision judgment, qualification, independence state, conflict, finding, and promotion recommendation is recorded separately.

## Human review handoff

`tools/foundation-validator/phase1_human_review_handoff.py` generates `atlas-review-handoff/0.1` bundles from live coverage data.

The generated package contains:

- `handoff.json` with all 25 remaining human tasks;
- five JSON and Markdown qualification-track packets;
- byte-for-byte snapshots of all ten exact canonical Markdown entities;
- original repository paths and SHA-256 digests;
- existing non-satisfying records and blockers;
- internal and external dependency impact;
- acceptance criteria and submission worksheets;
- no reviewer assignment.

Generation fails when:

- automation-eligible tasks still remain;
- advisory tasks are mixed into the gate handoff;
- a task permits nonhuman authority;
- accountability is not required;
- an exact canonical entity revision cannot be found;
- a task appears more than once;
- an unsupported qualification track appears.

The existing major finding `finding:feedback:periodicity-proof` remains visible in the domain-authority packet. The handoff cannot hide or resolve it.

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

### C. Coverage, backlog, and dependency reporting — implemented baseline

- packet and complete-slice coverage manifests;
- deterministic missing-review reports and tasks;
- internal reverse-dependency impact;
- optional external impact references;
- future-safe boundary for Principia artifacts.

### D. Complete English vertical-slice readiness — implemented baseline

- complete delayed-feedback manifest;
- reviewer-track and priority grouping;
- automation-versus-human classification;
- CI artifacts for coverage and backlog reports;
- no lifecycle promotion.

### E. Machine attestations — implemented baseline

- deterministic generator and exact committed outputs;
- ten structural records;
- three fully specified reproducibility records;
- generator drift detection in CI;
- post-attestation backlog assertion;
- no human authority or lifecycle promotion.

### F. Accountable-human review handoff — implementation in review

- `atlas-review-handoff/0.1` generated package;
- exact canonical snapshots and SHA-256 integrity;
- five bounded qualification-track bundles;
- proof that all 25 tasks appear exactly once;
- preservation of existing blockers and dependents;
- no reviewer assignment, review decision, finding resolution, or promotion.

### G. Accountable human review execution — external next work

- identify real qualified reviewers;
- disclose qualifications, independence, and conflicts honestly;
- obtain exact-revision review records;
- preserve disagreements and findings;
- resolve content defects through new canonical revisions;
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

The handoff reviews Atlas knowledge only. It cannot approve a future Principia explanation, lesson, simulation, investigation, or system dossier.

## Phase 1 exit gate

Phase 1 is complete only when:

- review, promotion, coverage, backlog, attestation, and handoff semantics are explicit and executable;
- review records, manifests, committed attestations, generated plans, and handoff bundles validate deterministically;
- promotion cannot occur from machine or AI review alone where human authority is required;
- every remaining review task is tied to an exact entity revision and accountable authority requirement;
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
- automatic reviewer assignment;
- direct Principia integration or repository merger;
- promotion of experimental `.atlas`, SQL, C++, Rust, or TypeScript structures as the final runtime.

Allowed:

- review-contract, promotion, coverage, provenance, backlog, attestation, handoff, and validator work;
- English reviewer packets, submission templates, and reports;
- source and literature challenge scans;
- accountable domain, methodological, ethical, legal-context, source, and editorial review records supplied by real reviewers;
- synthetic translation fixtures testing language-neutral contracts only;
- fixture-driven corrections to accepted foundation decisions;
- compatibility boundaries that do not create a live cross-repository dependency;
- prototype regression maintenance.

## Immediate next actions

1. verify the generated handoff contains exactly 25 tasks in five tracks;
2. verify all ten canonical snapshots and SHA-256 digests;
3. publish the handoff package as a CI artifact;
4. identify real qualified reviewers outside the generator;
5. receive and validate exact-revision review records;
6. resolve or preserve every major finding honestly;
7. regenerate coverage and determine whether the English slice can reach `reviewed`;
8. produce a Phase 1 completion report before entering Phase 2.

**Phase 1 is active. The goal is a trustworthy English knowledge authority that Principia can later depend on without inheriting false certainty.**
