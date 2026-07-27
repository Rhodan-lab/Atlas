from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase3_retrieval.fusion import (
    FUSION_MANIFEST_CONTRACT,
    FUSION_SCORING_CONTRACT,
    LEXICAL_WEIGHT,
    RRF_K,
    STRUCTURED_WEIGHT,
    build_fusion_manifest,
    run_rank_fusion_candidate,
    validate_fusion_manifest,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
QUERY_SET = ROOT / "content" / "fixtures" / "phase3_retrieval" / "reference-query-set.v01.json"
LEXICAL_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "lexical-baseline.json"
STRUCTURED_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "structured-baseline.json"


class RankFusionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)
        cls.repository = KernelRepository(cls.runtime)
        cls.query_set = load_json(QUERY_SET)
        cls.lexical_baseline = load_json(LEXICAL_BASELINE)
        cls.structured_baseline = load_json(STRUCTURED_BASELINE)

    def test_manifest_is_deterministic_and_predeclared(self) -> None:
        first = build_fusion_manifest(
            CANONICAL,
            self.query_set,
            self.lexical_baseline,
            self.structured_baseline,
        )
        second = build_fusion_manifest(
            CANONICAL,
            self.query_set,
            self.lexical_baseline,
            self.structured_baseline,
        )
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(first["contract"], FUSION_MANIFEST_CONTRACT)
        self.assertEqual(first["method"]["contract"], FUSION_SCORING_CONTRACT)
        self.assertEqual(first["method"]["rrf_k"], RRF_K)
        self.assertEqual(
            first["method"]["weights"],
            {"lexical": LEXICAL_WEIGHT, "structured": STRUCTURED_WEIGHT},
        )
        self.assertFalse(first["method"]["raw_score_blending"])
        validation = validate_fusion_manifest(
            first,
            self.query_set,
            self.lexical_baseline,
            self.structured_baseline,
            self.repository,
        )
        self.assertEqual(validation["decision"], "valid")

    def test_candidate_results_and_metrics_validate(self) -> None:
        manifest, results, metrics, report = run_rank_fusion_candidate(
            CANONICAL,
            self.query_set,
            self.lexical_baseline,
            self.structured_baseline,
            cutoff=5,
            limit=10,
        )
        self.assertEqual(len(results["responses"]), 13)
        self.assertEqual(metrics["evaluated_ranked_queries"], 12)
        self.assertEqual(metrics["expected_error_queries"], 1)
        self.assertEqual(report["decision"], "rank-fusion-candidate")
        self.assertEqual(report["manifest_validation"]["build_digest"], manifest["build_digest"])
        self.assertEqual(len(report["query_level_comparison"]), 12)
        self.assertEqual(report["complexity"]["additional_index_documents"], 0)
        self.assertEqual(report["complexity"]["additional_index_terms"], 0)
        self.assertEqual(report["complexity"]["embedding_dimensions"], 0)
        self.assertFalse(report["external_services"])
        self.assertFalse(report["embeddings"])
        self.assertFalse(report["vector_database"])

    def test_component_ranks_are_inspectable(self) -> None:
        _, results, _, _ = run_rank_fusion_candidate(
            CANONICAL,
            self.query_set,
            self.lexical_baseline,
            self.structured_baseline,
        )
        ranked = next(
            response for response in results["responses"] if response["outcome"] == "ranked"
        )
        item = ranked["items"][0]
        self.assertIn("RRF(k=60)", item["explanation"])
        self.assertTrue(
            any(field.startswith("lexical.") or field.startswith("structured.") for field in item["matched_fields"])
        )

    def test_unavailable_revision_error_is_preserved(self) -> None:
        _, results, metrics, _ = run_rank_fusion_candidate(
            CANONICAL,
            self.query_set,
            self.lexical_baseline,
            self.structured_baseline,
        )
        errors = [response for response in results["responses"] if response["outcome"] == "error"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["error"], "E-REVISION-MISSING")
        self.assertEqual(metrics["metrics"]["unavailable_revision_rate"], 1.0)

    def test_method_drift_is_rejected(self) -> None:
        manifest = build_fusion_manifest(
            CANONICAL,
            self.query_set,
            self.lexical_baseline,
            self.structured_baseline,
        )
        tampered = copy.deepcopy(manifest)
        tampered["method"]["weights"]["structured"] = 2.0
        with self.assertRaises(KernelError) as context:
            validate_fusion_manifest(
                tampered,
                self.query_set,
                self.lexical_baseline,
                self.structured_baseline,
                self.repository,
            )
        self.assertEqual(context.exception.code, "E-FUSION-METHOD")

    def test_baseline_drift_is_rejected(self) -> None:
        tampered = copy.deepcopy(self.structured_baseline)
        tampered["index_build_digest"] = "0" * 64
        with self.assertRaises(KernelError) as context:
            build_fusion_manifest(
                CANONICAL,
                self.query_set,
                self.lexical_baseline,
                tampered,
            )
        self.assertEqual(context.exception.code, "E-FUSION-STRUCTURED-INDEX")


if __name__ == "__main__":
    unittest.main()
