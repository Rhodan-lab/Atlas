# Phase 4 Workstream 4 Slice 1 — Catalase Fixture Generalization Candidate

## Candidate status

```yaml
phase: 4
workstream: 4
slice: 1
state: implementation-candidate
fixture_count: 1
domain: catalase-assay-methodology
accepted_workspace_contracts_modified: false
browser_implementation_authorized: false
production_implementation_authorized: false
canonical_authoring_authorized: false
repository_authority_introduced: false
```

This slice evaluates whether the accepted Workstream 3 research-workspace contracts can represent one materially different knowledge domain without changing those contracts. It does not replace the accepted recommender-system workspace, select production architecture, or authorize a browser implementation.

## Exact source pool

The fixture binds these eight existing canonical revisions and no implicit latest reference:

1. `question:en:how-assay-conditions-affect-catalase@1`
2. `concept:en:catalase@1`
3. `model:en:catalase-assay-observation@1`
4. `evidence:en:fluorescent-catalase-assay-neutral-ph@1`
5. `claim:en:catalase-optimum-requires-assay-scope@1`
6. `synthesis:en:catalase-assay-conditions@1`
7. `src:aebi-1984-catalase-in-vitro@1`
8. `src:wu-lin-wolfbeis-2003-catalase-assay@1`

No canonical content is added or edited by this slice.

## Five-entry trail

The ordered research-only trail is:

| Position | Exact revision | Decision | Reason |
|---:|---|---|---|
| 1 | `claim:en:catalase-optimum-requires-assay-scope@1` | include | Prevents one reported optimum from being generalized beyond its assay scope. |
| 2 | `synthesis:en:catalase-assay-conditions@1` | include | Integrates the methodological variables required for comparison. |
| 3 | `evidence:en:fluorescent-catalase-assay-neutral-ph@1` | context | Preserves a method-specific neutral-pH observation without making it universal. |
| 4 | `model:en:catalase-assay-observation@1` | context | Exposes the joint dependence of reported activity on assay choices. |
| 5 | `concept:en:catalase@1` | exclude | Broad background does not establish assay equivalence. |

The non-graph summary contains one corresponding statement for every entry.

## Advisory candidates

Two candidates remain unresolved, advisory, and non-mutating:

- a scope-difference assessment between the Aebi in-vitro source and the Wu–Lin–Wolfbeis fluorescent-assay source;
- a related-but-not-duplicate assessment between the assay-scope claim and the integrated synthesis.

Neither candidate may automatically resolve, merge, alter lifecycle state, or acquire canonical authority.

## Principia and unavailable revision evidence

The fixture contains one pinned offline Principia envelope with `draft` status. The envelope is fixture-only, non-live, and cannot inherit status automatically.

The fixture also preserves an explicit warning for the unavailable target `claim:en:catalase-optimum-requires-assay-scope@2`. The evaluator must reject substitution with revision 1 or implicit latest.

## Contract reuse

The implementation imports and exercises these accepted contracts unchanged:

- `atlas-research-workspace/0.1`
- `atlas-research-workspace-entry/0.1`
- `atlas-research-workspace-decision/0.1`
- `atlas-research-workspace-export/0.1`
- `atlas-research-workspace-manifest/0.1`
- `atlas-research-workspace-failure/0.1`

The generalization layer is an adapter and evidence wrapper. It does not modify `tools/phase4_workspace/contracts.py`.

## Validation evidence

The candidate executes all thirteen Workstream 4 Slice 1 gates and combines:

- the ten accepted Workstream 3 negative cases;
- fourteen cross-domain boundary cases, covering non-Catalase entries, trail reordering, contract drift, unavailable authority escalation, account/cloud/network/credential requirements, browser or production implementation, release mutation, a second fixture, and repository mutation;
- repeated deterministic builds;
- Python 3.11 and Python 3.13 byte-identity comparison for the report, core contract report, export, and manifest.

The workflow is `.github/workflows/phase4-workspace-generalization.yml`.

## Candidate recommendation

```yaml
recommendation: proceed-static-reader-reuse-evaluation
recommendation_authority: separate-governance-proposal-only
implementation_authorized: false
```

A passing result supports only a later governance proposal to test reuse of the existing static reader. It does not authorize browser code, deployment, production architecture, accounts, cloud persistence, live synchronization, canonical editing, or automatic candidate resolution.
