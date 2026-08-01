from __future__ import annotations

import copy
import unittest
from unittest.mock import patch

from tools.phase2_kernel.evidence_drift import build_evidence_drift_report
from tools.phase2_kernel.kernel import KernelError


def snapshot() -> dict:
    return {
        "contract": "principia-atlas-reference-snapshot/0.1",
        "source_repository": "Rhodan-lab/principle-to-system",
        "source_commit": "a" * 40,
        "source_path": "software/product_alpha/routes/refrigerator.json",
        "source_blob_sha": "b" * 40,
        "route_id": "refrigerator",
        "live": False,
        "status_inheritance": "prohibited",
        "references": [
            {
                "entity_id": "claim:en:model-boundary",
                "revision": 1,
                "declared_review_level": "ai-reviewed",
                "declared_human_verified": False,
                "purpose": "Preserve the model-to-world boundary.",
            },
            {
                "entity_id": "model:en:delayed-control",
                "revision": 2,
                "declared_review_level": "ai-reviewed",
                "declared_human_verified": False,
                "purpose": "Explain bounded recurrence.",
            },
        ],
    }


class FakeRepository:
    def manifest(self, payload, review_index):
        entries = []
        blocked = 0
        revalidate = 0
        for ref in sorted(
            payload["references"],
            key=lambda item: (item["entity_id"], item["revision"]),
        ):
            key = f"{ref['entity_id']}@{ref['revision']}"
            exists = key in {
                "claim:en:model-boundary@1",
                "model:en:delayed-control@2",
                "concept:en:feedback@1",
            }
            if not exists:
                blocked += 1
                entries.append(
                    {
                        "key": key,
                        "resolution": "unavailable-revision",
                        "required_action": "block-release",
                        "review_comparison": "unresolved",
                        "atlas_review_level": None,
                        "atlas_human_verified": None,
                        "review_authority": None,
                    }
                )
                continue
            record = review_index.get(key)
            comparison = (
                "match"
                if record
                and ref.get("declared_review_level")
                == record["review_level"]
                and ref.get("declared_human_verified")
                == record["human_verified"]
                and record["outcome"] == "pass"
                else "mismatch"
            )
            action = "inspect" if comparison == "match" else "revalidate"
            revalidate += action == "revalidate"
            entries.append(
                {
                    "key": key,
                    "resolution": "current",
                    "required_action": action,
                    "review_comparison": comparison,
                    "atlas_review_level": record["review_level"] if record else None,
                    "atlas_human_verified": (
                        record["human_verified"] if record else None
                    ),
                    "review_authority": record,
                }
            )
        decision = (
            "block-principia-release"
            if blocked
            else (
                "revalidate-principia-reference-metadata"
                if revalidate
                else "verified-offline-reference-manifest"
            )
        )
        return {
            "entries": entries,
            "blocked_count": blocked,
            "revalidate_count": revalidate,
            "decision": decision,
        }


REVIEW_INDEX = {
    key: {
        "source": "machine-readable-review",
        "record_id": "ai-review:test",
        "review_level": "ai-reviewed",
        "human_verified": False,
        "outcome": "pass",
    }
    for key in (
        "claim:en:model-boundary@1",
        "model:en:delayed-control@2",
        "concept:en:feedback@1",
    )
}


class EvidenceDriftTests(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = FakeRepository()

    def report(self, candidate: dict, baseline: dict | None = None) -> dict:
        with patch(
            "tools.phase2_kernel.evidence_drift.build_review_aware_manifest",
            side_effect=lambda payload, repository, review_index: self.repository.manifest(
                payload, review_index
            ),
        ):
            return build_evidence_drift_report(
                baseline or snapshot(),
                candidate,
                self.repository,
                REVIEW_INDEX,
            )

    def test_identical_snapshot_is_zero_drift(self) -> None:
        report = self.report(snapshot())
        self.assertEqual(report["decision"], "no-refresh-needed")
        self.assertEqual(report["change_classes"], ["none"])
        self.assertEqual(
            report["baseline_manifest_sha256"],
            report["candidate_manifest_sha256"],
        )
        self.assertFalse(report["automatic_snapshot_acceptance"])
        self.assertFalse(report["repository_mutation"])

    def test_source_identity_only_requires_review_not_automatic_acceptance(self) -> None:
        candidate = snapshot()
        candidate["source_commit"] = "c" * 40
        candidate["source_blob_sha"] = "d" * 40
        report = self.report(candidate)
        self.assertEqual(
            report["decision"], "proceed-source-identity-refresh-review"
        )
        self.assertEqual(report["change_classes"], ["source-identity"])
        self.assertEqual(
            sorted(report["source_identity_changes"]),
            ["source_blob_sha", "source_commit"],
        )

    def test_purpose_change_is_metadata_change(self) -> None:
        candidate = snapshot()
        candidate["references"][0]["purpose"] = "A narrower explanation."
        report = self.report(candidate)
        self.assertEqual(
            report["decision"], "review-reference-metadata-change"
        )
        self.assertIn("purpose-changed", report["change_classes"])
        self.assertEqual(report["change_counts"]["purpose_changes"], 1)

    def test_review_mismatch_requires_revalidation(self) -> None:
        candidate = snapshot()
        candidate["references"][0]["declared_review_level"] = "human-reviewed"
        report = self.report(candidate)
        self.assertEqual(report["decision"], "hold-for-evidence-revalidation")
        self.assertEqual(
            report["candidate_manifest_decision"],
            "revalidate-principia-reference-metadata",
        )
        self.assertIn(
            "validation-outcome-changed", report["change_classes"]
        )

    def test_unavailable_revision_rejects_refresh(self) -> None:
        candidate = snapshot()
        candidate["references"][1]["revision"] = 3
        report = self.report(candidate)
        self.assertEqual(
            report["decision"], "reject-unresolved-reference-refresh"
        )
        self.assertEqual(report["change_counts"]["revision_changes"], 1)
        change = report["reference_changes"]["revision_changes"][0]
        self.assertEqual(change["from_revision"], 2)
        self.assertEqual(change["to_revision"], 3)

    def test_clean_added_reference_requires_reference_review(self) -> None:
        candidate = snapshot()
        candidate["references"].append(
            {
                "entity_id": "concept:en:feedback",
                "revision": 1,
                "declared_review_level": "ai-reviewed",
                "declared_human_verified": False,
                "purpose": "Provide conceptual context.",
            }
        )
        report = self.report(candidate)
        self.assertEqual(report["decision"], "review-reference-set-change")
        self.assertEqual(
            report["reference_changes"]["added"],
            ["concept:en:feedback@1"],
        )

    def test_route_scope_change_is_rejected(self) -> None:
        candidate = snapshot()
        candidate["route_id"] = "microgrid"
        with self.assertRaisesRegex(KernelError, "E-EVIDENCE-DRIFT-SCOPE"):
            self.report(candidate)

    def test_report_is_deterministic(self) -> None:
        candidate = snapshot()
        candidate["source_commit"] = "c" * 40
        first = self.report(copy.deepcopy(candidate))
        second = self.report(copy.deepcopy(candidate))
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
