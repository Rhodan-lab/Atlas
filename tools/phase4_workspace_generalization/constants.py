"""Constants for the bounded Catalase workspace generalization."""
from __future__ import annotations

from tools.phase4_workspace.contracts import (
    DECISION_CONTRACT,
    ENTRY_CONTRACT,
    EXPORT_CONTRACT,
    FAILURE_CONTRACT,
    MANIFEST_CONTRACT,
    WORKSPACE_CONTRACT,
)

GENERALIZATION_FIXTURE_CONTRACT = "atlas-phase4-workspace-generalization-fixture/0.1"
GENERALIZATION_REPORT_CONTRACT = "atlas-phase4-workspace-generalization-report/0.1"
GENERALIZATION_VALIDATION_CONTRACT = "atlas-phase4-workspace-generalization-validation/0.1"

EXPECTED_SOURCE_POOL = (
    "question:en:how-assay-conditions-affect-catalase@1",
    "concept:en:catalase@1",
    "model:en:catalase-assay-observation@1",
    "evidence:en:fluorescent-catalase-assay-neutral-ph@1",
    "claim:en:catalase-optimum-requires-assay-scope@1",
    "synthesis:en:catalase-assay-conditions@1",
    "src:aebi-1984-catalase-in-vitro@1",
    "src:wu-lin-wolfbeis-2003-catalase-assay@1",
)
EXPECTED_TRAIL = (
    "claim:en:catalase-optimum-requires-assay-scope@1",
    "synthesis:en:catalase-assay-conditions@1",
    "evidence:en:fluorescent-catalase-assay-neutral-ph@1",
    "model:en:catalase-assay-observation@1",
    "concept:en:catalase@1",
)
ALLOWED_RECOMMENDATIONS = frozenset({
    "proceed-static-reader-reuse-evaluation",
    "hold-for-contract-review",
    "reject-catalase-generalization",
})
REUSED_CONTRACTS = (
    WORKSPACE_CONTRACT,
    ENTRY_CONTRACT,
    DECISION_CONTRACT,
    EXPORT_CONTRACT,
    MANIFEST_CONTRACT,
    FAILURE_CONTRACT,
)
