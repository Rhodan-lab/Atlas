# Atlas Project State

## Current status

**Phase 2 — Minimal Knowledge Kernel (active)**

Phase 1 is closed under an explicitly **AI-reviewed** policy. No human or expert verification is claimed.

## Accepted history

- Phase 0 foundation — PR #3, commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- review and promotion experiments — PR #4, commit `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency reporting — PR #5, commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- delayed-feedback readiness — PR #6, commit `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only authored corpus — PR #7, commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations — PR #8, commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- optional human handoff — PR #9, commit `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`;
- optional exact-snapshot intake — PR #10, commit `9809bcb523954770e87c78154cdb124f37aadf46`;
- optional admission boundary — PR #17, commit `01feffc696cc207305ef74c92d600f37f1e240a4`;
- Phase 1 AI review and Phase 2 activation — PR #18, commit `f90fa53f99ec9780451c9c50c57625759ba3b2b5`;
- first Phase 2 kernel and bridge receiver — PR #19, commit `8f1e473578d9086a73dae44f0b6001b246cfbc20`;
- Principia v0.2 importer implementation — PR #20, commit `1cc4aec6908a8703a7f505478329c633a23b4ef9`;
- accepted Principia importer governance baseline — PR #21, commit `9370cc746e9756e433ac3772d56d079c9803b144`;
- offline multi-artifact and lifecycle-protocol audit — PR #22, commit `1096a2176eb50e1921081bb3f46eeac8b13bd2c3`.

## Language policy

The active authored and review corpus is English-only.

Language-neutral translation identity, revision lineage, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent an active translated corpus.

## Review policy

Atlas distinguishes review levels instead of presenting all review as equivalent.

### AI-reviewed

An AI-reviewed artifact has:

- an identified AI reviewer;
- explicit model and non-human status;
- exact entity revisions;
- source-use checks;
- reproducibility or mathematical checks where applicable;
- recorded findings and corrections;
- explicit limitations;
- `human_verified: false`.

AI review is sufficient for the current Atlas development phase and does not require a separate human reviewer duty.

### Human-verified

Human verification is an optional stronger layer. Existing handoff, intake, admission, coverage, and promotion tools remain available for future use, but they are not active Phase 2 gates.

Atlas must never convert an AI review into a human review or invent reviewer identity, credentials, independence, or accountability.

## Phase 1 completion evidence

The active completion evidence remains:

- `content/reviews/ai/feedback-delayed-comprehensive.json`;
- `docs/phase-1/ai-review-report.md`;
- `tools/foundation-validator/phase1_ai_review.py`;
- corrected delayed-feedback canonical revisions.

The reviewer is `GPT-5.6 Thinking`, reviewer kind `ai`, with `human_verified: false` and `human_review_required: false`.

For:

```text
x[t+1] = x[t] - x[t-1]
x0 = 1
x1 = 0
```

the orbit is bounded and periodic with exact period 6. This is a formal result for one recurrence and initial history. It is not empirical evidence about a real system and not a general theorem that delay causes instability.

## Authority order

1. `PROJECT_STATE.md`;
2. accepted foundation documents in `docs/foundation/`;
3. accepted ADRs;
4. canonical authored content;
5. identified review records and reports, with review level visible;
6. generated manifests and operational artifacts;
7. experimental runtime and adapter code.

## Phase 2 objective

Phase 2 builds the smallest dependable runtime over authored `atlas-content/0.1` Markdown.

Required outcomes:

- canonical-to-runtime compilation;
- read-only exact-revision entity repository;
- typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- deterministic command and library interfaces;
- compatibility and failure tests;
- representative and scaled performance measurements;
- no change to authored Markdown meaning.

## Phase 2 workstream 1 — accepted

PR #19 implemented:

- `atlas-kernel-runtime/0.1` deterministic compilation;
- path-form-independent source identity;
- exact `ENTITY_ID@REVISION` lookup;
- typed relation and explicit provenance traversal;
- internal reverse-dependency impact queries;
- Atlas-local bridge receiver validation;
- normalized `atlas-external-dependent/0.1` operational records;
- deterministic rejection of ID-only exports, stale revisions, status inheritance, and `live: true`;
- Python 3.11 and 3.13 machine gates.

