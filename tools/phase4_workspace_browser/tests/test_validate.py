from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError
from tools.phase4_workspace_browser.validate import validate_directory


def _json_sha256(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _render(value):
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def _reseal(record):
    value = copy.deepcopy(record)
    value.pop("report_digest", None)
    value["report_digest"] = _json_sha256(value)
    return value


class WorkspaceBrowserEvidenceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        source = os.environ.get("ATLAS_WORKSPACE_BROWSER_EVIDENCE_DIR")
        if not source:
            raise unittest.SkipTest("ATLAS_WORKSPACE_BROWSER_EVIDENCE_DIR is not set")
        cls.source = Path(source)

    def _copy(self) -> tuple[tempfile.TemporaryDirectory, Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name) / "evidence"
        shutil.copytree(self.source, root)
        return temp, root

    def _tamper_child(self, root: Path, file_name: str, mutator) -> None:
        child_path = root / file_name
        child = json.loads(child_path.read_text(encoding="utf-8"))
        mutator(child)
        child = _reseal(child)
        child_path.write_text(_render(child), encoding="utf-8")

        report_path = root / "workspace-browser-report.json"
        report = json.loads(report_path.read_text(encoding="utf-8"))
        payload = child_path.read_bytes()
        artifact = next(item for item in report["evidence_files"] if item["file"] == file_name)
        artifact["bytes"] = len(payload)
        artifact["sha256"] = hashlib.sha256(payload).hexdigest()
        artifact["report_digest"] = child["report_digest"]
        report_path.write_text(_render(_reseal(report)), encoding="utf-8")

    def _tamper_report(self, root: Path, mutator) -> None:
        path = root / "workspace-browser-report.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        mutator(report)
        path.write_text(_render(_reseal(report)), encoding="utf-8")

    def test_valid_evidence_passes(self) -> None:
        validation = validate_directory(self.source)
        self.assertEqual(validation["decision"], "valid-workspace-browser-evidence-candidate")
        self.assertEqual(validation["route_count"], 13)
        self.assertEqual(validation["external_request_count"], 0)
        self.assertFalse(validation["human_verified"])
        self.assertFalse(validation["accessibility_certified"])

    def test_external_request_is_rejected_after_reseal(self) -> None:
        temp, root = self._copy()
        self.addCleanup(temp.cleanup)

        def mutate(record):
            record["external_request_count"] = 1
            record["records"].append({
                "count": 1,
                "decision": "blocked-external",
                "has_credentials": False,
                "method": "GET",
                "resource_type": "fetch",
                "url": "https://example.invalid/external.json",
            })

        self._tamper_child(root, "workspace-browser-network.json", mutate)
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-BROWSER-NETWORK"):
            validate_directory(root)

    def test_route_removal_is_rejected_after_reseal(self) -> None:
        temp, root = self._copy()
        self.addCleanup(temp.cleanup)

        def mutate(record):
            record["routes"].pop()
            record["route_count"] = 12
            record["keyboard_route_count"] = 12

        self._tamper_child(root, "workspace-browser-workflows.json", mutate)
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-BROWSER-ROUTES"):
            validate_directory(root)

    def test_human_verification_claim_is_rejected_after_reseal(self) -> None:
        temp, root = self._copy()
        self.addCleanup(temp.cleanup)

        def mutate(record):
            record["human_verified"] = True

        self._tamper_child(root, "workspace-browser-accessibility.json", mutate)
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-BROWSER-AUTHORITY"):
            validate_directory(root)

    def test_silent_fallback_is_rejected_after_reseal(self) -> None:
        temp, root = self._copy()
        self.addCleanup(temp.cleanup)

        def mutate(record):
            record["silent_fallback_allowed"] = True

        self._tamper_child(root, "workspace-browser-failures.json", mutate)
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-BROWSER-FAILURE"):
            validate_directory(root)

    def test_download_identity_claim_is_rejected_after_reseal(self) -> None:
        temp, root = self._copy()
        self.addCleanup(temp.cleanup)

        def mutate(record):
            record["local_download_byte_identical"] = False

        self._tamper_report(root, mutate)
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-BROWSER-REPORT"):
            validate_directory(root)


if __name__ == "__main__":
    unittest.main()
