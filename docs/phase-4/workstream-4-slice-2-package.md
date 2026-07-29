# Phase 4 Workstream 4 Slice 2 — Static Reader Reuse Package Candidate

## Objective

Reuse the accepted Workstream 3 static reader for two deterministic local packages:

1. the unchanged accepted recommender-system package;
2. the accepted Catalase assay-methodology package from Workstream 4 Slice 1.

This candidate adds only local fixture selection and packaging. It does not add a new reader, modify accepted workspace contracts, or claim browser evidence.

## Package layout

```text
index.html
selector.js
selector.css
package-index.json
reader-reuse-report.json
reader-reuse-validation.json
packages/
  recommender/
    index.html
    styles.css
    app.js
    data/
      workspace-shell-data.json
      workspace-export.json
      workspace-manifest.json
  catalase/
    index.html
    styles.css
    app.js
    data/
      workspace-shell-data.json
      workspace-export.json
      workspace-manifest.json
```

The three reader assets in both package directories must be byte-identical to the accepted Workstream 3 reader baseline. Only the local data artifacts differ.

## Deterministic selector

The root selector exposes exactly two package choices. An unknown `?fixture=` value is rejected visibly and never falls back to the recommender package. The selector stores no state, requires no credentials, and performs no external request.

## Accepted evidence bindings

The builder verifies before packaging:

- `atlas-phase4-workspace-shell-baseline/0.1` for the accepted recommender reader package;
- `atlas-phase4-workspace-generalization-baseline/0.1` for the accepted Catalase fixture, report, workspace report, export, and manifest;
- the accepted static reader asset byte identities;
- unchanged workspace export, manifest, entry, decision, warning, candidate, and Principia semantics.

## Candidate boundary

```yaml
phase: 4
workstream: 4
slice: 2
state: reader-reuse-package-candidate
fixture_packages: 2
generalized_fixtures: 1
existing_reader_assets_only: true
browser_evidence_included: false
slice2_recommendation_issued: false
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
candidate_resolution_authorized: false
account_required: false
cloud_required: false
external_network_required: false
production_frontend_architecture_selected: false
live_principia_dependency: false
repository_mutation: false
```

## Evidence process

The package workflow runs the accepted reader and Catalase regressions, builds the complete dual-package tree twice on Python 3.11 and 3.13, requires repeated-run and cross-Python byte identity, and smoke-tests both packages over an isolated loopback HTTP server.

Real-browser keyboard, focus, history, responsive, download, tamper, and zero-external-request evidence remains a separate follow-up candidate. No final Slice 2 recommendation is issued by this static package PR.
