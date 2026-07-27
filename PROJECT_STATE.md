# Atlas Project State

## Current status

**Phase 3 — Retrieval Evaluation (active)**

Phase 1 is complete under an explicitly **AI-reviewed** policy. Phase 2 is complete under deterministic kernel, compatibility, failure, scale, replay, replaceability, and rollback evidence. No human or expert verification is claimed, no live Principia dependency is active, and retrieval has advisory authority only.

## Accepted history

- Phase 0 foundation — PR #3, commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- review and promotion experiments — PR #4, commit `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency reporting — PR #5, commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- delayed-feedback readiness — PR #6, commit `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only authored corpus — PR #7, commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations — PR #8, commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- optional human handoff — PR #9, commit `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`;
- optional exact-snapshot intake — PR #10, commit `9809bcb523954770e87c78154cdb124f37aadf46`;
- optional admission boundary — PR #17, commit `01feffc696cc207305ef74c92d600f37aadf46`;
- Phase 1 AI review and Phase 2 activation — PR #18, commit `f90fa53f99ec9780451c9c50c57625759ba3b2b5`;
- first Phase 2 kernel and bridge receiver — PR #19, commit `8f1e473578d9086a73dae44f0b6001b246cfbc20`;
- Principia v0.2 importer implementation — PR #20, commit `1cc4aec6908a8703a7f505478329c633a23b4ef9`;
- accepted Principia importer governance baseline — PR #21, commit `9370cc746e9756e433ac3772d56d079c9803b144`;
- offline multi-artifact and lifecycle-protocol audit — PR #22, commit `1096a2176eb50e1921081bb3f46eeac8b13bd2c3`;
- accepted offline protocol governance record — PR #23, commit `ec666b59c4834c9a716006be9f9830d20178af34`;
- runtime hardening and failure semantics — PR #24, commit `7596e4fbae099304d64a5b2371c0fb4a2e55ffc4`;
- accepted runtime-hardening governance record — PR #25, commit `e66975a9a2e74f97fcd799ee80b47483a8390f0d`;
- scale, replay, and recovery validation — PR #26, commit `dd0c64447fb70727d260362f9877ffc6be560c3c`;
- accepted scale and replay governance record — PR #27, commit `fae9fc301a6d6d4bb91d8939c7d9a7fd6b48374b`;
- Phase 2 closure, replaceability, and retrieval-entry evidence — PR #28, commit `99b5c4db514da8ac1f6f30740fae66d42e242a74`.

## Language policy

The active authored and review corpus is English-only.

Language-neutral translation identity, revision lineage, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent an active translated corpus.

## Review policy

Atlas distinguishes review levels instead of presenting all review as equivalent.

### AI-reviewed

An AI-reviewed artifact has:

- an identified AI reviewer and model family;
- explicit non-human status;
- exact entity revisions;
- source-use checks;
- reproducibility or mathematical checks where applicable;
- recorded findings and corrections;
- explicit limitations;
- `human_verified: false`.

AI review is sufficient for current Atlas development and is not human verification.

### Human-verified

Human verification remains an optional stronger layer. Historical handoff, intake, admission, coverage, and promotion tools remain available, but they are not active Phase 3 gates.

Atlas must never convert an AI review into a human review or invent reviewer identity, credentials, independence, or accountability.

## Phase 1 completion

The delayed-feedback slice is accepted at `ai-reviewed` with:

```yaml
reviewer: GPT-5.6 Thinking
reviewer_kind: ai
human_verified: false
human_review_required: false
overall_outcome: pass
entity_count: 10
```

For `x[t+1] = x[t] - x[t-1]`, `x0 = 1`, and `x1 = 0`, the exact orbit is bounded and periodic with period 6. This is a formal result for one recurrence and initial history. It is not empirical evidence about a real system and not a general theorem that delay causes instability.

Active evidence:

- `content/reviews/ai/feedback-delayed-comprehensive.json`;
- `docs/phase-1/ai-review-report.md`;
- `tools/foundation-validator/phase1_ai_review.py`.

## Phase 2 completion

Phase 2 established the smallest dependable, deterministic, read-only kernel over canonical `atlas-content/0.1` Markdown.

Accepted capabilities:

