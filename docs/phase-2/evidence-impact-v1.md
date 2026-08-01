# Principia Evidence Impact Index v1

## Purpose

The impact index turns Atlas's accepted Principia evidence registry into a reverse dependency map.

The evidence registry answers which snapshot is accepted for each route. The impact index answers the opposite question:

> Which accepted Principia routes depend on this Atlas entity or exact revision?

This is useful before an Atlas revision is deprecated, retracted, superseded, marked stale, or otherwise changed. It exposes the learner-facing routes that require review without fetching or modifying Principia.

## Contracts

Full index:

```text
atlas-principia-evidence-impact-index/0.1
```

Entity or exact-revision query:

```text
atlas-principia-evidence-impact-query/0.1
```

## Inputs

The compiler reads only repository-controlled inputs:

- the accepted evidence registry;
- each registered offline Principia snapshot;
- the compiled Atlas canonical runtime;
- machine-readable Atlas review records.

It does not discover unregistered snapshots or fetch another repository.

## Index structure

The index provides three views.

### Routes

Each route records its accepted snapshot, registration identity, snapshot and manifest hashes, exact keys, and current impact state.

### Exact references

Each `entity_id@revision` records:

- canonical identity and hashes;
- all available Atlas revisions;
- whether the accepted revision is superseded;
- every dependent Principia route;
- each route's stated purpose;
- exact review authority;
- lifecycle resolution and required action.

Shared references are consolidated. If several routes depend on one exact revision, the exact reference appears once with multiple deterministic dependencies.

### Entities

Exact revisions are grouped under their Atlas entity ID. This supports entity-level impact queries when several accepted routes use different revisions.

## Impact states

```text
stable
revalidation-required
blocked
```

Index decisions:

```text
impact-index-clear
impact-index-revalidation-required
impact-index-blocked
```

Blocked impact has precedence over revalidation; revalidation has precedence over stable state.

## Commands

Compile the complete index:

```bash
python -m tools.phase2_kernel.evidence_impact_cli \
  --output /tmp/principia-evidence-impact.json
```

Use an existing Atlas runtime:

```bash
python -m tools.phase2_kernel.cli compile \
  --output /tmp/atlas-runtime.json

python -m tools.phase2_kernel.evidence_impact_cli \
  --runtime /tmp/atlas-runtime.json \
  --output /tmp/principia-evidence-impact.json
```

Query every accepted revision of one entity:

```bash
python -m tools.phase2_kernel.evidence_impact_cli \
  --entity model:en:delayed-correction-recurrence
```

Query one exact revision:

```bash
python -m tools.phase2_kernel.evidence_impact_cli \
  --entity model:en:delayed-correction-recurrence \
  --revision 2
```

An entity with no accepted Principia dependency fails closed instead of returning an ambiguous empty result.

## Current repository result

The current registry contains the accepted refrigerator route. It references two exact Atlas entities, so the expected index is:

```yaml
route_count: 1
entity_count: 2
exact_reference_count: 2
dependency_count: 2
affected_route_count: 0
decision: impact-index-clear
```

The exact query for:

```text
model:en:delayed-correction-recurrence@2
```

returns the `refrigerator` route and its declared purpose.

This result means the accepted exact references currently resolve without revalidation or blocking. It does not validate the complete lesson or claim learner effectiveness.

## Change workflow

Before changing Atlas evidence used by Principia:

1. compile the impact index;
2. query the entity or exact revision;
3. inspect every dependent route and purpose;
4. make the Atlas change through normal review;
5. rebuild the impact index;
6. use the drift and promotion gates for any required Principia snapshot replacement.

The index is advisory evidence for review. It does not veto or execute changes by itself.

## Preserved boundaries

```yaml
live: false
status_inheritance: prohibited
automatic_snapshot_acceptance: false
automatic_registry_update: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
principia_publication_status_granted: false
learner_effectiveness_claimed: false
```
