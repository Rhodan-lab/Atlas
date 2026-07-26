from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "phase1_review_gate.py"
SPEC = importlib.util.spec_from_file_location("phase1_review_gate", MODULE_PATH)
assert SPEC and SPEC.loader
gate = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = gate
SPEC.loader.exec_module(gate)


def review(
    review_type: str,
    *,
    entity_id: str = "claim:en:test",
    revision: int = 1,
    kind: str = "human",
    independence: str = "independent",
    accountable: bool = True,
    outcome: str = "pass",
    permits: bool = True,
    findings: list[dict] | None = None,
    horizon: str | None = None,
) -> dict:
    return {
        "contract": "atlas-review/0.1",
        "id": f"review:{review_type}:test-r{revision}:2026-07-26",
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
        "review_horizon": horizon,
        "outcome": outcome,
        "findings": findings or [],
        "summary": "Review completed for the exact revision.",
        "permits_promotion": permits,
    }


def promotion(
    *,
    entity: dict | None = None,
    reviews: list[dict] | None = None,
    requested_status: str = "reviewed",
    transition: dict | None = None,
    required: list[str] | None = None,
) -> dict:
    payload = {
        "contract": "atlas-promotion/0.1",
        "entity": entity
        or {
            "id": "claim:en:test",
            "revision": 1,
            "type": "claim",
            "status": "in-review",
            "staleness": "current",
            "claim_kind": "normative",
            "material_flags": [],
        },
        "requested_status": requested_status,
        "reviews": reviews or [],
        "decision_at": "2026-07-26",
        "accepted_by": {
            "display_name": "Maintainer",
            "kind": "human",
            "accountable": True,
        },
    }
    if transition is not None:
        payload["transition"] = transition
    if required is not None:
        payload["required_review_types"] = required
    return payload


class ReviewRecordTests(unittest.TestCase):
    def test_valid_human_review(self) -> None:
        self.assertEqual(gate.validate_review_record(review("domain")), [])

    def test_ai_cannot_be_accountable_or_permit_promotion(self) -> None:
        record = review(
            "domain",
            kind="ai-assisted",
            independence="internal",
            accountable=True,
            permits=True,
        )
        codes = {item.code for item in gate.validate_review_record(record)}
        self.assertIn("E-NONHUMAN-ACCOUNTABILITY", codes)
        self.assertIn("E-NONHUMAN-PROMOTION", codes)

    def test_machine_structural_review_is_valid_without_promotion(self) -> None:
        record = review(
            "structural",
            kind="machine",
            independence="not-applicable",
            accountable=False,
            permits=False,
        )
        self.assertEqual(gate.validate_review_record(record), [])

    def test_review_requires_exact_revision(self) -> None:
        codes = {item.code for item in gate.validate_review_record(review("domain", revision=0))}
        self.assertIn("E-REVIEW-ENTITY-REVISION", codes)

    def test_open_major_finding_blocks_passing_review(self) -> None:
        record = review(
            "domain",
            findings=[
                {
                    "id": "finding:test:scope",
                    "severity": "major",
                    "status": "open",
                    "summary": "Scope is too broad.",
                    "rationale": "The evidence covers one population.",
                }
            ],
        )
        codes = {item.code for item in gate.validate_review_record(record)}
        self.assertIn("E-REVIEW-PASS-OPEN-FINDING", codes)
        self.assertIn("E-REVIEW-PROMOTION-SERIOUS-FINDING", codes)

    def test_resolved_major_finding_requires_resolution_note(self) -> None:
        record = review(
            "domain",
            findings=[
                {
                    "id": "finding:test:scope",
                    "severity": "major",
                    "status": "resolved",
                    "summary": "Scope was broad.",
                    "rationale": "The original wording generalized too far.",
                }
            ],
        )
        codes = {item.code for item in gate.validate_review_record(record)}
        self.assertIn("E-FINDING-RESOLUTION-NOTE", codes)

    def test_review_horizon_and_unknown_field_validation(self) -> None:
        expired = review("legal-context", horizon="2026-07-25")
        self.assertIn(
            "E-REVIEW-HORIZON",
            {item.code for item in gate.validate_review_record(expired)},
        )
        unknown = review("domain")
        unknown["magic"] = True
        self.assertIn(
            "E-REVIEW-FIELD-UNKNOWN",
            {item.code for item in gate.validate_review_record(unknown)},
        )


