# Phase 4 Interaction Contract Evidence

## Candidate identity

```yaml
phase: 4
workstream: 1
mode: interactive-experience-foundation
state: interaction-contract-candidate
baseline_contract: atlas-phase4-interaction-contract-baseline/0.1
report_contract: atlas-phase4-interaction-contract-report/0.1
fixture_id: interaction-fixtures:phase4-reference-en-v1
fixture_version: 1
source_digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
entity_count: 34
```

## Pinned deterministic artifacts

The first evidence run completed successfully on Python 3.11 and Python 3.13. The assembled fixture and report artifacts were byte-identical across both versions.

```yaml
assembled_fixture_artifact_bytes: 28847
assembled_fixture_artifact_sha256: a4152c278c1345b0d8432dea1a1a7126216c7fd13ef7348ce732e7bf319764b9
fixture_semantic_sha256: 6b0508ed6c14f95ce3d11c3cd081cb79cbeea2c32b6442461982f191ce4628df
report_artifact_bytes: 2440
report_artifact_sha256: 2a9a2c74329b2954131754043814cec11072383acbcdc54d45b4d4f9adcb2c5a
report_digest: 9cbaa5f4675d995a183a6be5bee0b364eb7b6ae1da2ab9affc59b6d5fc452296
python_substantive_artifacts_byte_identical: true
```

## Coverage

```yaml
views: 8
states: 8
principia_references: 1
impact_warnings: 1
failure_states: 5
negative_cases: 6
workflow_kinds:
  - candidate
  - entity
  - filter
  - impact-warning
  - principia-reference
  - provenance
  - research-trail
  - retrieval
```

## Pinned negative outcomes

```text
E-INTERACTION-ACCESSIBILITY
E-INTERACTION-STATE-AUTHORITY
E-PRINCIPIA-REFERENCE
E-IMPACT-AUTHORITY
E-INTERACTION-FAILURE-AUTHORITY
E-INTERACTION-VIEW-KIND
```

The unit suite additionally rejects implicit `latest`, canonical source-digest tampering, view-level authority escalation, and silent failure fallback.

## Authority result

```yaml
exact_revision_preserved: true
authority_metadata_visible: true
keyboard_paths_required: true
non_graph_paths_required: true
principia_status_separate: true
impact_warnings_required: true
offline_capable: true
graph_visualization_optional: true
canonical_copy_authority: false
automatic_status_change: false
automatic_release_action: false
live_principia_dependency: false
external_services: false
embeddings: false
vector_database: false
live: false
repository_mutation: false
```

This evidence supports only the versioned interaction contract and fixture layer. Acceptance would authorize evaluation of a minimal local reference shell, not a production interface or live bridge.
