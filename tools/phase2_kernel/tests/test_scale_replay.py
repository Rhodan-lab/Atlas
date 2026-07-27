from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import (
    RECEIPT_LEDGER_CONTRACT,
    REPLAY_MATRIX_CONTRACT,
    SCALE_PROFILE_CONTRACT,
    SCALED_BENCHMARK_CONTRACT,
    KernelError,
    KernelRepository,
    apply_offline_batch,
    compile_canonical,
    continued_batch,
    load_json,
    load_snapshot_documents,
    new_receipt_ledger,
    render_json,
    run_replay_recovery_matrix,
    run_scaled_benchmark,
    validate_receipt_ledger,
    write_synthetic_corpus,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
PROTOCOL = ROOT / "content" / "fixtures" / "phase2_protocol"
SNAPSHOT = PROTOCOL / "principia-phase18.snapshot.json"
BASE_BATCH = PROTOCOL / "thermal-control.multi-artifact.batch.v02.json"


class ScaleReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = KernelRepository(compile_canonical(CANONICAL))
        _, cls.documents = load_snapshot_documents(SNAPSHOT)
        cls.base_batch = load_json(BASE_BATCH)

    def test_synthetic_corpus_compiles_deterministically(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "canonical"
            identity = write_synthetic_corpus(root, 8)
            first = compile_canonical(root)
            second = compile_canonical(root)
            self.assertEqual(identity["entity_count"], 34)
            self.assertEqual(first["entity_count"], 34)
            self.assertEqual(render_json(first), render_json(second))
            repository = KernelRepository(first)
            sources = repository.provenance_sources(
                "synthesis:en:synthetic-scale-000008", 1
            )
            self.assertEqual(
                {source["id"] for source in sources},
                {
                    "src:synthetic-scale-000008",
                    "src:synthetic-scale-root",
                },
            )

    def test_small_scaled_benchmark_is_complete(self) -> None:
        report = run_scaled_benchmark(
            {
                "compile_iterations": 1,
                "contract": SCALE_PROFILE_CONTRACT,
                "external_dependents": 4,
                "groups": 4,
                "live": False,
                "mode": "scale-replay-candidate",
                "operation_iterations": 1,
            }
        )
        self.assertEqual(report["contract"], SCALED_BENCHMARK_CONTRACT)
        self.assertEqual(report["entity_count"], 18)
        self.assertEqual(report["external_dependent_count"], 4)
        self.assertTrue(report["deterministic_runtime"])
        self.assertFalse(report["live"])
        self.assertFalse(report["mutation"])
        self.assertEqual(
            set(report["metrics"]),
            {
                "bridge_import_all",
                "compile",
                "exact_lookup",
                "impact_all",
                "provenance",
                "runtime_admission",
            },
        )

    def test_two_batches_and_idempotent_replay(self) -> None:
        ledger0 = new_receipt_ledger()
        self.assertEqual(ledger0["contract"], RECEIPT_LEDGER_CONTRACT)
        ledger1, first = apply_offline_batch(
            ledger0, self.base_batch, self.documents, self.repository
        )
        replayed, replay = apply_offline_batch(
            ledger1, self.base_batch, self.documents, self.repository
        )
        self.assertEqual(first["decision"], "accepted")
        self.assertEqual(replay["decision"], "idempotent-no-op")
        self.assertEqual(render_json(ledger1), render_json(replayed))

        batch2 = continued_batch(
            self.base_batch,
            sequence=2,
            previous_receipt_sha256=ledger1["head_receipt_sha256"],
            batch_id="principia-atlas:offline-batch:thermal-control:0002",
            input_count=2,
        )
        ledger2, second = apply_offline_batch(
            ledger1, batch2, self.documents, self.repository
        )
        self.assertEqual(second["decision"], "accepted")
        self.assertEqual(ledger2["head_sequence"], 2)
        self.assertEqual(validate_receipt_ledger(ledger2)["entry_count"], 2)

    def test_skipped_conflicting_and_wrong_predecessor_are_rejected(self) -> None:
        ledger1, _ = apply_offline_batch(
            new_receipt_ledger(), self.base_batch, self.documents, self.repository
        )
        skipped = continued_batch(
            self.base_batch,
            sequence=3,
            previous_receipt_sha256=ledger1["head_receipt_sha256"],
            batch_id="principia-atlas:offline-batch:thermal-control:0003",
            input_count=2,
        )
        with self.assertRaisesRegex(KernelError, "E-REPLAY-SKIPPED"):
            apply_offline_batch(ledger1, skipped, self.documents, self.repository)

        conflict = copy.deepcopy(self.base_batch)
        conflict["batch_id"] = "principia-atlas:offline-batch:thermal-control:conflict"
        conflict["inputs"] = conflict["inputs"][:2]
        with self.assertRaisesRegex(KernelError, "E-REPLAY-CONFLICT"):
            apply_offline_batch(ledger1, conflict, self.documents, self.repository)

        wrong = continued_batch(
            self.base_batch,
            sequence=2,
            previous_receipt_sha256="0" * 64,
            batch_id="principia-atlas:offline-batch:thermal-control:0002",
            input_count=2,
        )
        with self.assertRaisesRegex(KernelError, "E-REPLAY-PREDECESSOR"):
            apply_offline_batch(ledger1, wrong, self.documents, self.repository)

    def test_replay_matrix_is_deterministic_and_non_mutating(self) -> None:
        first = run_replay_recovery_matrix(
            self.base_batch, self.documents, self.repository
        )
        second = run_replay_recovery_matrix(
            self.base_batch, self.documents, self.repository
        )
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(first["contract"], REPLAY_MATRIX_CONTRACT)
        self.assertEqual(first["decision"], "verified-no-mutation")
        self.assertEqual(first["accepted_sequences"], [1, 2])
        self.assertTrue(first["idempotent_replay"])
        self.assertEqual(first["final_head_sequence"], 2)
        self.assertEqual(len(first["rejected_cases"]), 5)
        self.assertFalse(first["live"])
        self.assertFalse(first["automatic_status_change"])
        self.assertFalse(first["automatic_release_action"])
        self.assertFalse(first["repository_mutation"])


if __name__ == "__main__":
    unittest.main()
