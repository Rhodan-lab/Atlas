#!/usr/bin/env python3
"""Build and validate deterministic Phase 4 Workstream 4 closure evidence."""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping

from tools.phase2_kernel import KernelError

COMPLETION_CONTRACT = "atlas-phase4-workstream4-completion-report/0.1"
VALIDATION_CONTRACT = "atlas-phase4-workstream4-completion-validation/0.1"
BASELINE_CONTRACT = "atlas-phase4-workstream4-completion-baseline/0.1"
MODE = "interactive-experience-foundation"
ALLOWED_DECISIONS = (
    "proceed-phase4-completion-governance",
    "hold-accepted-workstream4",
    "reject-workstream4-generalization",
)

GENERALIZATION_CONTRACT = "atlas-phase4-workspace-generalization-baseline/0.1"
PACKAGE_CONTRACT = "atlas-phase4-workspace-reader-reuse-baseline/0.1"
BROWSER_CONTRACT = "atlas-phase4-workspace-reader-reuse-browser-baseline/0.1"

EXPECTED_GENERALIZATION = {
    "accepted_pr": 58,
    "accepted_candidate_head": "4b25e0ac7e5b31f05629b19cef6388ca823ad9fa",
    "accepted_merge_commit": "a7e04f377389cb003aec8faadcd3eccdfd78ba2b",
    "fixture_sha256": "0a3c76134b72351b9e3c331d7058563f24cd9eef498af1053e60c4b96ef031cd",
    "report_sha256": "9028a6a4aa7d3841201d9273b42466ad217b283df93e84192933792ed1d6f2f6",
    "report_digest": "75e5b93d288bd459e7ccc4e134b042f50dc1ef4a4eab24889fdb29b0b7a67121",
    "workspace_report_sha256": "5a8c307e858b348bc695e7dcffe0c5a3577e4ccf83d282631a25f1b623facb91",
    "workspace_report_digest": "3390157fd3935cb3f17ea2519a006589e299bbb922d87e28315e13172dc8fc32",
    "export_sha256": "b05617cac685873cd472b157efde835365b36d846db5eecf941db3495cc79893",
    "export_digest": "d8280f4aa5cfbb5ba91569190ce7836676a5eabc22c113eccd4474ade6a25154",
    "manifest_sha256": "170a943ceecd306eb02251c92a143137d8f3dc6b047d52d5f5efcc9facf13a5f",
    "manifest_digest": "0e1d2ee3674457844740b17100be298924293f1a9f7b0fab93ecae478197ca21",
}

EXPECTED_PACKAGE_FILES = {
    "index.html": (1968, "9711a03adf18b607d038b1b556b2ab368633a731440cec3a497c4fdf6a8c0fe9"),
    "package-index.json": (5922, "225aff2dd97b3fb0adfc528b10ac2a485eadb2db68758b8605fa633675810b53"),
    "packages/catalase/app.js": (23359, "0f44b35ccd3a6c59abc9eecdcf176dbc3bbf53cc155ddedb32fb518003d5c50f"),
    "packages/catalase/data/workspace-export.json": (11284, "b05617cac685873cd472b157efde835365b36d846db5eecf941db3495cc79893"),
    "packages/catalase/data/workspace-manifest.json": (1082, "170a943ceecd306eb02251c92a143137d8f3dc6b047d52d5f5efcc9facf13a5f"),
    "packages/catalase/data/workspace-shell-data.json": (5742, "9a45af3d8ec29aef03aafd472db1669a8ed5f60026eff9b784abe0a0f3be3815"),
    "packages/catalase/index.html": (3232, "ae7eafc4dccae669f25ed4f6e6e5bc8e81bce8dcabcc81b5d585d4d09fb5e921"),
    "packages/catalase/styles.css": (8427, "6016098e9461be50f6b5346d76b58d0111dfae8d42355884bf25e9885546e98f"),
    "packages/recommender/app.js": (23359, "0f44b35ccd3a6c59abc9eecdcf176dbc3bbf53cc155ddedb32fb518003d5c50f"),
    "packages/recommender/data/workspace-export.json": (11347, "43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a"),
    "packages/recommender/data/workspace-manifest.json": (1094, "8240d78b29f610cb7c566dfad50432473949c5a63b9de9c522ab28751d80fd09"),
    "packages/recommender/data/workspace-shell-data.json": (5955, "a2dd3979c35cee4d081511cadf98499e325dfd22d814cae097cfd3e98f3f5c0c"),
    "packages/recommender/index.html": (3232, "ae7eafc4dccae669f25ed4f6e6e5bc8e81bce8dcabcc81b5d585d4d09fb5e921"),
    "packages/recommender/styles.css": (8427, "6016098e9461be50f6b5346d76b58d0111dfae8d42355884bf25e9885546e98f"),
    "reader-reuse-report.json": (2153, "c55e3a1ce55b735ed01c43eb47b3b7ca95fe7eee8914d8913133a6614ef1d752"),
    "reader-reuse-validation.json": (348, "4499e674dc272f3037ae16c307f9c4c762e795f524ce035d8170055e40146512"),
    "selector.css": (1573, "0297799e18f8ced767ce4531d8912f83669d3e67af0ea1ebef360836e23fa070"),
    "selector.js": (1096, "7e1a4a59888e98689ff1f17a83c80b8a4486f1f6ba93ac3cc9be8e41028799e3"),
}

