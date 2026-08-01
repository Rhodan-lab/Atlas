from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.evidence_impact import compile_evidence_impact_index
from tools.phase2_kernel.evidence_review import load_review_index
from tools.phase2_kernel.evidence_simulation import (
    SCENARIO_CONTRACT,
    SIMULATION_CONTRACT,
    simulate_evidence_impact,
    validate_evidence_impact_scenario,
)
from tools.phase2_kernel.kernel import KernelError, load_json, render_json
from tools.phase2_kernel.repository import KernelRepository

ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = (
    ROOT
    / "content"
    / "fixtures"
    / "phase2_bridge"
    / "accepted-evidence-registry.v01.json"
)
CONTROL_PATH = (
    ROOT
    / "content"
    / "fixtures"
    / "phase2_bridge"
    / "evidence-impact-scenario.none.v01.json"
)
MODEL_ID = "model:en:delayed-correction-recurrence"
CLAIM_ID = "claim:en:model-oscillation-does-not-prove-real-system"


def scenario(changes: list[dict[str, object]]) -> dict[str, object]:
    return {
        "contract": SCENARIO_CONTRACT,
        "live": False,
        "status_inheritance": "prohibited",
        "changes": changes,
    }


def change(
    entity_id: str,
    revision: int,
    operation: str,
    reason: str = "proposed evidence maintenance change",
    new_revision: int | None = None,
) -> dict[str, object]:
    item: dict[str, object] = {
        "entity_id": entity_id,
        "revision": revision,
        "operation": operation,
        "reason": reason,
    }
    if new_revision is not None:
        item["new_revision"] = new_revision
    return item


class EvidenceSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        runtime = compile_canonical(ROOT / "content" / "canonical")
        cls.index = compile_evidence_impact_index(
            load_json(REGISTRY_PATH),
            KernelRepository(runtime),
            load_review_index(ROOT / "content" / "reviews" / "ai"),
            ROOT,
        )

    def simulate(self, changes: list[dict[str, object]]) -> dict[str, object]:
        return simulate_evidence_impact(self.index, scenario(changes))

    def test_empty_repository_control_is_clear(self) -> None:
        report = simulate_evidence_impact(self.index, load_json(CONTROL_PATH))
        self.assertEqual(report["contract"], SIMULATION_CONTRACT)
        self.assertEqual(report["change_count"], 0)
        self.assertEqual(report["decision"], "simulation-clear")
        self.assertEqual(report["simulated_affected_route_ids"], [])
        self.assertEqual(report["newly_affected_route_ids"], [])
        self.assertFalse(report["canonical_mutation"])
        self.assertFalse(report["repository_mutation"])

    def test_supersede_marks_refrigerator_for_revalidation(self) -> None:
        report = self.simulate(
            [change(MODEL_ID, 2, "supersede", new_revision=3)]
        )
        self.assertEqual(report["decision"], "simulation-revalidation-required")
        self.assertEqual(report["newly_affected_route_ids"], ["refrigerator"])
        self.assertEqual(report["escalated_route_ids"], ["refrigerator"])
        applied = report["applied_changes"][0]
        self.assertEqual(applied["key"], f"{MODEL_ID}@2")
        self.assertEqual(applied["to_impact_state"], "revalidation-required")
        exact = next(
            item
            for item in report["simulated_index"]["exact_references"]
            if item["key"] == f"{MODEL_ID}@2"
        )
        self.assertTrue(exact["superseded"])
        self.assertEqual(exact["latest_revision"], 3)
        self.assertIn(3, exact["available_revisions"])
        self.assertEqual(exact["available_revisions"][-1], 3)

    def test_review_required_marks_route_for_revalidation(self) -> None:
        report = self.simulate(
            [change(CLAIM_ID, 1, "mark-review-required")]
        )
        self.assertEqual(report["decision"], "simulation-revalidation-required")
        self.assertEqual(report["simulated_affected_route_ids"], ["refrigerator"])
        dependency = next(
            item
            for exact in report["simulated_index"]["exact_references"]
            if exact["key"] == f"{CLAIM_ID}@1"
            for item in exact["dependencies"]
        )
        self.assertEqual(dependency["resolution"], "review-required")
        self.assertEqual(dependency["required_action"], "revalidate")

    def test_confirmed_stale_marks_route_for_revalidation(self) -> None:
        report = self.simulate(
            [change(CLAIM_ID, 1, "mark-confirmed-stale")]
        )
        self.assertEqual(report["decision"], "simulation-revalidation-required")
        self.assertEqual(report["newly_affected_route_count"], 1)
        self.assertEqual(
            report["applied_changes"][0]["to_impact_state"],
            "revalidation-required",
        )

    def test_deprecation_marks_route_for_revalidation(self) -> None:
        report = self.simulate([change(MODEL_ID, 2, "deprecate")])
        self.assertEqual(report["decision"], "simulation-revalidation-required")
        self.assertEqual(report["newly_blocked_route_ids"], [])
        self.assertEqual(
            report["simulated_index"]["decision"],
            "impact-index-revalidation-required",
        )

    def test_retraction_blocks_affected_route(self) -> None:
        report = self.simulate([change(MODEL_ID, 2, "retract")])
        self.assertEqual(report["decision"], "simulation-blocked")
        self.assertEqual(report["newly_blocked_route_ids"], ["refrigerator"])
        self.assertEqual(report["simulated_index"]["decision"], "impact-index-blocked")
        route = report["simulated_index"]["routes"][0]
        self.assertEqual(route["impact_state"], "blocked")

    def test_duplicate_exact_target_is_rejected(self) -> None:
        payload = scenario(
            [
                change(MODEL_ID, 2, "deprecate"),
                change(MODEL_ID, 2, "retract"),
            ]
        )
        with self.assertRaisesRegex(KernelError, "duplicate simulated target"):
            validate_evidence_impact_scenario(payload)

    def test_missing_accepted_dependency_is_rejected(self) -> None:
        with self.assertRaisesRegex(KernelError, "no accepted Principia route"):
            self.simulate([change(MODEL_ID, 99, "deprecate")])

    def test_invalid_superseding_revision_is_rejected(self) -> None:
        payload = scenario(
            [change(MODEL_ID, 2, "supersede", new_revision=2)]
        )
        with self.assertRaisesRegex(KernelError, "greater than revision"):
            validate_evidence_impact_scenario(payload)

    def test_simulation_is_deterministic_and_does_not_mutate_source(self) -> None:
        baseline = render_json(copy.deepcopy(self.index))
        payload = scenario(
            [
                change(CLAIM_ID, 1, "mark-review-required", "claim review refresh"),
                change(MODEL_ID, 2, "retract", "model withdrawal proposal"),
            ]
        )
        first = render_json(simulate_evidence_impact(self.index, payload))
        second = render_json(simulate_evidence_impact(self.index, payload))
        self.assertEqual(first, second)
        self.assertEqual(render_json(self.index), baseline)
        report = simulate_evidence_impact(self.index, payload)
        self.assertEqual(
            [item["key"] for item in report["applied_changes"]],
            [f"{CLAIM_ID}@1", f"{MODEL_ID}@2"],
        )
        self.assertEqual(report["decision"], "simulation-blocked")
        self.assertFalse(report["automatic_status_change"])
        self.assertFalse(report["automatic_release_action"])


if __name__ == "__main__":
    unittest.main()
