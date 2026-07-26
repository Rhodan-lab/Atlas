#!/usr/bin/env python3
"""Deterministic Atlas Phase 2 knowledge kernel and Principia bridge receiver."""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

CONTENT_CONTRACT = "atlas-content/0.1"
RUNTIME_CONTRACT = "atlas-kernel-runtime/0.1"
BRIDGE_EXPORT_CONTRACT = "principia-atlas-bridge-export/0.1"
EXTERNAL_DEPENDENT_CONTRACT = "atlas-external-dependent/0.1"
PRINCIPIA_REPOSITORY = "Rhodan-lab/principle-to-system"
ENTITY_ID_RE = re.compile(
    r"^(?:src:[a-z0-9]+(?:-[a-z0-9]+)*|(?:evidence|claim|concept|model|question|synthesis):[a-z]{2,3}:[a-z0-9]+(?:-[a-z0-9]+)*)$"
)
PRINCIPIA_ID_RE = re.compile(
    r"^principia:(?:module|pathway|concept|map|system-dossier|failure-pattern|investigation|design-challenge|artifact):[a-z0-9]+(?:-[a-z0-9]+)*$"
)
ENTITY_TYPES = {"source", "evidence", "claim", "concept", "model", "question", "synthesis"}
BRIDGE_MODES = {"compatibility-fixture", "bridge-candidate"}
DEPENDENCY_ROLES = {"load-bearing", "supporting", "context"}
DEPENDENCY_USES = {
    "definition",
    "evidence",
    "claim-boundary",
    "model",
    "model-boundary",
    "source-context",
    "synthesis-context",
}
CHANGE_POLICIES = {"inspect", "revalidate", "block-release"}
PROHIBITED_STATUS_KEYS = {
    "status",
    "pedagogical_status",
    "release_status",
    "knowledge_status",
    "atlas_status",
    "review_status",
}
PROVENANCE_INBOUND_RELATIONS = {
    "supports",
    "derived-from",
    "contextualizes",
    "replicates",
}


class DuplicateKeyError(ValueError):
    pass


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise DuplicateKeyError(f"duplicate YAML key: {key!r}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _unique_mapping,
)


@dataclass(frozen=True)
class KernelError(ValueError):
    code: str
    message: str
    path: str | None = None

    def __str__(self) -> str:
        return f"{self.code}{f' [{self.path}]' if self.path else ''}: {self.message}"


@dataclass(frozen=True)
class AuthoredDocument:
    path: Path
    metadata: dict[str, Any]
    body: str
    source_sha256: str

    @property
    def entity_id(self) -> str:
        return str(self.metadata["id"])

    @property
    def revision(self) -> int:
        return int(self.metadata["revision"])

    @property
    def key(self) -> str:
        return exact_key(self.entity_id, self.revision)


def exact_key(entity_id: str, revision: int) -> str:
    return f"{entity_id}@{revision}"


