# Phase 4 Reference Shell Evidence

## Candidate identity

```yaml
phase: 4
workstream: 1
state: reference-shell-candidate
baseline_contract: atlas-phase4-reference-shell-baseline/0.1
shell_data_contract: atlas-reference-shell-data/0.1
shell_build_report_contract: atlas-reference-shell-build-report/0.1
source_digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
fixture_sha256: 6b0508ed6c14f95ce3d11c3cd081cb79cbeea2c32b6442461982f191ce4628df
interaction_report_digest: 9cbaa5f4675d995a183a6be5bee0b364eb7b6ae1da2ab9affc59b6d5fc452296
```

## Pinned generated evidence

```yaml
shell_data:
  artifact_bytes: 24054
  artifact_sha256: e0f9fcbff9b86cbd4fffcb43d9c2aff64c2eb602f9b2fa0a02b8804bd18eb762
  build_digest: ebc90a5781b7e974fe30034898364d87ebb5ed00ac05ce6cf0c27d6ded32b223
shell_build_report:
  artifact_bytes: 1131
  artifact_sha256: c9ca4259944bc4a90c42df26c4927c3f546a8358235b4e08a40715c692fa1eff
  report_digest: cfa4e37b07ed95337bb1fd1cb9e795656da78020d31b46eaf19828332c74d696
python_substantive_artifacts_byte_identical: true
```

## Pinned static assets

```yaml
index.html:
  bytes: 2786
  sha256: dd3854ea5e5dfd10a43ba7f28dbbac24a33acf3ca309b646e9256cd6cd52955d
styles.css:
  bytes: 8273
  sha256: 95d18d801687489e18edd7bee3a9ea43e40bf80607c586de2915ff35a6853579
app.js:
  bytes: 11280
  sha256: 2ac8f4343d8fe1d52d22a416897103bc7b231416d0214c7449f3cbb627d3b854
```

## Runtime coverage

```yaml
views: 8
states: 8
principia_references: 1
impact_warnings: 1
failure_states: 5
api_required: false
cloud_required: false
account_required: false
graph_required: false
keyboard_navigation_required: true
non_graph_navigation_required: true
local_first: true
replaceable: true
local_server_smoke_test: true
```

## Authority result

```yaml
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

The substantive runnable artifacts were identical across Python 3.11 and 3.13. Test transcripts and HTTP server logs differ only in runtime timing and process details and are not part of the pinned semantic artifact set.

This evidence supports a minimal local reference shell only. It does not establish production usability, production retrieval quality, live synchronization, or canonical write authority.
