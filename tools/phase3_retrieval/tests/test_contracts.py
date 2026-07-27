from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import (
    KernelError,
    KernelRepository,
    compile_canonical,
    load_json,
    render_json,
)
from tools.phase3_retrieval import (
    METRIC_REPORT_CONTRACT,
    QUERY_SET_CONTRACT,
    RESULT_SET_CONTRACT,
    validate_metric_report,
    validate_query_set,
    validate_result_set,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
QUERY_SET_PATH = (
    ROOT / "content" / "fixtures" / "phase3_retrieval" / "reference-query-set.v01.json"
)


class RetrievalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = KernelRepository(compile_canonical(CANONICAL))
        cls.query_set = load_json(QUERY_SET_PATH)

    def _item(
        self,
        entity_id: str,
        revision: int,
        rank: int = 1,
        score: float = 1.0,
    ) -> dict:
        entity = self.repository.exact(entity_id, revision)
        return {
            "id": entity_id,
            "revision": revision,
            "rank": rank,
            "score": score,
            "type": entity.get("type"),
            "title": entity.get("title"),
            "status": entity.get("status"),
            "staleness": entity.get("staleness"),
            "review_level": entity.get("review_level"),
            "matched_fields": ["title"],
            "explanation": "Synthetic contract fixture; not retrieval-quality evidence.",
            "provenance": [],
        }

    def _valid_result_set(self) -> dict:
        responses = []
        for query in self.query_set["queries"]:
            expected = query["expected"]
            if expected["kind"] == "error":
                responses.append(
                    {
                        "query_id": query["id"],
                        "outcome": "error",
                        "error": expected["error"],
                        "target": expected["target"],
                    }
                )
                continue
            top = expected["judgments"][0]
            responses.append(
                {
                    "query_id": query["id"],
                    "outcome": "ranked",
                    "items": [
                        self._item(top["id"], top["revision"]),
                    ],
                }
            )
        return {
            "contract": RESULT_SET_CONTRACT,
            "query_set_id": self.query_set["id"],
            "query_set_version": self.query_set["version"],
            "index": {
                "contract": "atlas-retrieval-index-fixture/0.1",
                "build_digest": "a" * 64,
                "source_digest": self.repository.runtime["source_digest"],
                "replaceable": True,
                "canonical_mutation": False,
            },
            "responses": responses,
            "advisory_only": True,
            "live": False,
            "repository_mutation": False,
        }

    def _valid_metric_report(self) -> dict:
        return {
            "contract": METRIC_REPORT_CONTRACT,
            "query_set_id": self.query_set["id"],
            "query_set_version": self.query_set["version"],
            "result_set_sha256": "b" * 64,
            "cutoff": 5,
            "evaluated_ranked_queries": 12,
            "expected_error_queries": 1,
            "metrics": {
                "precision_at_k": 0.5,
                "recall_at_k": 0.5,
                "mean_reciprocal_rank": 0.5,
                "ndcg_at_k": 0.5,
                "zero_result_rate": 0.0,
                "unavailable_revision_rate": 1.0,
            },
            "tie_count": 0,
            "advisory_only": True,
            "live": False,
            "repository_mutation": False,
        }

    def test_reference_query_set_is_valid_and_deterministic(self) -> None:
        first = validate_query_set(self.query_set, self.repository)
        second = validate_query_set(self.query_set, self.repository)
        self.assertEqual(self.query_set["contract"], QUERY_SET_CONTRACT)
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(first["decision"], "valid")
        self.assertEqual(first["entity_count"], 34)
        self.assertEqual(first["query_count"], 13)
        self.assertEqual(first["ranked_query_count"], 12)
        self.assertEqual(first["expected_error_query_count"], 1)
        self.assertEqual(first["positive_judgment_count"], 26)
        self.assertEqual(first["implicit_nonrelevant_judgment_count"], 382)
        self.assertEqual(
            first["slice_counts"],
            {
                "catalase": 4,
                "cross-slice": 1,
                "feedback": 4,
                "recommenders": 4,
            },
        )
        self.assertEqual(
            first["difficulty_counts"],
            {
                "ambiguous": 2,
                "compositional": 4,
                "direct": 6,
                "exact-revision-error": 1,
            },
        )
        self.assertFalse(first["live"])
        self.assertFalse(first["repository_mutation"])

    def test_duplicate_query_id_is_rejected(self) -> None:
        payload = copy.deepcopy(self.query_set)
        payload["queries"].append(copy.deepcopy(payload["queries"][0]))
        with self.assertRaisesRegex(KernelError, "E-RETRIEVAL-QUERY-DUPLICATE"):
            validate_query_set(payload, self.repository)

    def test_unknown_positive_judgment_is_rejected(self) -> None:
        payload = copy.deepcopy(self.query_set)
        payload["queries"][0]["expected"]["judgments"][0]["revision"] = 99
        with self.assertRaisesRegex(KernelError, "E-REVISION-MISSING"):
            validate_query_set(payload, self.repository)

    def test_unavailable_revision_expectation_is_exact(self) -> None:
        payload = copy.deepcopy(self.query_set)
        error_query = next(
            query
            for query in payload["queries"]
            if query["expected"]["kind"] == "error"
        )
        error_query["expected"]["available_revisions"] = [1, 2]
        with self.assertRaisesRegex(KernelError, "E-RETRIEVAL-ERROR-REVISIONS"):
            validate_query_set(payload, self.repository)

    def test_result_contract_preserves_exact_metadata_and_authority(self) -> None:
        report = validate_result_set(
            self._valid_result_set(),
            self.query_set,
            self.repository,
        )
        self.assertEqual(report["decision"], "valid")
        self.assertEqual(report["response_count"], 13)
        self.assertEqual(report["result_item_count"], 12)
        self.assertEqual(report["zero_result_count"], 0)
        self.assertTrue(report["advisory_only"])
        self.assertFalse(report["live"])
        self.assertFalse(report["repository_mutation"])

    def test_unversioned_result_is_rejected(self) -> None:
        payload = self._valid_result_set()
        ranked = next(
            response for response in payload["responses"] if response["outcome"] == "ranked"
        )
        ranked["items"][0]["revision"] = None
        with self.assertRaisesRegex(KernelError, "E-RETRIEVAL-RESULT-REVISION"):
            validate_result_set(payload, self.query_set, self.repository)

    def test_equal_score_ties_require_exact_key_order(self) -> None:
        payload = self._valid_result_set()
        query = self.query_set["queries"][0]
        response = next(
            item for item in payload["responses"] if item["query_id"] == query["id"]
        )
        first, second = query["expected"]["judgments"][:2]
        first_key = f"{first['id']}@{first['revision']}"
        second_key = f"{second['id']}@{second['revision']}"
        ordered = sorted(
            [
                (first_key, first["id"], first["revision"]),
                (second_key, second["id"], second["revision"]),
            ],
            reverse=True,
        )
        response["items"] = [
            self._item(entity_id, revision, rank=index, score=1.0)
            for index, (_, entity_id, revision) in enumerate(ordered, start=1)
        ]
        with self.assertRaisesRegex(KernelError, "E-RETRIEVAL-RESULT-TIE"):
            validate_result_set(payload, self.query_set, self.repository)

    def test_metric_contract_is_bounded(self) -> None:
        report = validate_metric_report(
            self._valid_metric_report(),
            self.query_set,
            self.repository,
        )
        self.assertEqual(report["decision"], "valid")
        self.assertEqual(report["cutoff"], 5)
        self.assertEqual(report["metric_count"], 6)
        self.assertTrue(report["advisory_only"])

        invalid = self._valid_metric_report()
        invalid["metrics"]["precision_at_k"] = 1.01
        with self.assertRaisesRegex(KernelError, "E-RETRIEVAL-METRIC-RANGE"):
            validate_metric_report(invalid, self.query_set, self.repository)


if __name__ == "__main__":
    unittest.main()
