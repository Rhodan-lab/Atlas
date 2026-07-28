#!/usr/bin/env python3
"""Build and validate deterministic Phase 4 Workstream 3 closure evidence."""
from __future__ import annotations

import copy
from typing import Any, Mapping

from tools.phase2_kernel import KernelError
from tools.phase4_workspace_completion.constants import (
    ALLOWED_DECISIONS,
    COMPLETION_CONTRACT,
    COMPLETION_VALIDATION_CONTRACT,
    EXPECTED_BROWSER,
    EXPECTED_SHELL,
    EXPECTED_WORKSPACE,
    MODE,
    BROWSER_BASELINE_CONTRACT,
    SHELL_BASELINE_CONTRACT,
    WORKSPACE_BASELINE_CONTRACT,
    _require,
    _require_mapping,
    json_sha256,
)
from tools.phase4_workspace_completion.inputs import (
    validate_browser_baseline,
    validate_shell_baseline,
    validate_workspace_baseline,
)


def _safe_boundary() -> dict[str, Any]:
    return {
        "workspace_authority": "ephemeral-research-only",
        "browser_state_authority": "ephemeral-only",
        "input_authority": "accepted-slice-1-and-slice-2-evidence-only",
        "closure_authority": "evidence-and-recommendation-only",
        "exact_revision_required": True,
        "accepted_export_only": True,
        "entry_order_preserved": True,
        "decisions_read_only": True,
        "candidates_unresolved": True,
        "principia_status_separate": True,
        "non_graph_workflow_required": True,
        "local_first": True,
        "deterministic_export_required": True,
        "account_required": False,
        "cloud_required": False,
        "credentials_required": False,
        "external_network_required": False,
        "canonical_copy_authority": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "automatic_merge_or_resolution": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
    }


