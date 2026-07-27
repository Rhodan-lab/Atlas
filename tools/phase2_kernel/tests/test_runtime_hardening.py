from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import (
    RUNTIME_VALIDATION_CONTRACT,
    KernelError,
    KernelRepository,
    compile_canonical,
    load_json,
    render_json,
    validate_runtime,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURES = ROOT / "content" / "fixtures" / "phase2_runtime"
RUNTIME_CASES = FIXTURES / "runtime-failure-cases.json"
CANONICAL_CASES = FIXTURES / "canonical-failure-cases.json"


def _entity_with_references(runtime: dict, *, without_relations: bool = False) -> dict:
    return next(
        entity
        for entity in runtime["entities"]
        if entity["references"] and (not without_relations or not entity["relations"])
    )


def _entity_with_relations(runtime: dict) -> dict:
    return next(entity for entity in runtime["entities"] if entity["relations"])


def _mutate_runtime(runtime: dict, name: str) -> None:
    if name == "source-contract-mismatch":
        runtime["source_contract"] = "atlas-content/9.9"
    elif name == "source-digest-malformed":
        runtime["source_digest"] = "not-a-sha256"
    elif name == "source-digest-mismatch":
        runtime["source_digest"] = "0" * 64
    elif name == "entity-count-mismatch":
        runtime["entity_count"] += 1
    elif name == "duplicate-entity":
        runtime["entities"].append(copy.deepcopy(runtime["entities"][0]))
        runtime["entity_count"] += 1
    elif name == "entity-key-mismatch":
        runtime["entities"][0]["key"] = "concept:en:wrong-runtime-key@1"
    elif name == "entity-order-nondeterministic":
        runtime["entities"].reverse()
    elif name == "metadata-identity-mismatch":
        runtime["entities"][0]["metadata"]["revision"] = 999
    elif name == "reference-order-nondeterministic":
        entity = next(item for item in runtime["entities"] if len(item["references"]) >= 2)
        entity["references"].reverse()
    elif name == "reference-target-missing":
        entity = _entity_with_references(runtime, without_relations=True)
        entity["references"] = [
            {
                "id": "concept:en:missing-runtime-target",
                "revision": 1,
                "fields": ["fixture"],
            }
        ]
    elif name == "relation-target-missing":
        entity = _entity_with_relations(runtime)
        entity["relations"] = [
            {
                "type": "related-to",
                "target": "concept:en:missing-runtime-target",
                "target_revision": 1,
                "note": None,
            }
        ]
    elif name == "relation-reference-drift":
        entity = _entity_with_relations(runtime)
        relation = entity["relations"][0]
        relation_key = f"{relation['target']}@{relation['target_revision']}"
        entity["references"] = [
            reference
            for reference in entity["references"]
            if f"{reference['id']}@{reference['revision']}" != relation_key
        ]
    elif name == "revision-index-missing":
        entity_id = runtime["entities"][0]["id"]
        runtime["revisions_by_id"].pop(entity_id)
    elif name == "revision-index-orphan":
        runtime["revisions_by_id"]["concept:en:orphan-runtime-index"] = [1]
    elif name == "reverse-index-missing":
        runtime["reverse_dependencies"].pop(runtime["entities"][0]["key"])
    elif name == "reverse-dependent-missing":
        target_key = runtime["entities"][0]["key"]
        runtime["reverse_dependencies"][target_key] = [
            "concept:en:missing-runtime-dependent@1"
        ]
    elif name == "reverse-index-drift":
        target_key = next(
            key
            for key, dependents in runtime["reverse_dependencies"].items()
            if dependents
        )
        runtime["reverse_dependencies"][target_key] = []
    else:
        raise AssertionError(f"unimplemented runtime fixture mutation: {name}")


class RuntimeHardeningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)

    def test_valid_runtime_has_deterministic_admission_report(self) -> None:
        first = validate_runtime(self.runtime)
        second = validate_runtime(copy.deepcopy(self.runtime))
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(first["contract"], RUNTIME_VALIDATION_CONTRACT)
        self.assertEqual(first["decision"], "valid")
        self.assertEqual(first["entity_count"], self.runtime["entity_count"])
        self.assertGreater(first["reference_count"], 0)
        self.assertGreater(first["relation_count"], 0)
        self.assertFalse(first["mutation"])

    def test_public_repository_validates_before_indexing(self) -> None:
        repository = KernelRepository(self.runtime)
        self.assertEqual(repository.validation_report["decision"], "valid")
        malformed = copy.deepcopy(self.runtime)
        malformed["entity_count"] += 1
        with self.assertRaisesRegex(KernelError, "E-RUNTIME-ENTITY-COUNT"):
            KernelRepository(malformed)

    def test_all_serialized_runtime_failure_fixtures_are_rejected(self) -> None:
        manifest = load_json(RUNTIME_CASES)
        self.assertEqual(manifest["contract"], "atlas-runtime-failure-fixtures/0.1")
        self.assertFalse(manifest["live"])
        for case in manifest["cases"]:
            with self.subTest(case=case["name"]):
                runtime = copy.deepcopy(self.runtime)
                _mutate_runtime(runtime, case["name"])
                with self.assertRaisesRegex(KernelError, case["expected_error"]):
                    validate_runtime(runtime)

    def test_all_canonical_failure_fixtures_fail_before_runtime_emission(self) -> None:
        manifest = load_json(CANONICAL_CASES)
        self.assertEqual(manifest["contract"], "atlas-canonical-failure-fixtures/0.1")
        self.assertFalse(manifest["live"])
        for case in manifest["cases"]:
            with self.subTest(case=case["name"]):
                with self.assertRaisesRegex(KernelError, case["expected_error"]):
                    compile_canonical(ROOT / case["path"])


if __name__ == "__main__":
    unittest.main()
