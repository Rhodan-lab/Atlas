from __future__ import annotations

import unittest
from pathlib import Path

from tools.phase2_kernel import load_json
from tools.phase3_retrieval.closure import run_phase3_closure, validate_completion_report

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURE_ROOT = ROOT / "content" / "fixtures" / "phase3_retrieval"


class Phase3CompletionBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.query_set = load_json(FIXTURE_ROOT / "reference-query-set.v01.json")
        cls.lexical = load_json(FIXTURE_ROOT / "lexical-baseline.json")
        cls.structured = load_json(FIXTURE_ROOT / "structured-baseline.json")
        cls.fusion = load_json(FIXTURE_ROOT / "rank-fusion.json")
        cls.research_fixtures = load_json(FIXTURE_ROOT / "research-foundations.v01.json")
        cls.research_baseline = load_json(FIXTURE_ROOT / "research-foundations-baseline.json")
        cls.completion_baseline = load_json(FIXTURE_ROOT / "phase3-completion-baseline.json")
        cls.report = run_phase3_closure(
            CANONICAL,
            cls.query_set,
            cls.lexical,
            cls.structured,
            cls.fusion,
            cls.research_fixtures,
            cls.research_baseline,
        )

    def test_completion_identity_and_decision_are_pinned(self) -> None:
        baseline = self.completion_baseline
        report = self.report
        self.assertEqual(report["contract"], "atlas-phase3-completion-report/0.1")
        for field in (
            "mode",
            "phase",
            "state",
            "decision",
            "preferred_bounded_retrieval",
            "semantic_infrastructure_decision",
            "entity_count",
            "source_digest",
            "accepted_workstreams",
            "exit_gates",
            "phase4_entry_boundary",
            "review_policy",
            "retrieval_authority",
            "exact_revision_required",
            "replaceable",
            "automatic_status_change",
            "automatic_merge_or_resolution",
            "automatic_release_action",
            "canonical_copy_authority",
            "external_services",
            "embeddings",
            "vector_database",
            "live",
            "repository_mutation",
        ):
            self.assertEqual(report[field], baseline[field], field)
        self.assertEqual(
            {"id": report["query_set"]["id"], "version": report["query_set"]["version"]},
            baseline["query_set"],
        )
        self.assertEqual(
            report["evaluated_rejected_candidates"],
            [baseline["expected_rejected_candidate"]],
        )
        self.assertEqual(
            validate_completion_report(report)["decision"],
            "valid-phase3-closure-candidate",
        )

    def test_accepted_retrieval_evidence_is_pinned(self) -> None:
        expected = self.completion_baseline["expected_evidence"]
        observed = self.report["evidence"]
        for name in ("lexical", "structured"):
            for field in ("index_build_digest", "result_set_sha256", "metrics"):
                self.assertEqual(observed[name][field], expected[name][field], f"{name}.{field}")
            self.assertGreater(observed[name]["visibility"]["ranked_items"], 0)
            self.assertEqual(observed[name]["visibility"]["error_responses"], 1)
        for field in ("manifest_build_digest", "result_set_sha256", "metrics", "decision"):
            self.assertEqual(observed["rank_fusion"][field], expected["rank_fusion"][field], f"rank_fusion.{field}")
        self.assertGreater(observed["rank_fusion"]["visibility"]["ranked_items"], 0)
        for field in ("report_digest", "counts", "negative_case_count"):
            self.assertEqual(
                observed["research_foundations"][field],
                expected["research_foundations"][field],
                f"research_foundations.{field}",
            )


if __name__ == "__main__":
    unittest.main()
