"""Public contract surface for Phase 4 workspace generalization."""
from tools.phase4_workspace_generalization.constants import (
    EXPECTED_SOURCE_POOL,
    EXPECTED_TRAIL,
    GENERALIZATION_FIXTURE_CONTRACT,
    GENERALIZATION_REPORT_CONTRACT,
    GENERALIZATION_VALIDATION_CONTRACT,
    REUSED_CONTRACTS,
)
from tools.phase4_workspace_generalization.report import render_bundle, validate_generalization_bundle

__all__ = [
    "EXPECTED_SOURCE_POOL",
    "EXPECTED_TRAIL",
    "GENERALIZATION_FIXTURE_CONTRACT",
    "GENERALIZATION_REPORT_CONTRACT",
    "GENERALIZATION_VALIDATION_CONTRACT",
    "REUSED_CONTRACTS",
    "render_bundle",
    "validate_generalization_bundle",
]
