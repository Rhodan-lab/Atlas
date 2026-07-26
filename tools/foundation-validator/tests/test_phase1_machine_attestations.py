from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GATE_SPEC = importlib.util.spec_from_file_location(
    "phase1_review_gate", ROOT / "phase1_review_gate.py"
)
assert GATE_SPEC and GATE_SPEC.loader
gate = importlib.util.module_from_spec(GATE_SPEC)
sys.modules[GATE_SPEC.name] = gate
GATE_SPEC.loader.exec_module(gate)

ATTESTATION_SPEC = importlib.util.spec_from_file_location(
    "phase1_machine_attestations", ROOT / "phase1_machine_attestations.py"
)
assert ATTESTATION_SPEC and ATTESTATION_SPEC.loader
attestations = importlib.util.module_from_spec(ATTESTATION_SPEC)
sys.modules[ATTESTATION_SPEC.name] = attestations
ATTESTATION_SPEC.loader.exec_module(attestations)


class MachineAttestationTests(unittest.TestCase):
    def test_exact_expected_task_count(self) -> None:
        records = attestations.expected_records()
        structural = [r for r in records.values() if r["review_type"] == "structural"]
        reproducibility = [
            r for r in records.values() if r["review_type"] == "reproducibility"
        ]
        self.assertEqual(len(records), 13)
        self.assertEqual(len(structural), 10)
        self.assertEqual(len(reproducibility), 3)

    def test_all_records_are_valid_nonaccountable_machine_reviews(self) -> None:
        for filename, record in attestations.expected_records().items():
            self.assertEqual(gate.validate_review_record(record, filename), [])
            self.assertEqual(record["reviewer"]["kind"], "machine")
            self.assertEqual(record["reviewer"]["independence"], "not-applicable")
            self.assertFalse(record["reviewer"]["accountable"])
            self.assertFalse(record["permits_promotion"])
            self.assertEqual(record["outcome"], "pass")
            self.assertEqual(record["findings"], [])

    def test_reproducibility_is_limited_to_fully_specified_entities(self) -> None:
        actual = {
            record["entity"]["id"]
            for record in attestations.expected_records().values()
            if record["review_type"] == "reproducibility"
        }
        self.assertEqual(
            actual,
            {
                "claim:en:stated-delayed-recurrence-oscillates",
                "evidence:en:delayed-feedback-periodic-sequence",
                "model:en:delayed-correction-recurrence",
            },
        )

    def test_sequence_is_recalculated_not_copied(self) -> None:
        self.assertEqual(
            attestations.recalculate_sequence(), attestations.EXPECTED_SEQUENCE
        )

    def test_generate_and_check_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            attestations.write_records(root)
            self.assertEqual(attestations.check_records(root), [])
            target = root / "feedback-model-structural-machine.json"
            target.write_text("{}\n", encoding="utf-8")
            self.assertTrue(attestations.check_records(root))


if __name__ == "__main__":
    unittest.main()
