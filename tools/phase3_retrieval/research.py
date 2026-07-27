#!/usr/bin/env python3
"""Deterministic Phase 3 filters, research trails, and candidate discovery contracts."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase3_retrieval.contracts import MODE, validate_query_set
from tools.phase3_retrieval.lexical import _json_sha256

FILTER_CONTRACT = "atlas-retrieval-filter/0.1"
FILTER_RESULT_CONTRACT = "atlas-filtered-result-set/0.1"
TRAIL_CONTRACT = "atlas-research-trail/0.1"
CONTRADICTION_CONTRACT = "atlas-contradiction-candidate/0.1"
DUPLICATE_CONTRACT = "atlas-duplicate-candidate/0.1"
FIXTURE_CONTRACT = "atlas-phase3-research-foundation-fixtures/0.1"
REPORT_CONTRACT = "atlas-phase3-research-foundation-report/0.1"
STRUCTURED_BASELINE_CONTRACT = "atlas-phase3-structured-baseline/0.1"

ID_RE = re.compile(r"^(?:filter|trail):en:[a-z0-9]+(?:-[a-z0-9]+)*$")
CANDIDATE_ID_RE = re.compile(
    r"^candidate:(?:contradiction|duplicate):[a-z0-9]+(?:-[a-z0-9]+)*$"
)
EVIDENCE_ROLES = frozenset({"supports", "derived-from", "contextualizes", "replicates"})
TRAIL_ACTIONS = frozenset({"include", "exclude", "context"})
CONTRADICTION_ASSESSMENTS = frozenset(
    {"needs-review", "scope-difference-likely", "substantive-tension"}
)
DUPLICATE_ASSESSMENTS = frozenset(
    {"needs-review", "related-not-duplicate", "probable-duplicate"}
)


def _require_mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def _require_string(value: Any, code: str, message: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KernelError(code, message)
    return value


def _require_string_list(
    value: Any,
    code: str,
    message: str,
    *,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise KernelError(code, message)
    if not allow_empty and not value:
        raise KernelError(code, message)
    if len(value) != len(set(value)):
        raise KernelError(code, message + " and may not contain duplicates")
    return list(value)


def _parse_date(value: Any, code: str, field: str) -> date:
    if not isinstance(value, str):
        raise KernelError(code, f"{field} must be an ISO date")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise KernelError(code, f"{field} must be an ISO date") from exc


def _entity_domain(entity: Mapping[str, Any]) -> str:
    path = str(entity["path"])
    return path.split("/", 1)[0]


def _entity_updated(entity: Mapping[str, Any]) -> str | None:
    metadata = entity.get("metadata")
    if not isinstance(metadata, Mapping):
        return None
    updated = metadata.get("updated")
    return str(updated) if updated is not None else None


def _entity_evidence_roles(entity: Mapping[str, Any]) -> list[str]:
    roles = {
        str(relation["type"])
        for relation in entity.get("relations", [])
        if isinstance(relation, Mapping)
        and isinstance(relation.get("type"), str)
        and relation["type"] in EVIDENCE_ROLES
    }
    return sorted(roles)


def _available_domains(repository: KernelRepository) -> set[str]:
    return {_entity_domain(entity) for entity in repository.runtime["entities"]}


def validate_filter(
    record: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    if record.get("contract") != FILTER_CONTRACT:
        raise KernelError("E-FILTER-CONTRACT", f"expected {FILTER_CONTRACT!r}")
    filter_id = record.get("id")
    if not isinstance(filter_id, str) or not ID_RE.fullmatch(filter_id) or not filter_id.startswith("filter:"):
        raise KernelError("E-FILTER-ID", "filter ID must be filter:en:<slug>")
    revision = record.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError("E-FILTER-REVISION", "filter revision must be positive")
    criteria = _require_mapping(
        record.get("criteria"),
        "E-FILTER-CRITERIA",
        "filter criteria must be an object",
    )
    allowed = {"entity_types", "statuses", "domains", "updated", "evidence_roles"}
    unknown = set(criteria) - allowed
    if unknown:
        raise KernelError("E-FILTER-CRITERIA", f"unknown filter dimensions: {sorted(unknown)}")
    if not criteria:
        raise KernelError("E-FILTER-EMPTY", "filter must declare at least one dimension")
    entity_types = criteria.get("entity_types", [])
    if entity_types:
        values = _require_string_list(
            entity_types,
            "E-FILTER-TYPE",
            "entity_types must be unique strings",
        )
        available = {str(entity["type"]) for entity in repository.runtime["entities"]}
        if not set(values) <= available:
            raise KernelError("E-FILTER-TYPE", "filter contains unavailable entity type")
    statuses = criteria.get("statuses", [])
    if statuses:
        values = _require_string_list(
            statuses,
            "E-FILTER-STATUS",
            "statuses must be unique strings",
        )
        available = {
            str(entity["status"])
            for entity in repository.runtime["entities"]
            if entity.get("status") is not None
        }
        if not set(values) <= available:
            raise KernelError("E-FILTER-STATUS", "filter contains unavailable status")
    domains = criteria.get("domains", [])
    if domains:
        values = _require_string_list(
            domains,
            "E-FILTER-DOMAIN",
            "domains must be unique strings",
        )
        if not set(values) <= _available_domains(repository):
            raise KernelError("E-FILTER-DOMAIN", "filter contains unavailable domain key")
    roles = criteria.get("evidence_roles", [])
    if roles:
        values = _require_string_list(
            roles,
            "E-FILTER-EVIDENCE-ROLE",
            "evidence_roles must be unique strings",
        )
        if not set(values) <= EVIDENCE_ROLES:
            raise KernelError(
                "E-FILTER-EVIDENCE-ROLE",
                "filter contains unsupported evidence role",
            )
    updated = criteria.get("updated")
    if updated is not None:
        updated_record = _require_mapping(
            updated,
            "E-FILTER-DATE",
            "updated filter must be an object",
        )
        if set(updated_record) - {"from", "to"} or not updated_record:
            raise KernelError(
                "E-FILTER-DATE",
                "updated filter supports nonempty from and/or to bounds",
            )
        lower = _parse_date(updated_record["from"], "E-FILTER-DATE", "updated.from") if "from" in updated_record else None
        upper = _parse_date(updated_record["to"], "E-FILTER-DATE", "updated.to") if "to" in updated_record else None
        if lower and upper and lower > upper:
            raise KernelError("E-FILTER-DATE", "updated.from may not exceed updated.to")
    if (
        record.get("exact_revision_required") is not True
        or record.get("preserve_input_order") is not True
        or record.get("advisory_only") is not True
        or record.get("live") is not False
        or record.get("repository_mutation") is not False
    ):
        raise KernelError(
            "E-FILTER-AUTHORITY",
            "filter must preserve exact revisions, order, advisory authority, and non-mutation",
        )
    return {
        "contract": "atlas-retrieval-filter-validation/0.1",
        "id": filter_id,
        "revision": revision,
        "dimensions": sorted(criteria),
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }


def _matches_filter(entity: Mapping[str, Any], criteria: Mapping[str, Any]) -> bool:
    if criteria.get("entity_types") and entity["type"] not in criteria["entity_types"]:
        return False
    if criteria.get("statuses") and entity.get("status") not in criteria["statuses"]:
        return False
    if criteria.get("domains") and _entity_domain(entity) not in criteria["domains"]:
        return False
    if criteria.get("evidence_roles"):
        if not set(criteria["evidence_roles"]) <= set(_entity_evidence_roles(entity)):
            return False
    updated = criteria.get("updated")
    if updated:
        value = _entity_updated(entity)
        if value is None:
            return False
        entity_date = date.fromisoformat(value)
        if "from" in updated and entity_date < date.fromisoformat(updated["from"]):
            return False
        if "to" in updated and entity_date > date.fromisoformat(updated["to"]):
            return False
    return True


def apply_filter(
    record: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    validate_filter(record, repository)
    criteria = record["criteria"]
    items: list[dict[str, Any]] = []
    for entity in repository.runtime["entities"]:
        if not _matches_filter(entity, criteria):
            continue
        provenance_entities = repository.provenance_sources(
            str(entity["id"]), int(entity["revision"])
        )
        provenance = sorted(
            f"{item['id']}@{item['revision']}" for item in provenance_entities
        )
        if entity["type"] == "source" and not provenance:
            provenance = [str(entity["key"])]
        items.append(
            {
                "id": entity["id"],
                "revision": entity["revision"],
                "type": entity["type"],
                "title": entity.get("title"),
                "status": entity.get("status"),
                "staleness": entity.get("staleness"),
                "review_level": entity.get("review_level"),
                "domain": _entity_domain(entity),
                "updated": _entity_updated(entity),
                "evidence_roles": _entity_evidence_roles(entity),
                "provenance": provenance,
            }
        )
    result = {
        "contract": FILTER_RESULT_CONTRACT,
        "filter": {"id": record["id"], "revision": record["revision"]},
        "source_digest": repository.runtime["source_digest"],
        "entity_count_before": repository.runtime["entity_count"],
        "entity_count_after": len(items),
        "items": items,
        "exact_revision_preserved": True,
        "advisory_only": True,
        "live": False,
        "repository_mutation": False,
    }
    result["result_digest"] = _json_sha256(result)
    return result


def _query_map(query_set: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {str(query["id"]): query for query in query_set["queries"]}


def validate_trail(
    trail: Mapping[str, Any],
    repository: KernelRepository,
    query_set: Mapping[str, Any],
    filters: Mapping[str, Mapping[str, Any]],
    structured_baseline: Mapping[str, Any],
) -> dict[str, Any]:
    if trail.get("contract") != TRAIL_CONTRACT:
        raise KernelError("E-TRAIL-CONTRACT", f"expected {TRAIL_CONTRACT!r}")
    trail_id = trail.get("id")
    if not isinstance(trail_id, str) or not ID_RE.fullmatch(trail_id) or not trail_id.startswith("trail:"):
        raise KernelError("E-TRAIL-ID", "trail ID must be trail:en:<slug>")
    revision = trail.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError("E-TRAIL-REVISION", "trail revision must be positive")
    query_snapshot = _require_mapping(
        trail.get("query_snapshot"),
        "E-TRAIL-QUERY",
        "query_snapshot must be an object",
    )
    query_id = _require_string(
        query_snapshot.get("id"), "E-TRAIL-QUERY", "query snapshot requires ID"
    )
    queries = _query_map(query_set)
    if query_id not in queries:
        raise KernelError("E-TRAIL-QUERY", "trail references unavailable query")
    if query_snapshot.get("text") != queries[query_id]["text"]:
        raise KernelError("E-TRAIL-QUERY", "trail query text differs from accepted fixture")
    filter_ref = _require_mapping(
        trail.get("filter"),
        "E-TRAIL-FILTER",
        "trail filter reference must be an object",
    )
    filter_id = _require_string(
        filter_ref.get("id"), "E-TRAIL-FILTER", "trail filter requires ID"
    )
    if filter_id not in filters or filter_ref.get("revision") != filters[filter_id]["revision"]:
        raise KernelError("E-TRAIL-FILTER", "trail references unavailable filter revision")
    ranking = _require_mapping(
        trail.get("ranking_reference"),
        "E-TRAIL-RANKING",
        "ranking_reference must be an object",
    )
    expected_ranking = {
        "baseline_contract": structured_baseline["contract"],
        "index_contract": structured_baseline["index_contract"],
        "index_build_digest": structured_baseline["index_build_digest"],
        "result_set_sha256": structured_baseline["result_set_sha256"],
    }
    if ranking != expected_ranking:
        raise KernelError("E-TRAIL-RANKING", "trail ranking reference is not accepted structured evidence")
    entries = trail.get("entries")
    if not isinstance(entries, list) or not entries:
        raise KernelError("E-TRAIL-ENTRIES", "trail entries must be a nonempty list")
    seen: set[str] = set()
    filter_result_keys = {
        f"{item['id']}@{item['revision']}"
        for item in apply_filter(filters[filter_id], repository)["items"]
    }
    for entry in entries:
        entry_record = _require_mapping(
            entry, "E-TRAIL-ENTRY", "trail entry must be an object"
        )
        action = entry_record.get("action")
        if action not in TRAIL_ACTIONS:
            raise KernelError("E-TRAIL-ACTION", "trail action is unsupported")
        entity_id = _require_string(
            entry_record.get("id"), "E-TRAIL-ENTITY", "trail entry requires entity ID"
        )
        entity_revision = entry_record.get("revision")
        if not isinstance(entity_revision, int) or isinstance(entity_revision, bool):
            raise KernelError("E-TRAIL-ENTITY", "trail entry requires exact revision")
        repository.exact(entity_id, entity_revision)
        key = f"{entity_id}@{entity_revision}"
        if key in seen:
            raise KernelError("E-TRAIL-DUPLICATE", "trail may reference an exact entity only once")
        seen.add(key)
        if key not in filter_result_keys:
            raise KernelError("E-TRAIL-FILTER-MISMATCH", "trail entry is outside the saved filter snapshot")
        rank = entry_record.get("original_rank")
        if rank is not None and (
            not isinstance(rank, int) or isinstance(rank, bool) or rank < 1
        ):
            raise KernelError("E-TRAIL-RANK", "original_rank must be positive or null")
        _require_string(
            entry_record.get("rationale"),
            "E-TRAIL-RATIONALE",
            "trail entry requires rationale",
        )
    created = _parse_date(trail.get("created"), "E-TRAIL-DATE", "created")
    updated = _parse_date(trail.get("updated"), "E-TRAIL-DATE", "updated")
    if updated < created:
        raise KernelError("E-TRAIL-DATE", "trail updated date may not precede created")
    _require_string_list(
        trail.get("open_questions", []),
        "E-TRAIL-OPEN-QUESTIONS",
        "open_questions must be unique strings",
        allow_empty=True,
    )
    if (
        trail.get("authority") != "research-only"
        or trail.get("canonical_copy") is not False
        or trail.get("automatic_status_change") is not False
        or trail.get("exact_revision_required") is not True
        or trail.get("live") is not False
        or trail.get("repository_mutation") is not False
    ):
        raise KernelError(
            "E-TRAIL-AUTHORITY",
            "trail must remain research-only, exact-revision, non-copying, and non-mutating",
        )
    return {
        "contract": "atlas-research-trail-validation/0.1",
        "id": trail_id,
        "revision": revision,
        "entry_count": len(entries),
        "decision": "valid",
        "authority": "research-only",
        "live": False,
        "repository_mutation": False,
    }


def _validate_exact_ref(
    value: Any,
    repository: KernelRepository,
    code: str,
    field: str,
) -> str:
    record = _require_mapping(value, code, f"{field} must be an exact reference")
    entity_id = _require_string(record.get("id"), code, f"{field} requires entity ID")
    revision = record.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError(code, f"{field} requires positive revision")
    repository.exact(entity_id, revision)
    return f"{entity_id}@{revision}"


def _validate_candidate_common(
    candidate: Mapping[str, Any],
    repository: KernelRepository,
    expected_contract: str,
    expected_prefix: str,
) -> tuple[str, str, str]:
    if candidate.get("contract") != expected_contract:
        raise KernelError("E-CANDIDATE-CONTRACT", f"expected {expected_contract!r}")
    candidate_id = candidate.get("id")
    if (
        not isinstance(candidate_id, str)
        or not CANDIDATE_ID_RE.fullmatch(candidate_id)
        or not candidate_id.startswith(expected_prefix)
    ):
        raise KernelError("E-CANDIDATE-ID", "candidate ID has the wrong kind or syntax")
    left = _validate_exact_ref(candidate.get("left"), repository, "E-CANDIDATE-ENTITY", "left")
    right = _validate_exact_ref(candidate.get("right"), repository, "E-CANDIDATE-ENTITY", "right")
    if left == right:
        raise KernelError("E-CANDIDATE-PAIR", "candidate sides must be different exact entities")
    paths = candidate.get("evidence_paths")
    if not isinstance(paths, list) or not paths:
        raise KernelError("E-CANDIDATE-EVIDENCE", "candidate requires evidence paths")
    path_keys = [
        _validate_exact_ref(item, repository, "E-CANDIDATE-EVIDENCE", "evidence path")
        for item in paths
    ]
    if len(path_keys) != len(set(path_keys)):
        raise KernelError("E-CANDIDATE-EVIDENCE", "evidence paths may not repeat")
    _require_string(candidate.get("rationale"), "E-CANDIDATE-RATIONALE", "candidate requires rationale")
    if (
        candidate.get("advisory_only") is not True
        or candidate.get("exact_revision_required") is not True
        or candidate.get("live") is not False
        or candidate.get("repository_mutation") is not False
    ):
        raise KernelError(
            "E-CANDIDATE-AUTHORITY",
            "candidate must remain advisory, exact-revision, non-live, and non-mutating",
        )
    return candidate_id, left, right


def validate_contradiction_candidate(
    candidate: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    candidate_id, left, right = _validate_candidate_common(
        candidate,
        repository,
        CONTRADICTION_CONTRACT,
        "candidate:contradiction:",
    )
    _require_string_list(
        candidate.get("compared_statements"),
        "E-CONTRADICTION-STATEMENTS",
        "contradiction candidate requires compared statements",
    )
    _require_string_list(
        candidate.get("scope_analysis"),
        "E-CONTRADICTION-SCOPE",
        "contradiction candidate requires scope analysis",
    )
    if candidate.get("assessment") not in CONTRADICTION_ASSESSMENTS:
        raise KernelError("E-CONTRADICTION-ASSESSMENT", "unsupported contradiction assessment")
    if candidate.get("automatic_resolution") is not False:
        raise KernelError("E-CONTRADICTION-AUTHORITY", "automatic contradiction resolution is forbidden")
    return {
        "contract": "atlas-contradiction-candidate-validation/0.1",
        "id": candidate_id,
        "left": left,
        "right": right,
        "assessment": candidate["assessment"],
        "decision": "valid-candidate-not-proven-contradiction",
        "advisory_only": True,
    }


def validate_duplicate_candidate(
    candidate: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    candidate_id, left, right = _validate_candidate_common(
        candidate,
        repository,
        DUPLICATE_CONTRACT,
        "candidate:duplicate:",
    )
    _require_string_list(
        candidate.get("similarity_basis"),
        "E-DUPLICATE-SIMILARITY",
        "duplicate candidate requires similarity basis",
    )
    _require_string_list(
        candidate.get("semantic_differences"),
        "E-DUPLICATE-DIFFERENCES",
        "duplicate candidate requires semantic differences",
    )
    if candidate.get("assessment") not in DUPLICATE_ASSESSMENTS:
        raise KernelError("E-DUPLICATE-ASSESSMENT", "unsupported duplicate assessment")
    if candidate.get("automatic_merge") is not False:
        raise KernelError("E-DUPLICATE-AUTHORITY", "automatic duplicate merge is forbidden")
    return {
        "contract": "atlas-duplicate-candidate-validation/0.1",
        "id": candidate_id,
        "left": left,
        "right": right,
        "assessment": candidate["assessment"],
        "decision": "valid-candidate-not-proven-duplicate",
        "advisory_only": True,
    }


def _validate_negative_case(
    case: Mapping[str, Any],
    repository: KernelRepository,
    query_set: Mapping[str, Any],
    filters: Mapping[str, Mapping[str, Any]],
    structured_baseline: Mapping[str, Any],
) -> dict[str, Any]:
    case_id = _require_string(case.get("id"), "E-NEGATIVE-ID", "negative case requires ID")
    expected_error = _require_string(
        case.get("expected_error"),
        "E-NEGATIVE-EXPECTED",
        "negative case requires expected error",
    )
    kind = case.get("kind")
    record = _require_mapping(case.get("record"), "E-NEGATIVE-RECORD", "negative case requires record")
    try:
        if kind == "filter":
            validate_filter(record, repository)
        elif kind == "trail":
            validate_trail(record, repository, query_set, filters, structured_baseline)
        elif kind == "contradiction":
            validate_contradiction_candidate(record, repository)
        elif kind == "duplicate":
            validate_duplicate_candidate(record, repository)
        else:
            raise KernelError("E-NEGATIVE-KIND", "unknown negative case kind")
    except KernelError as exc:
        if exc.code != expected_error:
            raise KernelError(
                "E-NEGATIVE-MISMATCH",
                f"negative case {case_id} expected {expected_error}, got {exc.code}",
            ) from exc
        return {"id": case_id, "kind": kind, "observed_error": exc.code, "decision": "expected-failure"}
    raise KernelError("E-NEGATIVE-PASSED", f"negative case {case_id} unexpectedly passed")


def validate_fixture_bundle(
    bundle: Mapping[str, Any],
    repository: KernelRepository,
    query_set: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    validate_query_set(query_set, repository)
    if bundle.get("contract") != FIXTURE_CONTRACT:
        raise KernelError("E-RESEARCH-FIXTURE-CONTRACT", f"expected {FIXTURE_CONTRACT!r}")
    if bundle.get("mode") != MODE:
        raise KernelError("E-RESEARCH-FIXTURE-MODE", f"mode must be {MODE!r}")
    if (
        bundle.get("source_digest") != repository.runtime["source_digest"]
        or bundle.get("entity_count") != repository.runtime["entity_count"]
        or bundle.get("query_set") != {"id": query_set["id"], "version": query_set["version"]}
    ):
        raise KernelError("E-RESEARCH-FIXTURE-IDENTITY", "fixture identity mismatch")
    if structured_baseline.get("contract") != STRUCTURED_BASELINE_CONTRACT:
        raise KernelError("E-RESEARCH-STRUCTURED-BASELINE", "accepted structured baseline required")
    if bundle.get("structured_baseline_sha256") != _json_sha256(structured_baseline):
        raise KernelError("E-RESEARCH-STRUCTURED-BASELINE", "structured baseline digest mismatch")
    filters_raw = bundle.get("filters")
    if not isinstance(filters_raw, list) or not filters_raw:
        raise KernelError("E-RESEARCH-FILTERS", "fixture bundle requires filters")
    filters: dict[str, Mapping[str, Any]] = {}
    filter_results: list[dict[str, Any]] = []
    filter_validations: list[dict[str, Any]] = []
    for record in filters_raw:
        filter_record = _require_mapping(record, "E-RESEARCH-FILTER", "filter fixture must be an object")
        validation = validate_filter(filter_record, repository)
        if validation["id"] in filters:
            raise KernelError("E-RESEARCH-FILTER-DUPLICATE", "duplicate filter ID")
        filters[validation["id"]] = filter_record
        result = apply_filter(filter_record, repository)
        expected_keys = filter_record.get("expected_keys")
        if expected_keys is not None:
            expected = _require_string_list(
                expected_keys,
                "E-FILTER-EXPECTED",
                "expected_keys must be unique exact keys",
                allow_empty=True,
            )
            actual = [f"{item['id']}@{item['revision']}" for item in result["items"]]
            if actual != expected:
                raise KernelError(
                    "E-FILTER-EXPECTED",
                    f"filter {validation['id']} result differs from expected exact keys",
                )
        filter_validations.append(validation)
        filter_results.append(result)
    trails_raw = bundle.get("trails")
    if not isinstance(trails_raw, list) or not trails_raw:
        raise KernelError("E-RESEARCH-TRAILS", "fixture bundle requires trails")
    trail_validations = [
        validate_trail(
            _require_mapping(item, "E-RESEARCH-TRAIL", "trail fixture must be an object"),
            repository,
            query_set,
            filters,
            structured_baseline,
        )
        for item in trails_raw
    ]
    contradictions_raw = bundle.get("contradiction_candidates")
    if not isinstance(contradictions_raw, list) or not contradictions_raw:
        raise KernelError("E-RESEARCH-CONTRADICTIONS", "fixture bundle requires contradiction candidates")
    contradiction_validations = [
        validate_contradiction_candidate(
            _require_mapping(item, "E-RESEARCH-CONTRADICTION", "candidate must be an object"),
            repository,
        )
        for item in contradictions_raw
    ]
    duplicates_raw = bundle.get("duplicate_candidates")
    if not isinstance(duplicates_raw, list) or not duplicates_raw:
        raise KernelError("E-RESEARCH-DUPLICATES", "fixture bundle requires duplicate candidates")
    duplicate_validations = [
        validate_duplicate_candidate(
            _require_mapping(item, "E-RESEARCH-DUPLICATE", "candidate must be an object"),
            repository,
        )
        for item in duplicates_raw
    ]
    negative_raw = bundle.get("negative_cases")
    if not isinstance(negative_raw, list) or not negative_raw:
        raise KernelError("E-RESEARCH-NEGATIVES", "fixture bundle requires negative cases")
    negative_validations = [
        _validate_negative_case(
            _require_mapping(item, "E-RESEARCH-NEGATIVE", "negative case must be an object"),
            repository,
            query_set,
            filters,
            structured_baseline,
        )
        for item in negative_raw
    ]
    if (
        bundle.get("advisory_only") is not True
        or bundle.get("automatic_merge_or_resolution") is not False
        or bundle.get("canonical_copy_authority") is not False
        or bundle.get("live") is not False
        or bundle.get("repository_mutation") is not False
    ):
        raise KernelError(
            "E-RESEARCH-AUTHORITY",
            "fixture bundle must remain advisory, non-copying, non-live, and non-mutating",
        )
    report = {
        "contract": REPORT_CONTRACT,
        "mode": MODE,
        "decision": "research-foundation-candidate",
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "query_set_id": query_set["id"],
        "query_set_version": query_set["version"],
        "structured_baseline_sha256": _json_sha256(structured_baseline),
        "filter_validations": filter_validations,
        "filter_result_digests": [result["result_digest"] for result in filter_results],
        "trail_validations": trail_validations,
        "contradiction_validations": contradiction_validations,
        "duplicate_validations": duplicate_validations,
        "negative_validations": negative_validations,
        "counts": {
            "filters": len(filter_validations),
            "filter_result_items": sum(result["entity_count_after"] for result in filter_results),
            "trails": len(trail_validations),
            "trail_entries": sum(item["entry_count"] for item in trail_validations),
            "contradiction_candidates": len(contradiction_validations),
            "duplicate_candidates": len(duplicate_validations),
            "negative_cases": len(negative_validations),
        },
        "exact_revision_preserved": True,
        "provenance_visible": True,
        "review_and_staleness_visible": True,
        "candidate_authority": "advisory-only",
        "automatic_merge_or_resolution": False,
        "canonical_copy_authority": False,
        "embeddings": False,
        "vector_database": False,
        "external_services": False,
        "live": False,
        "repository_mutation": False,
    }
    report["report_digest"] = _json_sha256(report)
    return report, filter_results


def _write(path: Path | None, value: Mapping[str, Any] | Sequence[Mapping[str, Any]]) -> None:
    if isinstance(value, Mapping):
        rendered = render_json(value)
    else:
        rendered = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if path is None:
        sys.stdout.write(rendered)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    print(f"wrote={path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--query-set",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/reference-query-set.v01.json"),
    )
    parser.add_argument(
        "--structured-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/structured-baseline.json"),
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/research-foundations.v01.json"),
    )
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--filter-results-output", type=Path)
    args = parser.parse_args(argv)
    try:
        runtime = compile_canonical(args.canonical_root)
        repository = KernelRepository(runtime)
        query_set = load_json(args.query_set)
        structured_baseline = load_json(args.structured_baseline)
        fixtures = load_json(args.fixtures)
        report, filter_results = validate_fixture_bundle(
            fixtures,
            repository,
            query_set,
            structured_baseline,
        )
        if args.report_output is None and args.filter_results_output is None:
            _write(None, report)
        else:
            if args.report_output is not None:
                _write(args.report_output, report)
            if args.filter_results_output is not None:
                _write(args.filter_results_output, filter_results)
        return 0
    except (KernelError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