- deterministic canonical-to-runtime compilation;
- strict admission of `atlas-kernel-runtime/0.1`;
- exact `ENTITY_ID@REVISION` lookup;
- typed relation traversal;
- synthesis-to-source provenance traversal;
- reverse-dependency and lifecycle-impact queries;
- deterministic failure behavior for malformed or incompatible content and runtime records;
- exact-revision Principia compatibility with `live: false`;
- atomic multi-artifact offline protocol validation;
- lifecycle escalation reporting without automatic action;
- representative and 1,026-entity scaled measurements;
- append-only receipt replay, idempotency, and deterministic recovery failures;
- storage-neutral portable snapshots;
- independent query-engine equivalence;
- deterministic migration and rollback rebuilding from canonical Markdown.

### Accepted closure evidence

```yaml
completion_contract: atlas-phase2-completion-report/0.1
portable_contract: atlas-kernel-portable-snapshot/0.1
mode: phase2-closure-candidate
state: accepted
accepted_pr: 28
tested_head: ad8bc4fa66eb894ca72b13f81be5e3c14bbd241a
accepted_merge_commit: 99b5c4db514da8ac1f6f30740fae66d42e242a74
entity_count: 34
query_equivalence_checks: 136
query_decision: equivalent
migration_decision: replaceable
retrieval_decision: proceed-bounded-retrieval-evaluation
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

The portable query engine independently reconstructs generated revision and reverse-dependency indexes and matches the standard repository for exact lookup, relation traversal, provenance traversal, and transitive impact for every canonical exact revision.

Generated runtimes, indexes, caches, and portable snapshots remain disposable. Canonical Markdown and pinned external fixtures remain authoritative. Rollback means deleting generated representations and rebuilding byte-identically from those authoritative sources.

## Authority order

1. `PROJECT_STATE.md`;
2. accepted foundation documents in `docs/foundation/`;
3. accepted phase completion reports and ADRs;
4. canonical authored content;
5. identified review records and reports, with review level visible;
6. generated manifests and operational artifacts;
7. experimental runtime, retrieval, adapter, and index code.

## Phase 3 objective

Phase 3 evaluates whether Atlas can retrieve relevant, versioned knowledge without weakening identity, provenance, review, lifecycle, or replaceability guarantees.

Phase 3 is an evaluation phase, not a production-search deployment phase.

Required outcomes:

1. a versioned query-and-judgment fixture set;
2. deterministic lexical retrieval baseline;
3. deterministic structured-field retrieval baseline;
4. explicit relevance metrics and deterministic tie handling;
5. exact entity ID and revision in every result;
6. visible provenance, review level, lifecycle, and staleness in every result;
7. safe failures for unavailable revisions and malformed indexes;
8. deletion and canonical rebuild tests for every generated index;
9. comparative evidence before any embedding or vector-store commitment;
10. a Phase 3 completion report recommending or rejecting broader retrieval work.

## Phase 3 entry boundary

Allowed:

- bounded lexical and structured retrieval experiments;
- versioned query and relevance fixtures;
- deterministic ranking and tie-breaking;
- advisory result sets with exact revisions and provenance;
- replaceable generated indexes;
- comparative embedding or vector experiments only after lexical and structured baselines exist.

Still frozen:

- production retrieval-quality claims;
- vector database commitment before comparative evaluation;
- unversioned or implicit `latest` lookup;
- retrieval-generated writes to canonical content;
- retrieval-driven lifecycle, review, promotion, or release mutation;
- live Principia synchronization;
- accepting external synthetic events as canonical lifecycle history;
- polished product UI;
- plugins and autonomous synchronization;
- active translated corpus;
- hidden or autonomous authority claims;
- automatic conversion of AI review into human verification.

## Principia & Atlas boundary

Atlas is the knowledge and governance layer of the future **Principia & Atlas** system.

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns causal explanation, pathways, investigations, simulations, system dossiers, failure analysis, design experiences, and its own publication readiness.
- Principia may reference exact Atlas revisions.
- Atlas may report dependency impact when upstream knowledge changes.
- Neither repository inherits the other repository's status automatically.
- The repositories remain separate and independently buildable.
- No live cross-repository dependency is activated by Phase 3 entry.

## Immediate next actions

1. define the Phase 3 query-and-judgment contract;
2. create a bounded fixture set spanning all three English reference slices;
3. implement a deterministic lexical baseline without external services;
4. implement a structured-field baseline over titles, types, claims, relations, and provenance;
5. define relevance metrics, tie rules, and exact-revision result contracts;
6. keep vector infrastructure, live synchronization, and automatic mutation frozen until comparative evidence supports a separate decision.

**Phase 1 and Phase 2 are complete. Phase 3 — Retrieval Evaluation is active. Retrieval remains bounded, advisory, exact-revision, provenance-visible, replaceable, and `live: false`.**
