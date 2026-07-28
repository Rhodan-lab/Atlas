#!/usr/bin/env python3
"""Deterministic Phase 4 interaction, bridge, warning, and failure contracts."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json

MODE = "interactive-experience-foundation"
INTERACTION_STATE_CONTRACT = "atlas-interaction-state/0.1"
INTERACTION_VIEW_CONTRACT = "atlas-interaction-view/0.1"
PRINCIPIA_REFERENCE_CONTRACT = "atlas-principia-reference-envelope/0.1"
IMPACT_WARNING_CONTRACT = "atlas-cross-repository-impact-warning/0.1"
FAILURE_STATE_CONTRACT = "atlas-interaction-failure/0.1"
FIXTURE_CONTRACT = "atlas-phase4-interaction-fixtures/0.1"
REPORT_CONTRACT = "atlas-phase4-interaction-contract-report/0.1"

ID_RE = re.compile(r"^[a-z][a-z0-9-]*(?::[a-z0-9-]+)+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
VIEW_KINDS = frozenset(
    {
        "entity",
        "provenance",
        "retrieval",
        "filter",
        "research-trail",
        "candidate",
        "principia-reference",
        "impact-warning",
    }
)
IMPACT_STATES = frozenset({"current", "stale", "unavailable", "status-mismatch", "fixture-only"})
WARNING_SEVERITIES = frozenset({"info", "warning", "blocking"})
FAILURE_CATEGORIES = frozenset(
    {
        "malformed-state",
        "unknown-view",
        "entity-missing",
        "revision-unavailable",
        "provenance-missing",
        "artifact-malformed",
        "principia-reference-unavailable",
        "principia-status-mismatch",
        "offline-artifact-missing",
        "authority-escalation",
    }
)
ALLOWED_GENERATED_CONTRACTS = frozenset(
    {
        "atlas-phase3-structured-baseline/0.1",
        "atlas-filtered-result-set/0.1",
        "atlas-research-trail/0.1",
        "atlas-contradiction-candidate/0.1",
        "atlas-duplicate-candidate/0.1",
    }
)


def _mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def _string(value: Any, code: str, message: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KernelError(code, message)
    return value


def _positive_int(value: Any, code: str, message: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise KernelError(code, message)
    return value


def _unique_strings(value: Any, code: str, message: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise KernelError(code, message)
    if not allow_empty and not value:
        raise KernelError(code, message)
    if len(value) != len(set(value)):
        raise KernelError(code, message + " and may not contain duplicates")
    return list(value)


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _validate_id(value: Any, code: str, label: str) -> str:
    identifier = _string(value, code, f"{label} ID is required")
    if not ID_RE.fullmatch(identifier):
        raise KernelError(code, f"{label} ID must be a colon-qualified lowercase identifier")
    return identifier


def _exact_key(entity_id: str, revision: int) -> str:
    return f"{entity_id}@{revision}"


def _validate_exact_ref(
    record: Mapping[str, Any],
    repository: KernelRepository,
    code: str,
    *,
    allow_unavailable: bool = False,
) -> dict[str, Any]:
    entity_id = _string(record.get("id"), code, "Atlas reference requires id")
    revision = _positive_int(record.get("revision"), code, "Atlas reference requires positive revision")
    try:
        entity = repository.exact(entity_id, revision)
    except KernelError:
        if not allow_unavailable:
            raise
        entity = None
    return {
        "id": entity_id,
        "revision": revision,
        "key": _exact_key(entity_id, revision),
        "available": entity is not None,
    }


def _validate_authority(record: Mapping[str, Any], code: str) -> None:
    expected = {
        "live": False,
        "repository_mutation": False,
        "canonical_mutation": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
    }
    for field, value in expected.items():
        if record.get(field) is not value:
            raise KernelError(code, f"{field} must be {value!r}")


def validate_view(record: Mapping[str, Any], repository: KernelRepository) -> dict[str, Any]:
    if record.get("contract") != INTERACTION_VIEW_CONTRACT:
        raise KernelError("E-INTERACTION-VIEW-CONTRACT", f"expected {INTERACTION_VIEW_CONTRACT!r}")
    view_id = _validate_id(record.get("id"), "E-INTERACTION-VIEW-ID", "view")
    revision = _positive_int(record.get("revision"), "E-INTERACTION-VIEW-REVISION", "view revision must be positive")
    kind = record.get("kind")
    if kind not in VIEW_KINDS:
        raise KernelError("E-INTERACTION-VIEW-KIND", f"unsupported view kind {kind!r}")
    _string(record.get("title"), "E-INTERACTION-VIEW-TITLE", "view title is required")

    atlas_refs_raw = record.get("atlas_refs")
    if not isinstance(atlas_refs_raw, list) or not atlas_refs_raw:
        raise KernelError("E-INTERACTION-VIEW-REF", "view requires at least one exact Atlas reference")
    refs = [
        _validate_exact_ref(_mapping(item, "E-INTERACTION-VIEW-REF", "atlas_refs entries must be objects"), repository, "E-INTERACTION-VIEW-REF")
        for item in atlas_refs_raw
    ]
    keys = [item["key"] for item in refs]
    if len(keys) != len(set(keys)):
        raise KernelError("E-INTERACTION-VIEW-REF", "view may not repeat an exact Atlas reference")

    authority = _mapping(record.get("authority"), "E-INTERACTION-VIEW-AUTHORITY", "view authority metadata is required")
    required_authority = {
        "exact_revision_visible": True,
        "provenance_visible": True,
        "review_level_visible": True,
        "lifecycle_visible": True,
        "staleness_visible": True,
        "advisory_only": True,
    }
    for field, expected in required_authority.items():
        if authority.get(field) is not expected:
            raise KernelError("E-INTERACTION-VIEW-AUTHORITY", f"view requires {field}={expected!r}")

    keyboard_path = _unique_strings(
        record.get("keyboard_path"),
        "E-INTERACTION-ACCESSIBILITY",
        "view requires a unique keyboard path",
    )
    non_graph_path = _unique_strings(
        record.get("non_graph_path"),
        "E-INTERACTION-ACCESSIBILITY",
        "view requires a unique non-graph path",
    )
    if record.get("graph_required") is not False:
        raise KernelError("E-INTERACTION-ACCESSIBILITY", "graph visualization may not be required")
    if not keyboard_path or not non_graph_path:
        raise KernelError("E-INTERACTION-ACCESSIBILITY", "keyboard and non-graph paths are required")

    artifact = record.get("generated_artifact")
    artifact_contract = None
    if artifact is not None:
        artifact_record = _mapping(
            artifact,
            "E-INTERACTION-ARTIFACT",
            "generated_artifact must be an object",
        )
        artifact_contract = artifact_record.get("contract")
        if artifact_contract not in ALLOWED_GENERATED_CONTRACTS:
            raise KernelError("E-INTERACTION-ARTIFACT", "view uses an unsupported generated artifact contract")
        for field in ("build_digest", "source_digest"):
            digest = artifact_record.get(field)
            if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                raise KernelError("E-INTERACTION-ARTIFACT", f"generated artifact {field} must be SHA-256")
        if artifact_record.get("replaceable") is not True or artifact_record.get("advisory_only") is not True:
            raise KernelError("E-INTERACTION-ARTIFACT", "generated artifact must remain replaceable and advisory")

    _validate_authority(record, "E-INTERACTION-VIEW-AUTHORITY")
    return {
        "contract": "atlas-interaction-view-validation/0.1",
        "id": view_id,
        "revision": revision,
        "kind": kind,
        "atlas_ref_count": len(refs),
        "artifact_contract": artifact_contract,
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }


def validate_state(
    record: Mapping[str, Any],
    views: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    if record.get("contract") != INTERACTION_STATE_CONTRACT:
        raise KernelError("E-INTERACTION-STATE-CONTRACT", f"expected {INTERACTION_STATE_CONTRACT!r}")
    state_id = _validate_id(record.get("id"), "E-INTERACTION-STATE-ID", "state")
    revision = _positive_int(record.get("revision"), "E-INTERACTION-STATE-REVISION", "state revision must be positive")
    if record.get("mode") != MODE:
        raise KernelError("E-INTERACTION-STATE-MODE", f"state mode must be {MODE!r}")
    route = _string(record.get("route"), "E-INTERACTION-STATE-ROUTE", "state route is required")
    if not route.startswith("/") or "latest" in route.lower():
        raise KernelError("E-INTERACTION-STATE-ROUTE", "route must be explicit and may not use implicit latest")

    active = _mapping(record.get("active_view"), "E-INTERACTION-STATE-VIEW", "active_view must be an object")
    active_id = _string(active.get("id"), "E-INTERACTION-STATE-VIEW", "active view id is required")
    active_revision = _positive_int(active.get("revision"), "E-INTERACTION-STATE-VIEW", "active view revision is required")
    active_key = _exact_key(active_id, active_revision)
    if active_key not in views:
        raise KernelError("E-INTERACTION-STATE-VIEW", f"active view {active_key} is unavailable")

    history_raw = record.get("history")
    if not isinstance(history_raw, list) or not history_raw:
        raise KernelError("E-INTERACTION-STATE-HISTORY", "state requires nonempty deterministic history")
    history_keys: list[str] = []
    for item in history_raw:
        entry = _mapping(item, "E-INTERACTION-STATE-HISTORY", "history entries must be objects")
        view_id = _string(entry.get("id"), "E-INTERACTION-STATE-HISTORY", "history view id is required")
        view_revision = _positive_int(entry.get("revision"), "E-INTERACTION-STATE-HISTORY", "history revision is required")
        key = _exact_key(view_id, view_revision)
        if key not in views:
            raise KernelError("E-INTERACTION-STATE-HISTORY", f"history view {key} is unavailable")
        history_keys.append(key)
    if len(history_keys) != len(set(history_keys)):
        raise KernelError("E-INTERACTION-STATE-HISTORY", "history may not repeat exact views")
    if history_keys[-1] != active_key:
        raise KernelError("E-INTERACTION-STATE-HISTORY", "active view must be the final history entry")

    if record.get("deterministic_navigation") is not True or record.get("offline_capable") is not True:
        raise KernelError("E-INTERACTION-STATE-NAVIGATION", "state must support deterministic offline navigation")
    if record.get("canonical_copy") is not False:
        raise KernelError("E-INTERACTION-STATE-AUTHORITY", "interaction state may not copy canonical authority")
    _validate_authority(record, "E-INTERACTION-STATE-AUTHORITY")
    return {
        "contract": "atlas-interaction-state-validation/0.1",
        "id": state_id,
        "revision": revision,
        "active_view": active_key,
        "history_length": len(history_keys),
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }


def validate_principia_reference(
    record: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    if record.get("contract") != PRINCIPIA_REFERENCE_CONTRACT:
        raise KernelError("E-PRINCIPIA-REFERENCE-CONTRACT", f"expected {PRINCIPIA_REFERENCE_CONTRACT!r}")
    reference_id = _validate_id(record.get("id"), "E-PRINCIPIA-REFERENCE-ID", "Principia reference")
    revision = _positive_int(record.get("revision"), "E-PRINCIPIA-REFERENCE-REVISION", "reference revision must be positive")
    _string(record.get("principia_artifact_id"), "E-PRINCIPIA-REFERENCE", "Principia artifact id is required")
    _positive_int(record.get("principia_artifact_revision"), "E-PRINCIPIA-REFERENCE", "Principia revision must be positive")
    _string(record.get("principia_status"), "E-PRINCIPIA-REFERENCE", "Principia status is required")
    _string(record.get("reference_purpose"), "E-PRINCIPIA-REFERENCE", "reference purpose is required")
    impact_state = record.get("impact_state")
    if impact_state not in IMPACT_STATES:
        raise KernelError("E-PRINCIPIA-REFERENCE", "unsupported impact state")

    refs_raw = record.get("atlas_references")
    if not isinstance(refs_raw, list) or not refs_raw:
        raise KernelError("E-PRINCIPIA-REFERENCE", "Principia envelope requires exact Atlas references")
    refs = [
        _validate_exact_ref(_mapping(item, "E-PRINCIPIA-REFERENCE", "Atlas references must be objects"), repository, "E-PRINCIPIA-REFERENCE")
        for item in refs_raw
    ]
    keys = [item["key"] for item in refs]
    if len(keys) != len(set(keys)):
        raise KernelError("E-PRINCIPIA-REFERENCE", "Principia envelope repeats an exact Atlas reference")

    if (
        record.get("fixture_only") is not True
        or record.get("principia_status_separate") is not True
        or record.get("implicit_latest") is not False
        or record.get("automatic_status_inheritance") is not False
    ):
        raise KernelError("E-PRINCIPIA-REFERENCE-AUTHORITY", "Principia reference must remain fixture-only, exact, and status-separate")
    _validate_authority(record, "E-PRINCIPIA-REFERENCE-AUTHORITY")
    return {
        "contract": "atlas-principia-reference-validation/0.1",
        "id": reference_id,
        "revision": revision,
        "atlas_reference_count": len(refs),
        "impact_state": impact_state,
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }


def validate_impact_warning(
    record: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    if record.get("contract") != IMPACT_WARNING_CONTRACT:
        raise KernelError("E-IMPACT-CONTRACT", f"expected {IMPACT_WARNING_CONTRACT!r}")
    warning_id = _validate_id(record.get("id"), "E-IMPACT-ID", "impact warning")
    revision = _positive_int(record.get("revision"), "E-IMPACT-REVISION", "impact warning revision must be positive")
    state = record.get("impact_state")
    if state not in IMPACT_STATES - {"current"}:
        raise KernelError("E-IMPACT-STATE", "impact warning requires a non-current impact state")
    severity = record.get("severity")
    if severity not in WARNING_SEVERITIES:
        raise KernelError("E-IMPACT-SEVERITY", "unsupported impact warning severity")
    target_record = _mapping(record.get("target"), "E-IMPACT-TARGET", "impact warning target is required")
    target = _validate_exact_ref(target_record, repository, "E-IMPACT-TARGET", allow_unavailable=True)
    available_revisions = record.get("available_revisions")
    if not isinstance(available_revisions, list) or not all(
        isinstance(item, int) and not isinstance(item, bool) and item > 0 for item in available_revisions
    ):
        raise KernelError("E-IMPACT-TARGET", "available_revisions must be positive integers")
    expected_available = repository.available_revisions(target["id"])
    if available_revisions != expected_available:
        raise KernelError("E-IMPACT-TARGET", f"available_revisions must equal {expected_available}")
    if state == "unavailable" and target["available"]:
        raise KernelError("E-IMPACT-STATE", "unavailable warning target unexpectedly exists")
    _string(record.get("message"), "E-IMPACT-MESSAGE", "impact warning message is required")
    actions = _unique_strings(record.get("recovery_actions"), "E-IMPACT-RECOVERY", "impact warning requires recovery actions")
    if record.get("automatic_update") is not False or record.get("implicit_latest") is not False:
        raise KernelError("E-IMPACT-AUTHORITY", "impact warnings may not update references or substitute latest")
    _validate_authority(record, "E-IMPACT-AUTHORITY")
    return {
        "contract": "atlas-impact-warning-validation/0.1",
        "id": warning_id,
        "revision": revision,
        "impact_state": state,
        "severity": severity,
        "target": target["key"],
        "recovery_action_count": len(actions),
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }


def validate_failure_state(record: Mapping[str, Any]) -> dict[str, Any]:
    if record.get("contract") != FAILURE_STATE_CONTRACT:
        raise KernelError("E-INTERACTION-FAILURE-CONTRACT", f"expected {FAILURE_STATE_CONTRACT!r}")
    failure_id = _validate_id(record.get("id"), "E-INTERACTION-FAILURE-ID", "failure state")
    revision = _positive_int(record.get("revision"), "E-INTERACTION-FAILURE-REVISION", "failure revision must be positive")
    category = record.get("category")
    if category not in FAILURE_CATEGORIES:
        raise KernelError("E-INTERACTION-FAILURE-CATEGORY", "unsupported failure category")
    error_code = _string(record.get("error_code"), "E-INTERACTION-FAILURE-CODE", "failure error code is required")
    if not error_code.startswith("E-"):
        raise KernelError("E-INTERACTION-FAILURE-CODE", "failure error code must start with E-")
    _string(record.get("summary"), "E-INTERACTION-FAILURE-SUMMARY", "failure summary is required")
    _unique_strings(record.get("recovery_actions"), "E-INTERACTION-FAILURE-RECOVERY", "failure requires recovery actions")
    if (
        record.get("preserve_previous_state") is not True
        or record.get("silent_fallback") is not False
        or record.get("implicit_latest") is not False
        or record.get("canonical_copy") is not False
    ):
        raise KernelError("E-INTERACTION-FAILURE-AUTHORITY", "failure state must preserve state and forbid silent authority changes")
    _validate_authority(record, "E-INTERACTION-FAILURE-AUTHORITY")
    return {
        "contract": "atlas-interaction-failure-validation/0.1",
        "id": failure_id,
        "revision": revision,
        "category": category,
        "error_code": error_code,
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }


def _expect_error(callable_, expected: str) -> dict[str, Any]:
    try:
        callable_()
    except KernelError as exc:
        if exc.code != expected:
            raise KernelError("E-INTERACTION-NEGATIVE", f"expected {expected}, observed {exc.code}") from exc
        return {"expected_error": expected, "observed_error": exc.code, "decision": "expected-failure"}
    raise KernelError("E-INTERACTION-NEGATIVE", f"expected failure {expected} was not raised")


def validate_fixture_bundle(
    payload: Mapping[str, Any],
    repository: KernelRepository,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    if payload.get("contract") != FIXTURE_CONTRACT:
        raise KernelError("E-INTERACTION-FIXTURE-CONTRACT", f"expected {FIXTURE_CONTRACT!r}")
    fixture_id = _validate_id(payload.get("id"), "E-INTERACTION-FIXTURE-ID", "fixture bundle")
    version = _positive_int(payload.get("version"), "E-INTERACTION-FIXTURE-VERSION", "fixture version must be positive")
    if payload.get("mode") != MODE:
        raise KernelError("E-INTERACTION-FIXTURE-MODE", f"fixture mode must be {MODE!r}")
    if payload.get("source_digest") != repository.runtime["source_digest"]:
        raise KernelError("E-INTERACTION-FIXTURE-SOURCE", "fixture source digest differs from canonical runtime")

    views_raw = payload.get("views")
    if not isinstance(views_raw, list) or not views_raw:
        raise KernelError("E-INTERACTION-FIXTURE-VIEWS", "fixture bundle requires views")
    views: dict[str, dict[str, Any]] = {}
    for raw in views_raw:
        record = _mapping(raw, "E-INTERACTION-FIXTURE-VIEWS", "view fixtures must be objects")
        validation = validate_view(record, repository)
        key = _exact_key(validation["id"], validation["revision"])
        if key in views:
            raise KernelError("E-INTERACTION-FIXTURE-VIEWS", f"duplicate view {key}")
        views[key] = dict(record)

    states_raw = payload.get("states")
    if not isinstance(states_raw, list) or not states_raw:
        raise KernelError("E-INTERACTION-FIXTURE-STATES", "fixture bundle requires states")
    state_validations = [
        validate_state(_mapping(raw, "E-INTERACTION-FIXTURE-STATES", "state fixtures must be objects"), views)
        for raw in states_raw
    ]

    principia_raw = payload.get("principia_references")
    if not isinstance(principia_raw, list) or not principia_raw:
        raise KernelError("E-INTERACTION-FIXTURE-PRINCIPIA", "fixture bundle requires Principia references")
    principia_validations = [
        validate_principia_reference(
            _mapping(raw, "E-INTERACTION-FIXTURE-PRINCIPIA", "Principia references must be objects"),
            repository,
        )
        for raw in principia_raw
    ]

    warnings_raw = payload.get("impact_warnings")
    if not isinstance(warnings_raw, list) or not warnings_raw:
        raise KernelError("E-INTERACTION-FIXTURE-WARNINGS", "fixture bundle requires impact warnings")
    warning_validations = [
        validate_impact_warning(
            _mapping(raw, "E-INTERACTION-FIXTURE-WARNINGS", "impact warnings must be objects"),
            repository,
        )
        for raw in warnings_raw
    ]

    failures_raw = payload.get("failure_states")
    if not isinstance(failures_raw, list) or not failures_raw:
        raise KernelError("E-INTERACTION-FIXTURE-FAILURES", "fixture bundle requires failure states")
    failure_validations = [
        validate_failure_state(_mapping(raw, "E-INTERACTION-FIXTURE-FAILURES", "failure states must be objects"))
        for raw in failures_raw
    ]

    negatives = payload.get("negative_cases")
    if not isinstance(negatives, list) or not negatives:
        raise KernelError("E-INTERACTION-FIXTURE-NEGATIVES", "fixture bundle requires negative cases")
    negative_validations: list[dict[str, Any]] = []
    for raw in negatives:
        case = _mapping(raw, "E-INTERACTION-FIXTURE-NEGATIVES", "negative cases must be objects")
        kind = case.get("kind")
        expected = _string(case.get("expected_error"), "E-INTERACTION-NEGATIVE", "negative case expected_error is required")
        record = _mapping(case.get("record"), "E-INTERACTION-NEGATIVE", "negative case record is required")
        if kind == "view":
            negative_validations.append(_expect_error(lambda record=record: validate_view(record, repository), expected))
        elif kind == "state":
            negative_validations.append(_expect_error(lambda record=record: validate_state(record, views), expected))
        elif kind == "principia-reference":
            negative_validations.append(
                _expect_error(lambda record=record: validate_principia_reference(record, repository), expected)
            )
        elif kind == "impact-warning":
            negative_validations.append(_expect_error(lambda record=record: validate_impact_warning(record, repository), expected))
        elif kind == "failure-state":
            negative_validations.append(_expect_error(lambda record=record: validate_failure_state(record), expected))
        else:
            raise KernelError("E-INTERACTION-NEGATIVE", f"unsupported negative case kind {kind!r}")

    workflow_kinds = sorted({validation["kind"] for validation in (validate_view(view, repository) for view in views.values())})
    report: dict[str, Any] = {
        "contract": REPORT_CONTRACT,
        "mode": MODE,
        "state": "interaction-contract-candidate",
        "fixture_id": fixture_id,
        "fixture_version": version,
        "fixture_sha256": _json_sha256(payload),
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "counts": {
            "views": len(views),
            "states": len(state_validations),
            "principia_references": len(principia_validations),
            "impact_warnings": len(warning_validations),
            "failure_states": len(failure_validations),
            "negative_cases": len(negative_validations),
        },
        "workflow_kinds": workflow_kinds,
        "exact_revision_preserved": True,
        "authority_metadata_visible": True,
        "keyboard_paths_required": True,
        "non_graph_paths_required": True,
        "principia_status_separate": True,
        "impact_warnings_required": True,
        "offline_capable": True,
        "graph_visualization_optional": True,
        "canonical_copy_authority": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "live_principia_dependency": False,
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "live": False,
        "repository_mutation": False,
        "negative_validations": negative_validations,
        "decision": "interaction-contract-candidate",
    }
    report["report_digest"] = _json_sha256(report)
    return report, views


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/reference-interactions.v01.json"),
    )
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args(argv)

    repository = KernelRepository(compile_canonical(args.canonical_root))
    payload = load_json(args.fixtures)
    report, _ = validate_fixture_bundle(payload, repository)
    rendered = render_json(report)
    if args.report_output is None:
        sys.stdout.write(rendered)
    else:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(rendered, encoding="utf-8")
        print(f"wrote={args.report_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
