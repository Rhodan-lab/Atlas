# Principia evidence runtime preflight v1

## Purpose

The evidence runtime preflight automatically answers a practical maintenance question:

> Does this candidate Atlas canonical corpus change any exact evidence revision used by an accepted Principia route?

It compares two complete compiled Atlas runtimes:

1. the exact pull-request base runtime;
2. the candidate runtime produced by the proposed change.

The preflight then maps detected runtime differences through the accepted Principia evidence impact index.

This is different from the evidence change simulator. The simulator evaluates a hand-authored hypothetical scenario. The preflight derives findings from actual before-and-after canonical runtime state.

## Contracts

The report contract is:

```text
atlas-principia-evidence-runtime-preflight/0.1
```

Its source dependency index remains:

```text
atlas-principia-evidence-impact-index/0.1
```

Both runtimes must independently pass the strict Atlas runtime validator before comparison begins.

## Detected changes

### Same-revision mutation

An accepted exact revision is immutable for preflight purposes. The following candidate changes block the affected Principia route:

- canonical path changed;
- canonical source SHA-256 changed;
- canonical body SHA-256 changed.

Finding:

```text
immutable-exact-revision-changed
```

Decision:

```text
preflight-blocked
```

A correction must be represented as a new reproducible revision rather than silently rewriting the accepted exact revision.

### Exact revision removal

When the candidate runtime no longer contains an accepted exact revision, the dependent route is blocked.

Finding:

```text
exact-revision-removed
```

### New higher revision

When the candidate adds a revision higher than the accepted revision, the exact accepted revision still resolves, but the dependent route must be reviewed for possible refresh.

Finding:

```text
superseding-revision-added
```

Decision:

```text
preflight-revalidation-required
```

The preflight does not automatically update the Principia snapshot or evidence registry.

### Lifecycle and staleness changes

The preflight recognizes lifecycle changes on accepted exact revisions:

```text
lifecycle-retracted
lifecycle-deprecated
lifecycle-status-changed
staleness-review-required
staleness-confirmed-stale
staleness-changed
```

Retraction blocks affected routes. Deprecation, review-required, confirmed-stale, and other lifecycle transitions require route revalidation unless a stronger immutable-revision blocker is also present.

In a normally compiled canonical change, editing lifecycle metadata on the same exact revision also changes the source hash. The report therefore preserves both semantic and immutable-revision findings, with blocked status taking precedence.

### Unrelated canonical changes

A candidate runtime may differ from the baseline without touching any accepted Principia evidence dependency.

In that case:

```text
runtime_changed: true
changed_accepted_exact_reference_count: 0
decision: preflight-clear
```

## Decisions

```text
preflight-clear
preflight-revalidation-required
preflight-blocked
```

Precedence is:

```text
blocked > revalidation-required > clear
```

The report includes baseline and projected route states, newly affected routes, escalated routes, and newly blocked routes.

## Pull-request use

The focused workflow checks out the exact pull-request base commit into `baseline-atlas/` and compares it with the candidate checkout.

Equivalent local command:

```bash
python -m tools.phase2_kernel.evidence_preflight_cli \
  --baseline-canonical-root baseline-atlas/content/canonical \
  --candidate-canonical-root content/canonical \
  --registry baseline-atlas/content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json \
  --review-root baseline-atlas/content/reviews/ai \
  --repository-root baseline-atlas \
  --output /tmp/principia-evidence-preflight.json
```

The baseline registry, accepted snapshots, and review records are taken from the exact base checkout. This prevents the candidate from redefining its own accepted evidence baseline during canonical preflight.

## Runtime-file use

Precompiled runtimes may be supplied directly:

```bash
python -m tools.phase2_kernel.evidence_preflight_cli \
  --baseline-runtime /tmp/atlas-base-runtime.json \
  --candidate-runtime /tmp/atlas-candidate-runtime.json \
  --impact-index /tmp/principia-evidence-impact.json \
  --output /tmp/principia-evidence-preflight.json
```

## Report identity

The report binds:

- baseline runtime contract;
- baseline source digest;
- baseline rendered-runtime SHA-256;
- candidate runtime contract;
- candidate source digest;
- candidate rendered-runtime SHA-256;
- accepted exact-reference findings;
- route-level projected impact.

Repeated runs over identical inputs are byte-identical.

## Current repository control

This capability adds no canonical changes. Comparing the current pull-request base corpus with the candidate corpus must therefore produce:

```yaml
runtime_changed: false
accepted_exact_reference_count: 2
changed_accepted_exact_reference_count: 0
immutable_violation_count: 0
removed_exact_reference_count: 0
superseding_revision_count: 0
lifecycle_change_count: 0
newly_affected_route_count: 0
newly_blocked_route_count: 0
decision: preflight-clear
```

The regression suite covers real and synthetic changes. Synthetic cases are contract tests, not claims that those maintenance events occurred in Atlas.

## Preserved boundaries

```yaml
live: false
status_inheritance: prohibited
automatic_snapshot_acceptance: false
automatic_registry_update: false
automatic_status_change: false
automatic_release_action: false
canonical_mutation: false
repository_mutation: false
principia_publication_status_granted: false
learner_effectiveness_claimed: false
```

The preflight reads, validates, compares, and reports. It does not alter either runtime, canonical content, review authority, the evidence registry, Principia, or release state.
