from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.evidence_promotion import (
    EVIDENCE_PROMOTION_CONTRACT,
    build_evidence_promotion_packet,
)
from tools.phase2_kernel.evidence_review import load_review_index
from tools.phase2_kernel.kernel import KernelError, load_json
from tools.phase2_kernel.repository import KernelRepository

MODEL_ID = "model:en:delayed-correction-recurrence"
CLAIM_ID = "claim:en:model-oscillation-does-not-prove-real-system"
BASELINE_PATH = "content/fixtures/phase2_bridge/baseline.references.json"
CANDIDATE_PATH = "content/fixtures/phase2_bridge/candidate.references.json"


class FakeRepository:
    def __init__(self) -> None:
        self.entities = {
            (MODEL_ID, 2): {
                "id": MODEL_ID,
                "revision": 2,
                "type": "model",
                "title": "Delayed correction recurrence",
                "path": "content/canonical/models/delayed-correction-recurrence.v02.md",
                "source_sha256": "1" * 64,
                "body_sha256": "2" * 64,
                "status": "active",
                "staleness": "current",
            },
            (CLAIM_ID, 1): {
                "id": CLAIM_ID,
                "revision": 1,
                "type": "claim",
                "title": "Model oscillation does not prove real-system oscillation",
                "path": "content/canonical/claims/model-oscillation-does-not-prove-real-system.v01.md",
                "source_sha256": "3" * 64,
                "body_sha256": "4" * 64,
                "status": "active",
                "staleness": "current",
            },
        }

    def exact(self, entity_id: str, revision: int):
        try:
            return copy.deepcopy(self.entities[(entity_id, revision)])
        except KeyError as exc:
            raise KernelError(
                "E-ENTITY-MISSING",
                f"missing entity {entity_id}@{revision}",
            ) from exc

    def available_revisions(self, entity_id: str):
        return sorted(
            revision
            for candidate_id, revision in self.entities
            if candidate_id == entity_id
        )

    def provenance_sources(self, entity_id: str, revision: int):
        if (entity_id, revision) not in self.entities:
            return []
        return [
            {
                "key": "source:en:test-authority",
                "path": "content/canonical/sources/test-authority.v01.md",
                "source_sha256": "5" * 64,
            }
        ]


def review_index() -> dict[str, dict[str, object]]:
    return {
        f"{MODEL_ID}@2": {
            "source": "machine-readable-review",
            "record_id": "ai-review:test-model",
            "record_path": "content/reviews/ai/test-model.json",
            "reviewed_at": "2026-08-01",
            "review_level": "ai-reviewed",
            "human_verified": False,
            "outcome": "pass",
        },
        f"{CLAIM_ID}@1": {
            "source": "machine-readable-review",
            "record_id": "ai-review:test-claim",
            "record_path": "content/reviews/ai/test-claim.json",
            "reviewed_at": "2026-08-01",
            "review_level": "ai-reviewed",
            "human_verified": False,
            "outcome": "pass",
        },
    }


def reference(entity_id: str, revision: int, purpose: str) -> dict[str, object]:
    return {
        "entity_id": entity_id,
        "revision": revision,
        "declared_review_level": "ai-reviewed",
        "declared_human_verified": False,
        "purpose": purpose,
    }


def snapshot(
    *,
    commit: str = "a" * 40,
    blob: str = "b" * 40,
    route_id: str = "refrigerator",
    references: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "contract": "principia-atlas-reference-snapshot/0.1",
        "source_repository": "Rhodan-lab/principle-to-system",
        "source_commit": commit,
        "source_path": f"software/product_alpha/routes/{route_id}.json",
        "source_blob_sha": blob,
        "route_id": route_id,
        "live": False,
        "status_inheritance": "prohibited",
        "references": references
        or [reference(MODEL_ID, 2, "Supports the bounded feedback model.")],
    }


def registry() -> dict[str, object]:
    return {
        "contract": "atlas-principia-evidence-registry/0.1",
        "live": False,
        "status_inheritance": "prohibited",
        "entries": [
            {
                "route_id": "refrigerator",
                "snapshot_path": BASELINE_PATH,
                "state": "repository-baseline",
                "registration_basis": "merged-test-baseline",
                "registration_commit": "d" * 40,
            }
        ],
    }


def packet(candidate: dict[str, object], **overrides):
    baseline = snapshot()
    values = {
        "baseline_snapshot_path": BASELINE_PATH,
        "candidate_snapshot_path": CANDIDATE_PATH,
        "submission_basis": "candidate-review-test",
    }
    values.update(overrides)
    return build_evidence_promotion_packet(
        registry(),
        baseline,
        candidate,
        FakeRepository(),
        review_index(),
        **values,
    )


