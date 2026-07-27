#!/usr/bin/env python3
"""Deterministic reciprocal-rank fusion candidate for Atlas Phase 3."""
from __future__ import annotations

import argparse
import json
import math
import sys
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
    LEXICAL_INDEX_CONTRACT,
    _json_sha256,
    _rounded,
    build_lexical_index,
    evaluate_result_set,
    run_lexical_queries,
    validate_lexical_index,
)
from tools.phase3_retrieval.structured import (
    STRUCTURED_INDEX_CONTRACT,
    build_structured_index,
    run_structured_queries,
    validate_structured_index,
)

FUSION_MANIFEST_CONTRACT = "atlas-rank-fusion-manifest/0.1"
FUSION_SCORING_CONTRACT = "atlas-reciprocal-rank-fusion/0.1"
FUSION_REPORT_CONTRACT = "atlas-rank-fusion-report/0.1"
LEXICAL_BASELINE_CONTRACT = "atlas-phase3-lexical-baseline/0.1"
STRUCTURED_BASELINE_CONTRACT = "atlas-phase3-structured-baseline/0.1"
RRF_K = 60
LEXICAL_WEIGHT = 1.0
STRUCTURED_WEIGHT = 1.0


def _exact_key(entity_id: str, revision: int) -> str:
    return f"{entity_id}@{revision}"


def _validate_baselines(
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    repository: KernelRepository,
) -> None:
    query_report = validate_query_set(query_set, repository)
    if lexical_baseline.get("contract") != LEXICAL_BASELINE_CONTRACT:
        raise KernelError(
            "E-FUSION-LEXICAL-BASELINE",
            "rank fusion requires the accepted lexical baseline",
        )
    if structured_baseline.get("contract") != STRUCTURED_BASELINE_CONTRACT:
        raise KernelError(
            "E-FUSION-STRUCTURED-BASELINE",
            "rank fusion requires the accepted structured baseline",
        )
    for baseline_name, baseline in (
        ("lexical", lexical_baseline),
        ("structured", structured_baseline),
    ):
        if (
            baseline.get("query_set_id") != query_report["query_set_id"]
            or baseline.get("query_set_version") != query_report["query_set_version"]
            or baseline.get("entity_count") != repository.runtime["entity_count"]
            or baseline.get("source_digest") != repository.runtime["source_digest"]
        ):
            raise KernelError(
                "E-FUSION-BASELINE-IDENTITY",
                f"{baseline_name} baseline does not match the accepted corpus and query set",
            )
        if (
            baseline.get("replaceable") is not True
            or baseline.get("rebuild_verified") is not True
            or baseline.get("live") is not False
            or baseline.get("repository_mutation") is not False
        ):
            raise KernelError(
                "E-FUSION-BASELINE-AUTHORITY",
                f"{baseline_name} baseline violates the retrieval authority boundary",
            )
    if structured_baseline.get("accepted_judgments_unchanged") is not True:
        raise KernelError(
            "E-FUSION-JUDGMENTS",
            "structured baseline must preserve the accepted judgments",
        )


def _prepare_inputs(
    canonical_root: Path,
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
) -> tuple[
    KernelRepository,
    dict[str, Any],
    dict[str, Any],
]:
    runtime = compile_canonical(canonical_root)
    repository = KernelRepository(runtime)
    _validate_baselines(query_set, lexical_baseline, structured_baseline, repository)
    lexical_index = build_lexical_index(canonical_root)
    structured_index = build_structured_index(canonical_root)
    validate_lexical_index(lexical_index, repository)
    validate_structured_index(structured_index, repository)
    if (
        lexical_index["contract"] != lexical_baseline.get("index_contract")
        or lexical_index["build_digest"] != lexical_baseline.get("index_build_digest")
    ):
        raise KernelError(
            "E-FUSION-LEXICAL-INDEX",
            "generated lexical index does not match the accepted lexical baseline",
        )
    if (
        structured_index["contract"] != structured_baseline.get("index_contract")
        or structured_index["build_digest"]
        != structured_baseline.get("index_build_digest")
    ):
        raise KernelError(
            "E-FUSION-STRUCTURED-INDEX",
            "generated structured index does not match the accepted structured baseline",
        )
    return repository, lexical_index, structured_index


