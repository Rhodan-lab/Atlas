# Principia Bridge Receiver

## Current state

Atlas now has a bounded receiving contract for exact-revision Principia dependencies. The receiver compiles canonical Atlas Markdown, validates every requested Atlas entity and revision, normalizes the external-dependent record, and produces dependency-impact reports.

It does not clone Principia, call Principia during Atlas validation, or activate a live bridge.

## Commands

```bash
python -m tools.phase2_kernel.cli compile \
  --canonical-root content/canonical \
  --output /tmp/atlas-runtime.json

python -m tools.phase2_kernel.cli bridge-validate \
  content/fixtures/phase2_bridge/principia-feedback-valid.json \
  --runtime /tmp/atlas-runtime.json

python -m tools.phase2_kernel.cli bridge-import \
  content/fixtures/phase2_bridge/principia-feedback-valid.json \
  --runtime /tmp/atlas-runtime.json \
  --output /tmp/principia-feedback.external-dependent.json

python -m tools.phase2_kernel.cli impact \
  model:en:delayed-correction-recurrence@2 \
  --runtime /tmp/atlas-runtime.json \
  --external /tmp/principia-feedback.external-dependent.json
```

## Deterministic rejection cases

- legacy ID-only export;
- missing or non-positive dependency revision;
- unavailable exact revision;
- missing Atlas entity;
- mismatched declared entity type;
- duplicate dependency ID;
- unsupported role, use, or change policy;
- any Principia pedagogical, release, knowledge, or review status field;
- `live: true` during Phase 2.

## Next boundary

After the updated Principia exporter is merged, its generated candidate export can replace the local Atlas fixture in an end-to-end compatibility test. The repositories must remain independently buildable and no status may cross automatically.