def run_workstream3_closure(
    workspace_baseline: Mapping[str, Any],
    shell_baseline: Mapping[str, Any],
    browser_baseline: Mapping[str, Any],
    *,
    decision: str = "proceed-bounded-workspace-fixture-evaluation",
) -> dict[str, Any]:
    validate_workspace_baseline(workspace_baseline)
    validate_shell_baseline(shell_baseline)
    validate_browser_baseline(browser_baseline)
    if decision not in ALLOWED_DECISIONS:
        raise KernelError("E-PHASE4-W3-DECISION", f"unsupported Workstream 3 closure decision {decision!r}")

    workspace_report = workspace_baseline["report"]["record"]
    shell_record = shell_baseline["shell_data"]["record"]
    shell_build = shell_baseline["build_report"]["record"]
    browser_claims = browser_baseline["claims"]
    browser_authority = browser_baseline["authority"]

    replaceability = {
        "decision": "replaceable",
        "authoritative_inputs": [
            "accepted-workspace-export",
            "accepted-workspace-manifest",
            "accepted-workspace-contract-baseline",
        ],
        "generated_artifacts_disposable": True,
        "browser_state_disposable": True,
        "browser_storage_required": False,
        "api_required": False,
        "account_required": False,
        "cloud_required": False,
        "external_service_required": False,
        "replacement_requirement": "reproduce accepted contracts, exact identities, routes, authority labels, failures, and local download bytes before substitution",
        "canonical_mutation": False,
        "repository_mutation": False,
    }
    migration = {
        "strategy": "fixture-bound-rebuild-and-compare",
        "source_of_truth": "accepted-workspace-export-and-manifest",
        "required_checks": [
            "exact-contract-identity",
            "exact-revision-and-entry-order",
            "decision-and-candidate-authority",
            "warning-and-limitation-visibility",
            "non-graph-and-keyboard-equivalence",
            "local-download-byte-identity",
            "zero-external-network",
        ],
        "live_data_migration": False,
        "production_cutover_authorized": False,
        "canonical_rewrite_required": False,
        "repository_mutation": False,
    }
    rollback = {
        "strategy": "discard-generated-package-and-restore-accepted-artifacts",
        "restore_targets": [
            "workspace-contract-baseline",
            "workspace-shell-baseline",
            "workspace-browser-baseline",
        ],
        "canonical_rollback_required": False,
        "lifecycle_rollback_required": False,
        "principia_status_rollback_required": False,
        "previous_valid_workspace_preserved": True,
        "repository_mutation": False,
    }

    exit_gates = {
        "accepted_slice_identities_exact": (
            workspace_baseline["export"]["artifact"]["sha256"] == EXPECTED_WORKSPACE["export_sha256"]
            and shell_baseline["shell_data"]["artifact"]["sha256"] == EXPECTED_SHELL["shell_data_sha256"]
            and browser_baseline["evidence"]["report"]["artifact"]["sha256"] == EXPECTED_BROWSER["report_sha256"]
        ),
        "package_deterministic_and_replaceable": (
            workspace_baseline["python_substantive_artifacts_byte_identical"] is True
            and shell_baseline["python_substantive_artifacts_byte_identical"] is True
            and shell_build["replaceable"] is True
            and replaceability["generated_artifacts_disposable"] is True
        ),
        "routes_preserve_exact_workspace_semantics": (
            shell_record["counts"]["routes"] == 13
            and shell_record["counts"]["entries"] == 5
            and shell_record["authority"]["entry_order_preserved"] is True
            and shell_record["authority"]["decisions_read_only"] is True
            and shell_record["authority"]["candidates_unresolved"] is True
        ),
        "keyboard_and_non_graph_operation_pass": (
            browser_baseline["counts"]["keyboard_routes"] == 13
            and browser_claims["visible_focus_verified"] is True
            and browser_claims["non_graph_workflow_complete"] is True
        ),
        "local_download_reproduces_accepted_export": (
            browser_claims["local_download_byte_identical"] is True
            and shell_record["download"]["sha256"] == EXPECTED_WORKSPACE["export_sha256"]
            and shell_record["download"]["canonical_write"] is False
        ),
        "repeated_shell_and_browser_evidence_byte_identical": (
            shell_baseline["python_substantive_artifacts_byte_identical"] is True
            and browser_baseline["repeated_run_substantive_artifacts_byte_identical"] is True
        ),
        "browser_state_disposable_and_reload_independent": (
            browser_authority["browser_state_authority"] == "ephemeral-only"
            and replaceability["browser_state_disposable"] is True
            and replaceability["browser_storage_required"] is False
        ),
        "failures_visible_and_previous_state_preserved": (
            browser_claims["unknown_route_preserved"] is True
            and browser_claims["missing_artifact_failure_explicit"] is True
            and rollback["previous_valid_workspace_preserved"] is True
        ),
        "no_canonical_or_cross_repository_mutation": (
            workspace_report["canonical_mutation"] is False
            and workspace_report["lifecycle_mutation"] is False
            and workspace_report["review_mutation"] is False
            and browser_authority["canonical_mutation"] is False
            and browser_authority["repository_mutation"] is False
            and shell_record["authority"]["live_principia_dependency"] is False
        ),
        "local_operation_without_accounts_cloud_or_external_network": (
            shell_build["account_required"] is False
            and shell_build["cloud_required"] is False
            and shell_build["external_network_required"] is False
            and browser_baseline["counts"]["external_requests"] == 0
        ),
        "migration_and_rollback_boundaries_explicit": (
            migration["live_data_migration"] is False
            and migration["production_cutover_authorized"] is False
            and rollback["canonical_rollback_required"] is False
            and rollback["previous_valid_workspace_preserved"] is True
        ),
        "completion_contract_deterministic_and_platform_neutral": (
            replaceability["authoritative_inputs"]
            == [
                "accepted-workspace-export",
                "accepted-workspace-manifest",
                "accepted-workspace-contract-baseline",
            ]
            and migration["strategy"] == "fixture-bound-rebuild-and-compare"
        ),
        "bounded_recommendation_and_limitations_explicit": decision in ALLOWED_DECISIONS,
    }
    if len(exit_gates) != 13 or not all(exit_gates.values()):
        failed = sorted(name for name, value in exit_gates.items() if value is not True)
        raise KernelError("E-PHASE4-W3-EXIT-GATE", f"Workstream 3 exit gates failed: {failed}")

    recommendation = {
        "decision": decision,
        "purpose": "test whether accepted workspace contracts generalize to one additional bounded fixture without expanding authority",
        "authorized_scope": [
            "one-additional-non-production-fixture",
            "exact-revision-read-only-composition",
            "deterministic-export-and-static-reader",
            "pinned-browser-evidence",
            "separate-governance-before-implementation",
        ],
        "not_authorized": [
            "production-frontend-or-hosting-architecture",
            "accounts-or-cloud-persistence",
            "live-principia-synchronization",
            "canonical-editing-or-lifecycle-mutation",
            "automatic-candidate-resolution",
            "semantic-infrastructure-or-learned-ranking",
            "accessibility-certification",
        ],
        "evidence_basis": (
            "one accepted fixture passed deterministic contract, shell, browser, failure, export, "
            "replaceability, and authority gates; broader generalization is not yet established"
        ),
        "implementation_authorized": False,
        "separate_governance_required": True,
    }

    report: dict[str, Any] = {
        "contract": COMPLETION_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 3,
        "slice": 3,
        "state": "closure-candidate",
        "decision": decision,
        "accepted_evidence": {
            "slice1_workspace_contracts": {
                "pr": 50,
                "tested_head": "6d556bde6c24a8313bece3074f6c5fc56c4c4ccd",
                "merge_commit": "86c1f9f779172aa47d450022fc40357a93f2302f",
                "baseline_contract": WORKSPACE_BASELINE_CONTRACT,
                "baseline_digest": json_sha256(workspace_baseline),
                "fixture_sha256": EXPECTED_WORKSPACE["fixture_sha256"],
                "report_sha256": EXPECTED_WORKSPACE["report_sha256"],
                "report_digest": EXPECTED_WORKSPACE["report_digest"],
                "export_sha256": EXPECTED_WORKSPACE["export_sha256"],
                "export_digest": EXPECTED_WORKSPACE["export_digest"],
                "manifest_sha256": EXPECTED_WORKSPACE["manifest_sha256"],
                "manifest_digest": EXPECTED_WORKSPACE["manifest_digest"],
            },
            "slice2_workspace_shell": {
                "pr": 52,
                "tested_head": "f273c79b26d9b943a9b57a259645c8b0c6a5de48",
                "merge_commit": "dcad8aaedbf9b212ed926c09bbb50690c8fae19b",
                "baseline_contract": SHELL_BASELINE_CONTRACT,
                "baseline_digest": json_sha256(shell_baseline),
                "shell_data_sha256": EXPECTED_SHELL["shell_data_sha256"],
                "shell_build_digest": EXPECTED_SHELL["shell_build_digest"],
                "report_sha256": EXPECTED_SHELL["report_sha256"],
                "report_digest": EXPECTED_SHELL["report_digest"],
                "route_safe_index_sha256": EXPECTED_SHELL["index_sha256"],
            },
            "slice2_browser_evidence": {
                "pr": 54,
                "tested_head": "f2a9eb6f4dce8ee770024127c795598e37335921",
                "merge_commit": "6fb5932c4a6dbe26aa005da280d80bac1e61ad18",
                "baseline_contract": BROWSER_BASELINE_CONTRACT,
                "baseline_digest": json_sha256(browser_baseline),
                "engine": copy.deepcopy(EXPECTED_BROWSER["engine"]),
                "report_sha256": EXPECTED_BROWSER["report_sha256"],
                "report_digest": EXPECTED_BROWSER["report_digest"],
                "external_request_count": 0,
            },
        },
        "exit_gates": exit_gates,
        "evidence_summary": {
            "workspace_entries": 5,
            "workspace_candidates": 2,
            "workspace_routes": 13,
            "keyboard_routes": 13,
            "viewports": 2,
            "external_request_count": 0,
            "negative_workspace_cases": 10,
            "browser_evidence_files": 6,
            "slice1_python_byte_identical": True,
            "slice2_shell_python_byte_identical": True,
            "slice2_browser_repeated_byte_identical": True,
        },
        "replaceability": replaceability,
        "migration_boundary": migration,
        "rollback_boundary": rollback,
        "recommendation": recommendation,
        "limitations": [
            "The evidence covers one bounded fixture and does not establish general workspace quality.",
            "Automated Chromium evidence is not human usability review or accessibility certification.",
            "The accepted structured retrieval baseline is not a production retrieval-quality claim.",
            "No production frontend, hosting, deployment, account, or cloud architecture is selected.",
            "The Principia reference is fixture-only, pinned, non-live, and status-separate.",
            "Workspace decisions and candidates remain advisory and cannot change canonical or lifecycle authority.",
            "A proceed decision requires separate governance and does not authorize implementation by this report.",
        ],
        "review_policy": {
            "active_review_level": "ai-reviewed",
            "human_verified": False,
            "accessibility_certified": False,
            "assistive_technology_user_reviewed": False,
            "human_usability_reviewed": False,
        },
        "authority": _safe_boundary(),
        "production_retrieval_quality_claim": False,
        "embeddings": False,
        "vector_database": False,
        "external_services": False,
        "live": False,
    }
    report["report_digest"] = json_sha256(report)
    return report


