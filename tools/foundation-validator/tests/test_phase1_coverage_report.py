from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_SPEC = importlib.util.spec_from_file_location(
    "phase1_review_gate", ROOT / "phase1_review_gate.py"
)
assert GATE_SPEC and GATE_SPEC.loader
gate = importlib.util.module_from_spec(GATE_SPEC)
sys.modules[GATE_SPEC.name] = gate
GATE_SPEC.loader.exec_module(gate)

COVERAGE_SPEC = importlib.util.spec_from_file_location(
    "phase1_coverage_report", ROOT / "phase1_coverage_report.py"
)
assert COVERAGE_SPEC and COVERAGE_SPEC.loader
coverage = importlib.util.module_from_spec(COVERAGE_SPEC)
sys.modules[COVERAGE_SPEC.name] = coverage
COVERAGE_SPEC.loader.exec_module(coverage)


def entity(
    *,
    entity_id: str = "claim:en:test",
    revision: int = 1,
    claim_kind: str = "methodological",
    role: str = "load-bearing",
    depends_on: list[str] | None = None,
) -> dict:
    return {
        "id": entity_id,
        "revision": revision,
        "type": "claim",
        "status": "draft",
        "staleness": "current",
        "claim_kind": claim_kind,
        "material_flags": [],
        "role": role,
        "depends_on": depends_on or [],
    }


def manifest(*, entities: list[dict] | None = None, requirement: str = "all") -> dict:
    return {
        "contract": "atlas-review-coverage/0.1",
        "id": "coverage:test:vertical-slice",
        "title": "Test vertical slice",
        "intended_status": "reviewed",
        "decision_at": "2026-07-26",
        "coverage_requirement": requirement,
        "entities": entities or [entity()],
        "external_dependents": [],
        "metadata": {"purpose": "test"},
    }


def review(
    review_type: str,
    *,
    entity_id: str = "claim:en:test",
    revision: int = 1,
    kind: str = "human",
    independence: str = "independent",
    accountable: bool = True,
    permits: bool = True,
    outcome: str = "pass",
) -> dict:
    return {
        "contract": "atlas-review/0.1",
        "id": f"review:{review_type}:coverage-r{revision}:2026-07-26",
        "entity": {"id": entity_id, "revision": revision},
        "review_type": review_type,
        "reviewer": {
            "display_name": "Qualified reviewer",
            "kind": kind,
            "independence": independence,
            "qualification": review_type,
            "accountable": accountable,
            "conflicts": [],
        },
        "completed_at": "2026-07-26",
        "review_horizon": None,
        "outcome": outcome,
        "findings": [],
        "summary": "Exact-revision review.",
        "permits_promotion": permits,
    }


def full_methodological_reviews(entity_id: str = "claim:en:test") -> list[dict]:
    return [
        review(
            "structural",
            entity_id=entity_id,
            kind="machine",
            independence="not-applicable",
            accountable=False,
            permits=False,
        ),
        review("editorial", entity_id=entity_id, independence="internal"),
        review("source", entity_id=entity_id, independence="internal"),
        review("domain", entity_id=entity_id),
        review("methodological", entity_id=entity_id),
    ]


class CoverageManifestTests(unittest.TestCase):
    def test_valid_manifest(self) -> None:
        self.assertEqual(coverage.validate_manifest(manifest()), [])

    def test_methodological_claim_requires_methodological_review(self) -> None:
        self.assertIn("methodological", gate.required_review_types(entity()))

    def test_invalid_external_target_is_rejected(self) -> None:
        payload = manifest()
        payload["external_dependents"] = [
            {
                "id": "principia:module:test",
                "kind": "principia-artifact",
                "repository": "Rhodan-lab/principle-to-system",
                "revision": 1,
                "role": "load-bearing",
                "depends_on": ["claim:en:missing"],
            }
        ]
        codes = {item.code for item in coverage.validate_manifest(payload)}
        self.assertIn("E-COVERAGE-EXTERNAL-TARGET", codes)

    def test_synthetic_translation_requires_revision_lineage(self) -> None:
        translated = entity(entity_id="claim:fr:test", claim_kind="model-derived")
        translated["translation_of"] = "claim:en:test"
        payload = manifest(entities=[translated])
        codes = {item.code for item in coverage.validate_manifest(payload)}
        self.assertIn("E-COVERAGE-TRANSLATION-SOURCE-REVISION", codes)
        self.assertIn("E-COVERAGE-SOURCE-CURRENT-REVISION", codes)


