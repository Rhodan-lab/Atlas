#!/usr/bin/env python3
"""Deterministic Phase 4 Workstream 1 closure proof and Workstream 2 recommendation."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase4_interaction.build_shell import build_shell_data
from tools.phase4_interaction.contracts import MODE, validate_fixture_bundle
from tools.phase4_interaction.fixtures import load_fixture_manifest

COMPLETION_CONTRACT = "atlas-phase4-workstream1-completion-report/0.1"
COMPLETION_VALIDATION_CONTRACT = "atlas-phase4-workstream1-completion-validation/0.1"
INTERACTION_BASELINE_CONTRACT = "atlas-phase4-interaction-contract-baseline/0.1"
SHELL_BASELINE_CONTRACT = "atlas-phase4-reference-shell-baseline/0.1"


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _artifact_evidence(path: Path) -> dict[str, Any]:
    payload = path.read_bytes()
    return {
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def _require(record: Mapping[str, Any], field: str, expected: Any, code: str) -> None:
    if record.get(field) != expected:
        raise KernelError(code, f"expected {field}={expected!r}")


def _validate_interaction_baseline(record: Mapping[str, Any]) -> None:
    _require(record, "contract", INTERACTION_BASELINE_CONTRACT, "E-PHASE4-W1-INTERACTION")
    _require(record, "mode", MODE, "E-PHASE4-W1-INTERACTION")
    _require(record, "decision", "interaction-contract-candidate", "E-PHASE4-W1-INTERACTION")
    _require(record, "exact_revision_preserved", True, "E-PHASE4-W1-INTERACTION")
    _require(record, "keyboard_paths_required", True, "E-PHASE4-W1-INTERACTION")
    _require(record, "non_graph_paths_required", True, "E-PHASE4-W1-INTERACTION")
    _require(record, "principia_status_separate", True, "E-PHASE4-W1-INTERACTION")
    _require(record, "offline_capable", True, "E-PHASE4-W1-INTERACTION")
    _require(record, "canonical_copy_authority", False, "E-PHASE4-W1-INTERACTION")
    _require(record, "live_principia_dependency", False, "E-PHASE4-W1-INTERACTION")
    _require(record, "live", False, "E-PHASE4-W1-INTERACTION")
    _require(record, "repository_mutation", False, "E-PHASE4-W1-INTERACTION")


def _validate_shell_baseline(record: Mapping[str, Any]) -> None:
    _require(record, "contract", SHELL_BASELINE_CONTRACT, "E-PHASE4-W1-SHELL")
    _require(record, "mode", MODE, "E-PHASE4-W1-SHELL")
    _require(record, "decision", "reference-shell-candidate", "E-PHASE4-W1-SHELL")
    for field in ("api_required", "cloud_required", "account_required", "graph_required"):
        _require(record, field, False, "E-PHASE4-W1-SHELL")
    _require(record, "keyboard_navigation_required", True, "E-PHASE4-W1-SHELL")
    _require(record, "non_graph_navigation_required", True, "E-PHASE4-W1-SHELL")
    _require(record, "local_first", True, "E-PHASE4-W1-SHELL")
    _require(record, "local_server_smoke_test", True, "E-PHASE4-W1-SHELL")
    _require(record, "replaceable", True, "E-PHASE4-W1-SHELL")
    _require(record, "live", False, "E-PHASE4-W1-SHELL")
    _require(record, "repository_mutation", False, "E-PHASE4-W1-SHELL")


def run_workstream1_closure(
    canonical_root: Path,
    manifest_path: Path,
    interaction_baseline: Mapping[str, Any],
    shell_baseline: Mapping[str, Any],
    shell_root: Path,
) -> dict[str, Any]:
    _validate_interaction_baseline(interaction_baseline)
    _validate_shell_baseline(shell_baseline)

    repository = KernelRepository(compile_canonical(canonical_root))
    fixture = load_fixture_manifest(manifest_path)
    interaction_report, _ = validate_fixture_bundle(fixture, repository)
    shell_data, shell_report = build_shell_data(canonical_root, manifest_path)

    if interaction_report["report_digest"] != interaction_baseline["report_digest"]:
        raise KernelError("E-PHASE4-W1-INTERACTION", "interaction report digest differs from pinned evidence")
    if interaction_report["fixture_sha256"] != interaction_baseline["fixture_semantic_sha256"]:
        raise KernelError("E-PHASE4-W1-INTERACTION", "interaction fixture digest differs from pinned evidence")
    if interaction_report["counts"] != interaction_baseline["counts"]:
        raise KernelError("E-PHASE4-W1-INTERACTION", "interaction counts differ from pinned evidence")
    if interaction_report["negative_errors"] != interaction_baseline["negative_errors"]:
        raise KernelError("E-PHASE4-W1-INTERACTION", "interaction negative boundaries differ from pinned evidence")

    expected_shell_data = shell_baseline["shell_data"]
    expected_shell_report = shell_baseline["shell_build_report"]
    if shell_data["build_digest"] != expected_shell_data["build_digest"]:
        raise KernelError("E-PHASE4-W1-SHELL", "shell build digest differs from pinned evidence")
    if shell_report["report_digest"] != expected_shell_report["report_digest"]:
        raise KernelError("E-PHASE4-W1-SHELL", "shell report digest differs from pinned evidence")
    if shell_data["fixture_sha256"] != shell_baseline["fixture_sha256"]:
        raise KernelError("E-PHASE4-W1-SHELL", "shell fixture identity differs from pinned evidence")
    if shell_data["interaction_report_digest"] != shell_baseline["interaction_report_digest"]:
        raise KernelError("E-PHASE4-W1-SHELL", "shell interaction identity differs from pinned evidence")

    static_assets: dict[str, dict[str, Any]] = {}
    for name, expected in shell_baseline["static_assets"].items():
        observed = _artifact_evidence(shell_root / name)
        if observed != expected:
            raise KernelError("E-PHASE4-W1-SHELL-ASSET", f"static asset {name!r} differs from pinned evidence")
        static_assets[name] = observed

    counts = interaction_report["counts"]
    exit_gates = {
        "interaction_contracts_executable": (
            interaction_report["decision"] == "interaction-contract-candidate"
            and interaction_report["report_digest"] == interaction_baseline["report_digest"]
        ),
        "representative_workflows_pinned": (
            counts == {
                "failure_states": 5,
                "impact_warnings": 1,
                "negative_cases": 6,
                "principia_references": 1,
                "states": 8,
                "views": 8,
            }
            and len(interaction_report["workflow_kinds"]) == 8
        ),
        "exact_revisions_and_authority_visible": (
            interaction_report["exact_revision_preserved"] is True
            and interaction_report["authority_metadata_visible"] is True
        ),
        "atlas_and_principia_status_separate": (
            interaction_report["principia_status_separate"] is True
            and shell_data["authority"]["principia_status_separate"] is True
        ),
        "generated_artifacts_deterministic_and_replaceable": (
            interaction_baseline["python_substantive_artifacts_byte_identical"] is True
            and shell_baseline["python_substantive_artifacts_byte_identical"] is True
            and shell_baseline["replaceable"] is True
        ),
        "offline_and_missing_reference_failures_explicit": (
            interaction_report["offline_capable"] is True
            and interaction_report["impact_warnings_required"] is True
            and counts["failure_states"] == 5
            and counts["impact_warnings"] == 1
        ),
        "interface_state_cannot_mutate_authority": (
            interaction_report["canonical_copy_authority"] is False
            and interaction_report["automatic_status_change"] is False
            and interaction_report["automatic_release_action"] is False
            and interaction_report["repository_mutation"] is False
            and shell_data["authority"]["canonical_mutation"] is False
        ),
        "accessibility_and_non_graph_requirements_machine_checkable": (
            interaction_report["keyboard_paths_required"] is True
            and interaction_report["non_graph_paths_required"] is True
            and shell_report["keyboard_navigation_required"] is True
            and shell_report["non_graph_navigation_required"] is True
            and shell_baseline["local_server_smoke_test"] is True
        ),
        "minimal_reference_shell_runnable_locally": (
            shell_report["api_required"] is False
            and shell_report["cloud_required"] is False
            and shell_report["account_required"] is False
            and shell_report["local_first"] is True
            and shell_report["view_count"] == 8
            and shell_report["failure_state_count"] == 5
        ),
        "expansion_boundary_remains_safe": (
            interaction_report["external_services"] is False
            and interaction_report["embeddings"] is False
            and interaction_report["vector_database"] is False
            and interaction_report["live_principia_dependency"] is False
            and shell_report["live"] is False
            and shell_report["repository_mutation"] is False
        ),
    }
    if not all(exit_gates.values()):
        failed = sorted(key for key, passed in exit_gates.items() if not passed)
        raise KernelError("E-PHASE4-W1-EXIT-GATE", f"Workstream 1 exit gates failed: {failed}")

    report: dict[str, Any] = {
        "contract": COMPLETION_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 1,
        "state": "closure-candidate",
        "decision": "proceed-workstream2-browser-accessibility-evidence",
        "implementation_expansion": "bounded-browser-evidence-only",
        "accepted_evidence": {
            "interaction_contracts": {
                "pr": 42,
                "tested_head": "8172a46cd400fbcf0bce225ca908275c0d1edfdf",
                "merge_commit": "1f15cee1f0ed86c5a85750659b4d35e1d535564f",
                "baseline_sha256": _json_sha256(interaction_baseline),
                "report_digest": interaction_report["report_digest"],
            },
            "reference_shell": {
                "pr": 43,
                "tested_head": "ae6e662656c40c2108c0ef52dd2c1d7f0e2f1c0f",
                "merge_commit": "4992d0caa0eb37db5b58158a9dd53a8ca10f1405",
                "baseline_sha256": _json_sha256(shell_baseline),
                "build_digest": shell_data["build_digest"],
                "report_digest": shell_report["report_digest"],
                "static_assets": static_assets,
            },
        },
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "counts": counts,
        "workflow_kinds": interaction_report["workflow_kinds"],
        "exit_gates": exit_gates,
        "workstream2_entry_boundary": {
            "purpose": "collect real-browser accessibility and workflow evidence over the accepted static shell",
            "browser_automation_required": True,
            "keyboard_workflows_required": True,
            "focus_visibility_required": True,
            "landmark_heading_and_label_checks_required": True,
            "non_graph_workflow_equivalence_required": True,
            "failure_state_visibility_required": True,
            "offline_package_required": True,
            "external_network_requests": False,
            "production_frontend_architecture_selected": False,
            "live_principia_dependency": False,
            "canonical_mutation": False,
            "repository_mutation": False,
        },
        "review_policy": {
            "active_review_level": "ai-reviewed",
            "human_verified": False,
            "human_review_required_for_workstream1_closure": False,
        },
        "local_first": True,
        "exact_revision_required": True,
        "principia_status_separate": True,
        "retrieval_authority": "advisory-only",
        "production_retrieval_quality_claim": False,
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
    _require(report, "contract", COMPLETION_CONTRACT, "E-PHASE4-W1-COMPLETION")
    _require(report, "mode", MODE, "E-PHASE4-W1-COMPLETION")
    _require(report, "phase", 4, "E-PHASE4-W1-COMPLETION")
    _require(report, "workstream", 1, "E-PHASE4-W1-COMPLETION")
    _require(report, "state", "closure-candidate", "E-PHASE4-W1-COMPLETION")
    _require(
        report,
        "decision",
        "proceed-workstream2-browser-accessibility-evidence",
        "E-PHASE4-W1-COMPLETION",
    )
    gates = report.get("exit_gates")
    if not isinstance(gates, Mapping) or not gates or not all(value is True for value in gates.values()):
        raise KernelError("E-PHASE4-W1-COMPLETION-GATES", "all Workstream 1 exit gates must pass")
    boundary = report.get("workstream2_entry_boundary")
    if not isinstance(boundary, Mapping):
        raise KernelError("E-PHASE4-W2-BOUNDARY", "completion report requires Workstream 2 boundary")
    required_boundary = {
        "browser_automation_required": True,
        "keyboard_workflows_required": True,
        "focus_visibility_required": True,
        "non_graph_workflow_equivalence_required": True,
        "external_network_requests": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "canonical_mutation": False,
        "repository_mutation": False,
    }
    for field, expected in required_boundary.items():
        if boundary.get(field) != expected:
            raise KernelError("E-PHASE4-W2-BOUNDARY", f"unsafe Workstream 2 boundary: {field}")
    required_fields = {
        "local_first": True,
        "exact_revision_required": True,
        "principia_status_separate": True,
        "retrieval_authority": "advisory-only",
        "production_retrieval_quality_claim": False,
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
            raise KernelError("E-PHASE4-W1-COMPLETION-AUTHORITY", f"completion requires {field}={expected!r}")
    digest = report.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError("E-PHASE4-W1-COMPLETION-DIGEST", "report_digest must be SHA-256")
    unsigned = dict(report)
    unsigned.pop("report_digest", None)
    if _json_sha256(unsigned) != digest:
        raise KernelError("E-PHASE4-W1-COMPLETION-DIGEST", "completion report digest is invalid")
    return {
        "contract": COMPLETION_VALIDATION_CONTRACT,
        "decision": "valid-workstream1-closure-candidate",
        "exit_gate_count": len(gates),
        "report_digest": digest,
        "live": False,
        "repository_mutation": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/reference-interactions.v01.json"),
    )
    parser.add_argument(
        "--interaction-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/interaction-contract-baseline.json"),
    )
    parser.add_argument(
        "--shell-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/reference-shell-baseline.json"),
    )
    parser.add_argument("--shell-root", type=Path, default=Path("apps/reference-shell"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    report = run_workstream1_closure(
        args.canonical_root,
        args.manifest,
        load_json(args.interaction_baseline),
        load_json(args.shell_baseline),
        args.shell_root,
    )
    validation = validate_completion_report(report)
    rendered = render_json(report)
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote={args.output}")
    print(f"phase4-workstream1-report-digest={report['report_digest']}")
    print(f"phase4-workstream1-exit-gates={validation['exit_gate_count']}")
    print("phase4-workstream1=closure-candidate; decision=proceed-workstream2-browser-accessibility-evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
