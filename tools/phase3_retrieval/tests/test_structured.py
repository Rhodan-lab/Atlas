from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase3_retrieval.structured import (
    STRUCTURED_INDEX_CONTRACT,
    build_structured_index,
    run_structured_baseline,
    run_structured_queries,
    validate_structured_index,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
QUERY_SET = ROOT / "content" / "fixtures" / "phase3_retrieval" / "reference-query-set.v01.json"
LEXICAL_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "lexical-baseline.json"


class StructuredBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)
        cls.repository = KernelRepository(cls.runtime)
        cls.query_set = load_json(QUERY_SET)
        cls.lexical_baseline = load_json(LEXICAL_BASELINE)

    def test_build_is_deterministic_and_valid(self) -> None:
        first = build_structured_index(CANONICAL)
        second = build_structured_index(CANONICAL)
        self.assertEqual(render_json(first), render_json(second))
        validation = validate_structured_index(first, self.repository)
        self.assertEqual(validation["decision"], "valid")
        self.assertEqual(first["contract"], STRUCTURED_INDEX_CONTRACT)
        self.assertFalse(first["field_policy"]["canonical_body_indexed"])

    def test_structured_fields_cover_graph_and_provenance(self) -> None:
        index = build_structured_index(CANONICAL)
        documents = {document["key"]: document for document in index["documents"]}
        target = documents["claim:en:catalase-optimum-requires-assay-scope@1"]
        self.assertIn("assay", target["fields"]["primary"])
        self.assertIn("src", target["fields"]["graph"])
        self.assertIn("catalase", target["fields"]["provenance"])
        self.assertNotIn("body", target["fields"])

    def test_queries_and_metrics_validate(self) -> None:
        index, results, metrics, report = run_structured_baseline(
            CANONICAL,
            self.query_set,
            self.lexical_baseline,
            cutoff=5,
            limit=10,
        )
        self.assertEqual(len(results["responses"]), 13)
        self.assertEqual(metrics["evaluated_ranked_queries"], 12)
        self.assertEqual(metrics["expected_error_queries"], 1)
        self.assertEqual(report["decision"], "structured-baseline-candidate")
        self.assertFalse(report["canonical_body_indexed"])
        self.assertTrue(report["accepted_judgments_unchanged"])
        self.assertEqual(report["index_validation"]["build_digest"], index["build_digest"])

    def test_unavailable_revision_does_not_fall_back_to_latest(self) -> None:
        index = build_structured_index(CANONICAL)
        results = run_structured_queries(index, self.query_set, self.repository, limit=10)
        errors = [response for response in results["responses"] if response["outcome"] == "error"]
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["error"], "E-ENTITY-REVISION-NOT-FOUND")

    def test_delete_and_rebuild_is_byte_identical(self) -> None:
        first = build_structured_index(CANONICAL)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "structured-index.json"
            path.write_text(render_json(first), encoding="utf-8")
            first_bytes = path.read_bytes()
            path.unlink()
            rebuilt = build_structured_index(CANONICAL)
            path.write_text(render_json(rebuilt), encoding="utf-8")
            self.assertEqual(first_bytes, path.read_bytes())

    def test_tampered_index_is_rejected(self) -> None:
        index = build_structured_index(CANONICAL)
        tampered = copy.deepcopy(index)
        tampered["documents"][0]["fields"]["title"].append("tampered")
        with self.assertRaises(KernelError) as context:
            validate_structured_index(tampered, self.repository)
        self.assertEqual(context.exception.code, "E-STRUCTURED-DOCUMENT-FIELDS")


if __name__ == "__main__":
    unittest.main()
