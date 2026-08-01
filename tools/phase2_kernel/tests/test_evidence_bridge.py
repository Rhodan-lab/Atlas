from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.evidence_bridge import (
    EVIDENCE_MANIFEST_CONTRACT,
    REFERENCE_SNAPSHOT_CONTRACT,
    build_evidence_manifest,
    validate_reference_snapshot,
)
from tools.phase2_kernel.evidence_review import (
    build_review_aware_manifest,
    load_review_index,
)
from tools.phase2_kernel.kernel import KernelError, load_json, render_json
from tools.phase2_kernel.repository import KernelRepository

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
REVIEWS = ROOT / "content" / "reviews" / "ai"
REVIEW_RECORD = REVIEWS / "feedback-delayed-comprehensive.json"
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
        cls.review_index = load_review_index(REVIEWS)
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

    def test_review_index_binds_exact_claim_review_record(self) -> None:
        review = self.review_index[CLAIM_KEY]
        self.assertEqual(
            review["record_id"], "ai-review:feedback-delayed-comprehensive"
        )
        self.assertEqual(review["review_level"], "ai-reviewed")
        self.assertFalse(review["human_verified"])
        self.assertEqual(review["outcome"], "pass")

    def test_manifest_resolves_exact_revisions_and_review_authority(self) -> None:
        manifest = build_review_aware_manifest(
            self.snapshot, self.repository, self.review_index
        )
        self.assertEqual(manifest["contract"], EVIDENCE_MANIFEST_CONTRACT)
        self.assertEqual(manifest["reference_count"], 2)
        self.assertEqual(manifest["resolved_count"], 2)
        self.assertEqual(manifest["review_record_count"], 2)
        self.assertEqual(manifest["blocked_count"], 0)
        self.assertEqual(manifest["revalidate_count"], 0)
        self.assertEqual(
            manifest["decision"], "verified-offline-reference-manifest"
        )
        entries = {entry["key"]: entry for entry in manifest["entries"]}
        self.assertEqual(entries[MODEL_KEY]["review_comparison"], "match")
        self.assertEqual(entries[MODEL_KEY]["required_action"], "inspect")
        self.assertEqual(entries[CLAIM_KEY]["review_comparison"], "match")
        self.assertEqual(entries[CLAIM_KEY]["required_action"], "inspect")
        self.assertEqual(
            entries[CLAIM_KEY]["review_authority"]["source"],
            "machine-readable-review",
        )
        self.assertEqual(
            entries[CLAIM_KEY]["review_authority"]["record_id"],
            "ai-review:feedback-delayed-comprehensive",
        )
        self.assertFalse(manifest["automatic_status_change"])
        self.assertFalse(manifest["automatic_release_action"])
        self.assertFalse(manifest["repository_mutation"])

    def test_base_manifest_keeps_missing_inline_review_visible(self) -> None:
        manifest = build_evidence_manifest(self.snapshot, self.repository)
        entries = {entry["key"]: entry for entry in manifest["entries"]}
        self.assertEqual(
            entries[CLAIM_KEY]["review_comparison"],
            "declared-without-atlas-review-record",
        )
        self.assertEqual(
            manifest["decision"], "revalidate-principia-reference-metadata"
        )

    def test_manifest_is_byte_deterministic(self) -> None:
        first = render_json(
            build_review_aware_manifest(
                self.snapshot, self.repository, self.review_index
            )
        )
        second = render_json(
            build_review_aware_manifest(
                self.snapshot, self.repository, self.review_index
            )
        )
        self.assertEqual(first.encode("utf-8"), second.encode("utf-8"))

    def test_unavailable_revision_is_reported_without_silent_fallback(self) -> None:
        snapshot = copy.deepcopy(self.snapshot)
        snapshot["references"][0]["revision"] = 999
        manifest = build_review_aware_manifest(
            snapshot, self.repository, self.review_index
        )
        self.assertEqual(manifest["decision"], "block-principia-release")
        self.assertEqual(manifest["blocked_count"], 1)
        unavailable = next(
            entry for entry in manifest["entries"] if entry["revision"] == 999
        )
        self.assertEqual(unavailable["resolution"], "unavailable-revision")
        self.assertEqual(unavailable["required_action"], "block-release")

    def test_non_passing_review_outcome_requires_revalidation(self) -> None:
        review_index = copy.deepcopy(self.review_index)
        review_index[CLAIM_KEY]["outcome"] = "fail"
        manifest = build_review_aware_manifest(
            self.snapshot, self.repository, review_index
        )
        entries = {entry["key"]: entry for entry in manifest["entries"]}
        self.assertEqual(entries[CLAIM_KEY]["review_comparison"], "mismatch")
        self.assertEqual(entries[CLAIM_KEY]["required_action"], "revalidate")
        self.assertEqual(
            manifest["decision"], "revalidate-principia-reference-metadata"
        )

    def test_duplicate_review_authority_is_rejected(self) -> None:
        payload = load_json(REVIEW_RECORD)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "content" / "reviews" / "ai"
            root.mkdir(parents=True)
            rendered = json.dumps(payload, sort_keys=True)
            (root / "review-a.json").write_text(rendered, encoding="utf-8")
            (root / "review-b.json").write_text(rendered, encoding="utf-8")
            with self.assertRaisesRegex(
                KernelError, "E-EVIDENCE-REVIEW-DUPLICATE"
            ):
                load_review_index(root)

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
