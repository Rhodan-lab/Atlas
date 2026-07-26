# Phase 2 Kernel and Principia Bridge Contract

## Decision

Atlas Phase 2 introduces a deterministic, replaceable, read-only runtime compiled from canonical `atlas-content/0.1` Markdown. It also defines the Atlas receiving side of the future Principia bridge.

This work does **not** activate a live cross-repository dependency. Every accepted pilot export must declare `live: false` and use either `compatibility-fixture` or `bridge-candidate` mode.

## Authority boundary

- Canonical Atlas Markdown remains the source of truth.
- Runtime JSON is generated and replaceable.
- Atlas owns entity identity, revision, provenance, lifecycle, staleness, and review level.
- Principia owns pedagogy, artifact maturity, and publication readiness.
- Principia status fields are rejected at the Atlas ingestion boundary.
- Importing a dependency never changes either repository's status.

## Runtime contract

`atlas-kernel-runtime/0.1` contains:

- deterministic source digest;
- exact keys in the form `ENTITY_ID@REVISION`;
- normalized canonical metadata;
- body and source hashes;
- exact-revision references and typed relations;
- revision inventory by stable entity ID;
- reverse dependency indexes.

The runtime contains no build timestamp, random identifier, machine path, or mutable database state.

## Exact lookup

An entity request must provide both stable ID and positive revision. `latest` and unversioned requests are not part of the Phase 2 contract.

Errors distinguish:

- missing entity;
- missing requested revision with other revisions available;
- malformed runtime;
- malformed authored content;
- missing canonical reference.

## Principia export contract

Atlas accepts `principia-atlas-bridge-export/0.1`:

```json
{
  "contract": "principia-atlas-bridge-export/0.1",
  "mode": "bridge-candidate",
  "live": false,
  "id": "principia:failure-pattern:feedback-instability",
  "kind": "principia-artifact",
  "repository": "Rhodan-lab/principle-to-system",
  "revision": 1,
  "role": "load-bearing",
  "dependencies": [
    {
      "id": "model:en:delayed-correction-recurrence",
      "revision": 2,
      "entity_type": "model",
      "role": "supporting",
      "use": "model-boundary",
      "change_policy": "inspect"
    }
  ]
}
```

The prior opaque `depends_on: [ID, ...]` export is intentionally rejected because it omits exact revisions.

## Import result

A valid export becomes a deterministic `atlas-external-dependent/0.1` record. It is an operational dependency record, not canonical Atlas content.

Each dependency is resolved as:

- `current`;
- `superseded` when the exact revision remains available but a newer revision exists;
- `deprecated`;
- `retracted`.

A missing exact revision or missing entity blocks import.

## Impact semantics

Atlas can report:

- internal direct and transitive dependents;
- external Principia artifacts that reference the exact revision;
- the Principia-declared action: `inspect`, `revalidate`, or `block-release`.

Atlas reports the action but does not execute Principia workflow or mutate Principia status.

## Phase 2 pilot

The bounded pilot is:

```text
principia:failure-pattern:feedback-instability@1
  -> claim:en:model-oscillation-does-not-prove-real-system@1
  -> model:en:delayed-correction-recurrence@2
  -> concept:en:feedback@1
  -> concept:en:oscillation@1
```

The pilot remains `live: false` until compatible exports and machine gates pass independently in both repositories.
