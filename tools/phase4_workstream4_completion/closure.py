"""Build and independently validate Phase 4 Workstream 4 closure evidence."""
from __future__ import annotations

import copy
import hashlib
from typing import Any, Mapping

from tools.phase2_kernel import KernelError, render_json
from tools.phase4_workstream4_completion.constants import (
    ALLOWED_DECISIONS,
    BROWSER_CONTRACT,
    COMPLETION_CONTRACT,
    EXPECTED_BROWSER,
    EXPECTED_GENERALIZATION,
    EXPECTED_PACKAGE,
    GENERALIZATION_CONTRACT,
    MODE,
    NEGATIVE_CASES,
    PACKAGE_CONTRACT,
    VALIDATION_CONTRACT,
)


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _mapping(value: Any, code: str, label: str) -> Mapping[str, Any]:
    _require(isinstance(value, Mapping), code, f"{label} must be an object")
    return value


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_sha256(record: Mapping[str, Any]) -> str:
    return _sha(render_json(record).encode("utf-8"))


def seal_record(record: Mapping[str, Any]) -> dict[str, Any]:
    sealed = copy.deepcopy(dict(record))
    sealed.pop("report_digest", None)
    sealed["report_digest"] = json_sha256(sealed)
    return sealed


def _safe_authority() -> dict[str, Any]:
    return {
        "workspace_authority": "ephemeral-research-only",
        "browser_state_authority": "ephemeral-only",
        "closure_authority": "evidence-and-recommendation-only",
        "accepted_evidence_only": True,
        "exact_revision_required": True,
        "decisions_read_only": True,
        "candidates_unresolved": True,
        "principia_status_separate": True,
        "local_first": True,
        "deterministic_export_required": True,
        "second_generalized_fixture_authorized": False,
        "new_canonical_authoring_authorized": False,
        "candidate_resolution_authorized": False,
        "account_required": False,
        "cloud_required": False,
        "credentials_required": False,
        "external_network_required": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "automatic_merge_or_resolution": False,
        "automatic_release_action": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "deployment_authorized": False,
        "live_principia_dependency": False,
        "human_verified": False,
        "accessibility_certified": False,
    }


def _validate_generalization(baseline: Mapping[str, Any]) -> None:
    code = "E-W4-CLOSURE-GENERALIZATION-DRIFT"
    _require(baseline.get("contract") == GENERALIZATION_CONTRACT, code, "generalization baseline contract drift")
    for key in ("accepted_pr", "accepted_candidate_head", "accepted_merge_commit"):
        _require(baseline.get(key) == EXPECTED_GENERALIZATION[key], code, f"generalization {key} drift")
    fixture = _mapping(baseline.get("fixture"), code, "generalization fixture")
    report = _mapping(baseline.get("report"), code, "generalization report")
    workspace_report = _mapping(baseline.get("workspace_contract_report"), code, "workspace report")
    export = _mapping(baseline.get("export"), code, "generalization export")
    manifest = _mapping(baseline.get("manifest"), code, "generalization manifest")
    counts = _mapping(baseline.get("counts"), code, "generalization counts")
    authority = _mapping(baseline.get("authority"), code, "generalization authority")
    _require(fixture.get("sha256") == EXPECTED_GENERALIZATION["fixture_sha256"], code, "fixture identity drift")
    _require(fixture.get("id") == "generalization-fixture:phase4-catalase-en-v1", code, "fixture id drift")
    _require(report.get("sha256") == EXPECTED_GENERALIZATION["report_sha256"], code, "report identity drift")
    _require(report.get("report_digest") == EXPECTED_GENERALIZATION["report_digest"], code, "report digest drift")
    _require(workspace_report.get("sha256") == EXPECTED_GENERALIZATION["workspace_report_sha256"], code, "workspace report identity drift")
    _require(workspace_report.get("report_digest") == EXPECTED_GENERALIZATION["workspace_report_digest"], code, "workspace report digest drift")
    _require(export.get("sha256") == EXPECTED_GENERALIZATION["export_sha256"], code, "export identity drift")
    _require(export.get("report_digest") == EXPECTED_GENERALIZATION["export_digest"], code, "export digest drift")
    _require(manifest.get("sha256") == EXPECTED_GENERALIZATION["manifest_sha256"], code, "manifest identity drift")
    _require(manifest.get("report_digest") == EXPECTED_GENERALIZATION["manifest_digest"], code, "manifest digest drift")
    _require(counts == {
        "acceptance_gates": 13,
        "canonical_source_pool": 8,
        "core_negative_cases": 10,
        "generalization_negative_cases": 14,
        "principia_references": 1,
        "total_negative_cases": 24,
        "unavailable_revision_warnings": 1,
        "unresolved_candidates": 2,
        "workspace_entries": 5,
    }, code, "generalization count drift")
    _require(report.get("recommendation") == "proceed-static-reader-reuse-evaluation", code, "generalization recommendation drift")
    for field in (
        "account_required", "browser_implementation_authorized", "candidate_resolution_authorized",
        "canonical_mutation", "cloud_required", "external_network_required", "lifecycle_mutation",
        "live_principia_dependency", "production_implementation_authorized", "release_mutation",
        "repository_mutation", "review_mutation",
    ):
        _require(authority.get(field) is False, code, f"generalization authority escalation: {field}")


