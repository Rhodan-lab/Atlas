from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import (
    KernelError,
    KernelRepository,
    compile_canonical,
    load_json,
    render_json,
)
from tools.phase3_retrieval.contracts import validate_metric_report, validate_result_set
from tools.phase3_retrieval.lexical import (
    LEXICAL_BASELINE_REPORT_CONTRACT,
    LEXICAL_INDEX_CONTRACT,
    build_lexical_index,
    evaluate_result_set,
    run_lexical_baseline,
    run_lexical_queries,
    search_lexical_index,
    tokenize,
    validate_lexical_index,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
QUERY_SET_PATH = (
    ROOT / "content" / "fixtures" / "phase3_retrieval" / "reference-query-set.v01.json"
)


class LexicalBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)
        cls.repository = KernelRepository(cls.runtime)
        cls.query_set = load_json(QUERY_SET_PATH)
        cls.index = build_lexical_index(CANONICAL)

    def test_tokenizer_is_explicit_and_deterministic(self) -> None:
        self.assertEqual(
            tokenize("Why does delayed-feedback repeat in a REAL system?"),
            ["delayed", "feedback", "repeat", "real", "system"],
        )
        self.assertEqual(tokenize("catalase pH pH"), ["catalase", "ph", "ph"])

    def test_index_is_deterministic_and_valid(self) -> None:
        second = build_lexical_index(CANONICAL)
        self.assertEqual(render_json(self.index), render_json(second))
        report = validate_lexical_index(self.index, self.repository)
        self.assertEqual(self.index["contract"], LEXICAL_INDEX_CONTRACT)
        self.assertEqual(report["decision"], "valid")
        self.assertEqual(report["entity_count"], 34)
        self.assertGreater(report["term_count"], 0)
        self.assertTrue(report["replaceable"])
        self.assertFalse(report["live"])
        self.assertFalse(report["repository_mutation"])

    def test_index_deletion_and_rebuild_is_lossless(self) -> None:
        rendered = render_json(self.index)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "lexical-index.json"
            path.write_text(rendered, encoding="utf-8")
            path.unlink()
            rebuilt = build_lexical_index(CANONICAL)
            path.write_text(render_json(rebuilt), encoding="utf-8")
            self.assertEqual(path.read_text(encoding="utf-8"), rendered)

    def test_corrupted_index_is_rejected(self) -> None:
        corrupted = copy.deepcopy(self.index)
        corrupted["build_digest"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-LEXICAL-BUILD-DIGEST"):
            validate_lexical_index(corrupted, self.repository)

        mutated = copy.deepcopy(self.index)
        mutated["canonical_mutation"] = True
        unsigned = copy.deepcopy(mutated)
        unsigned.pop("build_digest")
        with self.assertRaisesRegex(KernelError, "E-LEXICAL-INDEX-AUTHORITY"):
            validate_lexical_index(mutated, self.repository)

    def test_search_is_transparent_and_tie_ordered(self) -> None:
        first = search_lexical_index(
            self.index,
            "catalase optimum assay scope",
            limit=10,
        )
        second = search_lexical_index(
            self.index,
            "catalase optimum assay scope",
            limit=10,
        )
        self.assertEqual(first, second)
        self.assertTrue(first)
        self.assertIn("title", first[0]["matched_fields"])
        for left, right in zip(first, first[1:]):
            if left["score"] == right["score"]:
                self.assertLess(left["document"]["key"], right["document"]["key"])
            else:
                self.assertGreater(left["score"], right["score"])

    def test_result_and_metric_reports_satisfy_accepted_contracts(self) -> None:
        results = run_lexical_queries(
            self.index,
            self.query_set,
            self.repository,
            limit=10,
        )
        result_validation = validate_result_set(
            results,
            self.query_set,
            self.repository,
        )
        self.assertEqual(result_validation["decision"], "valid")
        self.assertEqual(result_validation["response_count"], 13)
        metrics = evaluate_result_set(
            results,
            self.query_set,
            self.repository,
            cutoff=5,
        )
        metric_validation = validate_metric_report(
            metrics,
            self.query_set,
            self.repository,
        )
        self.assertEqual(metric_validation["decision"], "valid")
        self.assertEqual(metrics["evaluated_ranked_queries"], 12)
        self.assertEqual(metrics["expected_error_queries"], 1)
        self.assertEqual(metrics["metrics"]["unavailable_revision_rate"], 1.0)
        for value in metrics["metrics"].values():
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_full_baseline_is_deterministic_and_bounded(self) -> None:
        first = run_lexical_baseline(CANONICAL, self.query_set)
        second = run_lexical_baseline(CANONICAL, self.query_set)
        self.assertEqual(
            [render_json(value) for value in first],
            [render_json(value) for value in second],
        )
        report = first[3]
        self.assertEqual(report["contract"], LEXICAL_BASELINE_REPORT_CONTRACT)
        self.assertEqual(report["decision"], "lexical-baseline-candidate")
        self.assertTrue(report["deterministic_index"])
        self.assertTrue(report["rebuild_verified"])
        self.assertTrue(report["replaceable"])
        self.assertFalse(report["external_services"])
        self.assertFalse(report["embeddings"])
        self.assertFalse(report["vector_database"])
        self.assertFalse(report["judgment_specific_tuning"])
        self.assertTrue(report["advisory_only"])
        self.assertFalse(report["live"])
        self.assertFalse(report["repository_mutation"])


if __name__ == "__main__":
    unittest.main()