This receiver is not a live integration. It does not clone Principia, call Principia during Atlas validation, copy Principia status, or modify canonical Atlas meaning.

## Phase 2 workstream 2 — accepted

PR #20 established and validated the Principia importer baseline using the exact export merged through Principia PR #16. PR #21 finalized the accepted governance record.

Atlas importer baseline:

```yaml
contract: principia-atlas-external-dependent/0.2
mode: importer-candidate
live: false
accepted_pr: 20
accepted_merge_commit: 1cc4aec6908a8703a7f505478329c633a23b4ef9
governance_pr: 21
governance_merge_commit: 9370cc746e9756e433ac3772d56d079c9803b144
```

Pinned Principia source identity:

```text
Principia PR: #16
Principia head: 405cfabb6eba71b42bd42ed81b922b458f9175e7
Principia merge: eb3a00dfbfdfaa5470cb40505fa213e5349a917f
Principia source bridge mode: bridge-candidate
```

Accepted exact dependencies:

- `claim:en:model-oscillation-does-not-prove-real-system@1`;
- `concept:en:feedback@1`;
- `concept:en:oscillation@1`;
- `model:en:delayed-correction-recurrence@2`.

Accepted importer evidence:

- pinned copy of the generated Principia export;
- source path, Git blob SHA, and SHA-256 verification;
- adapter from the Principia v0.2 wire format into the Atlas receiver;
- verification that `depends_on` exactly mirrors `depends_on_exact`;
- exact admission of all four accepted dependencies;
- preserved separation of Atlas and Principia status;
- lifecycle-aware impact escalation;
- representative benchmarks for compilation, lookup, provenance, bridge import, and impact reporting.

Lifecycle policy:

```text
current               -> preserve declared action
deprecated            -> at least revalidate
review-required stale -> at least revalidate
confirmed stale       -> at least revalidate
retracted             -> block-release
```

Atlas reports both the Principia-declared action and the effective lifecycle action. It does not mutate either repository or execute the action automatically.

PR #20 measurements on the 34-entity corpus passed their regression budgets on Python 3.11 and 3.13. These measurements are operational small-corpus evidence, not production-scale claims.

## Phase 2 workstream 3 — accepted

Principia was inspected before this workstream began. The pinned main commit `4ecb41ad4f9f524e83cc0db43f672bd9dcf3b67a` contains the merged Phase 18 offline reconciliation simulation and earlier Phase 16–17 evidence.

External-source observation:

- Principia PR #25 is merged at that pinned commit;
- the pinned Phase 18 artifacts exist on main;
- Principia `PROJECT_STATE.md` at that commit still contains candidate-era exact-head-validation-pending wording;
- Atlas records that inconsistency but does not change or reinterpret Principia governance.

Accepted workstream state:

```yaml
snapshot_contract: atlas-principia-offline-snapshot/0.1
batch_receipt_contract: atlas-principia-offline-batch-receipt/0.1
protocol_audit_contract: atlas-principia-offline-protocol-audit/0.1
mode: offline-protocol-audit-candidate
state: accepted
accepted_pr: 22
tested_head: 3a0e726869f5cc589606149b822865fa84724ac5
accepted_merge_commit: 1096a2176eb50e1921081bb3f46eeac8b13bd2c3
live: false
fixture_kind: bounded-synthetic
```

The mode remains `offline-protocol-audit-candidate` because this is still an offline, non-live protocol maturity level. The implementation workstream itself is accepted.

The accepted evidence chain contains:

```text
3 Principia artifact exports
1 atomic multi-artifact batch
1 Principia batch receipt
2 bounded-synthetic lifecycle events
2 Principia acknowledgements
1 event/acknowledgement digest chain
1 reconciliation report
```

The audit:

