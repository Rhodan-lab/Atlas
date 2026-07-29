from __future__ import annotations

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, render_json
from tools.phase4_workspace_reader_browser.validate import FILES, validate_directory


class ReaderReuseBrowserValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        value = os.environ.get("ATLAS_READER_REUSE_BROWSER_EVIDENCE_DIR")
        if value is None:
            raise unittest.SkipTest("browser evidence directory is not available")
        cls.source = Path(value)

    def _copy(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name) / "evidence"
        shutil.copytree(self.source, root)
        return temporary, root

    def _mutate_report(self, root: Path, mutate) -> None:
        path = root / FILES["report"]
        report = json.loads(path.read_text(encoding="utf-8"))
        mutate(report)
        unsigned = dict(report)
        unsigned.pop("report_digest", None)
        import hashlib
        report["report_digest"] = hashlib.sha256(render_json(unsigned).encode("utf-8")).hexdigest()
        path.write_text(render_json(report), encoding="utf-8")

    def test_valid_directory(self):
        result = validate_directory(self.source)
        self.assertEqual(result["decision"], "valid-reader-reuse-browser-candidate")
        self.assertEqual(result["recommendation"], "proceed-workstream4-closure-evaluation")
        self.assertEqual(result["exit_gate_count"], 13)

    def test_production_recommendation_is_rejected(self):
        temporary, root = self._copy()
        try:
            self._mutate_report(root, lambda report: report.update({"decision": "proceed-production-workspace"}))
            with self.assertRaisesRegex(KernelError, "E-READER-BROWSER-DECISION"):
                validate_directory(root)
        finally:
            temporary.cleanup()

    def test_self_authorization_is_rejected(self):
        temporary, root = self._copy()
        try:
            self._mutate_report(root, lambda report: report.update({"implementation_authorized": True}))
            with self.assertRaisesRegex(KernelError, "E-READER-BROWSER-DECISION"):
                validate_directory(root)
        finally:
            temporary.cleanup()

    def test_external_request_claim_is_rejected(self):
        temporary, root = self._copy()
        try:
            self._mutate_report(root, lambda report: report.update({"external_request_count": 1}))
            with self.assertRaisesRegex(KernelError, "E-READER-BROWSER-REPORT"):
                validate_directory(root)
        finally:
            temporary.cleanup()

    def test_selector_fallback_claim_is_rejected(self):
        temporary, root = self._copy()
        try:
            self._mutate_report(root, lambda report: report.update({"selector_unknown_fixture_refused": False}))
            with self.assertRaisesRegex(KernelError, "E-READER-BROWSER-REPORT"):
                validate_directory(root)
        finally:
            temporary.cleanup()

    def test_false_accessibility_certification_is_rejected(self):
        temporary, root = self._copy()
        try:
            self._mutate_report(root, lambda report: report.update({"accessibility_certified": True}))
            with self.assertRaisesRegex(KernelError, "E-READER-BROWSER-REPORT"):
                validate_directory(root)
        finally:
            temporary.cleanup()

    def test_package_identity_drift_is_rejected(self):
        temporary, root = self._copy()
        try:
            self._mutate_report(root, lambda report: report.update({"package_index_sha256": "0" * 64}))
            with self.assertRaisesRegex(KernelError, "E-READER-BROWSER-REPORT"):
                validate_directory(root)
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
