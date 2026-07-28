# Phase 4 Workstream 1 — Minimal Reference Shell Candidate

## Status

Implementation candidate built only after acceptance of the Phase 4 interaction contracts.

```yaml
phase: 4
workstream: 1
state: reference-shell-candidate
interaction_contracts: accepted
local_first: true
static_assets: [index.html, styles.css, app.js]
api_required: false
cloud_required: false
account_required: false
graph_required: false
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Purpose

Prove that the accepted interaction fixtures can support a useful browser experience without introducing an API, cloud service, account system, graph-only navigation, or new authority layer.

The shell is deliberately small. It is evidence that the semantics can be exposed safely, not a claim that the product interface is complete.

## Architecture

```text
canonical Markdown
      |
      v
Phase 2 deterministic kernel
      |
      v
accepted Phase 4 interaction fixtures
      |
      v
Python deterministic shell-data builder
      |
      v
reference-shell-data.json
      |
      v
static HTML + CSS + JavaScript
```

The browser never parses canonical Markdown and never reimplements domain validation. The builder validates canonical identity and the interaction fixtures before producing disposable presentation data.

## Static application

Source assets:

```text
apps/reference-shell/index.html
apps/reference-shell/styles.css
apps/reference-shell/app.js
apps/reference-shell/README.md
```

Generated artifact:

```text
apps/reference-shell/data/reference-shell-data.json
```

The generated directory is ignored by Git. It can be deleted and rebuilt deterministically.

## Supported workflows

The shell exposes all eight accepted reference-view kinds:

1. exact entity revision;
2. provenance path;
3. explainable structured retrieval;
4. deterministic filter result;
5. exact-revision research trail;
6. advisory contradiction candidate;
7. fixture-only Principia reference;
8. unavailable-revision impact warning.

A dedicated failure view exposes the five accepted deterministic failure states.

## Navigation

The application uses a persistent list of named views rather than requiring a graph.

Each view exposes:

- view kind and revision;
- exact Atlas entity references;
- visible authority metadata;
- deterministic route;
- keyboard path;
- equivalent non-graph path;
- generated artifact contract and digests when applicable;
- Principia or warning details for bridge views.

Hash routes identify exact view revisions. No route uses implicit `latest`.

## Local-first behavior

Build:

```bash
python -m tools.phase4_interaction.build_shell \
  --output-dir apps/reference-shell \
  --report-output phase4-reference-shell-report.json
```

Serve:

```bash
python -m http.server 8080 --directory apps/reference-shell
```

A static server is necessary only because browsers restrict module and JSON loading from raw `file://` pages. The shell does not contact an Atlas API or any external service.

## Failure behavior

If generated data is missing or malformed, the shell:

- marks the local fixture unavailable;
- presents an explicit error panel;
- states that canonical knowledge remains unchanged;
- instructs the user to rebuild the local artifact;
- does not fall back to a live service.

## Accessibility foundation

The candidate includes:

- a skip link;
- semantic header, navigation, main, and footer landmarks;
- labelled navigation and live regions;
- keyboard-operable native buttons;
- visible focus styling;
- responsive non-graph navigation;
- reduced-motion handling;
- text labels instead of color-only meaning;
- light and dark system preferences.

These checks establish the reference foundation. They do not certify full WCAG conformance. Browser-assisted accessibility audits remain required before broader interface acceptance.

## Static safety

The renderer:

- builds DOM nodes through `createElement` and `textContent`;
- does not use `innerHTML`;
- does not use local or session storage;
- does not load remote scripts, fonts, styles, or images;
- reads one generated local JSON file;
- has no write path.

## Deterministic build evidence

The builder emits:

```yaml
shell_data_contract: atlas-reference-shell-data/0.1
shell_build_report_contract: atlas-reference-shell-build-report/0.1
view_count: 8
state_count: 8
principia_reference_count: 1
impact_warning_count: 1
failure_state_count: 5
local_first: true
replaceable: true
```

The first candidate run generates exact data, report, and artifact digests on Python 3.11 and Python 3.13. Those identities must be pinned before merge.

## CI evidence

The Phase 4 Reference Shell workflow:

- runs deterministic builder and static tests on Python 3.11 and 3.13;
- checks JavaScript syntax with Node.js;
- rebuilds generated data;
- verifies the authority boundary;
- starts a local HTTP server;
- fetches the page and generated JSON;
- uploads the complete runnable shell and build report;
- retains the full Atlas platform and end-to-end regression gates.

## Authority boundary

```yaml
canonical_authority: content/canonical/**/*.md
shell_data: generated-and-replaceable
shell_interface: read-only-presentation
exact_revision_required: true
principia_status_separate: true
implicit_latest: false
canonical_copy_authority: false
canonical_mutation: false
automatic_status_change: false
automatic_release_action: false
live_principia_dependency: false
external_services: false
live: false
repository_mutation: false
```

## Non-goals

This candidate does not:

- replace the canonical Markdown or kernel;
- implement editing or content creation;
- activate live Principia synchronization;
- add accounts, permissions, sharing, comments, or collaboration;
- select a production frontend architecture;
- implement graph visualization;
- add semantic search infrastructure;
- claim production retrieval quality;
- automate lifecycle, review, promotion, merge, or release decisions;
- constitute a polished final product.

## Candidate acceptance rule

The shell candidate may be accepted only if:

- both Python evidence builds are byte-identical;
- the generated data and report identities are pinned;
- JavaScript syntax and static landmark tests pass;
- the local-server smoke test passes;
- missing data produces explicit failure rather than network fallback;
- Phase 4 interaction-contract regression remains green;
- Foundation and the complete Atlas platform and end-to-end suite remain green.

Acceptance authorizes further workflow and usability evaluation. It does not authorize production deployment or live integration.
