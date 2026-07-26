from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
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
handoff_tool = load_module(
    "phase1_human_review_handoff", ROOT / "phase1_human_review_handoff.py"
)
intake = load_module("phase1_review_intake", ROOT / "phase1_review_intake.py")


class ReviewIntakeTests(unittest.TestCase):
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
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "handoff"
            handoff_tool.generate(
                cls.manifest_path,
                cls.records_dir,
                cls.canonical_root,
                output,
            )
            cls.handoff = json.loads(
                (output / "handoff.json").read_text(encoding="utf-8")
            )
        cls.tasks = intake.task_index(cls.handoff)

    def task(self, review_type: str, *, independence: str | None = None):
        for task in self.tasks.values():
            if task["review_type"] != review_type:
                continue
            allowed = task["reviewer_requirement"]["allowed_independence"]
            if independence is None or independence in allowed:
                return task
        raise AssertionError(f"No task for {review_type!r} and {independence!r}")

    def submission(
        self,
        task,
        *,
        reviewer_kind: str = "human",
        independence: str | None = None,
        accountable: bool = True,
        used_ai: bool = False,
        ai_description=None,
    ):
        entity = task["entity"]
        snapshot = task["entity_snapshot"]
        if independence is None:
            independence = task["reviewer_requirement"]["allowed_independence"][0]
        review_type = task["review_type"]
        return {
            "contract": "atlas-review-submission/0.1",
            "coverage_id": self.handoff["coverage_id"],
            "task_id": task["id"],
            "snapshot": {
                "entity_id": entity["id"],
                "revision": entity["revision"],
                "sha256": snapshot["sha256"],
            },
            "submitted_at": "2026-07-26",
            "reviewed_exact_snapshot": True,
            "ai_assistance": {
                "used": used_ai,
                "description": ai_description,
            },
            "review_record": {
                "contract": "atlas-review/0.1",
                "id": f"review:{review_type}:synthetic-intake-r1:2026-07-26",
                "entity": {
                    "id": entity["id"],
                    "revision": entity["revision"],
                },
                "review_type": review_type,
                "reviewer": {
                    "display_name": "Synthetic fixture reviewer",
                    "kind": reviewer_kind,
                    "independence": independence,
                    "qualification": "Synthetic test qualification for the requested review type",
                    "accountable": accountable,
                    "conflicts": [],
                },
                "completed_at": "2026-07-26",
                "review_horizon": None,
                "outcome": "pass",
                "findings": [],
                "summary": "Synthetic fixture review for intake validation tests only.",
                "permits_promotion": reviewer_kind == "human" and accountable,
            },
        }

    def codes(self, submission):
        return {
            diagnostic.code
            for diagnostic in intake.validate_submission(submission, self.handoff)
        }

    def test_valid_synthetic_editorial_submission(self) -> None:
        submission = self.submission(self.task("editorial", independence="internal"))
        self.assertEqual(intake.validate_submission(submission, self.handoff), [])

    def test_wrong_task_and_snapshot_digest_are_rejected(self) -> None:
        submission = self.submission(self.task("editorial"))
        submission["task_id"] = "review-task:missing"
        self.assertIn("E-INTAKE-TASK", self.codes(submission))

        submission = self.submission(self.task("editorial"))
        submission["snapshot"]["sha256"] = "0" * 64
        self.assertIn("E-INTAKE-SNAPSHOT-DIGEST", self.codes(submission))

    def test_review_entity_revision_and_type_must_match_task(self) -> None:
        submission = self.submission(self.task("source"))
        submission["review_record"]["entity"]["revision"] = 2
        submission["review_record"]["review_type"] = "editorial"
        codes = self.codes(submission)
        self.assertIn("E-INTAKE-REVIEW-REVISION", codes)
        self.assertIn("E-INTAKE-REVIEW-TYPE", codes)

    def test_nonhuman_or_nonaccountable_submission_is_rejected(self) -> None:
        submission = self.submission(
            self.task("editorial"),
            reviewer_kind="ai-assisted",
            independence="internal",
            accountable=False,
        )
        codes = self.codes(submission)
        self.assertIn("E-INTAKE-HUMAN", codes)
        self.assertIn("E-INTAKE-ACCOUNTABILITY", codes)

    def test_independent_task_rejects_internal_reviewer(self) -> None:
        submission = self.submission(
            self.task("domain", independence="independent"),
            independence="internal",
        )
        self.assertIn("E-INTAKE-INDEPENDENCE", self.codes(submission))

    def test_ai_assistance_requires_disclosure(self) -> None:
        submission = self.submission(
            self.task("editorial"),
            used_ai=True,
            ai_description=None,
        )
        self.assertIn("E-INTAKE-AI-DISCLOSURE", self.codes(submission))

        submission = self.submission(
            self.task("editorial"),
            used_ai=True,
            ai_description="AI was used to compare terminology; the human reviewer made the final judgment.",
        )
        self.assertEqual(intake.validate_submission(submission, self.handoff), [])

    def test_exact_snapshot_attestation_is_required(self) -> None:
        submission = self.submission(self.task("editorial"))
        submission["reviewed_exact_snapshot"] = False
        self.assertIn("E-INTAKE-SNAPSHOT-ATTESTATION", self.codes(submission))

    def test_normalized_record_preserves_intake_lineage(self) -> None:
        submission = self.submission(
            self.task("editorial"),
            used_ai=True,
            ai_description="AI prepared a comparison table only.",
        )
        record = intake.normalized_review_record(submission, self.handoff)
        lineage = record["metadata"]["intake"]
        self.assertEqual(lineage["task_id"], submission["task_id"])
        self.assertEqual(lineage["snapshot"], submission["snapshot"])
        self.assertTrue(lineage["reviewed_exact_snapshot"])
        self.assertTrue(lineage["ai_assistance"]["used"])
        self.assertEqual(record["entity"], submission["review_record"]["entity"])

    def test_extract_does_not_modify_repository_records(self) -> None:
        before = {
            path.relative_to(self.records_dir).as_posix(): path.read_bytes()
            for path in self.records_dir.glob("*.json")
        }
        submission = self.submission(self.task("editorial"))
        intake.normalized_review_record(submission, self.handoff)
        after = {
            path.relative_to(self.records_dir).as_posix(): path.read_bytes()
            for path in self.records_dir.glob("*.json")
        }
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
