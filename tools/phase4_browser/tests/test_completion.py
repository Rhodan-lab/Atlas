from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, load_json
from tools.phase4_browser.completion import run_workstream2_closure, validate_completion_report

ROOT = Path(__file__).resolve().parents[3]
BROWSER_BASELINE = ROOT / "content" / "fixtures" / "phase4_browser" / "browser-evidence-baseline.json"
SHELL_PATCH = ROOT / "content" / "fixtures" / "phase4_interaction" / "reference-shell-accessibility-patch.json"
WORKSTREAM1_BASELINE = ROOT / "content" / "fixtures" / "phase4_interaction" / "workstream1-completion-baseline.json"


class Workstream2CompletionTests(unittest.TestCase):
    def _run(self, browser=None, patch=None, workstream1=None):
        return run_workstream2_closure(
            browser or load_json(BROWSER_BASELINE),
            patch or load_json(SHELL_PATCH),
            workstream1 or load_json(WORKSTREAM1_BASELINE),
        )

    def test_completion_report_is_deterministic_and_valid(self):
        first = self._run()
        second = self._run()
        self.assertEqual(first, second)
        validation = validate_completion_report(first)
        self.assertEqual(validation["decision"], "valid-workstream2-closure-candidate")
        self.assertEqual(validation["exit_gate_count"], 12)
        self.assertTrue(all(first["exit_gates"].values()))
        self.assertEqual(first["decision"], "proceed-workstream3-read-only-research-workspace")

    def test_external_request_drift_is_rejected(self):
        browser = copy.deepcopy(load_json(BROWSER_BASELINE))
        browser["external_request_count"] = 1
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W2-BROWSER"):
            self._run(browser=browser)

    def test_browser_engine_drift_is_rejected(self):
        browser = copy.deepcopy(load_json(BROWSER_BASELINE))
        browser["browser_engine"]["version"] = "152.0.0.0"
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W2-ENGINE"):
            self._run(browser=browser)

    def test_false_human_verification_is_rejected(self):
        browser = copy.deepcopy(load_json(BROWSER_BASELINE))
        browser["human_verified"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W2-BROWSER"):
            self._run(browser=browser)

    def test_shell_patch_must_be_bound_to_browser_evidence(self):
        patch = copy.deepcopy(load_json(SHELL_PATCH))
        patch["browser_evidence_report_digest"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W2-PATCH"):
            self._run(patch=patch)

    def test_completion_digest_tampering_is_rejected(self):
        report = self._run()
        report["decision"] = "proceed-production-ui"
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W2-COMPLETION"):
            validate_completion_report(report)

    def test_workstream3_cannot_gain_canonical_copy_authority(self):
        report = self._run()
        report["workstream3_entry_boundary"]["canonical_copy_authority"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-BOUNDARY"):
            validate_completion_report(report)

    def test_workstream3_cannot_select_production_architecture(self):
        report = self._run()
        report["workstream3_entry_boundary"]["production_frontend_architecture_selected"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-BOUNDARY"):
            validate_completion_report(report)


if __name__ == "__main__":
    unittest.main()