def _validate_package(baseline: Mapping[str, Any]) -> None:
    code = "E-W4-CLOSURE-PACKAGE-DRIFT"
    _require(baseline.get("contract") == PACKAGE_CONTRACT, code, "static package baseline contract drift")
    counts = _mapping(baseline.get("counts"), code, "package counts")
    files = _mapping(baseline.get("files"), code, "package files")
    authority = _mapping(baseline.get("authority"), code, "package authority")
    _require(counts.get("file_count") == EXPECTED_PACKAGE["file_count"], code, "package file count drift")
    _require(counts.get("fixture_packages") == EXPECTED_PACKAGE["fixture_packages"], code, "fixture package count drift")
    _require(counts.get("generalized_fixtures") == EXPECTED_PACKAGE["generalized_fixtures"], "E-W4-CLOSURE-SECOND-FIXTURE", "second generalized fixture detected")
    _require(counts.get("routes_per_package") == 13, code, "route count drift")
    _require(baseline.get("python_substantive_artifacts_byte_identical") is True, code, "cross-Python package identity failed")
    _require(baseline.get("package_index", {}).get("sha256") == EXPECTED_PACKAGE["package_index_sha256"], code, "package index drift")
    _require(baseline.get("package_index_digest") == EXPECTED_PACKAGE["package_index_digest"], code, "package index digest drift")
    _require(baseline.get("reader_reuse_report", {}).get("sha256") == EXPECTED_PACKAGE["report_sha256"], code, "reader reuse report drift")
    _require(baseline.get("reader_reuse_report", {}).get("report_digest") == EXPECTED_PACKAGE["report_digest"], code, "reader reuse report digest drift")
    _require(baseline.get("reader_reuse_validation", {}).get("sha256") == EXPECTED_PACKAGE["validation_sha256"], code, "reader reuse validation drift")
    expected_files = {
        "packages/recommender/app.js": EXPECTED_PACKAGE["reader_app_sha256"],
        "packages/recommender/index.html": EXPECTED_PACKAGE["reader_index_sha256"],
        "packages/recommender/styles.css": EXPECTED_PACKAGE["reader_styles_sha256"],
        "packages/catalase/app.js": EXPECTED_PACKAGE["reader_app_sha256"],
        "packages/catalase/index.html": EXPECTED_PACKAGE["reader_index_sha256"],
        "packages/catalase/styles.css": EXPECTED_PACKAGE["reader_styles_sha256"],
        "packages/recommender/data/workspace-export.json": EXPECTED_PACKAGE["recommender_export_sha256"],
        "packages/recommender/data/workspace-manifest.json": EXPECTED_PACKAGE["recommender_manifest_sha256"],
        "packages/recommender/data/workspace-shell-data.json": EXPECTED_PACKAGE["recommender_shell_sha256"],
        "packages/catalase/data/workspace-export.json": EXPECTED_PACKAGE["catalase_export_sha256"],
        "packages/catalase/data/workspace-manifest.json": EXPECTED_PACKAGE["catalase_manifest_sha256"],
        "packages/catalase/data/workspace-shell-data.json": EXPECTED_PACKAGE["catalase_shell_sha256"],
    }
    for path, expected in expected_files.items():
        record = _mapping(files.get(path), code, path)
        _require(record.get("sha256") == expected, "E-W4-CLOSURE-READER-MUTATION", f"accepted package file drift: {path}")
    for field in (
        "account_required", "candidate_resolution_authorized", "canonical_mutation", "cloud_required",
        "external_network_required", "lifecycle_mutation", "live_principia_dependency",
        "production_frontend_architecture_selected", "repository_mutation", "review_mutation",
    ):
        _require(authority.get(field) is False, code, f"package authority escalation: {field}")


