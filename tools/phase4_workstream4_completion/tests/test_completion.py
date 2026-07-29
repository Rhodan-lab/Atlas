from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, load_json, render_json
from tools.phase4_workstream4_completion.closure import (
    build_completion_report,
    seal_record,
    validate_completion_report,
)
from tools.phase4_workstream4_completion.verify_baseline import verify_baseline

ROOT = Path(__file__).resolve().parents[3]
GENERALIZATION = ROOT / "content/fixtures/phase4_workspace_generalization/catalase-generalization-baseline.json"
PACKAGE = ROOT / "content/fixtures/phase4_workspace_reader_reuse/reader-reuse-baseline.json"
BROWSER = ROOT / "content/fixtures/phase4_workspace_reader_browser/reader-reuse-browser-baseline.json"
BASELINE = ROOT / "content/fixtures/phase4_workstream4_completion/workstream4-completion-baseline.json"


class Workstream4CompletionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generalization = load_json(GENERALIZATION)
        self.package = load_json(PACKAGE)
        self.browser = load_json(BROWSER)
        self.baseline = load_json(BASELINE)

    def build(self, **kwargs):
        return build_completion_report(self.generalization, self.package, self.browser, **kwargs)

    def test_report_and_validation_are_deterministic(self) -> None:
        first = self.build()
        second = self.build()
        self.assertEqual(render_json(first), render_json(second))
        validation_first = validate_completion_report(first)
        validation_second = validate_completion_report(second)
        self.assertEqual(render_json(validation_first), render_json(validation_second))
        self.assertEqual(14, validation_first["exit_gate_count"])
        self.assertEqual(20, validation_first["negative_case_count"])
        self.assertEqual("proceed-phase4-completion-governance", validation_first["recommendation"])
        self.assertFalse(validation_first["implementation_authorized"])

    def test_pinned_completion_baseline(self) -> None:
        report = self.build()
        validation = validate_completion_report(report)
        verify_baseline(self.baseline, report, validation)

    def test_tampered_completion_baseline_rejected(self) -> None:
        report = self.build()
        validation = validate_completion_report(report)
        changed = copy.deepcopy(self.baseline)
        changed["completion_report"]["artifact"]["sha256"] = "0" * 64
        with self.assertRaises(KernelError):
            verify_baseline(changed, report, validation)

    def test_other_bounded_decisions_validate(self) -> None:
        for decision in ("hold-accepted-workstream4", "reject-workstream4-generalization"):
            report = self.build(decision=decision)
            validation = validate_completion_report(report)
            self.assertEqual(decision, validation["recommendation"])
            self.assertFalse(report["recommendation"]["implementation_authorized"])

    def test_unknown_decision_rejected(self) -> None:
        with self.assertRaises(KernelError):
            self.build(decision="deploy-production")

    def test_generalization_identity_drift_rejected(self) -> None:
        changed = copy.deepcopy(self.generalization)
        changed["fixture"]["sha256"] = "0" * 64
        with self.assertRaises(KernelError):
            build_completion_report(changed, self.package, self.browser)

    def test_second_generalized_fixture_rejected(self) -> None:
        changed = copy.deepcopy(self.package)
        changed["counts"]["generalized_fixtures"] = 2
        with self.assertRaises(KernelError):
            build_completion_report(self.generalization, changed, self.browser)

    def test_reader_asset_mutation_rejected(self) -> None:
        changed = copy.deepcopy(self.package)
        changed["files"]["packages/catalase/app.js"]["sha256"] = "f" * 64
        with self.assertRaises(KernelError):
            build_completion_report(self.generalization, changed, self.browser)

    def test_browser_external_request_rejected(self) -> None:
        changed = copy.deepcopy(self.browser)
        changed["counts"]["external_requests"] = 1
        with self.assertRaises(KernelError):
            build_completion_report(self.generalization, self.package, changed)

    def test_candidate_resolution_rejected(self) -> None:
        changed = copy.deepcopy(self.browser)
        changed["claims"]["candidates_unresolved"] = False
        with self.assertRaises(KernelError):
            build_completion_report(self.generalization, self.package, changed)

    def test_selector_fallback_rejected(self) -> None:
        changed = copy.deepcopy(self.browser)
        changed["claims"]["selector_unknown_fixture_refused"] = False
        with self.assertRaises(KernelError):
            build_completion_report(self.generalization, self.package, changed)

    def test_resealed_failed_gate_rejected(self) -> None:
        report = self.build()
        changed = copy.deepcopy(report)
        changed["exit_gates"]["download_and_zero_external_network_preserved"] = False
        with self.assertRaises(KernelError):
            validate_completion_report(seal_record(changed))

    def test_resealed_self_authorization_rejected(self) -> None:
        report = self.build()
        changed = copy.deepcopy(report)
        changed["recommendation"]["implementation_authorized"] = True
        with self.assertRaises(KernelError):
            validate_completion_report(seal_record(changed))

    def test_resealed_production_authority_rejected(self) -> None:
        report = self.build()
        changed = copy.deepcopy(report)
        changed["authority"]["production_frontend_architecture_selected"] = True
        with self.assertRaises(KernelError):
            validate_completion_report(seal_record(changed))

    def test_resealed_false_human_verification_rejected(self) -> None:
        report = self.build()
        changed = copy.deepcopy(report)
        changed["review_policy"]["human_verified"] = True
        with self.assertRaises(KernelError):
            validate_completion_report(seal_record(changed))

    def test_unsealed_digest_tamper_rejected(self) -> None:
        report = self.build()
        changed = copy.deepcopy(report)
        changed["limitations"][0] = "Universal generality proven."
        with self.assertRaises(KernelError):
            validate_completion_report(changed)


if __name__ == "__main__":
    unittest.main()
