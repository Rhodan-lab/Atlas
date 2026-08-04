# Principia & Atlas Product Input

Atlas provides one official command that creates the exact workspace package consumed by the unified Principia & Atlas runtime.

## Build, verify, and check

From the Atlas repository root:

```bash
python -m tools.phase4_workspace.package_product_input build \
  --output /tmp/atlas-product-input
python -m tools.phase4_workspace.package_product_input verify \
  --package /tmp/atlas-product-input
python -m tools.phase4_workspace.package_product_input check
```

The build is staged and published atomically to a previously absent destination. It produces exactly eight files:

```text
index.html
styles.css
app.js
README.md
data/workspace-shell-data.json
data/workspace-export.json
data/workspace-manifest.json
workspace-shell-build-report.json
```

## Verification boundary

Verification rejects:

- missing or extra files;
- symlinks and non-regular entries;
- static assets that differ from the Atlas repository;
- generated export, manifest, shell-data, or report drift;
- inconsistent workspace ID or revision;
- relaxed mutation or external-network boundaries;
- live Principia dependencies;
- automatic Principia status inheritance.

The package remains an offline exact-revision input. It gives the unified product a verified Atlas research surface, but it does not grant Atlas authority over Principia pedagogy or status.

## Relationship to the workspace-shell baseline

The existing `apps/workspace-shell/README.md` and static assets remain byte-pinned by the Phase 4 workspace-shell baseline. Product-integration instructions therefore live in this Phase 4 document rather than changing the pinned package README.

The lower-level `tools.phase4_workspace.build_shell` command remains the source builder for workspace-shell development. `package_product_input` wraps it with exact static copying, the in-package build report, atomic publication, self-contained verification, and repeated-build determinism checks.
