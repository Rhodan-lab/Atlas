# Principia Evidence Registry v1

## Purpose

The evidence registry turns Atlas's accepted offline Principia reference snapshots into one deterministic route catalog.

The earlier evidence bridge validates one exact Product Alpha snapshot. The drift auditor compares a candidate snapshot with that accepted baseline. The registry adds the missing multi-route layer: it records which snapshot is currently the repository baseline for each route and compiles every registered route through the same Atlas authority checks.

It does not fetch Principia, approve candidate snapshots, or replace repository review.

## Contracts

Registry input:

```text
atlas-principia-evidence-registry/0.1
```

Compiled catalog:

```text
atlas-principia-evidence-registry-catalog/0.1
```

Current registry:

```text
content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json
```

## Registry entry

Each entry contains:

```yaml
route_id: refrigerator
snapshot_path: content/fixtures/phase2_bridge/product-alpha-refrigerator.references.v01.json
state: repository-baseline
registration_basis: merged-evidence-bridge-pr-65
registration_commit: d446c97877e969f965562c94590a1305f138f631
```

`registration_commit` records the Atlas change that introduced the baseline. The compiler records it but does not perform a network or Git-history lookup.

## Invariants

The registry compiler requires:

- `live: false`;
- `status_inheritance: prohibited`;
- a non-empty registry;
- exactly one active baseline per route;
- one route per snapshot path;
- repository-relative JSON paths under `content/fixtures/phase2_bridge/`;
- `state: repository-baseline`;
- a non-empty registration basis;
- a lowercase 40-character registration commit;
- exact equality between the registry route ID and the snapshot route ID.

Unknown fields are rejected. Missing files, path traversal, duplicate routes, duplicate paths, and route mismatches fail closed.

## Compilation

For every registered route, Atlas:

1. reads the exact repository snapshot bytes;
2. validates the frozen Principia snapshot contract;
3. resolves exact Atlas entities and revisions;
4. resolves machine-readable review authority;
5. evaluates lifecycle and provenance state;
6. hashes the exact snapshot bytes;
7. hashes the deterministic route evidence manifest;
8. records route-level health in a sorted catalog.

Routes are sorted by `route_id`, so repository file order cannot affect output bytes.

## Route health

```text
verified
revalidation-required
blocked
```

Catalog decisions:

```text
registry-verified
registry-revalidation-required
registry-blocked
```

Blocked state has precedence over revalidation; revalidation has precedence over verified state.

## Current result

The current repository contains one registered route baseline:

```yaml
route_id: refrigerator
reference_count: 2
resolved_count: 2
review_record_count: 2
health: verified
decision: registry-verified
```

This means the registered reference identities and review metadata resolve in Atlas. It does not validate the complete lesson, authorize publication, or establish learner effectiveness.

## CLI

Compile from canonical Atlas content:

```bash
python -m tools.phase2_kernel.evidence_registry_cli \
  --output /tmp/principia-evidence-registry.json
```

Compile using an existing runtime:

```bash
python -m tools.phase2_kernel.cli compile \
  --output /tmp/atlas-runtime.json

python -m tools.phase2_kernel.evidence_registry_cli \
  --runtime /tmp/atlas-runtime.json \
  --output /tmp/principia-evidence-registry.json
```

Use a different explicit registry:

```bash
python -m tools.phase2_kernel.evidence_registry_cli \
  --registry path/to/registry.json \
  --output /tmp/principia-evidence-registry.json
```

## Adding or replacing a baseline

A registry change must arrive through repository review with:

1. an offline candidate snapshot;
2. a drift report against the current baseline;
3. a justified registry entry change;
4. passing bridge, drift, registry, and Atlas compatibility checks.

The compiler never writes the registry and never accepts a candidate automatically.

## Preserved boundaries

```yaml
live: false
status_inheritance: prohibited
automatic_snapshot_acceptance: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
principia_publication_status_granted: false
learner_effectiveness_claimed: false
```
