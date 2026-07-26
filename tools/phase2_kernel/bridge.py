"""Principia export adapters and lifecycle-aware Atlas impact reporting."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping, Sequence

from .kernel import (
    BRIDGE_EXPORT_CONTRACT,
    CONTENT_CONTRACT,
    KernelError,
    KernelRepository,
    impact_report,
    import_principia_export,
)

PRINCIPIA_EXTERNAL_DEPENDENT_CONTRACT = "principia-atlas-external-dependent/0.2"
BRIDGE_ADAPTER_CONTRACT = "atlas-principia-bridge-adapter/0.1"
LIFECYCLE_IMPACT_CONTRACT = "atlas-lifecycle-impact-report/0.1"

_TOP_LEVEL_FIELDS = {
    "contract",
    "id",
    "kind",
    "repository",
    "revision",
    "role",
    "bridge_mode",
    "live",
    "atlas_content_contract",
    "depends_on",
    "depends_on_exact",
}
_DEPENDENCY_FIELDS = {
    "id",
    "revision",
    "entity_type",
    "role",
    "use",
    "change_policy",
}
_PROHIBITED_STATUS_KEYS = {
    "status",
    "pedagogical_status",
    "release_status",
    "knowledge_status",
    "atlas_status",
    "review_status",
}
_ACTION_RANK = {"inspect": 0, "revalidate": 1, "block-release": 2}


def _status_path(value: Any, path: str = "$") -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            if key_text in _PROHIBITED_STATUS_KEYS:
                return f"{path}.{key_text}"
            found = _status_path(item, f"{path}.{key_text}")
            if found:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = _status_path(item, f"{path}[{index}]")
            if found:
                return found
    return None


def adapt_principia_export(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Adapt Principia's merged v0.2 export into the Atlas receiver contract.

    The earlier Atlas-local bridge prototype remains accepted for regression
    compatibility. Unknown contracts are passed through so the underlying
    receiver can produce its deterministic contract error.
    """
    source = deepcopy(dict(payload))
    status_path = _status_path(source)
    if status_path:
        raise KernelError(
            "E-BRIDGE-STATUS-INHERITANCE",
            f"Principia status data is prohibited at {status_path}",
        )

    contract = source.get("contract")
    if contract == BRIDGE_EXPORT_CONTRACT:
        return source
    if contract != PRINCIPIA_EXTERNAL_DEPENDENT_CONTRACT:
        return source

    unknown = sorted(set(source) - _TOP_LEVEL_FIELDS)
    if unknown:
        raise KernelError(
            "E-PRINCIPIA-EXPORT-FIELD",
            f"unsupported top-level fields: {unknown}",
        )
    if source.get("atlas_content_contract") != CONTENT_CONTRACT:
        raise KernelError(
            "E-PRINCIPIA-ATLAS-CONTRACT",
            f"expected {CONTENT_CONTRACT!r}, got {source.get('atlas_content_contract')!r}",
        )

    legacy_ids = source.get("depends_on")
    exact_dependencies = source.get("depends_on_exact")
    if not isinstance(legacy_ids, list) or not all(
        isinstance(item, str) for item in legacy_ids
    ):
        raise KernelError(
            "E-PRINCIPIA-LEGACY-INDEX",
            "depends_on must be a list of Atlas entity IDs",
        )
    if not isinstance(exact_dependencies, list) or not exact_dependencies:
        raise KernelError(
            "E-PRINCIPIA-EXACT-DEPENDENCIES",
            "depends_on_exact must be a non-empty list",
        )

    exact_ids: list[str] = []
    normalized_dependencies: list[dict[str, Any]] = []
    for index, dependency in enumerate(exact_dependencies):
        if not isinstance(dependency, Mapping):
            raise KernelError(
                "E-PRINCIPIA-EXACT-DEPENDENCY",
                f"depends_on_exact[{index}] must be an object",
            )
        unknown_dependency = sorted(set(dependency) - _DEPENDENCY_FIELDS)
        if unknown_dependency:
            raise KernelError(
                "E-PRINCIPIA-DEPENDENCY-FIELD",
                f"depends_on_exact[{index}] has unsupported fields: {unknown_dependency}",
            )
        entity_id = dependency.get("id")
        if not isinstance(entity_id, str):
            raise KernelError(
                "E-PRINCIPIA-EXACT-DEPENDENCY",
                f"depends_on_exact[{index}] requires a string id",
            )
        exact_ids.append(entity_id)
        normalized_dependencies.append(dict(dependency))

    if legacy_ids != sorted(legacy_ids) or exact_ids != sorted(exact_ids):
        raise KernelError(
            "E-PRINCIPIA-EXPORT-ORDER",
            "depends_on and depends_on_exact must use deterministic ID ordering",
        )
    if legacy_ids != exact_ids:
        raise KernelError(
            "E-PRINCIPIA-LEGACY-INDEX",
            "depends_on must exactly mirror the IDs in depends_on_exact",
        )

    return {
        "contract": BRIDGE_EXPORT_CONTRACT,
        "mode": source.get("bridge_mode"),
        "live": source.get("live"),
        "id": source.get("id"),
        "kind": source.get("kind"),
        "repository": source.get("repository"),
        "revision": source.get("revision"),
        "role": source.get("role"),
        "dependencies": normalized_dependencies,
    }


def import_principia_candidate(
    payload: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    """Validate either bridge shape and return one Atlas operational record."""
    source_contract = payload.get("contract")
    imported = import_principia_export(adapt_principia_export(payload), repository)
    if source_contract == PRINCIPIA_EXTERNAL_DEPENDENT_CONTRACT:
        imported["source_contract"] = PRINCIPIA_EXTERNAL_DEPENDENT_CONTRACT
        imported["adapter_contract"] = BRIDGE_ADAPTER_CONTRACT
        imported["source_shape"] = "depends_on+depends_on_exact"
        imported["legacy_id_index_verified"] = True
    return imported


def _effective_action(
    declared_action: str,
    lifecycle_status: str | None,
    staleness: str | None,
) -> tuple[str, str]:
    effective = declared_action
    reason = "principia-declared-policy"
    if lifecycle_status == "retracted":
        return "block-release", "atlas-entity-retracted"
    if lifecycle_status == "deprecated" and _ACTION_RANK[effective] < _ACTION_RANK["revalidate"]:
        effective = "revalidate"
        reason = "atlas-entity-deprecated"
    if staleness in {"review-required", "confirmed-stale"} and _ACTION_RANK[effective] < _ACTION_RANK["revalidate"]:
        effective = "revalidate"
        reason = f"atlas-staleness-{staleness}"
    return effective, reason


def lifecycle_impact_report(
    repository: KernelRepository,
    entity_id: str,
    revision: int,
    external_dependents: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    """Add lifecycle escalation while preserving the no-mutation boundary."""
    report = impact_report(repository, entity_id, revision, external_dependents)
    entity_status = report["entity"].get("status")
    staleness = report["entity"].get("staleness")
    enriched: list[dict[str, Any]] = []
    for dependent in report["external_dependents"]:
        item = dict(dependent)
        declared = str(item.get("action"))
        effective, reason = _effective_action(declared, entity_status, staleness)
        item["declared_action"] = declared
        item["effective_action"] = effective
        item["lifecycle_reason"] = reason
        enriched.append(item)
    report["contract"] = LIFECYCLE_IMPACT_CONTRACT
    report["base_contract"] = "atlas-impact-report/0.1"
    report["external_dependents"] = enriched
    report["automatic_status_change"] = False
    report["automatic_release_action"] = False
    return report
