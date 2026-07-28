# Phase 4 Workstream 3 Slice 2 — Pinned Browser Evidence Candidate

## Status

```yaml
phase: 4
workstream: 3
slice: 2
state: pinned-workspace-browser-candidate
baseline_contract: atlas-phase4-workspace-browser-baseline/0.1
input_authority: accepted-workspace-export-only
browser_state_authority: ephemeral-only
routes: 13
entries: 5
candidates: 2
principia_references: 1
warnings: 1
viewports: 2
external_request_count: 0
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

This candidate collects deterministic real-browser evidence over the accepted local workspace shell. The browser remains a reader over the accepted export and manifest. It does not create a second workspace model, change accepted decisions or order, resolve candidates, inherit Principia status, or acquire canonical, review, lifecycle, release, merge, or repository authority.

## Pinned toolchain

```yaml
engine: chromium
engine_version: 151.0.7922.34
playwright_version: 1.62.0
runner: ubuntu-24.04
node: 22
python: 3.13
```

The toolchain evidence is bounded automated evidence. It is not assistive-technology user review, human usability review, accessibility certification, production browser support, or product readiness.

## Accepted input identities

```yaml
workspace_export:
  contract: atlas-research-workspace-export/0.1
  bytes: 11347
  sha256: 43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a
  report_digest: 82f08c18ae76b4b4d091fe0d8be7d54cf5d10d989443132a26e550056af3f56a
workspace_manifest:
  contract: atlas-research-workspace-manifest/0.1
  bytes: 1094
  sha256: 8240d78b29f610cb7c566dfad50432473949c5a63b9de9c522ab28751d80fd09
  report_digest: 9aefaf24b130718f284eecb5502b3c1dd144347f6fdcfc85b47d8ec6ce3fda68
```

## Workspace-shell compatibility patch

Real-browser testing found that the original skip link used `#main-content`, while the shell router treats every hash as a workspace route. Activating the skip link therefore produced an explicit unknown-route failure instead of skipping into content.

The bounded compatibility patch:

- changes the skip target to the accepted `#overview` route;
- adds a focusable content marker at the top of `<main>`;
- preserves all thirteen accepted routes;
- preserves shell data, workspace export, workspace manifest, decisions, candidates, warnings, and authority;
- changes no retrieval, interaction, lifecycle, review, or repository semantics.

```yaml
accepted_shell_pr: 52
accepted_shell_tested_head: f273c79b26d9b943a9b57a259645c8b0c6a5de48
accepted_shell_merge_commit: dcad8aaedbf9b212ed926c09bbb50690c8fae19b
patched_index_html:
  bytes: 3232
  sha256: ae7eafc4dccae669f25ed4f6e6e5bc8e81bce8dcabcc81b5d585d4d09fb5e921
shell_data:
  bytes: 5955
  sha256: a2dd3979c35cee4d081511cadf98499e325dfd22d814cae097cfd3e98f3f5c0c
  build_digest: b4aa3fab14ecc66ee602c9c40dc88b10add23d3391915a72c31968c681edcaee
shell_build_report:
  bytes: 1448
  sha256: b8b29a61495ecfc420de9324006b6f8efac455905c7b2b69f03639d995e7f932
  report_digest: f1b13c7c202f93a1682d9366fcbef5265a7ae36f335d4e10ddff71ce216e955b
```

## Pinned evidence contracts and identities

### Keyboard and workflow evidence

```yaml
contract: atlas-workspace-browser-workflow-evidence/0.1
file: workspace-browser-workflows.json
bytes: 8003
sha256: c87b3a87aeb4fc97e01af33b08b9475a5fdf65790d972128b13b39eda22a1669
report_digest: 8731d86f49f3a1baf4f52955e1b1bd9de88f7907730e75250205117a0191af59
```

### Accessibility evidence

```yaml
contract: atlas-workspace-browser-accessibility-report/0.1
file: workspace-browser-accessibility.json
bytes: 990
sha256: 359cba535d1051dd90b2ce03e3a1932eec17c9b3adabd95bbf6b5a8633eae5e5
report_digest: c3047168d5e9a737452c69babf000caa7d2c2a89ae267127d1426296a921bf57
```

### Network evidence

