# Phase 4 Workstream 2 — Pinned Chromium Browser Evidence

## Status

Initial evidence candidate.

```yaml
phase: 4
workstream: 2
mode: interactive-experience-foundation
state: browser-evidence-candidate
engine: chromium
playwright: 1.62.0
production_frontend_architecture_selected: false
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Purpose

Use one pinned Chromium engine as a controlled measurement instrument to determine whether the accepted local reference shell is keyboard-operable, semantically inspectable, deterministic under deep links and browser history, complete without graph visualization, explicit under failure, responsive at two bounded viewports, and independent of external network services.

This is automated browser evidence. It is not human accessibility verification, accessibility certification, production browser support, or a frontend architecture decision.

## Toolchain

```yaml
package: playwright
version: 1.62.0
browser_install: chromium-only
ci_operating_system: ubuntu-24.04
node_major: 22
workers: one-controlled-runner
screenshots_authoritative: false
```

The package is pinned exactly. The initial CI run generates the npm lockfile; the final candidate must commit that lockfile and switch from `npm install` to `npm ci`.

## Evidence contracts

The runner emits:

- `atlas-phase4-browser-evidence-manifest/0.1`;
- `atlas-browser-workflow-evidence/0.1`;
- `atlas-browser-accessibility-report/0.1`;
- `atlas-browser-network-report/0.1`;
- `atlas-browser-failure-evidence/0.1`;
- `atlas-phase4-browser-evidence-report/0.1`.

Every file has a semantic `report_digest`. The overall report binds each child file by filename, byte count, artifact SHA-256, and semantic digest.

## Browser matrix

```yaml
desktop:
  width: 1440
  height: 1000
  reduced_motion: no-preference
mobile:
  width: 390
  height: 844
  reduced_motion: reduce
```

This is a bounded matrix, not complete device certification.

## Workflow evidence

The runner exercises all eight accepted view kinds:

1. entity;
2. provenance;
3. retrieval;
4. filter;
5. research trail;
6. advisory candidate;
7. Principia reference;
8. impact warning.

For every view, the record binds:

- exact workflow ID and revision;
- semantic keyboard input;
- visible focus result;
- expected and observed hash route;
- observed heading;
- exact Atlas reference count;
- equivalent non-graph route;
- pass or fail decision.

The runner also records:

- skip-link operation;
- deterministic browser back and forward behavior;
- direct exact-revision deep-link reload;
- explicit rejection of `@latest` and unknown routes;
- all five accepted failure-state codes;
- impact-warning text;
- separate Principia status;
- offline operation after local package boot.

## Accessibility evidence

The automated report records:

- document language and title;
- banner, navigation, main, and contentinfo landmarks;
- heading levels and text;
- accessible names for all buttons;
- live and alert regions;
- skip-link focus;
- main-target focus;
- focus order across eight workflow controls and the failure control;
- visible focus checks;
- desktop and mobile horizontal overflow;
- reduced-motion scroll behavior;
- availability of all mobile workflow controls.

The report declares:

```yaml
human_verified: false
accessibility_certified: false
assistive_technology_user_reviewed: false
```

## Network evidence

A browser-context route policy records every request and allows only the exact loopback origin. Records are normalized and sorted before output.

The candidate fails if:

- any external request is attempted;
- a remote font, image, script, stylesheet, analytics endpoint, credential, or cloud service is used;
- request records are missing or non-loopback;
- the external request count is not zero.

## Failure evidence

The browser verifies:

- five accepted failure states remain visible;
- unknown and malformed routes produce an explicit route failure;
- implicit `latest` is rejected;
- no silent fallback to the first view occurs;
- canonical and lifecycle mutation remain false.

## Bounded shell corrections

The browser requirements expose two static-shell defects that are corrected in this candidate:

1. the main skip-link target previously suppressed its visible outline;
2. unknown hash routes previously fell back silently to the first view.

The corrections:

- preserve the existing exact-revision interaction contracts;
- preserve generated shell data and its build digest;
- add semantic labels to dynamic panels;
- expose the runtime status as an atomic status region;
- show an explicit route error with no fallback or implicit revision substitution.

Because the accepted Workstream 1 baseline pins static asset bytes, the final candidate must add a versioned compatibility-patch baseline that binds old and new asset hashes without rewriting the historical accepted evidence.

## Determinism

CI runs the full browser evidence process twice against the same generated package and requires byte-identical evidence directories.

Authoritative records exclude:

- timestamps;
- action durations;
- animation frames;
- opaque temporary paths;
- screenshots;
- unordered request records;
- browser test-runner timing output.

## Independent validation

The Python validator independently checks:

- every evidence contract and digest;
- overall child-file bindings;
- pinned engine and viewport policy;
- exact-revision workflow IDs;
- expected and observed route equality;
- view-kind coverage;
- visible focus and non-graph routes;
- accessibility limitations;
- zero external requests;
- explicit failure behavior;
- all non-mutation boundaries.

Negative tests modify evidence, recompute valid semantic digests and parent file bindings, and still require rejection for:

- external requests;
- implicit `latest`;
- false human-verification claims;
- removal of non-graph equivalence.

## Evidence process

The first exact-head run is exploratory. It may expose browser behavior, shell defects, generated lockfile details, or compatibility-baseline requirements.

Before merge, the candidate must:

1. commit the generated package lock;
2. use `npm ci`;
3. pin the exact Chromium version;
4. pin all six evidence files and overall report identities;
5. pin old and new shell static-asset hashes through a compatibility patch;
6. make Workstream 1 closure and reference-shell regressions pass without changing their historical evidence meaning;
7. pass the complete Atlas platform and end-to-end matrix on one immutable final head.

## Boundary

This candidate does not:

- claim human accessibility verification or conformance certification;
- select a production browser or frontend framework;
- add analytics, accounts, cloud services, or deployment architecture;
- alter canonical content or accepted retrieval judgments;
- activate live Principia integration;
- grant browser state lifecycle, merge, review, promotion, or release authority;
- make screenshots authoritative.
