# Phase 4 Workstream 4 Slice 1 — Governance Acceptance

## Decision

```yaml
phase: 4
workstream: 4
slice: 1
decision: accepted
accepted_pr: 58
accepted_candidate_head: 4b25e0ac7e5b31f05629b19cef6388ca823ad9fa
accepted_merge_commit: a7e04f377389cb003aec8faadcd3eccdfd78ba2b
evidence_baseline_contract: atlas-phase4-workspace-generalization-baseline/0.1
recommendation_accepted: proceed-static-reader-reuse-evaluation
human_verified: false
accessibility_certified: false
```

The Catalase assay-methodology fixture demonstrates that the accepted Workstream 3 workspace contracts can represent one materially different domain without contract modification or authority expansion. This acceptance applies only to the single generated fixture `generalization-fixture:phase4-catalase-en-v1`.

## Accepted evidence

The accepted candidate binds eight existing canonical revisions, selects five ordered workspace entries, preserves two unresolved advisory candidates, includes one fixture-only non-live Principia envelope with separate status, and exposes one unavailable exact revision without fallback.

The evidence passed thirteen acceptance gates and twenty-four negative cases:

```yaml
canonical_source_pool: 8
workspace_entries: 5
unresolved_candidates: 2
principia_references: 1
unavailable_revision_warnings: 1
core_negative_cases: 10
generalization_negative_cases: 14
total_negative_cases: 24
acceptance_gates: 13
python_versions: [3.11, 3.13]
python_substantive_artifacts_byte_identical: true
```

Pinned identities are stored in `content/fixtures/phase4_workspace_generalization/catalase-generalization-baseline.json` and verified by `.github/workflows/phase4-workspace-generalization.yml`.

## Accepted artifact identities

| Artifact | SHA-256 | Internal report digest |
|---|---|---|
| `catalase-fixture.json` | `0a3c76134b72351b9e3c331d7058563f24cd9eef498af1053e60c4b96ef031cd` | — |
| `catalase-generalization-report.json` | `9028a6a4aa7d3841201d9273b42466ad217b283df93e84192933792ed1d6f2f6` | `75e5b93d288bd459e7ccc4e134b042f50dc1ef4a4eab24889fdb29b0b7a67121` |
| `workspace-contract-report.json` | `5a8c307e858b348bc695e7dcffe0c5a3577e4ccf83d282631a25f1b623facb91` | `3390157fd3935cb3f17ea2519a006589e299bbb922d87e28315e13172dc8fc32` |
| `workspace-export.json` | `b05617cac685873cd472b157efde835365b36d846db5eecf941db3495cc79893` | `d8280f4aa5cfbb5ba91569190ce7836676a5eabc22c113eccd4474ade6a25154` |
| `workspace-manifest.json` | `170a943ceecd306eb02251c92a143137d8f3dc6b047d52d5f5efcc9facf13a5f` | `0e1d2ee3674457844740b17100be298924293f1a9f7b0fab93ecae478197ca21` |

## Contract decision

The following accepted contracts remain unchanged:

- `atlas-research-workspace/0.1`;
- `atlas-research-workspace-entry/0.1`;
- `atlas-research-workspace-decision/0.1`;
- `atlas-research-workspace-export/0.1`;
- `atlas-research-workspace-manifest/0.1`;
- `atlas-research-workspace-failure/0.1`.

No generalized contract revision is created. The evidence supports reuse of the existing contract family for this one fixture only; it does not establish universal domain generality.

## Slice 2 authorization

This governance record activates **Workstream 4 Slice 2 — Catalase Static Reader Reuse Evaluation**.

Slice 2 may:

- reuse the existing accepted static workspace reader and route conventions;
- render only the accepted Catalase fixture and its deterministic export artifacts;
- add fixture-selection plumbing that remains local, deterministic, and replaceable;
- run keyboard, non-graph, responsive, history, download-identity, failure, warning, and zero-network evidence;
- use pinned Chromium automation as evidence, without claiming human review or accessibility certification.

Slice 2 may not:

- design a new production frontend architecture;
- add accounts, permissions, cloud state, collaboration, plugins, or external network dependencies;
- author or mutate canonical Atlas content;
- mutate review, lifecycle, promotion, merge, release, or repository state;
- resolve contradiction or duplicate candidates automatically;
- replace the accepted recommender-system workspace;
- add a second generalized fixture;
- introduce live Principia synchronization or inherited cross-repository status;
- claim production readiness, broad retrieval quality, universal contract generality, human verification, or accessibility certification.

## Rollback

If Slice 2 cannot reuse the existing reader without changing accepted semantics or authority, it must fail visibly, preserve Slice 1 as accepted evidence, and leave the accepted Workstream 3 reader unchanged. Any broader architecture or contract change requires new governance.
