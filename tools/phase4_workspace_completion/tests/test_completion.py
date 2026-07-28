from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, load_json
from tools.phase4_workspace_completion.contracts import (
    run_workstream3_closure,
    validate_completion_report,
)

ROOT = Path(__file__).resolve().parents[3]
WORKSPACE_BASELINE = ROOT / "content" / "fixtures" / "phase4_workspace" / "workspace-contract-baseline.json"
SHELL_BASELINE = ROOT / "content" / "fixtures" / "phase4_workspace" / "workspace-shell-baseline.json"
BROWSER_BASELINE = ROOT / "content" / "fixtures" / "phase4_workspace" / "workspace-browser-baseline.json"


class Workstream3CompletionTests(unittest.TestCase):
    def _run(self, *, workspace=None, shell=None, browser=None, decision=None):
        return run_workstream3_closure(
            load_json(WORKSPACE_BASELINE) if workspace is None else workspace,
            load_json(SHELL_BASELINE) if shell is None else shell,
            load_json(BROWSER_BASELINE) if browser is None else browser,
            decision=decision or "proceed-bounded-workspace-fixture-evaluation",
        )

    def test_completion_report_is_deterministic_and_valid(self):
        first = self._run()
        second = self._run()
        self.assertEqual(first, second)
        validation = validate_completion_report(first)
        self.assertEqual(validation["decision"], "valid-workstream3-closure-candidate")
        self.assertEqual(validation["recommendation"], "proceed-bounded-workspace-fixture-evaluation")
        self.assertEqual(validation["exit_gate_count"], 13)
        self.assertTrue(all(first["exit_gates"].values()))
        self.assertFalse(first["recommendation"]["implementation_authorized"])
        self.assertTrue(first["recommendation"]["separate_governance_required"])

    def test_workspace_export_identity_drift_is_rejected(self):
        workspace = copy.deepcopy(load_json(WORKSPACE_BASELINE))
        workspace["export"]["artifact"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-WORKSPACE"):
            self._run(workspace=workspace)

    def test_shell_static_asset_drift_is_rejected(self):
        shell = copy.deepcopy(load_json(SHELL_BASELINE))
        shell["static_assets"]["index.html"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-SHELL"):
            self._run(shell=shell)

    def test_browser_engine_drift_is_rejected(self):
        browser = copy.deepcopy(load_json(BROWSER_BASELINE))
        browser["engine"]["version"] = "152.0.0.0"
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-BROWSER"):
            self._run(browser=browser)

    def test_false_human_verification_is_rejected(self):
        browser = copy.deepcopy(load_json(BROWSER_BASELINE))
        browser["authority"]["human_verified"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-BROWSER"):
            self._run(browser=browser)

    def test_live_principia_dependency_is_rejected(self):
        report = self._run()
        report["authority"]["live_principia_dependency"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-AUTHORITY"):
            validate_completion_report(report)

    def test_production_architecture_selection_is_rejected(self):
        report = self._run()
        report["authority"]["production_frontend_architecture_selected"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-AUTHORITY"):
            validate_completion_report(report)

    def test_account_cloud_or_network_requirement_is_rejected(self):
        for field in ("account_required", "cloud_required", "external_network_required"):
            with self.subTest(field=field):
                report = self._run()
                report["authority"][field] = True
                with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-AUTHORITY"):
                    validate_completion_report(report)

    def test_canonical_review_lifecycle_or_repository_mutation_is_rejected(self):
        for field in ("canonical_mutation", "review_mutation", "lifecycle_mutation", "repository_mutation"):
            with self.subTest(field=field):
                report = self._run()
                report["authority"][field] = True
                with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-AUTHORITY"):
                    validate_completion_report(report)

    def test_candidate_resolution_authority_is_rejected(self):
        report = self._run()
        report["authority"]["automatic_merge_or_resolution"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-AUTHORITY"):
            validate_completion_report(report)

    def test_invalid_recommendation_is_rejected(self):
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-DECISION"):
            self._run(decision="proceed-production-workspace")

    def test_missing_replaceability_evidence_is_rejected(self):
        report = self._run()
        del report["replaceability"]["generated_artifacts_disposable"]
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-REPLACEABILITY"):
            validate_completion_report(report)

    def test_missing_migration_or_rollback_evidence_is_rejected(self):
        report = self._run()
        report["migration_boundary"]["required_checks"] = []
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-MIGRATION"):
            validate_completion_report(report)
        report = self._run()
        report["rollback_boundary"]["previous_valid_workspace_preserved"] = False
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-ROLLBACK"):
            validate_completion_report(report)

    def test_false_exit_gate_is_rejected(self):
        report = self._run()
        report["exit_gates"]["accepted_slice_identities_exact"] = False
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-COMPLETION-GATES"):
            validate_completion_report(report)

    def test_completion_digest_tampering_is_rejected(self):
        report = self._run()
        report["limitations"][0] = "tampered"
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W3-DIGEST"):
            validate_completion_report(report)


if __name__ == "__main__":
    unittest.main()
