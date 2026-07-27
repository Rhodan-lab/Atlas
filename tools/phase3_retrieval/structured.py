#!/usr/bin/env python3
"""Deterministic structured-field retrieval baseline for Atlas Phase 3."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import (
    KernelError,
    KernelRepository,
    compile_canonical,
    load_json,
    render_json,
)
from tools.phase3_retrieval.contracts import (
    MODE,
    RESULT_SET_CONTRACT,
    validate_query_set,
    validate_result_set,
)
from tools.phase3_retrieval.lexical import (
    DEFAULT_CUTOFF,
    DEFAULT_LIMIT,
    _json_sha256,
    _rounded,
    evaluate_result_set,
    tokenize,
)

STRUCTURED_INDEX_CONTRACT = "atlas-structured-index/0.1"
STRUCTURED_BASELINE_REPORT_CONTRACT = "atlas-structured-baseline-report/0.1"
STRUCTURED_SCORING_CONTRACT = "atlas-structured-bm25f-scoring/0.1"

FIELD_WEIGHTS = {
    "graph": 1.25,
    "id": 1.5,
    "lifecycle": 0.25,
    "primary": 2.5,
    "provenance": 1.0,
    "title": 3.0,
    "type": 0.75,
}
K1 = 1.2
B = 0.75

ADMIN_KEYS = frozenset(
    {
        "contract",
        "created",
        "id",
        "language",
        "revision",
        "status",
        "staleness",
        "title",
        "type",
        "updated",
        "work",
    }
)
LIFECYCLE_KEYS = frozenset(
    {
        "confidence",
        "human_verified",
        "kind",
        "level",
        "review",
        "review_level",
        "state",
        "status",
        "staleness",
    }
)
GRAPH_KEYS = frozenset(
    {
        "claims",
        "conclusion",
        "depends_on",
        "evidence_set",
        "models",
        "premises",
        "question",
        "relations",
        "source",
        "target",
        "transformation",
    }
)


def _scalars(value: Any) -> list[str]:
    if value is None or isinstance(value, bool):
        return []
    if isinstance(value, (str, int, float)):
        return [str(value)]
    if isinstance(value, Mapping):
        output: list[str] = []
        for key, item in sorted(value.items(), key=lambda pair: str(pair[0])):
            output.append(str(key))
            output.extend(_scalars(item))
        return output
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        output = []
        for item in value:
            output.extend(_scalars(item))
        return output
    return [str(value)]


def _metadata_partition(metadata: Mapping[str, Any]) -> tuple[list[str], list[str]]:
    primary: list[str] = []
    lifecycle: list[str] = []
    for key, value in sorted(metadata.items(), key=lambda pair: str(pair[0])):
        key_text = str(key)
        if key_text in ADMIN_KEYS or key_text in GRAPH_KEYS:
            continue
        values = [key_text, *_scalars(value)]
        if key_text in LIFECYCLE_KEYS:
            lifecycle.extend(values)
        else:
            primary.extend(values)
    for key in sorted(LIFECYCLE_KEYS):
        if key in metadata:
            lifecycle.extend([key, *_scalars(metadata[key])])
    return primary, lifecycle


def _entity_label(entity: Mapping[str, Any]) -> list[str]:
    title = entity.get("title")
    return [
        str(entity["id"]),
        str(entity["type"]),
        title if isinstance(title, str) else "",
    ]


def _graph_values(
    entity: Mapping[str, Any],
    repository: KernelRepository,
) -> list[str]:
    values: list[str] = []
    for reference in entity.get("references", []):
        if not isinstance(reference, Mapping):
            continue
        target = repository.exact(str(reference["id"]), int(reference["revision"]))
        values.extend(reference.get("fields", []))
        values.extend(_entity_label(target))
    for relation in entity.get("relations", []):
        if not isinstance(relation, Mapping):
            continue
        target = repository.exact(str(relation["target"]), int(relation["target_revision"]))
        values.append(str(relation.get("type", "")))
        values.extend(_entity_label(target))
        note = relation.get("note")
        if isinstance(note, str):
            values.append(note)
    for dependent_key in repository.runtime.get("reverse_dependencies", {}).get(entity["key"], []):
        dependent_id, raw_revision = str(dependent_key).rsplit("@", 1)
        dependent = repository.exact(dependent_id, int(raw_revision))
        values.append("inbound dependent")
        values.extend(_entity_label(dependent))
    return values


def _provenance_values(
    entity: Mapping[str, Any],
    repository: KernelRepository,
) -> list[str]:
    sources = repository.provenance_sources(str(entity["id"]), int(entity["revision"]))
    if entity["type"] == "source" and not sources:
        sources = [dict(entity)]
    values: list[str] = []
    for source in sources:
        values.extend(_entity_label(source))
        source_metadata = source.get("metadata")
        if isinstance(source_metadata, Mapping):
            source_record = source_metadata.get("source")
            if isinstance(source_record, Mapping):
                values.extend(_scalars(source_record))
    return values


def _structured_fields(
    entity: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, list[str]]:
    metadata = entity.get("metadata")
    if not isinstance(metadata, Mapping):
        raise KernelError(
            "E-STRUCTURED-METADATA",
            f"canonical entity {entity.get('key')!r} has malformed metadata",
        )
    primary, lifecycle = _metadata_partition(metadata)
    title = entity.get("title")
    raw_fields = {
        "graph": _graph_values(entity, repository),
        "id": [str(entity["id"])],
        "lifecycle": [
            *lifecycle,
            str(entity.get("status") or ""),
            str(entity.get("staleness") or ""),
            str(entity.get("review_level") or ""),
        ],
        "primary": primary,
        "provenance": _provenance_values(entity, repository),
        "title": [title if isinstance(title, str) else ""],
        "type": [str(entity["type"])],
    }
    return {
        field: tokenize(" ".join(value for value in values if value))
        for field, values in sorted(raw_fields.items())
    }


def _corpus_statistics(
    documents: list[Mapping[str, Any]],
) -> tuple[dict[str, float], dict[str, int]]:
    totals = {field: 0 for field in sorted(FIELD_WEIGHTS)}
    document_frequencies: dict[str, int] = defaultdict(int)
    for document in documents:
        terms: set[str] = set()
        for field in sorted(FIELD_WEIGHTS):
            tokens = document["fields"][field]
            totals[field] += len(tokens)
            terms.update(tokens)
        for term in terms:
            document_frequencies[term] += 1
    count = len(documents)
    averages = {
        field: _rounded(totals[field] / count) if count else 0.0
        for field in sorted(totals)
    }
    return averages, dict(sorted(document_frequencies.items()))


def build_structured_index(canonical_root: Path) -> dict[str, Any]:
    runtime = compile_canonical(canonical_root)
    repository = KernelRepository(runtime)
    documents: list[dict[str, Any]] = []
    for entity in runtime["entities"]:
        fields = _structured_fields(entity, repository)
        documents.append(
            {
                "key": entity["key"],
                "id": entity["id"],
                "revision": entity["revision"],
                "type": entity["type"],
                "title": entity.get("title"),
                "status": entity.get("status"),
                "staleness": entity.get("staleness"),
                "review_level": entity.get("review_level"),
                "path": entity["path"],
                "source_sha256": entity["source_sha256"],
                "fields": fields,
                "field_lengths": {
                    field: len(fields[field]) for field in sorted(fields)
                },
            }
        )
    documents.sort(key=lambda item: str(item["key"]))
    averages, document_frequencies = _corpus_statistics(documents)
    index: dict[str, Any] = {
        "contract": STRUCTURED_INDEX_CONTRACT,
        "mode": MODE,
        "source_contract": runtime["source_contract"],
        "source_digest": runtime["source_digest"],
        "entity_count": runtime["entity_count"],
        "field_policy": {
            "canonical_body_indexed": False,
            "fields": sorted(FIELD_WEIGHTS),
            "graph_neighborhood": "outbound-references-relations-and-inbound-dependents",
            "provenance": "exact-source-identities-and-authored-source-records",
            "query_expansion": False,
            "stemming": False,
        },
        "scoring": {
            "contract": STRUCTURED_SCORING_CONTRACT,
            "algorithm": "BM25F",
            "k1": K1,
            "b": B,
            "field_weights": FIELD_WEIGHTS,
            "tie_break": "exact-key-ascending",
        },
        "corpus": {
            "average_field_lengths": averages,
            "document_frequencies": document_frequencies,
        },
        "documents": documents,
        "replaceable": True,
        "canonical_mutation": False,
        "live": False,
        "repository_mutation": False,
    }
    index["build_digest"] = _json_sha256(index)
    return index


def validate_structured_index(
    index: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    if index.get("contract") != STRUCTURED_INDEX_CONTRACT:
        raise KernelError(
            "E-STRUCTURED-INDEX-CONTRACT",
            f"expected {STRUCTURED_INDEX_CONTRACT!r}, got {index.get('contract')!r}",
        )
    if index.get("mode") != MODE:
        raise KernelError("E-STRUCTURED-INDEX-MODE", f"index mode must be {MODE!r}")
    if index.get("source_contract") != repository.runtime.get("source_contract"):
        raise KernelError("E-STRUCTURED-INDEX-SOURCE", "source contract mismatch")
    if index.get("source_digest") != repository.runtime.get("source_digest"):
        raise KernelError("E-STRUCTURED-INDEX-SOURCE", "source digest mismatch")
    if index.get("entity_count") != repository.runtime.get("entity_count"):
        raise KernelError("E-STRUCTURED-INDEX-COUNT", "entity count mismatch")
    if (
        index.get("replaceable") is not True
        or index.get("canonical_mutation") is not False
        or index.get("live") is not False
        or index.get("repository_mutation") is not False
    ):
        raise KernelError(
            "E-STRUCTURED-INDEX-AUTHORITY",
            "structured indexes must be replaceable, non-live, and non-mutating",
        )
    expected_policy = {
        "canonical_body_indexed": False,
        "fields": sorted(FIELD_WEIGHTS),
        "graph_neighborhood": "outbound-references-relations-and-inbound-dependents",
        "provenance": "exact-source-identities-and-authored-source-records",
        "query_expansion": False,
        "stemming": False,
    }
    if index.get("field_policy") != expected_policy:
        raise KernelError("E-STRUCTURED-FIELD-POLICY", "unsupported field policy")
    expected_scoring = {
        "contract": STRUCTURED_SCORING_CONTRACT,
        "algorithm": "BM25F",
        "k1": K1,
        "b": B,
        "field_weights": FIELD_WEIGHTS,
        "tie_break": "exact-key-ascending",
    }
    if index.get("scoring") != expected_scoring:
        raise KernelError("E-STRUCTURED-SCORING", "unsupported scoring policy")
    documents = index.get("documents")
    if not isinstance(documents, list) or len(documents) != repository.runtime["entity_count"]:
        raise KernelError(
            "E-STRUCTURED-DOCUMENTS",
            "structured documents must cover every exact canonical entity",
        )
    keys: list[str] = []
    for raw_document in documents:
        if not isinstance(raw_document, Mapping):
            raise KernelError("E-STRUCTURED-DOCUMENT", "index document must be an object")
        entity_id = raw_document.get("id")
        revision = raw_document.get("revision")
        if not isinstance(entity_id, str) or not isinstance(revision, int):
            raise KernelError("E-STRUCTURED-DOCUMENT", "document identity is malformed")
        entity = repository.exact(entity_id, revision)
        key = str(entity["key"])
        keys.append(key)
        for field in (
            "key",
            "type",
            "title",
            "status",
            "staleness",
            "review_level",
            "path",
            "source_sha256",
        ):
            if raw_document.get(field) != entity.get(field):
                raise KernelError(
                    "E-STRUCTURED-DOCUMENT-METADATA",
                    f"index document {key} disagrees with canonical field {field}",
                )
        fields = raw_document.get("fields")
        lengths = raw_document.get("field_lengths")
        if not isinstance(fields, Mapping) or not isinstance(lengths, Mapping):
            raise KernelError("E-STRUCTURED-DOCUMENT-FIELDS", f"malformed fields for {key}")
        expected_fields = _structured_fields(entity, repository)
        if fields != expected_fields:
            raise KernelError(
                "E-STRUCTURED-DOCUMENT-FIELDS",
                f"indexed fields for {key} do not match canonical structured fields",
            )
        if set(fields) != set(FIELD_WEIGHTS) or set(lengths) != set(FIELD_WEIGHTS):
            raise KernelError(
                "E-STRUCTURED-DOCUMENT-FIELDS",
                f"index document {key} must contain exactly the declared fields",
            )
        for field in sorted(FIELD_WEIGHTS):
            tokens = fields[field]
            if not isinstance(tokens, list) or not all(
                isinstance(token, str) and token for token in tokens
            ):
                raise KernelError(
                    "E-STRUCTURED-DOCUMENT-TOKENS",
                    f"invalid tokens for {key} field {field}",
                )
            if lengths[field] != len(tokens):
                raise KernelError(
                    "E-STRUCTURED-DOCUMENT-LENGTH",
                    f"inconsistent length for {key} field {field}",
                )
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise KernelError(
            "E-STRUCTURED-DOCUMENT-ORDER",
            "documents must be unique and sorted by exact key",
        )
    averages, document_frequencies = _corpus_statistics(documents)
    corpus = index.get("corpus")
    if not isinstance(corpus, Mapping):
        raise KernelError("E-STRUCTURED-CORPUS-STATS", "corpus statistics are malformed")
    if corpus.get("average_field_lengths") != averages:
        raise KernelError("E-STRUCTURED-CORPUS-STATS", "average lengths mismatch")
    if corpus.get("document_frequencies") != document_frequencies:
        raise KernelError("E-STRUCTURED-CORPUS-STATS", "document frequencies mismatch")
    build_digest = index.get("build_digest")
    if not isinstance(build_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", build_digest):
        raise KernelError("E-STRUCTURED-BUILD-DIGEST", "build_digest must be a SHA-256")
    unsigned = dict(index)
    unsigned.pop("build_digest", None)
    if _json_sha256(unsigned) != build_digest:
        raise KernelError("E-STRUCTURED-BUILD-DIGEST", "build digest mismatch")
    return {
        "contract": "atlas-structured-index-validation/0.1",
        "validated_contract": STRUCTURED_INDEX_CONTRACT,
        "source_digest": index["source_digest"],
        "build_digest": build_digest,
        "entity_count": len(documents),
        "term_count": len(document_frequencies),
        "decision": "valid",
        "replaceable": True,
        "canonical_body_indexed": False,
        "live": False,
        "repository_mutation": False,
    }


def _score_document(
    query_terms: Counter[str],
    document: Mapping[str, Any],
    index: Mapping[str, Any],
) -> tuple[float, list[str]]:
    corpus = index["corpus"]
    averages = corpus["average_field_lengths"]
    frequencies = corpus["document_frequencies"]
    document_count = int(index["entity_count"])
    matched_fields: set[str] = set()
    score = 0.0
    for term, query_frequency in sorted(query_terms.items()):
        document_frequency = int(frequencies.get(term, 0))
        if document_frequency == 0:
            continue
        inverse_document_frequency = math.log(
            1.0 + (document_count - document_frequency + 0.5) / (document_frequency + 0.5)
        )
        query_weight = 1.0 + math.log(query_frequency)
        for field, field_weight in sorted(FIELD_WEIGHTS.items()):
            tokens = document["fields"][field]
            term_frequency = tokens.count(term)
            if term_frequency == 0:
                continue
            matched_fields.add(field)
            average_length = float(averages[field])
            length = float(document["field_lengths"][field])
            normalization = 1.0 - B
            if average_length > 0.0:
                normalization += B * length / average_length
            denominator = term_frequency + K1 * normalization
            score += (
                query_weight
                * inverse_document_frequency
                * field_weight
                * (term_frequency * (K1 + 1.0) / denominator)
            )
    return _rounded(score), sorted(matched_fields)


def search_structured_index(
    index: Mapping[str, Any],
    query: str,
    limit: int = DEFAULT_LIMIT,
) -> list[dict[str, Any]]:
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise KernelError("E-STRUCTURED-LIMIT", "search limit must be nonnegative")
    if limit == 0:
        return []
    query_terms = Counter(tokenize(query))
    if not query_terms:
        return []
    hits: list[dict[str, Any]] = []
    for document in index["documents"]:
        score, matched_fields = _score_document(query_terms, document, index)
        if score <= 0.0:
            continue
        hits.append(
            {
                "document": document,
                "score": score,
                "matched_fields": matched_fields,
            }
        )
    hits.sort(key=lambda item: (-float(item["score"]), str(item["document"]["key"])))
    return hits[:limit]


def _result_item(
    hit: Mapping[str, Any],
    rank: int,
    repository: KernelRepository,
) -> dict[str, Any]:
    document = hit["document"]
    entity_id = str(document["id"])
    revision = int(document["revision"])
    provenance_entities = repository.provenance_sources(entity_id, revision)
    provenance = sorted(
        f"{entity['id']}@{entity['revision']}" for entity in provenance_entities
    )
    if document["type"] == "source" and not provenance:
        provenance = [str(document["key"])]
    matched_fields = list(hit["matched_fields"])
    return {
        "id": entity_id,
        "revision": revision,
        "rank": rank,
        "score": hit["score"],
        "type": document["type"],
        "title": document.get("title"),
        "status": document.get("status"),
        "staleness": document.get("staleness"),
        "review_level": document.get("review_level"),
        "matched_fields": matched_fields,
        "explanation": (
            "Deterministic structured BM25F match in fields: "
            + ", ".join(matched_fields)
            + f"; score={hit['score']:.12f}; canonical body excluded."
        ),
        "provenance": provenance,
    }


def run_structured_queries(
    index: Mapping[str, Any],
    query_set: Mapping[str, Any],
    repository: KernelRepository,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    validate_query_set(query_set, repository)
    validate_structured_index(index, repository)
    responses: list[dict[str, Any]] = []
    for query in query_set["queries"]:
        expected = query["expected"]
        if expected["kind"] == "error":
            target = expected["target"]
            try:
                repository.exact(target["id"], target["revision"])
            except KernelError as exc:
                responses.append(
                    {
                        "query_id": query["id"],
                        "outcome": "error",
                        "error": exc.code,
                        "target": target,
                    }
                )
            else:
                raise KernelError(
                    "E-STRUCTURED-EXPECTED-ERROR",
                    f"expected unavailable target exists for {query['id']}",
                )
            continue
        hits = search_structured_index(index, query["text"], limit=limit)
        responses.append(
            {
                "query_id": query["id"],
                "outcome": "ranked",
                "items": [
                    _result_item(hit, rank, repository)
                    for rank, hit in enumerate(hits, start=1)
                ],
            }
        )
    result_set = {
        "contract": RESULT_SET_CONTRACT,
        "query_set_id": query_set["id"],
        "query_set_version": query_set["version"],
        "index": {
            "contract": STRUCTURED_INDEX_CONTRACT,
            "build_digest": index["build_digest"],
            "source_digest": index["source_digest"],
            "replaceable": True,
            "canonical_mutation": False,
        },
        "responses": responses,
        "advisory_only": True,
        "live": False,
        "repository_mutation": False,
    }
    validate_result_set(result_set, query_set, repository)
    return result_set


def _metric_delta(
    current: Mapping[str, Any],
    lexical: Mapping[str, Any],
) -> dict[str, float]:
    return {
        key: _rounded(float(current[key]) - float(lexical[key]))
        for key in sorted(current)
        if key in lexical
    }


def run_structured_baseline(
    canonical_root: Path,
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    cutoff: int = DEFAULT_CUTOFF,
    limit: int = DEFAULT_LIMIT,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = compile_canonical(canonical_root)
    repository = KernelRepository(runtime)
    validate_query_set(query_set, repository)
    if lexical_baseline.get("contract") != "atlas-phase3-lexical-baseline/0.1":
        raise KernelError(
            "E-STRUCTURED-LEXICAL-BASELINE",
            "structured comparison requires the accepted lexical baseline",
        )
    first_index = build_structured_index(canonical_root)
    second_index = build_structured_index(canonical_root)
    if render_json(first_index) != render_json(second_index):
        raise KernelError(
            "E-STRUCTURED-NONDETERMINISTIC",
            "repeated structured index builds produced different bytes",
        )
    index_validation = validate_structured_index(first_index, repository)
    result_set = run_structured_queries(first_index, query_set, repository, limit=limit)
    metric_report = evaluate_result_set(result_set, query_set, repository, cutoff=cutoff)
    lexical_metrics = lexical_baseline.get("metrics")
    if not isinstance(lexical_metrics, Mapping):
        raise KernelError(
            "E-STRUCTURED-LEXICAL-BASELINE",
            "accepted lexical baseline metrics are malformed",
        )
    report = {
        "contract": STRUCTURED_BASELINE_REPORT_CONTRACT,
        "mode": MODE,
        "decision": "structured-baseline-candidate",
        "index_contract": STRUCTURED_INDEX_CONTRACT,
        "query_set_id": query_set["id"],
        "query_set_version": query_set["version"],
        "entity_count": first_index["entity_count"],
        "query_count": len(query_set["queries"]),
        "deterministic_index": True,
        "index_validation": index_validation,
        "result_set_sha256": metric_report["result_set_sha256"],
        "metrics": metric_report["metrics"],
        "lexical_baseline_metrics": dict(lexical_metrics),
        "metric_delta_from_lexical": _metric_delta(metric_report["metrics"], lexical_metrics),
        "cutoff": cutoff,
        "limit": limit,
        "tie_count": metric_report["tie_count"],
        "rebuild_verified": True,
        "replaceable": True,
        "canonical_body_indexed": False,
        "accepted_judgments_unchanged": True,
        "quality_claim": "bounded-reference-fixture-only",
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "judgment_specific_tuning": False,
        "advisory_only": True,
        "live": False,
        "repository_mutation": False,
    }
    return first_index, result_set, metric_report, report


def _write(path: Path | None, value: Mapping[str, Any]) -> None:
    rendered = render_json(value)
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
        "--lexical-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/lexical-baseline.json"),
    )
    parser.add_argument("--cutoff", type=int, default=DEFAULT_CUTOFF)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--index-output", type=Path)
    parser.add_argument("--result-output", type=Path)
    parser.add_argument("--metric-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args(argv)
    try:
        query_set = load_json(args.query_set)
        lexical_baseline = load_json(args.lexical_baseline)
        index, results, metrics, report = run_structured_baseline(
            args.canonical_root,
            query_set,
            lexical_baseline,
            cutoff=args.cutoff,
            limit=args.limit,
        )
        if not any(
            (
                args.index_output,
                args.result_output,
                args.metric_output,
                args.report_output,
            )
        ):
            _write(None, report)
        else:
            if args.index_output is not None:
                _write(args.index_output, index)
            if args.result_output is not None:
                _write(args.result_output, results)
            if args.metric_output is not None:
                _write(args.metric_output, metrics)
            if args.report_output is not None:
                _write(args.report_output, report)
        return 0
    except (KernelError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
