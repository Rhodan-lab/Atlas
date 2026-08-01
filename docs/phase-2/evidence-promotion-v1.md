# Principia Evidence Promotion Gate v1

## Purpose

The evidence promotion gate turns one offline Principia candidate snapshot into a deterministic Atlas review packet.

It joins three existing Atlas capabilities:

1. the accepted evidence registry selects the current route baseline;
2. the evidence bridge validates exact Atlas entities, revisions, provenance, lifecycle, and review authority;
3. the drift auditor classifies what changed between the accepted baseline and the candidate.

The promotion gate adds the missing decision boundary before a registry change. It does not accept a candidate, edit the registry, fetch Principia, or mutate either repository.

## Contract

```text
atlas-principia-evidence-promotion-packet/0.1
```

The packet binds:

- the accepted registry contract and SHA-256 digest;
- the registered route baseline and registration metadata;
- exact baseline and candidate snapshot paths and SHA-256 digests;
- accepted and candidate Principia source identities;
- the drift report decision and digest;
- the candidate evidence-manifest decision and digest;
- candidate reference, review, revalidation, and block counts;
- one gate state;
- one bounded promotion decision;
- review and acceptance requirements;
- a non-operative registry replacement template when reviewable;
- explicit offline and no-mutation boundaries.

## Inputs

The CLI requires:

```text
--candidate
--submission-basis
```

The candidate must be a repository-relative JSON file under:

```text
content/fixtures/phase2_bridge/
```

The submission basis must be a lowercase slug. It records why the candidate entered review. It does not establish acceptance or publication authority.

The route ID in the candidate selects exactly one baseline from:

```text
content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json
```

An unregistered route fails closed. New routes must first arrive through a separately reviewed registry change.

## Gate states

### `no-change`

The candidate is evidence-equivalent to the accepted baseline.

Decision:

```text
candidate-redundant
```

No registry replacement is proposed.

### `reviewable`

The candidate resolves successfully and can enter repository review.

Possible decisions:

```text
ready-for-source-refresh-review
requires-reference-metadata-review
requires-reference-set-review
```

The packet emits a registry replacement template whose `registration_commit` is `null`. That value must be supplied only by the reviewed repository change that actually registers the candidate.

### `hold`

The candidate resolves, but review authority, lifecycle, staleness, or declared metadata requires revalidation.

Decision:

```text
hold-for-evidence-revalidation
```

No registry replacement is eligible.

### `blocked`

At least one exact Atlas reference is unavailable, missing, retracted, or otherwise requires a release block.

Decision:

```text
reject-unresolved-candidate
```

No registry replacement is eligible.

## Commands

Compile the Atlas runtime:

```bash
python -m tools.phase2_kernel.cli compile \
  --output /tmp/atlas-runtime.json
```

Build a promotion packet:

```bash
python -m tools.phase2_kernel.evidence_promotion_cli \
  --runtime /tmp/atlas-runtime.json \
  --candidate content/fixtures/phase2_bridge/candidate.references.json \
  --submission-basis reviewed-principia-route-refresh \
  --output /tmp/evidence-promotion-packet.json
```

Use a different explicit registry only when repository governance has selected it:

```bash
python -m tools.phase2_kernel.evidence_promotion_cli \
  --registry path/to/accepted-registry.json \
  --candidate path/to/candidate.references.json \
  --submission-basis reviewed-candidate-import \
  --output /tmp/evidence-promotion-packet.json
```

## Reviewable registry template

A reviewable packet may contain:

```yaml
route_id: refrigerator
snapshot_path: content/fixtures/phase2_bridge/candidate.references.json
state: repository-baseline
registration_basis: reviewed-principia-route-refresh
registration_commit: null
```

This is a template, not a write operation. Acceptance still requires:

1. review of the promotion packet;
2. merge of the candidate snapshot;
3. replacement of the route entry in the registry;
4. recording the exact Atlas registration commit;
5. rebuilding the complete evidence registry catalog;
6. passing bridge, drift, promotion, registry, and Atlas compatibility checks.

## Current repository control

No newer refrigerator candidate is stored in Atlas at the time this gate is introduced. The focused workflow therefore uses the accepted snapshot as a zero-drift control.

Expected result:

```yaml
gate_state: no-change
decision: candidate-redundant
registry_update_eligible_after_review: false
proposed_registry_replacement: null
automatic_snapshot_acceptance: false
repository_mutation: false
```

Changed candidates are exercised through deterministic regression tests rather than a fabricated Principia revision.

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

The gate validates evidence identity and review readiness. It does not validate the complete learner experience, authorize publication, or claim educational effectiveness.
