# Phase 2 Runtime Hardening and Failure Semantics

## Status

```yaml
workstream: 4
mode: runtime-hardening-candidate
live: false
mutation: false
```

This workstream hardens Atlas as an independent knowledge kernel. It does not expand live Principia integration, retrieval, ranking, synchronization, or canonical content scope.

## Admission rule

A serialized runtime is not queryable merely because it declares:

```text
atlas-kernel-runtime/0.1
```

It must pass the strict public admission boundary implemented by:

```text
tools/phase2_kernel/repository.py
```

The public `KernelRepository` validates the complete runtime before building query indexes. The same boundary is available through:

```bash
python -m tools.phase2_kernel.cli runtime-validate atlas-runtime.json
```

A passing report uses:

```yaml
contract: atlas-runtime-validation-report/0.1
decision: valid
mutation: false
```

## Runtime invariants

Admission verifies:

1. runtime and source contracts;
2. source-root shape and source-digest recomputation from ordered entity paths and source hashes;
3. exact entity count;
4. canonical entity IDs, types, revisions, and exact keys;
5. deterministic entity ordering;
6. source and body SHA-256 values;
7. runtime-to-metadata identity agreement;
8. deterministic, duplicate-free references;
9. exact reference targets;
10. deterministic, duplicate-free relation records and exact relation targets;
11. relation targets represented in the reference graph;
12. an exact `revisions_by_id` index;
13. a complete, deterministic reverse-dependency index;
14. exact agreement between references and reverse dependencies.

The validator performs no repair and silently drops no malformed record.

## Failure semantics

Representative deterministic errors include:

```text
E-RUNTIME-SOURCE-CONTRACT
E-RUNTIME-DIGEST
E-RUNTIME-SOURCE-DIGEST
E-RUNTIME-ENTITY-COUNT
E-RUNTIME-DUPLICATE
E-RUNTIME-KEY-MISMATCH
E-RUNTIME-ENTITY-ORDER
E-RUNTIME-METADATA
E-RUNTIME-REFERENCE-ORDER
E-RUNTIME-REFERENCE-TARGET
E-RUNTIME-RELATION-TARGET
E-RUNTIME-RELATION-REFERENCE
E-RUNTIME-REVISION-INDEX
E-RUNTIME-REVERSE-INDEX
```

Failures occur during admission, before traversal or impact queries can encounter a Python `KeyError`, inconsistent graph, or silently incomplete index.

## Canonical failure fixtures

`content/fixtures/phase2_runtime/canonical/` contains isolated authored-corpus failures for:

- missing canonical references;
- invalid relation targets;
- duplicate exact entities;
- duplicate YAML keys;
- malformed relation structures.

These fixtures prove that invalid authored input fails before runtime emission.

## Serialized runtime fixtures

`content/fixtures/phase2_runtime/runtime-failure-cases.json` declares deterministic corruption cases applied to a freshly compiled valid runtime. Cases cover identity, ordering, metadata, references, relations, revision indexes, reverse indexes, and digest integrity.

## Boundary

This workstream keeps:

```yaml
live: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

The validation report is operational evidence. It is not canonical Atlas knowledge, a human review, or a decision to begin retrieval work.
