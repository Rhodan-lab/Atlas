from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


foundation = load_module(
    "atlas_foundation_validator", ROOT / "atlas_foundation_validator.py"
)
gate = load_module("phase1_review_gate", ROOT / "phase1_review_gate.py")
coverage = load_module("phase1_coverage_report", ROOT / "phase1_coverage_report.py")
backlog = load_module("phase1_review_backlog", ROOT / "phase1_review_backlog.py")
handoff = load_module(
    "phase1_human_review_handoff", ROOT / "phase1_human_review_handoff.py"
)


class HumanReviewHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest_path = (
            REPO_ROOT
            / "content"
            / "reviews"
            / "coverage"
            / "feedback-complete-vertical-slice.json"
        )
        cls.records_dir = REPO_ROOT / "content" / "reviews" / "records"
        cls.canonical_root = REPO_ROOT / "content" / "canonical"
        cls.manifest = handoff.load_manifest(cls.manifest_path)
        cls.records, diagnostics = coverage.load_review_records(cls.records_dir)
        errors = [item for item in diagnostics if item.severity == "error"]
        if errors:
            raise AssertionError(errors)
        cls.snapshots = handoff.discover_snapshots(cls.canonical_root)
        cls.result = handoff.build_handoff(
            cls.manifest,
            cls.records,
            cls.snapshots,
            "content/reviews/coverage/feedback-complete-vertical-slice.json",
        )

    def test_exact_human_task_and_track_counts(self) -> None:
        self.assertEqual(self.result["contract"], "atlas-review-handoff/0.1")
        self.assertEqual(self.result["coverage_decision"], "blocked")
        self.assertEqual(self.result["task_count"], 25)
        self.assertEqual(self.result["track_count"], 5)
        self.assertEqual(self.result["entity_snapshot_count"], 10)
        counts = Counter(
            {
                track["id"]: track["task_count"]
                for track in self.result["tracks"]
            }
        )
        self.assertEqual(
            counts,
            Counter(
                {
                    "domain-authority": 7,
                    "editorial-and-scope": 7,
                    "methods-and-inference": 5,
                    "source-and-provenance": 5,
                    "reproducibility": 1,
                }
            ),
        )

    def test_every_task_is_human_accountable_and_unique(self) -> None:
        tasks = [task for track in self.result["tracks"] for task in track["tasks"]]
        task_ids = [task["id"] for task in tasks]
        self.assertEqual(len(task_ids), len(set(task_ids)))
        for task in tasks:
            self.assertEqual(task["execution_mode"], "human-required")
            self.assertTrue(task["required_for_gate"])
            requirement = task["reviewer_requirement"]
            self.assertEqual(requirement["allowed_kinds"], ["human"])
            self.assertTrue(requirement["accountability_required"])

    def test_no_reviewer_is_assigned_or_fabricated(self) -> None:
        self.assertIsNone(self.result["reviewer_assignment"])

        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    self.assertNotIn(key, {"reviewer", "assignee", "assigned_to"})
                    walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

        walk(self.result["tracks"])

    def test_entity_snapshots_match_exact_canonical_files(self) -> None:
        for item in self.result["entity_snapshots"]:
            path = REPO_ROOT / item["canonical_path"]
            self.assertTrue(path.is_file())
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            self.assertEqual(item["sha256"], digest)

    def test_existing_major_finding_remains_visible(self) -> None:
        domain = next(
            track for track in self.result["tracks"] if track["id"] == "domain-authority"
        )
        formal_claim = next(
            task
            for task in domain["tasks"]
            if task["entity"]["id"]
            == "claim:en:stated-delayed-recurrence-oscillates"
        )
        self.assertIn(
            "review:domain:feedback-oscillation-r1:2026-07-26",
            formal_claim["existing_review_ids"],
        )
        self.assertTrue(formal_claim["blockers"])
        self.assertTrue(
            any(
                "major" in blocker.lower()
                or "changes-required" in blocker.lower()
                or "authority" in blocker.lower()
                for blocker in formal_claim["blockers"]
            )
        )

    def test_bundle_generation_is_deterministic_and_self_contained(self) -> None:
        with tempfile.TemporaryDirectory() as first_tmp, tempfile.TemporaryDirectory() as second_tmp:
            first = Path(first_tmp) / "handoff"
            second = Path(second_tmp) / "handoff"
            first_result = handoff.generate(
                self.manifest_path,
                self.records_dir,
                self.canonical_root,
                first,
            )
            second_result = handoff.generate(
                self.manifest_path,
                self.records_dir,
                self.canonical_root,
                second,
            )
            self.assertEqual(first_result, second_result)
            self.assertEqual(handoff.directory_digest(first), handoff.directory_digest(second))
            self.assertTrue((first / "handoff.json").is_file())
            self.assertTrue((first / "README.md").is_file())
            self.assertEqual(len(list((first / "tracks").glob("*.json"))), 5)
            self.assertEqual(len(list((first / "tracks").glob("*.md"))), 5)
            self.assertEqual(len(list((first / "entities").rglob("*.md"))), 10)

            loaded = json.loads((first / "handoff.json").read_text(encoding="utf-8"))
            handoff.validate_handoff(loaded)


if __name__ == "__main__":
    unittest.main()