def build_fusion_manifest(
    canonical_root: Path,
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
) -> dict[str, Any]:
    repository, lexical_index, structured_index = _prepare_inputs(
        canonical_root,
        query_set,
        lexical_baseline,
        structured_baseline,
    )
    manifest: dict[str, Any] = {
        "contract": FUSION_MANIFEST_CONTRACT,
        "mode": MODE,
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "query_set": {
            "id": query_set["id"],
            "version": query_set["version"],
        },
        "method": {
            "contract": FUSION_SCORING_CONTRACT,
            "algorithm": "reciprocal-rank-fusion",
            "rrf_k": RRF_K,
            "weights": {
                "lexical": LEXICAL_WEIGHT,
                "structured": STRUCTURED_WEIGHT,
            },
            "input_limit": DEFAULT_LIMIT,
            "output_limit": DEFAULT_LIMIT,
            "tie_break": "exact-key-ascending",
            "raw_score_blending": False,
        },
        "inputs": {
            "lexical": {
                "baseline_contract": lexical_baseline["contract"],
                "baseline_sha256": _json_sha256(lexical_baseline),
                "index_contract": LEXICAL_INDEX_CONTRACT,
                "index_build_digest": lexical_index["build_digest"],
                "result_set_sha256": lexical_baseline["result_set_sha256"],
            },
            "structured": {
                "baseline_contract": structured_baseline["contract"],
                "baseline_sha256": _json_sha256(structured_baseline),
                "index_contract": STRUCTURED_INDEX_CONTRACT,
                "index_build_digest": structured_index["build_digest"],
                "result_set_sha256": structured_baseline["result_set_sha256"],
            },
        },
        "accepted_judgments_unchanged": True,
        "replaceable": True,
        "canonical_mutation": False,
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "learned_weights": False,
        "judgment_specific_tuning": False,
        "live": False,
        "repository_mutation": False,
    }
    manifest["build_digest"] = _json_sha256(manifest)
    return manifest


