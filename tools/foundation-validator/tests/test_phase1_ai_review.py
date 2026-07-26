from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

import phase1_ai_review as ai_review


class Phase1AIReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.review_path = REPO_ROOT / "content" / "reviews" / "ai" / "feedback-delayed-comprehensive.json"
        cls.canonical_root = REPO_ROOT / "content" / "canonical"
        cls.payload = json.loads(cls.review_path.read_text(encoding="utf-8"))

    def codes(self, payload: dict) -> set[str]:
        return {
            item.code
            for item in ai_review.validate_review(payload, self.canonical_root)
        }

    def test_repository_ai_review_is_valid(self) -> None:
        self.assertEqual(self.codes(copy.deepcopy(self.payload)), set())

    def test_human_verification_cannot_be_falsely_claimed(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["reviewer"]["human_verified"] = True
        self.assertIn("E-AI-HUMAN-CLAIM", self.codes(payload))

    def test_human_duty_must_be_disabled(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["human_review_required"] = True
        self.assertIn("E-AI-HUMAN-DUTY", self.codes(payload))

    def test_wrong_period_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["mathematical_verification"]["period"] = 8
        self.assertIn("E-AI-PERIOD", self.codes(payload))

    def test_wrong_sequence_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["mathematical_verification"]["states_x0_through_x7"][-1] = 1
        self.assertIn("E-AI-SEQUENCE", self.codes(payload))

    def test_missing_entity_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["entities"].pop()
        self.assertIn("E-AI-ENTITY-SET", self.codes(payload))

    def test_wrong_revision_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["entities"][0]["revision"] = 99
        self.assertIn("E-AI-ENTITY-SET", self.codes(payload))

    def test_open_major_finding_is_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["findings"][0]["status"] = "open"
        self.assertIn("E-AI-OPEN-SERIOUS", self.codes(payload))

    def test_source_locator_is_pinned(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["source_verification"]["locator"] = "https://example.invalid"
        self.assertIn("E-AI-SOURCE-LOCATOR", self.codes(payload))


if __name__ == "__main__":
    unittest.main()
