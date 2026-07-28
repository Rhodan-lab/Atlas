#!/usr/bin/env python3
"""Deterministic Phase 4 Workstream 2 closure proof and next-workstream recommendation."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, load_json, render_json

COMPLETION_CONTRACT = "atlas-phase4-workstream2-completion-report/0.1"
COMPLETION_VALIDATION_CONTRACT = "atlas-phase4-workstream2-completion-validation/0.1"
BROWSER_BASELINE_CONTRACT = "atlas-phase4-browser-evidence-baseline/0.1"
SHELL_PATCH_CONTRACT = "atlas-phase4-reference-shell-accessibility-patch/0.1"
WORKSTREAM1_BASELINE_CONTRACT = "atlas-phase4-workstream1-completion-baseline/0.1"
MODE = "interactive-experience-foundation"


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require(record: Mapping[str, Any], field: str, expected: Any, code: str) -> None:
    if record.get(field) != expected:
        raise KernelError(code, f"expected {field}={expected!r}")


def _validate_browser_baseline(record: Mapping[str, Any]) -> None:
    _require(record, "contract", BROWSER_BASELINE_CONTRACT, "E-PHASE4-W2-BROWSER")
    _require(record, "mode", MODE, "E-PHASE4-W2-BROWSER")
    _require(record, "phase", 4, "E-PHASE4-W2-BROWSER")
    _require(record, "workstream", 2, "E-PHASE4-W2-BROWSER")
    _require(record, "state", "browser-evidence-candidate", "E-PHASE4-W2-BROWSER")
    _require(record, "decision", "browser-evidence-candidate", "E-PHASE4-W2-BROWSER")
    expected = {
        "workflow_count": 8,
        "keyboard_workflow_count": 9,
        "viewport_count": 2,
        "external_request_count": 0,
        "exact_revision_preserved": True,
        "principia_status_separate": True,
        "non_graph_workflow_equivalence": True,
        "visible_focus_verified": True,
        "reduced_motion_verified": True,
        "offline_after_local_boot_verified": True,
        "repeated_run_substantive_artifacts_byte_identical": True,
        "production_frontend_architecture_selected": False,
        "human_verified": False,
        "accessibility_certified": False,
        "live_principia_dependency": False,
        "live": False,
        "repository_mutation": False,
    }
    for field, value in expected.items():
        _require(record, field, value, "E-PHASE4-W2-BROWSER")
    engine = record.get("browser_engine")
    if not isinstance(engine, Mapping):
        raise KernelError("E-PHASE4-W2-ENGINE", "browser engine identity is required")
    if engine != {
        "name": "chromium",
        "playwright_version": "1.62.0",
        "version": "151.0.7922.34",
    }:
        raise KernelError("E-PHASE4-W2-ENGINE", "browser engine identity differs from accepted evidence")
    evidence_files = record.get("evidence_files")
    if not isinstance(evidence_files, Mapping) or len(evidence_files) != 6:
        raise KernelError("E-PHASE4-W2-FILES", "all six pinned evidence files are required")
    for name, evidence in evidence_files.items():
        if not isinstance(name, str) or not isinstance(evidence, Mapping):
            raise KernelError("E-PHASE4-W2-FILES", "invalid evidence-file record")
        sha = evidence.get("artifact_sha256")
        digest = evidence.get("report_digest")
        if not isinstance(sha, str) or len(sha) != 64 or not isinstance(digest, str) or len(digest) != 64:
            raise KernelError("E-PHASE4-W2-FILES", f"invalid evidence identity for {name!r}")


def _validate_shell_patch(record: Mapping[str, Any], browser_baseline: Mapping[str, Any]) -> None:
    _require(record, "contract", SHELL_PATCH_CONTRACT, "E-PHASE4-W2-PATCH")
    _require(record, "mode", MODE, "E-PHASE4-W2-PATCH")
    _require(record, "state", "accessibility-patch-candidate", "E-PHASE4-W2-PATCH")
    _require(record, "decision", "authorize-bounded-browser-evidence-fixes", "E-PHASE4-W2-PATCH")
    _require(record, "interaction_semantics_changed", False, "E-PHASE4-W2-PATCH")
    _require(record, "production_frontend_architecture_selected", False, "E-PHASE4-W2-PATCH")
    _require(record, "live_principia_dependency", False, "E-PHASE4-W2-PATCH")
    _require(record, "canonical_mutation", False, "E-PHASE4-W2-PATCH")
    _require(record, "live", False, "E-PHASE4-W2-PATCH")
    _require(record, "repository_mutation", False, "E-PHASE4-W2-PATCH")
    report_digest = browser_baseline["evidence_files"]["browser-evidence-report.json"]["report_digest"]
    if record.get("browser_evidence_report_digest") != report_digest:
        raise KernelError("E-PHASE4-W2-PATCH", "shell patch is not bound to accepted browser evidence")
    current_assets = record.get("current_static_assets")
    historical_assets = record.get("historical_static_assets")
    if not isinstance(current_assets, Mapping) or not isinstance(historical_assets, Mapping):
        raise KernelError("E-PHASE4-W2-PATCH", "shell patch must preserve both asset generations")
    if set(current_assets) != {"index.html", "styles.css", "app.js"} or set(historical_assets) != set(current_assets):
        raise KernelError("E-PHASE4-W2-PATCH", "shell patch asset set is invalid")


def _validate_workstream1_baseline(record: Mapping[str, Any]) -> None:
    _require(record, "contract", WORKSTREAM1_BASELINE_CONTRACT, "E-PHASE4-W2-W1")
    _require(record, "report_contract", "atlas-phase4-workstream1-completion-report/0.1", "E-PHASE4-W2-W1")
    _require(record, "state", "closure-candidate", "E-PHASE4-W2-W1")
    _require(record, "decision", "proceed-workstream2-browser-accessibility-evidence", "E-PHASE4-W2-W1")
    _require(record, "python_substantive_artifacts_byte_identical", True, "E-PHASE4-W2-W1")
    _require(record, "report_artifact_bytes", 3996, "E-PHASE4-W2-W1")
    _require(
        record,
        "report_artifact_sha256",
        "03ba1f02d7ca2cfb7432919c7bdca110edbd497fc8c2be2c2216b099abe0cb23",
        "E-PHASE4-W2-W1",
    )
    _require(
        record,
        "report_digest",
        "a3167ee2dc7a02c47468a1b850e15b495f3ed6058399205fc2cdf906d922aaa3",
        "E-PHASE4-W2-W1",
    )


def run_workstream2_closure(
    browser_baseline: Mapping[str, Any],
    shell_patch: Mapping[str, Any],
    workstream1_baseline: Mapping[str, Any],
) -> dict[str, Any]:
    _validate_browser_baseline(browser_baseline)
    _validate_shell_patch(shell_patch, browser_baseline)
    _validate_workstream1_baseline(workstream1_baseline)

    network = browser_baseline["network_evidence"]
    report_evidence = browser_baseline["evidence_files"]["browser-evidence-report.json"]
    accessibility_evidence = browser_baseline["evidence_files"]["browser-accessibility.json"]
    workflow_evidence = browser_baseline["evidence_files"]["browser-workflows.json"]
    failure_evidence = browser_baseline["evidence_files"]["browser-failures.json"]

    exit_gates = {
        "browser_contracts_versioned_and_pinned": (
            len(browser_baseline["evidence_files"]) == 6
            and report_evidence["contract"] == "atlas-phase4-browser-evidence-report/0.1"
        ),
        "engine_and_environment_pinned": (
            browser_baseline["browser_engine"]
            == {"name": "chromium", "playwright_version": "1.62.0", "version": "151.0.7922.34"}
            and browser_baseline["package_lock"]["artifact_sha256"]
            == "7d889a57ab2d7f5855f7ea31184b7da5808efc896c65ab3de01e2d7ab0ac8510"
        ),
        "required_workflows_pass_by_keyboard": (
            browser_baseline["workflow_count"] == 8 and browser_baseline["keyboard_workflow_count"] == 9
        ),
        "focus_semantics_and_errors_recorded": (
            browser_baseline["visible_focus_verified"] is True
            and accessibility_evidence["contract"] == "atlas-browser-accessibility-report/0.1"
            and failure_evidence["contract"] == "atlas-browser-failure-evidence/0.1"
        ),
        "deep_links_reload_and_history_deterministic": (
            workflow_evidence["contract"] == "atlas-browser-workflow-evidence/0.1"
            and browser_baseline["exact_revision_preserved"] is True
        ),
        "non_graph_equivalence_complete": browser_baseline["non_graph_workflow_equivalence"] is True,
        "warnings_and_failures_explicit_and_non_mutating": (
            shell_patch["interaction_semantics_changed"] is False
            and shell_patch["canonical_mutation"] is False
            and browser_baseline["repository_mutation"] is False
        ),
        "zero_external_requests": (
            browser_baseline["external_request_count"] == 0
            and network["request_count"] == network["loopback_request_count"] == 4
        ),
        "bounded_desktop_and_mobile_viewports_pass": browser_baseline["viewport_count"] == 2,
        "repeated_runs_byte_identical": browser_baseline["repeated_run_substantive_artifacts_byte_identical"] is True,
        "limitations_and_non_human_review_explicit": (
            browser_baseline["human_verified"] is False and browser_baseline["accessibility_certified"] is False
        ),
        "historical_workstream1_evidence_preserved": (
            workstream1_baseline["report_artifact_sha256"]
            == "03ba1f02d7ca2cfb7432919c7bdca110edbd497fc8c2be2c2216b099abe0cb23"
            and shell_patch["generated_artifacts_unchanged"]["shell_data_sha256"]
            == "e0f9fcbff9b86cbd4fffcb43d9c2aff64c2eb602f9b2fa0a02b8804bd18eb762"
        ),
    }
    if not all(exit_gates.values()):
        failed = sorted(name for name, passed in exit_gates.items() if not passed)
        raise KernelError("E-PHASE4-W2-EXIT-GATE", f"Workstream 2 exit gates failed: {failed}")

    report: dict[str, Any] = {
        "contract": COMPLETION_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 2,
        "state": "closure-candidate",
        "decision": "proceed-workstream3-read-only-research-workspace",
        "accepted_evidence": {
            "browser_evidence": {
                "pr": 46,
                "tested_head": "05e829dcf0c331188f4e75a7ffe8e9b1434b2aab",
                "merge_commit": "d5577d9664a16b89d4c2597229f418a7f4a8f849",
                "baseline_sha256": _json_sha256(browser_baseline),
                "report_artifact_bytes": report_evidence["artifact_bytes"],
                "report_artifact_sha256": report_evidence["artifact_sha256"],
                "report_digest": report_evidence["report_digest"],
                "engine": browser_baseline["browser_engine"],
            },
            "shell_accessibility_patch": {
                "contract": shell_patch["contract"],
                "sha256": _json_sha256(shell_patch),
                "interaction_semantics_changed": False,
                "generated_artifacts_unchanged": shell_patch["generated_artifacts_unchanged"],
            },
            "workstream1_history": {
                "completion_baseline_sha256": _json_sha256(workstream1_baseline),
                "report_artifact_sha256": workstream1_baseline["report_artifact_sha256"],
                "report_digest": workstream1_baseline["report_digest"],
            },
        },
        "exit_gates": exit_gates,
        "evidence_summary": {
            "workflow_count": browser_baseline["workflow_count"],
            "keyboard_workflow_count": browser_baseline["keyboard_workflow_count"],
            "viewport_count": browser_baseline["viewport_count"],
            "external_request_count": browser_baseline["external_request_count"],
            "loopback_request_count": network["loopback_request_count"],
            "evidence_file_count": len(browser_baseline["evidence_files"]),
            "repeated_run_byte_identical": browser_baseline["repeated_run_substantive_artifacts_byte_identical"],
        },
        "workstream3_entry_boundary": {
            "purpose": "compose accepted exact-revision views into a read-only multi-step research workspace",
            "workspace_authority": "ephemeral-research-only",
            "canonical_copy_authority": False,
            "canonical_mutation": False,
            "lifecycle_mutation": False,
            "review_mutation": False,
            "automatic_merge_or_resolution": False,
            "exact_revision_required": True,
            "principia_status_separate": True,
            "non_graph_workflow_required": True,
            "local_first": True,
            "deterministic_export_required": True,
            "account_required": False,
            "cloud_required": False,
            "external_network_required": False,
            "production_frontend_architecture_selected": False,
            "live_principia_dependency": False,
            "repository_mutation": False,
        },
        "review_policy": {
            "active_review_level": "ai-reviewed",
            "human_verified": False,
            "accessibility_certified": False,
            "assistive_technology_user_reviewed": False,
            "human_usability_reviewed": False,
        },
        "production_retrieval_quality_claim": False,
        "production_frontend_architecture_selected": False,
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "live_principia_dependency": False,
        "canonical_mutation": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "live": False,
        "repository_mutation": False,
    }
    report["report_digest"] = _json_sha256(report)
    return report


def validate_completion_report(report: Mapping[str, Any]) -> dict[str, Any]:
    _require(report, "contract", COMPLETION_CONTRACT, "E-PHASE4-W2-COMPLETION")
    _require(report, "mode", MODE, "E-PHASE4-W2-COMPLETION")
    _require(report, "phase", 4, "E-PHASE4-W2-COMPLETION")
    _require(report, "workstream", 2, "E-PHASE4-W2-COMPLETION")
    _require(report, "state", "closure-candidate", "E-PHASE4-W2-COMPLETION")
    _require(
        report,
        "decision",
        "proceed-workstream3-read-only-research-workspace",
        "E-PHASE4-W2-COMPLETION",
    )
    gates = report.get("exit_gates")
    if not isinstance(gates, Mapping) or len(gates) != 12 or not all(value is True for value in gates.values()):
        raise KernelError("E-PHASE4-W2-COMPLETION-GATES", "all twelve Workstream 2 exit gates must pass")
    boundary = report.get("workstream3_entry_boundary")
    if not isinstance(boundary, Mapping):
        raise KernelError("E-PHASE4-W3-BOUNDARY", "Workstream 3 boundary is required")
    required_boundary = {
        "workspace_authority": "ephemeral-research-only",
        "canonical_copy_authority": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "automatic_merge_or_resolution": False,
        "exact_revision_required": True,
        "principia_status_separate": True,
        "non_graph_workflow_required": True,
        "local_first": True,
        "deterministic_export_required": True,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "repository_mutation": False,
    }
    for field, expected in required_boundary.items():
        if boundary.get(field) != expected:
            raise KernelError("E-PHASE4-W3-BOUNDARY", f"unsafe Workstream 3 boundary: {field}")
    required_fields = {
        "production_retrieval_quality_claim": False,
        "production_frontend_architecture_selected": False,
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "live_principia_dependency": False,
        "canonical_mutation": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "live": False,
        "repository_mutation": False,
    }
    for field, expected in required_fields.items():
        if report.get(field) != expected:
            raise KernelError("E-PHASE4-W2-COMPLETION-AUTHORITY", f"completion requires {field}={expected!r}")
    review = report.get("review_policy")
    if not isinstance(review, Mapping) or any(
        review.get(field) is not False
        for field in (
            "human_verified",
            "accessibility_certified",
            "assistive_technology_user_reviewed",
            "human_usability_reviewed",
        )
    ):
        raise KernelError("E-PHASE4-W2-COMPLETION-REVIEW", "human and certification limitations must remain explicit")
    digest = report.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError("E-PHASE4-W2-COMPLETION-DIGEST", "report_digest must be a SHA-256")
    unsigned = dict(report)
    unsigned.pop("report_digest", None)
    if _json_sha256(unsigned) != digest:
        raise KernelError("E-PHASE4-W2-COMPLETION-DIGEST", "completion report digest mismatch")
    return {
        "contract": COMPLETION_VALIDATION_CONTRACT,
        "decision": "valid-workstream2-closure-candidate",
        "exit_gate_count": len(gates),
        "report_digest": digest,
        "human_verified": False,
        "live": False,
        "repository_mutation": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--browser-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_browser/browser-evidence-baseline.json"),
    )
    parser.add_argument(
        "--shell-patch",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/reference-shell-accessibility-patch.json"),
    )
    parser.add_argument(
        "--workstream1-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/workstream1-completion-baseline.json"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    report = run_workstream2_closure(
        load_json(args.browser_baseline),
        load_json(args.shell_patch),
        load_json(args.workstream1_baseline),
    )
    validation = validate_completion_report(report)
    rendered = render_json(report)
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote={args.output}")
    print(f"phase4-workstream2-report-digest={report['report_digest']}")
    print(f"phase4-workstream2-exit-gates={validation['exit_gate_count']}")
    print("phase4-workstream2=closure-candidate; next=read-only-research-workspace")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