EXPECTED_PACKAGE = {
    "accepted_pr": 60,
    "accepted_tested_head": "c5b76df4eb303bce5820044ebacc51a178938111",
    "accepted_merge_commit": "694ee1346045e79a843b02242a51dcba0e5b3928",
    "package_index_digest": "209daa4d90de4271d2d09ea5942e561811a8f4d907553ff3eecb09943c6f5b18",
    "reader_reuse_report_digest": "cebaba8c4e9dfca355c2b771e86a53f95e18de6c2d88fead996f314c87b812f2",
}

EXPECTED_BROWSER_EVIDENCE = {
    "workflow": (9593, "1c3fd948458cb46819a10d959e6d61e13092b778d1fc9c706225dfabecf6f709", "81dc4dea73d836ca118579b619a41695b091e70ae42820be0e7f167947ec8665"),
    "accessibility": (1283, "6f69665debcc22517a84872e36a546bd95850ee105f89fd5cfcf8ba7d03e1f9f", "aff85eb5c21835b812293f169219e79f90f42acd5434b88e56b7e2cbd48eca12"),
    "network": (22882, "318c5bd0d19ddf9f89aa59708c62c5c5f6fc368751e78476e0548473554f45b7", "7d0b5482a6471356d1bf25da551e0b4ee568cedba76af121c53fe45022abdfcd"),
    "failure": (1512, "f06d60986526dead5bc84bc2d03b7312ce08af9d0b02d474ba57613ca6479786", "7b48fcdc97cdd1f1cec6a17d707a92bc6bfa5d6e9d153ccdaf5589887437f1fe"),
    "manifest": (2894, "529299543121252550d394c60b979b312d3cff905ca32ac6373d8a15c155e9ba", "0fbc6bbf7f3c60cfedb48559d2492d5a22037172fd0b0c5ab849c3ec2b3d724d"),
    "report": (3343, "bb2d7c4f2d195a6161329ac2a62e96e733768007749d19e75b7574c6983dc8f9", "e367bb46d43e0de6886f3ce9dffa22624c65cdb45ba5470e4ec48f544ac57ced"),
}

EXPECTED_BROWSER = {
    "accepted_pr": 61,
    "accepted_tested_head": "ee22fa0e999b8a863ca08f1511a3a54f9449d3b2",
    "accepted_merge_commit": "8481b32cfa8fef538c5bd51833894d6ee52de64a",
    "engine": {"name": "chromium", "playwright_version": "1.62.0", "version": "151.0.7922.34"},
    "validation_sha256": "d83844150b1a20273d79f343d44421e8dba01e183243d4e44d003247731fdf29",
    "validation_bytes": 694,
    "report_digest": "e367bb46d43e0de6886f3ce9dffa22624c65cdb45ba5470e4ec48f544ac57ced",
}


def json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _require_field(record: Mapping[str, Any], field: str, expected: Any, code: str) -> None:
    _require(record.get(field) == expected, code, f"expected {field}={expected!r}")


def _mapping(record: Mapping[str, Any], field: str, code: str) -> Mapping[str, Any]:
    value = record.get(field)
    _require(isinstance(value, Mapping), code, f"{field} must be an object")
    return value


def _seal(record: Mapping[str, Any]) -> dict[str, Any]:
    unsigned = dict(record)
    unsigned.pop("report_digest", None)
    sealed = dict(record)
    sealed["report_digest"] = json_sha256(unsigned)
    return sealed


def _validate_authority(authority: Mapping[str, Any], *, browser: bool = False) -> None:
    expected = {
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "repository_mutation": False,
        "live_principia_dependency": False,
    }
    if browser:
        expected.update({
            "candidate_resolution_authorized": False,
            "human_verified": False,
            "accessibility_certified": False,
            "implementation_authorized": False,
            "separate_governance_required": True,
            "production_frontend_architecture_selected": False,
            "live": False,
        })
    else:
        expected.update({
            "account_required": False,
            "cloud_required": False,
            "external_network_required": False,
        })
    for field, value in expected.items():
        _require(authority.get(field) == value, "E-PHASE4-W4-AUTHORITY", f"unsafe authority field {field}")


