"""Compile repository-registered Principia evidence snapshots into one Atlas catalog."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

from .evidence_bridge import validate_reference_snapshot
from .evidence_review import build_review_aware_manifest
from .kernel import KernelError, render_json

REGISTRY_CONTRACT = "atlas-principia-evidence-registry/0.1"
REGISTRY_CATALOG_CONTRACT = "atlas-principia-evidence-registry-catalog/0.1"
REGISTRY_STATE = "repository-baseline"
_ROUTE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_HEX_40 = re.compile(r"^[0-9a-f]{40}$")
_TOP_LEVEL_FIELDS = {"contract", "live", "status_inheritance", "entries"}
_ENTRY_FIELDS = {
    "route_id",
    "snapshot_path",
    "state",
    "registration_basis",
    "registration_commit",
}


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def validate_evidence_registry(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate the append-only repository baseline registry contract."""
    _require(
        isinstance(payload, Mapping),
        "E-EVIDENCE-REGISTRY",
        "registry must be an object",
    )
    source = dict(payload)
    unknown = sorted(set(source) - _TOP_LEVEL_FIELDS)
    _require(
        not unknown,
        "E-EVIDENCE-REGISTRY-FIELD",
        f"unsupported registry fields: {unknown}",
    )
    _require(
        source.get("contract") == REGISTRY_CONTRACT,
        "E-EVIDENCE-REGISTRY-CONTRACT",
        f"expected {REGISTRY_CONTRACT!r}",
    )
    _require(
        source.get("live") is False,
        "E-EVIDENCE-REGISTRY-LIVE",
        "registry must remain offline with live=false",
    )
    _require(
        source.get("status_inheritance") == "prohibited",
        "E-EVIDENCE-REGISTRY-STATUS",
        "status_inheritance must be 'prohibited'",
    )
    entries = source.get("entries")
    _require(
        isinstance(entries, list) and bool(entries),
        "E-EVIDENCE-REGISTRY-ENTRIES",
        "entries must be a non-empty list",
    )

    normalized: list[dict[str, Any]] = []
    route_ids: set[str] = set()
    snapshot_paths: set[str] = set()
    for index, entry in enumerate(entries):
        _require(
            isinstance(entry, Mapping),
            "E-EVIDENCE-REGISTRY-ENTRY",
            f"entries[{index}] must be an object",
        )
        item = dict(entry)
        unknown_entry = sorted(set(item) - _ENTRY_FIELDS)
        _require(
            not unknown_entry,
            "E-EVIDENCE-REGISTRY-ENTRY-FIELD",
            f"entries[{index}] has unsupported fields: {unknown_entry}",
        )
        route_id = item.get("route_id")
        _require(
            isinstance(route_id, str) and bool(_ROUTE_ID.fullmatch(route_id)),
            "E-EVIDENCE-REGISTRY-ROUTE",
            f"entries[{index}] route_id must be canonical kebab-case",
        )
        _require(
            route_id not in route_ids,
            "E-EVIDENCE-REGISTRY-DUPLICATE-ROUTE",
            f"duplicate active baseline for route {route_id!r}",
        )
        route_ids.add(route_id)

        snapshot_path = item.get("snapshot_path")
        path_parts = Path(snapshot_path).parts if isinstance(snapshot_path, str) else ()
        _require(
            isinstance(snapshot_path, str)
            and snapshot_path.startswith("content/fixtures/phase2_bridge/")
            and snapshot_path.endswith(".json")
            and ".." not in path_parts
            and not Path(snapshot_path).is_absolute(),
            "E-EVIDENCE-REGISTRY-PATH",
            f"entries[{index}] snapshot_path must be a safe phase2_bridge JSON path",
        )
        _require(
            snapshot_path not in snapshot_paths,
            "E-EVIDENCE-REGISTRY-DUPLICATE-PATH",
            f"duplicate snapshot_path {snapshot_path!r}",
        )
        snapshot_paths.add(snapshot_path)
        _require(
            item.get("state") == REGISTRY_STATE,
            "E-EVIDENCE-REGISTRY-STATE",
            f"entries[{index}] state must be {REGISTRY_STATE!r}",
        )
        _require(
            isinstance(item.get("registration_basis"), str)
            and bool(item["registration_basis"].strip()),
            "E-EVIDENCE-REGISTRY-BASIS",
            f"entries[{index}] registration_basis must be non-empty text",
        )
        commit = item.get("registration_commit")
        _require(
            isinstance(commit, str) and bool(_HEX_40.fullmatch(commit)),
            "E-EVIDENCE-REGISTRY-COMMIT",
            f"entries[{index}] registration_commit must be a lowercase Git SHA",
        )
        normalized.append(item)

    source["entries"] = sorted(normalized, key=lambda item: item["route_id"])
    return source


