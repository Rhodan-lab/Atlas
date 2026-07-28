from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, render_json
from tools.phase4_interaction.contracts import (
    REPORT_CONTRACT,
    validate_failure_state,
    validate_fixture_bundle,
    validate_impact_warning,
    validate_state,
    validate_view,
)
from tools.phase4_interaction.fixtures import load_fixture_manifest

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
MANIFEST = ROOT / "content" / "fixtures" / "phase4_interaction" / "reference-interactions.v01.json"


class Phase4InteractionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = KernelRepository(compile_canonical(CANONICAL))
        cls.fixture = load_fixture_manifest(MANIFEST)

    def test_fixture_bundle_is_deterministic_and_valid(self) -> None:
        first, first_views = validate_fixture_bundle(self.fixture, self.repository)
        second, second_views = validate_fixture_bundle(self.fixture, self.repository)
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(render_json(first_views), render_json(second_views))
        self.assertEqual(first["contract"], REPORT_CONTRACT)
        self.assertEqual(first["state"], "interaction-contract-candidate")
        self.assertEqual(
            first["counts"],
            {
                "views": 8,
                "states": 8,
                "principia_references": 1,
                "impact_warnings": 1,
                "failure_states": 5,
                "negative_cases": 6,
            },
        )
        self.assertEqual(
            first["workflow_kinds"],
            [
                "candidate",
                "entity",
                "filter",
                "impact-warning",
                "principia-reference",
                "provenance",
                "research-trail",
                "retrieval",
            ],
        )
        self.assertTrue(first["exact_revision_preserved"])
        self.assertTrue(first["authority_metadata_visible"])
        self.assertTrue(first["keyboard_paths_required"])
        self.assertTrue(first["non_graph_paths_required"])
        self.assertTrue(first["principia_status_separate"])
        self.assertTrue(first["offline_capable"])
        self.assertFalse(first["canonical_copy_authority"])
        self.assertFalse(first["live_principia_dependency"])
        self.assertFalse(first["live"])
        self.assertFalse(first["repository_mutation"])
        self.assertEqual(len(first_views), 8)

    def test_unavailable_revision_warning_is_explicit(self) -> None:
        warning = self.fixture["impact_warnings"][0]
        validation = validate_impact_warning(warning, self.repository)
        self.assertEqual(validation["impact_state"], "unavailable")
        self.assertEqual(
            validation["target"],
            "model:en:delayed-correction-recurrence@3",
        )
        self.assertEqual(validation["severity"], "blocking")

    def test_every_view_has_accessible_non_graph_navigation(self) -> None:
        for view in self.fixture["views"]:
            validation = validate_view(view, self.repository)
            self.assertEqual(validation["decision"], "valid")
            self.assertFalse(view["graph_required"])
            self.assertGreater(len(view["keyboard_path"]), 0)
            self.assertGreater(len(view["non_graph_path"]), 0)

    def test_implicit_latest_route_is_rejected(self) -> None:
        _, views = validate_fixture_bundle(self.fixture, self.repository)
        state = copy.deepcopy(self.fixture["states"][0])
        state["route"] = "/atlas/models/delayed-correction-recurrence/latest"
        with self.assertRaises(KernelError) as context:
            validate_state(state, views)
        self.assertEqual(context.exception.code, "E-INTERACTION-STATE-ROUTE")

    def test_view_authority_escalation_is_rejected(self) -> None:
        view = copy.deepcopy(self.fixture["views"][0])
        view["canonical_mutation"] = True
        with self.assertRaises(KernelError) as context:
            validate_view(view, self.repository)
        self.assertEqual(context.exception.code, "E-INTERACTION-VIEW-AUTHORITY")

    def test_failure_silent_fallback_is_rejected(self) -> None:
        failure = copy.deepcopy(self.fixture["failure_states"][0])
        failure["silent_fallback"] = True
        with self.assertRaises(KernelError) as context:
            validate_failure_state(failure)
        self.assertEqual(context.exception.code, "E-INTERACTION-FAILURE-AUTHORITY")

    def test_tampered_source_digest_is_rejected(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["source_digest"] = "0" * 64
        with self.assertRaises(KernelError) as context:
            validate_fixture_bundle(fixture, self.repository)
        self.assertEqual(context.exception.code, "E-INTERACTION-FIXTURE-SOURCE")


if __name__ == "__main__":
    unittest.main()
