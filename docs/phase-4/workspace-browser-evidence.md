# Phase 4 Workstream 3 Slice 2 — Workspace Browser Evidence Candidate

## Status

```yaml
phase: 4
workstream: 3
slice: 2
state: workspace-browser-evidence-candidate
engine: chromium
engine_version: 151.0.7922.34
playwright_version: 1.62.0
route_count: 13
entry_route_count: 5
viewports: 2
accepted_failure_states: 2
external_network_allowed: false
screenshots_authoritative: false
human_verified: false
accessibility_certified: false
production_frontend_architecture_selected: false
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Purpose

Collect deterministic real-browser evidence over the accepted static workspace shell without changing the shell, selecting a production frontend, or granting browser state any knowledge authority.

The browser is a test instrument. The accepted workspace export, manifest, shell data, and static package remain the evidence inputs.

## Candidate contracts

```yaml
workflow_evidence: atlas-workspace-browser-workflow-evidence/0.1
accessibility_report: atlas-workspace-browser-accessibility-report/0.1
network_report: atlas-workspace-browser-network-report/0.1
failure_evidence: atlas-workspace-browser-failure-evidence/0.1
browser_manifest: atlas-phase4-workspace-browser-manifest/0.1
browser_report: atlas-phase4-workspace-browser-report/0.1
independent_validation: atlas-phase4-workspace-browser-validation/0.1
```

These contracts remain candidates until exact evidence artifacts are pinned and accepted through an immutable-head merge.

## Accepted inputs

```yaml
workspace_shell_baseline: atlas-phase4-workspace-shell-baseline/0.1
workspace_shell_data: atlas-workspace-shell-data/0.1
workspace_shell_build_digest: b4aa3fab14ecc66ee602c9c40dc88b10add23d3391915a72c31968c681edcaee
workspace_export_sha256: 43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a
workspace_export_digest: 82f08c18ae76b4b4d091fe0d8be7d54cf5d10d989443132a26e550056af3f56a
workspace_manifest_sha256: 8240d78b29f610cb7c566dfad50432473949c5a63b9de9c522ab28751d80fd09
workspace_manifest_digest: 9aefaf24b130718f284eecb5502b3c1dd144347f6fdcfc85b47d8ec6ce3fda68
```

## Required workflow evidence

The candidate exercises all thirteen accepted routes by keyboard:

- workspace overview;
- five ordered entry decisions;
- unresolved advisory candidates;
- separate Principia status;
- warnings;
- open questions;
- limitations;
- export evidence;
- complete text-only summary.

Each entry must preserve its exact revision, position, and include, exclude, or context decision. The browser may not reinterpret or edit any accepted decision.

Additional workflow evidence covers:

- deterministic deep links and reload;
- browser back and forward history;
- offline navigation after local boot;
- exact-byte local export download;
- unresolved candidate status;
- separate, non-live Principia status;
- warning and limitation visibility;
- complete non-graph equivalence.

## Accessibility evidence

The automated evidence checks:

- English document language;
- one banner, navigation, main, and content-info landmark;
- heading hierarchy beginning with one level-one heading;
- accessible names for every link and button;
- skip navigation;
- visible focus on the skip link, main target, all thirteen routes, and download action;
- labelled main content and live or alert regions;
- reduced-motion behavior;
- bounded desktop and mobile viewports without horizontal overflow.

This evidence is automated and browser-specific. It is not human verification, assistive-technology user review, broad usability validation, or accessibility certification.

## Failure evidence

Two explicit browser failures are required:

1. an unknown route refuses silent fallback, retains the previous valid route, and provides deterministic recovery;
2. a missing local manifest refuses partial package exposure and loads no fallback workspace.

Neither failure may create, reorder, remove, merge, or mutate workspace state.

## Network evidence

Every request is intercepted. Only the exact loopback origin is permitted.

```yaml
external_request_count: 0
credentials_used: false
remote_assets_used: false
analytics_used: false
cloud_service_used: false
service_workers_blocked: true
```

The missing-artifact test may intentionally block one loopback manifest request. That record remains local test evidence and is not an external request.

## Download evidence

The browser download must:

- use the accepted deterministic filename;
- reproduce the accepted export byte length and SHA-256;
- require no external request;
- create no Atlas or Principia write;
- remain optional to inspection and navigation.

The downloaded file is included in the evidence directory and independently hashed.

## Determinism and validation

The workflow:

1. builds the accepted shell package;
2. launches pinned Chromium with service workers blocked;
3. generates the full evidence directory twice;
4. requires byte identity across repeated runs;
5. validates every contract, semantic digest, child-file hash, authority boundary, and downloaded artifact independently;
6. runs tamper-and-reseal tests for external requests, route loss, false human-verification claims, silent fallback, and false download identity.

## Non-goals

This candidate does not modify the accepted workspace shell, select a production framework, certify accessibility, claim broad browser support, add accounts or cloud state, activate live Principia synchronization, edit canonical knowledge, resolve candidates, or create repository write authority.
