# Atlas Research Workspace Shell

This directory contains a deliberately small static reader for the accepted Phase 4 Workstream 3 workspace export.

## Boundary

```yaml
input_authority: accepted-workspace-export-only
workspace_authority: ephemeral-research-only
browser_state_authority: ephemeral-only
exact_revision_required: true
entry_order_preserved: true
decisions_read_only: true
candidates_unresolved: true
principia_status_separate: true
local_first: true
external_network_required: false
canonical_mutation: false
lifecycle_mutation: false
review_mutation: false
repository_mutation: false
production_frontend_architecture_selected: false
live_principia_dependency: false
```

The shell does not contain authored workspace data. Its generated `data/` directory is built from canonical Atlas content and pinned accepted fixtures by `python -m tools.phase4_workspace.build_shell`.

## Principia & Atlas product input

Atlas now provides one official command that creates the exact package consumed by the unified Principia & Atlas runtime:

```bash
python -m tools.phase4_workspace.package_product_input build \
  --output /tmp/atlas-product-input
python -m tools.phase4_workspace.package_product_input verify \
  --package /tmp/atlas-product-input
python -m tools.phase4_workspace.package_product_input check
```

The build is staged and published atomically to a previously absent destination. It includes:

- the exact Atlas workspace-shell HTML, CSS, JavaScript, and README;
- the exact accepted workspace export and manifest;
- the deterministic workspace-shell data;
- `workspace-shell-build-report.json` inside the package.

Verification rejects missing or extra files, symlinks, static-asset drift from the Atlas repository, generated artifact drift, relaxed authority, live Principia dependencies, automatic status inheritance, and inconsistent workspace identity. The package remains an offline exact-revision input; it does not grant Atlas authority over Principia status.

## Local build

The lower-level manual shell build remains available for workspace-shell development:

```bash
rm -rf phase4-workspace-shell
mkdir -p phase4-workspace-shell
cp apps/workspace-shell/index.html phase4-workspace-shell/index.html
cp apps/workspace-shell/styles.css phase4-workspace-shell/styles.css
cp apps/workspace-shell/app.js phase4-workspace-shell/app.js
cp apps/workspace-shell/README.md phase4-workspace-shell/README.md
python -m tools.phase4_workspace.build_shell \
  --output-dir phase4-workspace-shell \
  --report-output phase4-workspace-shell-report.json
python -m http.server 8767 --bind 127.0.0.1 --directory phase4-workspace-shell
```

Open `http://127.0.0.1:8767/`.

## Generated files

- `data/workspace-shell-data.json` — deterministic route registry, accepted artifact identities, counts, download boundary, and authority metadata;
- `data/workspace-export.json` — exact bytes of the accepted read-only workspace export;
- `data/workspace-manifest.json` — exact bytes of the accepted export manifest;
- `phase4-workspace-shell-report.json` — deterministic package-build evidence.

Generated files are replaceable and non-authoritative. Deleting and rebuilding them from accepted inputs must reproduce the same bytes.

## Browser behavior

The shell provides routes for overview, five ordered decisions, advisory candidates, separate Principia status, warnings, open questions, limitations, export evidence, and a complete text-only summary.

Unknown routes fail explicitly and do not silently fall back. No fallback is permitted. Browser state is limited to the current URL hash and in-memory navigation state. The app does not use `localStorage`, `sessionStorage`, accounts, cloud persistence, analytics, plugins, or repository credentials.

The download button creates a local file from the already verified export bytes. It does not call an API or write to Atlas or Principia.

## Non-goals

This is not a production frontend, collaboration tool, editor, canonical knowledge interface, accessibility certification, production browser-support claim, or retrieval-quality claim.
