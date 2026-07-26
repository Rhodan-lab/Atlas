from __future__ import annotations

import copy
import hashlib
import unittest
from pathlib import Path

from tools.phase2_kernel.benchmark import BENCHMARK_CONTRACT, run_benchmark
from tools.phase2_kernel.bridge import (
    BRIDGE_ADAPTER_CONTRACT,
    LIFECYCLE_IMPACT_CONTRACT,
    PRINCIPIA_EXTERNAL_DEPENDENT_CONTRACT,
    import_principia_candidate,
    lifecycle_impact_report,
)
from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.kernel import KernelError, KernelRepository, load_json

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURES = ROOT / "content" / "fixtures" / "phase2_bridge"
PRINCIPIA_FIXTURE = FIXTURES / "principia-feedback-pr16-v02.json"
SOURCE_RECORD = FIXTURES / "principia-feedback-pr16-v02.source.json"
MODEL_ID = "model:en:delayed-correction-recurrence"


class PrincipiaV02BridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)
        cls.repository = KernelRepository(cls.runtime)
        cls.payload = load_json(PRINCIPIA_FIXTURE)

    def test_fixture_matches_recorded_principia_snapshot(self) -> None:
        source = load_json(SOURCE_RECORD)
        digest = hashlib.sha256(PRINCIPIA_FIXTURE.read_bytes()).hexdigest()
        self.assertEqual(source["source_pull_request"], 16)
        self.assertEqual(
            source["source_merge_commit"],
            "eb3a00dfbfdfaa5470cb40505fa213e5349a917f",
        )
        self.assertEqual(
            source["source_blob_sha"],
            "a0ab1e098b17a5cfe9fee521394513461a2f4e51",
        )
        self.assertEqual(digest, source["source_sha256"])
        self.assertFalse(source["live"])

    def test_merged_principia_export_imports_without_status_inheritance(self) -> None:
        imported = import_principia_candidate(self.payload, self.repository)
        self.assertEqual(
            imported["source_contract"], PRINCIPIA_EXTERNAL_DEPENDENT_CONTRACT
        )
        self.assertEqual(imported["adapter_contract"], BRIDGE_ADAPTER_CONTRACT)
        self.assertTrue(imported["legacy_id_index_verified"])
        self.assertFalse(imported["live"])
        self.assertEqual(imported["status_inheritance"], "prohibited")
        exact = {(item["id"], item["revision"]) for item in imported["dependencies"]}
        self.assertIn((MODEL_ID, 2), exact)
        self.assertEqual(len(exact), 4)

    def test_legacy_id_index_must_match_exact_dependencies(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["depends_on"].pop()
        with self.assertRaisesRegex(KernelError, "E-PRINCIPIA-LEGACY-INDEX"):
            import_principia_candidate(payload, self.repository)

    def test_v02_export_order_is_deterministic(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["depends_on_exact"].reverse()
        with self.assertRaisesRegex(KernelError, "E-PRINCIPIA-EXPORT-ORDER"):
            import_principia_candidate(payload, self.repository)

    def test_v02_status_data_is_rejected_at_any_depth(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["depends_on_exact"][0]["release_status"] = "draft"
        with self.assertRaisesRegex(KernelError, "E-BRIDGE-STATUS-INHERITANCE"):
            import_principia_candidate(payload, self.repository)

    def test_v02_live_activation_remains_frozen(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["live"] = True
        with self.assertRaisesRegex(KernelError, "E-BRIDGE-LIVE-FROZEN"):
            import_principia_candidate(payload, self.repository)

    def _repository_with_model_state(
        self,
        status: str,
        staleness: str = "current",
    ) -> KernelRepository:
        runtime = copy.deepcopy(self.runtime)
        for entity in runtime["entities"]:
            if entity["id"] == MODEL_ID and entity["revision"] == 2:
                entity["status"] = status
                entity["staleness"] = staleness
                entity["metadata"]["status"] = status
                entity["metadata"]["staleness"] = staleness
                break
        else:
            self.fail("model fixture not found")
        return KernelRepository(runtime)

    def test_deprecated_entity_escalates_inspect_to_revalidate(self) -> None:
        repository = self._repository_with_model_state("deprecated")
        imported = import_principia_candidate(self.payload, repository)
        report = lifecycle_impact_report(repository, MODEL_ID, 2, [imported])
        dependent = report["external_dependents"][0]
        self.assertEqual(report["contract"], LIFECYCLE_IMPACT_CONTRACT)
        self.assertEqual(dependent["declared_action"], "inspect")
        self.assertEqual(dependent["effective_action"], "revalidate")
        self.assertEqual(dependent["lifecycle_reason"], "atlas-entity-deprecated")
        self.assertFalse(report["automatic_status_change"])
        self.assertFalse(report["automatic_release_action"])

    def test_retracted_entity_escalates_to_block_release(self) -> None:
        repository = self._repository_with_model_state("retracted")
        imported = import_principia_candidate(self.payload, repository)
        report = lifecycle_impact_report(repository, MODEL_ID, 2, [imported])
        dependent = report["external_dependents"][0]
        self.assertEqual(dependent["declared_action"], "inspect")
        self.assertEqual(dependent["effective_action"], "block-release")
        self.assertEqual(dependent["lifecycle_reason"], "atlas-entity-retracted")
        self.assertFalse(report["automatic_release_action"])

    def test_confirmed_stale_entity_requires_revalidation(self) -> None:
        repository = self._repository_with_model_state(
            "draft", staleness="confirmed-stale"
        )
        imported = import_principia_candidate(self.payload, repository)
        report = lifecycle_impact_report(repository, MODEL_ID, 2, [imported])
        dependent = report["external_dependents"][0]
        self.assertEqual(dependent["effective_action"], "revalidate")
        self.assertEqual(
            dependent["lifecycle_reason"], "atlas-staleness-confirmed-stale"
        )

    def test_representative_benchmark_report_is_well_formed(self) -> None:
        report = run_benchmark(
            CANONICAL,
            PRINCIPIA_FIXTURE,
            compile_iterations=1,
            operation_iterations=3,
        )
        self.assertEqual(report["contract"], BENCHMARK_CONTRACT)
        self.assertEqual(
            report["fixture_contract"], PRINCIPIA_EXTERNAL_DEPENDENT_CONTRACT
        )
        self.assertEqual(set(report["metrics"]), {
            "compile",
            "exact_lookup",
            "provenance",
            "bridge_import",
            "impact",
        })
        for metric in report["metrics"].values():
            self.assertGreaterEqual(metric["median_ms"], 0)
            self.assertGreaterEqual(metric["p95_ms"], 0)


if __name__ == "__main__":
    unittest.main()