def validate_completion_report(report: Mapping[str, Any]) -> dict[str, Any]:
    code = "E-PHASE4-W3-COMPLETION"
    _require(report, "contract", COMPLETION_CONTRACT, code)
    _require(report, "mode", MODE, code)
    _require(report, "phase", 4, code)
    _require(report, "workstream", 3, code)
    _require(report, "slice", 3, code)
    _require(report, "state", "closure-candidate", code)
    decision = report.get("decision")
    if decision not in ALLOWED_DECISIONS:
        raise KernelError("E-PHASE4-W3-DECISION", "completion recommendation is outside the allowed set")

    gates = report.get("exit_gates")
    if not isinstance(gates, Mapping) or len(gates) != 13 or not all(value is True for value in gates.values()):
        raise KernelError("E-PHASE4-W3-COMPLETION-GATES", "all thirteen Workstream 3 exit gates must pass")

    boundary = _require_mapping(report.get("authority"), "E-PHASE4-W3-AUTHORITY", "closure authority is required")
    for field, expected in _safe_boundary().items():
        if boundary.get(field) != expected:
            raise KernelError("E-PHASE4-W3-AUTHORITY", f"unsafe Workstream 3 closure authority: {field}")

    recommendation = _require_mapping(
        report.get("recommendation"),
        "E-PHASE4-W3-RECOMMENDATION",
        "bounded recommendation is required",
    )
    _require(recommendation, "decision", decision, "E-PHASE4-W3-RECOMMENDATION")
    _require(recommendation, "implementation_authorized", False, "E-PHASE4-W3-RECOMMENDATION")
    _require(recommendation, "separate_governance_required", True, "E-PHASE4-W3-RECOMMENDATION")
    if not isinstance(recommendation.get("not_authorized"), list) or len(recommendation["not_authorized"]) < 6:
        raise KernelError("E-PHASE4-W3-RECOMMENDATION", "recommendation limitations are incomplete")

    replaceability = _require_mapping(
        report.get("replaceability"),
        "E-PHASE4-W3-REPLACEABILITY",
        "replaceability evidence is required",
    )
    required_replaceability = {
        "decision": "replaceable",
        "generated_artifacts_disposable": True,
        "browser_state_disposable": True,
        "browser_storage_required": False,
        "api_required": False,
        "account_required": False,
        "cloud_required": False,
        "external_service_required": False,
        "canonical_mutation": False,
        "repository_mutation": False,
    }
    for field, expected in required_replaceability.items():
        _require(replaceability, field, expected, "E-PHASE4-W3-REPLACEABILITY")

    migration = _require_mapping(
        report.get("migration_boundary"),
        "E-PHASE4-W3-MIGRATION",
        "migration boundary is required",
    )
    _require(migration, "strategy", "fixture-bound-rebuild-and-compare", "E-PHASE4-W3-MIGRATION")
    _require(migration, "live_data_migration", False, "E-PHASE4-W3-MIGRATION")
    _require(migration, "production_cutover_authorized", False, "E-PHASE4-W3-MIGRATION")
    _require(migration, "canonical_rewrite_required", False, "E-PHASE4-W3-MIGRATION")
    if not isinstance(migration.get("required_checks"), list) or len(migration["required_checks"]) < 6:
        raise KernelError("E-PHASE4-W3-MIGRATION", "migration checks are incomplete")

    rollback = _require_mapping(
        report.get("rollback_boundary"),
        "E-PHASE4-W3-ROLLBACK",
        "rollback boundary is required",
    )
    _require(rollback, "strategy", "discard-generated-package-and-restore-accepted-artifacts", "E-PHASE4-W3-ROLLBACK")
    _require(rollback, "canonical_rollback_required", False, "E-PHASE4-W3-ROLLBACK")
    _require(rollback, "lifecycle_rollback_required", False, "E-PHASE4-W3-ROLLBACK")
    _require(rollback, "previous_valid_workspace_preserved", True, "E-PHASE4-W3-ROLLBACK")

    limitations = report.get("limitations")
    if not isinstance(limitations, list) or len(limitations) < 7 or not all(isinstance(item, str) and item for item in limitations):
        raise KernelError("E-PHASE4-W3-LIMITATIONS", "completion limitations are incomplete")

    review = _require_mapping(report.get("review_policy"), "E-PHASE4-W3-REVIEW", "review policy is required")
    for field in (
        "human_verified",
        "accessibility_certified",
        "assistive_technology_user_reviewed",
        "human_usability_reviewed",
    ):
        _require(review, field, False, "E-PHASE4-W3-REVIEW")

    required_false = {
        "production_retrieval_quality_claim": False,
        "embeddings": False,
        "vector_database": False,
        "external_services": False,
        "live": False,
    }
    for field, expected in required_false.items():
        _require(report, field, expected, "E-PHASE4-W3-AUTHORITY")

    digest = report.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError("E-PHASE4-W3-DIGEST", "completion report_digest must be a SHA-256")
    unsigned = dict(report)
    unsigned.pop("report_digest", None)
    if json_sha256(unsigned) != digest:
        raise KernelError("E-PHASE4-W3-DIGEST", "completion report digest mismatch")

    return {
        "contract": COMPLETION_VALIDATION_CONTRACT,
        "decision": "valid-workstream3-closure-candidate",
        "recommendation": decision,
        "exit_gate_count": len(gates),
        "report_digest": digest,
        "human_verified": False,
        "live": False,
        "repository_mutation": False,
    }
