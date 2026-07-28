#!/usr/bin/env python3
"""Independent validator for deterministic workspace browser evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, render_json

CONTRACTS = {
    "workspace-browser-workflows.json": "atlas-workspace-browser-workflow-evidence/0.1",
    "workspace-browser-accessibility.json": "atlas-workspace-browser-accessibility-report/0.1",
    "workspace-browser-network.json": "atlas-workspace-browser-network-report/0.1",
    "workspace-browser-failures.json": "atlas-workspace-browser-failure-evidence/0.1",
    "workspace-browser-manifest.json": "atlas-phase4-workspace-browser-manifest/0.1",
    "workspace-browser-report.json": "atlas-phase4-workspace-browser-report/0.1",
}
MODE = "interactive-experience-foundation"


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _artifact(path: Path, record: Mapping[str, Any]) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "file": path.name,
        "contract": record["contract"],
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "report_digest": record["report_digest"],
    }


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise KernelError("E-WORKSPACE-BROWSER-FILE", f"cannot read {path.name}") from exc
    if not isinstance(value, dict):
        raise KernelError("E-WORKSPACE-BROWSER-FILE", f"{path.name} must contain an object")
    return value


def _require(record: Mapping[str, Any], field: str, expected: Any, code: str) -> None:
    if record.get(field) != expected:
        raise KernelError(code, f"expected {field}={expected!r}")


def _validate_digest(record: Mapping[str, Any], code: str) -> None:
    digest = record.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError(code, "report_digest must be SHA-256")
    unsigned = dict(record)
    unsigned.pop("report_digest", None)
    if _json_sha256(unsigned) != digest:
        raise KernelError(code, "report_digest is invalid")


def _validate_common(record: Mapping[str, Any], contract: str, code: str) -> None:
    _require(record, "contract", contract, code)
    _require(record, "mode", MODE, code)
    _require(record, "phase", 4, code)
    _require(record, "workstream", 3, code)
    _require(record, "slice", 2, code)
    _require(record, "state", "workspace-browser-evidence-candidate", code)
    _validate_digest(record, code)


def validate_directory(root: Path) -> dict[str, Any]:
    records: dict[str, dict[str, Any]] = {}
    for file_name, contract in CONTRACTS.items():
        path = root / file_name
        record = _load(path)
        _validate_common(record, contract, "E-WORKSPACE-BROWSER-CONTRACT")
        records[file_name] = record

    workflows = records["workspace-browser-workflows.json"]
    accessibility = records["workspace-browser-accessibility.json"]
    network = records["workspace-browser-network.json"]
    failures = records["workspace-browser-failures.json"]
    manifest = records["workspace-browser-manifest.json"]
    report = records["workspace-browser-report.json"]

    _require(workflows, "route_count", 13, "E-WORKSPACE-BROWSER-ROUTES")
    _require(workflows, "entry_route_count", 5, "E-WORKSPACE-BROWSER-ROUTES")
    _require(workflows, "keyboard_route_count", 13, "E-WORKSPACE-BROWSER-ROUTES")
    routes = workflows.get("routes")
    if not isinstance(routes, list) or len(routes) != 13:
        raise KernelError("E-WORKSPACE-BROWSER-ROUTES", "thirteen route records are required")
    route_ids = [item.get("route_id") for item in routes if isinstance(item, Mapping)]
    if len(route_ids) != 13 or len(route_ids) != len(set(route_ids)):
        raise KernelError("E-WORKSPACE-BROWSER-ROUTES", "route IDs must be complete and unique")
    if any(item.get("decision") != "pass" or item.get("aria_current") is not True for item in routes):
        raise KernelError("E-WORKSPACE-BROWSER-ROUTES", "all routes must pass with aria-current")
    entry_routes = [item for item in routes if item.get("route_kind") == "entry"]
    if [item.get("position") for item in entry_routes] != [1, 2, 3, 4, 5]:
        raise KernelError("E-WORKSPACE-BROWSER-ORDER", "entry order must remain 1 through 5")
    if any(item.get("exact_reference_visible") is not True or item.get("decision_visible") is not True for item in entry_routes):
        raise KernelError("E-WORKSPACE-BROWSER-ORDER", "entry exact references and decisions must be visible")
    for field in (
        "entry_order_preserved",
        "decisions_read_only",
        "candidates_unresolved",
        "principia_status_separate",
        "non_graph_workflow_complete",
        "exact_revision_preserved",
    ):
        _require(workflows, field, True, "E-WORKSPACE-BROWSER-AUTHORITY")
    _require(workflows, "canonical_mutation", False, "E-WORKSPACE-BROWSER-AUTHORITY")
    _require(workflows, "repository_mutation", False, "E-WORKSPACE-BROWSER-AUTHORITY")
    if workflows.get("history", {}).get("decision") != "pass":
        raise KernelError("E-WORKSPACE-BROWSER-HISTORY", "browser history evidence must pass")
    if workflows.get("deep_link", {}).get("decision") != "pass":
        raise KernelError("E-WORKSPACE-BROWSER-DEEP-LINK", "deep-link evidence must pass")
    if workflows.get("offline_after_local_boot", {}).get("decision") != "pass":
        raise KernelError("E-WORKSPACE-BROWSER-OFFLINE", "offline-after-boot evidence must pass")
    download = workflows.get("download")
    if not isinstance(download, Mapping):
        raise KernelError("E-WORKSPACE-BROWSER-DOWNLOAD", "download evidence is required")
    for field in ("byte_identical",):
        if download.get(field) is not True:
            raise KernelError("E-WORKSPACE-BROWSER-DOWNLOAD", "download must reproduce accepted export bytes")
    if download.get("bytes") != download.get("expected_bytes") or download.get("sha256") != download.get("expected_sha256"):
        raise KernelError("E-WORKSPACE-BROWSER-DOWNLOAD", "download identity differs from accepted export")
    _require(download, "canonical_write", False, "E-WORKSPACE-BROWSER-DOWNLOAD")

    if accessibility.get("document_language") != "en" or accessibility.get("first_heading_level") != 1:
        raise KernelError("E-WORKSPACE-BROWSER-ACCESSIBILITY", "language and first heading must be correct")
    if accessibility.get("landmarks") != {"banner": 1, "contentinfo": 1, "main": 1, "navigation": 1}:
        raise KernelError("E-WORKSPACE-BROWSER-ACCESSIBILITY", "required landmarks differ")
    for field in (
        "all_interactive_named",
        "main_labelled",
        "skip_link_focus_visible",
        "main_target_focus_visible",
        "all_route_focus_visible",
        "download_focus_visible",
        "mobile_skip_focus_visible",
        "mobile_main_focus_visible",
        "mobile_no_horizontal_overflow",
        "reduced_motion_verified",
        "non_graph_workflow_complete",
    ):
        _require(accessibility, field, True, "E-WORKSPACE-BROWSER-ACCESSIBILITY")
    _require(accessibility, "route_focus_count", 13, "E-WORKSPACE-BROWSER-ACCESSIBILITY")
    for field in (
        "human_verified",
        "assistive_technology_user_reviewed",
        "human_usability_reviewed",
        "accessibility_certified",
        "screenshots_authoritative",
        "live",
        "repository_mutation",
    ):
        _require(accessibility, field, False, "E-WORKSPACE-BROWSER-AUTHORITY")
    _require(accessibility, "decision", "pass", "E-WORKSPACE-BROWSER-ACCESSIBILITY")

    _require(network, "external_request_count", 0, "E-WORKSPACE-BROWSER-NETWORK")
    _require(network, "credentials_used", False, "E-WORKSPACE-BROWSER-NETWORK")
    _require(network, "remote_assets_used", False, "E-WORKSPACE-BROWSER-NETWORK")
    _require(network, "analytics_used", False, "E-WORKSPACE-BROWSER-NETWORK")
    _require(network, "cloud_service_used", False, "E-WORKSPACE-BROWSER-NETWORK")
    _require(network, "external_network_allowed", False, "E-WORKSPACE-BROWSER-NETWORK")
    _require(network, "service_workers_blocked", True, "E-WORKSPACE-BROWSER-NETWORK")
    _require(network, "decision", "pass", "E-WORKSPACE-BROWSER-NETWORK")
    network_records = network.get("records")
    if not isinstance(network_records, list) or not network_records:
        raise KernelError("E-WORKSPACE-BROWSER-NETWORK", "network records are required")
    if any(item.get("decision") == "blocked-external" or item.get("has_credentials") is not False for item in network_records):
        raise KernelError("E-WORKSPACE-BROWSER-NETWORK", "external or credentialed requests are forbidden")

    _require(failures, "accepted_failure_state_count", 2, "E-WORKSPACE-BROWSER-FAILURE")
    _require(failures, "silent_fallback_allowed", False, "E-WORKSPACE-BROWSER-FAILURE")
    _require(failures, "previous_valid_state_preserved", True, "E-WORKSPACE-BROWSER-FAILURE")
    _require(failures, "partial_package_exposed", False, "E-WORKSPACE-BROWSER-FAILURE")
    _require(failures, "canonical_mutation", False, "E-WORKSPACE-BROWSER-FAILURE")
    _require(failures, "repository_mutation", False, "E-WORKSPACE-BROWSER-FAILURE")
    _require(failures, "decision", "pass", "E-WORKSPACE-BROWSER-FAILURE")
    unknown = failures.get("unknown_route")
    missing = failures.get("missing_artifact")
    if not isinstance(unknown, Mapping) or not isinstance(missing, Mapping):
        raise KernelError("E-WORKSPACE-BROWSER-FAILURE", "both failure records are required")
    if unknown.get("explicit_failure") is not True or unknown.get("fallback_refused") is not True or unknown.get("previous_valid_state_preserved") is not True:
        raise KernelError("E-WORKSPACE-BROWSER-FAILURE", "unknown-route failure did not preserve state")
    if missing.get("explicit_failure") is not True or missing.get("fallback_data_loaded") is not False or missing.get("route_count") != 0:
        raise KernelError("E-WORKSPACE-BROWSER-FAILURE", "missing-artifact failure exposed partial state")

    _require(manifest, "engine_name", "chromium", "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "engine_version", "151.0.7922.34", "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "playwright_version", "1.62.0", "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "node_major", 22, "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "runner", "ubuntu-24.04", "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "shell_contract", "atlas-workspace-shell-data/0.1", "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "shell_baseline_contract", "atlas-phase4-workspace-shell-baseline/0.1", "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "external_network_allowed", False, "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "screenshots_authoritative", False, "E-WORKSPACE-BROWSER-MANIFEST")
    _require(manifest, "browser_state_authority", "ephemeral-only", "E-WORKSPACE-BROWSER-AUTHORITY")
    for field in ("production_frontend_architecture_selected", "live_principia_dependency", "canonical_mutation", "repository_mutation"):
        _require(manifest, field, False, "E-WORKSPACE-BROWSER-AUTHORITY")

    expected_child_artifacts = []
    for file_name in (
        "workspace-browser-workflows.json",
        "workspace-browser-accessibility.json",
        "workspace-browser-network.json",
        "workspace-browser-failures.json",
        "workspace-browser-manifest.json",
    ):
        expected_child_artifacts.append(_artifact(root / file_name, records[file_name]))
    if report.get("evidence_files") != expected_child_artifacts:
        raise KernelError("E-WORKSPACE-BROWSER-EVIDENCE", "report child artifact bindings differ")

    required_true = (
        "exact_revision_preserved",
        "entry_order_preserved",
        "decisions_read_only",
        "candidates_unresolved",
        "principia_status_separate",
        "warnings_visible",
        "limitations_visible",
        "export_identity_visible",
        "non_graph_workflow_complete",
        "visible_focus_verified",
        "deep_links_reload_and_history_verified",
        "reduced_motion_verified",
        "mobile_layout_verified",
        "offline_after_local_boot_verified",
        "unknown_route_preserved_previous_state",
        "missing_artifact_failed_explicitly",
        "local_download_byte_identical",
        "zero_external_requests",
    )
    for field in required_true:
        _require(report, field, True, "E-WORKSPACE-BROWSER-REPORT")
    _require(report, "route_count", 13, "E-WORKSPACE-BROWSER-REPORT")
    _require(report, "entry_route_count", 5, "E-WORKSPACE-BROWSER-REPORT")
    _require(report, "keyboard_route_count", 13, "E-WORKSPACE-BROWSER-REPORT")
    _require(report, "viewport_count", 2, "E-WORKSPACE-BROWSER-REPORT")
    _require(report, "accepted_failure_state_count", 2, "E-WORKSPACE-BROWSER-REPORT")
    _require(report, "external_request_count", 0, "E-WORKSPACE-BROWSER-NETWORK")
    _require(report, "browser_state_authority", "ephemeral-only", "E-WORKSPACE-BROWSER-AUTHORITY")
    for field in (
        "human_verified",
        "assistive_technology_user_reviewed",
        "human_usability_reviewed",
        "accessibility_certified",
        "screenshots_authoritative",
        "account_required",
        "cloud_required",
        "production_frontend_architecture_selected",
        "live_principia_dependency",
        "canonical_mutation",
        "lifecycle_mutation",
        "review_mutation",
        "repository_mutation",
        "live",
    ):
        _require(report, field, False, "E-WORKSPACE-BROWSER-AUTHORITY")
    _require(report, "decision", "workspace-browser-evidence-candidate", "E-WORKSPACE-BROWSER-REPORT")

    download_path = root / "downloaded-workspace-export.json"
    download_payload = download_path.read_bytes()
    download_record = report.get("download_artifact")
    if not isinstance(download_record, Mapping):
        raise KernelError("E-WORKSPACE-BROWSER-DOWNLOAD", "report download artifact is required")
    if (
        download_record.get("file") != download_path.name
        or download_record.get("bytes") != len(download_payload)
        or download_record.get("sha256") != hashlib.sha256(download_payload).hexdigest()
        or download_record.get("byte_identical") is not True
        or download_record.get("accepted_export_sha256") != download_record.get("sha256")
    ):
        raise KernelError("E-WORKSPACE-BROWSER-DOWNLOAD", "download artifact binding differs")

    validation = {
        "contract": "atlas-phase4-workspace-browser-validation/0.1",
        "decision": "valid-workspace-browser-evidence-candidate",
        "route_count": 13,
        "entry_route_count": 5,
        "viewport_count": 2,
        "failure_count": 2,
        "external_request_count": 0,
        "download_sha256": download_record["sha256"],
        "report_digest": report["report_digest"],
        "human_verified": False,
        "accessibility_certified": False,
        "live": False,
        "repository_mutation": False,
    }
    return validation


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_dir", type=Path)
    args = parser.parse_args(argv)
    try:
        validation = validate_directory(args.evidence_dir)
    except KernelError as exc:
        print(f"{exc.code}: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(render_json(validation))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
