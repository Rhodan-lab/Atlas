# Phase 4 Workstream 4 Slice 1 — Catalase Generalization Implementation

This slice implements one bounded Catalase workspace fixture while leaving the accepted Workstream 3 workspace contracts unchanged.

## Candidate

```yaml
spec_contract: atlas-phase4-workstream4-generalization-fixture/0.1
evaluation_contract: atlas-phase4-workstream4-generalization-report/0.1
validation_contract: atlas-phase4-workstream4-generalization-validation/0.1
baseline_contract_candidate: atlas-phase4-workstream4-generalization-baseline/0.1
workspace_contracts: reused-unchanged
selected_entries: 5
advisory_candidates: 2
principia_references: 1
warnings: 1
exit_gates: 13
recommendation_candidate: proceed-static-reader-reuse-evaluation
implementation_authorized: false
```

The evaluator rebuilds the accepted structured index, ranks the bounded Catalase query, derives the exact five-entry order, constructs a fixture-only research trail, and passes the generated workspace through `tools.phase4_workspace.contracts` without changing that validator.

The first pull-request run is exploratory. It must generate byte-identical evidence on Python 3.11 and 3.13. Exact identities are pinned in a machine-readable baseline before merge.

## Authority

No canonical record is edited. The Principia envelope is synthetic, pinned, separate-status, non-live, and fixture-only. The unavailable-revision warning forbids silent substitution. The recommendation cannot authorize browser code or static-reader reuse without a separate governance transition.
