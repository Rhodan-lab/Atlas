#!/usr/bin/env python3
"""Validate accepted Slice 1 and Slice 2 evidence for Workstream 3 closure."""
from __future__ import annotations

from typing import Any, Mapping

from tools.phase2_kernel import KernelError
from tools.phase4_workspace_completion.constants import (
    BROWSER_BASELINE_CONTRACT,
    EXPECTED_BROWSER,
    EXPECTED_BROWSER_EVIDENCE,
    EXPECTED_SHELL,
    EXPECTED_WORKSPACE,
    SHELL_BASELINE_CONTRACT,
    WORKSPACE_BASELINE_CONTRACT,
    _require,
    _require_artifact,
    _require_mapping,
)


def validate_workspace_baseline(record: Mapping[str, Any]) -> None:
    code = "E-PHASE4-W3-WORKSPACE"
    _require(record, "contract", WORKSPACE_BASELINE_CONTRACT, code)
    _require(record, "python_substantive_artifacts_byte_identical", True, code)

    fixture = _require_mapping(record.get("fixture"), code, "workspace fixture identity is required")
    _require(fixture, "contract", "atlas-phase4-workspace-fixtures/0.1", code)
    _require(fixture, "bytes", EXPECTED_WORKSPACE["fixture_bytes"], code)
    _require(fixture, "sha256", EXPECTED_WORKSPACE["fixture_sha256"], code)

    report = _require_mapping(record.get("report"), code, "workspace report identity is required")
    _require_artifact(
        report,
        expected_bytes=EXPECTED_WORKSPACE["report_bytes"],
        expected_sha256=EXPECTED_WORKSPACE["report_sha256"],
        code=code,
    )
    _require(report, "report_digest", EXPECTED_WORKSPACE["report_digest"], code)
    report_record = _require_mapping(report.get("record"), code, "workspace report record is required")
    required_report = {
        "contract": "atlas-phase4-workspace-contract-report/0.1",
        "decision": "workspace-contract-candidate",
        "deterministic_export": True,
        "exact_revision_preserved": True,
        "non_graph_workflow_complete": True,
        "principia_status_separate": True,
        "replaceable": True,
        "workspace_authority": "ephemeral-research-only",
        "canonical_copy_authority": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "automatic_merge_or_resolution": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "live": False,
        "repository_mutation": False,
    }
    for field, expected in required_report.items():
        _require(report_record, field, expected, code)
    if report_record.get("counts") != {
        "candidates": 2,
        "entries": 5,
        "negative_cases": 10,
        "open_questions": 2,
        "principia_references": 1,
        "warnings": 1,
    }:
        raise KernelError(code, "workspace report counts differ from accepted evidence")

    export = _require_mapping(record.get("export"), code, "workspace export identity is required")
    _require_artifact(
        export,
        expected_bytes=EXPECTED_WORKSPACE["export_bytes"],
        expected_sha256=EXPECTED_WORKSPACE["export_sha256"],
        code=code,
    )
    _require(export, "contract", "atlas-research-workspace-export/0.1", code)
    _require(export, "report_digest", EXPECTED_WORKSPACE["export_digest"], code)
    _require(export, "entry_count", 5, code)
    _require(export, "candidate_count", 2, code)
    _require(export, "principia_reference_count", 1, code)
    _require(export, "warning_count", 1, code)

    manifest = _require_mapping(record.get("manifest"), code, "workspace manifest identity is required")
    _require_artifact(
        manifest,
        expected_bytes=EXPECTED_WORKSPACE["manifest_bytes"],
        expected_sha256=EXPECTED_WORKSPACE["manifest_sha256"],
        code=code,
    )
    _require(manifest, "contract", "atlas-research-workspace-manifest/0.1", code)
    _require(manifest, "report_digest", EXPECTED_WORKSPACE["manifest_digest"], code)
    _require(manifest, "file_count", 1, code)