```yaml
contract: atlas-workspace-browser-network-report/0.1
file: workspace-browser-network.json
bytes: 17517
sha256: 110e7baa552e0a41c0912ff116c79d51e6e4b6d68bf77f1080f18587e4d0a9cd
report_digest: 1de7665443a296e1b81443d8fce8021640e0aaf52807259ced0bd52932cb490d
request_count: 120
external_request_count: 0
```

The 120 recorded requests are bounded loopback requests produced by repeated fresh keyboard traversals, direct-link and history checks, mobile coverage, and the explicit missing-artifact test. One loopback export request is deliberately blocked by the test harness. No remote asset, credential, analytics endpoint, cloud service, or external request is used.

### Failure evidence

```yaml
contract: atlas-workspace-browser-failure-evidence/0.1
file: workspace-browser-failures.json
bytes: 1145
sha256: b41c10299e0b3998f4d3c5db6d59972f57f38fd2f47cb4105a67683b657f4bcb
report_digest: 205915d16f6cf5009b04fb3cf404813d49bbdd35fba1640b174d4bc118d2603d
```

### Evidence manifest

```yaml
contract: atlas-phase4-workspace-browser-manifest/0.1
file: workspace-browser-manifest.json
bytes: 2688
sha256: 1515b645b7608ae26391f19c231169bc0567d6f5bdf518f8649119bbc5590e2e
report_digest: ef7a22a6be1f8c46b706b894bc44a10ae88a75b2e4a8e72695d9726e373f0131
```

### Evidence report

```yaml
contract: atlas-phase4-workspace-browser-report/0.1
file: workspace-browser-report.json
bytes: 2281
sha256: a1f259d1cbfc40d87311a5955e6fe77f932e652b3e8ccfad19d12f629c5103f2
report_digest: 971c44ef7863d313dceffc7356187b94a15d6543e346654cbf6eadc116213311
```

### Independent validation

```yaml
contract: atlas-phase4-workspace-browser-validation/0.1
file: phase4-workspace-browser-validation.json
bytes: 523
sha256: 8aa93a3c9240efa117f7a167736722c65e2ea905bcf04a1f77173d1969617591
decision: valid-workspace-browser-candidate
report_digest: 971c44ef7863d313dceffc7356187b94a15d6543e346654cbf6eadc116213311
```

## Evidence coverage

The pinned Chromium runner proves:

1. the accepted thirteen-route order;
2. keyboard-only activation and visible focus for every route;
3. route-safe skip navigation, landmarks, heading hierarchy, names, status, and alert regions;
4. five exact-revision decision views in accepted order;
5. unresolved contradiction and duplicate candidates;
6. separate fixture-only Principia status;
7. visible non-mutating impact warning;
8. complete text-only non-graph coverage;
9. deterministic deep links, reload, browser back, and browser forward;
10. explicit unknown-route refusal with the previous valid route recorded and recoverable;
11. explicit missing-export failure with no fallback data;
12. local download byte identity with the accepted export;
13. desktop `1440×1000` and mobile `390×844` viewports;
14. reduced-motion behavior and no mobile horizontal overflow;
15. loopback-only networking and zero external requests.

The complete evidence directory is generated twice and compared byte-for-byte. The independent Python validator verifies every record digest, child artifact SHA-256, manifest binding, report binding, count, and authority field. Resealed tamper tests reject external requests, download drift, false human-verification claims, and candidate resolution.

## Baseline and acceptance boundary

The machine-readable baseline is `content/fixtures/phase4_workspace/workspace-browser-baseline.json` under contract `atlas-phase4-workspace-browser-baseline/0.1`. CI regenerates all evidence and rejects any byte, digest, engine, count, accepted-input, shell-asset, validation, or authority drift.

These contracts remain candidates until one immutable final head passes the pinned workspace-browser workflow, deterministic shell workflow, workspace contracts, prior Phase 4 closures, reference shell, interaction contract, Foundation, the complete platform matrix, and end-to-end integration. Governance acceptance remains a separate transition after merge.

## Limitations

- Automated Chromium evidence is not assistive-technology user review, human usability review, accessibility certification, production browser support, or product readiness.
- The bounded fixture does not establish production workspace quality or corpus-scale performance.
- Browser state remains disposable and non-authoritative.
- No production framework, hosting platform, account model, cloud persistence, collaboration, live synchronization, canonical editor, or write path is selected.
