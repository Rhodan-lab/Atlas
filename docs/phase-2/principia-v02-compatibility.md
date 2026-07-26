# Principia v0.2 Compatibility

## Accepted external contract

Atlas consumes the exact export merged through Principia PR #16:

```text
contract: principia-atlas-external-dependent/0.2
source repository: Rhodan-lab/principle-to-system
source merge commit: eb3a00dfbfdfaa5470cb40505fa213e5349a917f
source path: integration/principia-atlas/exports/feedback-instability.external-dependent.fixture.json
mode: bridge-candidate
live: false
```

The Atlas fixture is a pinned copy, not a network call. Its sidecar records the Principia pull request, head and merge commits, source path, Git blob SHA, and SHA-256 digest.

## Dual dependency representation

The Principia export contains:

- `depends_on` — the deterministic legacy ID index;
- `depends_on_exact` — the authoritative revision-bearing dependency objects.

Atlas requires both lists to contain the same IDs in deterministic order. The legacy list does not grant admission by itself; exact positive revisions remain mandatory.

## Adapter boundary

`tools/phase2_kernel/bridge.py` adapts the Principia wire format into Atlas's internal bridge-receiver contract. The resulting operational record preserves:

- the original Principia source contract;
- the Atlas adapter contract;
- verification that the ID index matches the exact dependency list;
- exact Atlas entity resolution;
- the prohibition on status inheritance;
- `live: false`.

The adapter rejects unknown fields, nested status data, mismatched dependency indexes, nondeterministic ordering, incompatible Atlas content contracts, unavailable exact revisions, and live activation.

## Lifecycle impact

Principia declares the minimum response for each dependency:

- `inspect`;
- `revalidate`;
- `block-release`.

Atlas may escalate but never weaken that response:

```text
current entity         -> preserve Principia-declared action
deprecated entity      -> at least revalidate
review-required stale  -> at least revalidate
confirmed stale        -> at least revalidate
retracted entity       -> block-release
```

The report distinguishes `declared_action` from `effective_action`. It does not mutate Principia status, Atlas status, or release state, and it does not execute a release action automatically.

## Current pilot

```text
principia:failure-pattern:feedback-instability@1
  -> claim:en:model-oscillation-does-not-prove-real-system@1
  -> concept:en:feedback@1
  -> concept:en:oscillation@1
  -> model:en:delayed-correction-recurrence@2
```

This is a validated, bounded compatibility candidate. It is not a live cross-repository integration.
