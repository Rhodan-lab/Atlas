# Offline Principia Protocol Audit

## Purpose

This workstream verifies the later Principia Phase 16–18 offline integration evidence using Atlas's accepted importer and current canonical runtime.

It is an audit and recomputation boundary, not synchronization. Atlas reads only pinned files committed to this repository. CI does not clone or call Principia.

## Pinned Principia snapshot

```text
repository: Rhodan-lab/principle-to-system
commit: 4ecb41ad4f9f524e83cc0db43f672bd9dcf3b67a
merged source PR: #25
snapshot contract: atlas-principia-offline-snapshot/0.1
mode: offline-protocol-audit-candidate
live: false
```

The snapshot records the original Principia source path and Git blob SHA for every copied file. Atlas recomputes each local fixture's Git blob identity before using it.

The observed Principia commit contains merged Phase 18 evidence while its `PROJECT_STATE.md` still includes candidate-era exact-head-pending wording. Atlas records that inconsistency as an external-source observation and does not resolve Principia governance on Principia's behalf.

## Pinned files

The snapshot includes:

1. three `principia-atlas-external-dependent/0.2` exports;
2. one `principia-atlas-offline-import-batch/0.2` atomic batch;
3. one `principia-atlas-offline-batch-receipt/0.2` receipt;
4. one `principia-atlas-offline-lifecycle-event-stream/0.1` stream;
5. one `principia-atlas-offline-lifecycle-acknowledgement-stream/0.1` stream;
6. one `principia-atlas-offline-event-protocol-chain/0.1` chain;
7. one `principia-atlas-offline-reconciliation-report/0.1` report.

## Atomic import

`import_offline_batch` performs these checks before returning any operational record:

- exact Atlas implementation and governance merge commits;
- `atomic: true` and `live: false`;
- deterministic artifact order and unique IDs;
- exact export path and SHA-256;
- exact artifact revision and dependency count;
- successful import of every Principia v0.2 export;
- exact Atlas entity and revision resolution.

The accepted batch contains:

```text
principia:failure-pattern:feedback-instability@1
principia:investigation:room-cooling@1
principia:system-dossier:refrigerator@1
```

A partial or corrupted input fails the complete operation. No partial Atlas registration is returned.

## Receipt verification

Atlas freshly re-imports all three exports and compares the complete normalized records against Principia's receipt. Counts alone are insufficient.

The verification checks:

- batch identity, sequence, predecessor, and batch digest;
- accepted Atlas importer implementation and governance baseline;
- atomic acceptance with zero rejected records;
- complete dependency records, including roles, uses, policies, keys, revisions, and resolution;
- prohibition of status inheritance;
- no automatic mutation.

## Lifecycle fixtures

The event stream contains two events:

```text
concept:en:feedback@1
current -> deprecated
expected effective action: revalidate

claim:en:model-oscillation-does-not-prove-real-system@1
current -> retracted
expected effective action: block-release
```

Both events declare `fixture_kind: bounded-synthetic`. Atlas applies each transition only to a copied runtime used for deterministic impact calculation.

This does **not** change the actual canonical entity status and does **not** establish lifecycle history in Atlas.

## Acknowledgement audit

For every event Atlas independently computes:

- the exact external dependent set;
- the effective lifecycle action;
- the affected artifact revisions.

Principia's acknowledgement must preserve that result exactly. The audit rejects:

- a weakened or changed action;
- a missing or extra affected artifact;
- an event ID or digest mismatch;
- broken acknowledgement sequencing;
- status inheritance;
- automatic status or release action;
- repository mutation;
- `live: true`.

## Chain and reconciliation

Atlas verifies the event and acknowledgement digest chains, predecessor links, and chain heads. It then verifies the Phase 18 reconciliation report against the independently verified events and acknowledgements.

A successful result is:

```yaml
decision: verified-no-mutation
record_count: 3
event_count: 2
acknowledgement_count: 2
reconciled_count: 2
fixture_kind: bounded-synthetic
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

## Authority boundary

- Atlas remains authority for Atlas knowledge lifecycle.
- Principia remains authority for Principia pedagogical and release status.
- Principia acknowledgements are evidence that Principia recorded an offline response; they do not command Atlas.
- Principia reconciliation may observe its own current artifact revisions and statuses, but Atlas does not import those statuses.
- No network synchronization or live event delivery is implemented.
- No lifecycle or release action is executed automatically.

## Commands

```bash
python -m tools.phase2_kernel.cli offline-batch-import \
  --output /tmp/atlas-offline-batch-receipt.json

python -m tools.phase2_kernel.cli offline-protocol-audit \
  --output /tmp/atlas-offline-protocol-audit.json
```