class EvidencePromotionTests(unittest.TestCase):
    def test_redundant_candidate_is_no_change(self) -> None:
        result = packet(snapshot())
        self.assertEqual(result["contract"], EVIDENCE_PROMOTION_CONTRACT)
        self.assertEqual(result["decision"], "candidate-redundant")
        self.assertEqual(result["gate_state"], "no-change")
        self.assertFalse(result["registry_update_eligible_after_review"])
        self.assertIsNone(result["proposed_registry_replacement"])

    def test_source_identity_change_is_reviewable(self) -> None:
        result = packet(snapshot(commit="c" * 40, blob="e" * 40))
        self.assertEqual(result["decision"], "ready-for-source-refresh-review")
        self.assertEqual(result["gate_state"], "reviewable")
        self.assertEqual(result["required_reviews"], ["source-identity-review"])
        self.assertTrue(result["registry_update_eligible_after_review"])
        self.assertIsNone(
            result["proposed_registry_replacement"]["registration_commit"]
        )

    def test_metadata_change_requires_metadata_review(self) -> None:
        candidate = snapshot()
        candidate["references"][0]["purpose"] = "A changed explanatory purpose."
        result = packet(candidate)
        self.assertEqual(
            result["decision"], "requires-reference-metadata-review"
        )
        self.assertEqual(result["required_reviews"], ["reference-metadata-review"])

    def test_reference_addition_requires_reference_set_review(self) -> None:
        candidate = snapshot(
            references=[
                reference(MODEL_ID, 2, "Supports the bounded feedback model."),
                reference(CLAIM_ID, 1, "Preserves the model-to-world boundary."),
            ]
        )
        result = packet(candidate)
        self.assertEqual(result["decision"], "requires-reference-set-review")
        self.assertEqual(result["candidate_evidence"]["resolved_count"], 2)
        self.assertEqual(result["candidate_evidence"]["review_record_count"], 2)

    def test_review_mismatch_holds_candidate(self) -> None:
        candidate = snapshot()
        candidate["references"][0]["declared_review_level"] = "human-reviewed"
        result = packet(candidate)
        self.assertEqual(result["decision"], "hold-for-evidence-revalidation")
        self.assertEqual(result["gate_state"], "hold")
        self.assertFalse(result["registry_update_eligible_after_review"])

    def test_missing_reference_blocks_candidate(self) -> None:
        candidate = snapshot(
            references=[
                reference(
                    "claim:en:unavailable-promotion-reference",
                    1,
                    "Exercises fail-closed resolution.",
                )
            ]
        )
        result = packet(candidate)
        self.assertEqual(result["decision"], "reject-unresolved-candidate")
        self.assertEqual(result["gate_state"], "blocked")
        self.assertEqual(result["candidate_evidence"]["blocked_count"], 1)

    def test_unregistered_route_is_rejected(self) -> None:
        with self.assertRaisesRegex(KernelError, "exactly one baseline"):
            packet(snapshot(route_id="solar-battery-microgrid"))

    def test_unsafe_candidate_path_is_rejected(self) -> None:
        with self.assertRaisesRegex(KernelError, "repository-relative"):
            packet(snapshot(), candidate_snapshot_path="../candidate.json")

    def test_output_is_deterministic(self) -> None:
        first = packet(snapshot(commit="c" * 40, blob="e" * 40))
        second = packet(snapshot(commit="c" * 40, blob="e" * 40))
        self.assertEqual(first, second)
        self.assertTrue(
            all(len(value) == 64 for value in first["hashes"].values())
        )
        self.assertFalse(first["automatic_snapshot_acceptance"])
        self.assertFalse(first["repository_mutation"])

    def test_current_repository_baseline_builds_as_redundant_control(self) -> None:
        root = Path(__file__).resolve().parents[3]
        registry_path = root / "content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json"
        snapshot_path = root / "content/fixtures/phase2_bridge/product-alpha-refrigerator.references.v01.json"
        runtime = compile_canonical(root / "content/canonical")
        result = build_evidence_promotion_packet(
            load_json(registry_path),
            load_json(snapshot_path),
            load_json(snapshot_path),
            KernelRepository(runtime),
            load_review_index(root / "content/reviews/ai"),
            baseline_snapshot_path=snapshot_path.relative_to(root).as_posix(),
            candidate_snapshot_path=snapshot_path.relative_to(root).as_posix(),
            submission_basis="zero-drift-regression-control",
            registry_bytes=registry_path.read_bytes(),
            baseline_snapshot_bytes=snapshot_path.read_bytes(),
            candidate_snapshot_bytes=snapshot_path.read_bytes(),
        )
        self.assertEqual(result["decision"], "candidate-redundant")
        self.assertEqual(result["candidate_evidence"]["reference_count"], 2)
        self.assertEqual(result["candidate_evidence"]["review_record_count"], 2)
        self.assertEqual(result["candidate_evidence"]["blocked_count"], 0)


if __name__ == "__main__":
    unittest.main()
