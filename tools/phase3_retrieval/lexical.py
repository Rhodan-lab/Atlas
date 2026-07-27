#!/usr/bin/env python3
"""Deterministic, replaceable lexical retrieval baseline for Atlas Phase 3."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping

from tools.phase2_kernel import (
    KernelError,
    KernelRepository,
    compile_canonical,
    load_json,
    render_json,
)
from tools.phase2_kernel.kernel import parse_markdown
from tools.phase3_retrieval.contracts import (
    METRIC_REPORT_CONTRACT,
    MODE,
    RESULT_SET_CONTRACT,
    validate_metric_report,
    validate_query_set,
    validate_result_set,
)

LEXICAL_INDEX_CONTRACT = "atlas-lexical-index/0.1"
LEXICAL_BASELINE_REPORT_CONTRACT = "atlas-lexical-baseline-report/0.1"
TOKENIZER_CONTRACT = "atlas-english-tokenizer/0.1"
SCORING_CONTRACT = "atlas-bm25f-scoring/0.1"

TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "can",
        "did",
        "do",
        "does",
        "for",
        "from",
        "had",
        "has",
        "have",
        "how",
        "in",
        "into",
        "is",
        "it",
        "of",
        "on",
        "or",
        "that",
        "the",
        "their",
        "this",
        "to",
        "was",
        "were",
        "what",
        "when",
        "which",
        "why",
        "with",
    }
)
FIELD_WEIGHTS = {
    "body": 1.0,
    "id": 1.5,
    "title": 3.0,
    "type": 0.75,
}
K1 = 1.2
B = 0.75
DEFAULT_CUTOFF = 5
DEFAULT_LIMIT = 10


def _json_sha256(value: Mapping[str, Any]) -> str:
    return hashlib.sha256(render_json(value).encode("utf-8")).hexdigest()


def _rounded(value: float) -> float:
    return round(value, 12)


def tokenize(value: str) -> list[str]:
    """Normalize English lexical tokens without stemming or hidden expansion."""
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return [
        token
        for token in TOKEN_RE.findall(normalized)
        if token not in STOPWORDS
    ]


def _entity_fields(canonical_root: Path, entity: Mapping[str, Any]) -> dict[str, list[str]]:
    path = canonical_root / str(entity["path"])
    document = parse_markdown(path)
    if document.source_sha256 != entity.get("source_sha256"):
        raise KernelError(
            "E-LEXICAL-SOURCE-DIGEST",
            f"canonical source changed while indexing {entity.get('key')!r}",
            str(path),
        )
    title = entity.get("title")
    return {
        "body": tokenize(document.body),
        "id": tokenize(str(entity["id"])),
        "title": tokenize(title if isinstance(title, str) else ""),
        "type": tokenize(str(entity["type"])),
    }


def _corpus_statistics(
    documents: list[Mapping[str, Any]],
) -> tuple[dict[str, float], dict[str, int]]:
    totals = {field: 0 for field in sorted(FIELD_WEIGHTS)}
    document_frequencies: dict[str, int] = defaultdict(int)
    for document in documents:
        fields = document["fields"]
        terms: set[str] = set()
        for field in sorted(FIELD_WEIGHTS):
            tokens = fields[field]
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


def build_lexical_index(canonical_root: Path) -> dict[str, Any]:
    runtime = compile_canonical(canonical_root)
    documents: list[dict[str, Any]] = []
    for entity in runtime["entities"]:
        fields = _entity_fields(canonical_root, entity)
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
        "contract": LEXICAL_INDEX_CONTRACT,
        "mode": MODE,
        "source_contract": runtime["source_contract"],
        "source_digest": runtime["source_digest"],
        "entity_count": runtime["entity_count"],
        "tokenizer": {
            "contract": TOKENIZER_CONTRACT,
            "normalization": "NFKC-casefold",
            "pattern": "[a-z0-9]+",
            "stopwords": sorted(STOPWORDS),
            "stemming": False,
            "query_expansion": False,
        },
        "scoring": {
            "contract": SCORING_CONTRACT,
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


def validate_lexical_index(
    index: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    if index.get("contract") != LEXICAL_INDEX_CONTRACT:
        raise KernelError(
            "E-LEXICAL-INDEX-CONTRACT",
            f"expected {LEXICAL_INDEX_CONTRACT!r}, got {index.get('contract')!r}",
        )
    if index.get("mode") != MODE:
        raise KernelError("E-LEXICAL-INDEX-MODE", f"index mode must be {MODE!r}")
    if index.get("source_contract") != repository.runtime.get("source_contract"):
        raise KernelError(
            "E-LEXICAL-INDEX-SOURCE",
            "index source contract does not match the canonical runtime",
        )
    if index.get("source_digest") != repository.runtime.get("source_digest"):
        raise KernelError(
            "E-LEXICAL-INDEX-SOURCE",
            "index source digest does not match the canonical runtime",
        )
    if index.get("entity_count") != repository.runtime.get("entity_count"):
        raise KernelError(
            "E-LEXICAL-INDEX-COUNT",
            "index entity_count does not match the canonical runtime",
        )
    if (
        index.get("replaceable") is not True
        or index.get("canonical_mutation") is not False
        or index.get("live") is not False
        or index.get("repository_mutation") is not False
    ):
        raise KernelError(
            "E-LEXICAL-INDEX-AUTHORITY",
            "lexical indexes must be replaceable, non-live, and non-mutating",
        )
    tokenizer = index.get("tokenizer")
    if not isinstance(tokenizer, Mapping) or tokenizer != {
        "contract": TOKENIZER_CONTRACT,
        "normalization": "NFKC-casefold",
        "pattern": "[a-z0-9]+",
        "stopwords": sorted(STOPWORDS),
        "stemming": False,
        "query_expansion": False,
    }:
        raise KernelError(
            "E-LEXICAL-TOKENIZER",
            "lexical tokenizer configuration is malformed or unsupported",
        )
    scoring = index.get("scoring")
    if not isinstance(scoring, Mapping) or scoring != {
        "contract": SCORING_CONTRACT,
        "algorithm": "BM25F",
        "k1": K1,
        "b": B,
        "field_weights": FIELD_WEIGHTS,
        "tie_break": "exact-key-ascending",
    }:
        raise KernelError(
            "E-LEXICAL-SCORING",
            "lexical scoring configuration is malformed or unsupported",
        )
    documents = index.get("documents")
    if not isinstance(documents, list) or len(documents) != repository.runtime["entity_count"]:
        raise KernelError(
            "E-LEXICAL-DOCUMENTS",
            "lexical documents must cover every exact canonical entity",
        )
    keys: list[str] = []
    for raw_document in documents:
        if not isinstance(raw_document, Mapping):
            raise KernelError("E-LEXICAL-DOCUMENT", "index document must be an object")
        entity_id = raw_document.get("id")
        revision = raw_document.get("revision")
        if not isinstance(entity_id, str) or not isinstance(revision, int):
            raise KernelError("E-LEXICAL-DOCUMENT", "index document identity is malformed")
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
                    "E-LEXICAL-DOCUMENT-METADATA",
                    f"index document {key} disagrees with canonical field {field}",
                )
        fields = raw_document.get("fields")
        lengths = raw_document.get("field_lengths")
        if not isinstance(fields, Mapping) or not isinstance(lengths, Mapping):
            raise KernelError(
                "E-LEXICAL-DOCUMENT-FIELDS",
                f"index document {key} has malformed fields",
            )
        if set(fields) != set(FIELD_WEIGHTS) or set(lengths) != set(FIELD_WEIGHTS):
            raise KernelError(
                "E-LEXICAL-DOCUMENT-FIELDS",
                f"index document {key} must contain exactly the declared fields",
            )
        for field in sorted(FIELD_WEIGHTS):
            tokens = fields[field]
            if (
                not isinstance(tokens, list)
                or not all(
                    isinstance(token, str)
                    and token
                    and token == token.casefold()
                    and TOKEN_RE.fullmatch(token)
                    and token not in STOPWORDS
                    for token in tokens
                )
            ):
                raise KernelError(
                    "E-LEXICAL-DOCUMENT-TOKENS",
                    f"index document {key} field {field} has invalid tokens",
                )
            if lengths[field] != len(tokens):
                raise KernelError(
                    "E-LEXICAL-DOCUMENT-LENGTH",
                    f"index document {key} field {field} length is inconsistent",
                )
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        raise KernelError(
            "E-LEXICAL-DOCUMENT-ORDER",
            "lexical documents must be unique and sorted by exact key",
        )
    averages, document_frequencies = _corpus_statistics(documents)
    corpus = index.get("corpus")
    if not isinstance(corpus, Mapping) or corpus.get("average_field_lengths") != averages:
        raise KernelError(
            "E-LEXICAL-CORPUS-STATS",
            "average field lengths do not match indexed documents",
        )
    if corpus.get("document_frequencies") != document_frequencies:
        raise KernelError(
            "E-LEXICAL-CORPUS-STATS",
            "document frequencies do not match indexed documents",
        )
    build_digest = index.get("build_digest")
    if not isinstance(build_digest, str) or not re.fullmatch(r"[0-9a-f]{64}", build_digest):
        raise KernelError("E-LEXICAL-BUILD-DIGEST", "build_digest must be a SHA-256")
    unsigned = dict(index)
    unsigned.pop("build_digest", None)
    if _json_sha256(unsigned) != build_digest:
        raise KernelError(
            "E-LEXICAL-BUILD-DIGEST",
            "build_digest does not match the lexical index",
        )
    return {
        "contract": "atlas-lexical-index-validation/0.1",
        "validated_contract": LEXICAL_INDEX_CONTRACT,
        "source_digest": index["source_digest"],
        "build_digest": build_digest,
        "entity_count": len(documents),
        "term_count": len(document_frequencies),
        "decision": "valid",
        "replaceable": True,
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


def search_lexical_index(
    index: Mapping[str, Any],
    query: str,
    limit: int = DEFAULT_LIMIT,
) -> list[dict[str, Any]]:
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise KernelError("E-LEXICAL-LIMIT", "search limit must be a nonnegative integer")
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
            "Deterministic BM25F lexical match in fields: "
            + ", ".join(matched_fields)
            + f"; score={hit['score']:.12f}."
        ),
        "provenance": provenance,
    }


def run_lexical_queries(
    index: Mapping[str, Any],
    query_set: Mapping[str, Any],
    repository: KernelRepository,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    validate_query_set(query_set, repository)
    validate_lexical_index(index, repository)
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
                    "E-LEXICAL-EXPECTED-ERROR",
                    f"expected unavailable target exists for {query['id']}",
                )
            continue
        hits = search_lexical_index(index, query["text"], limit=limit)
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
            "contract": LEXICAL_INDEX_CONTRACT,
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


def _judgments(query: Mapping[str, Any]) -> dict[str, int]:
    expected = query["expected"]
    if expected["kind"] != "ranked":
        return {}
    return {
        f"{judgment['id']}@{judgment['revision']}": int(judgment["grade"])
        for judgment in expected["judgments"]
    }


def _ndcg(items: list[Mapping[str, Any]], judgments: Mapping[str, int], cutoff: int) -> float:
    def gain(grade: int, rank: int) -> float:
        return (2.0**grade - 1.0) / math.log2(rank + 1.0)

    dcg = 0.0
    for rank, item in enumerate(items[:cutoff], start=1):
        key = f"{item['id']}@{item['revision']}"
        dcg += gain(int(judgments.get(key, 0)), rank)
    ideal_grades = sorted(judgments.values(), reverse=True)[:cutoff]
    ideal = sum(gain(grade, rank) for rank, grade in enumerate(ideal_grades, start=1))
    return dcg / ideal if ideal > 0.0 else 0.0


def evaluate_result_set(
    result_set: Mapping[str, Any],
    query_set: Mapping[str, Any],
    repository: KernelRepository,
    cutoff: int = DEFAULT_CUTOFF,
) -> dict[str, Any]:
    if not isinstance(cutoff, int) or isinstance(cutoff, bool) or cutoff <= 0:
        raise KernelError("E-LEXICAL-CUTOFF", "metric cutoff must be positive")
    result_validation = validate_result_set(result_set, query_set, repository)
    responses = {response["query_id"]: response for response in result_set["responses"]}
    precision_values: list[float] = []
    recall_values: list[float] = []
    reciprocal_values: list[float] = []
    ndcg_values: list[float] = []
    zero_results = 0
    ranked_queries = 0
    expected_errors = 0
    correct_errors = 0
    tie_count = 0

    for query in query_set["queries"]:
        response = responses[query["id"]]
        if query["expected"]["kind"] == "error":
            expected_errors += 1
            if response["outcome"] == "error" and response["error"] == query["expected"]["error"]:
                correct_errors += 1
            continue
        ranked_queries += 1
        items = response["items"]
        if not items:
            zero_results += 1
        judgments = _judgments(query)
        top = items[:cutoff]
        relevant_hits = sum(
            1
            for item in top
            if judgments.get(f"{item['id']}@{item['revision']}", 0) > 0
        )
        precision_values.append(relevant_hits / cutoff)
        recall_values.append(relevant_hits / len(judgments))
        reciprocal = 0.0
        for rank, item in enumerate(items, start=1):
            if judgments.get(f"{item['id']}@{item['revision']}", 0) > 0:
                reciprocal = 1.0 / rank
                break
        reciprocal_values.append(reciprocal)
        ndcg_values.append(_ndcg(items, judgments, cutoff))
        for left, right in zip(items, items[1:]):
            if float(left["score"]) == float(right["score"]):
                tie_count += 1

    def average(values: list[float]) -> float:
        return _rounded(sum(values) / len(values)) if values else 0.0

    metrics = {
        "precision_at_k": average(precision_values),
        "recall_at_k": average(recall_values),
        "mean_reciprocal_rank": average(reciprocal_values),
        "ndcg_at_k": average(ndcg_values),
        "zero_result_rate": _rounded(zero_results / ranked_queries) if ranked_queries else 0.0,
        "unavailable_revision_rate": _rounded(correct_errors / expected_errors) if expected_errors else 0.0,
    }
    metric_report = {
        "contract": METRIC_REPORT_CONTRACT,
        "query_set_id": query_set["id"],
        "query_set_version": query_set["version"],
        "result_set_sha256": _json_sha256(result_set),
        "cutoff": cutoff,
        "evaluated_ranked_queries": ranked_queries,
        "expected_error_queries": expected_errors,
        "metrics": metrics,
        "tie_count": tie_count,
        "advisory_only": True,
        "live": False,
        "repository_mutation": False,
    }
    validate_metric_report(metric_report, query_set, repository)
    if result_validation["tie_count"] != tie_count:
        raise KernelError(
            "E-LEXICAL-TIE-COUNT",
            "metric tie count disagrees with result-set validation",
        )
    return metric_report


def run_lexical_baseline(
    canonical_root: Path,
    query_set: Mapping[str, Any],
    cutoff: int = DEFAULT_CUTOFF,
    limit: int = DEFAULT_LIMIT,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    runtime = compile_canonical(canonical_root)
    repository = KernelRepository(runtime)
    validate_query_set(query_set, repository)
    first_index = build_lexical_index(canonical_root)
    second_index = build_lexical_index(canonical_root)
    if render_json(first_index) != render_json(second_index):
        raise KernelError(
            "E-LEXICAL-NONDETERMINISTIC",
            "repeated lexical index builds produced different bytes",
        )
    index_validation = validate_lexical_index(first_index, repository)
    result_set = run_lexical_queries(first_index, query_set, repository, limit=limit)
    metric_report = evaluate_result_set(result_set, query_set, repository, cutoff=cutoff)
    report = {
        "contract": LEXICAL_BASELINE_REPORT_CONTRACT,
        "mode": MODE,
        "decision": "lexical-baseline-candidate",
        "index_contract": LEXICAL_INDEX_CONTRACT,
        "query_set_id": query_set["id"],
        "query_set_version": query_set["version"],
        "entity_count": first_index["entity_count"],
        "query_count": len(query_set["queries"]),
        "deterministic_index": True,
        "index_validation": index_validation,
        "result_set_sha256": metric_report["result_set_sha256"],
        "metrics": metric_report["metrics"],
        "cutoff": cutoff,
        "limit": limit,
        "tie_count": metric_report["tie_count"],
        "rebuild_verified": True,
        "replaceable": True,
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
    parser.add_argument("--cutoff", type=int, default=DEFAULT_CUTOFF)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--index-output", type=Path)
    parser.add_argument("--result-output", type=Path)
    parser.add_argument("--metric-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args(argv)
    try:
        query_set = load_json(args.query_set)
        index, results, metrics, report = run_lexical_baseline(
            args.canonical_root,
            query_set,
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
