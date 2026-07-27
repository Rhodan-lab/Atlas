from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase3_retrieval.research import (
    FILTER_CONTRACT,
    FILTER_RESULT_CONTRACT,
    REPORT_CONTRACT,
    apply_filter,
    validate_duplicate_candidate,
    validate_filter,
    validate_fixture_bundle,
    validate_trail,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
QUERY_SET = ROOT / "content" / "fixtures" / "phase3_retrieval" / "reference-query-set.v01.json"
STRUCTURED_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "structured-baseline.json"
FIXTURES = ROOT / "content" / "fixtures" / "phase3_retrieval" / "research-foundations.v01.json"


class ResearchFoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)
        cls.repository = KernelRepository(cls.runtime)
        cls.query_set = load_json(QUERY_SET)
        cls.structured_baseline = load_json(STRUCTURED_BASELINE)
        cls.fixtures = load_json(FIXTURES)
        cls.filters = {item["id"]: item for item in cls.fixtures["filters"]}

    def test_bundle_validates_deterministically(self) -> None:
        first_report, first_results = validate_fixture_bundle(
            self.fixtures,
            self.repository,
            self.query_set,
            self.structured_baseline,
        )
        second_report, second_results = validate_fixture_bundle(
            self.fixtures,
            self.repository,
            self.query_set,
            self.structured_baseline,
        )
        self.assertEqual(render_json(first_report), render_json(second_report))
        self.assertEqual(render_json({"results": first_results}), render_json({"results": second_results}))
        self.assertEqual(first_report["contract"], REPORT_CONTRACT)
        self.assertEqual(first_report["decision"], "research-foundation-candidate")
        self.assertEqual(first_report["counts"]["filters"], 4)
        self.assertEqual(first_report["counts"]["trails"], 1)
        self.assertEqual(first_report["counts"]["contradiction_candidates"], 1)
        self.assertEqual(first_report["counts"]["duplicate_candidates"], 1)
        self.assertEqual(first_report["counts"]["negative_cases"], 5)

    def test_filter_results_preserve_exact_revisions_and_metadata(self) -> None:
        record = self.filters["filter:en:feedback-draft-models"]
        validation = validate_filter(record, self.repository)
        result = apply_filter(record, self.repository)
        self.assertEqual(validation["decision"], "valid")
        self.assertEqual(record["contract"], FILTER_CONTRACT)
        self.assertEqual(result["contract"], FILTER_RESULT_CONTRACT)
        self.assertEqual(result["entity_count_after"], 1)
        item = result["items"][0]
        self.assertEqual(item["id"], "model:en:delayed-correction-recurrence")
        self.assertEqual(item["revision"], 2)
        self.assertEqual(item["domain"], "feedback")
        self.assertEqual(item["status"], "draft")
        self.assertEqual(item["staleness"], "current")
        self.assertTrue(result["exact_revision_preserved"])

    def test_evidence_role_filters_are_explicit(self) -> None:
        supporting = apply_filter(
            self.filters["filter:en:catalase-supporting-evidence"],
            self.repository,
        )
        contextual = apply_filter(
            self.filters["filter:en:recommender-contextual-evidence"],
            self.repository,
        )
        self.assertEqual(
            [f"{item['id']}@{item['revision']}" for item in supporting["items"]],
            ["evidence:en:fluorescent-catalase-assay-neutral-ph@1"],
        )
        self.assertIn("supports", supporting["items"][0]["evidence_roles"])
        self.assertEqual(
            [f"{item['id']}@{item['revision']}" for item in contextual["items"]],
            ["evidence:en:dsa-recommender-transparency-and-choice@1"],
        )
        self.assertIn("contextualizes", contextual["items"][0]["evidence_roles"])

    def test_trail_is_research_only_and_filter_bounded(self) -> None:
        trail = self.fixtures["trails"][0]
        validation = validate_trail(
            trail,
            self.repository,
            self.query_set,
            self.filters,
            self.structured_baseline,
        )
        self.assertEqual(validation["decision"], "valid")
        self.assertEqual(validation["authority"], "research-only")
        self.assertEqual(validation["entry_count"], 5)
        self.assertFalse(trail["canonical_copy"])
        self.assertFalse(trail["automatic_status_change"])

    def test_duplicate_candidate_cannot_auto_merge(self) -> None:
        candidate = copy.deepcopy(self.fixtures["duplicate_candidates"][0])
        candidate["automatic_merge"] = True
        with self.assertRaises(KernelError) as context:
            validate_duplicate_candidate(candidate, self.repository)
        self.assertEqual(context.exception.code, "E-DUPLICATE-AUTHORITY")

    def test_trail_entry_outside_filter_is_rejected(self) -> None:
        trail = copy.deepcopy(self.fixtures["trails"][0])
        trail["entries"][0]["id"] = "model:en:delayed-correction-recurrence"
        trail["entries"][0]["revision"] = 2
        with self.assertRaises(KernelError) as context:
            validate_trail(
                trail,
                self.repository,
                self.query_set,
                self.filters,
                self.structured_baseline,
            )
        self.assertEqual(context.exception.code, "E-TRAIL-FILTER-MISMATCH")


if __name__ == "__main__":
    unittest.main()
