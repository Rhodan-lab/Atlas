# Principia–Atlas Evidence Bridge v1

## Purpose

This maintenance capability audits exact Atlas revisions referenced by a pinned Principia Product Alpha route. It is offline, deterministic, read-only, and intentionally separate from live synchronization.

The bridge validates:

- the Principia source repository, commit, route path, and Git blob identity;
- canonical Atlas entity IDs and exact positive revisions;
- lifecycle and staleness state;
- Principia-declared review level and human-verification metadata against Atlas authority;
- canonical file and body digests;
- reachable Atlas source provenance;
- required inspect, revalidate, or block-release action.

It emits `atlas-principia-evidence-manifest/0.1`. The manifest can be consumed by Principia as evidence metadata, but it cannot grant Principia publication, pedagogical, review, or release status.

## Current pinned source

```yaml
repository: Rhodan-lab/principle-to-system
commit: 047867f5b0a803c59b918738c45c24909ea998be
path: software/product_alpha/routes/refrigerator.json
blob_sha: ec6195eb217efacf4d4e5d675ba1cf74b03f9600
route_id: refrigerator
live: false
```

The pinned route references:

- `model:en:delayed-correction-recurrence@2`;
- `claim:en:model-oscillation-does-not-prove-real-system@1`.

## Current audit result

Both exact revisions resolve. The model review declaration matches Atlas. The claim declares `ai-reviewed` and `human_verified: false` in Principia, while that exact Atlas canonical claim revision has no embedded review record. The bridge therefore returns:

```text
decision: revalidate-principia-reference-metadata
blocked_count: 0
revalidate_count: 1
```

This is a metadata defect signal, not an automatic correction. Atlas does not mutate the Principia route, Atlas canonical content, review records, lifecycle state, or release state.

## Command

```bash
python -m tools.phase2_kernel.evidence_bridge_cli \
  --output /tmp/product-alpha-refrigerator.evidence-manifest.json
```

A precompiled runtime may be supplied:

```bash
python -m tools.phase2_kernel.cli compile \
  --output /tmp/atlas-runtime.json

python -m tools.phase2_kernel.evidence_bridge_cli \
  --runtime /tmp/atlas-runtime.json \
  --output /tmp/product-alpha-refrigerator.evidence-manifest.json
```

## Deterministic behavior

- entries are sorted by exact Atlas identity;
- findings are sorted by severity, code, and identity;
- repeated builds over the same pinned snapshot and canonical corpus are byte-identical;
- missing entities and unavailable revisions are represented explicitly;
- unavailable revisions never fall back to latest;
- duplicate exact references are rejected;
- live snapshots and status inheritance are rejected.

## Authority boundary

```yaml
live_principia_dependency: false
status_inheritance: prohibited
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
principia_publication_status_granted: false
atlas_review_status_copied_into_principia: false
```

A future snapshot update must pin a new Principia commit and blob. A future live bridge remains unauthorized.
