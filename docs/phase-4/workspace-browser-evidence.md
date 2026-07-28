# Phase 4 Workstream 3 Slice 2 — Pinned Browser Evidence Candidate

## Status

```yaml
phase: 4
workstream: 3
slice: 2
state: workspace-browser-candidate
input_authority: accepted-workspace-export-only
browser_state_authority: ephemeral-only
routes: 13
entries: 5
candidates: 2
principia_references: 1
warnings: 1
viewports: 2
external_network_allowed: false
human_verified: false
accessibility_certified: false
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
repository_mutation: false
production_frontend_architecture_selected: false
live_principia_dependency: false
```

## Purpose

This candidate collects deterministic real-browser evidence over the accepted local workspace shell. It does not change the shell, workspace export, manifest, decisions, candidates, Principia reference, warning, or authority boundary.

## Candidate evidence contracts

```yaml
workflow: atlas-workspace-browser-workflow-evidence/0.1
accessibility: atlas-workspace-browser-accessibility-report/0.1
network: atlas-workspace-browser-network-report/0.1
failure: atlas-workspace-browser-failure-evidence/0.1
manifest: atlas-phase4-workspace-browser-manifest/0.1
report: atlas-phase4-workspace-browser-report/0.1
validation: atlas-phase4-workspace-browser-validation/0.1
```

These contracts remain candidates until exact artifacts are pinned and one immutable head passes the complete Atlas regression matrix.

## Evidence coverage

The pinned Chromium runner checks:

- the accepted thirteen-route order;
- keyboard operation and visible focus for every route;
- skip navigation, landmarks, headings, accessible link and button names, status, and alert regions;
- five exact-revision decision views in accepted order;
- unresolved contradiction and duplicate candidates;
- separate fixture-only Principia status;
- visible non-mutating impact warning;
- complete text-only non-graph coverage;
- deterministic deep links, reload, browser back, and browser forward;
- explicit unknown-route refusal with the previous valid route recorded and recoverable;
- explicit missing-export failure with no fallback data;
- the optional local download with exact accepted export bytes;
- desktop `1440×1000` and mobile `390×844` viewports;
- reduced-motion behavior and no mobile horizontal overflow;
- loopback-only requests and zero external requests.

The complete evidence directory is generated twice and compared byte-for-byte. An independent Python validator verifies each record digest, child artifact SHA-256, manifest binding, report binding, counts, and authority fields. Resealed tamper tests reject external requests, download drift, false human-verification claims, and candidate resolution.

## Limitations

- Automated Chromium evidence is not assistive-technology user review, human usability review, accessibility certification, production browser support, or product readiness.
- The bounded fixture does not establish production workspace quality or corpus-scale performance.
- Browser state remains disposable and non-authoritative.
- No production framework, hosting platform, account model, cloud persistence, collaboration, live synchronization, canonical editor, or write path is selected.