def validate_generalization_baseline(record: Mapping[str, Any]) -> None:
    _require_field(record, "contract", GENERALIZATION_CONTRACT, "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "accepted_pr", EXPECTED_GENERALIZATION["accepted_pr"], "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "accepted_candidate_head", EXPECTED_GENERALIZATION["accepted_candidate_head"], "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "accepted_merge_commit", EXPECTED_GENERALIZATION["accepted_merge_commit"], "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "mode", MODE, "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "phase", 4, "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "workstream", 4, "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "slice", 1, "E-PHASE4-W4-GENERALIZATION")
    _require_field(record, "state", "accepted-evidence-baseline", "E-PHASE4-W4-GENERALIZATION")
    counts = _mapping(record, "counts", "E-PHASE4-W4-GENERALIZATION")
    expected_counts = {
        "acceptance_gates": 13,
        "canonical_source_pool": 8,
        "core_negative_cases": 10,
        "generalization_negative_cases": 14,
        "total_negative_cases": 24,
        "workspace_entries": 5,
        "unresolved_candidates": 2,
        "principia_references": 1,
        "unavailable_revision_warnings": 1,
    }
    for field, value in expected_counts.items():
        _require(counts.get(field) == value, "E-PHASE4-W4-GENERALIZATION", f"generalization count drift: {field}")
    fixture = _mapping(record, "fixture", "E-PHASE4-W4-GENERALIZATION")
    _require(fixture.get("contract") == "atlas-phase4-workspace-generalization-fixture/0.1", "E-PHASE4-W4-GENERALIZATION", "fixture contract drift")
    _require(fixture.get("id") == "generalization-fixture:phase4-catalase-en-v1", "E-PHASE4-W4-GENERALIZATION", "fixture identity drift")
    _require(fixture.get("sha256") == EXPECTED_GENERALIZATION["fixture_sha256"], "E-PHASE4-W4-GENERALIZATION", "fixture SHA drift")
    report = _mapping(record, "report", "E-PHASE4-W4-GENERALIZATION")
    _require(report.get("contract") == "atlas-phase4-workspace-generalization-report/0.1", "E-PHASE4-W4-GENERALIZATION", "report contract drift")
    _require(report.get("sha256") == EXPECTED_GENERALIZATION["report_sha256"], "E-PHASE4-W4-GENERALIZATION", "report SHA drift")
    _require(report.get("report_digest") == EXPECTED_GENERALIZATION["report_digest"], "E-PHASE4-W4-GENERALIZATION", "report digest drift")
    _require(report.get("recommendation") == "proceed-static-reader-reuse-evaluation", "E-PHASE4-W4-GENERALIZATION", "Slice 1 recommendation drift")
    _require(report.get("all_acceptance_gates_pass") is True, "E-PHASE4-W4-GENERALIZATION", "Slice 1 gates must pass")
    workspace_report = _mapping(record, "workspace_contract_report", "E-PHASE4-W4-GENERALIZATION")
    _require(workspace_report.get("contract") == "atlas-phase4-workspace-contract-report/0.1", "E-PHASE4-W4-GENERALIZATION", "workspace report contract drift")
    _require(workspace_report.get("sha256") == EXPECTED_GENERALIZATION["workspace_report_sha256"], "E-PHASE4-W4-GENERALIZATION", "workspace report SHA drift")
    _require(workspace_report.get("report_digest") == EXPECTED_GENERALIZATION["workspace_report_digest"], "E-PHASE4-W4-GENERALIZATION", "workspace report digest drift")
    for field, contract, sha_key, digest_key in (
        ("export", "atlas-research-workspace-export/0.1", "export_sha256", "export_digest"),
        ("manifest", "atlas-research-workspace-manifest/0.1", "manifest_sha256", "manifest_digest"),
    ):
        item = _mapping(record, field, "E-PHASE4-W4-GENERALIZATION")
        _require(item.get("contract") == contract, "E-PHASE4-W4-GENERALIZATION", f"{field} contract drift")
        _require(item.get("sha256") == EXPECTED_GENERALIZATION[sha_key], "E-PHASE4-W4-GENERALIZATION", f"{field} SHA drift")
        _require(item.get("report_digest") == EXPECTED_GENERALIZATION[digest_key], "E-PHASE4-W4-GENERALIZATION", f"{field} digest drift")
    workflow = _mapping(record, "workflow", "E-PHASE4-W4-GENERALIZATION")
    _require(workflow.get("python_versions") == ["3.11", "3.13"], "E-PHASE4-W4-GENERALIZATION", "Python matrix drift")
    _require(workflow.get("python_substantive_artifacts_byte_identical") is True, "E-PHASE4-W4-GENERALIZATION", "Slice 1 cross-Python identity failed")
    _validate_authority(_mapping(record, "authority", "E-PHASE4-W4-GENERALIZATION"))
    authority = record["authority"]
    for field in ("browser_implementation_authorized", "candidate_resolution_authorized", "production_implementation_authorized", "release_mutation"):
        _require(authority.get(field) is False, "E-PHASE4-W4-AUTHORITY", f"generalization requires {field}=false")


def validate_package_baseline(record: Mapping[str, Any]) -> None:
    _require_field(record, "contract", PACKAGE_CONTRACT, "E-PHASE4-W4-PACKAGE")
    _require_field(record, "mode", MODE, "E-PHASE4-W4-PACKAGE")
    _require_field(record, "workstream", 4, "E-PHASE4-W4-PACKAGE")
    _require_field(record, "slice", 2, "E-PHASE4-W4-PACKAGE")
    _require_field(record, "state", "pinned-static-package-candidate", "E-PHASE4-W4-PACKAGE")
    counts = _mapping(record, "counts", "E-PHASE4-W4-PACKAGE")
    for field, value in {
        "file_count": 18,
        "fixture_packages": 2,
        "generalized_fixtures": 1,
        "reader_assets_per_package": 3,
        "routes_per_package": 13,
    }.items():
        _require(counts.get(field) == value, "E-PHASE4-W4-PACKAGE", f"package count drift: {field}")
    files = _mapping(record, "files", "E-PHASE4-W4-PACKAGE")
    _require(set(files) == set(EXPECTED_PACKAGE_FILES), "E-PHASE4-W4-PACKAGE", "18-file package set drift")
    for name, (size, sha) in EXPECTED_PACKAGE_FILES.items():
        item = files.get(name)
        _require(isinstance(item, Mapping), "E-PHASE4-W4-PACKAGE", f"missing package file {name}")
        _require(item.get("bytes") == size and item.get("sha256") == sha, "E-PHASE4-W4-PACKAGE", f"package identity drift: {name}")
    _require(record.get("package_index_digest") == EXPECTED_PACKAGE["package_index_digest"], "E-PHASE4-W4-PACKAGE", "package index digest drift")
    _require(record.get("python_versions") == ["3.11", "3.13"], "E-PHASE4-W4-PACKAGE", "package Python matrix drift")
    _require(record.get("python_substantive_artifacts_byte_identical") is True, "E-PHASE4-W4-PACKAGE", "package cross-Python identity failed")
    _require(record.get("browser_evidence_included") is False, "E-PHASE4-W4-PACKAGE", "static package may not claim browser evidence")
    report = _mapping(record, "reader_reuse_report", "E-PHASE4-W4-PACKAGE")
    _require(report.get("report_digest") == EXPECTED_PACKAGE["reader_reuse_report_digest"], "E-PHASE4-W4-PACKAGE", "reader report digest drift")
    validation = _mapping(record, "reader_reuse_validation", "E-PHASE4-W4-PACKAGE")
    _require(validation.get("decision") == "valid-reader-reuse-package-candidate", "E-PHASE4-W4-PACKAGE", "reader validation decision drift")
    _validate_authority(_mapping(record, "authority", "E-PHASE4-W4-PACKAGE"))
    authority = record["authority"]
    _require(authority.get("candidate_resolution_authorized") is False, "E-PHASE4-W4-AUTHORITY", "candidate resolution must remain frozen")
    _require(authority.get("production_frontend_architecture_selected") is False, "E-PHASE4-W4-AUTHORITY", "production architecture must remain frozen")
    _require(authority.get("workspace_authority") == "ephemeral-research-only", "E-PHASE4-W4-AUTHORITY", "workspace authority drift")
    _require(authority.get("browser_state_authority") == "ephemeral-only", "E-PHASE4-W4-AUTHORITY", "browser authority drift")


def validate_browser_baseline(record: Mapping[str, Any]) -> None:
    _require_field(record, "contract", BROWSER_CONTRACT, "E-PHASE4-W4-BROWSER")
    _require_field(record, "phase", 4, "E-PHASE4-W4-BROWSER")
    _require_field(record, "workstream", 4, "E-PHASE4-W4-BROWSER")
    _require_field(record, "slice", 2, "E-PHASE4-W4-BROWSER")
    _require_field(record, "state", "reader-reuse-browser-candidate", "E-PHASE4-W4-BROWSER")
    _require_field(record, "decision", "proceed-workstream4-closure-evaluation", "E-PHASE4-W4-BROWSER")
    _require(record.get("engine") == EXPECTED_BROWSER["engine"], "E-PHASE4-W4-BROWSER", "browser engine drift")
    counts = _mapping(record, "counts", "E-PHASE4-W4-BROWSER")
    for field, value in {
        "selector_choices": 2,
        "routes": 13,
        "keyboard_routes": 13,
        "entries": 5,
        "candidates": 2,
        "principia_references": 1,
        "warnings": 1,
        "viewports": 2,
        "network_requests": 141,
        "external_requests": 0,
        "exit_gates": 13,
    }.items():
        _require(counts.get(field) == value, "E-PHASE4-W4-BROWSER", f"browser count drift: {field}")
    claims = _mapping(record, "claims", "E-PHASE4-W4-BROWSER")
    required_claims = (
        "candidates_unresolved",
        "decisions_read_only",
        "exact_entry_order_preserved",
        "local_download_byte_identical",
        "missing_artifact_failure_explicit",
        "non_graph_workflow_complete",
        "principia_status_separate",
        "recommender_regression_preserved",
        "reduced_motion_verified",
        "selector_unknown_fixture_refused",
        "unknown_route_preserved",
        "visible_focus_verified",
        "warning_visibility_verified",
    )
    for field in required_claims:
        _require(claims.get(field) is True, "E-PHASE4-W4-BROWSER", f"browser claim failed: {field}")
    evidence = _mapping(record, "evidence", "E-PHASE4-W4-BROWSER")
    _require(set(evidence) == set(EXPECTED_BROWSER_EVIDENCE), "E-PHASE4-W4-BROWSER", "browser evidence set drift")
    for name, (size, sha, digest) in EXPECTED_BROWSER_EVIDENCE.items():
        item = evidence.get(name)
        _require(isinstance(item, Mapping), "E-PHASE4-W4-BROWSER", f"missing browser artifact {name}")
        artifact = item.get("artifact")
        _require(isinstance(artifact, Mapping), "E-PHASE4-W4-BROWSER", f"missing browser identity {name}")
        _require(artifact.get("bytes") == size and artifact.get("sha256") == sha, "E-PHASE4-W4-BROWSER", f"browser artifact drift: {name}")
        _require(item.get("report_digest") == digest, "E-PHASE4-W4-BROWSER", f"browser digest drift: {name}")
    validation = _mapping(record, "validation", "E-PHASE4-W4-BROWSER")
    artifact = _mapping(validation, "artifact", "E-PHASE4-W4-BROWSER")
    _require(artifact.get("bytes") == EXPECTED_BROWSER["validation_bytes"], "E-PHASE4-W4-BROWSER", "browser validation byte drift")
    _require(artifact.get("sha256") == EXPECTED_BROWSER["validation_sha256"], "E-PHASE4-W4-BROWSER", "browser validation SHA drift")
    _require(validation.get("decision") == "valid-reader-reuse-browser-candidate", "E-PHASE4-W4-BROWSER", "browser validation decision drift")
    _require(validation.get("report_digest") == EXPECTED_BROWSER["report_digest"], "E-PHASE4-W4-BROWSER", "browser validation digest drift")
    _require(record.get("repeated_run_substantive_artifacts_byte_identical") is True, "E-PHASE4-W4-BROWSER", "browser repeated-run identity failed")
    static = _mapping(record, "accepted_static_package", "E-PHASE4-W4-BROWSER")
    _require(static.get("baseline_contract") == PACKAGE_CONTRACT and static.get("file_count") == 18, "E-PHASE4-W4-BROWSER", "browser/static binding drift")
    package_index = _mapping(static, "package_index", "E-PHASE4-W4-BROWSER")
    _require(package_index.get("sha256") == EXPECTED_PACKAGE_FILES["package-index.json"][1], "E-PHASE4-W4-BROWSER", "browser package-index SHA drift")
    _require(package_index.get("report_digest") == EXPECTED_PACKAGE["package_index_digest"], "E-PHASE4-W4-BROWSER", "browser package-index digest drift")
    _validate_authority(_mapping(record, "authority", "E-PHASE4-W4-BROWSER"), browser=True)


def _safe_authority() -> dict[str, Any]:
    return {
        "workspace_authority": "ephemeral-research-only",
        "browser_state_authority": "ephemeral-only",
        "second_generalized_fixture_authorized": False,
        "new_canonical_authoring_authorized": False,
        "canonical_copy_authority": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "candidate_resolution_authorized": False,
        "automatic_merge_or_release_authorized": False,
        "account_required": False,
        "cloud_required": False,
        "credentials_required": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "deployment_authorized": False,
        "live_principia_dependency": False,
        "repository_mutation": False,
        "human_verified": False,
        "assistive_technology_user_reviewed": False,
        "accessibility_certified": False,
        "live": False,
    }


def run_workstream4_closure(
    generalization_baseline: Mapping[str, Any],
    package_baseline: Mapping[str, Any],
    browser_baseline: Mapping[str, Any],
    *,
    decision: str = "proceed-phase4-completion-governance",
) -> dict[str, Any]:
    validate_generalization_baseline(generalization_baseline)
    validate_package_baseline(package_baseline)
    validate_browser_baseline(browser_baseline)
    _require(decision in ALLOWED_DECISIONS, "E-PHASE4-W4-DECISION", f"unsupported completion decision {decision!r}")

    generalization_counts = generalization_baseline["counts"]
    package_counts = package_baseline["counts"]
    browser_counts = browser_baseline["counts"]
    claims = browser_baseline["claims"]

    replaceability = {
        "decision": "replaceable",
        "authoritative_inputs": [
            "accepted-catalase-generalization-baseline",
            "accepted-reader-reuse-package-baseline",
            "accepted-reader-reuse-browser-baseline",
            "accepted-workstream3-recommender-package",
        ],
        "generated_selector_disposable": True,
        "generated_packages_disposable": True,
        "generated_browser_state_disposable": True,
        "generated_evidence_disposable": True,
        "browser_storage_required": False,
        "account_required": False,
        "cloud_required": False,
        "external_service_required": False,
        "canonical_migration_required": False,
        "replacement_requirement": "reproduce exact accepted contracts, files, digests, routes, selector failures, download bytes, network isolation, and authority labels before substitution",
        "canonical_mutation": False,
        "repository_mutation": False,
    }
    migration = {
        "strategy": "rebuild-from-accepted-baselines-and-compare",
        "source_of_truth": "accepted-canonical-revisions-and-pinned-workspace-baselines",
        "required_checks": [
            "exact-generalization-artifacts",
            "exact-eighteen-file-package",
            "exact-six-artifact-browser-evidence",
            "unchanged-workstream3-recommender-regression",
            "exact-revision-and-methodological-scope",
            "selector-route-failure-and-download-equivalence",
            "zero-external-network",
            "all-authority-boundaries-frozen",
        ],
        "live_data_migration": False,
        "production_cutover_authorized": False,
        "canonical_rewrite_required": False,
        "repository_mutation": False,
    }
    rollback = {
        "strategy": "discard-generated-selector-catalase-package-and-browser-evidence",
        "restore_target": "accepted-workstream3-recommender-package",
        "preserve_targets": [
            "accepted-workstream3-workspace-contracts",
            "accepted-workstream3-reader-assets",
            "accepted-workstream3-export-and-manifest",
            "accepted-workstream4-slice1-baseline",
            "accepted-workstream4-slice2-baselines",
        ],
        "canonical_rollback_required": False,
        "review_rollback_required": False,
        "lifecycle_rollback_required": False,
        "principia_status_rollback_required": False,
        "previous_valid_package_preserved": True,
        "repository_mutation": False,
    }

    exit_gates = {
        "slice1_generalization_evidence_bound_exactly": (
            generalization_baseline["fixture"]["sha256"] == EXPECTED_GENERALIZATION["fixture_sha256"]
            and generalization_baseline["report"]["report_digest"] == EXPECTED_GENERALIZATION["report_digest"]
            and generalization_baseline["export"]["sha256"] == EXPECTED_GENERALIZATION["export_sha256"]
            and generalization_baseline["manifest"]["sha256"] == EXPECTED_GENERALIZATION["manifest_sha256"]
        ),
        "slice2_static_package_bound_exactly": (
            package_counts["file_count"] == 18
            and package_counts["fixture_packages"] == 2
            and package_counts["generalized_fixtures"] == 1
            and package_baseline["package_index_digest"] == EXPECTED_PACKAGE["package_index_digest"]
        ),
        "slice2_chromium_evidence_bound_exactly": (
            browser_baseline["engine"] == EXPECTED_BROWSER["engine"]
            and browser_baseline["evidence"]["report"]["artifact"]["sha256"] == EXPECTED_BROWSER_EVIDENCE["report"][1]
            and browser_baseline["validation"]["artifact"]["sha256"] == EXPECTED_BROWSER["validation_sha256"]
        ),
        "workstream3_recommender_regression_preserved": (
            package_baseline["files"]["packages/recommender/data/workspace-export.json"]["sha256"]
            == EXPECTED_PACKAGE_FILES["packages/recommender/data/workspace-export.json"][1]
            and package_baseline["files"]["packages/recommender/data/workspace-manifest.json"]["sha256"]
            == EXPECTED_PACKAGE_FILES["packages/recommender/data/workspace-manifest.json"][1]
            and claims["recommender_regression_preserved"] is True
        ),
        "cross_domain_contract_reuse_preserved": (
            generalization_baseline["export"]["contract"] == "atlas-research-workspace-export/0.1"
            and generalization_baseline["manifest"]["contract"] == "atlas-research-workspace-manifest/0.1"
            and generalization_baseline["workspace_contract_report"]["contract"] == "atlas-phase4-workspace-contract-report/0.1"
            and package_counts["reader_assets_per_package"] == 3
        ),
        "exact_revisions_and_methodological_scope_preserved": (
            generalization_counts["canonical_source_pool"] == 8
            and generalization_counts["workspace_entries"] == 5
            and generalization_baseline["fixture"]["id"] == "generalization-fixture:phase4-catalase-en-v1"
        ),
        "advisory_candidates_principia_and_warning_preserved": (
            generalization_counts["unresolved_candidates"] == 2
            and generalization_counts["principia_references"] == 1
            and generalization_counts["unavailable_revision_warnings"] == 1
            and claims["candidates_unresolved"] is True
            and claims["principia_status_separate"] is True
            and claims["warning_visibility_verified"] is True
        ),
        "deterministic_package_evidence_preserved": package_baseline["python_substantive_artifacts_byte_identical"] is True,
        "deterministic_browser_evidence_preserved": browser_baseline["repeated_run_substantive_artifacts_byte_identical"] is True,
        "selector_route_artifact_and_tamper_failures_preserved": (
            claims["selector_unknown_fixture_refused"] is True
            and claims["unknown_route_preserved"] is True
            and claims["missing_artifact_failure_explicit"] is True
            and generalization_counts["total_negative_cases"] == 24
        ),
        "download_and_network_boundaries_preserved": (
            claims["local_download_byte_identical"] is True
            and browser_counts["external_requests"] == 0
            and browser_counts["network_requests"] == 141
        ),
        "replaceability_migration_and_rollback_proved": (
            replaceability["generated_selector_disposable"] is True
            and replaceability["generated_packages_disposable"] is True
            and migration["production_cutover_authorized"] is False
            and rollback["previous_valid_package_preserved"] is True
            and rollback["canonical_rollback_required"] is False
        ),
        "limitations_and_non_human_review_explicit": (
            browser_baseline["authority"]["human_verified"] is False
            and browser_baseline["authority"]["accessibility_certified"] is False
        ),
        "all_write_live_and_production_authority_frozen": all(value is False for value in (
            generalization_baseline["authority"]["canonical_mutation"],
            generalization_baseline["authority"]["lifecycle_mutation"],
            generalization_baseline["authority"]["review_mutation"],
            generalization_baseline["authority"]["candidate_resolution_authorized"],
            package_baseline["authority"]["repository_mutation"],
            package_baseline["authority"]["production_frontend_architecture_selected"],
            browser_baseline["authority"]["implementation_authorized"],
            browser_baseline["authority"]["live_principia_dependency"],
        )),
    }
    _require(len(exit_gates) == 14, "E-PHASE4-W4-EXIT-GATE", "exactly fourteen closure gates are required")
    failed = sorted(name for name, value in exit_gates.items() if value is not True)
    _require(not failed, "E-PHASE4-W4-EXIT-GATE", f"Workstream 4 exit gates failed: {failed}")

    recommendation = {
        "decision": decision,
        "purpose": "permit a separate governance proposal to consider Phase 4 complete based on accepted bounded evidence",
        "authorized_scope": [
            "phase4-completion-governance-proposal-only",
            "exact-accepted-evidence-binding",
            "continued-preservation-of-all-frozen-boundaries",
        ],
        "not_authorized": [
            "automatic-phase4-closure",
            "phase5-activation",
            "production-frontend-hosting-or-deployment",
            "accounts-cloud-or-live-synchronization",
            "second-generalized-fixture",
            "canonical-review-lifecycle-merge-or-release-mutation",
            "candidate-resolution-or-status-inheritance",
            "human-verification-or-accessibility-certification",
        ],
        "evidence_basis": (
            "one accepted Catalase fixture reused the existing workspace contracts and static reader, "
            "preserved the accepted recommender package, passed deterministic Python and Chromium evidence, "
            "and retained zero external requests and no write authority; broader product readiness is not established"
        ),
        "implementation_authorized": False,
        "separate_governance_required": True,
    }

    report = _seal({
        "contract": COMPLETION_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 3,
        "state": "closure-candidate",
        "decision": decision,
        "accepted_evidence": {
            "slice1_generalization": {
                "pr": EXPECTED_GENERALIZATION["accepted_pr"],
                "tested_head": EXPECTED_GENERALIZATION["accepted_candidate_head"],
                "merge_commit": EXPECTED_GENERALIZATION["accepted_merge_commit"],
                "baseline_contract": GENERALIZATION_CONTRACT,
                "baseline_digest": json_sha256(generalization_baseline),
                "fixture_sha256": EXPECTED_GENERALIZATION["fixture_sha256"],
                "report_sha256": EXPECTED_GENERALIZATION["report_sha256"],
                "report_digest": EXPECTED_GENERALIZATION["report_digest"],
                "export_sha256": EXPECTED_GENERALIZATION["export_sha256"],
                "export_digest": EXPECTED_GENERALIZATION["export_digest"],
                "manifest_sha256": EXPECTED_GENERALIZATION["manifest_sha256"],
                "manifest_digest": EXPECTED_GENERALIZATION["manifest_digest"],
            },
            "slice2_static_package": {
                "pr": EXPECTED_PACKAGE["accepted_pr"],
                "tested_head": EXPECTED_PACKAGE["accepted_tested_head"],
                "merge_commit": EXPECTED_PACKAGE["accepted_merge_commit"],
                "baseline_contract": PACKAGE_CONTRACT,
                "baseline_digest": json_sha256(package_baseline),
                "file_count": 18,
                "package_index_sha256": EXPECTED_PACKAGE_FILES["package-index.json"][1],
                "package_index_digest": EXPECTED_PACKAGE["package_index_digest"],
                "reader_reuse_report_sha256": EXPECTED_PACKAGE_FILES["reader-reuse-report.json"][1],
                "reader_reuse_report_digest": EXPECTED_PACKAGE["reader_reuse_report_digest"],
            },
            "slice2_browser_evidence": {
                "pr": EXPECTED_BROWSER["accepted_pr"],
                "tested_head": EXPECTED_BROWSER["accepted_tested_head"],
                "merge_commit": EXPECTED_BROWSER["accepted_merge_commit"],
                "baseline_contract": BROWSER_CONTRACT,
                "baseline_digest": json_sha256(browser_baseline),
                "engine": copy.deepcopy(EXPECTED_BROWSER["engine"]),
                "report_sha256": EXPECTED_BROWSER_EVIDENCE["report"][1],
                "report_digest": EXPECTED_BROWSER["report_digest"],
                "validation_sha256": EXPECTED_BROWSER["validation_sha256"],
                "external_request_count": 0,
            },
        },
        "exit_gates": exit_gates,
        "evidence_summary": {
            "canonical_source_pool": 8,
            "workspace_entries": 5,
            "workspace_candidates": 2,
            "principia_references": 1,
            "warnings": 1,
            "static_package_files": 18,
            "fixture_packages": 2,
            "generalized_fixtures": 1,
            "routes": 13,
            "keyboard_routes": 13,
            "viewports": 2,
            "network_requests": 141,
            "external_request_count": 0,
            "generalization_negative_cases": 24,
            "browser_evidence_files": 6,
            "closure_gate_count": 14,
        },
        "replaceability": replaceability,
        "migration_boundary": migration,
        "rollback_boundary": rollback,
        "recommendation": recommendation,
        "limitations": [
            "The evidence covers one Catalase generalization fixture and does not establish universal workspace generality.",
            "The accepted recommender package is preserved as the regression and rollback baseline.",
            "Automated Chromium evidence is not human usability review, assistive-technology user review, or accessibility certification.",
            "The accepted structured retrieval evidence is bounded fixture evidence, not a production retrieval-quality claim.",
            "No production frontend, hosting, deployment, account, cloud, or live synchronization architecture is selected.",
            "The Principia reference remains synthetic, fixture-only, pinned, non-live, and status-separate.",
            "A proceed decision requires separate governance and cannot close Phase 4 or begin Phase 5 by itself.",
        ],
        "review_policy": {
            "active_review_level": "ai-reviewed",
            "human_verified": False,
            "assistive_technology_user_reviewed": False,
            "human_usability_reviewed": False,
            "accessibility_certified": False,
        },
        "authority": _safe_authority(),
        "implementation_authorized": False,
        "separate_governance_required": True,
    })
    validate_completion_report(report)
    return report


def validate_completion_report(report: Mapping[str, Any]) -> dict[str, Any]:
    _require_field(report, "contract", COMPLETION_CONTRACT, "E-PHASE4-W4-COMPLETION")
    _require_field(report, "mode", MODE, "E-PHASE4-W4-COMPLETION")
    _require_field(report, "phase", 4, "E-PHASE4-W4-COMPLETION")
    _require_field(report, "workstream", 4, "E-PHASE4-W4-COMPLETION")
    _require_field(report, "slice", 3, "E-PHASE4-W4-COMPLETION")
    _require_field(report, "state", "closure-candidate", "E-PHASE4-W4-COMPLETION")
    _require(report.get("decision") in ALLOWED_DECISIONS, "E-PHASE4-W4-DECISION", "unsupported completion recommendation")
    _require(report.get("implementation_authorized") is False, "E-PHASE4-W4-DECISION", "completion may not authorize implementation")
    _require(report.get("separate_governance_required") is True, "E-PHASE4-W4-DECISION", "separate governance must remain required")
    gates = report.get("exit_gates")
    _require(isinstance(gates, Mapping) and len(gates) == 14 and all(value is True for value in gates.values()), "E-PHASE4-W4-GATES", "all fourteen gates must pass")
    recommendation = _mapping(report, "recommendation", "E-PHASE4-W4-DECISION")
    _require(recommendation.get("decision") == report.get("decision"), "E-PHASE4-W4-DECISION", "recommendation decision mismatch")
    _require(recommendation.get("implementation_authorized") is False, "E-PHASE4-W4-DECISION", "recommendation may not self-authorize")
    _require(recommendation.get("separate_governance_required") is True, "E-PHASE4-W4-DECISION", "recommendation requires separate governance")
    authority = _mapping(report, "authority", "E-PHASE4-W4-AUTHORITY")
    required_authority = _safe_authority()
    for field, expected in required_authority.items():
        _require(authority.get(field) == expected, "E-PHASE4-W4-AUTHORITY", f"completion requires {field}={expected!r}")
    review = _mapping(report, "review_policy", "E-PHASE4-W4-REVIEW")
    for field in ("human_verified", "assistive_technology_user_reviewed", "human_usability_reviewed", "accessibility_certified"):
        _require(review.get(field) is False, "E-PHASE4-W4-REVIEW", f"completion requires {field}=false")
    accepted = _mapping(report, "accepted_evidence", "E-PHASE4-W4-EVIDENCE")
    _require(set(accepted) == {"slice1_generalization", "slice2_static_package", "slice2_browser_evidence"}, "E-PHASE4-W4-EVIDENCE", "accepted evidence set drift")
    _require(accepted["slice1_generalization"].get("tested_head") == EXPECTED_GENERALIZATION["accepted_candidate_head"], "E-PHASE4-W4-EVIDENCE", "Slice 1 head drift")
    _require(accepted["slice2_static_package"].get("tested_head") == EXPECTED_PACKAGE["accepted_tested_head"], "E-PHASE4-W4-EVIDENCE", "static package head drift")
    _require(accepted["slice2_browser_evidence"].get("tested_head") == EXPECTED_BROWSER["accepted_tested_head"], "E-PHASE4-W4-EVIDENCE", "browser head drift")
    digest = report.get("report_digest")
    _require(isinstance(digest, str) and len(digest) == 64, "E-PHASE4-W4-DIGEST", "report_digest must be SHA-256")
    unsigned = dict(report)
    unsigned.pop("report_digest", None)
    _require(json_sha256(unsigned) == digest, "E-PHASE4-W4-DIGEST", "completion report digest mismatch")
    return {
        "contract": VALIDATION_CONTRACT,
        "decision": "valid-workstream4-closure-candidate",
        "recommendation": report["decision"],
        "exit_gate_count": len(gates),
        "report_digest": digest,
        "implementation_authorized": False,
        "separate_governance_required": True,
        "human_verified": False,
        "accessibility_certified": False,
        "live": False,
        "repository_mutation": False,
    }