class RequiredReviewTests(unittest.TestCase):
    def test_normative_claim_requirements(self) -> None:
        entity = {
            "id": "claim:en:test",
            "revision": 1,
            "type": "claim",
            "claim_kind": "normative",
        }
        self.assertEqual(
            gate.required_review_types(entity),
            {"structural", "editorial", "ethical"},
        )

    def test_causal_legal_claim_requirements(self) -> None:
        entity = {
            "id": "claim:en:test",
            "revision": 1,
            "type": "claim",
            "claim_kind": "causal",
            "material_flags": ["legal"],
        }
        self.assertEqual(
            gate.required_review_types(entity),
            {
                "structural",
                "editorial",
                "source",
                "domain",
                "methodological",
                "legal-context",
            },
        )

    def test_synthetic_translated_model_requires_translation_and_reproducibility(self) -> None:
        entity = {
            "id": "model:fr:test",
            "revision": 1,
            "type": "model",
            "translation_of": "model:en:test",
            "material_flags": ["executable"],
        }
        required = gate.required_review_types(entity)
        self.assertIn("translation", required)
        self.assertIn("reproducibility", required)

    def test_methodological_claim_requires_methodological_review(self) -> None:
        entity = {
            "id": "claim:en:test",
            "revision": 1,
            "type": "claim",
            "claim_kind": "methodological",
            "material_flags": [],
        }
        self.assertIn("methodological", gate.required_review_types(entity))


