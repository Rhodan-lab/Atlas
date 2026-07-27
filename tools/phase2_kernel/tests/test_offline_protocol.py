from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.kernel import KernelError, KernelRepository, load_json
from tools.phase2_kernel.offline_protocol import (
    ATLAS_BATCH_RECEIPT_CONTRACT,
    ATLAS_PROTOCOL_AUDIT_CONTRACT,
    audit_offline_protocol,
    import_offline_batch,
    load_snapshot_documents,
    sha256_document,
    verify_principia_receipt,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURES = ROOT / "content" / "fixtures" / "phase2_protocol"
SNAPSHOT = FIXTURES / "principia-phase18.snapshot.json"
BATCH = FIXTURES / "thermal-control.multi-artifact.batch.v02.json"
RECEIPT = FIXTURES / "thermal-control.multi-artifact.receipt.v02.json"
EVENTS = FIXTURES / "thermal-control.lifecycle-events.v01.json"
ACKS = FIXTURES / "thermal-control.lifecycle-acknowledgements.v01.json"
CHAIN = FIXTURES / "thermal-control.event-protocol-chain.v01.json"
RECONCILIATION = FIXTURES / "thermal-control.reconciliation-report.v01.json"


class OfflineProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = KernelRepository(compile_canonical(CANONICAL))
        cls.snapshot, cls.documents = load_snapshot_documents(SNAPSHOT)
        cls.batch = load_json(BATCH)
        cls.receipt = load_json(RECEIPT)
        cls.events = load_json(EVENTS)
        cls.acks = load_json(ACKS)
        cls.chain = load_json(CHAIN)
        cls.reconciliation = load_json(RECONCILIATION)

    def test_snapshot_is_exact_and_offline(self) -> None:
        self.assertEqual(
            self.snapshot["source_commit"],
            "4ecb41ad4f9f524e83cc0db43f672bd9dcf3b67a",
        )
        self.assertEqual(len(self.documents), 9)
        self.assertFalse(self.snapshot["live"])

    def test_atomic_batch_reimports_three_exact_artifacts(self) -> None:
        receipt = import_offline_batch(self.batch, self.documents, self.repository)
        self.assertEqual(receipt["contract"], ATLAS_BATCH_RECEIPT_CONTRACT)
        self.assertTrue(receipt["atomic"])
        self.assertFalse(receipt["live"])
        self.assertEqual(receipt["record_count"], 3)
        self.assertEqual(
            [record["id"] for record in receipt["records"]],
            [
                "principia:failure-pattern:feedback-instability",
                "principia:investigation:room-cooling",
                "principia:system-dossier:refrigerator",
            ],
        )
        feedback = receipt["records"][0]
        self.assertIn(
            "model:en:delayed-correction-recurrence@2",
            [dependency["key"] for dependency in feedback["dependencies"]],
        )

    def test_principia_receipt_matches_fresh_atlas_import(self) -> None:
        atlas_receipt = import_offline_batch(
            self.batch,
            self.documents,
            self.repository,
        )
        verification = verify_principia_receipt(
            self.batch,
            self.receipt,
            atlas_receipt,
        )
        self.assertTrue(verification["verified"])
        self.assertEqual(verification["record_count"], 3)
        self.assertFalse(verification["repository_mutation"])

    def test_full_protocol_audit_recomputes_fanout_and_reconciliation(self) -> None:
        report = audit_offline_protocol(
            self.batch,
            self.receipt,
            self.events,
            self.acks,
            self.chain,
            self.reconciliation,
            self.documents,
            self.repository,
        )
        self.assertEqual(report["contract"], ATLAS_PROTOCOL_AUDIT_CONTRACT)
        self.assertEqual(report["record_count"], 3)
        self.assertEqual(report["event_count"], 2)
        self.assertEqual(report["acknowledgement_count"], 2)
        self.assertEqual(report["reconciled_count"], 2)
        self.assertEqual(report["decision"], "verified-no-mutation")
        self.assertEqual(report["fixture_kind"], "bounded-synthetic")
        self.assertFalse(report["automatic_status_change"])
        self.assertFalse(report["automatic_release_action"])
        self.assertFalse(report["repository_mutation"])

    def test_partial_batch_cannot_match_atomic_receipt(self) -> None:
        batch = copy.deepcopy(self.batch)
        batch["inputs"].pop()
        with self.assertRaisesRegex(KernelError, "E-RECEIPT-BATCH-DIGEST"):
            audit_offline_protocol(
                batch,
                self.receipt,
                self.events,
                self.acks,
                self.chain,
                self.reconciliation,
                self.documents,
                self.repository,
            )

    def test_corrupted_export_digest_is_rejected_before_import(self) -> None:
        documents = dict(self.documents)
        path = "integration/principia-atlas/exports/room-cooling.external-dependent.fixture.json"
        payload = json.loads(documents[path].decode("utf-8"))
        payload["revision"] = 2
        documents[path] = json.dumps(payload, indent=2).encode("utf-8") + b"\n"
        with self.assertRaisesRegex(
            KernelError,
            "E-BATCH-EXPORT-DIGEST-MISMATCH",
        ):
            import_offline_batch(self.batch, documents, self.repository)

    def test_live_batch_is_rejected(self) -> None:
        batch = copy.deepcopy(self.batch)
        batch["live"] = True
        with self.assertRaisesRegex(KernelError, "E-BATCH-LIVE"):
            import_offline_batch(batch, self.documents, self.repository)

    def test_event_digest_corruption_is_rejected(self) -> None:
        events = copy.deepcopy(self.events)
        events["events"][0]["event"]["transition"]["reason_code"] = "changed"
        with self.assertRaisesRegex(KernelError, "E-EVENT-DIGEST-MISMATCH"):
            audit_offline_protocol(
                self.batch,
                self.receipt,
                events,
                self.acks,
                self.chain,
                self.reconciliation,
                self.documents,
                self.repository,
            )

    def test_weakened_acknowledgement_action_is_rejected(self) -> None:
        acknowledgements = copy.deepcopy(self.acks)
        first = acknowledgements["acknowledgements"][0]
        first["acknowledgement"]["required_action"] = "inspect"
        first["acknowledgement_sha256"] = sha256_document(first["acknowledgement"])
        with self.assertRaisesRegex(KernelError, "E-ACK-ACTION"):
            audit_offline_protocol(
                self.batch,
                self.receipt,
                self.events,
                acknowledgements,
                self.chain,
                self.reconciliation,
                self.documents,
                self.repository,
            )

    def test_acknowledgement_affected_set_is_recomputed_by_atlas(self) -> None:
        acknowledgements = copy.deepcopy(self.acks)
        first = acknowledgements["acknowledgements"][0]
        first["acknowledgement"]["affected_artifacts"].pop()
        first["acknowledgement_sha256"] = sha256_document(first["acknowledgement"])
        with self.assertRaisesRegex(KernelError, "E-ACK-AFFECTED"):
            audit_offline_protocol(
                self.batch,
                self.receipt,
                self.events,
                acknowledgements,
                self.chain,
                self.reconciliation,
                self.documents,
                self.repository,
            )

    def test_chain_predecessor_mismatch_is_rejected(self) -> None:
        chain = copy.deepcopy(self.chain)
        chain["links"][1]["previous_event_sha256"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-CHAIN-LINK"):
            audit_offline_protocol(
                self.batch,
                self.receipt,
                self.events,
                self.acks,
                chain,
                self.reconciliation,
                self.documents,
                self.repository,
            )

    def test_stale_reconciliation_reference_is_rejected(self) -> None:
        reconciliation = copy.deepcopy(self.reconciliation)
        reconciliation["records"][0]["affected_artifacts"][0][
            "current_revision"
        ] = 2
        with self.assertRaisesRegex(KernelError, "E-RECONCILIATION-STALE"):
            audit_offline_protocol(
                self.batch,
                self.receipt,
                self.events,
                self.acks,
                self.chain,
                reconciliation,
                self.documents,
                self.repository,
            )


if __name__ == "__main__":
    unittest.main()
