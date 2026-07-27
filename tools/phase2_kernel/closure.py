#!/usr/bin/env python3
"""Phase 2 closure, kernel replaceability, and retrieval-entry evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping

from .compiler import compile_canonical
from .kernel import (
    CONTENT_CONTRACT,
    RUNTIME_CONTRACT,
    KernelError,
    exact_key,
    render_json,
)
from .repository import KernelRepository, validate_runtime

PORTABLE_SNAPSHOT_CONTRACT = "atlas-kernel-portable-snapshot/0.1"
CLOSURE_REPORT_CONTRACT = "atlas-phase2-completion-report/0.1"
MODE = "phase2-closure-candidate"
RETRIEVAL_DECISION = "proceed-bounded-retrieval-evaluation"


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")


def _require_mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def _runtime_from_portable_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    if snapshot.get("contract") != PORTABLE_SNAPSHOT_CONTRACT:
        raise KernelError(
            "E-PORTABLE-CONTRACT",
            f"expected {PORTABLE_SNAPSHOT_CONTRACT!r}, got {snapshot.get('contract')!r}",
        )
    if snapshot.get("source_contract") != CONTENT_CONTRACT:
        raise KernelError(
            "E-PORTABLE-SOURCE-CONTRACT",
            f"expected {CONTENT_CONTRACT!r}, got {snapshot.get('source_contract')!r}",
        )
    if snapshot.get("live") is not False or snapshot.get("mutation") is not False:
        raise KernelError(
            "E-PORTABLE-AUTHORITY",
            "portable snapshots must remain live=false and mutation=false",
        )
    forbidden = {"source_root", "revisions_by_id", "reverse_dependencies"}
    present = sorted(forbidden.intersection(snapshot))
    if present:
        raise KernelError(
            "E-PORTABLE-GENERATED-INDEX",
            f"portable snapshot contains generated runtime fields: {present}",
        )
    entities = snapshot.get("entities")
    if not isinstance(entities, list):
        raise KernelError("E-PORTABLE-STRUCTURE", "entities must be a list")
    if snapshot.get("entity_count") != len(entities) or not entities:
        raise KernelError(
            "E-PORTABLE-ENTITY-COUNT",
            "entity_count must equal the positive number of portable entities",
        )

    revisions: dict[str, list[int]] = defaultdict(list)
    reverse: dict[str, set[str]] = {}
    copied_entities = copy.deepcopy(entities)
    for entity in copied_entities:
        record = _require_mapping(
            entity, "E-PORTABLE-ENTITY", "portable entity must be an object"
        )
        key = record.get("key")
        entity_id = record.get("id")
        revision = record.get("revision")
        if not isinstance(key, str) or not isinstance(entity_id, str):
            raise KernelError("E-PORTABLE-ENTITY", "portable entity identity is malformed")
        if not isinstance(revision, int) or isinstance(revision, bool):
            raise KernelError("E-PORTABLE-ENTITY", "portable entity revision is malformed")
        revisions[entity_id].append(revision)
        reverse[key] = set()

    for entity in copied_entities:
        dependent_key = str(entity["key"])
        references = entity.get("references")
        if not isinstance(references, list):
            raise KernelError("E-PORTABLE-REFERENCE", "references must be a list")
        for reference in references:
            record = _require_mapping(
                reference,
                "E-PORTABLE-REFERENCE",
                "portable reference must be an object",
            )
            target_id = record.get("id")
            target_revision = record.get("revision")
            if (
                not isinstance(target_id, str)
                or not isinstance(target_revision, int)
                or isinstance(target_revision, bool)
            ):
                raise KernelError(
                    "E-PORTABLE-REFERENCE",
                    "portable reference identity or revision is malformed",
                )
            target = exact_key(target_id, target_revision)
            if target not in reverse:
                raise KernelError(
                    "E-PORTABLE-REFERENCE-TARGET",
                    f"portable reference targets unavailable exact entity {target!r}",
                )
            reverse[target].add(dependent_key)

    runtime = {
        "contract": RUNTIME_CONTRACT,
        "source_contract": CONTENT_CONTRACT,
        "source_root": "portable-snapshot",
        "source_digest": snapshot.get("source_digest"),
        "entity_count": len(copied_entities),
        "entities": copied_entities,
        "revisions_by_id": {
            entity_id: sorted(set(values))
            for entity_id, values in sorted(revisions.items())
        },
        "reverse_dependencies": {
            key: sorted(values) for key, values in sorted(reverse.items())
        },
    }
    validate_runtime(runtime)
    return runtime


def export_portable_snapshot(runtime: Mapping[str, Any]) -> dict[str, Any]:
    """Export semantic records without runtime-specific generated indexes."""
    validation = validate_runtime(runtime)
    return {
        "contract": PORTABLE_SNAPSHOT_CONTRACT,
        "source_contract": CONTENT_CONTRACT,
        "source_digest": validation["source_digest"],
        "entity_count": validation["entity_count"],
        "entities": copy.deepcopy(runtime["entities"]),
        "live": False,
        "mutation": False,
    }


def validate_portable_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    runtime = _runtime_from_portable_snapshot(snapshot)
    validation = validate_runtime(runtime)
    return {
        "contract": "atlas-kernel-portable-validation/0.1",
        "portable_contract": PORTABLE_SNAPSHOT_CONTRACT,
        "runtime_contract": RUNTIME_CONTRACT,
        "source_digest": validation["source_digest"],
        "entity_count": validation["entity_count"],
        "reference_count": validation["reference_count"],
        "relation_count": validation["relation_count"],
        "reverse_edge_count": validation["reverse_edge_count"],
        "decision": "valid",
        "live": False,
        "mutation": False,
    }


class PortableKernelRepository:
    """Independent read-only query engine over a storage-neutral snapshot."""

    def __init__(self, snapshot: Mapping[str, Any]):
        runtime = _runtime_from_portable_snapshot(snapshot)
        self.validation_report = validate_portable_snapshot(snapshot)
        self._entities = {
            str(entity["key"]): copy.deepcopy(entity) for entity in runtime["entities"]
        }
        self._revisions = {
            str(entity_id): list(revisions)
            for entity_id, revisions in runtime["revisions_by_id"].items()
        }
        self._reverse = {
            str(key): list(values)
            for key, values in runtime["reverse_dependencies"].items()
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
        raise KernelError("E-ENTITY-MISSING", f"entity {entity_id!r} is unavailable")

    def relation_targets(
        self, entity_id: str, revision: int, relation_type: str | None = None
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

    def provenance_sources(self, entity_id: str, revision: int) -> list[dict[str, Any]]:
        start = exact_key(entity_id, revision)
        self.exact(entity_id, revision)
        pending = [start]
        visited: set[str] = set()
        sources: dict[str, dict[str, Any]] = {}
        inbound = {"supports", "derived-from", "contextualizes", "replicates"}
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
                target = exact_key(str(reference["id"]), int(reference["revision"]))
                if target not in visited:
                    pending.append(target)
            for dependent_key in self._reverse.get(key, []):
                dependent = self._entities[dependent_key]
                for relation in dependent.get("relations", []):
                    target = exact_key(
                        str(relation["target"]), int(relation["target_revision"])
                    )
                    if (
                        target == key
                        and relation.get("type") in inbound
                        and dependent_key not in visited
                    ):
                        pending.append(dependent_key)
                        break
        return [sources[key] for key in sorted(sources)]

    def internal_impact(
        self, entity_id: str, revision: int, transitive: bool = True
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


def _assert_equal(name: str, expected: Any, actual: Any) -> None:
    if _json_bytes(expected) != _json_bytes(actual):
        raise KernelError(
            "E-CLOSURE-QUERY-DIVERGENCE",
            f"portable repository diverged for {name}",
        )


def run_phase2_closure(canonical_root: Path) -> dict[str, Any]:
    first = compile_canonical(canonical_root)
    second = compile_canonical(canonical_root)
    if render_json(first) != render_json(second):
        raise KernelError(
            "E-CLOSURE-NONDETERMINISTIC",
            "repeated canonical compilation produced different runtimes",
        )
    first_validation = validate_runtime(first)
    second_validation = validate_runtime(second)
    _assert_equal("runtime validation", first_validation, second_validation)

    snapshot = export_portable_snapshot(first)
    portable_validation = validate_portable_snapshot(snapshot)
    standard = KernelRepository(first)
    portable = PortableKernelRepository(snapshot)

    exact_checks = 0
    relation_checks = 0
    provenance_checks = 0
    impact_checks = 0
    for entity in first["entities"]:
        entity_id = str(entity["id"])
        revision = int(entity["revision"])
        key = str(entity["key"])
        _assert_equal(
            f"exact {key}",
            standard.exact(entity_id, revision),
            portable.exact(entity_id, revision),
        )
        exact_checks += 1
        _assert_equal(
            f"relations {key}",
            standard.relation_targets(entity_id, revision),
            portable.relation_targets(entity_id, revision),
        )
        relation_checks += 1
        _assert_equal(
            f"provenance {key}",
            standard.provenance_sources(entity_id, revision),
            portable.provenance_sources(entity_id, revision),
        )
        provenance_checks += 1
        _assert_equal(
            f"impact {key}",
            standard.internal_impact(entity_id, revision),
            portable.internal_impact(entity_id, revision),
        )
        impact_checks += 1

    rollback = compile_canonical(canonical_root)
    if render_json(first) != render_json(rollback):
        raise KernelError(
            "E-CLOSURE-ROLLBACK",
            "rollback rebuild from canonical Markdown changed the runtime",
        )
    snapshot_sha256 = hashlib.sha256(_json_bytes(snapshot)).hexdigest()
    total_checks = exact_checks + relation_checks + provenance_checks + impact_checks

    return {
        "contract": CLOSURE_REPORT_CONTRACT,
        "mode": MODE,
        "decision": "phase2-complete-candidate",
        "runtime_contract": RUNTIME_CONTRACT,
        "portable_contract": PORTABLE_SNAPSHOT_CONTRACT,
        "source_contract": CONTENT_CONTRACT,
        "source_digest": first_validation["source_digest"],
        "entity_count": first_validation["entity_count"],
        "deterministic_compilation": True,
        "strict_runtime_admission": first_validation["decision"] == "valid",
        "portable_validation": portable_validation,
        "query_equivalence": {
            "exact_lookup_checks": exact_checks,
            "relation_checks": relation_checks,
            "provenance_checks": provenance_checks,
            "impact_checks": impact_checks,
            "total_checks": total_checks,
            "decision": "equivalent",
        },
        "migration_and_rollback": {
            "portable_snapshot_sha256": snapshot_sha256,
            "generated_indexes_excluded": True,
            "alternate_repository_implementation": True,
            "canonical_rebuild_verified": True,
            "rollback_rebuild_verified": True,
            "canonical_markdown_remains_authoritative": True,
            "decision": "replaceable",
        },
        "retrieval_entry": {
            "decision": RETRIEVAL_DECISION,
            "next_phase": "phase-3-retrieval-evaluation-candidate",
            "allowed": [
                "bounded lexical and structured retrieval baselines",
                "deterministic relevance evaluation on versioned entities",
                "generated replaceable indexes",
                "results carrying exact entity IDs, revisions, and provenance",
            ],
            "blocked": [
                "automatic lifecycle or release mutation",
                "canonical content writes from retrieval output",
                "live Principia synchronization",
                "production retrieval quality claims",
                "unversioned latest-entity lookup",
                "vector database commitment before comparative evaluation",
            ],
        },
        "live": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = run_phase2_closure(args.canonical_root)
        rendered = render_json(report)
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"wrote={args.output}")
        return 0
    except (KernelError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
