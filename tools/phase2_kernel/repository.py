"""Strict admission boundary for compiled Atlas Phase 2 runtimes.

The original kernel repository remains the query engine. This module validates a
serialized runtime completely before exposing that engine through the public
``KernelRepository`` name. Validation is read-only and deterministic.
"""
from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Mapping

from .kernel import (
    CONTENT_CONTRACT,
    ENTITY_ID_RE,
    ENTITY_TYPES,
    RUNTIME_CONTRACT,
    KernelError,
    KernelRepository as _KernelRepository,
    exact_key,
)

RUNTIME_VALIDATION_CONTRACT = "atlas-runtime-validation-report/0.1"
_HEX_64 = re.compile(r"^[0-9a-f]{64}$")


def _positive_int(value: Any, code: str, message: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise KernelError(code, message)
    return value


def _digest(value: Any, path: str) -> str:
    if not isinstance(value, str) or not _HEX_64.fullmatch(value):
        raise KernelError(
            "E-RUNTIME-DIGEST",
            "expected a lowercase 64-character SHA-256 digest",
            path,
        )
    return value


def _entity_type(entity_id: str) -> str:
    return "source" if entity_id.startswith("src:") else entity_id.split(":", 1)[0]


def _ordered_unique_strings(value: Any, code: str, path: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise KernelError(code, "expected a list of strings", path)
    if value != sorted(value) or len(value) != len(set(value)):
        raise KernelError(code, "list must be sorted and duplicate-free", path)
    return list(value)


def validate_runtime(runtime: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a complete ``atlas-kernel-runtime/0.1`` document.

    The validator rejects malformed entities and any disagreement between the
    entity list, exact revision index, reference graph, relation graph, and
    reverse dependency index before query execution begins.
    """
    if not isinstance(runtime, Mapping):
        raise KernelError("E-RUNTIME-STRUCTURE", "runtime must be an object")
    if runtime.get("contract") != RUNTIME_CONTRACT:
        raise KernelError(
            "E-RUNTIME-CONTRACT",
            f"expected {RUNTIME_CONTRACT!r}, got {runtime.get('contract')!r}",
        )
    if runtime.get("source_contract") != CONTENT_CONTRACT:
        raise KernelError(
            "E-RUNTIME-SOURCE-CONTRACT",
            f"expected {CONTENT_CONTRACT!r}, got {runtime.get('source_contract')!r}",
        )
    if not isinstance(runtime.get("source_root"), str) or not runtime["source_root"]:
        raise KernelError("E-RUNTIME-SOURCE", "source_root must be a non-empty string")
    _digest(runtime.get("source_digest"), "$.source_digest")

    entities = runtime.get("entities")
    revisions = runtime.get("revisions_by_id")
    reverse = runtime.get("reverse_dependencies")
    if (
        not isinstance(entities, list)
        or not isinstance(revisions, Mapping)
        or not isinstance(reverse, Mapping)
    ):
        raise KernelError(
            "E-RUNTIME-STRUCTURE",
            "entities, revisions_by_id, and reverse_dependencies are required",
        )
    entity_count = runtime.get("entity_count")
    if (
        not isinstance(entity_count, int)
        or isinstance(entity_count, bool)
        or entity_count < 0
        or entity_count != len(entities)
    ):
        raise KernelError(
            "E-RUNTIME-ENTITY-COUNT",
            "entity_count must equal the number of entity records",
        )

    by_key: dict[str, Mapping[str, Any]] = {}
    expected_revisions: dict[str, list[int]] = defaultdict(list)
    reference_targets: dict[str, list[str]] = {}
    relation_targets: dict[str, list[str]] = {}
    reference_count = 0
    relation_count = 0
    ordering: list[tuple[str, int, str]] = []

    for index, entity in enumerate(entities):
        path = f"$.entities[{index}]"
        if not isinstance(entity, Mapping):
            raise KernelError("E-RUNTIME-ENTITY", "entity must be an object", path)
        entity_id = entity.get("id")
        if not isinstance(entity_id, str) or not ENTITY_ID_RE.fullmatch(entity_id):
            raise KernelError("E-RUNTIME-ENTITY-ID", "invalid canonical entity ID", path)
        entity_type = entity.get("type")
        if entity_type not in ENTITY_TYPES or entity_type != _entity_type(entity_id):
            raise KernelError(
                "E-RUNTIME-ENTITY-TYPE",
                "entity ID prefix and type must agree",
                path,
            )
        revision = _positive_int(
            entity.get("revision"),
            "E-RUNTIME-ENTITY-REVISION",
            "entity revision must be a positive integer",
        )
        key = entity.get("key")
        expected_key = exact_key(entity_id, revision)
        if key != expected_key:
            raise KernelError(
                "E-RUNTIME-KEY-MISMATCH",
                f"expected key {expected_key!r}, got {key!r}",
                path,
            )
        if key in by_key:
            raise KernelError("E-RUNTIME-DUPLICATE", f"duplicate runtime key {key!r}", path)
        by_key[key] = entity
        expected_revisions[entity_id].append(revision)
        ordering.append((entity_id, revision, str(entity.get("path", ""))))

        if not isinstance(entity.get("path"), str) or not entity["path"]:
            raise KernelError("E-RUNTIME-ENTITY", "entity path must be non-empty", path)
        _digest(entity.get("source_sha256"), f"{path}.source_sha256")
        _digest(entity.get("body_sha256"), f"{path}.body_sha256")
        metadata = entity.get("metadata")
        if not isinstance(metadata, Mapping):
            raise KernelError("E-RUNTIME-METADATA", "metadata must be an object", path)
        if (
            metadata.get("contract") != CONTENT_CONTRACT
            or metadata.get("id") != entity_id
            or metadata.get("type") != entity_type
            or metadata.get("revision") != revision
        ):
            raise KernelError(
                "E-RUNTIME-METADATA",
                "metadata identity must match the runtime entity",
                path,
            )

        references = entity.get("references")
        if not isinstance(references, list):
            raise KernelError("E-RUNTIME-REFERENCE", "references must be a list", path)
        current_reference_targets: list[str] = []
        reference_order: list[tuple[str, int]] = []
        for reference_index, reference in enumerate(references):
            reference_path = f"{path}.references[{reference_index}]"
            if not isinstance(reference, Mapping):
                raise KernelError("E-RUNTIME-REFERENCE", "reference must be an object", reference_path)
            target_id = reference.get("id")
            if not isinstance(target_id, str) or not ENTITY_ID_RE.fullmatch(target_id):
                raise KernelError("E-RUNTIME-REFERENCE", "invalid reference entity ID", reference_path)
            target_revision = _positive_int(
                reference.get("revision"),
                "E-RUNTIME-REFERENCE",
                "reference revision must be a positive integer",
            )
            _ordered_unique_strings(
                reference.get("fields"),
                "E-RUNTIME-REFERENCE",
                f"{reference_path}.fields",
            )
            target_key = exact_key(target_id, target_revision)
            current_reference_targets.append(target_key)
            reference_order.append((target_id, target_revision))
            reference_count += 1
        if reference_order != sorted(reference_order) or len(current_reference_targets) != len(set(current_reference_targets)):
            raise KernelError(
                "E-RUNTIME-REFERENCE-ORDER",
                "references must be sorted and target each exact entity at most once",
                path,
            )
        reference_targets[key] = current_reference_targets

        relations = entity.get("relations")
        if not isinstance(relations, list):
            raise KernelError("E-RUNTIME-RELATION", "relations must be a list", path)
        current_relation_targets: list[str] = []
        relation_order: list[tuple[str, str, int]] = []
        for relation_index, relation in enumerate(relations):
            relation_path = f"{path}.relations[{relation_index}]"
            if not isinstance(relation, Mapping):
                raise KernelError("E-RUNTIME-RELATION", "relation must be an object", relation_path)
            relation_type = relation.get("type")
            target_id = relation.get("target")
            if not isinstance(relation_type, str) or not relation_type:
                raise KernelError("E-RUNTIME-RELATION", "relation type must be non-empty", relation_path)
            if not isinstance(target_id, str) or not ENTITY_ID_RE.fullmatch(target_id):
                raise KernelError("E-RUNTIME-RELATION", "invalid relation target ID", relation_path)
            target_revision = _positive_int(
                relation.get("target_revision"),
                "E-RUNTIME-RELATION",
                "relation target_revision must be a positive integer",
            )
            target_key = exact_key(target_id, target_revision)
            current_relation_targets.append(target_key)
            relation_order.append((relation_type, target_id, target_revision))
            relation_count += 1
        if relation_order != sorted(relation_order):
            raise KernelError(
                "E-RUNTIME-RELATION-ORDER",
                "relations must use deterministic ordering",
                path,
            )
        relation_targets[key] = current_relation_targets

    if ordering != sorted(ordering):
        raise KernelError(
            "E-RUNTIME-ENTITY-ORDER",
            "entities must use deterministic ID, revision, and path ordering",
        )

    entity_keys = set(by_key)
    for source_key, targets in reference_targets.items():
        for target_key in targets:
            if target_key not in entity_keys:
                raise KernelError(
                    "E-RUNTIME-REFERENCE-TARGET",
                    f"{source_key!r} references unavailable exact entity {target_key!r}",
                )
    for source_key, targets in relation_targets.items():
        for target_key in targets:
            if target_key not in entity_keys:
                raise KernelError(
                    "E-RUNTIME-RELATION-TARGET",
                    f"{source_key!r} relates to unavailable exact entity {target_key!r}",
                )
            if target_key not in reference_targets[source_key]:
                raise KernelError(
                    "E-RUNTIME-RELATION-REFERENCE",
                    f"relation target {target_key!r} is absent from {source_key!r} references",
                )

    normalized_revisions: dict[str, list[int]] = {}
    for entity_id, value in revisions.items():
        if not isinstance(entity_id, str) or not ENTITY_ID_RE.fullmatch(entity_id):
            raise KernelError("E-RUNTIME-REVISION-INDEX", "invalid revision-index entity ID")
        if not isinstance(value, list) or any(
            not isinstance(item, int) or isinstance(item, bool) or item < 1 for item in value
        ):
            raise KernelError("E-RUNTIME-REVISION-INDEX", "revision index values must be positive integers")
        if value != sorted(value) or len(value) != len(set(value)):
            raise KernelError("E-RUNTIME-REVISION-INDEX", "revision index values must be sorted and unique")
        normalized_revisions[entity_id] = list(value)
    expected_revision_map = {
        entity_id: sorted(values) for entity_id, values in sorted(expected_revisions.items())
    }
    if normalized_revisions != expected_revision_map:
        raise KernelError(
            "E-RUNTIME-REVISION-INDEX",
            "revisions_by_id does not exactly describe the entity records",
        )

    normalized_reverse: dict[str, list[str]] = {}
    for target_key, dependents in reverse.items():
        if target_key not in entity_keys:
            raise KernelError(
                "E-RUNTIME-REVERSE-INDEX",
                f"reverse index contains unavailable target {target_key!r}",
            )
        values = _ordered_unique_strings(
            dependents,
            "E-RUNTIME-REVERSE-INDEX",
            f"$.reverse_dependencies.{target_key}",
        )
        for dependent_key in values:
            if dependent_key not in entity_keys:
                raise KernelError(
                    "E-RUNTIME-REVERSE-INDEX",
                    f"reverse index contains unavailable dependent {dependent_key!r}",
                )
        normalized_reverse[target_key] = values
    if set(normalized_reverse) != entity_keys:
        raise KernelError(
            "E-RUNTIME-REVERSE-INDEX",
            "reverse_dependencies must contain every exact entity key",
        )
    expected_reverse: dict[str, list[str]] = {key: [] for key in sorted(entity_keys)}
    for dependent_key, targets in reference_targets.items():
        for target_key in targets:
            expected_reverse[target_key].append(dependent_key)
    expected_reverse = {
        key: sorted(set(values)) for key, values in sorted(expected_reverse.items())
    }
    if normalized_reverse != expected_reverse:
        raise KernelError(
            "E-RUNTIME-REVERSE-INDEX",
            "reverse_dependencies does not exactly mirror entity references",
        )

    return {
        "contract": RUNTIME_VALIDATION_CONTRACT,
        "runtime_contract": RUNTIME_CONTRACT,
        "source_contract": CONTENT_CONTRACT,
        "source_digest": runtime["source_digest"],
        "entity_count": len(entities),
        "reference_count": reference_count,
        "relation_count": relation_count,
        "reverse_edge_count": sum(len(values) for values in normalized_reverse.values()),
        "decision": "valid",
        "mutation": False,
    }


class KernelRepository(_KernelRepository):
    """Public repository that rejects malformed runtimes before indexing them."""

    def __init__(self, runtime: Mapping[str, Any]):
        self.validation_report = validate_runtime(runtime)
        super().__init__(runtime)