def validate_shell_baseline(record: Mapping[str, Any]) -> None:
    code = "E-PHASE4-W3-SHELL"
    _require(record, "contract", SHELL_BASELINE_CONTRACT, code)
    _require(record, "python_substantive_artifacts_byte_identical", True, code)

    shell_data = _require_mapping(record.get("shell_data"), code, "workspace shell data is required")
    _require_artifact(
        shell_data,
        expected_bytes=EXPECTED_SHELL["shell_data_bytes"],
        expected_sha256=EXPECTED_SHELL["shell_data_sha256"],
        code=code,
    )
    _require(shell_data, "build_digest", EXPECTED_SHELL["shell_build_digest"], code)
    shell_record = _require_mapping(shell_data.get("record"), code, "workspace shell record is required")
    _require(shell_record, "contract", "atlas-workspace-shell-data/0.1", code)
    _require(shell_record, "state", "workspace-shell-candidate", code)
    _require(shell_record, "build_digest", EXPECTED_SHELL["shell_build_digest"], code)
    if shell_record.get("counts") != {
        "candidates": 2,
        "entries": 5,
        "limitations": 5,
        "open_questions": 2,
        "principia_references": 1,
        "routes": 13,
        "warnings": 1,
    }:
        raise KernelError(code, "workspace shell counts differ from accepted evidence")
    authority = _require_mapping(shell_record.get("authority"), code, "workspace shell authority is required")
    required_authority = {
        "workspace_authority": "ephemeral-research-only",
        "browser_state_authority": "ephemeral-only",
        "accepted_export_only": True,
        "exact_revision_required": True,
        "entry_order_preserved": True,
        "decisions_read_only": True,
        "candidates_unresolved": True,
        "principia_status_separate": True,
        "keyboard_workflow_required": True,
        "non_graph_workflow_required": True,
        "reduced_motion_required": True,
        "zero_external_requests_required": True,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
    }
    for field, expected in required_authority.items():
        _require(authority, field, expected, code)
    download = _require_mapping(shell_record.get("download"), code, "workspace shell download identity is required")
    _require(download, "bytes", EXPECTED_WORKSPACE["export_bytes"], code)
    _require(download, "sha256", EXPECTED_WORKSPACE["export_sha256"], code)
    _require(download, "local_only", True, code)
    _require(download, "canonical_write", False, code)
    routes = shell_record.get("routes")
    if not isinstance(routes, list) or len(routes) != EXPECTED_SHELL["route_count"]:
        raise KernelError(code, "workspace shell route set differs from accepted evidence")
    entry_routes = [route for route in routes if isinstance(route, Mapping) and route.get("kind") == "entry"]
    if [route.get("position") for route in entry_routes] != [1, 2, 3, 4, 5]:
        raise KernelError(code, "workspace shell entry order differs from accepted evidence")

    build_report = _require_mapping(record.get("build_report"), code, "workspace shell build report is required")
    _require_artifact(
        build_report,
        expected_bytes=EXPECTED_SHELL["report_bytes"],
        expected_sha256=EXPECTED_SHELL["report_sha256"],
        code=code,
    )
    _require(build_report, "report_digest", EXPECTED_SHELL["report_digest"], code)
    build_record = _require_mapping(build_report.get("record"), code, "workspace shell build record is required")
    required_build = {
        "contract": "atlas-workspace-shell-build-report/0.1",
        "decision": "workspace-shell-candidate",
        "route_count": 13,
        "entry_route_count": 5,
        "replaceable": True,
        "local_first": True,
        "api_required": False,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "canonical_mutation": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
    }
    for field, expected in required_build.items():
        _require(build_record, field, expected, code)

    static_assets = _require_mapping(record.get("static_assets"), code, "workspace shell static assets are required")
    index = _require_mapping(static_assets.get("index.html"), code, "workspace shell index identity is required")
    _require(index, "bytes", EXPECTED_SHELL["index_bytes"], code)
    _require(index, "sha256", EXPECTED_SHELL["index_sha256"], code)


