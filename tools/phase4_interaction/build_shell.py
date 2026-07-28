#!/usr/bin/env python3
"""Build deterministic local data for the Phase 4 Atlas reference shell."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, render_json
from tools.phase4_interaction.contracts import MODE, validate_fixture_bundle
from tools.phase4_interaction.fixtures import load_fixture_manifest

SHELL_DATA_CONTRACT = "atlas-reference-shell-data/0.1"
SHELL_BUILD_REPORT_CONTRACT = "atlas-reference-shell-build-report/0.1"


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _view_key(record: Mapping[str, Any]) -> str:
    return f"{record['id']}@{record['revision']}"


def validate_shell_data(payload: Mapping[str, Any]) -> dict[str, Any]:
    if payload.get("contract") != SHELL_DATA_CONTRACT:
        raise KernelError("E-SHELL-DATA-CONTRACT", f"expected {SHELL_DATA_CONTRACT!r}")
    if payload.get("mode") != MODE:
        raise KernelError("E-SHELL-DATA-MODE", f"mode must be {MODE!r}")
    for field in ("source_digest", "fixture_sha256", "interaction_report_digest", "build_digest"):
        value = payload.get(field)
        if not isinstance(value, str) or len(value) != 64:
            raise KernelError("E-SHELL-DATA-DIGEST", f"{field} must be SHA-256")
    expected_digest = dict(payload)
    observed = expected_digest.pop("build_digest")
    if _json_sha256(expected_digest) != observed:
        raise KernelError("E-SHELL-DATA-DIGEST", "shell build digest is invalid")

    views = payload.get("views")
    states = payload.get("states")
    failures = payload.get("failure_states")
    if not isinstance(views, list) or not views:
        raise KernelError("E-SHELL-DATA-VIEWS", "shell data requires views")
    if not isinstance(states, list) or not states:
        raise KernelError("E-SHELL-DATA-STATES", "shell data requires states")
    if not isinstance(failures, list) or not failures:
        raise KernelError("E-SHELL-DATA-FAILURES", "shell data requires failure states")

    view_keys = [_view_key(view) for view in views]
    if len(view_keys) != len(set(view_keys)):
        raise KernelError("E-SHELL-DATA-VIEWS", "shell data repeats an exact view")
    available = set(view_keys)
    for state in states:
        route = state.get("route")
        if not isinstance(route, str) or not route.startswith("/") or "latest" in route.lower():
            raise KernelError("E-SHELL-DATA-ROUTE", "shell state route must be explicit")
        active = state.get("active_view")
        if not isinstance(active, Mapping):
            raise KernelError("E-SHELL-DATA-STATE", "shell state requires active_view")
        key = f"{active.get('id')}@{active.get('revision')}"
        if key not in available:
            raise KernelError("E-SHELL-DATA-STATE", f"shell state references unavailable view {key}")

    authority = payload.get("authority")
    if not isinstance(authority, Mapping):
        raise KernelError("E-SHELL-DATA-AUTHORITY", "shell data requires authority record")
    required_false = (
        "canonical_copy_authority",
        "canonical_mutation",
        "automatic_status_change",
        "automatic_release_action",
        "live_principia_dependency",
        "external_services",
        "embeddings",
        "vector_database",
        "live",
        "repository_mutation",
    )
    for field in required_false:
        if authority.get(field) is not False:
            raise KernelError("E-SHELL-DATA-AUTHORITY", f"{field} must remain false")
    required_true = (
        "exact_revision_required",
        "authority_metadata_visible",
        "keyboard_paths_required",
        "non_graph_paths_required",
        "principia_status_separate",
        "offline_capable",
        "graph_visualization_optional",
    )
    for field in required_true:
        if authority.get(field) is not True:
            raise KernelError("E-SHELL-DATA-AUTHORITY", f"{field} must remain true")

    return {
        "contract": "atlas-reference-shell-data-validation/0.1",
        "view_count": len(views),
        "state_count": len(states),
        "failure_count": len(failures),
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }


def build_shell_data(
    canonical_root: Path,
    manifest_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    repository = KernelRepository(compile_canonical(canonical_root))
    fixture = load_fixture_manifest(manifest_path)
    interaction_report, _ = validate_fixture_bundle(fixture, repository)

    states_by_view = {
        _view_key(state["active_view"]): state
        for state in fixture["states"]
    }
    views: list[dict[str, Any]] = []
    for source_view in fixture["views"]:
        view = dict(source_view)
        state = states_by_view[_view_key(source_view)]
        view["route"] = state["route"]
        views.append(view)

    payload: dict[str, Any] = {
        "contract": SHELL_DATA_CONTRACT,
        "mode": MODE,
        "fixture_id": fixture["id"],
        "fixture_version": fixture["version"],
        "fixture_sha256": interaction_report["fixture_sha256"],
        "interaction_report_digest": interaction_report["report_digest"],
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "views": views,
        "states": fixture["states"],
        "principia_references": fixture["principia_references"],
        "impact_warnings": fixture["impact_warnings"],
        "failure_states": fixture["failure_states"],
        "authority": {
            "exact_revision_required": True,
            "authority_metadata_visible": True,
            "keyboard_paths_required": True,
            "non_graph_paths_required": True,
            "principia_status_separate": True,
            "offline_capable": True,
            "graph_visualization_optional": True,
            "canonical_copy_authority": False,
            "canonical_mutation": False,
            "automatic_status_change": False,
            "automatic_release_action": False,
            "live_principia_dependency": False,
            "external_services": False,
            "embeddings": False,
            "vector_database": False,
            "live": False,
            "repository_mutation": False,
        },
    }
    payload["build_digest"] = _json_sha256(payload)
    validation = validate_shell_data(payload)
    report = {
        "contract": SHELL_BUILD_REPORT_CONTRACT,
        "mode": MODE,
        "state": "reference-shell-candidate",
        "decision": "reference-shell-candidate",
        "source_digest": payload["source_digest"],
        "fixture_sha256": payload["fixture_sha256"],
        "interaction_report_digest": payload["interaction_report_digest"],
        "shell_build_digest": payload["build_digest"],
        "view_count": validation["view_count"],
        "state_count": validation["state_count"],
        "principia_reference_count": len(payload["principia_references"]),
        "impact_warning_count": len(payload["impact_warnings"]),
        "failure_state_count": validation["failure_count"],
        "static_assets": ["index.html", "styles.css", "app.js"],
        "api_required": False,
        "cloud_required": False,
        "account_required": False,
        "graph_required": False,
        "keyboard_navigation_required": True,
        "non_graph_navigation_required": True,
        "local_first": True,
        "replaceable": True,
        "live": False,
        "repository_mutation": False,
    }
    report["report_digest"] = _json_sha256(report)
    return payload, report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/reference-interactions.v01.json"),
    )
    parser.add_argument("--output-dir", type=Path, default=Path("apps/reference-shell"))
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args(argv)

    payload, report = build_shell_data(args.canonical_root, args.manifest)
    data_path = args.output_dir / "data" / "reference-shell-data.json"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(render_json(payload), encoding="utf-8")
    print(f"wrote={data_path}")

    rendered_report = render_json(report)
    if args.report_output is None:
        sys.stdout.write(rendered_report)
    else:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(rendered_report, encoding="utf-8")
        print(f"wrote={args.report_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
