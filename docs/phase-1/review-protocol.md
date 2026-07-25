# Atlas Review Protocol — `atlas-review/0.1`

## Status

Accepted Phase 1 draft for executable review fixtures. This protocol governs review records, not authored knowledge entities.

## Purpose

A review record captures accountable judgment about an exact canonical entity revision. It must remain distinguishable from:

- machine diagnostics;
- source metadata verification;
- AI-assisted analysis;
- editorial maintenance;
- independent domain or professional review.

## Record shape

```json
{
  "contract": "atlas-review/0.1",
  "id": "review:domain:feedback-r1:2026-07-26",
  "entity": {
    "id": "claim:en:one-delayed-feedback-model-can-oscillate",
    "revision": 1,
    "content_digest": "sha256:optional"
  },
  "review_type": "domain",
  "reviewer": {
    "display_name": "Reviewer name or stable role",
    "kind": "human",
    "independence": "independent",
    "qualification": "control systems",
    "accountable": true,
    "conflicts": []
  },
  "completed_at": "2026-07-26",
  "review_horizon": null,
  "outcome": "pass",
  "findings": [],
  "summary": "Bounded conclusion for this revision.",
  "permits_promotion": true
}
```

## Required top-level fields

- `contract`
- `id`
- `entity`
- `review_type`
- `reviewer`
- `completed_at`
- `outcome`
- `findings`
- `summary`
- `permits_promotion`

Unknown fields are rejected unless introduced by a contract revision.

## Identity

Review IDs use:

```text
review:<review-type>:<stable-slug>:<date-or-sequence>
```

A review record is immutable after acceptance. Corrections create a new review record that supersedes the earlier record with explicit linkage.

## Exact target

`entity.id` and `entity.revision` are mandatory.

A review of revision 1 cannot authorize revision 2. A content digest is recommended for signed or exported review packets but is not treated as semantic proof.

## Review types

Initial review types:

- `structural`
- `editorial`
- `source`
- `domain`
- `methodological`
- `reproducibility`
- `ethical`
- `translation`
- `legal-context`
- `conflict`

A review record covers exactly one review type. This avoids one broad review silently claiming competence across unrelated areas.

## Reviewer kinds

- `machine`
- `ai-assisted`
- `human`

## Independence

- `internal`
- `independent`
- `not-applicable`

Independence describes relationship to the authored material and project, not whether a reviewer is intelligent or technically skilled.

## Accountable reviewer

`reviewer.accountable` is `true` only when a human accepts responsibility for the review record.

Machine and AI-assisted records must set it to `false`. They may provide evidence and findings but cannot impersonate accountable judgment.

## Conflicts

`reviewer.conflicts` is always present, including when empty.

Examples:

- authored the entity;
- employed by a platform studied;
- financial relationship;
- access to non-public data;
- direct project-maintainer role;
- prior public position on the disputed issue.

A disclosed conflict does not automatically invalidate review. The promotion policy determines whether additional independent review is required.

## Outcomes

- `pass`
- `pass-with-minor-findings`
- `changes-required`
- `blocked`
- `not-applicable`

`pass-with-minor-findings` permits promotion only when every remaining finding is `minor` or `info` and explicitly accepted under policy.

## Finding shape

```json
{
  "id": "finding:feedback:stability-definition",
  "severity": "major",
  "status": "open",
  "summary": "The stability definition is too broad for the modeled recurrence.",
  "rationale": "Bounded periodic behavior and asymptotic stability are not equivalent.",
  "affected_fields": ["definition", "claim.statement"],
  "suggested_action": "Narrow the terminology before promotion."
}
```

Required finding fields:

- `id`
- `severity`
- `status`
- `summary`
- `rationale`

Optional:

- `affected_fields`
- `suggested_action`
- `references`
- `resolution_note`

## Finding severity

- `critical` — authority, safety, integrity, or meaning failure requiring immediate block;
- `major` — material accuracy, scope, method, provenance, or interpretation defect;
- `minor` — non-material correction or clarity improvement;
- `info` — observation or future improvement.

## Finding status

- `open`
- `resolved`
- `accepted-risk`
- `not-applicable`

Critical findings cannot be accepted as risk for promotion. Major findings require resolution or a documented contested-state decision; they cannot silently disappear.

## Promotion declaration

`permits_promotion` records the reviewer’s bounded recommendation. It does not itself promote the entity.

The Phase 1 promotion gate independently evaluates:

- required review coverage;
- reviewer authority;
- exact revision;
- conflicts;
- review horizon;
- staleness;
- open findings;
- lifecycle transition requirements.

## Review horizons

Time-sensitive reviews include `review_horizon` as an ISO date.

Examples:

- legal-context interpretation;
- platform behavior;
- policy guidance;
- rapidly changing evidence;
- translation tied to an evolving source revision.

An expired review becomes insufficient for promotion until renewed or explicitly found unaffected.

## AI-assisted records

AI-assisted review records:

- set reviewer kind to `ai-assisted`;
- set independence to `internal` or `not-applicable`;
- set accountable to `false`;
- set permits promotion to `false`;
- identify model and procedure in the summary or metadata;
- preserve uncertainty and candidate findings.

They may accelerate review preparation but never satisfy accountable human review requirements.

## Supersession

A corrected review record may include:

```json
{
  "supersedes": "review:domain:feedback-r1:2026-07-26"
}
```

Supersession preserves the prior record. Deletion is reserved for secrets, personal data, or material that should never have been committed.

## Review record migration

Future versions must preserve:

- review identity;
- target entity and revision;
- reviewer kind, independence, accountability, and conflicts;
- outcome;
- findings and their resolution history;
- completed date and horizon;
- promotion recommendation;
- supersession chain.

No migration may convert AI-assisted or machine review into human accountability.
