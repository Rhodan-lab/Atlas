from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, load_json
from tools.phase4_interaction.completion import (
    run_workstream1_closure,
    validate_completion_report,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL_ROOT = ROOT / "content" / "canonical"
MANIFEST = ROOT / "content" / "fixtures" / "phase4_interaction" / "reference-interactions.v01.json"
INTERACTION_BASELINE = (
    ROOT / "content" / "fixtures" / "phase4_interaction" / "interaction-contract-baseline.json"
)
SHELL_BASELINE = ROOT / "content" / "fixtures" / "phase4_interaction" / "reference-shell-baseline.json"
SHELL_ROOT = ROOT / "apps" / "reference-shell"


class Workstream1CompletionTests(unittest.TestCase):
    def _run(self, interaction=None, shell=None):
        return run_workstream1_closure(
            CANONICAL_ROOT,
            MANIFEST,
            interaction or load_json(INTERACTION_BASELINE),
            shell or load_json(SHELL_BASELINE),
            SHELL_ROOT,
        )

    def test_completion_report_is_deterministic_and_valid(self):
        first = self._run()
        second = self._run()
        self.assertEqual(first, second)
        validation = validate_completion_report(first)
        self.assertEqual(validation["decision"], "valid-workstream1-closure-candidate")
        self.assertEqual(validation["exit_gate_count"], 10)
        self.assertEqual(first["decision"], "proceed-workstream2-browser-accessibility-evidence")
        self.assertTrue(all(first["exit_gates"].values()))

    def test_shell_baseline_authority_escalation_is_rejected(self):
        shell = copy.deepcopy(load_json(SHELL_BASELINE))
        shell["repository_mutation"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W1-SHELL"):
            self._run(shell=shell)

    def test_interaction_report_identity_drift_is_rejected(self):
        interaction = copy.deepcopy(load_json(INTERACTION_BASELINE))
        interaction["report_digest"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W1-INTERACTION"):
            self._run(interaction=interaction)

    def test_completion_digest_tampering_is_rejected(self):
        report = self._run()
        report["implementation_expansion"] = "unbounded-ui-expansion"
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W1-COMPLETION-DIGEST"):
            validate_completion_report(report)

    def test_workstream2_boundary_cannot_activate_live_dependency(self):
        report = self._run()
        report["workstream2_entry_boundary"]["live_principia_dependency"] = True
        with self.assertRaisesRegex(KernelError, "E-PHASE4-W2-BOUNDARY"):
            validate_completion_report(report)


if __name__ == "__main__":
    unittest.main()
