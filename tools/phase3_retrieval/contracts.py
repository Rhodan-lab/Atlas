#!/usr/bin/env python3
"""Phase 3 retrieval evaluation contracts and fixture validation."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any, Mapping

from tools.phase2_kernel import (
    KernelError,
    KernelRepository,
    compile_canonical,
    load_json,
    render_json,
)

QUERY_SET_CONTRACT = "atlas-retrieval-query-set/0.1"
RESULT_SET_CONTRACT = "atlas-retrieval-result-set/0.1"
METRIC_REPORT_CONTRACT = "atlas-retrieval-metric-report/0.1"
VALIDATION_REPORT_CONTRACT = "atlas-retrieval-contract-validation/0.1"
MODE = "retrieval-evaluation"
QUERY_ID_RE = re.compile(r"^query:retrieval:[a-z0-9]+(?:-[a-z0-9]+)*$")
QUERY_SET_ID_RE = re.compile(r"^retrieval-query-set:[a-z0-9]+(?:-[a-z0-9]+)*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SLICES = {"catalase", "feedback", "recommenders", "cross-slice"}
DIFFICULTIES = {"direct", "compositional", "ambiguous", "exact-revision-error"}
AMBIGUITY_STATUSES = {"needs-scope", "contested-normative", "multi-intent"}
METRIC_NAMES = {
    "precision_at_k",
    "recall_at_k",
    "mean_reciprocal_rank",
    "ndcg_at_k",
    "zero_result_rate",
    "unavailable_revision_rate",
}


def _mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def _list(value: Any, code: str, message: str) -> list[Any]:
    if not isinstance(value, list):
        raise KernelError(code, message)
    return value


def _nonempty_string(value: Any, code: str, message: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KernelError(code, message)
    return value


def _positive_int(value: Any, code: str, message: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise KernelError(code, message)
    return value


def _exact_key(entity_id: str, revision: int) -> str:
    return f"{entity_id}@{revision}"


def _parse_exact_key(value: Any, code: str) -> tuple[str, int]:
    text = _nonempty_string(value, code, "exact entity key must be a string")
    if "@" not in text:
        raise KernelError(code, f"exact entity key {text!r} must include @REVISION")
    entity_id, revision_text = text.rsplit("@", 1)
    try:
        revision = int(revision_text)
    except ValueError as exc:
        raise KernelError(code, f"exact entity key {text!r} has invalid revision") from exc
    return entity_id, _positive_int(revision, code, "revision must be positive")


def _query_map(payload: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    queries = _list(
        payload.get("queries"),
        "E-RETRIEVAL-QUERY-SET",
        "queries must be a list",
    )
    result: dict[str, Mapping[str, Any]] = {}
    for raw in queries:
        query = _mapping(raw, "E-RETRIEVAL-QUERY", "query must be an object")
        query_id = _nonempty_string(
            query.get("id"),
            "E-RETRIEVAL-QUERY-ID",
            "query id is required",
        )
        if not QUERY_ID_RE.fullmatch(query_id):
            raise KernelError(
                "E-RETRIEVAL-QUERY-ID",
                f"invalid retrieval query id {query_id!r}",
            )
        if query_id in result:
            raise KernelError(
                "E-RETRIEVAL-QUERY-DUPLICATE",
                f"duplicate retrieval query id {query_id!r}",
            )
        result[query_id] = query
    return result


def validate_query_set(
    payload: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    if payload.get("contract") != QUERY_SET_CONTRACT:
        raise KernelError(
            "E-RETRIEVAL-QUERY-CONTRACT",
            f"expected {QUERY_SET_CONTRACT!r}, got {payload.get('contract')!r}",
        )
    query_set_id = _nonempty_string(
        payload.get("id"),
        "E-RETRIEVAL-QUERY-SET-ID",
        "query-set id is required",
    )
    if not QUERY_SET_ID_RE.fullmatch(query_set_id):
        raise KernelError(
            "E-RETRIEVAL-QUERY-SET-ID",
            f"invalid query-set id {query_set_id!r}",
        )
    version = _positive_int(
        payload.get("version"),
        "E-RETRIEVAL-QUERY-VERSION",
        "query-set version must be positive",
    )
    if payload.get("language") != "en":
        raise KernelError(
            "E-RETRIEVAL-QUERY-LANGUAGE",
            "the active Phase 3 fixture set must be English",
        )
    if payload.get("mode") != MODE:
        raise KernelError(
            "E-RETRIEVAL-QUERY-MODE",
            f"query-set mode must be {MODE!r}",
        )
    if payload.get("live") is not False or payload.get("repository_mutation") is not False:
        raise KernelError(
            "E-RETRIEVAL-QUERY-AUTHORITY",
            "query fixtures must remain live=false and repository_mutation=false",
        )
    if payload.get("corpus_contract") != repository.runtime.get("source_contract"):
        raise KernelError(
            "E-RETRIEVAL-QUERY-CORPUS",
            "query-set corpus contract does not match the compiled runtime",
        )
    entity_count = int(repository.runtime.get("entity_count", 0))
    if payload.get("corpus_entity_count") != entity_count:
        raise KernelError(
            "E-RETRIEVAL-QUERY-CORPUS",
            f"expected corpus_entity_count {entity_count}",
        )

    policy = _mapping(
        payload.get("judgment_policy"),
        "E-RETRIEVAL-JUDGMENT-POLICY",
        "judgment_policy must be an object",
    )
    if policy.get("authority") != "evaluation-only":
        raise KernelError(
            "E-RETRIEVAL-JUDGMENT-AUTHORITY",
            "retrieval judgments must have evaluation-only authority",
        )
    if policy.get("grade_scale") != [0, 1, 2, 3]:
        raise KernelError(
            "E-RETRIEVAL-JUDGMENT-SCALE",
            "grade_scale must be [0, 1, 2, 3]",
        )
    if policy.get("unlisted_grade") != 0:
        raise KernelError(
            "E-RETRIEVAL-JUDGMENT-SCALE",
            "unlisted exact entities must receive grade 0",
        )
    if policy.get("exhaustive_over_pinned_corpus") is not True:
        raise KernelError(
            "E-RETRIEVAL-JUDGMENT-POLICY",
            "the pinned 34-entity corpus must be judged exhaustively",
        )

    minimums = _mapping(
        payload.get("minimum_queries_per_slice"),
        "E-RETRIEVAL-QUERY-COVERAGE",
        "minimum_queries_per_slice must be an object",
    )
    required_slices = _list(
        payload.get("required_slices"),
        "E-RETRIEVAL-QUERY-COVERAGE",
        "required_slices must be a list",
    )
    if set(required_slices) != SLICES:
        raise KernelError(
            "E-RETRIEVAL-QUERY-COVERAGE",
            f"required_slices must equal {sorted(SLICES)}",
        )

    queries = _query_map(payload)
    if not queries:
        raise KernelError("E-RETRIEVAL-QUERY-SET", "query set cannot be empty")

    slice_counts = {name: 0 for name in sorted(SLICES)}
    difficulty_counts = {name: 0 for name in sorted(DIFFICULTIES)}
    ranked_count = 0
    error_count = 0
    judged_exact_count = 0

    for query_id, query in queries.items():
        _nonempty_string(
            query.get("text"),
            "E-RETRIEVAL-QUERY-TEXT",
            f"{query_id} requires query text",
        )
        _nonempty_string(
            query.get("intent"),
            "E-RETRIEVAL-QUERY-INTENT",
            f"{query_id} requires an information-need statement",
        )
        slice_name = query.get("slice")
        difficulty = query.get("difficulty")
        if slice_name not in SLICES:
            raise KernelError(
                "E-RETRIEVAL-QUERY-SLICE",
                f"{query_id} has invalid slice {slice_name!r}",
            )
        if difficulty not in DIFFICULTIES:
            raise KernelError(
                "E-RETRIEVAL-QUERY-DIFFICULTY",
                f"{query_id} has invalid difficulty {difficulty!r}",
            )
        slice_counts[str(slice_name)] += 1
        difficulty_counts[str(difficulty)] += 1

        ambiguity = query.get("ambiguity")
        if difficulty == "ambiguous":
            ambiguity_record = _mapping(
                ambiguity,
                "E-RETRIEVAL-QUERY-AMBIGUITY",
                f"{query_id} requires an ambiguity record",
            )
            if ambiguity_record.get("status") not in AMBIGUITY_STATUSES:
                raise KernelError(
                    "E-RETRIEVAL-QUERY-AMBIGUITY",
                    f"{query_id} has invalid ambiguity status",
                )
            _nonempty_string(
                ambiguity_record.get("note"),
                "E-RETRIEVAL-QUERY-AMBIGUITY",
                f"{query_id} requires an ambiguity note",
            )
        elif ambiguity is not None:
            raise KernelError(
                "E-RETRIEVAL-QUERY-AMBIGUITY",
                f"{query_id} may declare ambiguity only when difficulty=ambiguous",
            )

        expected = _mapping(
            query.get("expected"),
            "E-RETRIEVAL-EXPECTATION",
            f"{query_id} requires an expected outcome",
        )
        kind = expected.get("kind")
        if kind == "ranked":
            if difficulty == "exact-revision-error":
                raise KernelError(
                    "E-RETRIEVAL-EXPECTATION",
                    f"{query_id} error difficulty cannot expect ranked results",
                )
            judgments = _list(
                expected.get("judgments"),
                "E-RETRIEVAL-JUDGMENT",
                f"{query_id} judgments must be a list",
            )
            if not judgments:
                raise KernelError(
                    "E-RETRIEVAL-JUDGMENT",
                    f"{query_id} requires at least one positive judgment",
                )
            seen_exact: set[str] = set()
            grades: list[int] = []
            for raw_judgment in judgments:
                judgment = _mapping(
                    raw_judgment,
                    "E-RETRIEVAL-JUDGMENT",
                    f"{query_id} judgment must be an object",
                )
                entity_id = _nonempty_string(
                    judgment.get("id"),
                    "E-RETRIEVAL-JUDGMENT-ENTITY",
                    f"{query_id} judgment id is required",
                )
                revision = _positive_int(
                    judgment.get("revision"),
                    "E-RETRIEVAL-JUDGMENT-REVISION",
                    f"{query_id} judgment revision must be positive",
                )
                grade = judgment.get("grade")
                if (
                    not isinstance(grade, int)
                    or isinstance(grade, bool)
                    or grade not in {1, 2, 3}
                ):
                    raise KernelError(
                        "E-RETRIEVAL-JUDGMENT-GRADE",
                        f"{query_id} positive judgment grade must be 1, 2, or 3",
                    )
                _nonempty_string(
                    judgment.get("rationale"),
                    "E-RETRIEVAL-JUDGMENT-RATIONALE",
                    f"{query_id} judgment requires a rationale",
                )
                key = _exact_key(entity_id, revision)
                if key in seen_exact:
                    raise KernelError(
                        "E-RETRIEVAL-JUDGMENT-DUPLICATE",
                        f"{query_id} repeats judgment {key}",
                    )
                seen_exact.add(key)
                repository.exact(entity_id, revision)
                grades.append(grade)
            if 3 not in grades:
                raise KernelError(
                    "E-RETRIEVAL-JUDGMENT-GRADE",
                    f"{query_id} requires at least one grade-3 target",
                )
            ranked_count += 1
            judged_exact_count += len(judgments)
        elif kind == "error":
            if difficulty != "exact-revision-error":
                raise KernelError(
                    "E-RETRIEVAL-EXPECTATION",
                    f"{query_id} error expectation requires exact-revision-error difficulty",
                )
            target = _mapping(
                expected.get("target"),
                "E-RETRIEVAL-ERROR-TARGET",
                f"{query_id} requires an error target",
            )
            entity_id = _nonempty_string(
                target.get("id"),
                "E-RETRIEVAL-ERROR-TARGET",
                f"{query_id} target id is required",
            )
            revision = _positive_int(
                target.get("revision"),
                "E-RETRIEVAL-ERROR-TARGET",
                f"{query_id} target revision must be positive",
            )
            error = expected.get("error")
            if error not in {"E-REVISION-MISSING", "E-ENTITY-MISSING"}:
                raise KernelError(
                    "E-RETRIEVAL-ERROR-CODE",
                    f"{query_id} has unsupported expected error {error!r}",
                )
            try:
                repository.exact(entity_id, revision)
            except KernelError as exc:
                if exc.code != error:
                    raise KernelError(
                        "E-RETRIEVAL-ERROR-CODE",
                        f"{query_id} expected {error}, observed {exc.code}",
                    ) from exc
            else:
                raise KernelError(
                    "E-RETRIEVAL-ERROR-TARGET",
                    f"{query_id} target unexpectedly exists",
                )
            available = repository.available_revisions(entity_id)
            if expected.get("available_revisions") != available:
                raise KernelError(
                    "E-RETRIEVAL-ERROR-REVISIONS",
                    f"{query_id} available revisions must equal {available}",
                )
            error_count += 1
        else:
            raise KernelError(
                "E-RETRIEVAL-EXPECTATION",
                f"{query_id} has invalid expectation kind {kind!r}",
            )

    for slice_name in sorted(SLICES):
        minimum = minimums.get(slice_name)
        if not isinstance(minimum, int) or isinstance(minimum, bool) or minimum < 0:
            raise KernelError(
                "E-RETRIEVAL-QUERY-COVERAGE",
                f"minimum for {slice_name} must be a nonnegative integer",
            )
        if slice_counts[slice_name] < minimum:
            raise KernelError(
                "E-RETRIEVAL-QUERY-COVERAGE",
                f"slice {slice_name} has {slice_counts[slice_name]} queries, requires {minimum}",
            )
    if any(difficulty_counts[name] == 0 for name in DIFFICULTIES):
        raise KernelError(
            "E-RETRIEVAL-QUERY-COVERAGE",
            "query set must cover every declared difficulty",
        )

    implicit_nonrelevant = ranked_count * entity_count - judged_exact_count
    return {
        "contract": VALIDATION_REPORT_CONTRACT,
        "validated_contract": QUERY_SET_CONTRACT,
        "query_set_id": query_set_id,
        "query_set_version": version,
        "source_digest": repository.runtime["source_digest"],
        "entity_count": entity_count,
        "query_count": len(queries),
        "ranked_query_count": ranked_count,
        "expected_error_query_count": error_count,
        "positive_judgment_count": judged_exact_count,
        "implicit_nonrelevant_judgment_count": implicit_nonrelevant,
        "slice_counts": slice_counts,
        "difficulty_counts": difficulty_counts,
        "decision": "valid",
        "judgment_authority": "evaluation-only",
        "live": False,
        "repository_mutation": False,
    }


def validate_result_set(
    payload: Mapping[str, Any],
    query_set: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    query_report = validate_query_set(query_set, repository)
    if payload.get("contract") != RESULT_SET_CONTRACT:
        raise KernelError(
            "E-RETRIEVAL-RESULT-CONTRACT",
            f"expected {RESULT_SET_CONTRACT!r}, got {payload.get('contract')!r}",
        )
    if (
        payload.get("query_set_id") != query_report["query_set_id"]
        or payload.get("query_set_version") != query_report["query_set_version"]
    ):
        raise KernelError(
            "E-RETRIEVAL-RESULT-QUERY-SET",
            "result set does not bind the exact query-set id and version",
        )
    if payload.get("advisory_only") is not True:
        raise KernelError(
            "E-RETRIEVAL-RESULT-AUTHORITY",
            "retrieval results must remain advisory_only=true",
        )
    if payload.get("live") is not False or payload.get("repository_mutation") is not False:
        raise KernelError(
            "E-RETRIEVAL-RESULT-AUTHORITY",
            "result set must remain live=false and repository_mutation=false",
        )
    index = _mapping(
        payload.get("index"),
        "E-RETRIEVAL-INDEX",
        "result set requires an index record",
    )
    _nonempty_string(
        index.get("contract"),
        "E-RETRIEVAL-INDEX",
        "index contract is required",
    )
    for field in ("build_digest", "source_digest"):
        digest = index.get(field)
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            raise KernelError(
                "E-RETRIEVAL-INDEX-DIGEST",
                f"index {field} must be a lowercase SHA-256",
            )
    if index.get("source_digest") != repository.runtime.get("source_digest"):
        raise KernelError(
            "E-RETRIEVAL-INDEX-DIGEST",
            "index source_digest does not match canonical runtime",
        )
    if index.get("replaceable") is not True or index.get("canonical_mutation") is not False:
        raise KernelError(
            "E-RETRIEVAL-INDEX-AUTHORITY",
            "retrieval index must be replaceable and canonical_mutation=false",
        )

    query_map = _query_map(query_set)
    responses = _list(
        payload.get("responses"),
        "E-RETRIEVAL-RESPONSE",
        "responses must be a list",
    )
    by_query: dict[str, Mapping[str, Any]] = {}
    result_item_count = 0
    zero_result_count = 0
    tie_count = 0

    for raw in responses:
        response = _mapping(raw, "E-RETRIEVAL-RESPONSE", "response must be an object")
        query_id = _nonempty_string(
            response.get("query_id"),
            "E-RETRIEVAL-RESPONSE-QUERY",
            "response query_id is required",
        )
        if query_id not in query_map:
            raise KernelError(
                "E-RETRIEVAL-RESPONSE-QUERY",
                f"response references unknown query {query_id!r}",
            )
        if query_id in by_query:
            raise KernelError(
                "E-RETRIEVAL-RESPONSE-DUPLICATE",
                f"duplicate response for query {query_id!r}",
            )
        by_query[query_id] = response

        expected = _mapping(
            query_map[query_id].get("expected"),
            "E-RETRIEVAL-EXPECTATION",
            "query expectation is malformed",
        )
        expected_kind = expected.get("kind")
        outcome = response.get("outcome")
        if expected_kind == "error":
            if outcome != "error":
                raise KernelError(
                    "E-RETRIEVAL-RESPONSE-OUTCOME",
                    f"{query_id} must return the expected error",
                )
            if response.get("error") != expected.get("error"):
                raise KernelError(
                    "E-RETRIEVAL-RESPONSE-ERROR",
                    f"{query_id} returned the wrong error code",
                )
            if response.get("target") != expected.get("target"):
                raise KernelError(
                    "E-RETRIEVAL-RESPONSE-ERROR",
                    f"{query_id} returned the wrong error target",
                )
            if "items" in response:
                raise KernelError(
                    "E-RETRIEVAL-RESPONSE-ERROR",
                    f"{query_id} error response cannot contain ranked items",
                )
            continue

        if outcome != "ranked":
            raise KernelError(
                "E-RETRIEVAL-RESPONSE-OUTCOME",
                f"{query_id} must return ranked results",
            )
        items = _list(
            response.get("items"),
            "E-RETRIEVAL-RESULT-ITEM",
            f"{query_id} items must be a list",
        )
        if not items:
            zero_result_count += 1
        seen_keys: set[str] = set()
        previous_score: float | None = None
        previous_key: str | None = None
        for index_position, raw_item in enumerate(items, start=1):
            item = _mapping(
                raw_item,
                "E-RETRIEVAL-RESULT-ITEM",
                f"{query_id} result item must be an object",
            )
            if item.get("rank") != index_position:
                raise KernelError(
                    "E-RETRIEVAL-RESULT-RANK",
                    f"{query_id} ranks must be consecutive from 1",
                )
            score = item.get("score")
            if (
                not isinstance(score, (int, float))
                or isinstance(score, bool)
                or not math.isfinite(float(score))
            ):
                raise KernelError(
                    "E-RETRIEVAL-RESULT-SCORE",
                    f"{query_id} result score must be finite",
                )
            entity_id = _nonempty_string(
                item.get("id"),
                "E-RETRIEVAL-RESULT-ENTITY",
                f"{query_id} result id is required",
            )
            revision = _positive_int(
                item.get("revision"),
                "E-RETRIEVAL-RESULT-REVISION",
                f"{query_id} result requires a positive exact revision",
            )
            key = _exact_key(entity_id, revision)
            if key in seen_keys:
                raise KernelError(
                    "E-RETRIEVAL-RESULT-DUPLICATE",
                    f"{query_id} repeats result {key}",
                )
            seen_keys.add(key)
            entity = repository.exact(entity_id, revision)
            for field in ("type", "title", "status", "staleness", "review_level"):
                if item.get(field) != entity.get(field):
                    raise KernelError(
                        "E-RETRIEVAL-RESULT-METADATA",
                        f"{query_id} result {key} disagrees on {field}",
                    )
            matched_fields = _list(
                item.get("matched_fields"),
                "E-RETRIEVAL-RESULT-EVIDENCE",
                f"{query_id} result {key} matched_fields must be a list",
            )
            if (
                not matched_fields
                or matched_fields != sorted(set(matched_fields))
                or not all(isinstance(value, str) and value for value in matched_fields)
            ):
                raise KernelError(
                    "E-RETRIEVAL-RESULT-EVIDENCE",
                    f"{query_id} result {key} matched_fields must be sorted and unique",
                )
            _nonempty_string(
                item.get("explanation"),
                "E-RETRIEVAL-RESULT-EVIDENCE",
                f"{query_id} result {key} requires an explanation",
            )
            provenance = _list(
                item.get("provenance"),
                "E-RETRIEVAL-RESULT-PROVENANCE",
                f"{query_id} result {key} provenance must be a list",
            )
            if provenance != sorted(set(provenance)):
                raise KernelError(
                    "E-RETRIEVAL-RESULT-PROVENANCE",
                    f"{query_id} result {key} provenance must be sorted and unique",
                )
            for exact in provenance:
                provenance_id, provenance_revision = _parse_exact_key(
                    exact,
                    "E-RETRIEVAL-RESULT-PROVENANCE",
                )
                repository.exact(provenance_id, provenance_revision)

            numeric_score = float(score)
            if previous_score is not None:
                if numeric_score > previous_score:
                    raise KernelError(
                        "E-RETRIEVAL-RESULT-ORDER",
                        f"{query_id} scores must be non-increasing",
                    )
                if numeric_score == previous_score:
                    tie_count += 1
                    if previous_key is not None and key < previous_key:
                        raise KernelError(
                            "E-RETRIEVAL-RESULT-TIE",
                            f"{query_id} equal-score ties must use ascending exact keys",
                        )
            previous_score = numeric_score
            previous_key = key
            result_item_count += 1

    if set(by_query) != set(query_map):
        missing = sorted(set(query_map) - set(by_query))
        extra = sorted(set(by_query) - set(query_map))
        raise KernelError(
            "E-RETRIEVAL-RESPONSE-COVERAGE",
            f"responses must cover every query exactly; missing={missing}, extra={extra}",
        )

    return {
        "contract": VALIDATION_REPORT_CONTRACT,
        "validated_contract": RESULT_SET_CONTRACT,
        "query_set_id": query_report["query_set_id"],
        "query_set_version": query_report["query_set_version"],
        "response_count": len(responses),
        "result_item_count": result_item_count,
        "zero_result_count": zero_result_count,
        "tie_count": tie_count,
        "decision": "valid",
        "advisory_only": True,
        "live": False,
        "repository_mutation": False,
    }


def validate_metric_report(
    payload: Mapping[str, Any],
    query_set: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    query_report = validate_query_set(query_set, repository)
    if payload.get("contract") != METRIC_REPORT_CONTRACT:
        raise KernelError(
            "E-RETRIEVAL-METRIC-CONTRACT",
            f"expected {METRIC_REPORT_CONTRACT!r}, got {payload.get('contract')!r}",
        )
    if (
        payload.get("query_set_id") != query_report["query_set_id"]
        or payload.get("query_set_version") != query_report["query_set_version"]
    ):
        raise KernelError(
            "E-RETRIEVAL-METRIC-QUERY-SET",
            "metric report does not bind the exact query set",
        )
    digest = payload.get("result_set_sha256")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        raise KernelError(
            "E-RETRIEVAL-METRIC-DIGEST",
            "result_set_sha256 must be a lowercase SHA-256",
        )
    cutoff = _positive_int(
        payload.get("cutoff"),
        "E-RETRIEVAL-METRIC-CUTOFF",
        "metric cutoff must be positive",
    )
    if payload.get("evaluated_ranked_queries") != query_report["ranked_query_count"]:
        raise KernelError(
            "E-RETRIEVAL-METRIC-COVERAGE",
            "evaluated_ranked_queries does not match the query set",
        )
    if payload.get("expected_error_queries") != query_report["expected_error_query_count"]:
        raise KernelError(
            "E-RETRIEVAL-METRIC-COVERAGE",
            "expected_error_queries does not match the query set",
        )
    metrics = _mapping(
        payload.get("metrics"),
        "E-RETRIEVAL-METRIC",
        "metrics must be an object",
    )
    if set(metrics) != METRIC_NAMES:
        raise KernelError(
            "E-RETRIEVAL-METRIC",
            f"metrics must contain exactly {sorted(METRIC_NAMES)}",
        )
    for name in sorted(METRIC_NAMES):
        value = metrics[name]
        if (
            not isinstance(value, (int, float))
            or isinstance(value, bool)
            or not math.isfinite(float(value))
            or not 0.0 <= float(value) <= 1.0
        ):
            raise KernelError(
                "E-RETRIEVAL-METRIC-RANGE",
                f"metric {name} must be finite and within [0, 1]",
            )
    tie_count = payload.get("tie_count")
    if not isinstance(tie_count, int) or isinstance(tie_count, bool) or tie_count < 0:
        raise KernelError(
            "E-RETRIEVAL-METRIC-TIES",
            "tie_count must be a nonnegative integer",
        )
    if payload.get("advisory_only") is not True:
        raise KernelError(
            "E-RETRIEVAL-METRIC-AUTHORITY",
            "metric reports must remain advisory_only=true",
        )
    if payload.get("live") is not False or payload.get("repository_mutation") is not False:
        raise KernelError(
            "E-RETRIEVAL-METRIC-AUTHORITY",
            "metric report must remain live=false and repository_mutation=false",
        )
    return {
        "contract": VALIDATION_REPORT_CONTRACT,
        "validated_contract": METRIC_REPORT_CONTRACT,
        "query_set_id": query_report["query_set_id"],
        "query_set_version": query_report["query_set_version"],
        "cutoff": cutoff,
        "metric_count": len(metrics),
        "tie_count": tie_count,
        "decision": "valid",
        "advisory_only": True,
        "live": False,
        "repository_mutation": False,
    }


def _write_or_print(report: Mapping[str, Any], output: Path | None) -> None:
    rendered = render_json(report)
    if output is None:
        sys.stdout.write(rendered)
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f"wrote={output}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--canonical-root",
        type=Path,
        default=Path("content/canonical"),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    query_parser = subparsers.add_parser("validate-query-set")
    query_parser.add_argument("--query-set", type=Path, required=True)
    query_parser.add_argument("--output", type=Path)

    result_parser = subparsers.add_parser("validate-result-set")
    result_parser.add_argument("--query-set", type=Path, required=True)
    result_parser.add_argument("--result-set", type=Path, required=True)
    result_parser.add_argument("--output", type=Path)

    metric_parser = subparsers.add_parser("validate-metric-report")
    metric_parser.add_argument("--query-set", type=Path, required=True)
    metric_parser.add_argument("--metric-report", type=Path, required=True)
    metric_parser.add_argument("--output", type=Path)

    args = parser.parse_args(argv)
    try:
        repository = KernelRepository(compile_canonical(args.canonical_root))
        query_set = load_json(args.query_set)
        if args.command == "validate-query-set":
            report = validate_query_set(query_set, repository)
        elif args.command == "validate-result-set":
            report = validate_result_set(
                load_json(args.result_set),
                query_set,
                repository,
            )
        else:
            report = validate_metric_report(
                load_json(args.metric_report),
                query_set,
                repository,
            )
        _write_or_print(report, args.output)
        return 0
    except (KernelError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
