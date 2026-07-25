# Atlas Project State

## Current status

**Phase 1 — Reference Corpus, Review Gate, and Coverage Reporting (active)**

Phase 0 was accepted through merged PR #3 at commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`. The versioned `atlas-content/0.1` foundation, canonical corpus, multilingual lineage, migration fixtures, identity rules, and deterministic conformance validator are the accepted baseline.

The initial Phase 1 review and promotion infrastructure was merged through PR #4 at commit `09488b76c43fdbe46f94fcb14a27637472adfa38`. It established `atlas-review/0.1`, `atlas-promotion/0.1`, revision-specific review records, lifecycle fixtures, reviewer packets, and CI enforcement.

Current Phase 1 work adds deterministic packet and slice coverage reporting, missing-review visibility, dependency impact, and a reviewer submission workflow. It does not begin product feature development.

All reference entities remain `draft`. No AI-assisted record, validator pass, packet, or coverage report grants scientific, methodological, legal, ethical, or translation authority.

## Authority order

1. `PROJECT_STATE.md`
2. accepted foundation documents in `docs/foundation/`
3. accepted ADRs
4. canonical authored content and revision-specific review records
5. generated reports and indexes
6. experimental prototype code

A validator can establish conformance. It cannot establish scientific truth, legal correctness, ethical acceptability, or translation equivalence.

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

Phase 0 may be reopened only when a representative review or migration exposes an actual ontology or contract failure.

## Phase 1 implemented baseline

- `atlas-review/0.1` exact-revision review records;
- `atlas-promotion/0.1` deterministic lifecycle decisions;
- accountable reviewer, qualification, independence, and conflict fields;
- critical and major finding blockers;
- review horizons and expiration behavior;
- AI and machine authority boundaries;
- contested, deprecated, and retracted transition fixtures;
- reviewer-ready packets for catalase, delayed feedback, recommender governance, and Indonesian translation;
- AI-assisted internal challenge records that explicitly remain non-authoritative;
- Python 3.11 and 3.13 CI coverage.

## Current coverage and provenance work

The current branch adds `atlas-review-coverage/0.1` and a deterministic reporter that shows:

- exact entities and revisions in a bounded packet or slice;
- required, satisfied, and missing review types;
- review records found for each exact revision;
- authority, outcome, horizon, staleness, and translation blockers;
- internal dependents;
- optional opaque external dependents;
- whether the bounded scope is coverage-complete or blocked.

The work also corrects the review requirement for methodological claims. A methodological claim now requires structural, editorial, source, domain, and methodological review.

Four current packet manifests intentionally report `blocked`:

1. catalase assay methodology;
2. delayed-feedback domain review;
3. recommender legal context;
4. English–Indonesian feedback translation.

They remain blocked because accountable human review coverage is incomplete. These packet manifests do not claim full vertical-slice closure.

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

### C. Reviewer packets — implemented baseline

Bounded packets exist for:

1. catalase and assay methodology;
2. delayed-feedback and control-systems terminology;
3. recommender evidence, DSA context, and normative governance;
4. Indonesian translation equivalence for the feedback slice.

A submission guide and JSON example provide a code-independent path for accountable reviewers.

### D. Coverage and dependency reports — implementation in review

- packet and future vertical-slice coverage manifests;
- `all` and `load-bearing` coverage policies;
- deterministic missing-review reports;
- internal reverse-dependency impact;
- optional external dependency references;
- CI proof that current known gaps remain honestly blocked.

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

- `atlas-review/0.1`, `atlas-promotion/0.1`, and coverage semantics are explicit;
- review records and coverage manifests validate deterministically;
- promotion cannot occur from machine or AI review alone where human authority is required;
- review coverage and blockers can be generated without reading validator code;
- contradiction, contested, deprecation, retraction, stale-review, and dependency-impact fixtures pass;
- at least one complete vertical slice has revision-specific review coverage sufficient for its intended lifecycle state;
- remaining independent-review gaps are visible and do not masquerade as passes;
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

- review-contract, promotion, coverage, provenance, and validator work;
- reviewer packets, submission templates, and reports;
- source and literature challenge scans;
- accountable domain, methodological, ethical, legal-context, and translation review records;
- fixture-driven corrections to accepted content or foundation decisions;
- compatibility boundaries that do not create a live cross-repository dependency;
- prototype regression maintenance.

## Immediate next actions

1. review and merge the coverage and provenance implementation only after CI is green;
2. obtain real accountable human reviews for the four bounded packets;
3. record submissions against exact canonical revisions and regenerate reports;
4. expand one packet into a complete vertical-slice coverage manifest;
5. resolve or preserve every major finding honestly;
6. produce a Phase 1 completion report before entering Phase 2.

**Phase 1 is active. The goal is trustworthy review, visible coverage, and controlled promotion—not more product surface area.**
