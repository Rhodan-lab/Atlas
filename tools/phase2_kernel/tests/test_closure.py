from __future__ import annotations

import copy
import unittest
from pathlib import Path

from tools.phase2_kernel.closure import (
    CLOSURE_REPORT_CONTRACT,
    PORTABLE_SNAPSHOT_CONTRACT,
    RETRIEVAL_DECISION,
    PortableKernelRepository,
    export_portable_snapshot,
    run_phase2_closure,
    validate_portable_snapshot,
)
from tools.phase2_kernel import (
    KernelError,
    KernelRepository,
    compile_canonical,
    render_json,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"


class Phase2ClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.runtime = compile_canonical(CANONICAL)
        cls.snapshot = export_portable_snapshot(cls.runtime)

    def test_portable_snapshot_excludes_generated_indexes(self) -> None:
        self.assertEqual(self.snapshot["contract"], PORTABLE_SNAPSHOT_CONTRACT)
        self.assertNotIn("source_root", self.snapshot)
        self.assertNotIn("revisions_by_id", self.snapshot)
        self.assertNotIn("reverse_dependencies", self.snapshot)
        validation = validate_portable_snapshot(self.snapshot)
        self.assertEqual(validation["decision"], "valid")
        self.assertEqual(validation["entity_count"], self.runtime["entity_count"])
        self.assertFalse(validation["live"])
        self.assertFalse(validation["mutation"])

    def test_portable_repository_matches_representative_queries(self) -> None:
        standard = KernelRepository(self.runtime)
        portable = PortableKernelRepository(self.snapshot)
        exact = ("model:en:delayed-correction-recurrence", 2)
        self.assertEqual(standard.exact(*exact), portable.exact(*exact))
        synthesis = ("synthesis:en:delayed-feedback-and-oscillation", 2)
        self.assertEqual(
            standard.provenance_sources(*synthesis),
            portable.provenance_sources(*synthesis),
        )
        concept = ("concept:en:feedback", 1)
        self.assertEqual(
            standard.internal_impact(*concept), portable.internal_impact(*concept)
        )
        self.assertEqual(
            standard.relation_targets(*synthesis), portable.relation_targets(*synthesis)
        )

    def test_corrupted_portable_snapshot_is_rejected(self) -> None:
        corrupted = copy.deepcopy(self.snapshot)
        corrupted["source_digest"] = "0" * 64
        with self.assertRaisesRegex(KernelError, "E-RUNTIME-SOURCE-DIGEST"):
            validate_portable_snapshot(corrupted)

        indexed = copy.deepcopy(self.snapshot)
        indexed["reverse_dependencies"] = {}
        with self.assertRaisesRegex(KernelError, "E-PORTABLE-GENERATED-INDEX"):
            validate_portable_snapshot(indexed)

    def test_closure_report_is_deterministic_and_complete(self) -> None:
        first = run_phase2_closure(CANONICAL)
        second = run_phase2_closure(CANONICAL)
        self.assertEqual(render_json(first), render_json(second))
        self.assertEqual(first["contract"], CLOSURE_REPORT_CONTRACT)
        self.assertEqual(first["decision"], "phase2-complete-candidate")
        self.assertTrue(first["deterministic_compilation"])
        self.assertTrue(first["strict_runtime_admission"])
        self.assertEqual(
            first["query_equivalence"]["total_checks"],
            first["entity_count"] * 4,
        )
        self.assertEqual(first["query_equivalence"]["decision"], "equivalent")
        self.assertEqual(
            first["migration_and_rollback"]["decision"], "replaceable"
        )
        self.assertEqual(first["retrieval_entry"]["decision"], RETRIEVAL_DECISION)
        self.assertFalse(first["live"])
        self.assertFalse(first["repository_mutation"])

    def test_retrieval_entry_remains_bounded(self) -> None:
        report = run_phase2_closure(CANONICAL)
        blocked = set(report["retrieval_entry"]["blocked"])
        self.assertIn("live Principia synchronization", blocked)
        self.assertIn("production retrieval quality claims", blocked)
        self.assertIn("canonical content writes from retrieval output", blocked)
        self.assertIn("unversioned latest-entity lookup", blocked)


if __name__ == "__main__":
    unittest.main()
