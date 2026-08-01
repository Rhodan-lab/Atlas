from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.evidence_bridge import (
    EVIDENCE_MANIFEST_CONTRACT,
    REFERENCE_SNAPSHOT_CONTRACT,
    build_evidence_manifest,
    validate_reference_snapshot,
)
from tools.phase2_kernel.kernel import KernelError, load_json, render_json
from tools.phase2_kernel.repository import KernelRepository

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
SNAPSHOT = (
    ROOT
    / "content"
    / "fixtures"
    / "phase2_bridge"
    / "product-alpha-refrigerator.references.v01.json"
)
MODEL_KEY = "model:en:delayed-correction-recurrence@2"
CLAIM_KEY = "claim:en:model-oscillation-does-not-prove-real-system@1"


class PrincipiaEvidenceBridgeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repository = KernelRepository(compile_canonical(CANONICAL))
        cls.snapshot = load_json(SNAPSHOT)

    def test_current_product_alpha_snapshot_is_pinned_and_non_live(self) -> None:
        snapshot = validate_reference_snapshot(self.snapshot)
        self.assertEqual(snapshot["contract"], REFERENCE_SNAPSHOT_CONTRACT)
        self.assertEqual(
            snapshot["source_commit"],
            "047867f5b0a803c59b918738c45c24909ea998be",
        )
        self.assertEqual(
            snapshot["source_blob_sha"],
            "ec6195eb217efacf4d4e5d675ba1cf74b03f9600",
        )
        self.assertEqual(snapshot["route_id"], "refrigerator")
        self.assertFalse(snapshot["live"])
        self.assertEqual(snapshot["status_inheritance"], "prohibited")

    def test_manifest_resolves_exact_revisions_and_surfaces_review_drift(self) -> None:
        manifest = build_evidence_manifest(self.snapshot, self.repository)
        self.assertEqual(manifest["contract"], EVIDENCE_MANIFEST_CONTRACT)
        self.assertEqual(manifest["reference_count"], 2)
        self.assertEqual(manifest["resolved_count"], 2)
        self.assertEqual(manifest["blocked_count"], 0)
        self.assertEqual(manifest["revalidate_count"], 1)
        self.assertEqual(
            manifest["decision"], "revalidate-principia-reference-metadata"
        )
        entries = {entry["key"]: entry for entry in manifest["entries"]}
        self.assertEqual(entries[MODEL_KEY]["review_comparison"], "match")
        self.assertEqual(entries[MODEL_KEY]["required_action"], "inspect")
        self.assertEqual(
            entries[CLAIM_KEY]["review_comparison"],
            "declared-without-atlas-review-record",
        )
        self.assertEqual(entries[CLAIM_KEY]["required_action"], "revalidate")
        self.assertFalse(manifest["automatic_status_change"])
        self.assertFalse(manifest["automatic_release_action"])
        self.assertFalse(manifest["repository_mutation"])

    def test_manifest_is_byte_deterministic(self) -> None:
        first = render_json(build_evidence_manifest(self.snapshot, self.repository))
        second = render_json(build_evidence_manifest(self.snapshot, self.repository))
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

    def test_unavailable_revision_is_reported_without_silent_fallback(self) -> None:
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["references"][0]["revision"] = 999
        manifest = build_evidence_manifest(snapshot, self.repository)
        self.assertEqual(manifest["decision"], "block-principia-release")
        self.assertEqual(manifest["blocked_count"], 1)
        unavailable = next(
            entry for entry in manifest["entries"] if entry["revision"] == 999
        )
        self.assertEqual(unavailable["resolution"], "unavailable-revision")
        self.assertEqual(unavailable["required_action"], "block-release")

    def test_duplicate_exact_reference_is_rejected(self) -> None:
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["references"].append(copy.deepcopy(snapshot["references"][0]))
        with self.assertRaisesRegex(KernelError, "E-EVIDENCE-DUPLICATE"):
            validate_reference_snapshot(snapshot)

    def test_live_or_status_inheriting_snapshots_are_rejected(self) -> None:
        live = copy.deepcopy(self.snapshot)
        live["live"] = True
        with self.assertRaisesRegex(KernelError, "E-EVIDENCE-LIVE-FROZEN"):
            validate_reference_snapshot(live)
        inheriting = copy.deepcopy(self.snapshot)
        inheriting["status_inheritance"] = "allowed"
        with self.assertRaisesRegex(KernelError, "E-EVIDENCE-STATUS-INHERITANCE"):
            validate_reference_snapshot(inheriting)


if __name__ == "__main__":
    unittest.main()
