from __future__ import annotations

import copy
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

import phase1_coverage_report as coverage
import phase1_human_review_handoff as handoff_tool
import phase1_review_admission as admission_tool
import phase1_review_gate as gate


class ReviewAdmissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        manifest = handoff_tool.load_manifest(handoff_tool.DEFAULT_MANIFEST)
        records, diagnostics = coverage.load_review_records(
            handoff_tool.DEFAULT_RECORDS_DIR
        )
        cls.assert_no_errors(diagnostics)
        snapshots = handoff_tool.discover_snapshots(
            handoff_tool.DEFAULT_CANONICAL_ROOT
        )
        cls.handoff = handoff_tool.build_handoff(
            manifest,
            records,
            snapshots,
            "content/reviews/coverage/feedback-complete-vertical-slice.json",
        )
        tasks = [
            task for track in cls.handoff["tracks"] for task in track["tasks"]
        ]
        cls.task = next(
            task
            for task in tasks
            if task["review_type"] == "editorial"
            and "internal" in task["reviewer_requirement"]["allowed_independence"]
        )

    @staticmethod
    def assert_no_errors(diagnostics) -> None:
        errors = [item for item in diagnostics if item.severity == "error"]
        if errors:
            raise AssertionError(errors)

    def valid_submission(self) -> dict:
        task = self.task
        entity = task["entity"]
        snapshot = task["entity_snapshot"]
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
            "ai_assistance": {"used": False, "description": None},
            "review_record": {
                "contract": "atlas-review/0.1",
                "id": "review:editorial:admission-test-r1:2026-07-26",
                "entity": {
                    "id": entity["id"],
                    "revision": entity["revision"],
                },
                "review_type": "editorial",
                "reviewer": {
                    "display_name": "Accountable test reviewer",
                    "kind": "human",
                    "independence": "internal",
                    "qualification": "Technical editing and scope-control test fixture",
                    "accountable": True,
                    "conflicts": [],
                },
                "completed_at": "2026-07-26",
                "review_horizon": None,
                "outcome": "pass",
                "findings": [],
                "summary": "Synthetic unit-test review; no real authority is claimed.",
                "permits_promotion": True,
            },
        }

    def valid_admission(self, *, test_fixture: bool = False) -> dict:
        return {
            "contract": "atlas-review-admission/0.1",
            "id": "admission:editorial-test:2026-07-26",
            "decision": "accept",
            "decided_at": "2026-07-26",
            "decider": {
                "display_name": "Accountable test maintainer",
                "kind": "human",
                "role": "Atlas review-record maintainer test fixture",
                "accountable": True,
                "conflicts": [],
            },
            "external_verification": {
                "reviewer_identity_checked": True,
                "qualification_checked": True,
                "independence_checked": True,
                "conflicts_checked": True,
                "method": "Synthetic unit-test declarations only; no real identity was verified.",
            },
            "rationale": "Accept the synthetic record into test history without accepting the knowledge.",
            "test_fixture": test_fixture,
        }

    def codes(self, admission: dict, submission: dict, known=None) -> set[str]:
        return {
            item.code
            for item in admission_tool.validate_admission(
                admission,
                submission,
                self.handoff,
                known_record_ids=known or set(),
            )
        }

    def test_valid_accept_prepares_lineage_without_changing_findings(self) -> None:
        submission = self.valid_submission()
        admission = self.valid_admission()
        self.assertEqual(self.codes(admission, submission), set())
        record = admission_tool.admitted_review_record(
            admission, submission, self.handoff
        )
        self.assertIn("intake", record["metadata"])
        self.assertIn("admission", record["metadata"])
        self.assertEqual(record["metadata"]["admission"]["decision"], "accept")
        self.assertTrue(record["permits_promotion"])
        self.assert_no_errors(gate.validate_review_record(record))

    def test_test_fixture_cannot_permit_promotion(self) -> None:
        record = admission_tool.admitted_review_record(
            self.valid_admission(test_fixture=True),
            self.valid_submission(),
            self.handoff,
        )
        self.assertFalse(record["permits_promotion"])
        self.assertTrue(record["metadata"]["admission"]["test_fixture"])

    def test_request_changes_can_receive_receipt_but_not_prepare_record(self) -> None:
        admission = self.valid_admission()
        admission["decision"] = "request-changes"
        admission["external_verification"]["qualification_checked"] = False
        self.assertEqual(self.codes(admission, self.valid_submission()), set())
        receipt = admission_tool.admission_receipt(admission, self.valid_submission())
        self.assertEqual(receipt["decision"], "request-changes")
        with self.assertRaisesRegex(ValueError, "only an accept decision"):
            admission_tool.admitted_review_record(
                admission, self.valid_submission(), self.handoff
            )

    def test_accept_requires_all_external_checks(self) -> None:
        admission = self.valid_admission()
        admission["external_verification"]["reviewer_identity_checked"] = False
        self.assertIn(
            "E-ADMISSION-VERIFICATION-INCOMPLETE",
            self.codes(admission, self.valid_submission()),
        )

    def test_decider_must_be_accountable_human(self) -> None:
        admission = self.valid_admission()
        admission["decider"]["kind"] = "ai-assisted"
        admission["decider"]["accountable"] = False
        codes = self.codes(admission, self.valid_submission())
        self.assertIn("E-ADMISSION-DECIDER-KIND", codes)
        self.assertIn("E-ADMISSION-DECIDER-ACCOUNTABILITY", codes)

    def test_decision_cannot_predate_submission(self) -> None:
        admission = self.valid_admission()
        admission["decided_at"] = "2026-07-25"
        self.assertIn(
            "E-ADMISSION-DATE-ORDER",
            self.codes(admission, self.valid_submission()),
        )

    def test_existing_review_id_blocks_acceptance(self) -> None:
        submission = self.valid_submission()
        known = {submission["review_record"]["id"]}
        self.assertIn(
            "E-ADMISSION-REVIEW-ID-EXISTS",
            self.codes(self.valid_admission(), submission, known),
        )

    def test_serious_findings_may_be_admitted_without_becoming_approval(self) -> None:
        submission = self.valid_submission()
        record = submission["review_record"]
        record["outcome"] = "changes-required"
        record["permits_promotion"] = False
        record["findings"] = [
            {
                "id": "finding:admission-test:material-scope",
                "severity": "major",
                "status": "open",
                "summary": "Material scope correction is required.",
                "rationale": "The review history must preserve this criticism.",
                "affected_fields": ["claim.statement"],
                "suggested_action": "Create a corrected canonical revision.",
            }
        ]
        admitted = admission_tool.admitted_review_record(
            self.valid_admission(), submission, self.handoff
        )
        self.assertEqual(admitted["outcome"], "changes-required")
        self.assertFalse(admitted["permits_promotion"])
        self.assertEqual(admitted["findings"][0]["severity"], "major")

    def test_prepare_function_does_not_write_repository_records(self) -> None:
        before = {
            path.name: path.read_bytes()
            for path in handoff_tool.DEFAULT_RECORDS_DIR.glob("*.json")
        }
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "admitted.json"
            record = admission_tool.admitted_review_record(
                self.valid_admission(test_fixture=True),
                self.valid_submission(),
                self.handoff,
            )
            output.write_text("{}", encoding="utf-8")
            self.assertTrue(output.exists())
            self.assertIn("admission", record["metadata"])
        after = {
            path.name: path.read_bytes()
            for path in handoff_tool.DEFAULT_RECORDS_DIR.glob("*.json")
        }
        self.assertEqual(before, after)

    def test_receipt_digests_are_deterministic(self) -> None:
        first = admission_tool.admission_receipt(
            self.valid_admission(), self.valid_submission()
        )
        second = admission_tool.admission_receipt(
            copy.deepcopy(self.valid_admission()), copy.deepcopy(self.valid_submission())
        )
        self.assertEqual(first, second)
        self.assertRegex(first["submission_sha256"], r"^[0-9a-f]{64}$")


if __name__ == "__main__":
    unittest.main()
