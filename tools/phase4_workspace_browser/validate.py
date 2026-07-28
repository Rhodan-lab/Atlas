#!/usr/bin/env python3
"""Independently validate Phase 4 workspace browser evidence artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, render_json

FILES = {
    "workflow": "workspace-browser-workflows.json",
    "accessibility": "workspace-browser-accessibility.json",
    "network": "workspace-browser-network.json",
    "failure": "workspace-browser-failures.json",
    "manifest": "workspace-browser-manifest.json",
    "report": "workspace-browser-report.json",
}
CONTRACTS = {
    "workflow": "atlas-workspace-browser-workflow-evidence/0.1",
    "accessibility": "atlas-workspace-browser-accessibility-report/0.1",
    "network": "atlas-workspace-browser-network-report/0.1",
    "failure": "atlas-workspace-browser-failure-evidence/0.1",
    "manifest": "atlas-phase4-workspace-browser-manifest/0.1",
    "report": "atlas-phase4-workspace-browser-report/0.1",
}
VALIDATION_CONTRACT = "atlas-phase4-workspace-browser-validation/0.1"


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _json_sha256(value: Any) -> str:
    return _sha256(render_json(value).encode("utf-8"))


def _load(path: Path) -> tuple[dict[str, Any], bytes]:
    payload = path.read_bytes()
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise KernelError("E-WS-BROWSER-JSON", f"invalid JSON in {path.name}") from exc
    if not isinstance(value, dict):
        raise KernelError("E-WS-BROWSER-JSON", f"{path.name} must contain an object")
    return value, payload


def _require(record: Mapping[str, Any], field: str, expected: Any, code: str) -> None:
    if record.get(field) != expected:
        raise KernelError(code, f"expected {field}={expected!r}")


def _validate_seal(record: Mapping[str, Any], code: str) -> None:
    digest = record.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError(code, "report_digest must be SHA-256")
    unsigned = dict(record)
    unsigned.pop("report_digest", None)
    if _json_sha256(unsigned) != digest:
        raise KernelError(code, "report_digest is invalid")


def validate_directory(root: Path) -> dict[str, Any]:
    records: dict[str, dict[str, Any]] = {}
    payloads: dict[str, bytes] = {}
    for key, filename in FILES.items():
        path = root / filename
        if not path.is_file():
            raise KernelError("E-WS-BROWSER-FILE", f"missing {filename}")
        records[key], payloads[key] = _load(path)
        _require(records[key], "contract", CONTRACTS[key], "E-WS-BROWSER-CONTRACT")
        _validate_seal(records[key], "E-WS-BROWSER-DIGEST")

    workflow = records["workflow"]
    accessibility = records["accessibility"]
    network = records["network"]
    failure = records["failure"]
    manifest = records["manifest"]
    report = records["report"]

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 4:
        raise KernelError("E-WS-BROWSER-MANIFEST", "manifest requires four child artifacts")
    expected_files = {FILES[key]: key for key in ("workflow", "accessibility", "network", "failure")}
    observed_files: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise KernelError("E-WS-BROWSER-MANIFEST", "manifest artifact must be an object")
        filename = artifact.get("file")
        if filename not in expected_files or filename in observed_files:
            raise KernelError("E-WS-BROWSER-MANIFEST", "manifest artifact set is invalid")
        observed_files.add(filename)
        key = expected_files[filename]
        if artifact.get("bytes") != len(payloads[key]) or artifact.get("sha256") != _sha256(payloads[key]):
            raise KernelError("E-WS-BROWSER-MANIFEST", f"manifest bytes or SHA mismatch for {filename}")
        if artifact.get("report_digest") != records[key]["report_digest"] or artifact.get("contract") != records[key]["contract"]:
            raise KernelError("E-WS-BROWSER-MANIFEST", f"manifest semantic identity mismatch for {filename}")
    if observed_files != set(expected_files):
        raise KernelError("E-WS-BROWSER-MANIFEST", "manifest does not bind every child artifact")

    _require(workflow, "engine_name", "chromium", "E-WS-BROWSER-ENGINE")
    _require(workflow, "playwright_version", "1.62.0", "E-WS-BROWSER-ENGINE")
    _require(workflow, "route_count", 13, "E-WS-BROWSER-WORKFLOW")
    routes = workflow.get("route_records")
    if not isinstance(routes, list) or len(routes) != 13:
        raise KernelError("E-WS-BROWSER-WORKFLOW", "workflow requires thirteen route records")
    if [item.get("route_id") for item in routes] != workflow.get("route_order"):
        raise KernelError("E-WS-BROWSER-WORKFLOW", "route records must preserve route order")
    if not all(item.get("focus_visible") is True and item.get("outcome") == "pass" for item in routes):
        raise KernelError("E-WS-BROWSER-FOCUS", "every route requires visible focus and passing evidence")
    entry_routes = [item for item in routes if item.get("kind") == "entry"]
    if len(entry_routes) != 5 or [item.get("decision") for item in entry_routes] != ["include", "include", "context", "exclude", "context"]:
        raise KernelError("E-WS-BROWSER-ENTRY", "entry order and decisions must match the accepted export")
    if not all(item.get("decision_read_only") is True and item.get("exact_reference") for item in entry_routes):
        raise KernelError("E-WS-BROWSER-ENTRY", "entry decisions must be read-only and exact-revision")
    required_workflow = {
        "exact_entry_order_preserved": True,
        "decisions_read_only": True,
        "candidates_unresolved": True,
        "principia_status_separate": True,
        "warning_visible": True,
        "non_graph_workflow_complete": True,
        "browser_state_authority": "ephemeral-only",
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live": False,
    }
    for field, expected in required_workflow.items():
        _require(workflow, field, expected, "E-WS-BROWSER-AUTHORITY")
    download = workflow.get("local_download")
    if not isinstance(download, dict) or download.get("byte_identical") is not True or download.get("sha256") != download.get("accepted_sha256"):
        raise KernelError("E-WS-BROWSER-DOWNLOAD", "local download must match accepted export bytes")
    if download.get("bytes") != download.get("accepted_bytes") or download.get("network_required") is not False or download.get("repository_mutation") is not False:
        raise KernelError("E-WS-BROWSER-DOWNLOAD", "download boundary is unsafe")

    required_accessibility = {
        "document_language": "en",
        "first_heading_level": 1,
        "named_buttons": True,
        "skip_link_focus_visible": True,
        "skip_target_focus_visible": True,
        "keyboard_route_count": 13,
        "all_route_focus_visible": True,
        "reduced_motion_verified": True,
        "mobile_no_horizontal_overflow": True,
        "human_verified": False,
        "assistive_technology_user_reviewed": False,
        "accessibility_certified": False,
        "live": False,
        "repository_mutation": False,
    }
    for field, expected in required_accessibility.items():
        _require(accessibility, field, expected, "E-WS-BROWSER-ACCESSIBILITY")
    if accessibility.get("landmarks") != {"banner": 1, "navigation": 1, "main": 1, "contentinfo": 1}:
        raise KernelError("E-WS-BROWSER-ACCESSIBILITY", "primary landmark counts are invalid")

    _require(network, "external_request_count", 0, "E-WS-BROWSER-NETWORK")
    _require(network, "external_network_allowed", False, "E-WS-BROWSER-NETWORK")
    for field in ("credentials_used", "remote_assets_used", "analytics_used", "cloud_service_used", "account_required", "live", "repository_mutation"):
        _require(network, field, False, "E-WS-BROWSER-NETWORK")
    requests = network.get("requests")
    if not isinstance(requests, list) or not requests:
        raise KernelError("E-WS-BROWSER-NETWORK", "network evidence requires request records")
    if any(item.get("decision") == "blocked-external" for item in requests):
        raise KernelError("E-WS-BROWSER-NETWORK", "external request was attempted")
    if network.get("blocked_test_loopback_count") != 1:
        raise KernelError("E-WS-BROWSER-NETWORK", "missing-artifact test must block one loopback artifact")

    _require(failure, "prior_valid_view_preserved", True, "E-WS-BROWSER-FAILURE")
    _require(failure, "silent_fallback_used", False, "E-WS-BROWSER-FAILURE")
    _require(failure, "implicit_latest_used", False, "E-WS-BROWSER-FAILURE")
    _require(failure, "browser_state_persisted_as_authority", False, "E-WS-BROWSER-FAILURE")
    for field in ("canonical_mutation", "lifecycle_mutation", "review_mutation", "repository_mutation", "live"):
        _require(failure, field, False, "E-WS-BROWSER-FAILURE")
    if failure.get("unknown_route", {}).get("outcome") != "rejected-preserved" or failure.get("missing_artifact", {}).get("outcome") != "rejected-preserved":
        raise KernelError("E-WS-BROWSER-FAILURE", "unknown route and missing artifact must reject while preserving state")

    _require(manifest, "engine_name", "chromium", "E-WS-BROWSER-ENGINE")
    _require(manifest, "playwright_version", "1.62.0", "E-WS-BROWSER-ENGINE")
    _require(manifest, "repeated_run_byte_identity_required", True, "E-WS-BROWSER-MANIFEST")
    for field in ("screenshots_authoritative", "external_network_allowed", "production_frontend_architecture_selected", "live", "repository_mutation"):
        _require(manifest, field, False, "E-WS-BROWSER-MANIFEST")

    _require(report, "state", "workspace-browser-candidate", "E-WS-BROWSER-REPORT")
    required_report = {
        "route_count": 13,
        "keyboard_route_count": 13,
        "entry_count": 5,
        "candidate_count": 2,
        "principia_reference_count": 1,
        "warning_count": 1,
        "viewport_count": 2,
        "external_request_count": 0,
        "local_download_byte_identical": True,
        "exact_entry_order_preserved": True,
        "decisions_read_only": True,
        "candidates_unresolved": True,
        "principia_status_separate": True,
        "warning_visibility_verified": True,
        "non_graph_workflow_complete": True,
        "visible_focus_verified": True,
        "reduced_motion_verified": True,
        "unknown_route_preserved": True,
        "missing_artifact_failure_explicit": True,
        "browser_state_authority": "ephemeral-only",
        "human_verified": False,
        "accessibility_certified": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "live": False,
    }
    for field, expected in required_report.items():
        _require(report, field, expected, "E-WS-BROWSER-REPORT")
    expected_child_digests = {
        "workflow": workflow["report_digest"],
        "accessibility": accessibility["report_digest"],
        "network": network["report_digest"],
        "failure": failure["report_digest"],
        "manifest": manifest["report_digest"],
    }
    if report.get("child_digests") != expected_child_digests:
        raise KernelError("E-WS-BROWSER-REPORT", "report child digest binding is invalid")
    if report.get("accepted_export_sha256") != manifest.get("accepted_export", {}).get("artifact", {}).get("sha256"):
        raise KernelError("E-WS-BROWSER-REPORT", "report export identity differs from manifest")
    if report.get("accepted_manifest_sha256") != manifest.get("accepted_manifest", {}).get("artifact", {}).get("sha256"):
        raise KernelError("E-WS-BROWSER-REPORT", "report accepted manifest identity differs from evidence manifest")

    result = {
        "contract": VALIDATION_CONTRACT,
        "decision": "valid-workspace-browser-candidate",
        "engine_name": report["engine_name"],
        "engine_version": report["engine_version"],
        "playwright_version": report["playwright_version"],
        "route_count": report["route_count"],
        "external_request_count": 0,
        "local_download_byte_identical": True,
        "human_verified": False,
        "accessibility_certified": False,
        "canonical_mutation": False,
        "repository_mutation": False,
        "report_digest": report["report_digest"],
    }
    return result


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_dir", type=Path)
    args = parser.parse_args(argv)
    try:
        result = validate_directory(args.evidence_dir)
    except KernelError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(render_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
