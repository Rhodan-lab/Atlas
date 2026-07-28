from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase4_workspace.contracts import (
    EXPORT_CONTRACT,
    MANIFEST_CONTRACT,
    REPORT_CONTRACT,
    validate_fixture_bundle,
    validate_manifest,
    validate_workspace,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURE = ROOT / "content" / "fixtures" / "phase4_workspace" / "research-workspace.v01.json"
RESEARCH_FIXTURE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "research-foundations.v01.json"
RESEARCH_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "research-foundations-baseline.json"
STRUCTURED_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "structured-baseline.json"
BRIDGE_FIXTURE = ROOT / "content" / "fixtures" / "phase4_interaction" / "bridge-failures.v01.json"


class Phase4WorkspaceContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = KernelRepository(compile_canonical(CANONICAL))
        cls.fixture = load_json(FIXTURE)
        cls.research_fixture = load_json(RESEARCH_FIXTURE)
        cls.research_baseline = load_json(RESEARCH_BASELINE)
        cls.structured_baseline = load_json(STRUCTURED_BASELINE)
        cls.bridge_fixture = load_json(BRIDGE_FIXTURE)

    def _validate_workspace(self, workspace):
        return validate_workspace(
            workspace,
            self.repository,
            self.research_fixture,
            self.research_baseline,
            self.structured_baseline,
            self.bridge_fixture,
        )

    def test_fixture_build_is_deterministic_and_valid(self) -> None:
        first = validate_fixture_bundle(
            self.fixture,
            self.repository,
            self.research_fixture,
            self.research_baseline,
            self.structured_baseline,
            self.bridge_fixture,
        )
        second = validate_fixture_bundle(
            self.fixture,
            self.repository,
            self.research_fixture,
            self.research_baseline,
            self.structured_baseline,
            self.bridge_fixture,
        )
        self.assertEqual([render_json(item) for item in first], [render_json(item) for item in second])
        report, export, manifest = first
        self.assertEqual(report["contract"], REPORT_CONTRACT)
        self.assertEqual(export["contract"], EXPORT_CONTRACT)
        self.assertEqual(manifest["contract"], MANIFEST_CONTRACT)
        self.assertEqual(report["counts"]["entries"], 5)
        self.assertEqual(report["counts"]["candidates"], 2)
        self.assertEqual(report["counts"]["principia_references"], 1)
        self.assertEqual(report["counts"]["negative_cases"], 10)
        self.assertEqual(report["decision_counts"], {"context": 2, "exclude": 1, "include": 2})
        self.assertTrue(report["exact_revision_preserved"])
        self.assertTrue(report["deterministic_export"])
        self.assertFalse(report["canonical_copy_authority"])
        self.assertFalse(report["canonical_mutation"])
        self.assertFalse(report["repository_mutation"])

    def test_export_contains_references_and_metadata_not_canonical_body(self) -> None:
        _, export, _ = validate_fixture_bundle(
            self.fixture,
            self.repository,
            self.research_fixture,
            self.research_baseline,
            self.structured_baseline,
            self.bridge_fixture,
        )
        rendered = render_json(export)
        self.assertEqual(len(export["entries"]), 5)
        self.assertNotIn('"body"', rendered)
        self.assertNotIn('"content"', rendered)
        self.assertNotIn("canonical_body", rendered)
        self.assertTrue(all("visible_metadata" in item for item in export["entries"]))
        self.assertTrue(all(item["resolution"] == "unresolved" for item in export["candidate_references"]))
        self.assertTrue(export["principia_references"][0]["principia_status_separate"])

    def test_manifest_tampering_is_rejected(self) -> None:
        _, export, manifest = validate_fixture_bundle(
            self.fixture,
            self.repository,
            self.research_fixture,
            self.research_baseline,
            self.structured_baseline,
            self.bridge_fixture,
        )
        export_bytes = render_json(export).encode("utf-8")
        tampered = copy.deepcopy(manifest)
        tampered["files"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-MANIFEST"):
            validate_manifest(tampered, export, export_bytes)

    def test_workspace_contract_drift_is_rejected(self) -> None:
        workspace = copy.deepcopy(self.fixture["workspace"])
        workspace["contract"] = "atlas-research-workspace/9.9"
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-CONTRACT"):
            self._validate_workspace(workspace)

    def test_workspace_digest_inputs_reject_latest(self) -> None:
        workspace = copy.deepcopy(self.fixture["workspace"])
        workspace["entries"][0]["exact_reference"]["revision"] = "latest"
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-LATEST"):
            self._validate_workspace(workspace)

    def test_candidate_resolution_cannot_gain_authority(self) -> None:
        workspace = copy.deepcopy(self.fixture["workspace"])
        workspace["candidate_references"][0]["resolution"] = "resolved"
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-CANDIDATE-AUTHORITY"):
            self._validate_workspace(workspace)

    def test_principia_status_cannot_be_inherited(self) -> None:
        workspace = copy.deepcopy(self.fixture["workspace"])
        workspace["principia_references"][0]["automatic_status_inheritance"] = True
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-PRINCIPIA-STATUS"):
            self._validate_workspace(workspace)

    def test_canonical_authority_escalation_is_rejected(self) -> None:
        workspace = copy.deepcopy(self.fixture["workspace"])
        workspace["authority"]["canonical_copy_authority"] = True
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-COPIED-AUTHORITY"):
            self._validate_workspace(workspace)


if __name__ == "__main__":
    unittest.main()
