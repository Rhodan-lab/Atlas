# Atlas Project State

## Current status

**Phase 1 — English Reference Corpus and Accountable Vertical-Slice Review (active)**

Accepted history:

- Phase 0 foundation — PR #3, commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- review and promotion gate — PR #4, commit `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency reporting — PR #5, commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- complete delayed-feedback readiness and backlog — PR #6, commit `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only authored and review corpus — PR #7, commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations — PR #8, commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- accountable-human handoff bundles — PR #9, commit `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`;
- exact-snapshot review intake — PR #10, commit `9809bcb523954770e87c78154cdb124f37aadf46`.

All machine-authorized structural and fully specified reproducibility work for the complete English delayed-feedback slice is complete. The remaining 25 gate tasks require accountable humans.

Current work adds an explicit maintainer admission decision between validated intake and canonical review history. Admission does not approve knowledge, resolve findings, permit promotion, or write automatically to `content/reviews/records/`.

All canonical reference entities remain `draft`. No validator pass, machine attestation, handoff bundle, submission envelope, admission receipt, prepared record, or synthetic fixture grants scientific, methodological, editorial, source, legal, ethical, or lifecycle authority.

## Authority order

1. `PROJECT_STATE.md`
2. accepted foundation documents in `docs/foundation/`
3. accepted ADRs
4. canonical authored content and committed exact-revision review records
5. generated reports, manifests, backlogs, handoff bundles, intake artifacts, and admission receipts
6. experimental prototype code

A tool may establish bounded conformance, arithmetic reproduction, task-to-snapshot integrity, submission consistency, or declared admission consistency. It cannot establish scientific truth, source interpretation, model applicability, reviewer identity, reviewer qualification, reviewer independence, or lifecycle authority by itself.

## Language policy

The active authored corpus and review program are English-only.

Language-neutral translation identity, source-revision lineage, independent lifecycle, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent a supported authored language or active review queue.

## Accepted contracts

### Phase 0

- `atlas-content/0.1` authored Markdown contract;
- source, evidence, claim, concept, relation, model, question, synthesis, and revision semantics;
- claim-level provenance, scope, uncertainty, and explicit normative values;
- controlled relation vocabulary and compatibility;
- migration, alias, collision, federation, and synthetic translation fixtures;
- deterministic validation and closure records.

### Phase 1

- `atlas-review/0.1` — exact-revision review records;
- `atlas-promotion/0.1` — deterministic lifecycle decisions;
- `atlas-review-coverage/0.1` — packet and complete-slice coverage;
- `atlas-review-backlog/0.1` — deterministic missing-review tasks;
- deterministic machine-attestation generation and drift checks;
- `atlas-review-handoff/0.1` — self-contained accountable-human reviewer bundles;
- `atlas-review-submission/0.1` — exact-task and exact-snapshot return envelope;
- `atlas-review-admission/0.1` — explicit human-maintainer decision about entry into review history.

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

- 10 structural machine records;
- 3 fully specified recurrence-reproducibility machine records.

Every machine record targets one exact revision, uses reviewer kind `machine`, sets `accountable: false`, sets `permits_promotion: false`, and remains bounded to its declared procedure.

## Remaining human-required backlog

The complete slice remains `blocked` with:

- 25 gate tasks;
- 0 automation-eligible tasks;
- 25 human-required tasks;
- 0 advisory-only tasks.

| Track | Tasks | Minimum authority |
|---|---:|---|
| Domain authority | 7 | independent control-systems, dynamical-systems, or difference-equation expertise |
| Editorial and scope | 7 | accountable human technical editing and scope review |
| Methods and inference | 5 | independent mathematical-modeling or scientific-inference expertise |
| Source and provenance | 5 | accountable source, locator, and provenance review |
| Independent reproducibility | 1 | independent human reproduction of the generated source procedure |

These are exact entity/review-type tasks, not a required number of distinct people.

## Accountable-human handoff

`phase1_human_review_handoff.py` generates:

- all 25 tasks exactly once;
- five qualification-track bundles;
- byte-for-byte snapshots of all ten canonical entities;
- repository paths and SHA-256 digests;
- existing blockers and dependency impact;
- task-specific acceptance criteria;
- `reviewer_assignment: null`.

The existing major finding `finding:feedback:periodicity-proof` remains visible. The handoff performs no review and changes no status.

## Exact-snapshot review intake

`phase1_review_intake.py` validates `atlas-review-submission/0.1` envelopes against the active handoff.

It checks:

- active coverage and task identity;
- exact entity ID, revision, and snapshot SHA-256;
- exact review type;
- human reviewer kind and accountability;
- task-specific independence;
- qualification and conflicts declarations;
- review-record contract validity;
- AI-assistance disclosure;
- completion and submission date order.

