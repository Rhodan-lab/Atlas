from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.evidence_registry import (
    REGISTRY_CATALOG_CONTRACT,
    REGISTRY_CONTRACT,
    compile_evidence_registry,
    validate_evidence_registry,
)
from tools.phase2_kernel.evidence_review import load_review_index
from tools.phase2_kernel.kernel import KernelError, load_json, render_json
from tools.phase2_kernel.repository import KernelRepository

ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = (
    ROOT
    / "content"
    / "fixtures"
    / "phase2_bridge"
    / "accepted-evidence-registry.v01.json"
)
SNAPSHOT_PATH = (
    ROOT
    / "content"
    / "fixtures"
    / "phase2_bridge"
    / "product-alpha-refrigerator.references.v01.json"
)
COMMIT = "a" * 40


def registration(route_id: str, snapshot_path: str) -> dict[str, object]:
    return {
        "route_id": route_id,
        "snapshot_path": snapshot_path,
        "state": "repository-baseline",
        "registration_basis": "merged-test-change",
        "registration_commit": COMMIT,
    }


def registry(entries: list[dict[str, object]]) -> dict[str, object]:
    return {
        "contract": REGISTRY_CONTRACT,
        "live": False,
        "status_inheritance": "prohibited",
        "entries": entries,
    }


class EvidenceRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(ROOT / "content" / "canonical")
        cls.repository = KernelRepository(cls.runtime)
        cls.review_index = load_review_index(ROOT / "content" / "reviews" / "ai")

    def test_current_registry_compiles_verified_catalog(self) -> None:
        catalog = compile_evidence_registry(
            load_json(REGISTRY_PATH),
            self.repository,
            self.review_index,
            ROOT,
        )
        self.assertEqual(catalog["contract"], REGISTRY_CATALOG_CONTRACT)
        self.assertEqual(catalog["route_ids"], ["refrigerator"])
        self.assertEqual(catalog["route_count"], 1)
        self.assertEqual(catalog["verified_count"], 1)
        self.assertEqual(catalog["revalidation_required_count"], 0)
        self.assertEqual(catalog["blocked_count"], 0)
        self.assertEqual(catalog["decision"], "registry-verified")
        self.assertEqual(catalog["entries"][0]["reference_count"], 2)
        self.assertEqual(catalog["entries"][0]["resolved_count"], 2)
        self.assertEqual(catalog["entries"][0]["review_record_count"], 2)
        self.assertEqual(catalog["entries"][0]["health"], "verified")
        self.assertEqual(len(catalog["entries"][0]["snapshot_sha256"]), 64)
        self.assertEqual(len(catalog["entries"][0]["manifest_sha256"]), 64)
        self.assertFalse(catalog["automatic_snapshot_acceptance"])
        self.assertFalse(catalog["repository_mutation"])

    def test_current_registry_is_deterministic(self) -> None:
        payload = load_json(REGISTRY_PATH)
        first = render_json(
            compile_evidence_registry(
                payload,
                self.repository,
                self.review_index,
                ROOT,
            )
        )
        second = render_json(
            compile_evidence_registry(
                payload,
                self.repository,
                self.review_index,
                ROOT,
            )
        )
        self.assertEqual(first, second)

    def test_duplicate_route_is_rejected(self) -> None:
        relative = "content/fixtures/phase2_bridge/a.json"
        payload = registry(
            [
                registration("refrigerator", relative),
                registration(
                    "refrigerator",
                    "content/fixtures/phase2_bridge/b.json",
                ),
            ]
        )
        with self.assertRaisesRegex(KernelError, "duplicate active baseline"):
            validate_evidence_registry(payload)

    def test_duplicate_snapshot_path_is_rejected(self) -> None:
        relative = "content/fixtures/phase2_bridge/a.json"
        payload = registry(
            [
                registration("a-route", relative),
                registration("b-route", relative),
            ]
        )
        with self.assertRaisesRegex(KernelError, "duplicate snapshot_path"):
            validate_evidence_registry(payload)

    def test_path_escape_is_rejected(self) -> None:
        payload = registry(
            [
                registration(
                    "refrigerator",
                    "content/fixtures/phase2_bridge/../outside.json",
                )
            ]
        )
        with self.assertRaisesRegex(KernelError, "safe phase2_bridge"):
            validate_evidence_registry(payload)

    def test_missing_snapshot_is_rejected(self) -> None:
        payload = registry(
            [
                registration(
                    "refrigerator",
                    "content/fixtures/phase2_bridge/missing.json",
                )
            ]
        )
        with self.assertRaisesRegex(KernelError, "snapshot is unavailable"):
            compile_evidence_registry(
                payload,
                self.repository,
                self.review_index,
                ROOT,
            )

    def test_registry_route_must_match_snapshot_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = "content/fixtures/phase2_bridge/snapshot.json"
            path = root / relative
            path.parent.mkdir(parents=True)
            snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
            path.write_text(json.dumps(snapshot), encoding="utf-8")
            payload = registry([registration("other-route", relative)])
            with self.assertRaisesRegex(
                KernelError,
                "does not match snapshot route",
            ):
                compile_evidence_registry(
                    payload,
                    self.repository,
                    self.review_index,
                    root,
                )

    def test_revalidation_health_is_aggregated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = "content/fixtures/phase2_bridge/refrigerator.json"
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes(SNAPSHOT_PATH.read_bytes())
            payload = registry([registration("refrigerator", relative)])
            manifest = {
                "source": {"route_id": "refrigerator"},
                "reference_count": 2,
                "resolved_count": 2,
                "review_record_count": 1,
                "revalidate_count": 1,
                "blocked_count": 0,
                "decision": "revalidate-principia-reference-metadata",
            }
            with mock.patch(
                "tools.phase2_kernel.evidence_registry.build_review_aware_manifest",
                return_value=manifest,
            ):
                catalog = compile_evidence_registry(
                    payload,
                    self.repository,
                    self.review_index,
                    root,
                )
            self.assertEqual(
                catalog["decision"],
                "registry-revalidation-required",
            )
            self.assertEqual(catalog["verified_count"], 0)
            self.assertEqual(catalog["revalidation_required_count"], 1)
            self.assertEqual(
                catalog["entries"][0]["health"],
                "revalidation-required",
            )

    def test_blocked_health_has_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            relative = "content/fixtures/phase2_bridge/refrigerator.json"
            path = root / relative
            path.parent.mkdir(parents=True)
            path.write_bytes(SNAPSHOT_PATH.read_bytes())
            payload = registry([registration("refrigerator", relative)])
            manifest = {
                "source": {"route_id": "refrigerator"},
                "reference_count": 2,
                "resolved_count": 1,
                "review_record_count": 1,
                "revalidate_count": 0,
                "blocked_count": 1,
                "decision": "block-principia-release",
            }
            with mock.patch(
                "tools.phase2_kernel.evidence_registry.build_review_aware_manifest",
                return_value=manifest,
            ):
                catalog = compile_evidence_registry(
                    payload,
                    self.repository,
                    self.review_index,
                    root,
                )
            self.assertEqual(catalog["decision"], "registry-blocked")
            self.assertEqual(catalog["blocked_count"], 1)
            self.assertEqual(catalog["entries"][0]["health"], "blocked")

    def test_unknown_registry_field_is_rejected(self) -> None:
        payload = registry(
            [
                registration(
                    "refrigerator",
                    "content/fixtures/phase2_bridge/a.json",
                )
            ]
        )
        payload["automatic_accept"] = True
        with self.assertRaisesRegex(
            KernelError,
            "unsupported registry fields",
        ):
            validate_evidence_registry(payload)


if __name__ == "__main__":
    unittest.main()
