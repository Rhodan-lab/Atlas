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
- offline multi-artifact and lifecycle-protocol audit — PR #22, commit `1096a2176eb50e1921081bb3f46eeac8b13bd2c3`;
- accepted offline protocol governance record — PR #23, commit `ec666b59c4834c9a716006be9f9830d20178af34`;
- runtime hardening and failure semantics — PR #24, commit `7596e4fbae099304d64a5b2371c0fb4a2e55ffc4`;
- scale, replay, and recovery validation — PR #26, commit `dd0c64447fb70727d260362f9877ffc6be560c3c`.

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

Accepted exact dependencies:

- `claim:en:model-oscillation-does-not-prove-real-system@1`;
- `concept:en:feedback@1`;
- `concept:en:oscillation@1`;
- `model:en:delayed-correction-recurrence@2`.

Lifecycle policy:

```text
current               -> preserve declared action
deprecated            -> at least revalidate
review-required stale -> at least revalidate
confirmed stale       -> at least revalidate
retracted             -> block-release
```

Atlas reports both the Principia-declared action and the effective lifecycle action. It does not mutate either repository or execute the action automatically.

## Phase 2 workstream 3 — accepted

The accepted offline protocol workstream pins Principia commit `4ecb41ad4f9f524e83cc0db43f672bd9dcf3b67a` and records:

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

The accepted evidence chain contains three Principia artifact exports, one atomic batch, one Principia receipt, two bounded-synthetic lifecycle events, two acknowledgements, one digest chain, and one reconciliation report.

The audit binds exact source paths, Atlas fixture paths, Git blob SHAs, the accepted Atlas importer snapshot, lifecycle fan-out, acknowledgement actions, affected-artifact sets, chain heads, and Phase 17–18 provenance.

The lifecycle events remain Principia-authored `bounded-synthetic` fixtures. Atlas does not accept them as real lifecycle transitions and does not change actual Atlas entity status.

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

## Phase 2 workstream 4 — accepted

PR #24 established strict runtime admission and canonical failure semantics.

Accepted workstream state:

```yaml
runtime_contract: atlas-kernel-runtime/0.1
validation_contract: atlas-runtime-validation-report/0.1
mode: runtime-hardening-candidate
state: accepted
accepted_pr: 24
tested_head: a7b2998937f6225462bf2b0f3820e5bf76ac56d8
accepted_merge_commit: 7596e4fbae099304d64a5b2371c0fb4a2e55ffc4
live: false
mutation: false
```

The public `KernelRepository` now validates a complete serialized runtime before indexing it. Admission checks:

- runtime and source contracts;
- recomputed source digest from ordered entity paths and source hashes;
- exact entity count, identity, revision, type, key, path, and deterministic order;
- source and body digest shape;
- runtime-to-metadata identity agreement;
- sorted, duplicate-free references and exact targets;
- sorted, duplicate-free relations and exact targets;
- relation-to-reference graph agreement;
- an exact `revisions_by_id` index;
- a complete reverse-dependency index that exactly mirrors references.

Failure evidence includes:

```text
17 serialized-runtime corruption cases
5 authored-corpus failure cases
22 deterministic negative fixtures total
```

The authored-corpus fixtures cover missing canonical references, invalid relation targets, duplicate exact entities, duplicate YAML keys, and malformed relation structures.

Accepted runtime validation result:

```yaml
contract: atlas-runtime-validation-report/0.1
decision: valid
entity_count: 34
reference_count: 50
relation_count: 7
reverse_edge_count: 50
mutation: false
```

Validation passed on Python 3.11 and 3.13, Foundation Contract, Atlas CI, TypeScript, Rust, Python 3.11–3.13, C++ on Ubuntu/macOS/Windows, and end-to-end contracts.

## Phase 2 workstream 5 — accepted

PR #26 established deterministic scale, replay, and recovery evidence without expanding canonical Atlas content.

Accepted workstream state:

```yaml
scaled_contract: atlas-kernel-scaled-benchmark/0.1
replay_contract: atlas-principia-offline-replay-matrix/0.1
ledger_contract: atlas-principia-offline-receipt-ledger/0.1
mode: scale-replay-candidate
state: accepted
accepted_pr: 26
tested_head: a5bf1d6bf481c3d8f35312050f12ec4ab48b1f08
accepted_merge_commit: dd0c64447fb70727d260362f9877ffc6be560c3c
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

The accepted scale evidence uses an isolated deterministic corpus with:

```text
256 groups
1,026 exact entity revisions
256 synthetic Principia external dependents
```

The corpus exists only in temporary test directories and is not canonical Atlas knowledge. Two independent compilations must remain byte-identical and preserve the exact source digest.

The accepted replay evidence:

- admits two independently normalized batch sequences;
- records append-only receipt-chain continuation;
- treats an exact duplicate replay as an idempotent no-op;
- rejects conflicting sequence, skipped sequence, wrong predecessor, duplicate batch ID, and corrupted ledger digest;
- reports `decision: verified-no-mutation`;
- performs no status, release, repository, or live-integration mutation.

Validation passed on the exact tested head through Phase 2 Scale and Replay, Phase 2 Knowledge Kernel, Foundation Contract, Atlas CI, TypeScript, Rust, Python 3.11–3.13, C++ on Ubuntu/macOS/Windows, and end-to-end contracts.

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
- repairing or silently dropping malformed runtime records;
- treating prototype runtime formats as canonical before kernel evaluation.

Allowed:

- minimal knowledge-kernel implementation;
- deterministic compilation and queries;
- strict serialized-runtime admission;
- deterministic canonical and runtime failure fixtures;
- English canonical content corrections;
- explicitly labeled AI reviews;
- optional human verification that remains separately labeled;
- read-only exact-revision Principia compatibility;
- pinned external fixtures and impact reports;
- atomic offline multi-artifact import tests;
- bounded-synthetic event and acknowledgement audits;
- lifecycle escalation reporting;
- scaled deterministic corpus benchmarks;
- append-only offline receipt replay and recovery tests;
- benchmark and regression maintenance.

## Immediate next actions

1. define Phase 2 closure evidence and the remaining retrieval-entry blockers;
2. verify kernel replaceability, migration boundaries, and rollback expectations;
3. produce the Phase 2 completion report with an explicit retrieval-entry recommendation;
4. keep `live: false` until independent machine contracts pass in both repositories and a separate activation decision is recorded.

**Phase 1 is complete under the AI-reviewed policy. Phase 2 remains active. PRs #19–#26 are accepted. Scale, replay, and recovery are accepted as `mode: scale-replay-candidate` with `live: false`; retrieval and live integration remain frozen pending the Phase 2 completion report.**
