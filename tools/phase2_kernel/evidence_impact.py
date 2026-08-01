"""Build a deterministic reverse index from Atlas evidence to Principia routes."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .evidence_bridge import validate_reference_snapshot
from .evidence_registry import validate_evidence_registry
from .evidence_review import build_review_aware_manifest
from .kernel import ENTITY_ID_RE, KernelError, render_json

IMPACT_INDEX_CONTRACT = "atlas-principia-evidence-impact-index/0.1"
IMPACT_QUERY_CONTRACT = "atlas-principia-evidence-impact-query/0.1"
_STATE_RANK = {"stable": 0, "revalidation-required": 1, "blocked": 2}


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _load_snapshot(
    repository_root: Path,
    relative_path: str,
) -> tuple[dict[str, Any], bytes]:
    root = repository_root.resolve()
    path = (root / relative_path).resolve()
    _require(
        path.is_relative_to(root),
        "E-EVIDENCE-IMPACT-PATH-ESCAPE",
        f"snapshot path escapes repository root: {relative_path}",
    )
    _require(
        path.is_file(),
        "E-EVIDENCE-IMPACT-SNAPSHOT-MISSING",
        f"registered snapshot is unavailable: {relative_path}",
    )
    try:
        raw = path.read_bytes()
        payload = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise KernelError(
            "E-EVIDENCE-IMPACT-SNAPSHOT-READ",
            f"cannot read registered snapshot {relative_path}: {exc}",
        ) from exc
    _require(
        isinstance(payload, Mapping),
        "E-EVIDENCE-IMPACT-SNAPSHOT",
        f"registered snapshot must be an object: {relative_path}",
    )
    return dict(payload), raw


def _state_from_action(action: Any) -> str:
    if action == "block-release":
        return "blocked"
    if action == "revalidate":
        return "revalidation-required"
    return "stable"


def _max_state(states: list[str]) -> str:
    return max(states, key=lambda value: _STATE_RANK[value]) if states else "stable"


def _digest(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(render_json(dict(payload)).encode("utf-8")).hexdigest()


def compile_evidence_impact_index(
    registry_payload: Mapping[str, Any],
    repository: Any,
    review_index: Mapping[str, Mapping[str, Any]],
    repository_root: Path,
) -> dict[str, Any]:
    """Compile reverse dependencies from accepted route snapshots to Atlas revisions."""
    registry = validate_evidence_registry(registry_payload)
    exact_map: dict[str, dict[str, Any]] = {}
    routes: list[dict[str, Any]] = []

    for registration in registry["entries"]:
        snapshot_payload, raw = _load_snapshot(
            repository_root,
            registration["snapshot_path"],
        )
        snapshot = validate_reference_snapshot(snapshot_payload)
        _require(
            snapshot["route_id"] == registration["route_id"],
            "E-EVIDENCE-IMPACT-ROUTE-MISMATCH",
            (
                f"registry route {registration['route_id']!r} does not match "
                f"snapshot route {snapshot['route_id']!r}"
            ),
        )
        manifest = build_review_aware_manifest(snapshot, repository, review_index)
        manifest_entries = {
            str(entry["key"]): dict(entry) for entry in manifest["entries"]
        }
        _require(
            len(manifest_entries) == len(manifest["entries"]),
            "E-EVIDENCE-IMPACT-MANIFEST-DUPLICATE",
            "candidate manifest contains duplicate exact keys",
        )
        manifest_sha256 = _digest(manifest)
        snapshot_sha256 = hashlib.sha256(raw).hexdigest()
        if manifest["blocked_count"]:
            route_state = "blocked"
        elif manifest["revalidate_count"]:
            route_state = "revalidation-required"
        else:
            route_state = "stable"

        exact_keys: list[str] = []
        for reference in sorted(
            snapshot["references"],
            key=lambda item: (item["entity_id"], item["revision"]),
        ):
            key = f"{reference['entity_id']}@{reference['revision']}"
            _require(
                key in manifest_entries,
                "E-EVIDENCE-IMPACT-MANIFEST-MISSING",
                f"manifest is missing exact reference {key}",
            )
            authority = manifest_entries[key]
            try:
                revisions = repository.available_revisions(reference["entity_id"])
            except KernelError:
                revisions = []
            exact = exact_map.setdefault(
                key,
                {
                    "key": key,
                    "entity_id": reference["entity_id"],
                    "revision": reference["revision"],
                    "entity_type": authority.get("entity_type"),
                    "title": authority.get("title"),
                    "canonical_path": authority.get("canonical_path"),
                    "canonical_source_sha256": authority.get(
                        "canonical_source_sha256"
                    ),
                    "canonical_body_sha256": authority.get(
                        "canonical_body_sha256"
                    ),
                    "available_revisions": sorted(int(value) for value in revisions),
                    "latest_revision": max(revisions) if revisions else None,
                    "dependencies": [],
                },
            )
            dependency = {
                "route_id": registration["route_id"],
                "snapshot_path": registration["snapshot_path"],
                "snapshot_sha256": snapshot_sha256,
                "route_manifest_sha256": manifest_sha256,
                "purpose": reference["purpose"],
                "declared_review_level": reference.get("declared_review_level"),
                "declared_human_verified": reference.get(
                    "declared_human_verified"
                ),
                "resolution": authority.get("resolution"),
                "required_action": authority.get("required_action"),
                "impact_state": _state_from_action(
                    authority.get("required_action")
                ),
                "review_comparison": authority.get("review_comparison"),
                "review_record_id": (
                    authority.get("review_authority", {}).get("record_id")
                    if isinstance(authority.get("review_authority"), Mapping)
                    else None
                ),
            }
            exact["dependencies"].append(dependency)
            exact_keys.append(key)

        routes.append(
            {
                "route_id": registration["route_id"],
                "snapshot_path": registration["snapshot_path"],
                "registration_basis": registration["registration_basis"],
                "registration_commit": registration["registration_commit"],
                "snapshot_sha256": snapshot_sha256,
                "manifest_sha256": manifest_sha256,
                "reference_count": manifest["reference_count"],
                "resolved_count": manifest["resolved_count"],
                "review_record_count": manifest.get("review_record_count", 0),
                "revalidate_count": manifest["revalidate_count"],
                "blocked_count": manifest["blocked_count"],
                "impact_state": route_state,
                "exact_keys": sorted(exact_keys),
            }
        )

    exact_references: list[dict[str, Any]] = []
    for key in sorted(exact_map):
        item = exact_map[key]
        item["dependencies"].sort(
            key=lambda dependency: (
                dependency["route_id"],
                dependency["snapshot_path"],
                dependency["purpose"],
            )
        )
        route_ids = sorted(
            {dependency["route_id"] for dependency in item["dependencies"]}
        )
        states = [
            dependency["impact_state"] for dependency in item["dependencies"]
        ]
        item["route_ids"] = route_ids
        item["route_count"] = len(route_ids)
        item["dependency_count"] = len(item["dependencies"])
        item["impact_state"] = _max_state(states)
        item["superseded"] = (
            item["latest_revision"] is not None
            and int(item["latest_revision"]) > int(item["revision"])
        )
        exact_references.append(item)

    entity_map: dict[str, dict[str, Any]] = {}
    for item in exact_references:
        entity = entity_map.setdefault(
            item["entity_id"],
            {
                "entity_id": item["entity_id"],
                "entity_type": item.get("entity_type"),
                "title": item.get("title"),
                "exact_keys": [],
                "revisions": [],
                "route_ids": set(),
                "states": [],
            },
        )
        entity["exact_keys"].append(item["key"])
        entity["revisions"].append(item["revision"])
        entity["route_ids"].update(item["route_ids"])
        entity["states"].append(item["impact_state"])

    entities: list[dict[str, Any]] = []
    for entity_id in sorted(entity_map):
        source = entity_map[entity_id]
        route_ids = sorted(source["route_ids"])
        entities.append(
            {
                "entity_id": entity_id,
                "entity_type": source["entity_type"],
                "title": source["title"],
                "exact_reference_count": len(source["exact_keys"]),
                "exact_keys": sorted(source["exact_keys"]),
                "revisions": sorted(source["revisions"]),
                "route_count": len(route_ids),
                "route_ids": route_ids,
                "impact_state": _max_state(source["states"]),
            }
        )

    routes.sort(key=lambda item: item["route_id"])
    affected_route_ids = sorted(
        route["route_id"]
        for route in routes
        if route["impact_state"] != "stable"
    )
    stable_count = sum(
        item["impact_state"] == "stable" for item in exact_references
    )
    revalidation_count = sum(
        item["impact_state"] == "revalidation-required"
        for item in exact_references
    )
    blocked_count = sum(
        item["impact_state"] == "blocked" for item in exact_references
    )
    if blocked_count:
        decision = "impact-index-blocked"
    elif revalidation_count:
        decision = "impact-index-revalidation-required"
    else:
        decision = "impact-index-clear"

    return {
        "contract": IMPACT_INDEX_CONTRACT,
        "registry_contract": registry["contract"],
        "registry_sha256": _digest(registry),
        "route_count": len(routes),
        "entity_count": len(entities),
        "exact_reference_count": len(exact_references),
        "dependency_count": sum(
            item["dependency_count"] for item in exact_references
        ),
        "stable_exact_reference_count": stable_count,
        "revalidation_required_exact_reference_count": revalidation_count,
        "blocked_exact_reference_count": blocked_count,
        "affected_route_count": len(affected_route_ids),
        "affected_route_ids": affected_route_ids,
        "routes": routes,
        "entities": entities,
        "exact_references": exact_references,
        "decision": decision,
        "live": False,
        "status_inheritance": "prohibited",
        "automatic_snapshot_acceptance": False,
        "automatic_registry_update": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }


def query_evidence_impact(
    index: Mapping[str, Any],
    entity_id: str,
    revision: int | None = None,
) -> dict[str, Any]:
    """Return the accepted Principia route impact for one Atlas entity or revision."""
    _require(
        index.get("contract") == IMPACT_INDEX_CONTRACT,
        "E-EVIDENCE-IMPACT-QUERY-CONTRACT",
        f"expected {IMPACT_INDEX_CONTRACT!r}",
    )
    _require(
        isinstance(entity_id, str) and bool(ENTITY_ID_RE.fullmatch(entity_id)),
        "E-EVIDENCE-IMPACT-QUERY-ENTITY",
        "entity_id must be a canonical Atlas entity ID",
    )
    if revision is not None:
        _require(
            isinstance(revision, int)
            and not isinstance(revision, bool)
            and revision > 0,
            "E-EVIDENCE-IMPACT-QUERY-REVISION",
            "revision must be a positive integer",
        )
        key = f"{entity_id}@{revision}"
        results = [
            dict(item)
            for item in index.get("exact_references", [])
            if item.get("key") == key
        ]
    else:
        results = [
            dict(item)
            for item in index.get("exact_references", [])
            if item.get("entity_id") == entity_id
        ]
    _require(
        bool(results),
        "E-EVIDENCE-IMPACT-QUERY-MISSING",
        (
            f"no accepted Principia route depends on {entity_id}@{revision}"
            if revision is not None
            else f"no accepted Principia route depends on {entity_id}"
        ),
    )
    route_ids = sorted(
        {
            route_id
            for item in results
            for route_id in item.get("route_ids", [])
        }
    )
    return {
        "contract": IMPACT_QUERY_CONTRACT,
        "source_index_contract": IMPACT_INDEX_CONTRACT,
        "query": {"entity_id": entity_id, "revision": revision},
        "match_count": len(results),
        "route_count": len(route_ids),
        "route_ids": route_ids,
        "impact_state": _max_state(
            [str(item.get("impact_state", "stable")) for item in results]
        ),
        "results": results,
        "live": False,
        "repository_mutation": False,
    }