def validate_browser_baseline(record: Mapping[str, Any]) -> None:
    code = "E-PHASE4-W3-BROWSER"
    _require(record, "contract", BROWSER_BASELINE_CONTRACT, code)
    _require(record, "phase", 4, code)
    _require(record, "workstream", 3, code)
    _require(record, "slice", 2, code)
    _require(record, "state", "workspace-browser-candidate", code)
    _require(record, "repeated_run_substantive_artifacts_byte_identical", True, code)
    if record.get("engine") != EXPECTED_BROWSER["engine"]:
        raise KernelError(code, "workspace browser engine differs from accepted evidence")
    if record.get("counts") != {
        "candidates": 2,
        "entries": 5,
        "external_requests": 0,
        "keyboard_routes": 13,
        "principia_references": 1,
        "routes": 13,
        "viewports": 2,
        "warnings": 1,
    }:
        raise KernelError(code, "workspace browser counts differ from accepted evidence")

    claims = _require_mapping(record.get("claims"), code, "workspace browser claims are required")
    expected_claims = {
        "candidates_unresolved": True,
        "decisions_read_only": True,
        "exact_entry_order_preserved": True,
        "local_download_byte_identical": True,
        "missing_artifact_failure_explicit": True,
        "non_graph_workflow_complete": True,
        "principia_status_separate": True,
        "reduced_motion_verified": True,
        "unknown_route_preserved": True,
        "visible_focus_verified": True,
        "warning_visibility_verified": True,
    }
    for field, expected in expected_claims.items():
        _require(claims, field, expected, code)

    authority = _require_mapping(record.get("authority"), code, "workspace browser authority is required")
    expected_authority = {
        "accessibility_certified": False,
        "browser_state_authority": "ephemeral-only",
        "canonical_mutation": False,
        "human_verified": False,
        "lifecycle_mutation": False,
        "live": False,
        "live_principia_dependency": False,
        "production_frontend_architecture_selected": False,
        "repository_mutation": False,
        "review_mutation": False,
    }
    for field, expected in expected_authority.items():
        _require(authority, field, expected, code)

    evidence = _require_mapping(record.get("evidence"), code, "workspace browser evidence identities are required")
    if set(evidence) != set(EXPECTED_BROWSER_EVIDENCE):
        raise KernelError(code, "workspace browser evidence file set differs from accepted evidence")
    for name, expected in EXPECTED_BROWSER_EVIDENCE.items():
        item = _require_mapping(evidence.get(name), code, f"workspace browser evidence {name!r} is required")
        contract, artifact_bytes, artifact_sha, digest = expected
        _require(item, "contract", contract, code)
        _require_artifact(item, expected_bytes=artifact_bytes, expected_sha256=artifact_sha, code=code)
        _require(item, "report_digest", digest, code)

    validation = _require_mapping(record.get("validation"), code, "workspace browser validation is required")
    _require(validation, "contract", "atlas-phase4-workspace-browser-validation/0.1", code)
    _require(validation, "decision", "valid-workspace-browser-candidate", code)
    _require(validation, "report_digest", EXPECTED_BROWSER["report_digest"], code)

    accepted = _require_mapping(record.get("accepted_workspace"), code, "accepted workspace identities are required")
    for name, expected_contract, expected_bytes, expected_sha, expected_digest in (
        ("export", "atlas-research-workspace-export/0.1", EXPECTED_WORKSPACE["export_bytes"], EXPECTED_WORKSPACE["export_sha256"], EXPECTED_WORKSPACE["export_digest"]),
        ("manifest", "atlas-research-workspace-manifest/0.1", EXPECTED_WORKSPACE["manifest_bytes"], EXPECTED_WORKSPACE["manifest_sha256"], EXPECTED_WORKSPACE["manifest_digest"]),
    ):
        item = _require_mapping(accepted.get(name), code, f"accepted workspace {name} identity is required")
        _require(item, "contract", expected_contract, code)
        _require_artifact(item, expected_bytes=expected_bytes, expected_sha256=expected_sha, code=code)
        _require(item, "report_digest", expected_digest, code)
