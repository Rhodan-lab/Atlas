from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.kernel import KernelError, KernelRepository, load_json
from tools.phase2_kernel.offline_protocol import (
    ATLAS_BATCH_RECEIPT_CONTRACT,
    ATLAS_PROTOCOL_AUDIT_CONTRACT,
    sha256_document,
    verify_principia_receipt,
)
from tools.phase2_kernel.offline_protocol_policy import (
    EXPECTED_PRINCIPIA_COMMIT,
    audit_pinned_offline_protocol,
    import_pinned_offline_batch,
    load_pinned_snapshot_documents,
    validate_pinned_snapshot,
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
        cls.snapshot, cls.documents = load_pinned_snapshot_documents(SNAPSHOT)
        cls.batch = load_json(BATCH)
        cls.receipt = load_json(RECEIPT)
        cls.events = load_json(EVENTS)
        cls.acks = load_json(ACKS)
        cls.chain = load_json(CHAIN)
        cls.reconciliation = load_json(RECONCILIATION)

    def audit(
        self,
        *,
        batch: dict | None = None,
        receipt: dict | None = None,
        events: dict | None = None,
        acknowledgements: dict | None = None,
        chain: dict | None = None,
        reconciliation: dict | None = None,
        documents: dict[str, bytes] | None = None,
    ) -> dict:
        return audit_pinned_offline_protocol(
            self.snapshot,
            batch or self.batch,
            receipt or self.receipt,
            events or self.events,
            acknowledgements or self.acks,
            chain or self.chain,
            reconciliation or self.reconciliation,
            documents or self.documents,
            self.repository,
        )

    def test_snapshot_is_exact_and_offline(self) -> None:
        self.assertEqual(self.snapshot["source_commit"], EXPECTED_PRINCIPIA_COMMIT)
        self.assertEqual(self.snapshot["source_pull_request"], 25)
        self.assertEqual(len(self.documents), 9)
        self.assertFalse(self.snapshot["live"])

    def test_snapshot_fixture_path_cannot_escape_repository(self) -> None:
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["files"][0]["fixture_path"] = "../../etc/passwd"
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            dir=FIXTURES,
            encoding="utf-8",
        ) as handle:
            json.dump(snapshot, handle)
            handle.flush()
            with self.assertRaisesRegex(KernelError, "E-SNAPSHOT-PATH-ESCAPE"):
                validate_pinned_snapshot(Path(handle.name))

    def test_atomic_batch_reimports_three_exact_artifacts(self) -> None:
        receipt = import_pinned_offline_batch(
            self.batch,
            self.documents,
            self.repository,
        )
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

    def test_complete_atlas_snapshot_metadata_is_required(self) -> None:
        batch = copy.deepcopy(self.batch)
        batch["atlas_snapshot"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-BATCH-ATLAS-SNAPSHOT"):
            import_pinned_offline_batch(batch, self.documents, self.repository)

    def test_principia_receipt_matches_fresh_atlas_import(self) -> None:
        atlas_receipt = import_pinned_offline_batch(
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
        report = self.audit()
        self.assertEqual(report["contract"], ATLAS_PROTOCOL_AUDIT_CONTRACT)
        self.assertEqual(report["record_count"], 3)
        self.assertEqual(report["event_count"], 2)
        self.assertEqual(report["acknowledgement_count"], 2)
        self.assertEqual(report["reconciled_count"], 2)
        self.assertEqual(report["decision"], "verified-no-mutation")
        self.assertEqual(report["fixture_kind"], "bounded-synthetic")
        self.assertEqual(report["source_commit"], EXPECTED_PRINCIPIA_COMMIT)
        self.assertEqual(report["source_pull_request"], 25)
        self.assertFalse(report["automatic_status_change"])
        self.assertFalse(report["automatic_release_action"])
        self.assertFalse(report["repository_mutation"])

    def test_partial_batch_cannot_match_atomic_receipt(self) -> None:
        batch = copy.deepcopy(self.batch)
        batch["inputs"].pop()
        with self.assertRaisesRegex(KernelError, "E-RECEIPT-BATCH-DIGEST"):
            self.audit(batch=batch)

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
            import_pinned_offline_batch(self.batch, documents, self.repository)

    def test_live_batch_is_rejected(self) -> None:
        batch = copy.deepcopy(self.batch)
        batch["live"] = True
        with self.assertRaisesRegex(KernelError, "E-BATCH-LIVE"):
            import_pinned_offline_batch(batch, self.documents, self.repository)

    def test_event_digest_corruption_is_rejected(self) -> None:
        events = copy.deepcopy(self.events)
        events["events"][0]["event"]["transition"]["reason_code"] = "changed"
        with self.assertRaisesRegex(KernelError, "E-EVENT-DIGEST-MISMATCH"):
            self.audit(events=events)

    def test_duplicate_event_id_is_rejected(self) -> None:
        events = copy.deepcopy(self.events)
        events["events"][1]["event"]["event_id"] = events["events"][0]["event"][
            "event_id"
        ]
        with self.assertRaisesRegex(KernelError, "E-EVENT-DUPLICATE"):
            self.audit(events=events)

    def test_weakened_acknowledgement_action_is_rejected(self) -> None:
        acknowledgements = copy.deepcopy(self.acks)
        first = acknowledgements["acknowledgements"][0]
        first["acknowledgement"]["required_action"] = "inspect"
        first["acknowledgement_sha256"] = sha256_document(first["acknowledgement"])
        with self.assertRaisesRegex(KernelError, "E-ACK-ACTION"):
            self.audit(acknowledgements=acknowledgements)

    def test_acknowledgement_affected_set_is_recomputed_by_atlas(self) -> None:
        acknowledgements = copy.deepcopy(self.acks)
        first = acknowledgements["acknowledgements"][0]
        first["acknowledgement"]["affected_artifacts"].pop()
        first["acknowledgement_sha256"] = sha256_document(first["acknowledgement"])
        with self.assertRaisesRegex(KernelError, "E-ACK-AFFECTED"):
            self.audit(acknowledgements=acknowledgements)

    def test_chain_predecessor_mismatch_is_rejected(self) -> None:
        chain = copy.deepcopy(self.chain)
        chain["links"][1]["previous_event_sha256"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-CHAIN-LINK"):
            self.audit(chain=chain)

    def test_phase17_provenance_mismatch_is_rejected(self) -> None:
        reconciliation = copy.deepcopy(self.reconciliation)
        reconciliation["source"]["phase17_merge_commit"] = "0" * 40
        with self.assertRaisesRegex(KernelError, "E-RECONCILIATION-PROVENANCE"):
            self.audit(reconciliation=reconciliation)

    def test_stale_reconciliation_reference_is_rejected(self) -> None:
        reconciliation = copy.deepcopy(self.reconciliation)
        reconciliation["records"][0]["affected_artifacts"][0][
            "current_revision"
        ] = 2
        with self.assertRaisesRegex(KernelError, "E-RECONCILIATION-STALE"):
            self.audit(reconciliation=reconciliation)


if __name__ == "__main__":
    unittest.main()
