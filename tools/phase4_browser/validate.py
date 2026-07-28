#!/usr/bin/env python3
"""Validate deterministic Phase 4 browser evidence contracts and authority boundaries."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence


class BrowserEvidenceError(ValueError):
    """Raised when browser evidence violates its contract or authority boundary."""


EXPECTED_FILES = {
    "browser-manifest.json": "atlas-phase4-browser-evidence-manifest/0.1",
    "browser-workflows.json": "atlas-browser-workflow-evidence/0.1",
    "browser-accessibility.json": "atlas-browser-accessibility-report/0.1",
    "browser-network.json": "atlas-browser-network-report/0.1",
    "browser-failures.json": "atlas-browser-failure-evidence/0.1",
}
REPORT_CONTRACT = "atlas-phase4-browser-evidence-report/0.1"
MODE = "interactive-experience-foundation"


def render_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _load(path: Path) -> tuple[dict[str, Any], bytes]:
    payload = path.read_bytes()
    record = json.loads(payload)
    if not isinstance(record, dict):
        raise BrowserEvidenceError(f"E-BROWSER-JSON: {path.name} must contain an object")
    return record, payload


def _validate_digest(record: Mapping[str, Any], filename: str) -> None:
    digest = record.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise BrowserEvidenceError(f"E-BROWSER-DIGEST: {filename} requires a SHA-256 report_digest")
    unsigned = dict(record)
    unsigned.pop("report_digest", None)
    expected = sha256_bytes(render_json(unsigned).encode("utf-8"))
    if digest != expected:
        raise BrowserEvidenceError(f"E-BROWSER-DIGEST: {filename} digest mismatch")


def _require(record: Mapping[str, Any], field: str, expected: Any, code: str) -> None:
    if record.get(field) != expected:
        raise BrowserEvidenceError(f"{code}: expected {field}={expected!r}")


def _validate_common(record: Mapping[str, Any], contract: str, filename: str) -> None:
    _require(record, "contract", contract, "E-BROWSER-CONTRACT")
    _require(record, "mode", MODE, "E-BROWSER-MODE")
    _require(record, "live", False, "E-BROWSER-AUTHORITY")
    _require(record, "repository_mutation", False, "E-BROWSER-AUTHORITY")
    _validate_digest(record, filename)


def validate_evidence_directory(root: Path) -> dict[str, Any]:
    report, report_bytes = _load(root / "browser-evidence-report.json")
    _validate_common(report, REPORT_CONTRACT, "browser-evidence-report.json")
    _require(report, "phase", 4, "E-BROWSER-PHASE")
    _require(report, "workstream", 2, "E-BROWSER-WORKSTREAM")
    _require(report, "state", "browser-evidence-candidate", "E-BROWSER-STATE")
    _require(report, "decision", "browser-evidence-candidate", "E-BROWSER-DECISION")

    evidence_entries = report.get("evidence_files")
    if not isinstance(evidence_entries, list) or len(evidence_entries) != len(EXPECTED_FILES):
        raise BrowserEvidenceError("E-BROWSER-FILES: report must bind all five evidence files")
    entry_by_name = {entry.get("file"): entry for entry in evidence_entries if isinstance(entry, dict)}
    if set(entry_by_name) != set(EXPECTED_FILES):
        raise BrowserEvidenceError("E-BROWSER-FILES: evidence file set mismatch")

    records: dict[str, dict[str, Any]] = {}
    for filename, contract in EXPECTED_FILES.items():
        record, payload = _load(root / filename)
        _validate_common(record, contract, filename)
        entry = entry_by_name[filename]
        if entry.get("bytes") != len(payload):
            raise BrowserEvidenceError(f"E-BROWSER-FILE-BYTES: {filename} byte count mismatch")
        if entry.get("sha256") != sha256_bytes(payload):
            raise BrowserEvidenceError(f"E-BROWSER-FILE-SHA: {filename} SHA-256 mismatch")
        if entry.get("report_digest") != record.get("report_digest"):
            raise BrowserEvidenceError(f"E-BROWSER-FILE-DIGEST: {filename} semantic digest mismatch")
        records[filename] = record

    manifest = records["browser-manifest.json"]
    workflows = records["browser-workflows.json"]
    accessibility = records["browser-accessibility.json"]
    network = records["browser-network.json"]
    failures = records["browser-failures.json"]

    _require(manifest, "phase", 4, "E-BROWSER-MANIFEST")
    _require(manifest, "workstream", 2, "E-BROWSER-MANIFEST")
    _require(manifest, "state", "browser-evidence-candidate", "E-BROWSER-MANIFEST")
    _require(manifest, "engine_name", "chromium", "E-BROWSER-ENGINE")
    _require(manifest, "playwright_version", "1.62.0", "E-BROWSER-ENGINE")
    _require(manifest, "external_network_allowed", False, "E-BROWSER-NETWORK")
    _require(manifest, "screenshots_authoritative", False, "E-BROWSER-AUTHORITY")
    _require(manifest, "human_verified", False, "E-BROWSER-REVIEW")
    _require(manifest, "accessibility_certified", False, "E-BROWSER-REVIEW")
    _require(manifest, "assistive_technology_user_reviewed", False, "E-BROWSER-REVIEW")
    if not isinstance(manifest.get("engine_version"), str) or not manifest["engine_version"]:
        raise BrowserEvidenceError("E-BROWSER-ENGINE: engine_version is required")
    if manifest.get("viewport_matrix") != [
        {"height": 1000, "id": "desktop", "reduced_motion": "no-preference", "width": 1440},
        {"height": 844, "id": "mobile", "reduced_motion": "reduce", "width": 390},
    ]:
        raise BrowserEvidenceError("E-BROWSER-VIEWPORT: pinned viewport matrix mismatch")

    _require(workflows, "workflow_count", 8, "E-BROWSER-WORKFLOW")
    _require(workflows, "decision", "pass", "E-BROWSER-WORKFLOW")
    _require(workflows, "non_graph_workflow_equivalence", True, "E-BROWSER-NON-GRAPH")
    _require(workflows, "exact_revision_required", True, "E-BROWSER-REVISION")
    _require(workflows, "implicit_latest_allowed", False, "E-BROWSER-REVISION")
    workflow_items = workflows.get("workflows")
    if not isinstance(workflow_items, list) or len(workflow_items) != 8:
        raise BrowserEvidenceError("E-BROWSER-WORKFLOW: eight workflow records are required")
    kinds = set()
    for item in workflow_items:
        if not isinstance(item, Mapping):
            raise BrowserEvidenceError("E-BROWSER-WORKFLOW: workflow record must be an object")
        _require(item, "contract", "atlas-browser-workflow-evidence/0.1", "E-BROWSER-WORKFLOW")
        _require(item, "focus_visible", True, "E-BROWSER-FOCUS")
        _require(item, "non_graph_route_exercised", True, "E-BROWSER-NON-GRAPH")
        _require(item, "decision", "pass", "E-BROWSER-WORKFLOW")
        if item.get("expected_hash") != item.get("observed_hash"):
            raise BrowserEvidenceError("E-BROWSER-ROUTE: expected and observed route differ")
        workflow_id = item.get("workflow_id")
        if not isinstance(workflow_id, str) or "@" not in workflow_id or workflow_id.endswith("@latest"):
            raise BrowserEvidenceError("E-BROWSER-REVISION: workflow ID must carry an exact numeric revision")
        kinds.add(item.get("view_kind"))
    expected_kinds = {
        "candidate",
        "entity",
        "filter",
        "impact-warning",
        "principia-reference",
        "provenance",
        "research-trail",
        "retrieval",
    }
    if kinds != expected_kinds:
        raise BrowserEvidenceError("E-BROWSER-WORKFLOW: workflow-kind coverage mismatch")
    _require(workflows.get("history", {}), "decision", "pass", "E-BROWSER-HISTORY")
    _require(workflows.get("deep_link", {}), "decision", "pass", "E-BROWSER-DEEP-LINK")
    _require(workflows.get("offline", {}), "decision", "pass", "E-BROWSER-OFFLINE")

    _require(accessibility, "keyboard_workflow_count", 9, "E-BROWSER-KEYBOARD")
    _require(accessibility, "visible_focus_required", True, "E-BROWSER-FOCUS")
    _require(accessibility, "skip_link_operational", True, "E-BROWSER-SKIP-LINK")
    _require(accessibility, "landmarks_recorded", True, "E-BROWSER-LANDMARK")
    _require(accessibility, "headings_recorded", True, "E-BROWSER-HEADING")
    _require(accessibility, "labels_recorded", True, "E-BROWSER-LABEL")
    _require(accessibility, "live_regions_recorded", True, "E-BROWSER-LIVE-REGION")
    _require(accessibility, "non_graph_routes_required", True, "E-BROWSER-NON-GRAPH")
    _require(accessibility, "reduced_motion_checked", True, "E-BROWSER-MOTION")
    _require(accessibility, "human_verified", False, "E-BROWSER-REVIEW")
    _require(accessibility, "accessibility_certified", False, "E-BROWSER-REVIEW")
    _require(accessibility, "assistive_technology_user_reviewed", False, "E-BROWSER-REVIEW")
    _require(accessibility, "decision", "pass-bounded-automated-evidence", "E-BROWSER-ACCESSIBILITY")
    desktop = accessibility.get("desktop")
    mobile = accessibility.get("mobile")
    if not isinstance(desktop, Mapping) or not isinstance(mobile, Mapping):
        raise BrowserEvidenceError("E-BROWSER-ACCESSIBILITY: desktop and mobile evidence are required")
    _require(desktop.get("skip_link_focus", {}), "visible", True, "E-BROWSER-FOCUS")
    _require(desktop.get("main_focus", {}), "visible", True, "E-BROWSER-FOCUS")
    _require(desktop.get("desktop_overflow", {}), "passes", True, "E-BROWSER-OVERFLOW")
    _require(mobile, "decision", "pass", "E-BROWSER-MOBILE")
    if mobile.get("responsive", {}).get("horizontal_overflow") is not False:
        raise BrowserEvidenceError("E-BROWSER-MOBILE-OVERFLOW: mobile horizontal overflow detected")
    if mobile.get("responsive", {}).get("scroll_behavior") != "auto":
        raise BrowserEvidenceError("E-BROWSER-MOTION: reduced-motion scroll behavior must be auto")

    _require(network, "external_request_count", 0, "E-BROWSER-NETWORK")
    _require(network, "blocked_external_request_count", 0, "E-BROWSER-NETWORK")
    _require(network, "credentials_used", False, "E-BROWSER-NETWORK")
    _require(network, "remote_assets_used", False, "E-BROWSER-NETWORK")
    _require(network, "analytics_used", False, "E-BROWSER-NETWORK")
    _require(network, "cloud_service_used", False, "E-BROWSER-NETWORK")
    _require(network, "decision", "pass-zero-external-requests", "E-BROWSER-NETWORK")
    request_records = network.get("request_records")
    if not isinstance(request_records, list) or not request_records:
        raise BrowserEvidenceError("E-BROWSER-NETWORK: deterministic request records are required")
    if any(record.get("decision") != "allowed-loopback" for record in request_records):
        raise BrowserEvidenceError("E-BROWSER-NETWORK: non-loopback request record detected")

    _require(failures, "accepted_failure_state_count", 5, "E-BROWSER-FAILURE")
    _require(failures, "unknown_route_explicit", True, "E-BROWSER-FAILURE")
    _require(failures, "silent_fallback", False, "E-BROWSER-FAILURE")
    _require(failures, "implicit_latest_rejected", True, "E-BROWSER-FAILURE")
    _require(failures, "canonical_mutation", False, "E-BROWSER-AUTHORITY")
    _require(failures, "lifecycle_mutation", False, "E-BROWSER-AUTHORITY")
    _require(failures, "decision", "pass", "E-BROWSER-FAILURE")

    expected_report_fields = {
        "workflow_count": 8,
        "keyboard_workflow_count": 9,
        "accepted_failure_state_count": 5,
        "viewport_count": 2,
        "external_request_count": 0,
        "exact_revision_preserved": True,
        "principia_status_separate": True,
        "non_graph_workflow_equivalence": True,
        "visible_focus_verified": True,
        "reduced_motion_verified": True,
        "offline_after_local_boot_verified": True,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "canonical_mutation": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "human_verified": False,
        "accessibility_certified": False,
    }
    for field, expected in expected_report_fields.items():
        _require(report, field, expected, "E-BROWSER-REPORT")
    if report.get("manifest_digest") != manifest.get("report_digest"):
        raise BrowserEvidenceError("E-BROWSER-MANIFEST: report manifest digest mismatch")

    return {
        "contract": "atlas-phase4-browser-evidence-validation/0.1",
        "decision": "valid-browser-evidence-candidate",
        "browser_report_sha256": sha256_bytes(report_bytes),
        "browser_report_digest": report["report_digest"],
        "evidence_file_count": len(EXPECTED_FILES) + 1,
        "workflow_count": report["workflow_count"],
        "external_request_count": report["external_request_count"],
        "human_verified": False,
        "live": False,
        "repository_mutation": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence_dir", type=Path)
    args = parser.parse_args(argv)
    result = validate_evidence_directory(args.evidence_dir)
    sys.stdout.write(render_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