def validate_fusion_manifest(
    manifest: Mapping[str, Any],
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    repository: KernelRepository,
) -> dict[str, Any]:
    _validate_baselines(query_set, lexical_baseline, structured_baseline, repository)
    if manifest.get("contract") != FUSION_MANIFEST_CONTRACT:
        raise KernelError(
            "E-FUSION-MANIFEST-CONTRACT",
            f"expected {FUSION_MANIFEST_CONTRACT!r}",
        )
    if manifest.get("mode") != MODE:
        raise KernelError("E-FUSION-MANIFEST-MODE", f"mode must be {MODE!r}")
    if (
        manifest.get("source_digest") != repository.runtime["source_digest"]
        or manifest.get("entity_count") != repository.runtime["entity_count"]
        or manifest.get("query_set")
        != {"id": query_set["id"], "version": query_set["version"]}
    ):
        raise KernelError(
            "E-FUSION-MANIFEST-IDENTITY",
            "fusion manifest does not match the accepted corpus and query set",
        )
    expected_method = {
        "contract": FUSION_SCORING_CONTRACT,
        "algorithm": "reciprocal-rank-fusion",
        "rrf_k": RRF_K,
        "weights": {
            "lexical": LEXICAL_WEIGHT,
            "structured": STRUCTURED_WEIGHT,
        },
        "input_limit": DEFAULT_LIMIT,
        "output_limit": DEFAULT_LIMIT,
        "tie_break": "exact-key-ascending",
        "raw_score_blending": False,
    }
    if manifest.get("method") != expected_method:
        raise KernelError(
            "E-FUSION-METHOD",
            "fusion manifest differs from the predeclared equal-weight RRF method",
        )
    expected_inputs = {
        "lexical": {
            "baseline_contract": lexical_baseline["contract"],
            "baseline_sha256": _json_sha256(lexical_baseline),
            "index_contract": lexical_baseline["index_contract"],
            "index_build_digest": lexical_baseline["index_build_digest"],
            "result_set_sha256": lexical_baseline["result_set_sha256"],
        },
        "structured": {
            "baseline_contract": structured_baseline["contract"],
            "baseline_sha256": _json_sha256(structured_baseline),
            "index_contract": structured_baseline["index_contract"],
            "index_build_digest": structured_baseline["index_build_digest"],
            "result_set_sha256": structured_baseline["result_set_sha256"],
        },
    }
    if manifest.get("inputs") != expected_inputs:
        raise KernelError(
            "E-FUSION-INPUTS",
            "fusion manifest does not bind the exact accepted baseline identities",
        )
    for field, expected in (
        ("accepted_judgments_unchanged", True),
        ("replaceable", True),
        ("canonical_mutation", False),
        ("external_services", False),
        ("embeddings", False),
        ("vector_database", False),
        ("learned_weights", False),
        ("judgment_specific_tuning", False),
        ("live", False),
        ("repository_mutation", False),
    ):
        if manifest.get(field) is not expected:
            raise KernelError(
                "E-FUSION-AUTHORITY",
                f"fusion manifest requires {field}={expected!r}",
            )
    digest = manifest.get("build_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError("E-FUSION-BUILD-DIGEST", "build_digest must be a SHA-256")
    unsigned = dict(manifest)
    unsigned.pop("build_digest", None)
    if _json_sha256(unsigned) != digest:
        raise KernelError("E-FUSION-BUILD-DIGEST", "fusion build digest mismatch")
    return {
        "contract": "atlas-rank-fusion-validation/0.1",
        "validated_contract": FUSION_MANIFEST_CONTRACT,
        "build_digest": digest,
        "source_digest": manifest["source_digest"],
        "entity_count": manifest["entity_count"],
        "decision": "valid",
        "replaceable": True,
        "live": False,
        "repository_mutation": False,
    }


def _response_map(result_set: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        str(response["query_id"]): response
        for response in result_set["responses"]
    }


def _source_contribution(weight: float, rank: int) -> float:
    return weight / (RRF_K + rank)


def _fused_item(
    key: str,
    record: Mapping[str, Any],
    rank: int,
    repository: KernelRepository,
) -> dict[str, Any]:
    entity_id, raw_revision = key.rsplit("@", 1)
    revision = int(raw_revision)
    entity = repository.exact(entity_id, revision)
    provenance_entities = repository.provenance_sources(entity_id, revision)
    provenance = sorted(
        _exact_key(str(item["id"]), int(item["revision"]))
        for item in provenance_entities
    )
    if entity["type"] == "source" and not provenance:
        provenance = [key]
    components = record["components"]
    component_parts: list[str] = []
    for source in ("lexical", "structured"):
        component = components.get(source)
        if component is None:
            component_parts.append(f"{source}=not-ranked")
            continue
        component_parts.append(
            f"{source}=rank:{component['rank']},contribution:{component['contribution']:.12f}"
        )
    return {
        "id": entity_id,
        "revision": revision,
        "rank": rank,
        "score": _rounded(float(record["score"])),
        "type": entity["type"],
        "title": entity.get("title"),
        "status": entity.get("status"),
        "staleness": entity.get("staleness"),
        "review_level": entity.get("review_level"),
        "matched_fields": sorted(record["matched_fields"]),
        "explanation": (
            f"Equal-weight RRF(k={RRF_K}); "
            + "; ".join(component_parts)
            + f"; total={record['score']:.12f}."
        ),
        "provenance": provenance,
    }


def fuse_result_sets(
    manifest: Mapping[str, Any],
    lexical_results: Mapping[str, Any],
    structured_results: Mapping[str, Any],
    query_set: Mapping[str, Any],
    repository: KernelRepository,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
        raise KernelError("E-FUSION-LIMIT", "fusion limit must be nonnegative")
    lexical_map = _response_map(lexical_results)
    structured_map = _response_map(structured_results)
    responses: list[dict[str, Any]] = []
    for query in query_set["queries"]:
        query_id = str(query["id"])
        lexical_response = lexical_map[query_id]
        structured_response = structured_map[query_id]
        if query["expected"]["kind"] == "error":
            if lexical_response != structured_response:
                raise KernelError(
                    "E-FUSION-ERROR-DISAGREEMENT",
                    f"accepted inputs disagree on error behavior for {query_id}",
                )
            responses.append(dict(lexical_response))
            continue
        candidates: dict[str, dict[str, Any]] = {}
        for source, response, weight in (
            ("lexical", lexical_response, LEXICAL_WEIGHT),
            ("structured", structured_response, STRUCTURED_WEIGHT),
        ):
            if response.get("outcome") != "ranked":
                raise KernelError(
                    "E-FUSION-INPUT-OUTCOME",
                    f"{source} input is not ranked for {query_id}",
                )
            for item in response["items"]:
                key = _exact_key(str(item["id"]), int(item["revision"]))
                contribution = _source_contribution(weight, int(item["rank"]))
                candidate = candidates.setdefault(
                    key,
                    {
                        "score": 0.0,
                        "components": {},
                        "matched_fields": set(),
                    },
                )
                candidate["score"] += contribution
                candidate["components"][source] = {
                    "rank": int(item["rank"]),
                    "raw_score": float(item["score"]),
                    "contribution": contribution,
                }
                candidate["matched_fields"].update(
                    f"{source}.{field}" for field in item["matched_fields"]
                )
        ordered = sorted(
            candidates.items(),
            key=lambda pair: (-float(pair[1]["score"]), pair[0]),
        )
        items = [
            _fused_item(key, record, rank, repository)
            for rank, (key, record) in enumerate(ordered[:limit], start=1)
        ]
        responses.append(
            {
                "query_id": query_id,
                "outcome": "ranked",
                "items": items,
            }
        )
    result_set = {
        "contract": RESULT_SET_CONTRACT,
        "query_set_id": query_set["id"],
        "query_set_version": query_set["version"],
        "index": {
            "contract": FUSION_MANIFEST_CONTRACT,
            "build_digest": manifest["build_digest"],
            "source_digest": manifest["source_digest"],
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
        _exact_key(str(item["id"]), int(item["revision"])): int(item["grade"])
        for item in expected["judgments"]
    }


def _query_metrics(
    response: Mapping[str, Any],
    judgments: Mapping[str, int],
    cutoff: int,
) -> dict[str, Any]:
    items = response["items"]
    grades = [
        int(judgments.get(_exact_key(str(item["id"]), int(item["revision"])), 0))
        for item in items
    ]
    first_relevant_rank = next(
        (index for index, grade in enumerate(grades, start=1) if grade > 0),
        None,
    )
    relevant_total = sum(1 for grade in judgments.values() if grade > 0)
    relevant_at_cutoff = sum(1 for grade in grades[:cutoff] if grade > 0)
    dcg = sum(
        (2**grade - 1) / math.log2(rank + 1)
        for rank, grade in enumerate(grades[:cutoff], start=1)
        if grade > 0
    )
    ideal = sorted(judgments.values(), reverse=True)[:cutoff]
    ideal_dcg = sum(
        (2**grade - 1) / math.log2(rank + 1)
        for rank, grade in enumerate(ideal, start=1)
        if grade > 0
    )
    return {
        "first_relevant_rank": first_relevant_rank,
        "reciprocal_rank": _rounded(1.0 / first_relevant_rank)
        if first_relevant_rank
        else 0.0,
        "relevant_at_cutoff": relevant_at_cutoff,
        "relevant_total": relevant_total,
        "recall_at_cutoff": _rounded(relevant_at_cutoff / relevant_total)
        if relevant_total
        else 0.0,
        "ndcg_at_cutoff": _rounded(dcg / ideal_dcg) if ideal_dcg else 0.0,
    }


def _compare_query_metrics(
    candidate: Mapping[str, Any],
    baseline: Mapping[str, Any],
) -> dict[str, Any]:
    deltas = {
        "reciprocal_rank": _rounded(
            float(candidate["reciprocal_rank"]) - float(baseline["reciprocal_rank"])
        ),
        "recall_at_cutoff": _rounded(
            float(candidate["recall_at_cutoff"])
            - float(baseline["recall_at_cutoff"])
        ),
        "ndcg_at_cutoff": _rounded(
            float(candidate["ndcg_at_cutoff"])
            - float(baseline["ndcg_at_cutoff"])
        ),
    }
    values = list(deltas.values())
    if any(value > 0 for value in values) and not any(value < 0 for value in values):
        outcome = "gain"
    elif any(value < 0 for value in values) and not any(value > 0 for value in values):
        outcome = "regression"
    elif any(value != 0 for value in values):
        outcome = "mixed"
    else:
        outcome = "unchanged"
    return {"outcome": outcome, "deltas": deltas}


def query_level_comparison(
    query_set: Mapping[str, Any],
    lexical_results: Mapping[str, Any],
    structured_results: Mapping[str, Any],
    fused_results: Mapping[str, Any],
    cutoff: int,
) -> list[dict[str, Any]]:
    maps = {
        "lexical": _response_map(lexical_results),
        "structured": _response_map(structured_results),
        "fusion": _response_map(fused_results),
    }
    output: list[dict[str, Any]] = []
    for query in query_set["queries"]:
        if query["expected"]["kind"] != "ranked":
            continue
        query_id = str(query["id"])
        judgments = _judgments(query)
        metrics = {
            name: _query_metrics(responses[query_id], judgments, cutoff)
            for name, responses in maps.items()
        }
        output.append(
            {
                "query_id": query_id,
                "slice": query["slice"],
                "difficulty": query["difficulty"],
                "metrics": metrics,
                "fusion_vs_lexical": _compare_query_metrics(
                    metrics["fusion"], metrics["lexical"]
                ),
                "fusion_vs_structured": _compare_query_metrics(
                    metrics["fusion"], metrics["structured"]
                ),
            }
        )
    return output


def _metric_delta(
    candidate: Mapping[str, Any],
    baseline: Mapping[str, Any],
) -> dict[str, float]:
    return {
        key: _rounded(float(candidate[key]) - float(baseline[key]))
        for key in sorted(candidate)
        if key in baseline
    }


def _candidate_recommendation(delta_from_structured: Mapping[str, float]) -> str:
    core = [
        float(delta_from_structured[key])
        for key in (
            "precision_at_k",
            "recall_at_k",
            "mean_reciprocal_rank",
            "ndcg_at_k",
        )
    ]
    if all(value >= 0 for value in core) and any(value > 0 for value in core):
        return "retain-candidate-quality-improves-or-matches-structured"
    if all(value <= 0 for value in core):
        return "reject-candidate-no-quality-gain-over-structured"
    return "retain-candidate-mixed-quality-requires-query-review"


def run_rank_fusion_candidate(
    canonical_root: Path,
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    cutoff: int = DEFAULT_CUTOFF,
    limit: int = DEFAULT_LIMIT,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    repository, lexical_index, structured_index = _prepare_inputs(
        canonical_root,
        query_set,
        lexical_baseline,
        structured_baseline,
    )
    manifest = build_fusion_manifest(
        canonical_root,
        query_set,
        lexical_baseline,
        structured_baseline,
    )
    manifest_validation = validate_fusion_manifest(
        manifest,
        query_set,
        lexical_baseline,
        structured_baseline,
        repository,
    )
    lexical_results = run_lexical_queries(
        lexical_index,
        query_set,
        repository,
        limit=limit,
    )
    structured_results = run_structured_queries(
        structured_index,
        query_set,
        repository,
        limit=limit,
    )
    fused_results = fuse_result_sets(
        manifest,
        lexical_results,
        structured_results,
        query_set,
        repository,
        limit=limit,
    )
    metric_report = evaluate_result_set(
        fused_results,
        query_set,
        repository,
        cutoff=cutoff,
    )
    lexical_metrics = lexical_baseline["metrics"]
    structured_metrics = structured_baseline["metrics"]
    delta_from_lexical = _metric_delta(metric_report["metrics"], lexical_metrics)
    delta_from_structured = _metric_delta(metric_report["metrics"], structured_metrics)
    query_comparison = query_level_comparison(
        query_set,
        lexical_results,
        structured_results,
        fused_results,
        cutoff,
    )
    input_ranked_items = sum(
        len(response.get("items", []))
        for result_set in (lexical_results, structured_results)
        for response in result_set["responses"]
        if response["outcome"] == "ranked"
    )
    output_ranked_items = sum(
        len(response.get("items", []))
        for response in fused_results["responses"]
        if response["outcome"] == "ranked"
    )
    report = {
        "contract": FUSION_REPORT_CONTRACT,
        "mode": MODE,
        "decision": "rank-fusion-candidate",
        "recommendation": _candidate_recommendation(delta_from_structured),
        "query_set_id": query_set["id"],
        "query_set_version": query_set["version"],
        "entity_count": repository.runtime["entity_count"],
        "query_count": len(query_set["queries"]),
        "cutoff": cutoff,
        "limit": limit,
        "manifest_validation": manifest_validation,
        "result_set_sha256": metric_report["result_set_sha256"],
        "metrics": metric_report["metrics"],
        "lexical_baseline_metrics": dict(lexical_metrics),
        "structured_baseline_metrics": dict(structured_metrics),
        "metric_delta_from_lexical": delta_from_lexical,
        "metric_delta_from_structured": delta_from_structured,
        "query_level_comparison": query_comparison,
        "tie_count": metric_report["tie_count"],
        "complexity": {
            "input_ranked_items": input_ranked_items,
            "output_ranked_items": output_ranked_items,
            "additional_index_documents": 0,
            "additional_index_terms": 0,
            "embedding_dimensions": 0,
            "external_calls": 0,
            "manifest_bytes": len(render_json(manifest).encode("utf-8")),
            "result_set_bytes": len(render_json(fused_results).encode("utf-8")),
            "metric_report_bytes": len(render_json(metric_report).encode("utf-8")),
        },
        "failure_behavior": [
            "exact unavailable-revision error is preserved from both accepted inputs",
            "input baseline identity mismatch fails before fusion",
            "method or weight drift fails manifest validation",
            "manifest digest mismatch fails validation",
            "authority escalation fails validation",
        ],
        "inspectability": {
            "component_ranks_visible": True,
            "component_contributions_visible": True,
            "matched_fields_source_prefixed": True,
            "raw_score_blending": False,
        },
        "deterministic": True,
        "accepted_judgments_unchanged": True,
        "replaceable": True,
        "quality_claim": "bounded-reference-fixture-only",
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "learned_weights": False,
        "judgment_specific_tuning": False,
        "advisory_only": True,
        "live": False,
        "repository_mutation": False,
    }
    return manifest, fused_results, metric_report, report


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
    parser.add_argument(
        "--structured-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/structured-baseline.json"),
    )
    parser.add_argument("--cutoff", type=int, default=DEFAULT_CUTOFF)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--manifest-output", type=Path)
    parser.add_argument("--result-output", type=Path)
    parser.add_argument("--metric-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args(argv)
    try:
        query_set = load_json(args.query_set)
        lexical_baseline = load_json(args.lexical_baseline)
        structured_baseline = load_json(args.structured_baseline)
        manifest, results, metrics, report = run_rank_fusion_candidate(
            args.canonical_root,
            query_set,
            lexical_baseline,
            structured_baseline,
            cutoff=args.cutoff,
            limit=args.limit,
        )
        if not any(
            (
                args.manifest_output,
                args.result_output,
                args.metric_output,
                args.report_output,
            )
        ):
            _write(None, report)
        else:
            if args.manifest_output is not None:
                _write(args.manifest_output, manifest)
            if args.result_output is not None:
                _write(args.result_output, results)
            if args.metric_output is not None:
                _write(args.metric_output, metrics)
            if args.report_output is not None:
                _write(args.report_output, report)
        return 0
    except (KernelError, OSError, json.JSONDecodeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