def _load_snapshot(
    repository_root: Path,
    relative_path: str,
) -> tuple[dict[str, Any], bytes]:
    root = repository_root.resolve()
    path = (root / relative_path).resolve()
    _require(
        path.is_relative_to(root),
        "E-EVIDENCE-REGISTRY-PATH-ESCAPE",
        f"snapshot path escapes repository root: {relative_path}",
    )
    _require(
        path.is_file(),
        "E-EVIDENCE-REGISTRY-SNAPSHOT-MISSING",
        f"registered snapshot is unavailable: {relative_path}",
    )
    try:
        raw = path.read_bytes()
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise KernelError(
            "E-EVIDENCE-REGISTRY-SNAPSHOT-READ",
            f"cannot read registered snapshot {relative_path}: {exc}",
        ) from exc
    _require(
        isinstance(payload, Mapping),
        "E-EVIDENCE-REGISTRY-SNAPSHOT",
        f"registered snapshot must be an object: {relative_path}",
    )
    return dict(payload), raw


def compile_evidence_registry(
    payload: Mapping[str, Any],
    repository: Any,
    review_index: Mapping[str, Mapping[str, Any]],
    repository_root: Path,
) -> dict[str, Any]:
    """Compile every registered route baseline into one deterministic catalog."""
    registry = validate_evidence_registry(payload)
    entries: list[dict[str, Any]] = []
    for registration in registry["entries"]:
        snapshot, raw = _load_snapshot(
            repository_root,
            registration["snapshot_path"],
        )
        snapshot = validate_reference_snapshot(snapshot)
        _require(
            snapshot["route_id"] == registration["route_id"],
            "E-EVIDENCE-REGISTRY-ROUTE-MISMATCH",
            (
                f"registry route {registration['route_id']!r} does not match "
                f"snapshot route {snapshot['route_id']!r}"
            ),
        )
        manifest = build_review_aware_manifest(
            snapshot,
            repository,
            review_index,
        )
        manifest_bytes = render_json(manifest).encode("utf-8")
        if manifest["blocked_count"]:
            health = "blocked"
        elif manifest["revalidate_count"]:
            health = "revalidation-required"
        else:
            health = "verified"
        entries.append(
            {
                "route_id": registration["route_id"],
                "snapshot_path": registration["snapshot_path"],
                "state": registration["state"],
                "registration_basis": registration["registration_basis"],
                "registration_commit": registration["registration_commit"],
                "snapshot_sha256": hashlib.sha256(raw).hexdigest(),
                "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
                "source": manifest["source"],
                "reference_count": manifest["reference_count"],
                "resolved_count": manifest["resolved_count"],
                "review_record_count": manifest.get("review_record_count", 0),
                "revalidate_count": manifest["revalidate_count"],
                "blocked_count": manifest["blocked_count"],
                "manifest_decision": manifest["decision"],
                "health": health,
            }
        )

    entries.sort(key=lambda item: item["route_id"])
    blocked_count = sum(item["health"] == "blocked" for item in entries)
    revalidate_count = sum(
        item["health"] == "revalidation-required" for item in entries
    )
    verified_count = sum(item["health"] == "verified" for item in entries)
    if blocked_count:
        decision = "registry-blocked"
    elif revalidate_count:
        decision = "registry-revalidation-required"
    else:
        decision = "registry-verified"
    return {
        "contract": REGISTRY_CATALOG_CONTRACT,
        "registry_contract": REGISTRY_CONTRACT,
        "route_count": len(entries),
        "route_ids": [item["route_id"] for item in entries],
        "verified_count": verified_count,
        "revalidation_required_count": revalidate_count,
        "blocked_count": blocked_count,
        "entries": entries,
        "decision": decision,
        "live": False,
        "status_inheritance": "prohibited",
        "automatic_snapshot_acceptance": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }
