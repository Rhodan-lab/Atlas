from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.phase4_browser.validate import BrowserEvidenceError, render_json, validate_evidence_directory


class BrowserEvidenceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        configured = os.environ.get("ATLAS_BROWSER_EVIDENCE_DIR", "phase4-browser-evidence-a")
        cls.source = Path(configured).resolve()
        if not cls.source.exists():
            raise unittest.SkipTest(f"browser evidence directory does not exist: {cls.source}")

    def _copy(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        target = Path(temporary.name) / "evidence"
        shutil.copytree(self.source, target)
        return temporary, target

    @staticmethod
    def _seal(record: dict) -> dict:
        unsigned = dict(record)
        unsigned.pop("report_digest", None)
        record["report_digest"] = hashlib.sha256(render_json(unsigned).encode("utf-8")).hexdigest()
        return record

    @classmethod
    def _rewrite_bound_file(cls, root: Path, filename: str, mutate) -> None:
        path = root / filename
        record = json.loads(path.read_text(encoding="utf-8"))
        mutate(record)
        cls._seal(record)
        payload = render_json(record).encode("utf-8")
        path.write_bytes(payload)

        report_path = root / "browser-evidence-report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        entry = next(item for item in report["evidence_files"] if item["file"] == filename)
        entry["bytes"] = len(payload)
        entry["sha256"] = hashlib.sha256(payload).hexdigest()
        entry["report_digest"] = record["report_digest"]
        cls._seal(report)
        report_path.write_text(render_json(report), encoding="utf-8")

    def test_valid_generated_evidence(self) -> None:
        result = validate_evidence_directory(self.source)
        self.assertEqual(result["decision"], "valid-browser-evidence-candidate")
        self.assertEqual(result["workflow_count"], 8)
        self.assertEqual(result["external_request_count"], 0)
        self.assertFalse(result["human_verified"])

    def test_external_request_is_rejected_even_with_valid_digests(self) -> None:
        temporary, target = self._copy()
        self.addCleanup(temporary.cleanup)

        def mutate(record: dict) -> None:
            record["external_request_count"] = 1
            record["blocked_external_request_count"] = 1
            record["request_records"].append(
                {
                    "decision": "blocked-external",
                    "method": "GET",
                    "resource_type": "script",
                    "url": "https://example.invalid/remote.js",
                }
            )

        self._rewrite_bound_file(target, "browser-network.json", mutate)
        with self.assertRaisesRegex(BrowserEvidenceError, "E-BROWSER-NETWORK"):
            validate_evidence_directory(target)

    def test_implicit_latest_is_rejected_even_with_valid_digests(self) -> None:
        temporary, target = self._copy()
        self.addCleanup(temporary.cleanup)

        def mutate(record: dict) -> None:
            record["workflows"][0]["workflow_id"] = "claim:en:example@latest"

        self._rewrite_bound_file(target, "browser-workflows.json", mutate)
        with self.assertRaisesRegex(BrowserEvidenceError, "E-BROWSER-REVISION"):
            validate_evidence_directory(target)

    def test_human_verification_escalation_is_rejected(self) -> None:
        temporary, target = self._copy()
        self.addCleanup(temporary.cleanup)

        def mutate(record: dict) -> None:
            record["human_verified"] = True

        self._rewrite_bound_file(target, "browser-accessibility.json", mutate)
        with self.assertRaisesRegex(BrowserEvidenceError, "E-BROWSER-REVIEW"):
            validate_evidence_directory(target)

    def test_non_graph_equivalence_cannot_be_removed(self) -> None:
        temporary, target = self._copy()
        self.addCleanup(temporary.cleanup)

        def mutate(record: dict) -> None:
            record["workflows"][0]["non_graph_route_exercised"] = False

        self._rewrite_bound_file(target, "browser-workflows.json", mutate)
        with self.assertRaisesRegex(BrowserEvidenceError, "E-BROWSER-NON-GRAPH"):
            validate_evidence_directory(target)


if __name__ == "__main__":
    unittest.main()