def _validate_browser(baseline: Mapping[str, Any]) -> None:
    code = "E-W4-CLOSURE-BROWSER-DRIFT"
    _require(baseline.get("contract") == BROWSER_CONTRACT, code, "browser baseline contract drift")
    _require(baseline.get("engine") == EXPECTED_BROWSER["engine"], code, "browser engine drift")
    _require(baseline.get("decision") == "proceed-workstream4-closure-evaluation", code, "browser decision drift")
    _require(baseline.get("repeated_run_substantive_artifacts_byte_identical") is True, code, "repeated browser evidence drift")
    counts = _mapping(baseline.get("counts"), code, "browser counts")
    claims = _mapping(baseline.get("claims"), code, "browser claims")
    authority = _mapping(baseline.get("authority"), code, "browser authority")
    evidence = _mapping(baseline.get("evidence"), code, "browser evidence")
    _require(counts == {
        "candidates": 2,
        "entries": 5,
        "external_requests": 0,
        "exit_gates": 13,
        "keyboard_routes": 13,
        "network_requests": 141,
        "principia_references": 1,
        "routes": 13,
        "selector_choices": 2,
        "viewports": 2,
        "warnings": 1,
    }, code, "browser count drift")
    expected_evidence = {
        "workflow": EXPECTED_BROWSER["workflow_sha256"],
        "accessibility": EXPECTED_BROWSER["accessibility_sha256"],
        "network": EXPECTED_BROWSER["network_sha256"],
        "failure": EXPECTED_BROWSER["failure_sha256"],
        "manifest": EXPECTED_BROWSER["manifest_sha256"],
        "report": EXPECTED_BROWSER["report_sha256"],
    }
    for name, expected in expected_evidence.items():
        child = _mapping(evidence.get(name), code, f"browser evidence {name}")
        artifact = _mapping(child.get("artifact"), code, f"browser evidence {name} artifact")
        _require(artifact.get("sha256") == expected, code, f"browser evidence drift: {name}")
    _require(evidence["report"].get("report_digest") == EXPECTED_BROWSER["report_digest"], code, "browser report digest drift")
    _require(baseline.get("validation", {}).get("artifact", {}).get("sha256") == EXPECTED_BROWSER["validation_sha256"], code, "browser validation drift")
    required_claims = (
        "candidates_unresolved", "decisions_read_only", "exact_entry_order_preserved",
        "local_download_byte_identical", "missing_artifact_failure_explicit", "non_graph_workflow_complete",
        "principia_status_separate", "recommender_regression_preserved", "reduced_motion_verified",
        "selector_unknown_fixture_refused", "unknown_route_preserved", "visible_focus_verified",
        "warning_visibility_verified",
    )
    for field in required_claims:
        _require(claims.get(field) is True, code, f"browser claim failed: {field}")
    for field in (
        "accessibility_certified", "candidate_resolution_authorized", "canonical_mutation", "human_verified",
        "implementation_authorized", "lifecycle_mutation", "live", "live_principia_dependency",
        "production_frontend_architecture_selected", "repository_mutation", "review_mutation",
    ):
        _require(authority.get(field) is False, code, f"browser authority escalation: {field}")
    _require(authority.get("separate_governance_required") is True, code, "separate governance removed")


