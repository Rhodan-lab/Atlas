# Revision Impact and Staleness Policy

## Status

**Accepted for `atlas-content/0.1`.** Automated propagation creates review obligations and diagnostic states; it does not decide the final semantic effect.

## Core distinction

Atlas separates:

- **change detection** — an input revision or status changed;
- **possible impact** — a dependency may require review;
- **confirmed impact** — a reviewer determined how meaning or confidence changed;
- **supersession** — a newer item replaces an older item for a stated purpose.

Automation may reliably detect the first two. Human or domain-specific review is required for the third.

## Dependency classes

### Material dependency

The target materially contributes to the subject’s meaning, evidence, inference, model, or conclusion.

Examples:

- evidence supports a claim;
- a synthesis is derived from a claim;
- a claim is model-derived;
- an argument uses a claim as a premise;
- a translation targets a source revision;
- a concept definition depends on a prerequisite definition.

A material dependency can create staleness.

### Navigational dependency

The link aids discovery but does not materially determine the subject’s conclusion.

Examples:

- an illustrative analogy;
- a related reading link;
- a non-material contextual source.

Navigational changes do not automatically mark the subject stale, though they may create a low-severity review note.

## Staleness states

Staleness is separate from lifecycle status.

- `current` — no known dependency change requires review;
- `possibly-stale` — automated rules detected a potentially material upstream change;
- `review-required` — policy or reviewer determined reassessment is necessary;
- `confirmed-stale` — current text or conclusion relies on superseded, invalid, or materially changed input;
- `unaffected` — review confirmed that an upstream change does not alter this revision;
- `updated` — the item was revised and its dependency assessment is current.

A reviewed item can become `possibly-stale` without being retracted or automatically returned to `draft`.

## Automatic propagation triggers

The following upstream events create at least `possibly-stale` on material dependents:

- source becomes corrected, retracted, deprecated, or unavailable;
- evidence changes value, locator, access, method, or appraisal materially;
- evidence relation changes from support to challenge or contradiction;
- claim statement, scope, kind, confidence rationale, or status changes;
- model assumptions, formal structure, parameters, validation, or failure modes change;
- question scope or resolution criterion changes;
- translation source revision changes;
- contract migration changes semantics or identity mapping;
- relation meaning or direction changes in the vocabulary.

## Relation-specific default impact

| Upstream relation | Default dependent state | Reason |
|---|---|---|
| evidence `supports` claim | possibly-stale | claim support changed |
| evidence `challenges` claim | possibly-stale | limitation or confidence may change |
| claim `contradicts` claim | review-required when contradiction status changes | disagreement structure changed |
| synthesis `derived-from` claim | possibly-stale | conclusion basis changed |
| claim `derived-from` model | review-required for model-semantic change | derivation may no longer hold |
| concept `prerequisite-of` concept | possibly-stale for definition change | downstream interpretation may shift |
| entity `analogous-to` entity | no automatic stale state | analogy is non-evidentiary by default |
| evidence `illustrates` concept | no automatic stale state unless central example | illustration is not support |
| item `supersedes` item | review-required for current dependents of old item | current reference may need replacement |

Projects may tighten these defaults but may not suppress material-impact visibility.

## Impact event record

```yaml
impact_event:
  id: impact:claim-feedback-2026-07-26
  trigger_entity: evidence:en:new-feedback-result
  trigger_revision: 2
  trigger_change: relation-role-changed
  dependent: claim:en:delay-contributed-to-oscillation
  detected_at: 2026-07-26
  state: possibly-stale
  rule: evidence-support-change
```

Impact events are derived reports. The final review finding belongs to the dependent entity’s review history.

## Reviewer impact assessment

A reviewer records:

```yaml
impact_review:
  event: impact:claim-feedback-2026-07-26
  outcome: unaffected
  rationale: The changed evidence was illustrative and not used in the confidence rationale.
  reviewed_by:
    - reviewer:example-domain-01
  reviewed_at: 2026-07-27
```

Possible outcomes:

- `unaffected`
- `editorial-update`
- `confidence-change`
- `scope-change`
- `claim-revision`
- `status-change`
- `synthesis-rebuild`
- `translation-update`
- `unable-to-assess`

## Synthesis impact

A synthesis enters `review-required` when:

- a material claim is retracted or confirmed stale;
- its evidence-selection method no longer matches available evidence;
- a central contradiction is resolved or newly introduced;
- a model producing a material conclusion changes;
- the addressed question scope changes;
- a normative value premise changes;
- a legal or policy source is amended in a way relevant to its conclusion.

Minor wording changes to a non-material source do not require full synthesis review.

## Translation impact

When a source-language item changes:

- translation becomes `possibly-stale` automatically;
- translation review compares semantic diff, not only text diff;
- metadata-only changes can be marked unaffected;
- material changes require a new translation revision;
- reviewed status refers to the new translated revision only after review.

## Source correction and retraction

### Correction

- preserve original source version;
- add corrected version or status;
- mark dependent evidence possibly stale;
- assess whether evidence locator or interpretation changes.

### Retraction

- source remains in provenance;
- dependent evidence becomes `review-required` or `confirmed-stale` depending on reason;
- claims do not automatically become false, but they lose that support until reassessed;
- syntheses using the source materially become review-required;
- public views display the retraction relationship prominently.

## Migration impact

A mechanical migration with verified semantic equivalence may retain review status and mark items `unaffected` through a reproducibility report.

A semantic migration:

- marks affected items review-required;
- records identity mappings;
- does not automatically inherit review status;
- reports downstream dependencies before adoption.

## Impact traversal limits

To avoid meaningless alert storms:

- propagation follows material dependencies by default;
- each event retains the path explaining why the dependent was flagged;
- duplicate paths are consolidated without losing provenance;
- cycles are reported explicitly;
- configurable depth may control display, but not hide critical material paths;
- low-severity navigational changes are grouped separately.

## Human judgment boundary

Automation must not claim:

- that a changed claim makes every synthesis false;
- that unchanged wording means unchanged meaning;
- that a numerical confidence update can be calculated universally;
- that a replacement source is equivalent;
- that a legal amendment has one uncontested interpretation;
- that translation remains faithful after a source change.

## Validation fixtures

Phase 1 must include:

- supporting evidence corrected without changing claim outcome;
- supporting evidence retracted, causing review-required;
- model parameter change affecting one derived claim but not another;
- concept definition change propagating through prerequisite links;
- analogy change that does not trigger material staleness;
- source-language revision marking translation stale;
- mechanical migration retaining review;
- semantic migration requiring new review;
- dependency cycle with deterministic reporting;
- synthesis with one material and one non-material claim change.

## Exit criterion

This policy is mature enough for Phase 0 when every reference slice identifies material dependencies and revision triggers, and reviewers can explain why a dependent was or was not flagged without reading implementation code.
