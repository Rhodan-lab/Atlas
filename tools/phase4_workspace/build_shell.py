#!/usr/bin/env python3
"""Build the deterministic local browser package for the accepted workspace export."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import quote

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase4_workspace.contracts import MODE, validate_fixture_bundle

SHELL_DATA_CONTRACT = "atlas-workspace-shell-data/0.1"
SHELL_BUILD_REPORT_CONTRACT = "atlas-workspace-shell-build-report/0.1"
WORKSPACE_BASELINE_CONTRACT = "atlas-phase4-workspace-contract-baseline/0.1"


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _artifact(payload: bytes) -> dict[str, Any]:
    return {"bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()}


def _seal(record: Mapping[str, Any], field: str = "build_digest") -> dict[str, Any]:
    unsigned = dict(record)
    unsigned.pop(field, None)
    sealed = dict(record)
    sealed[field] = _json_sha256(unsigned)
    return sealed


def _require_accepted_artifacts(
    baseline: Mapping[str, Any],
    fixture_bytes: bytes,
    report_bytes: bytes,
    export_bytes: bytes,
    manifest_bytes: bytes,
    report: Mapping[str, Any],
    export: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> None:
    if baseline.get("contract") != WORKSPACE_BASELINE_CONTRACT:
        raise KernelError("E-WORKSPACE-SHELL-BASELINE", "workspace baseline contract mismatch")
    expected = {
        "fixture": fixture_bytes,
        "report": report_bytes,
        "export": export_bytes,
        "manifest": manifest_bytes,
    }
    for name, payload in expected.items():
        record = baseline.get(name)
        if not isinstance(record, Mapping):
            raise KernelError("E-WORKSPACE-SHELL-BASELINE", f"workspace baseline missing {name}")
        artifact_record = record.get("artifact") if name != "fixture" else record
        if not isinstance(artifact_record, Mapping):
            raise KernelError("E-WORKSPACE-SHELL-BASELINE", f"workspace baseline missing {name} artifact")
        if artifact_record.get("bytes") != len(payload):
            raise KernelError("E-WORKSPACE-SHELL-BASELINE", f"workspace {name} byte length differs from accepted evidence")
        if artifact_record.get("sha256") != hashlib.sha256(payload).hexdigest():
            raise KernelError("E-WORKSPACE-SHELL-BASELINE", f"workspace {name} SHA-256 differs from accepted evidence")
    if baseline["report"].get("report_digest") != report.get("report_digest"):
        raise KernelError("E-WORKSPACE-SHELL-BASELINE", "workspace report digest differs from accepted evidence")
    if baseline["export"].get("report_digest") != export.get("report_digest"):
        raise KernelError("E-WORKSPACE-SHELL-BASELINE", "workspace export digest differs from accepted evidence")
    if baseline["manifest"].get("report_digest") != manifest.get("report_digest"):
        raise KernelError("E-WORKSPACE-SHELL-BASELINE", "workspace manifest digest differs from accepted evidence")


def _routes(export: Mapping[str, Any]) -> list[dict[str, Any]]:
    routes: list[dict[str, Any]] = [
        {
            "id": "overview",
            "kind": "overview",
            "label": "Workspace overview",
            "hash": "#overview",
        }
    ]
    for entry in export["entries"]:
        entry_id = str(entry["entry_id"])
        routes.append(
            {
                "id": f"entry:{entry_id}",
                "kind": "entry",
                "label": f"{entry['position']}. {entry['visible_metadata']['title']}",
                "hash": f"#entry={quote(entry_id, safe='')}",
                "entry_id": entry_id,
                "position": entry["position"],
                "exact_reference": dict(entry["exact_reference"]),
                "decision": entry["decision"]["action"],
            }
        )
    routes.extend(
        [
            {"id": "candidates", "kind": "candidates", "label": "Advisory candidates", "hash": "#candidates"},
            {"id": "principia", "kind": "principia", "label": "Principia reference", "hash": "#principia"},
            {"id": "warnings", "kind": "warnings", "label": "Warnings", "hash": "#warnings"},
            {"id": "questions", "kind": "questions", "label": "Open questions", "hash": "#questions"},
            {"id": "limitations", "kind": "limitations", "label": "Limitations", "hash": "#limitations"},
            {"id": "evidence", "kind": "evidence", "label": "Export evidence", "hash": "#evidence"},
            {"id": "summary", "kind": "summary", "label": "Text summary", "hash": "#summary"},
        ]
    )
    return routes


def validate_shell_data(shell_data: Mapping[str, Any]) -> dict[str, Any]:
    if shell_data.get("contract") != SHELL_DATA_CONTRACT:
        raise KernelError("E-WORKSPACE-SHELL-CONTRACT", f"expected {SHELL_DATA_CONTRACT!r}")
    if shell_data.get("mode") != MODE or shell_data.get("phase") != 4 or shell_data.get("workstream") != 3:
        raise KernelError("E-WORKSPACE-SHELL-CONTRACT", "workspace shell phase or mode mismatch")
    if shell_data.get("slice") != 2 or shell_data.get("state") != "workspace-shell-candidate":
        raise KernelError("E-WORKSPACE-SHELL-CONTRACT", "workspace shell slice or state mismatch")
    digest = shell_data.get("build_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError("E-WORKSPACE-SHELL-DIGEST", "workspace shell requires SHA-256 build_digest")
    unsigned = dict(shell_data)
    unsigned.pop("build_digest", None)
    if _json_sha256(unsigned) != digest:
        raise KernelError("E-WORKSPACE-SHELL-DIGEST", "workspace shell build digest mismatch")
    routes = shell_data.get("routes")
    if not isinstance(routes, list) or len(routes) != 13:
        raise KernelError("E-WORKSPACE-SHELL-ROUTES", "workspace shell requires thirteen deterministic routes")
    route_ids = [route.get("id") for route in routes if isinstance(route, Mapping)]
    route_hashes = [route.get("hash") for route in routes if isinstance(route, Mapping)]
    if len(route_ids) != len(set(route_ids)) or len(route_hashes) != len(set(route_hashes)):
        raise KernelError("E-WORKSPACE-SHELL-ROUTES", "workspace shell route IDs and hashes must be unique")
    if any("latest" in str(value).lower() for value in route_hashes):
        raise KernelError("E-WORKSPACE-SHELL-ROUTES", "workspace shell routes may not use implicit latest")
    entry_routes = [route for route in routes if isinstance(route, Mapping) and route.get("kind") == "entry"]
    if [route.get("position") for route in entry_routes] != [1, 2, 3, 4, 5]:
        raise KernelError("E-WORKSPACE-SHELL-ORDER", "workspace entry routes must preserve accepted order")
    authority = shell_data.get("authority")
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
    if not isinstance(authority, Mapping):
        raise KernelError("E-WORKSPACE-SHELL-AUTHORITY", "workspace shell authority block is required")
    for field, expected in required_authority.items():
        if authority.get(field) != expected:
            raise KernelError("E-WORKSPACE-SHELL-AUTHORITY", f"workspace shell requires {field}={expected!r}")
    return {
        "contract": "atlas-workspace-shell-validation/0.1",
        "decision": "valid",
        "route_count": len(routes),
        "entry_route_count": len(entry_routes),
        "build_digest": digest,
        "live": False,
        "repository_mutation": False,
    }


def build_workspace_shell(
    canonical_root: Path,
    fixture_path: Path,
    research_fixture_path: Path,
    research_baseline_path: Path,
    structured_baseline_path: Path,
    bridge_fixture_path: Path,
    workspace_baseline_path: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, bytes]]:
    repository = KernelRepository(compile_canonical(canonical_root))
    fixture = load_json(fixture_path)
    report, export, manifest = validate_fixture_bundle(
        fixture,
        repository,
        load_json(research_fixture_path),
        load_json(research_baseline_path),
        load_json(structured_baseline_path),
        load_json(bridge_fixture_path),
    )
    artifact_bytes = {
        "fixture": fixture_path.read_bytes(),
        "report": render_json(report).encode("utf-8"),
        "export": render_json(export).encode("utf-8"),
        "manifest": render_json(manifest).encode("utf-8"),
    }
    baseline = load_json(workspace_baseline_path)
    _require_accepted_artifacts(
        baseline,
        artifact_bytes["fixture"],
        artifact_bytes["report"],
        artifact_bytes["export"],
        artifact_bytes["manifest"],
        report,
        export,
        manifest,
    )
    routes = _routes(export)
    shell_data = _seal(
        {
            "contract": SHELL_DATA_CONTRACT,
            "mode": MODE,
            "phase": 4,
            "workstream": 3,
            "slice": 2,
            "state": "workspace-shell-candidate",
            "source_digest": repository.runtime["source_digest"],
            "workspace": dict(export["workspace"]),
            "accepted_export": {
                "contract": export["contract"],
                "artifact": _artifact(artifact_bytes["export"]),
                "report_digest": export["report_digest"],
                "file": "data/workspace-export.json",
            },
            "accepted_manifest": {
                "contract": manifest["contract"],
                "artifact": _artifact(artifact_bytes["manifest"]),
                "report_digest": manifest["report_digest"],
                "file": "data/workspace-manifest.json",
            },
            "routes": routes,
            "counts": {
                "routes": len(routes),
                "entries": len(export["entries"]),
                "candidates": len(export["candidate_references"]),
                "principia_references": len(export["principia_references"]),
                "warnings": len(export["warning_references"]),
                "open_questions": len(export["open_questions"]),
                "limitations": len(export["limitations"]),
            },
            "download": {
                "file": "workspace-export.json",
                "bytes": len(artifact_bytes["export"]),
                "sha256": hashlib.sha256(artifact_bytes["export"]).hexdigest(),
                "local_only": True,
                "canonical_write": False,
            },
            "authority": {
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
            },
        }
    )
    validation = validate_shell_data(shell_data)
    build_report = _seal(
        {
            "contract": SHELL_BUILD_REPORT_CONTRACT,
            "mode": MODE,
            "phase": 4,
            "workstream": 3,
            "slice": 2,
            "state": "workspace-shell-candidate",
            "decision": "workspace-shell-candidate",
            "source_digest": repository.runtime["source_digest"],
            "workspace_id": shell_data["workspace"]["id"],
            "workspace_revision": shell_data["workspace"]["revision"],
            "shell_build_digest": shell_data["build_digest"],
            "validation_digest": validation["build_digest"],
            "export_digest": export["report_digest"],
            "manifest_digest": manifest["report_digest"],
            "route_count": len(routes),
            "entry_route_count": 5,
            "static_assets": ["index.html", "styles.css", "app.js"],
            "generated_files": [
                "data/workspace-shell-data.json",
                "data/workspace-export.json",
                "data/workspace-manifest.json",
            ],
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
        },
        field="report_digest",
    )
    return shell_data, build_report, export, manifest, artifact_bytes


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument("--fixture", type=Path, default=Path("content/fixtures/phase4_workspace/research-workspace.v01.json"))
    parser.add_argument("--research-fixture", type=Path, default=Path("content/fixtures/phase3_retrieval/research-foundations.v01.json"))
    parser.add_argument("--research-baseline", type=Path, default=Path("content/fixtures/phase3_retrieval/research-foundations-baseline.json"))
    parser.add_argument("--structured-baseline", type=Path, default=Path("content/fixtures/phase3_retrieval/structured-baseline.json"))
    parser.add_argument("--bridge-fixture", type=Path, default=Path("content/fixtures/phase4_interaction/bridge-failures.v01.json"))
    parser.add_argument("--workspace-baseline", type=Path, default=Path("content/fixtures/phase4_workspace/workspace-contract-baseline.json"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args(argv)

    shell_data, report, export, manifest, _ = build_workspace_shell(
        args.canonical_root,
        args.fixture,
        args.research_fixture,
        args.research_baseline,
        args.structured_baseline,
        args.bridge_fixture,
        args.workspace_baseline,
    )
    if args.output_dir is not None:
        data_dir = args.output_dir / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "workspace-shell-data.json").write_text(render_json(shell_data), encoding="utf-8")
        (data_dir / "workspace-export.json").write_text(render_json(export), encoding="utf-8")
        (data_dir / "workspace-manifest.json").write_text(render_json(manifest), encoding="utf-8")
        print(f"wrote={data_dir / 'workspace-shell-data.json'}")
        print(f"wrote={data_dir / 'workspace-export.json'}")
        print(f"wrote={data_dir / 'workspace-manifest.json'}")
    rendered_report = render_json(report)
    if args.report_output is None:
        sys.stdout.write(rendered_report)
    else:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(rendered_report, encoding="utf-8")
        print(f"wrote={args.report_output}")
    print(f"phase4-workspace-shell-build-digest={shell_data['build_digest']}")
    print(f"phase4-workspace-shell-report-digest={report['report_digest']}")
    print("phase4-workspace-shell=candidate; accepted-export-only=true; live=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