class PromotionTests(unittest.TestCase):
    def test_valid_normative_claim_promotion(self) -> None:
        records = [
            review(
                "structural",
                kind="machine",
                independence="not-applicable",
                accountable=False,
                permits=False,
            ),
            review("editorial", independence="internal"),
            review("ethical", independence="independent"),
        ]
        result, diagnostics = gate.evaluate_promotion(promotion(reviews=records))
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.decision, "eligible")
        self.assertEqual(
            set(result.satisfied_review_types),
            {"structural", "editorial", "ethical"},
        )

    def test_ai_only_domain_review_is_insufficient(self) -> None:
        entity = {
            "id": "concept:en:test",
            "revision": 1,
            "type": "concept",
            "status": "in-review",
            "staleness": "current",
        }
        records = [
            review(
                "structural",
                entity_id="concept:en:test",
                kind="machine",
                independence="not-applicable",
                accountable=False,
                permits=False,
            ),
            review("editorial", entity_id="concept:en:test", independence="internal"),
            review(
                "domain",
                entity_id="concept:en:test",
                kind="ai-assisted",
                independence="internal",
                accountable=False,
                permits=False,
            ),
        ]
        result, diagnostics = gate.evaluate_promotion(
            promotion(entity=entity, reviews=records)
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.decision, "blocked")
        self.assertTrue(
            any("missing acceptable domain review" in item for item in result.reasons)
        )

    def test_wrong_revision_review_is_insufficient(self) -> None:
        entity = {
            "id": "source:en:test",
            "revision": 2,
            "type": "source",
            "status": "in-review",
            "staleness": "current",
        }
        records = [
            review(
                "structural",
                entity_id="source:en:test",
                revision=1,
                kind="machine",
                independence="not-applicable",
                accountable=False,
                permits=False,
            ),
            review("source", entity_id="source:en:test", revision=1, independence="internal"),
        ]
        result, diagnostics = gate.evaluate_promotion(
            promotion(entity=entity, reviews=records, required=["structural", "source"])
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.decision, "blocked")
        self.assertTrue(any("another entity revision" in item for item in result.reasons))

    def test_synthetic_stale_translation_is_blocked(self) -> None:
        entity = {
            "id": "claim:fr:test",
            "revision": 1,
            "type": "claim",
            "status": "in-review",
            "staleness": "possibly-stale",
            "claim_kind": "model-derived",
            "translation_of": "claim:en:test",
            "translation_source_revision": 1,
            "source_current_revision": 2,
            "material_flags": ["fully-specified-reproducibility"],
        }
        result, _ = gate.evaluate_promotion(promotion(entity=entity, reviews=[]))
        self.assertEqual(result.decision, "blocked")
        self.assertIn(
            "translation source revision does not match current source revision",
            result.reasons,
        )

    def test_expired_review_is_blocked(self) -> None:
        payload = promotion(
            reviews=[
                review(
                    "structural",
                    kind="machine",
                    independence="not-applicable",
                    accountable=False,
                    permits=False,
                ),
                review("editorial", independence="internal"),
                review("ethical", horizon="2026-07-26"),
            ]
        )
        payload["decision_at"] = "2026-07-27"
        result, diagnostics = gate.evaluate_promotion(payload)
        self.assertEqual(diagnostics, [])
        self.assertEqual(result.decision, "blocked")
        self.assertTrue(any("expired" in reason for reason in result.reasons))

    def test_contested_transitions(self) -> None:
        blocked, diagnostics = gate.evaluate_promotion(
            promotion(
                requested_status="contested",
                transition={
                    "positions": ["claim:en:a"],
                    "unresolved_questions": ["question:en:q"],
                    "reason": "Dispute",
                },
            )
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(blocked.decision, "blocked")

        eligible, diagnostics = gate.evaluate_promotion(
            promotion(
                requested_status="contested",
                transition={
                    "positions": ["claim:en:a", "claim:en:b"],
                    "unresolved_questions": ["question:en:q"],
                    "reason": "Credible interpretations remain incompatible.",
                },
            )
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(eligible.decision, "eligible")

    def test_deprecation_and_retraction_transitions(self) -> None:
        deprecated, _ = gate.evaluate_promotion(
            promotion(
                requested_status="deprecated",
                transition={
                    "reason": "Superseded",
                    "effective_date": "2026-07-26",
                    "affected_dependents": [],
                },
            )
        )
        self.assertEqual(deprecated.decision, "blocked")
        self.assertTrue(any("replacement" in reason for reason in deprecated.reasons))

        retracted, diagnostics = gate.evaluate_promotion(
            promotion(
                requested_status="retracted",
                transition={
                    "reason": "Integrity failure",
                    "effective_date": "2026-07-26",
                    "replacement": None,
                    "affected_dependents": ["synthesis:en:test"],
                    "evidence": ["review:source:test-r1:2026-07-26"],
                    "current_use_prohibited": True,
                },
            )
        )
        self.assertEqual(diagnostics, [])
        self.assertEqual(retracted.decision, "eligible")

    def test_nonhuman_acceptor_is_rejected(self) -> None:
        payload = promotion(
            requested_status="contested",
            transition={
                "positions": ["claim:en:a", "claim:en:b"],
                "unresolved_questions": ["question:en:q"],
                "reason": "Dispute",
            },
        )
        payload["accepted_by"] = {
            "display_name": "Agent",
            "kind": "ai-assisted",
            "accountable": False,
        }
        result, diagnostics = gate.evaluate_promotion(payload)
        self.assertEqual(result.decision, "blocked")
        self.assertIn(
            "E-PROMOTION-HUMAN-ACCEPTANCE",
            {item.code for item in diagnostics},
        )

    def test_report_is_deterministic(self) -> None:
        payload = promotion(
            requested_status="contested",
            transition={
                "positions": ["claim:en:a", "claim:en:b"],
                "unresolved_questions": ["question:en:q"],
                "reason": "Dispute",
            },
        )
        result, diagnostics = gate.evaluate_promotion(payload)
        first = gate.render_report(payload, result, diagnostics)
        second = gate.render_report(payload, result, diagnostics)
        self.assertEqual(first, second)
        self.assertIn("Decision: **eligible**", first)


if __name__ == "__main__":
    unittest.main()
