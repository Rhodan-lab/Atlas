# Principia–Atlas Evidence Drift Auditor v1

## Purpose

The evidence drift auditor compares one new, offline Principia reference snapshot with the accepted Atlas snapshot for the same Product Alpha route.

It answers four bounded questions:

1. Did the Principia source commit or route blob change?
2. Were Atlas references added, removed, or moved to another exact revision?
3. Did reference purposes or declared review metadata change?
4. Does the candidate still resolve against current Atlas entities and machine-readable review authority?

The auditor emits a deterministic report. It does not fetch Principia, accept a snapshot, change lifecycle state, execute a release action, or mutate either repository.

## Contract

```text
atlas-principia-evidence-drift-report/0.1
```

The report binds:

- accepted and candidate snapshot contracts;
- accepted and candidate Principia source identities;
- SHA-256 digests of the two review-aware Atlas evidence manifests;
- source-identity changes;
- exact reference additions and removals;
- revision transitions;
- purpose changes;
- declared review-metadata changes;
- changed Atlas validation outcomes;
- one bounded refresh-review decision;
- explicit no-live and no-mutation fields.

## Route boundary

A candidate must describe the same:

```text
source_repository
source_path
route_id
```

A different route is not drift within the accepted route. It requires a separate baseline and is rejected with `E-EVIDENCE-DRIFT-SCOPE`.

## Decisions

### `no-refresh-needed`

The accepted and candidate snapshots produce the same source identity, reference set, metadata, and Atlas validation result.

### `proceed-source-identity-refresh-review`

Only the Principia commit or route blob identity changed. The decision allows human or governed review of the candidate; it does not automatically replace the baseline.

### `review-reference-metadata-change`

The exact reference set is unchanged, but purpose text, declared review metadata, or the resulting Atlas validation outcome changed.

### `review-reference-set-change`

A reference was added, removed, or moved to another exact revision and the candidate still resolves without a block or revalidation requirement.

### `hold-for-evidence-revalidation`

The candidate resolves, but Atlas authority requires revalidation because review declarations, lifecycle state, staleness, or another evidence boundary does not match.

### `reject-unresolved-reference-refresh`

At least one candidate reference is missing, unavailable, or otherwise requires `block-release` under the evidence manifest.

## Commands

Compile the current Atlas runtime:

```bash
python -m tools.phase2_kernel.cli compile \
  --output /tmp/atlas-runtime.json
```

Compare a candidate snapshot:

```bash
python -m tools.phase2_kernel.evidence_drift_cli \
  --runtime /tmp/atlas-runtime.json \
  --candidate /path/to/candidate.references.json \
  --output /tmp/evidence-drift-report.json
```

Use a different accepted baseline only when governance has explicitly selected it:

```bash
python -m tools.phase2_kernel.evidence_drift_cli \
  --baseline /path/to/accepted.references.json \
  --candidate /path/to/candidate.references.json \
  --output /tmp/evidence-drift-report.json
```

## Current repository control

Principia has no route commit newer than the accepted Product Alpha refrigerator snapshot at the time this auditor was added. The focused workflow therefore compares the accepted snapshot with itself as a zero-drift control.

Expected result:

```yaml
decision: no-refresh-needed
change_classes:
  - none
baseline_manifest_sha256: equal-to-candidate-manifest-sha256
automatic_snapshot_acceptance: false
repository_mutation: false
```

Changed candidate behavior is exercised through explicit deterministic tests rather than a fabricated Principia revision.

## Preserved boundaries

```yaml
live: false
status_inheritance: prohibited
automatic_snapshot_acceptance: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

The auditor does not grant Principia publication status, validate the full learner experience, claim learner effectiveness, or activate live cross-repository synchronization.
