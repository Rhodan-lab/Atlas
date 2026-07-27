# Phase 2 Scale, Replay, and Recovery Validation

## Status

```yaml
workstream: 5
mode: scale-replay-candidate
live: false
mutation: false
```

This workstream measures the Phase 2 kernel on a larger deterministic corpus and validates Atlas-local receipt replay semantics. It does not begin retrieval, enable synchronization, or recognize synthetic protocol records as canonical lifecycle history.

## Deterministic scale profile

The machine-readable profile is:

```text
content/fixtures/phase2_scale/scaled-benchmark-profile.json
```

It generates an isolated corpus containing:

```text
256 deterministic groups
1,026 exact entity revisions
256 synthetic Principia external dependents
```

Each group contains one source, concept, claim, and synthesis. A shared root source and root concept create a 256-dependent impact fan-out. The corpus exists only in a temporary directory during tests and CI. It does not expand canonical Atlas content.

The scaled report uses:

```yaml
contract: atlas-kernel-scaled-benchmark/0.1
mode: scale-replay-candidate
live: false
mutation: false
```

Measured operations include:

- canonical compilation;
- strict serialized-runtime admission;
- exact-revision lookup;
- synthesis-to-source provenance traversal;
- batch import of all synthetic external dependents;
- impact reporting across the full external-dependent fan-out.

Two independent compilations must produce byte-identical runtime JSON and the same source digest. Timing budgets are regression guardrails, not production-capacity claims.

## Receipt ledger

Atlas models replay with an append-only, read-only operational ledger:

```yaml
contract: atlas-principia-offline-receipt-ledger/0.1
mode: scale-replay-candidate
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

Each entry contains a complete normalized Atlas batch receipt and its deterministic SHA-256 digest. Ledger admission verifies:

- contiguous sequence numbers;
- exact predecessor digest linkage;
- unique batch IDs;
- receipt digest integrity;
- exact head sequence and digest;
- all no-mutation authority flags.

The ledger is operational evidence only. It is not repository state, canonical knowledge, or an automatic release queue.

## Replay semantics

```text
correct next sequence + correct predecessor -> accepted
exact duplicate replay                      -> idempotent-no-op
same sequence + different receipt           -> E-REPLAY-CONFLICT
skipped sequence                            -> E-REPLAY-SKIPPED
wrong predecessor                           -> E-REPLAY-PREDECESSOR
duplicate batch ID at another sequence      -> E-REPLAY-BATCH-ID
corrupted stored receipt digest             -> E-REPLAY-LEDGER-DIGEST
```

The recovery matrix accepts two independently normalized batches in sequence. The second batch uses a different batch ID and a two-artifact input set. Replaying the first batch produces a no-op and leaves the ledger byte-identical.

The matrix report uses:

```yaml
contract: atlas-principia-offline-replay-matrix/0.1
decision: verified-no-mutation
accepted_sequences: [1, 2]
idempotent_replay: true
live: false
```

## Authority boundary

This workstream preserves:

```yaml
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

Atlas does not call Principia, mutate Principia artifacts, inherit pedagogical or release status, activate a live dependency, or claim that synthetic benchmark data is canonical knowledge.
