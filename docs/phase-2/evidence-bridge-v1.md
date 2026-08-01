# Principia–Atlas Evidence Bridge v1

## Purpose

This maintenance capability audits exact Atlas revisions referenced by a pinned Principia Product Alpha route. It is offline, deterministic, read-only, and intentionally separate from live synchronization.

The bridge validates:

- the Principia source repository, commit, route path, and Git blob identity;
- canonical Atlas entity IDs and exact positive revisions;
- lifecycle and staleness state;
- Principia-declared review level and human-verification metadata against Atlas review authority;
- canonical file and body digests;
- reachable Atlas source provenance;
- required inspect, revalidate, or block-release action.

It emits `atlas-principia-evidence-manifest/0.1`. The manifest can be consumed by Principia as evidence metadata, but it cannot grant Principia publication, pedagogical, review, or release status.

## Review authority

Canonical entity revisions and review records are separate governed objects. The bridge first resolves the immutable exact canonical entity, then resolves exact entity outcomes from machine-readable records under `content/reviews/ai/` with contract `atlas-ai-review/0.1`.

This prevents two errors:

- rewriting an existing canonical revision merely to add review metadata;
- treating the absence of an inline `review` block as proof that no review exists.

A review record is accepted only when it identifies the same entity ID and exact revision, has a passing outcome, and its review level and human-verification value match the declaration carried by Principia.

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

Both exact revisions resolve. Both declarations match the machine-readable comprehensive delayed-feedback review:

```text
review record: ai-review:feedback-delayed-comprehensive
review contract: atlas-ai-review/0.1
review level: ai-reviewed
human verified: false
```

The current manifest therefore returns:

```yaml
decision: verified-offline-reference-manifest
reference_count: 2
resolved_count: 2
review_record_count: 2
revalidate_count: 0
blocked_count: 0
```

This verifies reference identity and review metadata only. It does not automatically validate a Principia lesson, authorize publication, or establish learner effectiveness.

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

An alternate review directory may be supplied with `--review-root`, but it remains a local pinned input and receives no write authority.

## Deterministic behavior

- entries are sorted by exact Atlas identity;
- findings are sorted by severity, code, and identity;
- review files and exact entity outcomes are indexed deterministically;
- duplicate exact review authority is rejected;
- repeated builds over the same pinned snapshot, canonical corpus, and review records are byte-identical;
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
canonical_mutation: false
review_mutation: false
principia_publication_status_granted: false
atlas_review_status_copied_into_principia: false
learner_effectiveness_claimed: false
```

A future snapshot update must pin a new Principia commit and blob. A future live bridge remains unauthorized.
