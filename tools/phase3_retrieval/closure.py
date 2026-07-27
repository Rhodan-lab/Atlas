#!/usr/bin/env python3
"""Deterministic Phase 3 closure proof and Phase 4 entry recommendation."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase3_retrieval.contracts import MODE, validate_query_set
from tools.phase3_retrieval.fusion import run_rank_fusion_candidate
from tools.phase3_retrieval.lexical import _json_sha256, run_lexical_baseline
from tools.phase3_retrieval.research import validate_fixture_bundle
from tools.phase3_retrieval.structured import run_structured_baseline

COMPLETION_CONTRACT = "atlas-phase3-completion-report/0.1"
COMPLETION_VALIDATION_CONTRACT = "atlas-phase3-completion-validation/0.1"


def _require_contract(record: Mapping[str, Any], contract: str, code: str) -> None:
    if record.get("contract") != contract:
        raise KernelError(code, f"expected {contract!r}")
    if record.get("mode") != MODE:
        raise KernelError(code, f"mode must be {MODE!r}")
    if record.get("live") is not False or record.get("repository_mutation") is not False:
        raise KernelError(code, "evidence must remain non-live and non-mutating")


def _compare_metrics(observed: Mapping[str, Any], expected: Mapping[str, Any], code: str) -> None:
    if dict(observed) != dict(expected):
        raise KernelError(code, "observed metrics differ from pinned evidence")


def _visibility(result_set: Mapping[str, Any], code: str) -> dict[str, int]:
    ranked_responses = 0
    ranked_items = 0
    error_responses = 0
    required = {
        "id",
        "revision",
        "rank",
        "score",
        "type",
        "title",
        "status",
        "staleness",
        "review_level",
        "matched_fields",
        "explanation",
        "provenance",
    }
    for response in result_set.get("responses", []):
        outcome = response.get("outcome")
        if outcome == "error":
            error_responses += 1
            continue
        if outcome != "ranked":
            raise KernelError(code, "unsupported response outcome")
        ranked_responses += 1
        for item in response.get("items", []):
            ranked_items += 1
            if not required <= set(item):
                raise KernelError(code, "ranked item hides required authority or explanation fields")
            if not isinstance(item["revision"], int) or item["revision"] < 1:
                raise KernelError(code, "ranked item requires positive exact revision")
            if not isinstance(item["matched_fields"], list) or not item["matched_fields"]:
                raise KernelError(code, "ranked item requires matched fields")
            if not isinstance(item["explanation"], str) or not item["explanation"].strip():
                raise KernelError(code, "ranked item requires explanation")
            if not isinstance(item["provenance"], list):
                raise KernelError(code, "ranked item requires provenance list")
    return {
        "ranked_responses": ranked_responses,
        "ranked_items": ranked_items,
        "error_responses": error_responses,
    }


def run_phase3_closure(
    canonical_root: Path,
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    fusion_baseline: Mapping[str, Any],
    research_fixtures: Mapping[str, Any],
    research_baseline: Mapping[str, Any],
) -> dict[str, Any]:
    runtime = compile_canonical(canonical_root)
    repository = KernelRepository(runtime)
    query_validation = validate_query_set(query_set, repository)

    _require_contract(lexical_baseline, "atlas-phase3-lexical-baseline/0.1", "E-PHASE3-LEXICAL")
    _require_contract(structured_baseline, "atlas-phase3-structured-baseline/0.1", "E-PHASE3-STRUCTURED")
    _require_contract(fusion_baseline, "atlas-phase3-rank-fusion-candidate/0.1", "E-PHASE3-FUSION")
    _require_contract(research_baseline, "atlas-phase3-research-foundation-baseline/0.1", "E-PHASE3-RESEARCH")

    lexical_index, lexical_results, lexical_metrics, lexical_report = run_lexical_baseline(
        canonical_root,
        query_set,
        cutoff=int(lexical_baseline["cutoff"]),
        limit=int(lexical_baseline["limit"]),
    )
    if lexical_index["build_digest"] != lexical_baseline["index_build_digest"]:
        raise KernelError("E-PHASE3-LEXICAL", "lexical index digest differs from accepted evidence")
    if lexical_metrics["result_set_sha256"] != lexical_baseline["result_set_sha256"]:
        raise KernelError("E-PHASE3-LEXICAL", "lexical result digest differs from accepted evidence")
    _compare_metrics(lexical_metrics["metrics"], lexical_baseline["metrics"], "E-PHASE3-LEXICAL")
    lexical_visibility = _visibility(lexical_results, "E-PHASE3-LEXICAL-VISIBILITY")

    structured_index, structured_results, structured_metrics, structured_report = run_structured_baseline(
        canonical_root,
        query_set,
        lexical_baseline,
        cutoff=int(structured_baseline["cutoff"]),
        limit=int(structured_baseline["limit"]),
    )
    if structured_index["build_digest"] != structured_baseline["index_build_digest"]:
        raise KernelError("E-PHASE3-STRUCTURED", "structured index digest differs from accepted evidence")
    if structured_metrics["result_set_sha256"] != structured_baseline["result_set_sha256"]:
        raise KernelError("E-PHASE3-STRUCTURED", "structured result digest differs from accepted evidence")
    _compare_metrics(structured_metrics["metrics"], structured_baseline["metrics"], "E-PHASE3-STRUCTURED")
    structured_visibility = _visibility(structured_results, "E-PHASE3-STRUCTURED-VISIBILITY")

    fusion_manifest, fusion_results, fusion_metrics, fusion_report = run_rank_fusion_candidate(
        canonical_root,
        query_set,
        lexical_baseline,
        structured_baseline,
        cutoff=int(fusion_baseline["cutoff"]),
        limit=int(fusion_baseline["limit"]),
    )
    if fusion_manifest["build_digest"] != fusion_baseline["fusion_manifest_build_digest"]:
        raise KernelError("E-PHASE3-FUSION", "fusion manifest digest differs from pinned evidence")
    if fusion_metrics["result_set_sha256"] != fusion_baseline["fusion_result_set_sha256"]:
        raise KernelError("E-PHASE3-FUSION", "fusion result digest differs from pinned evidence")
    _compare_metrics(fusion_metrics["metrics"], fusion_baseline["metrics"], "E-PHASE3-FUSION")
    if fusion_baseline.get("decision") != "rejected":
        raise KernelError("E-PHASE3-FUSION", "fusion rejection is not preserved")
    if fusion_report.get("recommendation") != "reject-candidate-no-quality-gain-over-structured":
        raise KernelError("E-PHASE3-FUSION", "fusion recommendation differs from pinned evidence")
    fusion_visibility = _visibility(fusion_results, "E-PHASE3-FUSION-VISIBILITY")

    research_report, filter_results = validate_fixture_bundle(
        research_fixtures,
        repository,
        query_set,
        structured_baseline,
    )
    if research_report["report_digest"] != research_baseline["report_digest"]:
        raise KernelError("E-PHASE3-RESEARCH", "research report digest differs from pinned evidence")
    if research_report["counts"] != research_baseline["counts"]:
        raise KernelError("E-PHASE3-RESEARCH", "research counts differ from pinned evidence")
    if research_report["filter_result_digests"] != research_baseline["filter_result_digests"]:
        raise KernelError("E-PHASE3-RESEARCH", "filter result digests differ from pinned evidence")
    if [item["entity_count_after"] for item in filter_results] != research_baseline["filter_result_counts"]:
        raise KernelError("E-PHASE3-RESEARCH", "filter result counts differ from pinned evidence")

    exit_gates = {
        "documented_relevance_collection": (
            query_validation["query_count"] == 13
            and query_validation["entity_count"] == 34
            and query_validation["positive_judgment_count"] == 26
        ),
        "review_status_and_provenance_visible": (
            lexical_visibility["ranked_items"] > 0
            and structured_visibility["ranked_items"] > 0
            and fusion_visibility["ranked_items"] > 0
        ),
        "ranking_behavior_explainable": (
            lexical_report["tie_count"] == 0
            and structured_report["tie_count"] == 0
            and fusion_report["inspectability"]["component_ranks_visible"] is True
            and fusion_report["inspectability"]["component_contributions_visible"] is True
        ),
        "specialized_boundaries_pass_policy": (
            lexical_report["external_services"] is False
            and lexical_report["embeddings"] is False
            and lexical_report["vector_database"] is False
            and structured_report["external_services"] is False
            and structured_report["embeddings"] is False
            and structured_report["vector_database"] is False
            and structured_report["canonical_body_indexed"] is False
            and fusion_report["external_services"] is False
            and fusion_report["embeddings"] is False
            and fusion_report["vector_database"] is False
            and fusion_baseline["decision"] == "rejected"
        ),
        "retrieval_failure_cannot_corrupt_authority": (
            lexical_metrics["metrics"]["unavailable_revision_rate"] == 1.0
            and structured_metrics["metrics"]["unavailable_revision_rate"] == 1.0
            and fusion_metrics["metrics"]["unavailable_revision_rate"] == 1.0
            and research_report["automatic_merge_or_resolution"] is False
            and research_report["canonical_copy_authority"] is False
            and research_report["repository_mutation"] is False
        ),
        "filters_and_research_trails_operational": (
            research_report["counts"]["filters"] == 4
            and research_report["counts"]["filter_result_items"] == 9
            and research_report["counts"]["trails"] == 1
            and research_report["counts"]["trail_entries"] == 5
            and research_report["exact_revision_preserved"] is True
        ),
        "candidate_discovery_advisory": (
            research_report["counts"]["contradiction_candidates"] == 1
            and research_report["counts"]["duplicate_candidates"] == 1
            and research_report["candidate_authority"] == "advisory-only"
            and research_report["automatic_merge_or_resolution"] is False
        ),
        "generated_artifacts_replaceable": (
            lexical_report["rebuild_verified"] is True
            and structured_report["rebuild_verified"] is True
            and lexical_report["replaceable"] is True
            and structured_report["replaceable"] is True
            and fusion_report["replaceable"] is True
        ),
    }
    if not all(exit_gates.values()):
        failed = sorted(key for key, passed in exit_gates.items() if not passed)
        raise KernelError("E-PHASE3-EXIT-GATE", f"Phase 3 exit gates failed: {failed}")

    report: dict[str, Any] = {
        "contract": COMPLETION_CONTRACT,
        "mode": MODE,
        "phase": 3,
        "state": "closure-candidate",
        "decision": "proceed-phase4-interactive-experience",
        "preferred_bounded_retrieval": "structured-field-baseline",
        "semantic_infrastructure_decision": "defer-until-broader-benchmark-and-architecture-approval",
        "source_digest": runtime["source_digest"],
        "entity_count": runtime["entity_count"],
        "query_set": {
            "id": query_set["id"],
            "version": query_set["version"],
            "semantic_sha256": _json_sha256(query_set),
        },
        "accepted_workstreams": [1, 2, 3, 5],
        "evaluated_rejected_candidates": [
            {
                "workstream": 4,
                "candidate": "equal-weight-reciprocal-rank-fusion",
                "decision": fusion_baseline["decision"],
                "recommendation": fusion_baseline["recommendation"],
            }
        ],
        "evidence": {
            "lexical": {
                "baseline_sha256": _json_sha256(lexical_baseline),
                "index_build_digest": lexical_index["build_digest"],
                "result_set_sha256": lexical_metrics["result_set_sha256"],
                "metrics": lexical_metrics["metrics"],
                "visibility": lexical_visibility,
            },
            "structured": {
                "baseline_sha256": _json_sha256(structured_baseline),
                "index_build_digest": structured_index["build_digest"],
                "result_set_sha256": structured_metrics["result_set_sha256"],
                "metrics": structured_metrics["metrics"],
                "visibility": structured_visibility,
            },
            "rank_fusion": {
                "baseline_sha256": _json_sha256(fusion_baseline),
                "manifest_build_digest": fusion_manifest["build_digest"],
                "result_set_sha256": fusion_metrics["result_set_sha256"],
                "metrics": fusion_metrics["metrics"],
                "visibility": fusion_visibility,
                "decision": fusion_baseline["decision"],
            },
            "research_foundations": {
                "baseline_sha256": _json_sha256(research_baseline),
                "fixture_sha256": _json_sha256(research_fixtures),
                "report_digest": research_report["report_digest"],
                "counts": research_report["counts"],
                "negative_case_count": len(research_report["negative_validations"]),
            },
        },
        "exit_gates": exit_gates,
        "phase4_entry_boundary": {
            "purpose": "build a unified Principia and Atlas interactive experience over proven semantics",
            "atlas_semantics_authoritative": True,
            "principia_status_separate": True,
            "exact_cross_repository_references": True,
            "impact_warnings_required": True,
            "graph_visualization_optional": True,
            "accessibility_and_failure_tests_required": True,
            "local_first": True,
            "production_retrieval_quality_claim": False,
            "vector_database": False,
            "live_principia_dependency": False,
            "canonical_mutation": False,
        },
        "review_policy": {
            "active_review_level": "ai-reviewed",
            "human_verified": False,
            "human_review_required_for_phase3_closure": False,
        },
        "retrieval_authority": "advisory-only",
        "exact_revision_required": True,
        "replaceable": True,
        "automatic_status_change": False,
        "automatic_merge_or_resolution": False,
        "automatic_release_action": False,
        "canonical_copy_authority": False,
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "live": False,
        "repository_mutation": False,
    }
    report["report_digest"] = _json_sha256(report)
    return report


def validate_completion_report(report: Mapping[str, Any]) -> dict[str, Any]:
    if report.get("contract") != COMPLETION_CONTRACT:
        raise KernelError("E-PHASE3-COMPLETION-CONTRACT", f"expected {COMPLETION_CONTRACT!r}")
    if report.get("mode") != MODE or report.get("phase") != 3:
        raise KernelError("E-PHASE3-COMPLETION-MODE", "completion report identity is invalid")
    if report.get("state") != "closure-candidate":
        raise KernelError("E-PHASE3-COMPLETION-STATE", "completion report must be a closure candidate")
    if report.get("decision") != "proceed-phase4-interactive-experience":
        raise KernelError("E-PHASE3-COMPLETION-DECISION", "completion decision is unsupported")
    gates = report.get("exit_gates")
    if not isinstance(gates, Mapping) or not gates or not all(value is True for value in gates.values()):
        raise KernelError("E-PHASE3-COMPLETION-GATES", "all Phase 3 exit gates must pass")
    boundary = report.get("phase4_entry_boundary")
    if not isinstance(boundary, Mapping):
        raise KernelError("E-PHASE3-PHASE4-BOUNDARY", "completion report requires Phase 4 boundary")
    if (
        boundary.get("atlas_semantics_authoritative") is not True
        or boundary.get("principia_status_separate") is not True
        or boundary.get("production_retrieval_quality_claim") is not False
        or boundary.get("vector_database") is not False
        or boundary.get("live_principia_dependency") is not False
        or boundary.get("canonical_mutation") is not False
    ):
        raise KernelError("E-PHASE3-PHASE4-BOUNDARY", "Phase 4 entry boundary is unsafe")
    expected_fields = {
        "retrieval_authority": "advisory-only",
        "exact_revision_required": True,
        "replaceable": True,
        "automatic_status_change": False,
        "automatic_merge_or_resolution": False,
        "automatic_release_action": False,
        "canonical_copy_authority": False,
        "external_services": False,
        "embeddings": False,
        "vector_database": False,
        "live": False,
        "repository_mutation": False,
    }
    for field, expected in expected_fields.items():
        if report.get(field) != expected:
            raise KernelError("E-PHASE3-COMPLETION-AUTHORITY", f"completion requires {field}={expected!r}")
    digest = report.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError("E-PHASE3-COMPLETION-DIGEST", "report_digest must be a SHA-256")
    unsigned = dict(report)
    unsigned.pop("report_digest", None)
    if _json_sha256(unsigned) != digest:
        raise KernelError("E-PHASE3-COMPLETION-DIGEST", "completion report digest mismatch")
    return {
        "contract": COMPLETION_VALIDATION_CONTRACT,
        "validated_contract": COMPLETION_CONTRACT,
        "report_digest": digest,
        "decision": "valid-phase3-closure-candidate",
        "phase4_recommendation": report["decision"],
        "preferred_bounded_retrieval": report["preferred_bounded_retrieval"],
        "semantic_infrastructure_decision": report["semantic_infrastructure_decision"],
        "live": False,
        "repository_mutation": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument("--query-set", type=Path, default=Path("content/fixtures/phase3_retrieval/reference-query-set.v01.json"))
    parser.add_argument("--lexical-baseline", type=Path, default=Path("content/fixtures/phase3_retrieval/lexical-baseline.json"))
    parser.add_argument("--structured-baseline", type=Path, default=Path("content/fixtures/phase3_retrieval/structured-baseline.json"))
    parser.add_argument("--fusion-baseline", type=Path, default=Path("content/fixtures/phase3_retrieval/rank-fusion.json"))
    parser.add_argument("--research-fixtures", type=Path, default=Path("content/fixtures/phase3_retrieval/research-foundations.v01.json"))
    parser.add_argument("--research-baseline", type=Path, default=Path("content/fixtures/phase3_retrieval/research-foundations-baseline.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = run_phase3_closure(
            args.canonical_root,
            load_json(args.query_set),
            load_json(args.lexical_baseline),
            load_json(args.structured_baseline),
            load_json(args.fusion_baseline),
            load_json(args.research_fixtures),
            load_json(args.research_baseline),
        )
        validation = validate_completion_report(report)
        rendered = render_json(report)
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"wrote={args.output}")
            print(f"phase3-closure={validation['decision']}")
            print(f"phase4-recommendation={validation['phase4_recommendation']}")
        return 0
    except (KernelError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
