from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json
from tools.phase4_workspace_generalization.constants import RECOMMENDATION
from tools.phase4_workspace_generalization.evaluation import (
    run_generalization,
    validate_evaluation_report,
)
from tools.phase4_workspace_generalization.spec import (
    validate_spec,
)

ROOT = Path(__file__).resolve().parents[3]
SPEC = ROOT / "content" / "fixtures" / "phase4_workspace_generalization" / "catalase-generalization.v01.json"
STRUCTURED_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "structured-baseline.json"
CANONICAL_ROOT = ROOT / "content" / "canonical"


class Workstream4GeneralizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repository = KernelRepository(compile_canonical(CANONICAL_ROOT))

    def _run(self, spec=None):
        return run_generalization(
            spec or load_json(SPEC),
            CANONICAL_ROOT,
            load_json(STRUCTURED_BASELINE),
        )

    def test_generalization_is_deterministic_and_valid(self):
        first = self._run()
        second = self._run()
        self.assertEqual(first, second)
        validation = validate_evaluation_report(first["evaluation_report"])
        self.assertEqual(validation["decision"], "valid-workstream4-generalization-candidate")
        self.assertEqual(validation["recommendation"], RECOMMENDATION)
        self.assertEqual(validation["exit_gate_count"], 13)
        self.assertEqual(validation["negative_case_count"], 21)

    def test_exactly_five_catalase_entries_are_selected(self):
        result = self._run()
        entries = result["fixture"]["workspace"]["entries"]
        self.assertEqual(len(entries), 5)
        self.assertTrue(all("catalase" in entry["exact_reference"]["id"] for entry in entries))
        self.assertEqual(sorted(entry["position"] for entry in entries), [1, 2, 3, 4, 5])
        self.assertEqual(
            {entry["decision"]["action"] for entry in entries},
            {"include", "exclude", "context"},
        )

    def test_non_catalase_entry_is_rejected(self):
        spec = copy.deepcopy(load_json(SPEC))
        spec["selected_entries"][0]["exact_reference"] = {
            "id": "claim:en:recommender-effects-are-context-dependent",
            "revision": 1,
        }
        with self.assertRaisesRegex(KernelError, "E-W4-DOMAIN"):
            validate_spec(spec, self.repository)

    def test_duplicate_selection_is_rejected(self):
        spec = copy.deepcopy(load_json(SPEC))
        spec["selected_entries"][1]["exact_reference"] = dict(
            spec["selected_entries"][0]["exact_reference"]
        )
        with self.assertRaisesRegex(KernelError, "E-W4-SELECTION"):
            validate_spec(spec, self.repository)

    def test_browser_implementation_cannot_be_authorized(self):
        spec = copy.deepcopy(load_json(SPEC))
        spec["authority"]["browser_implementation_authorized"] = True
        with self.assertRaisesRegex(KernelError, "E-W4-AUTHORITY"):
            validate_spec(spec, self.repository)

    def test_new_canonical_authoring_cannot_be_authorized(self):
        spec = copy.deepcopy(load_json(SPEC))
        spec["authority"]["new_canonical_authoring_authorized"] = True
        with self.assertRaisesRegex(KernelError, "E-W4-AUTHORITY"):
            validate_spec(spec, self.repository)

    def test_report_recommendation_tampering_is_rejected(self):
        report = self._run()["evaluation_report"]
        report["decision"] = "proceed-production-workspace"
        with self.assertRaisesRegex(KernelError, "E-W4-DECISION"):
            validate_evaluation_report(report)

    def test_report_authority_tampering_is_rejected(self):
        report = self._run()["evaluation_report"]
        report["authority"]["canonical_mutation"] = True
        with self.assertRaisesRegex(KernelError, "E-W4-AUTHORITY"):
            validate_evaluation_report(report)

    def test_report_digest_tampering_is_rejected(self):
        report = self._run()["evaluation_report"]
        report["limitations"].append("tampered")
        with self.assertRaisesRegex(KernelError, "E-W4-DIGEST"):
            validate_evaluation_report(report)


if __name__ == "__main__":
    unittest.main()