def build_completion_report(
    generalization_baseline: Mapping[str, Any],
    package_baseline: Mapping[str, Any],
    browser_baseline: Mapping[str, Any],
    *,
    decision: str = "proceed-phase4-completion-governance",
) -> dict[str, Any]:
    _validate_generalization(generalization_baseline)
    _validate_package(package_baseline)
    _validate_browser(browser_baseline)
    _require(decision in ALLOWED_DECISIONS, "E-W4-CLOSURE-DECISION", f"unsupported completion decision {decision!r}")

    package_files = package_baseline["files"]
    browser_claims = browser_baseline["claims"]
    browser_authority = browser_baseline["authority"]
    authority = _safe_authority()
    limitations = [
        "The evidence covers one additional Catalase fixture and does not establish universal workspace-contract generality.",
        "The static selector and packages are local evidence artifacts, not a selected production frontend or deployment architecture.",
        "Automated Chromium evidence is not human usability review, assistive-technology user review, or accessibility certification.",
        "The structured retrieval baseline remains advisory and is not a production retrieval-quality claim.",
        "Both candidate relationships remain unresolved and cannot change canonical, review, lifecycle, merge, or release authority.",
        "The Principia envelope remains fixture-only, pinned, offline, non-live, and status-separate.",
        "A proceed recommendation requires separate governance and cannot authorize itself, Phase 5, production, or deployment.",
    ]
    replaceability = {
        "decision": "replaceable",
        "generated_selector_disposable": True,
        "generated_packages_disposable": True,
        "browser_state_disposable": True,
        "evidence_artifacts_reproducible": True,
        "canonical_migration_required": False,
        "live_data_migration_required": False,
        "account_or_cloud_migration_required": False,
        "replacement_requirement": "reproduce exact accepted contracts, artifact identities, routes, failures, downloads, authority labels, and zero-external-request evidence",
    }
    rollback = {
        "strategy": "discard-catalase-selector-package-and-restore-accepted-workstream3-recommender-package",
        "rollback_target": "accepted-workstream-3-recommender-package",
        "previous_valid_state_preserved": True,
        "canonical_rollback_required": False,
        "lifecycle_rollback_required": False,
        "review_rollback_required": False,
        "principia_status_rollback_required": False,
        "repository_mutation": False,
    }

    exit_gates = {
        "slice1_generalization_evidence_bound_exactly": generalization_baseline["report"]["sha256"] == EXPECTED_GENERALIZATION["report_sha256"],
        "slice2_static_package_evidence_bound_exactly": package_baseline["package_index"]["sha256"] == EXPECTED_PACKAGE["package_index_sha256"],
        "slice2_chromium_evidence_bound_exactly": browser_baseline["evidence"]["report"]["artifact"]["sha256"] == EXPECTED_BROWSER["report_sha256"],
        "workstream3_recommender_regression_preserved": (
            package_files["packages/recommender/data/workspace-export.json"]["sha256"] == EXPECTED_PACKAGE["recommender_export_sha256"]
            and browser_claims["recommender_regression_preserved"] is True
        ),
        "cross_domain_contract_reuse_preserved": (
            generalization_baseline["export"]["contract"] == "atlas-research-workspace-export/0.1"
            and generalization_baseline["manifest"]["contract"] == "atlas-research-workspace-manifest/0.1"
            and package_baseline["counts"]["generalized_fixtures"] == 1
        ),
        "exact_revisions_and_methodological_scope_preserved": (
            generalization_baseline["counts"]["canonical_source_pool"] == 8
            and generalization_baseline["counts"]["unavailable_revision_warnings"] == 1
            and authority["exact_revision_required"] is True
        ),
        "advisory_candidates_principia_and_warning_boundaries_preserved": (
            generalization_baseline["counts"]["unresolved_candidates"] == 2
            and generalization_baseline["counts"]["principia_references"] == 1
            and browser_claims["candidates_unresolved"] is True
            and browser_claims["principia_status_separate"] is True
            and browser_claims["warning_visibility_verified"] is True
        ),
        "deterministic_package_evidence_preserved": package_baseline["python_substantive_artifacts_byte_identical"] is True,
        "deterministic_browser_evidence_preserved": browser_baseline["repeated_run_substantive_artifacts_byte_identical"] is True,
        "selector_route_and_artifact_failures_preserved": (
            browser_claims["selector_unknown_fixture_refused"] is True
            and browser_claims["unknown_route_preserved"] is True
            and browser_claims["missing_artifact_failure_explicit"] is True
        ),
        "download_and_zero_external_network_preserved": (
            browser_claims["local_download_byte_identical"] is True
            and browser_baseline["counts"]["external_requests"] == 0
        ),
        "replaceability_migration_and_rollback_proved": (
            replaceability["generated_selector_disposable"] is True
            and replaceability["canonical_migration_required"] is False
            and rollback["previous_valid_state_preserved"] is True
            and rollback["canonical_rollback_required"] is False
        ),
        "limitations_and_non_certification_explicit": (
            len(limitations) == 7
            and browser_authority["human_verified"] is False
            and browser_authority["accessibility_certified"] is False
        ),
        "all_write_live_production_and_self_authority_frozen": all(
            authority[field] is False for field in (
                "second_generalized_fixture_authorized", "new_canonical_authoring_authorized",
                "candidate_resolution_authorized", "account_required", "cloud_required",
                "credentials_required", "external_network_required", "canonical_mutation",
                "lifecycle_mutation", "review_mutation", "automatic_merge_or_resolution",
                "automatic_release_action", "repository_mutation",
                "production_frontend_architecture_selected", "deployment_authorized",
                "live_principia_dependency", "human_verified", "accessibility_certified",
            )
        ),
    }
    _require(len(exit_gates) == 14 and all(exit_gates.values()), "E-W4-CLOSURE-EXIT-GATE", "one or more Workstream 4 closure gates failed")

    report = {
        "contract": COMPLETION_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 3,
        "state": "closure-candidate",
        "decision": decision,
        "accepted_evidence": {
            "slice1_generalization": {
                "accepted_pr": EXPECTED_GENERALIZATION["accepted_pr"],
                "accepted_tested_head": EXPECTED_GENERALIZATION["accepted_candidate_head"],
                "accepted_merge_commit": EXPECTED_GENERALIZATION["accepted_merge_commit"],
                "baseline_contract": GENERALIZATION_CONTRACT,
                "baseline_sha256": json_sha256(generalization_baseline),
                "fixture_sha256": EXPECTED_GENERALIZATION["fixture_sha256"],
                "report_sha256": EXPECTED_GENERALIZATION["report_sha256"],
                "report_digest": EXPECTED_GENERALIZATION["report_digest"],
                "export_sha256": EXPECTED_GENERALIZATION["export_sha256"],
                "manifest_sha256": EXPECTED_GENERALIZATION["manifest_sha256"],
            },
            "slice2_static_package": {
                "accepted_pr": EXPECTED_PACKAGE["accepted_pr"],
                "accepted_tested_head": EXPECTED_PACKAGE["accepted_tested_head"],
                "accepted_merge_commit": EXPECTED_PACKAGE["accepted_merge_commit"],
                "baseline_contract": PACKAGE_CONTRACT,
                "baseline_sha256": json_sha256(package_baseline),
                "package_index_sha256": EXPECTED_PACKAGE["package_index_sha256"],
                "package_index_digest": EXPECTED_PACKAGE["package_index_digest"],
                "report_sha256": EXPECTED_PACKAGE["report_sha256"],
                "report_digest": EXPECTED_PACKAGE["report_digest"],
            },
            "slice2_browser_evidence": {
                "accepted_pr": EXPECTED_BROWSER["accepted_pr"],
                "accepted_tested_head": EXPECTED_BROWSER["accepted_tested_head"],
                "accepted_merge_commit": EXPECTED_BROWSER["accepted_merge_commit"],
                "baseline_contract": BROWSER_CONTRACT,
                "baseline_sha256": json_sha256(browser_baseline),
                "engine": copy.deepcopy(EXPECTED_BROWSER["engine"]),
                "report_sha256": EXPECTED_BROWSER["report_sha256"],
                "report_digest": EXPECTED_BROWSER["report_digest"],
                "validation_sha256": EXPECTED_BROWSER["validation_sha256"],
            },
        },
        "evidence_summary": {
            "generalized_fixtures": 1,
            "fixture_packages": 2,
            "package_files": 18,
            "reader_assets_per_package": 3,
            "routes": 13,
            "keyboard_routes": 13,
            "entries": 5,
            "candidates": 2,
            "principia_references": 1,
            "warnings": 1,
            "viewports": 2,
            "external_requests": 0,
            "slice1_negative_cases": 24,
            "closure_negative_cases": len(NEGATIVE_CASES),
            "exit_gates": 14,
            "python_3_11_and_3_13_byte_identical_required": True,
        },
        "exit_gates": exit_gates,
        "replaceability": replaceability,
        "rollback_boundary": rollback,
        "authority": authority,
        "limitations": limitations,
        "negative_cases": list(NEGATIVE_CASES),
        "recommendation": {
            "decision": decision,
            "purpose": "permit a separate governance proposal to consider Phase 4 complete and choose the next bounded project transition",
            "evidence_basis": "one cross-domain Catalase fixture reused accepted workspace contracts and the unchanged static reader with deterministic local packaging, pinned Chromium evidence, preserved failures, and zero external requests",
            "implementation_authorized": False,
            "phase4_closed_by_report": False,
            "phase5_authorized": False,
            "production_authorized": False,
            "deployment_authorized": False,
            "separate_governance_required": True,
        },
        "review_policy": {
            "reviewer_kind": "ai",
            "human_verified": False,
            "accessibility_certified": False,
            "screenshots_authoritative": False,
        },
    }
    return seal_record(report)


