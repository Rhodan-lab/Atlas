from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel import (
    KernelError,
    KernelRepository,
    compile_canonical,
    impact_report,
    import_principia_export,
    load_json,
    render_json,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURES = ROOT / "content" / "fixtures" / "phase2_bridge"


class Phase2KernelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)
        cls.repository = KernelRepository(cls.runtime)

    def test_compilation_is_deterministic_and_covers_three_slices(self) -> None:
        second = compile_canonical(CANONICAL)
        relative = compile_canonical(Path("content/canonical"))
        self.assertEqual(render_json(self.runtime), render_json(second))
        self.assertEqual(render_json(self.runtime), render_json(relative))
        self.assertEqual(self.runtime["source_root"], "content/canonical")
        syntheses = [
            entity for entity in self.runtime["entities"] if entity["type"] == "synthesis"
        ]
        self.assertGreaterEqual(len(syntheses), 3)
        self.assertEqual(self.runtime["entity_count"], len(self.runtime["entities"]))

    def test_exact_revision_lookup(self) -> None:
        entity = self.repository.exact(
            "model:en:delayed-correction-recurrence", 2
        )
        self.assertEqual(entity["revision"], 2)
        with self.assertRaisesRegex(KernelError, "E-REVISION-MISSING"):
            self.repository.exact("model:en:delayed-correction-recurrence", 1)

    def test_relation_and_provenance_queries(self) -> None:
        evidence = self.repository.relation_targets(
            "evidence:en:delayed-feedback-periodic-sequence", 2, "supports"
        )
        self.assertEqual(
            [item["entity"]["id"] for item in evidence],
            ["claim:en:stated-delayed-recurrence-oscillates"],
        )
        sources = self.repository.provenance_sources(
            "synthesis:en:delayed-feedback-and-oscillation", 2
        )
        source_ids = {source["id"] for source in sources}
        self.assertIn("src:synthetic-feedback-run-delay-one-gain-one", source_ids)
        self.assertNotIn("src:astrom-murray-2008-feedback-systems", source_ids)

    def test_valid_principia_candidate_import_is_deterministic(self) -> None:
        payload = load_json(FIXTURES / "principia-feedback-valid.json")
        first = import_principia_export(payload, self.repository)
        second = import_principia_export(copy.deepcopy(payload), self.repository)
        self.assertEqual(render_json(first), render_json(second))
        self.assertFalse(first["live"])
        self.assertEqual(first["status_inheritance"], "prohibited")
        self.assertEqual(len(first["dependencies"]), 4)

    def test_legacy_id_only_export_is_rejected(self) -> None:
        payload = load_json(
            FIXTURES / "principia-feedback-legacy-id-only.json"
        )
        with self.assertRaisesRegex(KernelError, "E-BRIDGE-LEGACY-EXPORT"):
            import_principia_export(payload, self.repository)

    def test_stale_revision_is_rejected(self) -> None:
        payload = load_json(
            FIXTURES / "principia-feedback-stale-revision.json"
        )
        with self.assertRaisesRegex(KernelError, "E-BRIDGE-REVISION-MISSING"):
            import_principia_export(payload, self.repository)

    def test_status_inheritance_is_rejected(self) -> None:
        payload = load_json(
            FIXTURES / "principia-feedback-status-inheritance.json"
        )
        with self.assertRaisesRegex(KernelError, "E-BRIDGE-STATUS-INHERITANCE"):
            import_principia_export(payload, self.repository)

    def test_impact_report_includes_principia_action_without_status_mutation(self) -> None:
        imported = import_principia_export(
            load_json(FIXTURES / "principia-feedback-valid.json"),
            self.repository,
        )
        report = impact_report(
            self.repository,
            "model:en:delayed-correction-recurrence",
            2,
            [imported],
        )
        self.assertEqual(
            report["external_dependents"][0]["id"], imported["id"]
        )
        self.assertEqual(
            report["external_dependents"][0]["action"], "inspect"
        )
        self.assertFalse(report["automatic_status_change"])


if __name__ == "__main__":
    unittest.main()
