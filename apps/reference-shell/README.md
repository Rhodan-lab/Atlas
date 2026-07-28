# Atlas Reference Shell

A deliberately small, local-first browser shell over the accepted Phase 4 interaction fixtures.

## Build

From the repository root:

```bash
python -m tools.phase4_interaction.build_shell \
  --output-dir apps/reference-shell \
  --report-output phase4-reference-shell-report.json
```

The command validates canonical content and every interaction fixture before generating:

```text
apps/reference-shell/data/reference-shell-data.json
```

The generated directory is ignored by Git because it is disposable and deterministically rebuildable.

## Run locally

```bash
python -m http.server 8080 --directory apps/reference-shell
```

Open the local address shown by Python.

A static server is used because browsers generally block module and JSON loading from a raw `file://` page. No Atlas API, cloud database, account, or external service is required.

## Included workflows

- exact-revision Atlas entity inspection;
- provenance paths;
- explainable structured retrieval;
- deterministic filters;
- exact-revision research trails;
- advisory candidate inspection;
- fixture-only Principia references;
- explicit cross-repository impact warnings;
- deterministic failure-state inspection.

## Boundary

The shell is generated presentation state. It cannot write canonical knowledge, inherit Principia status, silently follow `latest`, change lifecycle state, or activate live synchronization.

This is a reference implementation for contract validation, not a production interface.
