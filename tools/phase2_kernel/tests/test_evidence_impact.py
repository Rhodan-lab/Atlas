from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.evidence_impact import (
    IMPACT_INDEX_CONTRACT,
    IMPACT_QUERY_CONTRACT,
    compile_evidence_impact_index,
    query_evidence_impact,
)
from tools.phase2_kernel.evidence_registry import REGISTRY_CONTRACT
from tools.phase2_kernel.evidence_review import load_review_index
from tools.phase2_kernel.kernel import KernelError, load_json, render_json
from tools.phase2_kernel.repository import KernelRepository

ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = ROOT / "content" / "fixtures" / "phase2_bridge" / "accepted-evidence-registry.v01.json"
COMMIT = "a" * 40
ENTITY_ID = "model:en:test-model"


class FakeRepository:
    def __init__(self, entities: list[dict[str, object]]) -> None:
        self.entities = {(str(item["id"]), int(item["revision"])): dict(item) for item in entities}

    def exact(self, entity_id: str, revision: int) -> dict[str, object]:
        if not any(key[0] == entity_id for key in self.entities):
            raise KernelError("E-ENTITY-MISSING", f"missing entity {entity_id}")
        try:
            return dict(self.entities[(entity_id, revision)])
        except KeyError as exc:
            raise KernelError("E-REVISION-MISSING", f"missing revision {entity_id}@{revision}") from exc

    def available_revisions(self, entity_id: str) -> list[int]:
        return sorted(revision for candidate, revision in self.entities if candidate == entity_id)

    def provenance_sources(self, entity_id: str, revision: int) -> list[dict[str, object]]:
        if (entity_id, revision) not in self.entities:
            return []
        return [{"key": "source:en:test-source@1", "path": "content/canonical/sources/test-source.md", "source_sha256": "3" * 64}]


def entity(revision: int = 1, *, status: str = "active") -> dict[str, object]:
    return {
        "id": ENTITY_ID,
        "revision": revision,
        "type": "model",
        "title": f"Test Entity {revision}",
        "path": "content/canonical/models/test-model.md",
        "source_sha256": str(revision) * 64,
        "body_sha256": str(revision + 1) * 64,
        "status": status,
        "staleness": "current",
    }


def reviews(items: list[dict[str, object]]) -> dict[str, dict[str, object]]:
    return {
        f"{item['id']}@{item['revision']}": {
            "source": "machine-readable-review",
            "record_id": f"ai-review:test:{item['revision']}",
            "record_path": "content/reviews/ai/test.json",
            "reviewed_at": "2026-08-01",
            "review_level": "ai-reviewed",
            "human_verified": False,
            "outcome": "pass",
        }
        for item in items
    }


def snapshot(route_id: str, revision: int = 1) -> dict[str, object]:
    return {
        "contract": "principia-atlas-reference-snapshot/0.1",
        "source_repository": "Rhodan-lab/principle-to-system",
        "source_commit": "b" * 40,
        "source_path": f"software/product_alpha/routes/{route_id}.json",
        "source_blob_sha": "c" * 40,
        "route_id": route_id,
        "live": False,
        "status_inheritance": "prohibited",
        "references": [{
            "entity_id": ENTITY_ID,
            "revision": revision,
            "declared_review_level": "ai-reviewed",
            "declared_human_verified": False,
            "purpose": f"Support {route_id}.",
        }],
    }


def workspace(root: Path, routes: dict[str, dict[str, object]]) -> dict[str, object]:
    entries = []
    for route_id, payload in routes.items():
        relative = f"content/fixtures/phase2_bridge/{route_id}.json"
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
        entries.append({
            "route_id": route_id,
            "snapshot_path": relative,
            "state": "repository-baseline",
            "registration_basis": "merged-test-baseline",
            "registration_commit": COMMIT,
        })
    return {"contract": REGISTRY_CONTRACT, "live": False, "status_inheritance": "prohibited", "entries": entries}


class EvidenceImpactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        runtime = compile_canonical(ROOT / "content" / "canonical")
        cls.repository = KernelRepository(runtime)
        cls.review_index = load_review_index(ROOT / "content" / "reviews" / "ai")

    def test_current_registry_compiles_clear_index(self) -> None:
        index = compile_evidence_impact_index(load_json(REGISTRY_PATH), self.repository, self.review_index, ROOT)
        self.assertEqual(index["contract"], IMPACT_INDEX_CONTRACT)
        self.assertEqual(index["route_count"], 1)
        self.assertEqual(index["entity_count"], 2)
        self.assertEqual(index["exact_reference_count"], 2)
        self.assertEqual(index["dependency_count"], 2)
        self.assertEqual(index["affected_route_count"], 0)
        self.assertEqual(index["decision"], "impact-index-clear")
        self.assertFalse(index["repository_mutation"])

    def test_current_registry_is_deterministic(self) -> None:
        payload = load_json(REGISTRY_PATH)
        first = render_json(compile_evidence_impact_index(payload, self.repository, self.review_index, ROOT))
        second = render_json(compile_evidence_impact_index(payload, self.repository, self.review_index, ROOT))
        self.assertEqual(first, second)

    def test_shared_exact_reference_consolidates_routes(self) -> None:
        items = [entity()]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = workspace(root, {"route-a": snapshot("route-a"), "route-b": snapshot("route-b")})
            index = compile_evidence_impact_index(registry, FakeRepository(items), reviews(items), root)
        exact = index["exact_references"][0]
        self.assertEqual(exact["route_ids"], ["route-a", "route-b"])
        self.assertEqual(exact["route_count"], 2)
        self.assertEqual(exact["dependency_count"], 2)

    def test_multiple_revisions_group_under_one_entity(self) -> None:
        items = [entity(1), entity(2)]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = workspace(root, {"route-a": snapshot("route-a", 1), "route-b": snapshot("route-b", 2)})
            index = compile_evidence_impact_index(registry, FakeRepository(items), reviews(items), root)
        grouped = index["entities"][0]
        self.assertEqual(grouped["revisions"], [1, 2])
        self.assertEqual(grouped["exact_reference_count"], 2)
        self.assertEqual(grouped["route_ids"], ["route-a", "route-b"])

    def test_superseded_reference_requires_revalidation(self) -> None:
        items = [entity(1), entity(2)]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = workspace(root, {"route-a": snapshot("route-a", 1)})
            index = compile_evidence_impact_index(registry, FakeRepository(items), reviews(items), root)
        self.assertEqual(index["decision"], "impact-index-revalidation-required")
        self.assertEqual(index["affected_route_ids"], ["route-a"])
        self.assertTrue(index["exact_references"][0]["superseded"])

    def test_retracted_reference_blocks_route(self) -> None:
        items = [entity(status="retracted")]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = workspace(root, {"route-a": snapshot("route-a")})
            index = compile_evidence_impact_index(registry, FakeRepository(items), reviews(items), root)
        self.assertEqual(index["decision"], "impact-index-blocked")
        self.assertEqual(index["blocked_exact_reference_count"], 1)
        self.assertEqual(index["affected_route_ids"], ["route-a"])

    def test_exact_query_returns_route_dependency(self) -> None:
        items = [entity()]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = workspace(root, {"route-a": snapshot("route-a")})
            index = compile_evidence_impact_index(registry, FakeRepository(items), reviews(items), root)
        result = query_evidence_impact(index, ENTITY_ID, 1)
        self.assertEqual(result["contract"], IMPACT_QUERY_CONTRACT)
        self.assertEqual(result["route_ids"], ["route-a"])
        self.assertEqual(result["impact_state"], "stable")

    def test_entity_query_returns_all_revisions(self) -> None:
        items = [entity(1), entity(2)]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = workspace(root, {"route-a": snapshot("route-a", 1), "route-b": snapshot("route-b", 2)})
            index = compile_evidence_impact_index(registry, FakeRepository(items), reviews(items), root)
        result = query_evidence_impact(index, ENTITY_ID)
        self.assertEqual(result["match_count"], 2)
        self.assertEqual(result["route_ids"], ["route-a", "route-b"])
        self.assertEqual(result["impact_state"], "revalidation-required")

    def test_query_rejects_unreferenced_entity(self) -> None:
        with self.assertRaisesRegex(KernelError, "no accepted Principia route depends"):
            query_evidence_impact({"contract": IMPACT_INDEX_CONTRACT, "exact_references": []}, ENTITY_ID)

    def test_registry_route_must_match_snapshot(self) -> None:
        items = [entity()]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            registry = workspace(root, {"route-a": snapshot("other-route")})
            with self.assertRaisesRegex(KernelError, "does not match snapshot route"):
                compile_evidence_impact_index(registry, FakeRepository(items), reviews(items), root)


if __name__ == "__main__":
    unittest.main()
