#!/usr/bin/env python3
"""Independently validate Workstream 4 static-reader reuse browser evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, render_json

FILES = {
    "workflow": "reader-reuse-browser-workflows.json",
    "accessibility": "reader-reuse-browser-accessibility.json",
    "network": "reader-reuse-browser-network.json",
    "failure": "reader-reuse-browser-failures.json",
    "manifest": "reader-reuse-browser-manifest.json",
    "report": "reader-reuse-browser-report.json",
}
CONTRACTS = {
    "workflow": "atlas-workspace-reader-reuse-browser-workflow-evidence/0.1",
    "accessibility": "atlas-workspace-reader-reuse-browser-accessibility-report/0.1",
    "network": "atlas-workspace-reader-reuse-browser-network-report/0.1",
    "failure": "atlas-workspace-reader-reuse-browser-failure-evidence/0.1",
    "manifest": "atlas-phase4-workspace-reader-reuse-browser-manifest/0.1",
    "report": "atlas-phase4-workspace-reader-reuse-browser-report/0.1",
}
VALIDATION_CONTRACT = "atlas-phase4-workspace-reader-reuse-browser-validation/0.1"


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _load(path: Path) -> tuple[dict[str, Any], bytes]:
    payload = path.read_bytes()
    try:
        value = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise KernelError("E-READER-BROWSER-JSON", f"invalid JSON in {path.name}") from exc
    if not isinstance(value, dict):
        raise KernelError("E-READER-BROWSER-JSON", f"{path.name} must contain an object")
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
    if _sha256(render_json(unsigned).encode("utf-8")) != digest:
        raise KernelError(code, "report_digest is invalid")


def validate_directory(root: Path) -> dict[str, Any]:
    records: dict[str, dict[str, Any]] = {}
    payloads: dict[str, bytes] = {}
    for key, filename in FILES.items():
        path = root / filename
        if not path.is_file():
            raise KernelError("E-READER-BROWSER-FILE", f"missing {filename}")
        records[key], payloads[key] = _load(path)
        _require(records[key], "contract", CONTRACTS[key], "E-READER-BROWSER-CONTRACT")
        _validate_seal(records[key], "E-READER-BROWSER-DIGEST")

    workflow = records["workflow"]
    accessibility = records["accessibility"]
    network = records["network"]
    failure = records["failure"]
    manifest = records["manifest"]
    report = records["report"]

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or len(artifacts) != 4:
        raise KernelError("E-READER-BROWSER-MANIFEST", "manifest requires four child artifacts")
    expected_files = {FILES[key]: key for key in ("workflow", "accessibility", "network", "failure")}
    observed: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict):
            raise KernelError("E-READER-BROWSER-MANIFEST", "manifest artifact must be an object")
        filename = artifact.get("file")
        if filename not in expected_files or filename in observed:
            raise KernelError("E-READER-BROWSER-MANIFEST", "manifest artifact set is invalid")
        observed.add(filename)
        key = expected_files[filename]
        if artifact.get("bytes") != len(payloads[key]) or artifact.get("sha256") != _sha256(payloads[key]):
            raise KernelError("E-READER-BROWSER-MANIFEST", f"artifact identity mismatch for {filename}")
        if artifact.get("report_digest") != records[key]["report_digest"] or artifact.get("contract") != records[key]["contract"]:
            raise KernelError("E-READER-BROWSER-MANIFEST", f"semantic identity mismatch for {filename}")
    if observed != set(expected_files):
        raise KernelError("E-READER-BROWSER-MANIFEST", "manifest does not bind every child artifact")

    _require(workflow, "engine_name", "chromium", "E-READER-BROWSER-ENGINE")
    _require(workflow, "playwright_version", "1.62.0", "E-READER-BROWSER-ENGINE")
    _require(workflow, "route_count", 13, "E-READER-BROWSER-WORKFLOW")
    routes = workflow.get("route_records")
    if not isinstance(routes, list) or len(routes) != 13:
        raise KernelError("E-READER-BROWSER-WORKFLOW", "Catalase workflow requires thirteen route records")
    if [item.get("route_id") for item in routes] != workflow.get("route_order"):
        raise KernelError("E-READER-BROWSER-WORKFLOW", "route records must preserve route order")
    if not all(item.get("focus_visible") is True and item.get("outcome") == "pass" for item in routes):
        raise KernelError("E-READER-BROWSER-FOCUS", "every Catalase route requires visible focus")
    entry_routes = [item for item in routes if item.get("kind") == "entry"]
    if len(entry_routes) != 5:
        raise KernelError("E-READER-BROWSER-ENTRY", "Catalase workflow requires five entry routes")
    if not all(item.get("decision") in {"include", "exclude", "context"} and item.get("decision_read_only") is True and item.get("exact_reference") for item in entry_routes):
        raise KernelError("E-READER-BROWSER-ENTRY", "Catalase entries must expose exact read-only decisions")
    selector = workflow.get("selector")
    if not isinstance(selector, dict):
        raise KernelError("E-READER-BROWSER-SELECTOR", "selector evidence is required")
    choices = selector.get("choices")
    if not isinstance(choices, list) or [item.get("fixture") for item in choices] != ["recommender", "catalase"]:
        raise KernelError("E-READER-BROWSER-SELECTOR", "selector choices differ from accepted package index")
    if selector.get("known_selector", {}).get("outcome") != "pass":
        raise KernelError("E-READER-BROWSER-SELECTOR", "known Catalase selector must pass")
    unknown = selector.get("unknown_selector", {})
    if unknown.get("outcome") != "rejected-preserved" or unknown.get("fallback") != "refused" or unknown.get("package_mutation") != "none":
        raise KernelError("E-READER-BROWSER-SELECTOR", "unknown selector must reject without fallback or mutation")
    if workflow.get("recommender_regression", {}).get("outcome") != "pass":
        raise KernelError("E-READER-BROWSER-REGRESSION", "recommender regression must pass")
    for field, expected in {
        "exact_entry_order_preserved": True,
        "decisions_read_only": True,
        "candidates_unresolved": True,
        "principia_status_separate": True,
        "warning_visible": True,
        "non_graph_workflow_complete": True,
        "selector_fallback_refused": True,
        "accepted_reader_assets_reused": True,
        "browser_state_authority": "ephemeral-only",
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live": False,
    }.items():
        _require(workflow, field, expected, "E-READER-BROWSER-AUTHORITY")
    download = workflow.get("local_download")
    if not isinstance(download, dict) or download.get("byte_identical") is not True or download.get("sha256") != download.get("accepted_sha256"):
        raise KernelError("E-READER-BROWSER-DOWNLOAD", "Catalase download must match accepted export")

    for field, expected in {
        "selector_document_language": "en",
        "selector_first_heading_level": 1,
        "selector_skip_link_focus_visible": True,
        "selector_target_focus_visible": True,
        "selector_known_fixture_focus_visible": True,
        "catalase_document_language": "en",
        "catalase_first_heading_level": 1,
        "catalase_named_buttons": True,
        "catalase_skip_link_focus_visible": True,
        "catalase_skip_target_focus_visible": True,
        "keyboard_route_count": 13,
        "all_route_focus_visible": True,
        "reduced_motion_verified": True,
        "mobile_no_horizontal_overflow": True,
        "human_verified": False,
        "assistive_technology_user_reviewed": False,
        "accessibility_certified": False,
        "live": False,
        "repository_mutation": False,
    }.items():
        _require(accessibility, field, expected, "E-READER-BROWSER-ACCESSIBILITY")
    if accessibility.get("catalase_landmarks") != {"banner": 1, "navigation": 1, "main": 1, "contentinfo": 1}:
        raise KernelError("E-READER-BROWSER-ACCESSIBILITY", "Catalase landmark counts are invalid")

    _require(network, "external_request_count", 0, "E-READER-BROWSER-NETWORK")
    _require(network, "external_network_allowed", False, "E-READER-BROWSER-NETWORK")
    for field in ("credentials_used", "remote_assets_used", "analytics_used", "cloud_service_used", "account_required", "live", "repository_mutation"):
        _require(network, field, False, "E-READER-BROWSER-NETWORK")
    requests = network.get("requests")
    if not isinstance(requests, list) or not requests or any(item.get("decision") == "blocked-external" for item in requests):
        raise KernelError("E-READER-BROWSER-NETWORK", "network evidence must contain loopback-only requests")
    if network.get("blocked_test_loopback_count") != 1:
        raise KernelError("E-READER-BROWSER-NETWORK", "missing-artifact test must block one Catalase artifact")

    if failure.get("unknown_selector", {}).get("outcome") != "rejected-preserved":
        raise KernelError("E-READER-BROWSER-FAILURE", "unknown selector failure must preserve state")
    if failure.get("unknown_catalase_route", {}).get("outcome") != "rejected-preserved":
        raise KernelError("E-READER-BROWSER-FAILURE", "unknown Catalase route must preserve state")
    if failure.get("missing_catalase_artifact", {}).get("outcome") != "rejected-preserved":
        raise KernelError("E-READER-BROWSER-FAILURE", "missing Catalase artifact must preserve state")
    _require(failure, "recommender_prior_valid_package_preserved", True, "E-READER-BROWSER-FAILURE")
    _require(failure, "silent_fallback_used", False, "E-READER-BROWSER-FAILURE")
    for field in ("canonical_mutation", "lifecycle_mutation", "review_mutation", "repository_mutation", "live"):
        _require(failure, field, False, "E-READER-BROWSER-FAILURE")

    _require(manifest, "engine_name", "chromium", "E-READER-BROWSER-ENGINE")
    _require(manifest, "playwright_version", "1.62.0", "E-READER-BROWSER-ENGINE")
    _require(manifest, "repeated_run_byte_identity_required", True, "E-READER-BROWSER-MANIFEST")
    for field in ("screenshots_authoritative", "external_network_allowed", "production_frontend_architecture_selected", "live", "repository_mutation"):
        _require(manifest, field, False, "E-READER-BROWSER-MANIFEST")

    _require(report, "state", "reader-reuse-browser-candidate", "E-READER-BROWSER-REPORT")
    _require(report, "decision", "proceed-workstream4-closure-evaluation", "E-READER-BROWSER-DECISION")
    _require(report, "implementation_authorized", False, "E-READER-BROWSER-DECISION")
    _require(report, "separate_governance_required", True, "E-READER-BROWSER-DECISION")
    for field, expected in {
        "selector_choice_count": 2,
        "route_count": 13,
        "keyboard_route_count": 13,
        "entry_count": 5,
        "candidate_count": 2,
        "principia_reference_count": 1,
        "warning_count": 1,
        "viewport_count": 2,
        "external_request_count": 0,
        "local_download_byte_identical": True,
        "recommender_regression_preserved": True,
        "selector_unknown_fixture_refused": True,
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
        "candidate_resolution_authorized": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "live": False,
    }.items():
        _require(report, field, expected, "E-READER-BROWSER-REPORT")
    gates = report.get("exit_gates")
    if not isinstance(gates, dict) or len(gates) != 13 or not all(value is True for value in gates.values()):
        raise KernelError("E-READER-BROWSER-GATES", "all thirteen Slice 2 gates must pass")
    expected_child_digests = {
        "workflow": workflow["report_digest"],
        "accessibility": accessibility["report_digest"],
        "network": network["report_digest"],
        "failure": failure["report_digest"],
        "manifest": manifest["report_digest"],
    }
    if report.get("child_digests") != expected_child_digests:
        raise KernelError("E-READER-BROWSER-REPORT", "report child digest binding is invalid")
    if report.get("package_index_sha256") != manifest.get("package_index", {}).get("artifact", {}).get("sha256"):
        raise KernelError("E-READER-BROWSER-REPORT", "package index identity differs from manifest")
    if report.get("accepted_catalase_export_sha256") != manifest.get("accepted_catalase_export", {}).get("artifact", {}).get("sha256"):
        raise KernelError("E-READER-BROWSER-REPORT", "Catalase export identity differs from manifest")

    return {
        "contract": VALIDATION_CONTRACT,
        "decision": "valid-reader-reuse-browser-candidate",
        "recommendation": report["decision"],
        "engine_name": report["engine_name"],
        "engine_version": report["engine_version"],
        "playwright_version": report["playwright_version"],
        "selector_choice_count": 2,
        "route_count": 13,
        "exit_gate_count": 13,
        "external_request_count": 0,
        "local_download_byte_identical": True,
        "human_verified": False,
        "accessibility_certified": False,
        "implementation_authorized": False,
        "canonical_mutation": False,
        "repository_mutation": False,
        "report_digest": report["report_digest"],
    }


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