def validate_completion_report(report: Mapping[str, Any]) -> dict[str, Any]:
    code = "E-W4-CLOSURE-VALIDATION"
    _require(report.get("contract") == COMPLETION_CONTRACT, code, "completion contract mismatch")
    _require(report.get("mode") == MODE, code, "completion mode mismatch")
    _require(report.get("phase") == 4 and report.get("workstream") == 4 and report.get("slice") == 3, code, "completion coordinates mismatch")
    _require(report.get("state") == "closure-candidate", code, "completion state mismatch")
    _require(report.get("decision") in ALLOWED_DECISIONS, code, "completion decision mismatch")
    digest = report.get("report_digest")
    _require(isinstance(digest, str), "E-W4-CLOSURE-DIGEST-TAMPER", "completion digest missing")
    unsealed = copy.deepcopy(dict(report))
    unsealed.pop("report_digest", None)
    _require(digest == json_sha256(unsealed), "E-W4-CLOSURE-DIGEST-TAMPER", "completion digest mismatch")
    gates = _mapping(report.get("exit_gates"), code, "exit gates")
    _require(len(gates) == 14 and all(value is True for value in gates.values()), "E-W4-CLOSURE-GATE-TAMPER", "closure gate failure")
    authority = _mapping(report.get("authority"), code, "authority")
    _require(authority == _safe_authority(), "E-W4-CLOSURE-PRODUCTION-AUTHORITY", "authority boundary drift")
    recommendation = _mapping(report.get("recommendation"), code, "recommendation")
    _require(recommendation.get("decision") == report.get("decision"), code, "recommendation decision drift")
    for field in ("implementation_authorized", "phase4_closed_by_report", "phase5_authorized", "production_authorized", "deployment_authorized"):
        _require(recommendation.get(field) is False, "E-W4-CLOSURE-SELF-AUTHORIZATION", f"self-authorization detected: {field}")
    _require(recommendation.get("separate_governance_required") is True, "E-W4-CLOSURE-SELF-AUTHORIZATION", "separate governance removed")
    review = _mapping(report.get("review_policy"), code, "review policy")
    _require(review.get("human_verified") is False, "E-W4-CLOSURE-HUMAN-VERIFICATION", "false human verification claim")
    _require(review.get("accessibility_certified") is False, "E-W4-CLOSURE-ACCESSIBILITY-CERTIFICATION", "false accessibility certification claim")
    _require(report.get("negative_cases") == list(NEGATIVE_CASES), code, "negative case registry drift")
    _require(len(report.get("limitations", [])) == 7, code, "limitations drift")
    return seal_record({
        "contract": VALIDATION_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 3,
        "state": "validated-closure-candidate",
        "decision": "valid-workstream4-closure-candidate",
        "completion_report_digest": digest,
        "exit_gate_count": 14,
        "negative_case_count": len(NEGATIVE_CASES),
        "recommendation": report["decision"],
        "implementation_authorized": False,
        "separate_governance_required": True,
        "human_verified": False,
        "accessibility_certified": False,
    })
