"""Simulate proposed Atlas evidence changes against accepted Principia routes."""
from __future__ import annotations

import copy
import hashlib
from typing import Any, Mapping

from .evidence_impact import IMPACT_INDEX_CONTRACT
from .kernel import ENTITY_ID_RE, KernelError, render_json

SCENARIO_CONTRACT = "atlas-principia-evidence-impact-scenario/0.1"
SIMULATION_CONTRACT = "atlas-principia-evidence-impact-simulation/0.1"
_ALLOWED_OPERATIONS = {
    "supersede",
    "mark-review-required",
    "mark-confirmed-stale",
    "deprecate",
    "retract",
}
_STATE_RANK = {"stable": 0, "revalidation-required": 1, "blocked": 2}
_TOP_LEVEL_FIELDS = {"contract", "live", "status_inheritance", "changes"}
_CHANGE_FIELDS = {"entity_id", "revision", "operation", "reason", "new_revision"}


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _digest(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(render_json(dict(payload)).encode("utf-8")).hexdigest()


def _max_state(states: list[str]) -> str:
    return max(states, key=lambda value: _STATE_RANK[value]) if states else "stable"


def validate_evidence_impact_scenario(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Validate a read-only proposed evidence-change scenario."""
    _require(
        isinstance(payload, Mapping),
        "E-EVIDENCE-SIMULATION-SCENARIO",
        "scenario must be an object",
    )
    source = dict(payload)
    unknown = sorted(set(source) - _TOP_LEVEL_FIELDS)
    _require(
        not unknown,
        "E-EVIDENCE-SIMULATION-SCENARIO-FIELD",
        f"unsupported scenario fields: {unknown}",
    )
    _require(
        source.get("contract") == SCENARIO_CONTRACT,
        "E-EVIDENCE-SIMULATION-SCENARIO-CONTRACT",
        f"expected {SCENARIO_CONTRACT!r}",
    )
    _require(
        source.get("live") is False,
        "E-EVIDENCE-SIMULATION-LIVE",
        "scenario must remain offline with live=false",
    )
    _require(
        source.get("status_inheritance") == "prohibited",
        "E-EVIDENCE-SIMULATION-STATUS",
        "status_inheritance must be 'prohibited'",
    )
    changes = source.get("changes")
    _require(
        isinstance(changes, list),
        "E-EVIDENCE-SIMULATION-CHANGES",
        "changes must be a list",
    )

    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for index, change in enumerate(changes):
        _require(
            isinstance(change, Mapping),
            "E-EVIDENCE-SIMULATION-CHANGE",
            f"changes[{index}] must be an object",
        )
        item = dict(change)
        unknown_change = sorted(set(item) - _CHANGE_FIELDS)
        _require(
            not unknown_change,
            "E-EVIDENCE-SIMULATION-CHANGE-FIELD",
            f"changes[{index}] has unsupported fields: {unknown_change}",
        )
        entity_id = item.get("entity_id")
        revision = item.get("revision")
        operation = item.get("operation")
        _require(
            isinstance(entity_id, str) and bool(ENTITY_ID_RE.fullmatch(entity_id)),
            "E-EVIDENCE-SIMULATION-ENTITY",
            f"changes[{index}] has an invalid Atlas entity ID",
        )
        _require(
            isinstance(revision, int)
            and not isinstance(revision, bool)
            and revision > 0,
            "E-EVIDENCE-SIMULATION-REVISION",
            f"changes[{index}] revision must be a positive integer",
        )
        _require(
            operation in _ALLOWED_OPERATIONS,
            "E-EVIDENCE-SIMULATION-OPERATION",
            f"changes[{index}] operation is unsupported: {operation!r}",
        )
        _require(
            isinstance(item.get("reason"), str) and bool(item["reason"].strip()),
            "E-EVIDENCE-SIMULATION-REASON",
            f"changes[{index}] reason must be non-empty text",
        )
        target = (entity_id, revision)
        _require(
            target not in seen,
            "E-EVIDENCE-SIMULATION-DUPLICATE",
            f"duplicate simulated target {entity_id}@{revision}",
        )
        seen.add(target)

        new_revision = item.get("new_revision")
        if operation == "supersede":
            _require(
                isinstance(new_revision, int)
                and not isinstance(new_revision, bool)
                and new_revision > revision,
                "E-EVIDENCE-SIMULATION-NEW-REVISION",
                (
                    f"changes[{index}] supersede requires new_revision "
                    "greater than revision"
                ),
            )
        else:
            _require(
                "new_revision" not in item,
                "E-EVIDENCE-SIMULATION-NEW-REVISION",
                f"changes[{index}] new_revision is only valid for supersede",
            )
        normalized.append(item)

    normalized.sort(key=lambda item: (item["entity_id"], item["revision"]))
    source["changes"] = normalized
    return source


def _operation_effect(change: Mapping[str, Any]) -> tuple[str, str, str]:
    operation = change["operation"]
    if operation == "supersede":
        return "superseded", "revalidate", "revalidation-required"
    if operation == "mark-review-required":
        return "review-required", "revalidate", "revalidation-required"
    if operation == "mark-confirmed-stale":
        return "confirmed-stale", "revalidate", "revalidation-required"
    if operation == "deprecate":
        return "deprecated", "revalidate", "revalidation-required"
    return "retracted", "block-release", "blocked"


def simulate_evidence_impact(
    index_payload: Mapping[str, Any],
    scenario_payload: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply a scenario to an impact index without mutating Atlas or the registry."""
    _require(
        isinstance(index_payload, Mapping)
        and index_payload.get("contract") == IMPACT_INDEX_CONTRACT,
        "E-EVIDENCE-SIMULATION-INDEX-CONTRACT",
        f"expected {IMPACT_INDEX_CONTRACT!r}",
    )
    scenario = validate_evidence_impact_scenario(scenario_payload)
    simulated = copy.deepcopy(dict(index_payload))

    exact_references = simulated.get("exact_references")
    routes = simulated.get("routes")
    entities = simulated.get("entities")
    _require(
        isinstance(exact_references, list)
        and isinstance(routes, list)
        and isinstance(entities, list),
        "E-EVIDENCE-SIMULATION-INDEX",
        "impact index must contain exact_references, routes, and entities lists",
    )

    exact_map: dict[str, dict[str, Any]] = {}
    for item in exact_references:
        _require(
            isinstance(item, Mapping) and isinstance(item.get("key"), str),
            "E-EVIDENCE-SIMULATION-INDEX-EXACT",
            "every exact reference must contain a string key",
        )
        key = str(item["key"])
        _require(
            key not in exact_map,
            "E-EVIDENCE-SIMULATION-INDEX-DUPLICATE",
            f"duplicate exact reference in impact index: {key}",
        )
        exact_map[key] = item

    applied_changes: list[dict[str, Any]] = []
    changed_keys: set[str] = set()
    for change in scenario["changes"]:
        key = f"{change['entity_id']}@{change['revision']}"
        _require(
            key in exact_map,
            "E-EVIDENCE-SIMULATION-TARGET-MISSING",
            f"no accepted Principia route depends on simulated target {key}",
        )
        exact = exact_map[key]
        before_state = str(exact.get("impact_state", "stable"))
        resolution, action, proposed_state = _operation_effect(change)
        final_state = _max_state([before_state, proposed_state])

        dependencies = exact.get("dependencies")
        _require(
            isinstance(dependencies, list) and bool(dependencies),
            "E-EVIDENCE-SIMULATION-DEPENDENCIES",
            f"exact reference {key} must contain dependencies",
        )
        for dependency in dependencies:
            _require(
                isinstance(dependency, dict),
                "E-EVIDENCE-SIMULATION-DEPENDENCY",
                f"exact reference {key} contains a malformed dependency",
            )
            dependency_before = str(dependency.get("impact_state", "stable"))
            dependency["baseline_resolution"] = dependency.get("resolution")
            dependency["baseline_required_action"] = dependency.get(
                "required_action"
            )
            dependency["baseline_impact_state"] = dependency_before
            if _STATE_RANK[proposed_state] >= _STATE_RANK[dependency_before]:
                dependency["resolution"] = resolution
                dependency["required_action"] = action
                dependency["impact_state"] = proposed_state
            dependency["simulated_operation"] = change["operation"]
            dependency["simulated_reason"] = change["reason"]

        exact["baseline_impact_state"] = before_state
        exact["impact_state"] = final_state
        exact["simulated_operation"] = change["operation"]
        exact["simulated_reason"] = change["reason"]
        if change["operation"] == "supersede":
            new_revision = int(change["new_revision"])
            available = {
                int(value) for value in exact.get("available_revisions", [])
            }
            available.add(new_revision)
            exact["available_revisions"] = sorted(available)
            exact["latest_revision"] = max(available)
            exact["superseded"] = True
            exact["simulated_new_revision"] = new_revision

        route_ids = sorted(
            {
                str(dependency.get("route_id"))
                for dependency in dependencies
                if isinstance(dependency.get("route_id"), str)
            }
        )
        applied_changes.append(
            {
                "key": key,
                "entity_id": change["entity_id"],
                "revision": change["revision"],
                "operation": change["operation"],
                "reason": change["reason"],
                "new_revision": change.get("new_revision"),
                "from_impact_state": before_state,
                "to_impact_state": final_state,
                "route_ids": route_ids,
                "route_count": len(route_ids),
            }
        )
        changed_keys.add(key)

    exact_state = {
        str(item["key"]): str(item.get("impact_state", "stable"))
        for item in exact_references
    }
    baseline_route_states: dict[str, str] = {}
    simulated_route_states: dict[str, str] = {}
    for route in routes:
        _require(
            isinstance(route, dict)
            and isinstance(route.get("route_id"), str)
            and isinstance(route.get("exact_keys"), list),
            "E-EVIDENCE-SIMULATION-ROUTE",
            "every route must contain route_id and exact_keys",
        )
        route_id = route["route_id"]
        baseline_state = str(route.get("impact_state", "stable"))
        states = [exact_state.get(str(key), "stable") for key in route["exact_keys"]]
        final_state = _max_state(states)
        changed_for_route = sorted(set(route["exact_keys"]).intersection(changed_keys))
        route["baseline_impact_state"] = baseline_state
        route["impact_state"] = final_state
        route["simulated_change_keys"] = changed_for_route
        route["simulated_change_count"] = len(changed_for_route)
        baseline_route_states[route_id] = baseline_state
        simulated_route_states[route_id] = final_state

    for entity in entities:
        _require(
            isinstance(entity, dict) and isinstance(entity.get("exact_keys"), list),
            "E-EVIDENCE-SIMULATION-ENTITY-INDEX",
            "every entity must contain exact_keys",
        )
        baseline_state = str(entity.get("impact_state", "stable"))
        states = [exact_state.get(str(key), "stable") for key in entity["exact_keys"]]
        entity["baseline_impact_state"] = baseline_state
        entity["impact_state"] = _max_state(states)
        entity["simulated_change_keys"] = sorted(
            set(entity["exact_keys"]).intersection(changed_keys)
        )

    baseline_affected = sorted(
        route_id
        for route_id, state in baseline_route_states.items()
        if state != "stable"
    )
    simulated_affected = sorted(
        route_id
        for route_id, state in simulated_route_states.items()
        if state != "stable"
    )
    newly_affected = sorted(set(simulated_affected) - set(baseline_affected))
    escalated = sorted(
        route_id
        for route_id in simulated_route_states
        if _STATE_RANK[simulated_route_states[route_id]]
        > _STATE_RANK[baseline_route_states[route_id]]
    )
    newly_blocked = sorted(
        route_id
        for route_id, state in simulated_route_states.items()
        if state == "blocked" and baseline_route_states[route_id] != "blocked"
    )

    changed_states = [
        str(exact_map[key].get("impact_state", "stable")) for key in changed_keys
    ]
    scenario_state = _max_state(changed_states)
    if scenario_state == "blocked":
        decision = "simulation-blocked"
    elif scenario_state == "revalidation-required":
        decision = "simulation-revalidation-required"
    else:
        decision = "simulation-clear"

    simulated["stable_exact_reference_count"] = sum(
        item.get("impact_state") == "stable" for item in exact_references
    )
    simulated["revalidation_required_exact_reference_count"] = sum(
        item.get("impact_state") == "revalidation-required"
        for item in exact_references
    )
    simulated["blocked_exact_reference_count"] = sum(
        item.get("impact_state") == "blocked" for item in exact_references
    )
    simulated["affected_route_count"] = len(simulated_affected)
    simulated["affected_route_ids"] = simulated_affected
    simulated["decision"] = {
        "stable": "impact-index-clear",
        "revalidation-required": "impact-index-revalidation-required",
        "blocked": "impact-index-blocked",
    }[_max_state(list(simulated_route_states.values()))]

    applied_changes.sort(key=lambda item: item["key"])
    return {
        "contract": SIMULATION_CONTRACT,
        "source_index_contract": IMPACT_INDEX_CONTRACT,
        "scenario_contract": SCENARIO_CONTRACT,
        "source_index_sha256": _digest(index_payload),
        "scenario_sha256": _digest(scenario),
        "change_count": len(applied_changes),
        "applied_changes": applied_changes,
        "baseline_affected_route_ids": baseline_affected,
        "simulated_affected_route_ids": simulated_affected,
        "newly_affected_route_ids": newly_affected,
        "escalated_route_ids": escalated,
        "newly_blocked_route_ids": newly_blocked,
        "baseline_affected_route_count": len(baseline_affected),
        "simulated_affected_route_count": len(simulated_affected),
        "newly_affected_route_count": len(newly_affected),
        "escalated_route_count": len(escalated),
        "newly_blocked_route_count": len(newly_blocked),
        "simulated_index": simulated,
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