def _json_safe(value: Any) -> Any:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {
            str(key): _json_safe(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    return value


def render_json(value: Mapping[str, Any]) -> str:
    return json.dumps(_json_safe(value), indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise KernelError("E-JSON-READ", str(exc), str(path)) from exc
    except json.JSONDecodeError as exc:
        raise KernelError("E-JSON-PARSE", str(exc), str(path)) from exc
    if not isinstance(value, dict):
        raise KernelError(
            "E-JSON-OBJECT",
            "document must contain a JSON object",
            str(path),
        )
    return value


def _validate_metadata(metadata: Mapping[str, Any], path: Path) -> None:
    if metadata.get("contract") != CONTENT_CONTRACT:
        raise KernelError(
            "E-CONTRACT-UNSUPPORTED",
            f"expected {CONTENT_CONTRACT!r}, got {metadata.get('contract')!r}",
            str(path),
        )
    entity_id = metadata.get("id")
    entity_type = metadata.get("type")
    revision = metadata.get("revision")
    if not isinstance(entity_id, str) or not ENTITY_ID_RE.fullmatch(entity_id):
        raise KernelError(
            "E-ID-NONCANONICAL",
            "invalid canonical entity ID",
            str(path),
        )
    if entity_type not in ENTITY_TYPES:
        raise KernelError(
            "E-TYPE-UNSUPPORTED",
            f"unsupported entity type {entity_type!r}",
            str(path),
        )
    expected_type = (
        "source" if entity_id.startswith("src:") else entity_id.split(":", 1)[0]
    )
    if expected_type != entity_type:
        raise KernelError(
            "E-ID-TYPE-MISMATCH",
            "entity ID prefix and type differ",
            str(path),
        )
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError(
            "E-REVISION",
            "revision must be a positive integer",
            str(path),
        )


def parse_markdown(path: Path) -> AuthoredDocument:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise KernelError("E-CANONICAL-READ", str(exc), str(path)) from exc
    lines = raw.splitlines()
    if not lines or lines[0].strip() != "---":
        raise KernelError(
            "E-FRONT-MATTER-MISSING",
            "file must start with '---'",
            str(path),
        )
    closing = next(
        (
            index
            for index, line in enumerate(lines[1:], 1)
            if line.strip() == "---"
        ),
        None,
    )
    if closing is None:
        raise KernelError(
            "E-FRONT-MATTER-UNCLOSED",
            "missing closing '---'",
            str(path),
        )
    try:
        metadata = yaml.load(
            "\n".join(lines[1:closing]),
            Loader=UniqueKeyLoader,
        )
    except (yaml.YAMLError, DuplicateKeyError) as exc:
        raise KernelError("E-YAML-PARSE", str(exc), str(path)) from exc
    if not isinstance(metadata, dict):
        raise KernelError(
            "E-FRONT-MATTER-TYPE",
            "front matter must be a mapping",
            str(path),
        )
    _validate_metadata(metadata, path)
    return AuthoredDocument(
        path=path,
        metadata=metadata,
        body="\n".join(lines[closing + 1 :]).strip(),
        source_sha256=hashlib.sha256(raw.encode("utf-8")).hexdigest(),
    )


def _walk_entity_ids(
    value: Any,
    field: str = "",
) -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        if ENTITY_ID_RE.fullmatch(value):
            yield field, value
    elif isinstance(value, Mapping):
        for key, item in sorted(value.items(), key=lambda pair: str(pair[0])):
            yield from _walk_entity_ids(
                item,
                f"{field}.{key}" if field else str(key),
            )
    elif isinstance(value, Sequence) and not isinstance(
        value,
        (str, bytes, bytearray),
    ):
        for index, item in enumerate(value):
            yield from _walk_entity_ids(
                item,
                f"{field}[{index}]" if field else f"[{index}]",
            )


def _review_level(metadata: Mapping[str, Any]) -> str | None:
    review = metadata.get("review")
    return (
        str(review["level"])
        if isinstance(review, Mapping)
        and isinstance(review.get("level"), str)
        else None
    )


def compile_canonical(canonical_root: Path) -> dict[str, Any]:
    root = canonical_root.resolve()
    paths = sorted(path for path in root.rglob("*.md") if path.is_file())
    if not paths:
        raise KernelError(
            "E-CANONICAL-EMPTY",
            "no canonical Markdown files found",
            str(root),
        )
    documents = [parse_markdown(path) for path in paths]
    by_key: dict[str, AuthoredDocument] = {}
    revisions_by_id: dict[str, list[int]] = {}
    for document in documents:
        if document.key in by_key:
            raise KernelError(
                "E-ENTITY-DUPLICATE",
                f"duplicate exact entity {document.key}",
            )
        by_key[document.key] = document
        revisions_by_id.setdefault(document.entity_id, []).append(document.revision)
    revisions_by_id = {
        entity_id: sorted(set(revisions))
        for entity_id, revisions in sorted(revisions_by_id.items())
    }
    latest_by_id = {
        entity_id: revisions[-1]
        for entity_id, revisions in revisions_by_id.items()
    }
    reverse_dependencies: dict[str, set[str]] = {
        key: set() for key in sorted(by_key)
    }
    entities: list[dict[str, Any]] = []
    source_digest = hashlib.sha256()

    for document in sorted(
        documents,
        key=lambda item: (item.entity_id, item.revision, str(item.path)),
    ):
        relative_path = document.path.resolve().relative_to(root).as_posix()
        source_digest.update(
            f"{relative_path}\0{document.source_sha256}\n".encode("utf-8")
        )
        references: dict[tuple[str, int], set[str]] = {}
        for field, target_id in _walk_entity_ids(document.metadata):
            if field == "id" or target_id == document.entity_id:
                continue
            if target_id not in latest_by_id:
                raise KernelError(
                    "E-CANONICAL-REFERENCE-MISSING",
                    f"{document.key} references missing entity {target_id!r} at {field}",
                    relative_path,
                )
            references.setdefault(
                (target_id, latest_by_id[target_id]),
                set(),
            ).add(field)
        relation_records: list[dict[str, Any]] = []
        relations = document.metadata.get("relations")
        if relations is not None:
            if not isinstance(relations, list):
                raise KernelError(
                    "E-RELATION-STRUCTURE",
                    "relations must be a list",
                    relative_path,
                )
            for index, relation in enumerate(relations):
                if not isinstance(relation, Mapping):
                    raise KernelError(
                        "E-RELATION-STRUCTURE",
                        f"relation {index} must be a mapping",
                        relative_path,
                    )
                target_id = relation.get("target")
                relation_type = relation.get("type")
                if not isinstance(target_id, str) or target_id not in latest_by_id:
                    raise KernelError(
                        "E-RELATION-TARGET",
                        f"relation {index} has unavailable target {target_id!r}",
                        relative_path,
                    )
                if not isinstance(relation_type, str) or not relation_type:
                    raise KernelError(
                        "E-RELATION-TYPE",
                        f"relation {index} requires a type",
                        relative_path,
                    )
                relation_records.append(
                    {
                        "type": relation_type,
                        "target": target_id,
                        "target_revision": latest_by_id[target_id],
                        "note": relation.get("note"),
                    }
                )
        reference_records = [
            {
                "id": target_id,
                "revision": target_revision,
                "fields": sorted(fields),
            }
            for (target_id, target_revision), fields in sorted(references.items())
        ]
        for reference in reference_records:
            reverse_dependencies[
                exact_key(reference["id"], reference["revision"])
            ].add(document.key)
        entities.append(
            {
                "key": document.key,
                "id": document.entity_id,
                "revision": document.revision,
                "type": document.metadata["type"],
                "title": document.metadata.get("title"),
                "status": document.metadata.get("status"),
                "staleness": document.metadata.get("staleness", "current"),
                "review_level": _review_level(document.metadata),
                "path": relative_path,
                "source_sha256": document.source_sha256,
                "body_sha256": hashlib.sha256(
                    document.body.encode("utf-8")
                ).hexdigest(),
                "metadata": _json_safe(document.metadata),
                "references": reference_records,
                "relations": sorted(
                    relation_records,
                    key=lambda item: (
                        item["type"],
                        item["target"],
                        item["target_revision"],
                    ),
                ),
            }
        )
    return {
        "contract": RUNTIME_CONTRACT,
        "source_contract": CONTENT_CONTRACT,
        "source_root": (
            canonical_root.as_posix()
            if not canonical_root.is_absolute()
            else root.name
        ),
        "source_digest": source_digest.hexdigest(),
        "entity_count": len(entities),
        "entities": entities,
        "revisions_by_id": revisions_by_id,
        "reverse_dependencies": {
            key: sorted(values)
            for key, values in sorted(reverse_dependencies.items())
        },
    }


class KernelRepository:
    def __init__(self, runtime: Mapping[str, Any]):
        if runtime.get("contract") != RUNTIME_CONTRACT:
            raise KernelError(
                "E-RUNTIME-CONTRACT",
                f"expected {RUNTIME_CONTRACT!r}, got {runtime.get('contract')!r}",
            )
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
                "runtime index is malformed",
            )
        self.runtime = dict(runtime)
        self._entities: dict[str, dict[str, Any]] = {}
        for entity in entities:
            if not isinstance(entity, dict) or not isinstance(
                entity.get("key"),
                str,
            ):
                raise KernelError(
                    "E-RUNTIME-ENTITY",
                    "runtime entity is malformed",
                )
            if entity["key"] in self._entities:
                raise KernelError(
                    "E-RUNTIME-DUPLICATE",
                    f"duplicate runtime key {entity['key']}",
                )
            self._entities[entity["key"]] = entity
        self._revisions = {
            str(entity_id): [int(revision) for revision in value]
            for entity_id, value in revisions.items()
            if isinstance(value, list)
        }
        self._reverse = {
            str(key): sorted(str(item) for item in value)
            for key, value in reverse.items()
            if isinstance(value, list)
        }

    def available_revisions(self, entity_id: str) -> list[int]:
        return list(self._revisions.get(entity_id, []))

    def exact(self, entity_id: str, revision: int) -> dict[str, Any]:
        entity = self._entities.get(exact_key(entity_id, revision))
        if entity is not None:
            return entity
        available = self.available_revisions(entity_id)
        if available:
            raise KernelError(
                "E-REVISION-MISSING",
                f"{entity_id!r} has revisions {available}, not revision {revision}",
            )
        raise KernelError(
            "E-ENTITY-MISSING",
            f"entity {entity_id!r} is unavailable",
        )

    def relation_targets(
        self,
        entity_id: str,
        revision: int,
        relation_type: str | None = None,
    ) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for relation in self.exact(entity_id, revision).get("relations", []):
            if relation_type is None or relation.get("type") == relation_type:
                result.append(
                    {
                        "relation": relation,
                        "entity": self.exact(
                            str(relation["target"]),
                            int(relation["target_revision"]),
                        ),
                    }
                )
        return result

    def provenance_sources(
        self,
        entity_id: str,
        revision: int,
    ) -> list[dict[str, Any]]:
        start = exact_key(entity_id, revision)
        self.exact(entity_id, revision)
        pending = [start]
        visited: set[str] = set()
        sources: dict[str, dict[str, Any]] = {}
        while pending:
            key = pending.pop(0)
            if key in visited:
                continue
            visited.add(key)
            entity = self._entities[key]
            if entity.get("type") == "source":
                sources[key] = entity
                continue
            for reference in entity.get("references", []):
                target_key = exact_key(
                    str(reference["id"]),
                    int(reference["revision"]),
                )
                if target_key not in visited:
                    pending.append(target_key)
            for dependent_key in self._reverse.get(key, []):
                dependent = self._entities[dependent_key]
                for relation in dependent.get("relations", []):
                    relation_target = exact_key(
                        str(relation["target"]),
                        int(relation["target_revision"]),
                    )
                    if (
                        relation_target == key
                        and relation.get("type")
                        in PROVENANCE_INBOUND_RELATIONS
                        and dependent_key not in visited
                    ):
                        pending.append(dependent_key)
                        break
        return [sources[key] for key in sorted(sources)]

    def internal_impact(
        self,
        entity_id: str,
        revision: int,
        transitive: bool = True,
    ) -> list[dict[str, Any]]:
        start = exact_key(entity_id, revision)
        self.exact(entity_id, revision)
        pending: list[tuple[str, int]] = [(start, 0)]
        visited = {start}
        results: dict[str, dict[str, Any]] = {}
        while pending:
            key, depth = pending.pop(0)
            for dependent_key in self._reverse.get(key, []):
                if dependent_key in visited:
                    continue
                visited.add(dependent_key)
                results[dependent_key] = {
                    "depth": depth + 1,
                    "entity": self._entities[dependent_key],
                }
                if transitive:
                    pending.append((dependent_key, depth + 1))
        return [results[key] for key in sorted(results)]


def _find_prohibited_status_key(
    value: Any,
    path: str = "$",
) -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if str(key) in PROHIBITED_STATUS_KEYS:
                return f"{path}.{key}"
            found = _find_prohibited_status_key(item, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found = _find_prohibited_status_key(
                item,
                f"{path}[{index}]",
            )
            if found:
                return found
    return None


def import_principia_export(
    payload: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    prohibited = _find_prohibited_status_key(payload)
    if prohibited:
        raise KernelError(
            "E-BRIDGE-STATUS-INHERITANCE",
            f"Principia status data is prohibited at {prohibited}",
        )
    if payload.get("contract") != BRIDGE_EXPORT_CONTRACT:
        if "depends_on" in payload and "dependencies" not in payload:
            raise KernelError(
                "E-BRIDGE-LEGACY-EXPORT",
                "legacy id-only depends_on exports omit exact revisions; use the exact-revision bridge export contract",
            )
        raise KernelError(
            "E-BRIDGE-CONTRACT",
            f"expected {BRIDGE_EXPORT_CONTRACT!r}, got {payload.get('contract')!r}",
        )
    if payload.get("mode") not in BRIDGE_MODES:
        raise KernelError(
            "E-BRIDGE-MODE",
            f"unsupported bridge mode {payload.get('mode')!r}",
        )
    if payload.get("live") is not False:
        raise KernelError(
            "E-BRIDGE-LIVE-FROZEN",
            "Phase 2 accepts only live=false bridge candidates",
        )
    artifact_id = payload.get("id")
    if not isinstance(artifact_id, str) or not PRINCIPIA_ID_RE.fullmatch(
        artifact_id
    ):
        raise KernelError(
            "E-BRIDGE-ID",
            "invalid Principia artifact ID",
        )
    if payload.get("repository") != PRINCIPIA_REPOSITORY:
        raise KernelError(
            "E-BRIDGE-REPOSITORY",
            f"expected repository {PRINCIPIA_REPOSITORY!r}",
        )
    revision = payload.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError(
            "E-BRIDGE-ARTIFACT-REVISION",
            "artifact revision must be a positive integer",
        )
    if payload.get("kind") != "principia-artifact":
        raise KernelError(
            "E-BRIDGE-KIND",
            "kind must be 'principia-artifact'",
        )
    role = payload.get("role")
    if role not in DEPENDENCY_ROLES:
        raise KernelError(
            "E-BRIDGE-ROLE",
            f"unsupported artifact role {role!r}",
        )
    dependencies = payload.get("dependencies")
    if not isinstance(dependencies, list) or not dependencies:
        raise KernelError(
            "E-BRIDGE-DEPENDENCIES",
            "dependencies must be a non-empty list",
        )
    imported: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, dependency in enumerate(dependencies):
        if not isinstance(dependency, Mapping):
            raise KernelError(
                "E-BRIDGE-DEPENDENCY",
                f"dependency {index} must be an object",
            )
        entity_id = dependency.get("id")
        entity_revision = dependency.get("revision")
        if not isinstance(entity_id, str) or not ENTITY_ID_RE.fullmatch(
            entity_id
        ):
            raise KernelError(
                "E-BRIDGE-ENTITY-ID",
                f"dependency {index} has an invalid entity ID",
            )
        if entity_id in seen_ids:
            raise KernelError(
                "E-BRIDGE-DUPLICATE",
                f"duplicate dependency ID {entity_id!r}",
            )
        seen_ids.add(entity_id)
        if (
            not isinstance(entity_revision, int)
            or isinstance(entity_revision, bool)
            or entity_revision < 1
        ):
            raise KernelError(
                "E-BRIDGE-REVISION-MISSING",
                f"dependency {entity_id!r} requires a positive exact revision",
            )
        try:
            entity = repository.exact(entity_id, entity_revision)
        except KernelError as exc:
            mapped = (
                "E-BRIDGE-REVISION-MISSING"
                if exc.code == "E-REVISION-MISSING"
                else (
                    "E-BRIDGE-ENTITY-MISSING"
                    if exc.code == "E-ENTITY-MISSING"
                    else exc.code
                )
            )
            raise KernelError(mapped, exc.message) from exc
        if (
            dependency.get("entity_type") is not None
            and dependency.get("entity_type") != entity.get("type")
        ):
            raise KernelError(
                "E-BRIDGE-TYPE-MISMATCH",
                f"{entity_id!r} is {entity.get('type')!r}, not {dependency.get('entity_type')!r}",
            )
        dependency_role = dependency.get("role")
        dependency_use = dependency.get("use")
        policy = dependency.get("change_policy")
        if dependency_role not in DEPENDENCY_ROLES:
            raise KernelError(
                "E-BRIDGE-DEPENDENCY-ROLE",
                f"unsupported role for {entity_id!r}",
            )
        if dependency_use not in DEPENDENCY_USES:
            raise KernelError(
                "E-BRIDGE-USE",
                f"unsupported use for {entity_id!r}",
            )
        if policy not in CHANGE_POLICIES:
            raise KernelError(
                "E-BRIDGE-CHANGE-POLICY",
                f"unsupported change policy for {entity_id!r}",
            )
        available = repository.available_revisions(entity_id)
        resolution = "current"
        if entity.get("status") in {"retracted", "deprecated"}:
            resolution = str(entity["status"])
        elif available and max(available) > entity_revision:
            resolution = "superseded"
        imported.append(
            {
                "id": entity_id,
                "revision": entity_revision,
                "key": exact_key(entity_id, entity_revision),
                "entity_type": entity.get("type"),
                "role": dependency_role,
                "use": dependency_use,
                "change_policy": policy,
                "resolution": resolution,
            }
        )
    return {
        "contract": EXTERNAL_DEPENDENT_CONTRACT,
        "source_contract": BRIDGE_EXPORT_CONTRACT,
        "mode": payload["mode"],
        "live": False,
        "id": artifact_id,
        "kind": "principia-artifact",
        "repository": PRINCIPIA_REPOSITORY,
        "revision": revision,
        "role": role,
        "dependencies": sorted(
            imported,
            key=lambda item: (item["id"], item["revision"]),
        ),
        "status_inheritance": "prohibited",
    }


def impact_report(
    repository: KernelRepository,
    entity_id: str,
    revision: int,
    external_dependents: Sequence[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    entity = repository.exact(entity_id, revision)
    target_key = exact_key(entity_id, revision)
    external: list[dict[str, Any]] = []
    for dependent in external_dependents:
        if dependent.get("contract") != EXTERNAL_DEPENDENT_CONTRACT:
            raise KernelError(
                "E-EXTERNAL-CONTRACT",
                "external dependent record has an unsupported contract",
            )
        for dependency in dependent.get("dependencies", []):
            if (
                isinstance(dependency, Mapping)
                and dependency.get("key") == target_key
            ):
                external.append(
                    {
                        "id": dependent.get("id"),
                        "revision": dependent.get("revision"),
                        "repository": dependent.get("repository"),
                        "role": dependency.get("role"),
                        "use": dependency.get("use"),
                        "action": dependency.get("change_policy"),
                        "resolution": dependency.get("resolution"),
                    }
                )
    return {
        "contract": "atlas-impact-report/0.1",
        "entity": {
            "id": entity_id,
            "revision": revision,
            "key": target_key,
            "status": entity.get("status"),
            "staleness": entity.get("staleness"),
        },
        "internal_dependents": repository.internal_impact(
            entity_id,
            revision,
            transitive=True,
        ),
        "external_dependents": sorted(
            external,
            key=lambda item: (
                str(item["id"]),
                int(item["revision"]),
            ),
        ),
        "automatic_status_change": False,
    }
