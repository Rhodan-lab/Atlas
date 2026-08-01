"""Automatically preflight Atlas runtime changes against accepted Principia routes."""
from __future__ import annotations

import hashlib
from typing import Any, Mapping

from .evidence_impact import IMPACT_INDEX_CONTRACT
from .kernel import KernelError, render_json
from .repository import KernelRepository

PREFLIGHT_CONTRACT = "atlas-principia-evidence-runtime-preflight/0.1"
_STATE_RANK = {"stable": 0, "revalidation-required": 1, "blocked": 2}


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _digest(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(render_json(dict(payload)).encode("utf-8")).hexdigest()


def _max_state(*states: str) -> str:
    return max(states, key=lambda value: _STATE_RANK[value])


def _runtime_entities(runtime: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(entity["key"]): entity
        for entity in runtime.get("entities", [])
        if isinstance(entity, Mapping) and isinstance(entity.get("key"), str)
    }


def _metadata_value(entity: Mapping[str, Any], field: str) -> Any:
    if field in entity:
        return entity.get(field)
    metadata = entity.get("metadata")
    return metadata.get(field) if isinstance(metadata, Mapping) else None


def _route_baselines(index: Mapping[str, Any]) -> dict[str, str]:
    routes = index.get("routes")
    _require(
        isinstance(routes, list),
        "E-EVIDENCE-PREFLIGHT-ROUTES",
        "impact index routes must be a list",
    )
    result: dict[str, str] = {}
    for position, route in enumerate(routes):
        _require(
            isinstance(route, Mapping),
            "E-EVIDENCE-PREFLIGHT-ROUTE",
            f"routes[{position}] must be an object",
        )
        route_id = route.get("route_id")
        state = route.get("impact_state")
        _require(
            isinstance(route_id, str) and route_id,
            "E-EVIDENCE-PREFLIGHT-ROUTE",
            f"routes[{position}] route_id must be non-empty text",
        )
        _require(
            state in _STATE_RANK,
            "E-EVIDENCE-PREFLIGHT-STATE",
            f"routes[{position}] has an invalid impact state",
        )
        _require(
            route_id not in result,
            "E-EVIDENCE-PREFLIGHT-DUPLICATE-ROUTE",
            f"duplicate route {route_id!r} in impact index",
        )
        result[route_id] = str(state)
    return result


def analyze_evidence_runtime_preflight(
    impact_index: Mapping[str, Any],
    baseline_runtime: Mapping[str, Any],
    candidate_runtime: Mapping[str, Any],
) -> dict[str, Any]:
    """Compare valid runtimes and map accepted evidence changes to Principia routes."""
    _require(
        isinstance(impact_index, Mapping)
        and impact_index.get("contract") == IMPACT_INDEX_CONTRACT,
        "E-EVIDENCE-PREFLIGHT-INDEX-CONTRACT",
        f"expected {IMPACT_INDEX_CONTRACT!r}",
    )
    baseline_validation = KernelRepository(baseline_runtime).validation_report
    candidate_validation = KernelRepository(candidate_runtime).validation_report
    baseline_entities = _runtime_entities(baseline_runtime)
    candidate_entities = _runtime_entities(candidate_runtime)
    baseline_revisions = baseline_runtime.get("revisions_by_id", {})
    candidate_revisions = candidate_runtime.get("revisions_by_id", {})
    route_states = _route_baselines(impact_index)
    baseline_route_states = dict(route_states)

    exact_references = impact_index.get("exact_references")
    _require(
        isinstance(exact_references, list),
        "E-EVIDENCE-PREFLIGHT-EXACT",
        "impact index exact_references must be a list",
    )

    exact_results: list[dict[str, Any]] = []
    immutable_violation_count = 0
    removed_exact_reference_count = 0
    superseding_revision_count = 0
    lifecycle_change_count = 0

    for position, exact in enumerate(exact_references):
        _require(
            isinstance(exact, Mapping),
            "E-EVIDENCE-PREFLIGHT-EXACT",
            f"exact_references[{position}] must be an object",
        )
        key = exact.get("key")
        entity_id = exact.get("entity_id")
        revision = exact.get("revision")
        route_ids = exact.get("route_ids")
        baseline_state = exact.get("impact_state")
        _require(
            isinstance(key, str)
            and isinstance(entity_id, str)
            and isinstance(revision, int)
            and not isinstance(revision, bool)
            and revision > 0,
            "E-EVIDENCE-PREFLIGHT-EXACT",
            f"exact_references[{position}] has invalid identity",
        )
        _require(
            key == f"{entity_id}@{revision}",
            "E-EVIDENCE-PREFLIGHT-EXACT-KEY",
            f"exact reference key does not match identity: {key}",
        )
        _require(
            isinstance(route_ids, list)
            and all(
                isinstance(route_id, str) and route_id in route_states
                for route_id in route_ids
            ),
            "E-EVIDENCE-PREFLIGHT-DEPENDENCY",
            f"{key} has invalid route dependencies",
        )
        _require(
            baseline_state in _STATE_RANK,
            "E-EVIDENCE-PREFLIGHT-STATE",
            f"{key} has an invalid baseline impact state",
        )
        baseline_entity = baseline_entities.get(key)
        _require(
            baseline_entity is not None,
            "E-EVIDENCE-PREFLIGHT-BASELINE-MISSING",
            f"accepted exact reference is unavailable in baseline runtime: {key}",
        )

        candidate_entity = candidate_entities.get(key)
        finding_codes: list[str] = []
        immutable_fields: list[str] = []
        projected_state = str(baseline_state)
        from_status = _metadata_value(baseline_entity, "status")
        to_status = (
            _metadata_value(candidate_entity, "status")
            if candidate_entity is not None
            else None
        )
        from_staleness = _metadata_value(baseline_entity, "staleness")
        to_staleness = (
            _metadata_value(candidate_entity, "staleness")
            if candidate_entity is not None
            else None
        )

        if candidate_entity is None:
            finding_codes.append("exact-revision-removed")
            removed_exact_reference_count += 1
            projected_state = "blocked"
        else:
            for field in ("path", "source_sha256", "body_sha256"):
                if baseline_entity.get(field) != candidate_entity.get(field):
                    immutable_fields.append(field)
            if immutable_fields:
                finding_codes.append("immutable-exact-revision-changed")
                immutable_violation_count += 1
                projected_state = "blocked"

            if from_status != to_status:
                lifecycle_change_count += 1
                if to_status == "retracted":
                    finding_codes.append("lifecycle-retracted")
                    projected_state = "blocked"
                elif to_status == "deprecated":
                    finding_codes.append("lifecycle-deprecated")
                    projected_state = _max_state(
                        projected_state, "revalidation-required"
                    )
                else:
                    finding_codes.append("lifecycle-status-changed")
                    projected_state = _max_state(
                        projected_state, "revalidation-required"
                    )

            if from_staleness != to_staleness:
                lifecycle_change_count += 1
                if to_staleness in {"review-required", "confirmed-stale"}:
                    finding_codes.append(f"staleness-{to_staleness}")
                    projected_state = _max_state(
                        projected_state, "revalidation-required"
                    )
                else:
                    finding_codes.append("staleness-changed")
                    projected_state = _max_state(
                        projected_state, "revalidation-required"
                    )

        before_revisions = sorted(
            int(value)
            for value in (
                baseline_revisions.get(entity_id, [])
                if isinstance(baseline_revisions, Mapping)
                else []
            )
        )
        after_revisions = sorted(
            int(value)
            for value in (
                candidate_revisions.get(entity_id, [])
                if isinstance(candidate_revisions, Mapping)
                else []
            )
        )
        new_higher_revisions = sorted(
            value
            for value in after_revisions
            if value > revision and value not in before_revisions
        )
        if new_higher_revisions:
            finding_codes.append("superseding-revision-added")
            superseding_revision_count += len(new_higher_revisions)
            projected_state = _max_state(projected_state, "revalidation-required")

        finding_codes = sorted(set(finding_codes))
        changed = bool(finding_codes)
        for route_id in route_ids:
            route_states[route_id] = _max_state(
                route_states[route_id], projected_state
            )
        unique_route_ids = sorted(set(route_ids))
        exact_results.append(
            {
                "key": key,
                "entity_id": entity_id,
                "revision": revision,
                "route_ids": unique_route_ids,
                "route_count": len(unique_route_ids),
                "baseline_impact_state": baseline_state,
                "projected_impact_state": projected_state,
                "changed": changed,
                "finding_codes": finding_codes,
                "immutable_changed_fields": immutable_fields,
                "baseline_status": from_status,
                "candidate_status": to_status,
                "baseline_staleness": from_staleness,
                "candidate_staleness": to_staleness,
                "baseline_revisions": before_revisions,
                "candidate_revisions": after_revisions,
                "new_higher_revisions": new_higher_revisions,
            }
        )

    exact_results.sort(key=lambda item: (item["entity_id"], item["revision"]))
    routes: list[dict[str, Any]] = []
    newly_affected_route_ids: list[str] = []
    escalated_route_ids: list[str] = []
    newly_blocked_route_ids: list[str] = []
    for route_id in sorted(route_states):
        baseline_state = baseline_route_states[route_id]
        projected_state = route_states[route_id]
        if baseline_state == "stable" and projected_state != "stable":
            newly_affected_route_ids.append(route_id)
        if _STATE_RANK[projected_state] > _STATE_RANK[baseline_state]:
            escalated_route_ids.append(route_id)
        if baseline_state != "blocked" and projected_state == "blocked":
            newly_blocked_route_ids.append(route_id)
        routes.append(
            {
                "route_id": route_id,
                "baseline_impact_state": baseline_state,
                "projected_impact_state": projected_state,
                "changed": baseline_state != projected_state,
            }
        )

    changed_results = [item for item in exact_results if item["changed"]]
    blocked_changes = any(
        item["projected_impact_state"] == "blocked"
        and (
            item["baseline_impact_state"] != "blocked"
            or item["changed"]
        )
        for item in changed_results
    )
    revalidation_changes = any(
        item["projected_impact_state"] == "revalidation-required"
        and item["changed"]
        for item in changed_results
    )
    if blocked_changes:
        decision = "preflight-blocked"
    elif revalidation_changes:
        decision = "preflight-revalidation-required"
    else:
        decision = "preflight-clear"

    baseline_digest = _digest(baseline_runtime)
    candidate_digest = _digest(candidate_runtime)
    return {
        "contract": PREFLIGHT_CONTRACT,
        "source_impact_index_contract": IMPACT_INDEX_CONTRACT,
        "baseline_runtime": {
            "contract": baseline_runtime.get("contract"),
            "source_digest": baseline_runtime.get("source_digest"),
            "runtime_sha256": baseline_digest,
            "entity_count": baseline_validation["entity_count"],
        },
        "candidate_runtime": {
            "contract": candidate_runtime.get("contract"),
            "source_digest": candidate_runtime.get("source_digest"),
            "runtime_sha256": candidate_digest,
            "entity_count": candidate_validation["entity_count"],
        },
        "runtime_changed": baseline_digest != candidate_digest,
        "accepted_exact_reference_count": len(exact_results),
        "changed_accepted_exact_reference_count": len(changed_results),
        "immutable_violation_count": immutable_violation_count,
        "removed_exact_reference_count": removed_exact_reference_count,
        "superseding_revision_count": superseding_revision_count,
        "lifecycle_change_count": lifecycle_change_count,
        "baseline_affected_route_count": sum(
            state != "stable" for state in baseline_route_states.values()
        ),
        "projected_affected_route_count": sum(
            state != "stable" for state in route_states.values()
        ),
        "newly_affected_route_count": len(newly_affected_route_ids),
        "newly_affected_route_ids": newly_affected_route_ids,
        "escalated_route_count": len(escalated_route_ids),
        "escalated_route_ids": escalated_route_ids,
        "newly_blocked_route_count": len(newly_blocked_route_ids),
        "newly_blocked_route_ids": newly_blocked_route_ids,
        "routes": routes,
        "exact_references": exact_results,
        "decision": decision,
        "live": False,
        "status_inheritance": "prohibited",
        "automatic_snapshot_acceptance": False,
        "automatic_registry_update": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "canonical_mutation": False,
        "repository_mutation": False,
        "principia_publication_status_granted": False,
        "learner_effectiveness_claimed": False,
    }
