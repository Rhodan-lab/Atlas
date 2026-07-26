# Atlas Phase 2 Kernel

This package compiles canonical `atlas-content/0.1` Markdown into a deterministic read-only runtime and implements the Atlas receiving side of the Principia bridge candidate.

## Commands

```bash
python -m tools.phase2_kernel.cli compile --output /tmp/atlas-runtime.json
python -m tools.phase2_kernel.cli lookup model:en:delayed-correction-recurrence@2 --runtime /tmp/atlas-runtime.json
python -m tools.phase2_kernel.cli provenance synthesis:en:delayed-feedback-and-oscillation@2 --runtime /tmp/atlas-runtime.json
python -m tools.phase2_kernel.cli bridge-validate content/fixtures/phase2_bridge/principia-feedback-valid.json --runtime /tmp/atlas-runtime.json
```

## Tests

```bash
python -m unittest discover -s tools/phase2_kernel/tests -v
```

## Boundaries

- canonical Markdown is never rewritten;
- exact revisions are mandatory;
- `latest` is unsupported;
- legacy ID-only Principia exports fail;
- Principia status fields fail;
- Phase 2 accepts only `live: false`;
- imports do not change Atlas or Principia lifecycle state.