class CoverageEvaluationTests(unittest.TestCase):
    def test_complete_exact_revision_coverage(self) -> None:
        result, diagnostics = coverage.evaluate_coverage(
            manifest(), full_methodological_reviews()
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.decision, "coverage-complete")
        self.assertEqual(result.complete_entity_count, 1)

    def test_ai_methodology_review_cannot_satisfy_authority(self) -> None:
        records = full_methodological_reviews()
        records[-1] = review(
            "methodological",
            kind="ai-assisted",
            independence="internal",
            accountable=False,
            permits=False,
            outcome="changes-required",
        )
        result, diagnostics = coverage.evaluate_coverage(manifest(), records)
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.decision, "blocked")
        item = result.entity_results[0]
        self.assertIn("methodological", item.missing_review_types)
        self.assertTrue(
            any("lacks authority" in reason or "outcome" in reason for reason in item.blockers)
        )

    def test_wrong_revision_is_not_counted(self) -> None:
        records = full_methodological_reviews()
        records[-1] = review("methodological", revision=2)
        result, _ = coverage.evaluate_coverage(manifest(), records)
        self.assertEqual(result.decision, "blocked")
        self.assertIn("methodological", result.entity_results[0].missing_review_types)

    def test_load_bearing_policy_ignores_incomplete_context_entity(self) -> None:
        load = entity(entity_id="claim:en:load", role="load-bearing")
        context = entity(entity_id="claim:en:context", role="context")
        payload = manifest(entities=[load, context], requirement="load-bearing")
        result, diagnostics = coverage.evaluate_coverage(
            payload, full_methodological_reviews("claim:en:load")
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.decision, "coverage-complete")
        self.assertEqual(result.required_entity_count, 1)

    def test_dependency_impact_lists_internal_and_external_dependents(self) -> None:
        source = entity(entity_id="claim:en:source", role="load-bearing")
        dependent = entity(
            entity_id="claim:en:dependent",
            role="context",
            depends_on=["claim:en:source"],
        )
        payload = manifest(entities=[source, dependent], requirement="load-bearing")
        payload["external_dependents"] = [
            {
                "id": "principia:system-dossier:refrigerator",
                "kind": "principia-artifact",
                "repository": "Rhodan-lab/principle-to-system",
                "revision": 1,
                "role": "load-bearing",
                "depends_on": ["claim:en:source"],
            }
        ]
        result, diagnostics = coverage.evaluate_coverage(
            payload, full_methodological_reviews("claim:en:source")
        )
        self.assertEqual(diagnostics, [])
        item = next(x for x in result.entity_results if x.entity_id == "claim:en:source")
        self.assertEqual(item.internal_dependents, ("claim:en:dependent",))
        self.assertEqual(
            item.external_dependents,
            ("principia:system-dossier:refrigerator",),
        )

    def test_report_is_deterministic(self) -> None:
        payload = manifest()
        result, diagnostics = coverage.evaluate_coverage(
            payload, full_methodological_reviews()
        )
        first = coverage.render_report(payload, result, diagnostics)
        second = coverage.render_report(payload, result, diagnostics)
        self.assertEqual(first, second)
        self.assertIn("Decision: **coverage-complete**", first)

    def test_records_directory_load_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for index, item in enumerate(reversed(full_methodological_reviews())):
                (root / f"{index}.json").write_text(
                    json.dumps(item), encoding="utf-8"
                )
            records, diagnostics = coverage.load_review_records(root)
            self.assertEqual(diagnostics, [])
            self.assertEqual(len(records), 5)


if __name__ == "__main__":
    unittest.main()
