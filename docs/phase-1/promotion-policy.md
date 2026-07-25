# Phase 1 Promotion and Lifecycle Policy

## Purpose

This policy determines when an exact Atlas entity revision may move from `draft` or `in-review` to another lifecycle state. It prevents status changes based on parsing success, prestige, one reviewer, or AI output.

## Promotion is a separate decision

A review record may recommend promotion. Only the promotion gate may determine whether all requirements are satisfied.

A valid promotion decision records:

- entity ID and exact revision;
- current and requested lifecycle state;
- required review types;
- review records used;
- missing or stale coverage;
- unresolved findings;
- conflicts and authority limitations;
- decision and reasons;
- decision date;
- actor accepting the transition.

## Reviewer authority classes

### Machine-satisfiable

Machine review may satisfy:

- structural conformance;
- deterministic reference integrity;
- exact arithmetic or reproducibility fixtures when the procedure is fully specified;
- migration invariants;
- staleness computation.

### Accountable internal human

An accountable internal human may satisfy:

- editorial review;
- source-locator verification;
- conflict disclosure review;
- project-specific scope and usability review.

Internal review cannot be presented as independent.

### Independent qualified human

Independent qualified human review is required for:

- domain accuracy of factual or explanatory claims;
- methodological validity of empirical causal, correlational, or model-to-world inference;
- ethical review of normative claims and recommendations;
- legal-context interpretation;
- translation equivalence for reviewed translations.

A project may require additional independent reviews when conflicts are material.

## Required review types by entity

### Source

- structural
- source

### Evidence

- structural
- source
- methodological when empirical interpretation, measurement, sampling, or transformation is material
- reproducibility when generated or derived

### Claim

Always:

- structural
- editorial

Additionally:

- source and domain for factual, descriptive, definitional, or explanatory claims;
- source, domain, and methodological for causal or correlational claims;
- domain, methodological, and reproducibility for model-derived claims;
- ethical for normative claims;
- translation for translated claims;
- legal-context when a legal proposition or interpretation is material.

### Concept

- structural
- editorial
- domain
- translation when translated

### Model

- structural
- editorial
- domain
- methodological
- reproducibility when executable or used for derived evidence
- translation when translated

### Question

- structural
- editorial
- domain when the scope presupposes contested terminology or factual boundaries
- translation when translated

### Synthesis

- structural
- editorial
- source
- domain
- methodological when empirical or model-based inference is material
- ethical when normative claims or recommendations are included
- legal-context when law or regulation is interpreted
- translation when translated

## State transitions

### `draft` → `in-review`

Required:

- structural validation passes;
- review scope is frozen to an exact revision;
- required review types are calculated;
- reviewer conflicts are collected.

### `in-review` → `reviewed`

Required:

- every required review type has acceptable authority;
- every record targets the exact revision;
- all critical and major findings are resolved;
- no required review is stale or expired;
- translations match the current source revision;
- outcome is pass or pass-with-minor-findings;
- an accountable human accepts the promotion decision.

### any current state → `contested`

Use when credible, materially different positions remain unresolved.

Required:

- disagreement summary;
- competing claims or interpretations;
- evidence and review records for each material position;
- unresolved questions;
- reason a single reviewed synthesis would mislead.

Contested does not mean invalid. It means disagreement must remain visible.

### current state → `deprecated`

Use when the entity should no longer be used as current guidance but is retained for provenance.

Required:

- reason;
- effective date;
- replacement or explicit statement that none exists;
- affected dependent entities;
- migration or navigation guidance;
- accountable human decision.

### current state → `retracted`

Use for serious error, integrity failure, or invalid authority.

Required:

- reason and evidence;
- effective date;
- affected dependents;
- explicit prohibition on current evidentiary use;
- replacement when available;
- accountable human decision;
- preserved historical record.

Retraction is not deletion.

## Finding rules

Promotion to reviewed is blocked when:

- any critical finding is open or accepted-risk;
- any major finding is open;
- a major finding is marked resolved without a resolution note;
- required review coverage is missing;
- a review targets another revision;
- a required independent review is supplied only by internal, machine, or AI-assisted work;
- a review horizon has expired;
- the target entity is `possibly-stale`, `review-required`, or `confirmed-stale`;
- a translation source revision differs from the reviewed source revision.

Minor findings may remain open only when:

- the review outcome is pass-with-minor-findings;
- the promotion decision lists them;
- they do not alter meaning, scope, evidence, or authority.

## Conflict rules

A reviewer always declares conflicts, including an empty list.

A material conflict requires one of:

- additional independent review;
- reduced authority for that review record;
- contested status;
- explicit block.

A conflict cannot be resolved by deleting it from the record.

## AI and machine boundary

Machine and AI-assisted records may never provide accountable human acceptance.

They may block promotion by finding a defect. They may not authorize promotion where human review is required.

## Time-sensitive content

Legal, policy, platform, rapidly changing empirical, and translated material uses review horizons.

When a horizon expires:

- the review record remains historical;
- current promotion coverage becomes incomplete;
- dependent syntheses may become `possibly-stale` or `review-required`;
- renewal may confirm that the entity is unaffected.

## Promotion output

The gate emits one of:

- `eligible`
- `blocked`
- `contested-path-required`
- `deprecated-path-required`
- `retracted-path-required`

It also emits deterministic reasons and must not change authored files automatically.

## Reopening foundation decisions

If a valid review cannot be represented without loss of meaning, Phase 1 records a contract-gap fixture. Only then may the relevant Phase 0 decision be reopened through an ADR or foundation revision.