- binds the exact nine source-path, Atlas-fixture-path, and Git-blob-SHA mappings;
- rejects fixture path escape and snapshot mapping substitution;
- binds the complete accepted Atlas PR #20/#21 importer snapshot;
- atomically re-imports `principia:failure-pattern:feedback-instability@1`, `principia:investigation:room-cooling@1`, and `principia:system-dossier:refrigerator@1`;
- compares all normalized records against Principia's Phase 16 receipt;
- independently recomputes lifecycle fan-out from the imported dependency records;
- verifies unique protocol identities, events, and acknowledgements;
- verifies event and acknowledgement digests, order, predecessors, and chain heads;
- rejects weakened actions and affected-artifact-set drift;
- binds Phase 17 provenance and verifies the Phase 18 reconciliation report;
- rejects partial batches, corrupted exports, stale reconciliation references, automatic mutation, status inheritance, and `live: true`.

The two lifecycle events are Principia-authored `bounded-synthetic` fixtures. Atlas does not accept them as real lifecycle transitions and does not change the actual status of `concept:en:feedback@1` or `claim:en:model-oscillation-does-not-prove-real-system@1`.

Accepted audit result:

```yaml
contract: atlas-principia-offline-protocol-audit/0.1
decision: verified-no-mutation
source_repository: Rhodan-lab/principle-to-system
source_pull_request: 25
source_commit: 4ecb41ad4f9f524e83cc0db43f672bd9dcf3b67a
record_count: 3
event_count: 2
acknowledgement_count: 2
reconciled_count: 2
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

Validation passed on the exact tested head through:

- Phase 2 Knowledge Kernel on Python 3.11 and 3.13;
- Foundation Contract;
- Phase 1 AI Review regression;
- Atlas CI;
- TypeScript, Rust, and Python 3.11–3.13;
- C++ on Ubuntu, macOS, and Windows;
- end-to-end contracts.

## Principia & Atlas boundary

Atlas is the knowledge and governance layer of the future **Principia & Atlas** system.

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns causal explanation, learning pathways, investigations, simulations, system dossiers, failure analysis, and design experiences.
- Principia may reference exact Atlas revisions.
- Atlas may report dependency impact when upstream knowledge changes.
- Principia may acknowledge an offline impact report, but that acknowledgement does not command or mutate Atlas.
- Neither repository inherits the other repository's status automatically.
- The repositories remain separate and independently buildable.
- No live cross-repository dependency is declared during Phase 2.

## Current restrictions

Still frozen:

- polished product UI;
- specialized retrieval and ranking;
- vector database selection;
- synchronization and plugins;
- active translated corpus;
- hidden or autonomous authority claims;
- automatic conversion of AI review into human verification;
- direct repository merger with Principia;
- live Principia dependency;
- accepting external synthetic events as canonical Atlas lifecycle history;
- automatic status or release mutation;
- treating prototype runtime formats as canonical before kernel evaluation.

Allowed:

- minimal knowledge-kernel implementation;
- deterministic compilation and queries;
- English canonical content corrections;
- explicitly labeled AI reviews;
- optional human verification that remains separately labeled;
- read-only exact-revision Principia compatibility;
- pinned external fixtures and impact reports;
- atomic offline multi-artifact import tests;
- bounded-synthetic event and acknowledgement audits;
- lifecycle escalation reporting;
- benchmark and regression maintenance.

## Immediate next actions

1. add malformed runtime and missing canonical-reference fixtures beyond bridge-specific cases;
2. build a larger deterministic synthetic corpus for scaled benchmarks;
3. test multiple independent batches, receipt-chain continuation, idempotent replay, and conflicting sequence recovery;
4. define the Phase 2 closure evidence and remaining retrieval-entry blockers;
5. keep `live: false` until independent machine contracts pass in both repositories and a separate activation decision is recorded;
6. produce the Phase 2 completion report before retrieval work.

**Phase 1 is complete under the AI-reviewed policy. Phase 2 is active. PRs #19–#22 are accepted. The offline multi-artifact and lifecycle-protocol audit remains non-live, treats lifecycle events as bounded-synthetic fixtures only, and does not imply human verification.**
