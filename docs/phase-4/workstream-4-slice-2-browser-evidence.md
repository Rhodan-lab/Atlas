# Phase 4 Workstream 4 Slice 2 — Reader Reuse Browser Evidence Candidate

## Objective

Collect pinned real-browser evidence over the accepted dual-package static-reader output without changing the reader, selector, workspace contracts, recommender package, or Catalase package.

## Evidence scope

The pinned Chromium harness verifies:

- the root selector exposes exactly the accepted recommender and Catalase packages;
- keyboard-visible skip navigation and known Catalase preselection;
- explicit rejection of unknown fixture selectors without fallback, navigation, persistence, or mutation;
- the accepted recommender package still verifies and renders its thirteen-route baseline;
- the Catalase package exposes all thirteen routes by keyboard with visible focus;
- five exact-revision Catalase decisions remain ordered and read-only;
- two advisory candidates remain unresolved;
- the fixture-only Principia status remains separate and non-live;
- the unavailable-revision warning remains explicit and non-mutating;
- complete non-graph summary coverage;
- deterministic deep links, reload, browser back, and browser forward;
- unknown-route refusal with deterministic recovery;
- missing Catalase export refusal without fallback or persistence;
- byte-identical local Catalase export download;
- desktop `1440×1000`, mobile `390×844`, and reduced-motion behavior;
- zero external browser requests;
- two byte-identical evidence generations;
- independent validation and resealed tamper rejection.

## Candidate contracts

```yaml
workflow: atlas-workspace-reader-reuse-browser-workflow-evidence/0.1
accessibility: atlas-workspace-reader-reuse-browser-accessibility-report/0.1
network: atlas-workspace-reader-reuse-browser-network-report/0.1
failure: atlas-workspace-reader-reuse-browser-failure-evidence/0.1
manifest: atlas-phase4-workspace-reader-reuse-browser-manifest/0.1
report: atlas-phase4-workspace-reader-reuse-browser-report/0.1
validation: atlas-phase4-workspace-reader-reuse-browser-validation/0.1
baseline_candidate: atlas-phase4-workspace-reader-reuse-browser-baseline/0.1
```

## Candidate decision

If all thirteen Slice 2 gates pass, the report may recommend:

`proceed-workstream4-closure-evaluation`

The recommendation cannot authorize its own implementation. A separate governance transition must accept the evidence before any closure work begins.

## Frozen authority

```yaml
implementation_authorized: false
separate_governance_required: true
browser_state_authority: ephemeral-only
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
candidate_resolution_authorized: false
repository_mutation: false
production_frontend_architecture_selected: false
live_principia_dependency: false
human_verified: false
accessibility_certified: false
```

Automated Chromium evidence is not human usability review, assistive-technology user review, accessibility certification, or production readiness.
