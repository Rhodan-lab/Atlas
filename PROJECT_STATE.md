# Atlas Project State

## Current status

**Phase 1 — Reference Corpus and Review Gate (active)**

Phase 0 was accepted through merged PR #3 at commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`. The versioned `atlas-content/0.1` foundation, canonical corpus, multilingual lineage, migration fixtures, identity rules, and deterministic conformance validator are now the accepted baseline.

Phase 1 does not begin product feature development. It proves that exact canonical revisions can be reviewed, challenged, promoted, contested, deprecated, or retracted without losing provenance or confusing machine checks with human authority.

All reference entities remain `draft` until their required review records pass the Phase 1 promotion gate.

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

## Phase 1 objectives

1. Define `atlas-review/0.1` for revision-specific review records.
2. Define required review types and acceptable reviewer authority by entity and claim kind.
3. Make unresolved critical or major findings block promotion deterministically.
4. Make AI-only, machine-only, stale, conflicted, or wrong-revision reviews insufficient for authority.
5. Generate reviewer-ready packets without requiring implementation knowledge.
6. Exercise contradiction, contested status, deprecation, retraction, and review staleness.
7. Record internal and AI-assisted findings honestly while preserving independent-review requirements.
8. Harden the validator only where fixtures demonstrate a real gap.

## Phase 1 work packages

### A. Review contract

- review identity and exact target revision;
- review type, reviewer role, independence, and conflicts;
- outcome and promotion effect;
- structured findings with severity and resolution state;
- reviewed-at date and review horizon;
- evidence or rationale for each decision.

### B. Promotion gate

- calculate required review types;
- reject wrong-revision records;
- reject unresolved critical or major findings;
- reject authority derived only from AI or machine review;
- reject stale translations and expired time-sensitive reviews;
- preserve disagreement and conflicts;
- require explicit transition records for reviewed, contested, deprecated, and retracted states.

### C. Reviewer packets

Create bounded packets for:

1. catalase and assay methodology;
2. delayed-feedback and control-systems terminology;
3. recommender evidence, DSA context, and normative governance;
4. Indonesian translation equivalence for the feedback slice.

### D. Review reports

Generate deterministic coverage reports that show:

- exact entities and revisions in scope;
- completed and missing review types;
- open findings by severity;
- conflicts and independence;
- stale or expired records;
- whether promotion is permitted and why.

## Phase 1 exit gate

Phase 1 is complete only when:

- `atlas-review/0.1` and its migration policy are explicit;
- review records validate deterministically;
- promotion cannot occur from machine or AI review alone where human authority is required;
- review coverage and blockers can be generated without reading validator code;
- contradiction, contested, deprecation, retraction, and stale-review fixtures pass;
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
- promotion of the experimental `.atlas`, SQL, C++, Rust, or TypeScript structures as the final runtime.

Allowed:

- review-contract and validator work;
- reviewer packets and reports;
- source and literature challenge scans;
- domain, methodological, ethical, legal-context, and translation review records;
- fixture-driven corrections to accepted content or foundation decisions;
- prototype regression maintenance.

## Immediate next actions

1. implement the Phase 1 review gate and tests;
2. create review records that explicitly remain non-authoritative;
3. create the three domain review packets and translation packet;
4. run CI on Python 3.11 and 3.13;
5. record all findings before considering any lifecycle promotion.

**Phase 1 is active. The goal is trustworthy review and controlled promotion, not more product surface area.**
