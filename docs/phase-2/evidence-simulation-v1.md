# Principia Evidence Change Simulator v1

## Purpose

The simulator previews the effect of a proposed Atlas evidence change on accepted Principia learner routes before canonical content is edited.

The evidence impact index answers which accepted routes currently depend on an Atlas entity or exact revision. The simulator adds the missing prospective layer: maintainers can describe a proposed supersession, review-state change, staleness finding, deprecation, or retraction and receive one deterministic route-impact report.

The scenario is an overlay. It does not edit the Atlas runtime, canonical files, lifecycle state, review records, accepted evidence registry, or Principia.

## Contracts

Scenario:

```text
atlas-principia-evidence-impact-scenario/0.1
```

Simulation report:

```text
atlas-principia-evidence-impact-simulation/0.1
```

Current repository control:

```text
content/fixtures/phase2_bridge/evidence-impact-scenario.none.v01.json
```

The repository control contains no proposed change. It exists to prove deterministic integration against the current accepted evidence registry without inventing a maintenance decision.

## Scenario shape

```json
{
  "contract": "atlas-principia-evidence-impact-scenario/0.1",
  "live": false,
  "status_inheritance": "prohibited",
  "changes": [
    {
      "entity_id": "model:en:delayed-correction-recurrence",
      "revision": 2,
      "operation": "supersede",
      "new_revision": 3,
      "reason": "proposed corrected model revision"
    }
  ]
}
```

Every target is an exact Atlas entity revision already referenced by at least one accepted Principia route.

## Supported operations

### `supersede`

Simulates the existence of a newer revision. `new_revision` is required and must be greater than the accepted revision.

Result:

```yaml
resolution: superseded
required_action: revalidate
impact_state: revalidation-required
```

### `mark-review-required`

Simulates a lifecycle or review finding that requires renewed evidence review.

```yaml
resolution: review-required
required_action: revalidate
impact_state: revalidation-required
```

### `mark-confirmed-stale`

Simulates a confirmed staleness finding.

```yaml
resolution: confirmed-stale
required_action: revalidate
impact_state: revalidation-required
```

### `deprecate`

Simulates deprecation of the exact accepted revision.

```yaml
resolution: deprecated
required_action: revalidate
impact_state: revalidation-required
```

### `retract`

Simulates retraction of the exact accepted revision.

```yaml
resolution: retracted
required_action: block-release
impact_state: blocked
```

## Validation rules

The simulator requires:

- `live: false`;
- `status_inheritance: prohibited`;
- canonical Atlas entity IDs;
- positive exact revisions;
- non-empty reasons;
- one operation per exact target;
- `new_revision` only for `supersede`;
- a superseding revision greater than the accepted revision;
- an exact target present in the accepted Principia impact index.

Unknown fields, unsupported operations, duplicate or conflicting targets, malformed revisions, and targets with no accepted dependency fail closed.

## Output

The report records:

- SHA-256 of the source impact index;
- SHA-256 of the normalized scenario;
- every applied exact-revision change;
- before and simulated impact states;
- affected route IDs per change;
- baseline affected routes;
- simulated affected routes;
- newly affected routes;
- routes whose severity escalated;
- newly blocked routes;
- a complete simulated impact index;
- explicit no-mutation boundaries.

## Decisions

```text
simulation-clear
simulation-revalidation-required
simulation-blocked
```

`simulation-clear` means the scenario contains no change or does not raise the state of any targeted accepted dependency.

`simulation-revalidation-required` means at least one targeted dependency requires review, but none is blocked.

`simulation-blocked` means at least one targeted dependency is blocked under the scenario.

These are simulation results, not lifecycle actions or release decisions.

## Commands

Run the honest repository control:

```bash
python -m tools.phase2_kernel.evidence_simulation_cli \
  --output /tmp/principia-evidence-simulation.json
```

Run an explicit scenario:

```bash
python -m tools.phase2_kernel.evidence_simulation_cli \
  --scenario /path/to/proposed-scenario.json \
  --output /tmp/principia-evidence-simulation.json
```

Reuse a previously compiled impact index:

```bash
python -m tools.phase2_kernel.evidence_simulation_cli \
  --impact-index /tmp/principia-evidence-impact.json \
  --scenario /path/to/proposed-scenario.json \
  --output /tmp/principia-evidence-simulation.json
```

Use an existing Atlas runtime:

```bash
python -m tools.phase2_kernel.cli compile \
  --output /tmp/atlas-runtime.json

python -m tools.phase2_kernel.evidence_simulation_cli \
  --runtime /tmp/atlas-runtime.json \
  --scenario /path/to/proposed-scenario.json \
  --output /tmp/principia-evidence-simulation.json
```

## Current repository control result

```yaml
change_count: 0
baseline_affected_route_count: 0
simulated_affected_route_count: 0
newly_affected_route_count: 0
newly_blocked_route_count: 0
decision: simulation-clear
```

The changed-state behavior is covered by explicit synthetic regression scenarios. Atlas does not claim that a supersession, deprecation, staleness finding, or retraction has actually occurred.

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

The simulator provides prospective dependency visibility only. A real canonical or lifecycle change still requires its normal Atlas review, versioning, provenance, and merge process.
