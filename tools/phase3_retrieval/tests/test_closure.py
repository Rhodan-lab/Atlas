from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, load_json, render_json
from tools.phase3_retrieval.closure import (
    COMPLETION_CONTRACT,
    run_phase3_closure,
    validate_completion_report,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURE_ROOT = ROOT / "content" / "fixtures" / "phase3_retrieval"
QUERY_SET = FIXTURE_ROOT / "reference-query-set.v01.json"
LEXICAL = FIXTURE_ROOT / "lexical-baseline.json"
STRUCTURED = FIXTURE_ROOT / "structured-baseline.json"
FUSION = FIXTURE_ROOT / "rank-fusion.json"
RESEARCH_FIXTURES = FIXTURE_ROOT / "research-foundations.v01.json"
RESEARCH_BASELINE = FIXTURE_ROOT / "research-foundations-baseline.json"


class Phase3ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.query_set = load_json(QUERY_SET)
        cls.lexical = load_json(LEXICAL)
        cls.structured = load_json(STRUCTURED)
        cls.fusion = load_json(FUSION)
        cls.research_fixtures = load_json(RESEARCH_FIXTURES)
        cls.research_baseline = load_json(RESEARCH_BASELINE)

    def _run(self, **overrides):
        return run_phase3_closure(
            CANONICAL,
            overrides.get("query_set", self.query_set),
            overrides.get("lexical", self.lexical),
            overrides.get("structured", self.structured),
            overrides.get("fusion", self.fusion),
            overrides.get("research_fixtures", self.research_fixtures),
            overrides.get("research_baseline", self.research_baseline),
        )

    def test_closure_is_deterministic_and_valid(self) -> None:
        first = self._run()
        second = self._run()
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(first["contract"], COMPLETION_CONTRACT)
        self.assertTrue(all(first["exit_gates"].values()))
        validation = validate_completion_report(first)
        self.assertEqual(validation["decision"], "valid-phase3-closure-candidate")
        self.assertEqual(
            validation["phase4_recommendation"],
            "proceed-phase4-interactive-experience",
        )
        self.assertEqual(validation["preferred_bounded_retrieval"], "structured-field-baseline")

    def test_closure_preserves_rejected_fusion_decision(self) -> None:
        report = self._run()
        candidate = report["evaluated_rejected_candidates"][0]
        self.assertEqual(candidate["decision"], "rejected")
        self.assertEqual(
            candidate["recommendation"],
            "reject-candidate-no-quality-gain-over-structured",
        )
        self.assertEqual(report["semantic_infrastructure_decision"], "defer-until-broader-benchmark-and-architecture-approval")

    def test_phase4_boundary_is_safe(self) -> None:
        report = self._run()
        boundary = report["phase4_entry_boundary"]
        self.assertTrue(boundary["atlas_semantics_authoritative"])
        self.assertTrue(boundary["principia_status_separate"])
        self.assertFalse(boundary["production_retrieval_quality_claim"])
        self.assertFalse(boundary["vector_database"])
        self.assertFalse(boundary["live_principia_dependency"])
        self.assertFalse(boundary["canonical_mutation"])

    def test_tampered_structured_baseline_is_rejected(self) -> None:
        tampered = copy.deepcopy(self.structured)
        tampered["index_build_digest"] = "0" * 64
        with self.assertRaises(KernelError) as context:
            self._run(structured=tampered)
        self.assertEqual(context.exception.code, "E-PHASE3-STRUCTURED")

    def test_completion_digest_tampering_is_rejected(self) -> None:
        report = self._run()
        report["preferred_bounded_retrieval"] = "lexical-baseline"
        with self.assertRaises(KernelError) as context:
            validate_completion_report(report)
        self.assertEqual(context.exception.code, "E-PHASE3-COMPLETION-DIGEST")


if __name__ == "__main__":
    unittest.main()