A successful intake may extract a normalized proposed record with `metadata.intake` lineage only to an explicit output path. Intake never writes to the canonical review directory.

## Explicit review admission

`phase1_review_admission.py` validates `atlas-review-admission/0.1` decisions after intake.

Admission decisions:

- `accept` — prepare the proposed record for normal repository review;
- `request-changes` — preserve a receipt, but prepare no record;
- `reject` — preserve a receipt, but prepare no record.

An `accept` decision requires a real accountable human decider to declare completion of external checks for reviewer identity, qualification, independence, and conflicts.

The validator can confirm that these declarations are present. It cannot perform the real-world verification.

Admission may preserve a review whose outcome is `changes-required` or that contains major findings. Accepting the **record into review history** is not the same as accepting the **reviewed knowledge**.

The `prepare` command:

- preserves `metadata.intake`;
- adds `metadata.admission`;
- rejects duplicate canonical review IDs;
- writes only to an explicit output path;
- never resolves or removes findings;
- never writes automatically to `content/reviews/records/`;
- never changes canonical lifecycle status.

Synthetic admissions set `test_fixture: true`; their prepared records are forced to `permits_promotion: false`.

## Phase 1 work packages

### Implemented baseline

- review and promotion contracts;
- lifecycle and dishonest-authority fixtures;
- coverage and dependency reporting;
- deterministic backlog generation;
- complete English delayed-feedback readiness scope;
- bounded machine attestations;
- accountable-human handoff bundles;
- exact-snapshot review intake.

### Explicit review admission — implementation in review

- `atlas-review-admission/0.1` decisions and receipts;
- accountable human decider declaration;
- external identity, qualification, independence, and conflict check declarations;
- duplicate review-ID rejection;
- preserved intake and admission lineage;
- synthetic fixture promotion suppression;
- proof that no canonical review file is written automatically.

### Accountable human review execution — external next work

- identify real qualified reviewers;
- provide exact-snapshot track bundles;
- receive exact-snapshot submission envelopes;
- perform real external verification;
- issue accountable admission decisions;
- commit acceptable review records through normal pull requests;
- preserve disagreements and findings;
- create new canonical revisions for content defects;
- regenerate coverage, backlog, and handoff;
- keep the slice blocked until every required review class passes.

## Future Principia & Atlas boundary

Atlas is being prepared as the knowledge and governance layer of a future **Principia & Atlas** product without becoming dependent on the Principia repository.

- Atlas owns canonical knowledge identity, evidence, provenance, revision, review, lifecycle, and staleness.
- Principia will own causal explanation, pedagogy, pathways, systems, investigations, simulations, and design experiences.
- Atlas may report that a Principia artifact is affected by revision, deprecation, or retraction.
- Atlas does not inherit Principia pedagogical status.
- Principia does not inherit Atlas review status automatically.
- No live Principia dependency is declared during Phase 1.

Handoff, intake, and admission govern Atlas review provenance only. They cannot approve a Principia explanation, lesson, simulation, investigation, system dossier, or release.

## Phase 1 exit gate

Phase 1 is complete only when:

- review, promotion, coverage, backlog, attestation, handoff, intake, and admission semantics are executable;
- committed and generated artifacts validate deterministically;
- promotion cannot occur from machine or AI review alone where human authority is required;
- every remaining task is tied to an exact revision, exact snapshot, and accountable authority requirement;
- contradiction, contested, deprecation, retraction, stale-review, and dependency-impact fixtures pass;
- the complete English delayed-feedback slice has sufficient accountable exact-revision review coverage;
- remaining gaps remain visible and do not masquerade as passes;
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
- automatic reviewer identity or qualification claims;
- automatic commitment or acceptance of prepared review records;
- direct Principia integration or repository merger;
- promotion of experimental runtime structures as canonical.

Allowed:

- review-contract, promotion, coverage, provenance, backlog, attestation, handoff, intake, admission, and validator work;
- English reviewer packets, templates, receipts, and reports;
- accountable review records supplied by real reviewers;
- synthetic CI fixtures that clearly grant no real authority;
- fixture-driven corrections to accepted foundation decisions;
- compatibility boundaries without a live cross-repository dependency;
- prototype regression maintenance.

## Immediate next actions

1. verify admission tests on Python 3.11 and 3.13;
2. prove synthetic admission preserves intake and admission lineage;
3. prove fixture records cannot permit promotion;
4. prove no automatic canonical review-directory write occurs;
5. identify real qualified reviewers outside Atlas automation;
6. receive, inspect, and externally verify real submissions;
7. commit only acceptable records through normal pull-request review;
8. resolve or preserve every major finding honestly;
9. regenerate coverage and determine whether the English slice can reach `reviewed`;
10. produce a Phase 1 completion report before Phase 2.

**Phase 1 is active. The goal is a trustworthy English knowledge authority that Principia can later depend on without inheriting false certainty.**