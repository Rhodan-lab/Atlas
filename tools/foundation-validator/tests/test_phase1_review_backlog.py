from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

VALIDATOR_DIR = Path(__file__).resolve().parents[1]


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_load_module("phase1_review_gate", VALIDATOR_DIR / "phase1_review_gate.py")
_load_module("phase1_coverage_report", VALIDATOR_DIR / "phase1_coverage_report.py")
backlog = _load_module("phase1_review_backlog", VALIDATOR_DIR / "phase1_review_backlog.py")


class ReviewerRequirementTests(unittest.TestCase):
    def test_translation_requires_independent_accountable_human(self) -> None:
        requirement = backlog.reviewer_requirement("translation", {})
        self.assertEqual(requirement.allowed_kinds, ("human",))
        self.assertEqual(requirement.allowed_independence, ("independent",))
        self.assertTrue(requirement.accountability_required)

    def test_fully_specified_reproduction_can_be_machine_checked(self) -> None:
        requirement = backlog.reviewer_requirement(
            "reproducibility",
            {"material_flags": ["fully-specified-reproducibility"]},
        )
        self.assertIn("machine", requirement.allowed_kinds)
        self.assertFalse(requirement.accountability_required)

    def test_domain_review_cannot_be_ai_authority(self) -> None:
        requirement = backlog.reviewer_requirement("domain", {})
        self.assertNotIn("ai-assisted", requirement.allowed_kinds)
        self.assertEqual(requirement.allowed_kinds, ("human",))


class BacklogTests(unittest.TestCase):
    def _manifest(self, *, requirement: str = "all", role: str = "load-bearing") -> dict:
        return {
            "contract": "atlas-review-coverage/0.1",
            "id": "coverage:test:feedback",
            "title": "Test feedback coverage",
            "intended_status": "reviewed",
            "decision_at": "2026-07-26",
            "coverage_requirement": requirement,
            "entities": [
                {
                    "id": "claim:en:test",
                    "revision": 1,
                    "type": "claim",
                    "status": "draft",
                    "staleness": "current",
                    "claim_kind": "model-derived",
                    "material_flags": ["fully-specified-reproducibility"],
                    "role": role,
                    "depends_on": [],
                }
            ],
            "external_dependents": [],
        }

    def _coverage_result(self, *, role: str = "load-bearing"):
        item = backlog.coverage.EntityCoverage(
            entity_id="claim:en:test",
            revision=1,
            role=role,
            required_review_types=(
                "domain",
                "editorial",
                "methodological",
                "reproducibility",
                "structural",
            ),
            satisfied_review_types=("structural",),
            missing_review_types=(
                "domain",
                "editorial",
                "methodological",
                "reproducibility",
            ),
            review_ids=("review:domain:test-r1:2026-07-26",),
            blockers=("review lacks authority for domain",),
            internal_dependents=("synthesis:en:test",),
            external_dependents=(),
        )
        return backlog.coverage.CoverageResult(
            decision="blocked",
            coverage_requirement="all",
            required_entity_count=1,
            complete_entity_count=0,
            entity_results=(item,),
            reasons=("claim:en:test@1 is missing acceptable review coverage",),
        )

    def test_builds_one_task_per_missing_review_type(self) -> None:
        with patch.object(
            backlog.coverage,
            "evaluate_coverage",
            return_value=(self._coverage_result(), []),
        ):
            result, diagnostics = backlog.build_backlog(self._manifest(), [])
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.task_count, 4)
        self.assertEqual(result.gate_task_count, 4)
        self.assertEqual(
            {task.review_type for task in result.tasks},
            {"domain", "editorial", "methodological", "reproducibility"},
        )

    def test_existing_non_authoritative_review_remains_visible(self) -> None:
        with patch.object(
            backlog.coverage,
            "evaluate_coverage",
            return_value=(self._coverage_result(), []),
        ):
            result, _ = backlog.build_backlog(self._manifest(), [])
        domain = next(task for task in result.tasks if task.review_type == "domain")
        self.assertIn("review:domain:test-r1:2026-07-26", domain.existing_review_ids)
        self.assertIn("review lacks authority for domain", domain.blockers)

    def test_context_gap_is_advisory_under_load_bearing_policy(self) -> None:
        coverage_result = self._coverage_result(role="context")
        coverage_result = backlog.coverage.CoverageResult(
            decision="coverage-complete",
            coverage_requirement="load-bearing",
            required_entity_count=0,
            complete_entity_count=0,
            entity_results=coverage_result.entity_results,
            reasons=(),
        )
        with patch.object(
            backlog.coverage,
            "evaluate_coverage",
            return_value=(coverage_result, []),
        ):
            result, _ = backlog.build_backlog(
                self._manifest(requirement="load-bearing", role="context"), []
            )
        self.assertEqual(result.gate_task_count, 0)
        self.assertEqual(result.advisory_task_count, 4)
        self.assertTrue(all(task.priority == "low" for task in result.tasks))

    def test_backlog_and_report_are_deterministic(self) -> None:
        with patch.object(
            backlog.coverage,
            "evaluate_coverage",
            return_value=(self._coverage_result(), []),
        ):
            first, _ = backlog.build_backlog(self._manifest(), [])
            second, _ = backlog.build_backlog(self._manifest(), [])
        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(backlog.render_report(first), backlog.render_report(second))

    def test_load_bearing_dependents_receive_high_priority(self) -> None:
        with patch.object(
            backlog.coverage,
            "evaluate_coverage",
            return_value=(self._coverage_result(), []),
        ):
            result, _ = backlog.build_backlog(self._manifest(), [])
        self.assertTrue(all(task.priority == "high" for task in result.tasks))
        self.assertTrue(
            all("synthesis:en:test" in task.internal_dependents for task in result.tasks)
        )


if __name__ == "__main__":
    unittest.main()
