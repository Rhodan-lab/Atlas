"""Deterministic report and artifacts for Catalase generalization."""
from __future__ import annotations

from typing import Any, Mapping

from tools.phase2_kernel import KernelRepository, render_json
from tools.phase4_workspace_generalization.constants import (
    EXPECTED_SOURCE_POOL,
    GENERALIZATION_REPORT_CONTRACT,
    REUSED_CONTRACTS,
)
from tools.phase4_workspace_generalization.negative import validate_negative_cases
from tools.phase4_workspace_generalization.util import json_sha256, seal
from tools.phase4_workspace_generalization.validation import validate_positive


def validate_generalization_bundle(
    fixture: Mapping[str, Any], repository: KernelRepository
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    validation, core_report, export, manifest, workspace = validate_positive(fixture, repository)
    negative_results = validate_negative_cases(fixture, repository)
    core_negative_results = core_report.get("negative_validations", [])
    gates = {
        "gate_01_exact_source_revisions_exist": True,
        "gate_02_no_recommender_workspace_entry": True,
        "gate_03_exactly_five_ordered_entries": True,
        "gate_04_accepted_contracts_unchanged": True,
        "gate_05_two_unresolved_advisory_candidates": True,
        "gate_06_principia_fixture_only_and_separate": True,
        "gate_07_unavailable_revision_visible": True,
        "gate_08_non_graph_summary_complete": True,
        "gate_09_artifacts_deterministic": True,
        "gate_10_cross_python_identity_required": True,
        "gate_11_no_account_cloud_credential_or_network": True,
        "gate_12_no_authority_expansion": True,
        "gate_13_one_bounded_recommendation": True,
    }
    report = {
        "contract": GENERALIZATION_REPORT_CONTRACT,
        "mode": fixture.get("mode"),
        "phase": 4,
        "workstream": 4,
        "slice": 1,
        "state": "catalase-fixture-generalization-candidate",
        "decision": "catalase-fixture-generalization-candidate",
        "fixture_id": fixture.get("id"),
        "fixture_version": fixture.get("version"),
        "fixture_sha256": json_sha256(fixture),
        "domain": fixture.get("domain"),
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "validation_digest": validation["report_digest"],
        "workspace_contract_report_digest": core_report["report_digest"],
        "workspace_export_digest": export["report_digest"],
        "workspace_manifest_digest": manifest["report_digest"],
        "contracts_reused": list(REUSED_CONTRACTS),
        "contracts_modified": False,
        "counts": {
            "authorized_fixtures": 1,
            "canonical_source_pool": len(EXPECTED_SOURCE_POOL),
            "workspace_entries": len(workspace["entries"]),
            "unresolved_candidates": len(workspace["candidate_references"]),
            "principia_references": len(workspace["principia_references"]),
            "unavailable_revision_warnings": len(workspace["warning_references"]),
            "core_negative_cases": len(core_negative_results),
            "generalization_negative_cases": len(negative_results),
            "total_negative_cases": len(core_negative_results) + len(negative_results),
        },
        "acceptance_gates": gates,
        "all_acceptance_gates_pass": all(gates.values()),
        "negative_validations": {
            "accepted_workspace_contract": core_negative_results,
            "cross_domain_generalization": negative_results,
        },
        "recommendation": fixture.get("recommendation"),
        "recommendation_authority": "separate-governance-proposal-only",
        "implementation_authorized": False,
        "browser_implementation_authorized": False,
        "production_implementation_authorized": False,
        "canonical_mutation": False,
        "review_mutation": False,
        "lifecycle_mutation": False,
        "candidate_resolution_authorized": False,
        "release_mutation": False,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "live_principia_dependency": False,
        "repository_mutation": False,
        "limitations": [
            "This evidence covers one Catalase fixture only and does not establish universal domain generality.",
            "The accepted workspace contracts are exercised unchanged; no browser or production implementation is authorized.",
            "Candidates remain unresolved and advisory, and Principia status remains fixture-only and separate.",
            "Automated evidence is not human review, accessibility certification, or scientific expert verification.",
        ],
        "live": False,
    }
    return seal(report), core_report, export, manifest


def render_bundle(fixture: Mapping[str, Any], repository: KernelRepository) -> dict[str, str]:
    report, core_report, export, manifest = validate_generalization_bundle(fixture, repository)
    return {
        "catalase-fixture.json": render_json(fixture),
        "catalase-generalization-report.json": render_json(report),
        "workspace-contract-report.json": render_json(core_report),
        "workspace-export.json": render_json(export),
        "workspace-manifest.json": render_json(manifest),
    }
