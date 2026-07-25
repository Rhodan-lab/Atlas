# Contributing to Atlas

## Before changing code

1. Read `docs/architecture.md` and `docs/language-decisions.md`.
2. Identify the component that owns the behavior.
3. Avoid duplicating domain rules across languages.
4. Update the shared contract documentation when process output or `.atlas` data changes.

## Component checks

```bash
# Everything available on the machine
./scripts/check.sh

# Individual layers
make cpp
make python
make rust
make api
make integration
```

## Change rules

- C++ owns graph validity, mutation, traversal, and portable persistence.
- Rust search remains read-only.
- Python ingestion must be deterministic for identical input files.
- TypeScript should orchestrate native components rather than reproduce their algorithms.
- SQL changes require a schema-version update and a migration plan.
- A new language requires an ADR and must pass the admission test in `docs/language-decisions.md`.

## Pull requests

Keep changes bounded to one architectural purpose. Include:

- what changed and why;
- affected language boundaries;
- contract or migration impact;
- tests run;
- known follow-up work.
