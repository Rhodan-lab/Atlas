# Content Contract Versioning and Migration Policy

## Status

**Provisional Phase 0 policy.** It is sufficiently specific for reference fixtures, but remains open to revision until the Phase 0 completion report is accepted.

## Separate version domains

Atlas versions three things independently:

1. **Authoring contract** — the canonical Markdown semantics and required fields.
2. **Derived data contract** — database, index, JSON, or portable runtime formats.
3. **Application release** — software packaging and user-facing behavior.

A software release does not automatically change authored knowledge. A storage migration does not automatically change the authoring contract.

## Initial authoring version

The first reference corpus uses:

```yaml
contract: atlas-content/0.1
```

Version `0.1` is an experimental foundation contract. It is not guaranteed stable, but every change must still preserve history and provide migration notes.

## Version semantics

The authoring contract follows semantic intent:

- **patch** — clarifies wording or validation without changing valid meaning;
- **minor** — adds optional capability or a migratable entity or field;
- **major** — changes identity, meaning, lifecycle, relation semantics, required fields, or provenance in a way that can invalidate existing authored content.

During `0.x`, breaking changes may occur between minor versions, but they still require an explicit migration plan and compatibility report.

## Required contract header

Every canonical item includes:

```yaml
contract: atlas-content/0.1
```

A validator must reject an unsupported version rather than guessing how to interpret it.

## Migration invariants

A migration must preserve:

- canonical identity or a traceable identity mapping;
- authored statement meaning and qualifiers;
- source and evidence locators;
- evidence roles;
- review status tied to the exact reviewed revision;
- uncertainty and limitations;
- revision and supersession history;
- links to dependent items;
- authorship and reviewer information where present.

A migration may not silently:

- merge distinct claims;
- split a claim without recording the mapping;
- turn prose links into canonical relations;
- promote lifecycle status;
- discard unknown fields;
- replace a precise uncertainty measure with a generic confidence label;
- rewrite restricted evidence as if it were redistributable.

## Migration record

Each migration has a durable record:

```yaml
migration:
  id: migration:atlas-content-0.1-to-0.2
  from: atlas-content/0.1
  to: atlas-content/0.2
  created: 2026-07-26
  status: draft
  reversible: true
```

The migration document explains:

- why the change is needed;
- which entities and fields are affected;
- deterministic transformation rules;
- ambiguous cases requiring human review;
- identity mappings;
- validation before and after migration;
- rollback procedure;
- known losses or changes in interpretation.

## Migration classes

### Mechanical migration

A deterministic transformation that preserves meaning without editorial judgment.

Examples:

- renaming a metadata key;
- normalizing a date representation;
- moving a field to a nested object while retaining its value.

### Semantic migration

A transformation that may change interpretation or requires item-level decisions.

Examples:

- splitting compound claims;
- changing relation direction or meaning;
- separating evidence from a concept-level citation;
- revising a confidence model.

Semantic migrations require human review and cannot automatically retain `reviewed` status unless the review policy explicitly allows it.

## Compatibility fixtures

Each contract version includes:

- minimal valid records for every entity;
- complete valid vertical slices;
- invalid records with expected diagnostic codes;
- migration input and expected output;
- identity-stability cases;
- unknown-field cases;
- unsupported-version cases;
- round-trip checks where applicable.

## Deprecation window

Once Atlas reaches a stable `1.x` authoring contract, a new implementation should read at least the current major version and the immediately previous major version, or provide a bundled migration tool. This requirement may be revised through an ADR based on actual distribution and maintenance cost.

## Derived contract rule

A derived format declares both its own version and the authoring contract used to generate it:

```json
{
  "derivedContract": "atlas-runtime/0.1",
  "sourceContract": "atlas-content/0.1"
}
```

Derived formats are disposable. Their migrations must never become the only record of an authored semantic change.

## Change procedure

1. Expose the limitation through a real fixture.
2. Propose the contract change and classify its compatibility impact.
3. Update ontology, editorial policy, vocabulary, and examples together.
4. Write migration and rollback rules.
5. Add valid, invalid, and migration fixtures.
6. Run cross-document consistency review.
7. Record the decision and affected review statuses.
8. Publish a compatibility report before adoption.
