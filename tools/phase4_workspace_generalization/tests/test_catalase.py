from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase4_workspace.contracts import (
    DECISION_CONTRACT,
    ENTRY_CONTRACT,
    EXPORT_CONTRACT,
    FAILURE_CONTRACT,
    MANIFEST_CONTRACT,
    WORKSPACE_CONTRACT,
)
from tools.phase4_workspace_generalization.contracts import (
    EXPECTED_SOURCE_POOL,
    EXPECTED_TRAIL,
    GENERALIZATION_REPORT_CONTRACT,
    REUSED_CONTRACTS,
    render_bundle,
    validate_generalization_bundle,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURE = ROOT / "content" / "fixtures" / "phase4_workspace_generalization" / "catalase.v01.json"


class CatalaseWorkspaceGeneralizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = KernelRepository(compile_canonical(CANONICAL))
        cls.fixture = load_json(FIXTURE)

    def test_all_thirteen_acceptance_gates_pass(self) -> None:
        report, core_report, export, manifest = validate_generalization_bundle(self.fixture, self.repository)
        self.assertEqual(report["contract"], GENERALIZATION_REPORT_CONTRACT)
        self.assertTrue(report["all_acceptance_gates_pass"])
        self.assertEqual(len(report["acceptance_gates"]), 13)
        self.assertEqual(report["counts"]["authorized_fixtures"], 1)
        self.assertEqual(report["counts"]["canonical_source_pool"], 8)
        self.assertEqual(report["counts"]["workspace_entries"], 5)
        self.assertEqual(report["counts"]["unresolved_candidates"], 2)
        self.assertGreaterEqual(report["counts"]["total_negative_cases"], 22)
        self.assertEqual(report["recommendation"], "proceed-static-reader-reuse-evaluation")
        self.assertFalse(report["implementation_authorized"])
        self.assertEqual(export["contract"], EXPORT_CONTRACT)
        self.assertEqual(manifest["contract"], MANIFEST_CONTRACT)
        self.assertEqual(core_report["counts"]["entries"], 5)

    def test_accepted_contract_names_are_reused_unchanged(self) -> None:
        report, _, _, _ = validate_generalization_bundle(self.fixture, self.repository)
        self.assertEqual(tuple(report["contracts_reused"]), REUSED_CONTRACTS)
        self.assertEqual(REUSED_CONTRACTS, (
            WORKSPACE_CONTRACT,
            ENTRY_CONTRACT,
            DECISION_CONTRACT,
            EXPORT_CONTRACT,
            MANIFEST_CONTRACT,
            FAILURE_CONTRACT,
        ))
        self.assertFalse(report["contracts_modified"])

    def test_source_pool_and_trail_are_exact_and_cross_domain(self) -> None:
        pool = tuple(f"{item['id']}@{item['revision']}" for item in self.fixture["canonical_source_pool"])
        entries = self.fixture["workspace_fixture"]["workspace"]["entries"]
        trail = tuple(f"{item['exact_reference']['id']}@{item['exact_reference']['revision']}" for item in entries)
        self.assertEqual(pool, EXPECTED_SOURCE_POOL)
        self.assertEqual(trail, EXPECTED_TRAIL)
        self.assertFalse(any("recommender" in key for key in trail))

    def test_outputs_are_byte_deterministic(self) -> None:
        first = render_bundle(self.fixture, self.repository)
        second = render_bundle(self.fixture, self.repository)
        self.assertEqual(first, second)
        self.assertEqual(
            [render_json(item) for item in validate_generalization_bundle(self.fixture, self.repository)],
            [render_json(item) for item in validate_generalization_bundle(self.fixture, self.repository)],
        )

    def test_unavailable_revision_warning_does_not_substitute(self) -> None:
        warning = self.fixture["bridge_fixture"]["impact_warnings"][0]
        self.assertEqual(warning["target"]["revision"], 2)
        with self.assertRaises(KernelError):
            self.repository.exact(warning["target"]["id"], warning["target"]["revision"])
        report, _, export, _ = validate_generalization_bundle(self.fixture, self.repository)
        self.assertTrue(report["acceptance_gates"]["gate_07_unavailable_revision_visible"])
        self.assertFalse(export["warning_references"][0]["automatic_update"])
        self.assertFalse(export["warning_references"][0]["implicit_latest"])

    def test_non_catalase_entry_is_rejected_before_contract_evidence(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["workspace_fixture"]["workspace"]["entries"][0]["exact_reference"] = {
            "id": "claim:en:recommender-effects-are-context-dependent",
            "revision": 1,
        }
        with self.assertRaisesRegex(KernelError, "E-GENERALIZATION-DOMAIN"):
            validate_generalization_bundle(fixture, self.repository)

    def test_contract_drift_is_rejected(self) -> None:
        fixture = copy.deepcopy(self.fixture)
        fixture["workspace_fixture"]["workspace"]["contract"] = "atlas-research-workspace/9.9"
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-CONTRACT"):
            validate_generalization_bundle(fixture, self.repository)

    def test_static_reader_recommendation_does_not_authorize_implementation(self) -> None:
        report, _, _, _ = validate_generalization_bundle(self.fixture, self.repository)
        self.assertEqual(report["recommendation_authority"], "separate-governance-proposal-only")
        self.assertFalse(report["browser_implementation_authorized"])
        self.assertFalse(report["production_implementation_authorized"])
        self.assertFalse(report["repository_mutation"])


if __name__ == "__main__":
    unittest.main()
