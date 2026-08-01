from __future__ import annotations

import copy
import hashlib
import unittest
from collections import defaultdict
from pathlib import Path

from tools.phase2_kernel.compiler import compile_canonical
from tools.phase2_kernel.evidence_impact import (
    IMPACT_INDEX_CONTRACT,
    compile_evidence_impact_index,
)
from tools.phase2_kernel.evidence_preflight import (
    PREFLIGHT_CONTRACT,
    analyze_evidence_runtime_preflight,
)
from tools.phase2_kernel.evidence_review import load_review_index
from tools.phase2_kernel.kernel import (
    CONTENT_CONTRACT,
    RUNTIME_CONTRACT,
    KernelError,
    load_json,
    render_json,
)
from tools.phase2_kernel.repository import KernelRepository

ROOT = Path(__file__).resolve().parents[3]
REGISTRY_PATH = (
    ROOT
    / "content"
    / "fixtures"
    / "phase2_bridge"
    / "accepted-evidence-registry.v01.json"
)
ENTITY_ID = "model:en:preflight-test"
KEY = f"{ENTITY_ID}@1"


def entity(
    revision: int = 1,
    *,
    entity_id: str = ENTITY_ID,
    path: str | None = None,
    source_sha256: str | None = None,
    body_sha256: str | None = None,
    status: str = "draft",
    staleness: str = "current",
) -> dict[str, object]:
    key = f"{entity_id}@{revision}"
    return {
        "id": entity_id,
        "type": "model",
        "key": key,
        "revision": revision,
        "title": f"Preflight test {revision}",
        "path": path or f"content/canonical/test/preflight-{revision}.md",
        "source_sha256": source_sha256 or (str(revision) * 64)[-64:],
        "body_sha256": body_sha256 or (hex(revision)[2:] * 64)[-64:],
        "status": status,
        "staleness": staleness,
        "metadata": {
            "contract": CONTENT_CONTRACT,
            "id": entity_id,
            "type": "model",
            "revision": revision,
            "status": status,
            "staleness": staleness,
        },
        "references": [],
        "relations": [],
    }


def runtime(entities: list[dict[str, object]]) -> dict[str, object]:
    ordered = sorted(
        copy.deepcopy(entities),
        key=lambda item: (
            str(item["id"]),
            int(item["revision"]),
            str(item["path"]),
        ),
    )
    revisions: dict[str, list[int]] = defaultdict(list)
    reverse: dict[str, list[str]] = {}
    digest = hashlib.sha256()
    for item in ordered:
        revisions[str(item["id"])].append(int(item["revision"]))
        reverse[str(item["key"])] = []
        digest.update(
            f"{item['path']}\0{item['source_sha256']}\n".encode("utf-8")
        )
    return {
        "contract": RUNTIME_CONTRACT,
        "source_contract": CONTENT_CONTRACT,
        "source_root": "canonical/test",
        "source_digest": digest.hexdigest(),
        "entity_count": len(ordered),
        "entities": ordered,
        "revisions_by_id": {
            entity_id: sorted(values)
            for entity_id, values in sorted(revisions.items())
        },
        "reverse_dependencies": {
            key: value for key, value in sorted(reverse.items())
        },
    }


def impact_index() -> dict[str, object]:
    return {
        "contract": IMPACT_INDEX_CONTRACT,
        "routes": [
            {
                "route_id": "refrigerator",
                "impact_state": "stable",
            }
        ],
        "exact_references": [
            {
                "key": KEY,
                "entity_id": ENTITY_ID,
                "revision": 1,
                "route_ids": ["refrigerator"],
                "impact_state": "stable",
            }
        ],
    }


class EvidencePreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = runtime([entity()])
        self.index = impact_index()

    def preflight(self, candidate: dict[str, object]) -> dict[str, object]:
        return analyze_evidence_runtime_preflight(
            self.index,
            self.baseline,
            candidate,
        )

    def test_unchanged_runtime_is_clear(self) -> None:
        report = self.preflight(copy.deepcopy(self.baseline))
        self.assertEqual(report["contract"], PREFLIGHT_CONTRACT)
        self.assertEqual(report["decision"], "preflight-clear")
        self.assertFalse(report["runtime_changed"])
        self.assertEqual(report["changed_accepted_exact_reference_count"], 0)
        self.assertEqual(report["newly_affected_route_ids"], [])
        self.assertFalse(report["canonical_mutation"])
        self.assertFalse(report["repository_mutation"])

    def test_unrelated_entity_addition_is_clear(self) -> None:
        candidate = runtime(
            [
                entity(),
                entity(
                    entity_id="model:en:unrelated-preflight",
                    path="content/canonical/test/unrelated.md",
                    source_sha256="a" * 64,
                    body_sha256="b" * 64,
                ),
            ]
        )
        report = self.preflight(candidate)
        self.assertTrue(report["runtime_changed"])
        self.assertEqual(report["decision"], "preflight-clear")
        self.assertEqual(report["changed_accepted_exact_reference_count"], 0)

    def test_new_higher_revision_requires_revalidation(self) -> None:
        candidate = runtime(
            [
                entity(),
                entity(
                    revision=2,
                    source_sha256="c" * 64,
                    body_sha256="d" * 64,
                ),
            ]
        )
        report = self.preflight(candidate)
        self.assertEqual(report["decision"], "preflight-revalidation-required")
        self.assertEqual(report["superseding_revision_count"], 1)
        self.assertEqual(report["newly_affected_route_ids"], ["refrigerator"])
        exact = report["exact_references"][0]
        self.assertEqual(exact["new_higher_revisions"], [2])
        self.assertIn("superseding-revision-added", exact["finding_codes"])

    def test_same_revision_source_change_is_blocked(self) -> None:
        candidate = runtime([entity(source_sha256="e" * 64)])
        report = self.preflight(candidate)
        self.assertEqual(report["decision"], "preflight-blocked")
        self.assertEqual(report["immutable_violation_count"], 1)
        self.assertEqual(report["newly_blocked_route_ids"], ["refrigerator"])
        self.assertIn(
            "source_sha256",
            report["exact_references"][0]["immutable_changed_fields"],
        )

    def test_same_revision_path_move_is_blocked(self) -> None:
        candidate = runtime(
            [entity(path="content/canonical/test/preflight-moved.md")]
        )
        report = self.preflight(candidate)
        self.assertEqual(report["decision"], "preflight-blocked")
        self.assertIn(
            "path",
            report["exact_references"][0]["immutable_changed_fields"],
        )

    def test_exact_revision_removal_is_blocked(self) -> None:
        candidate = runtime(
            [
                entity(
                    entity_id="model:en:replacement-only",
                    path="content/canonical/test/replacement.md",
                    source_sha256="f" * 64,
                    body_sha256="a" * 64,
                )
            ]
        )
        report = self.preflight(candidate)
        self.assertEqual(report["decision"], "preflight-blocked")
        self.assertEqual(report["removed_exact_reference_count"], 1)
        self.assertIn(
            "exact-revision-removed",
            report["exact_references"][0]["finding_codes"],
        )

    def test_deprecation_requires_revalidation(self) -> None:
        candidate = runtime([entity(status="deprecated")])
        report = self.preflight(candidate)
        self.assertEqual(report["decision"], "preflight-revalidation-required")
        self.assertEqual(report["lifecycle_change_count"], 1)
        self.assertIn(
            "lifecycle-deprecated",
            report["exact_references"][0]["finding_codes"],
        )

    def test_retraction_blocks_route(self) -> None:
        candidate = runtime([entity(status="retracted")])
        report = self.preflight(candidate)
        self.assertEqual(report["decision"], "preflight-blocked")
        self.assertIn(
            "lifecycle-retracted",
            report["exact_references"][0]["finding_codes"],
        )

    def test_confirmed_stale_requires_revalidation(self) -> None:
        candidate = runtime([entity(staleness="confirmed-stale")])
        report = self.preflight(candidate)
        self.assertEqual(report["decision"], "preflight-revalidation-required")
        self.assertIn(
            "staleness-confirmed-stale",
            report["exact_references"][0]["finding_codes"],
        )

    def test_invalid_candidate_runtime_fails_closed(self) -> None:
        candidate = copy.deepcopy(self.baseline)
        candidate["source_digest"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "source_digest"):
            self.preflight(candidate)

    def test_deterministic_and_source_inputs_unchanged(self) -> None:
        candidate = runtime(
            [
                entity(),
                entity(
                    revision=2,
                    source_sha256="c" * 64,
                    body_sha256="d" * 64,
                ),
            ]
        )
        baseline_before = render_json(copy.deepcopy(self.baseline))
        candidate_before = render_json(copy.deepcopy(candidate))
        index_before = render_json(copy.deepcopy(self.index))
        first = render_json(self.preflight(candidate))
        second = render_json(self.preflight(candidate))
        self.assertEqual(first, second)
        self.assertEqual(render_json(self.baseline), baseline_before)
        self.assertEqual(render_json(candidate), candidate_before)
        self.assertEqual(render_json(self.index), index_before)

    def test_current_repository_runtime_is_clear_against_itself(self) -> None:
        current = compile_canonical(ROOT / "content" / "canonical")
        repository = KernelRepository(current)
        index = compile_evidence_impact_index(
            load_json(REGISTRY_PATH),
            repository,
            load_review_index(ROOT / "content" / "reviews" / "ai"),
            ROOT,
        )
        report = analyze_evidence_runtime_preflight(index, current, current)
        self.assertEqual(report["decision"], "preflight-clear")
        self.assertEqual(report["changed_accepted_exact_reference_count"], 0)
        self.assertEqual(report["newly_affected_route_count"], 0)


if __name__ == "__main__":
    unittest.main()
