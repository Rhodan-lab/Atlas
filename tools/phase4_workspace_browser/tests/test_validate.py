from __future__ import annotations

import hashlib
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError, render_json
from tools.phase4_workspace_browser.validate import FILES, validate_directory


def seal(record: dict) -> dict:
    unsigned = dict(record)
    unsigned.pop("report_digest", None)
    sealed = dict(record)
    sealed["report_digest"] = hashlib.sha256(render_json(unsigned).encode("utf-8")).hexdigest()
    return sealed


def write_record(path: Path, record: dict) -> bytes:
    payload = render_json(record).encode("utf-8")
    path.write_bytes(payload)
    return payload


def mutate_resealed(root: Path, key: str, mutation) -> None:
    target_path = root / FILES[key]
    target = json.loads(target_path.read_bytes())
    mutation(target)
    target = seal(target)
    target_bytes = write_record(target_path, target)

    manifest_path = root / FILES["manifest"]
    manifest = json.loads(manifest_path.read_bytes())
    artifact = next(item for item in manifest["artifacts"] if item["file"] == FILES[key])
    artifact["bytes"] = len(target_bytes)
    artifact["sha256"] = hashlib.sha256(target_bytes).hexdigest()
    artifact["report_digest"] = target["report_digest"]
    artifact["contract"] = target["contract"]
    manifest = seal(manifest)
    write_record(manifest_path, manifest)

    report_path = root / FILES["report"]
    report = json.loads(report_path.read_bytes())
    report["child_digests"][key] = target["report_digest"]
    report["child_digests"]["manifest"] = manifest["report_digest"]
    report = seal(report)
    write_record(report_path, report)


class WorkspaceBrowserEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        raw = os.environ.get("ATLAS_WORKSPACE_BROWSER_EVIDENCE_DIR")
        if not raw:
            raise unittest.SkipTest("ATLAS_WORKSPACE_BROWSER_EVIDENCE_DIR is required")
        cls.source = Path(raw)

    def copied(self):
        directory = tempfile.TemporaryDirectory()
        root = Path(directory.name) / "evidence"
        shutil.copytree(self.source, root)
        return directory, root

    def test_valid_directory_passes(self) -> None:
        result = validate_directory(self.source)
        self.assertEqual(result["decision"], "valid-workspace-browser-candidate")
        self.assertEqual(result["route_count"], 13)
        self.assertEqual(result["external_request_count"], 0)
        self.assertTrue(result["local_download_byte_identical"])
        self.assertFalse(result["human_verified"])
        self.assertFalse(result["repository_mutation"])

    def test_resealed_external_request_is_rejected(self) -> None:
        directory, root = self.copied()
        with directory:
            def mutation(record):
                record["external_request_count"] = 1
                record["requests"].append({
                    "decision": "blocked-external",
                    "method": "GET",
                    "resource_type": "fetch",
                    "url": "https://example.invalid/unsafe",
                })
            mutate_resealed(root, "network", mutation)
            with self.assertRaisesRegex(KernelError, "E-WS-BROWSER-NETWORK"):
                validate_directory(root)

    def test_resealed_download_mismatch_is_rejected(self) -> None:
        directory, root = self.copied()
        with directory:
            def mutation(record):
                record["local_download"]["sha256"] = "0" * 64
                record["local_download"]["byte_identical"] = False
            mutate_resealed(root, "workflow", mutation)
            with self.assertRaisesRegex(KernelError, "E-WS-BROWSER-DOWNLOAD"):
                validate_directory(root)

    def test_resealed_human_verification_claim_is_rejected(self) -> None:
        directory, root = self.copied()
        with directory:
            mutate_resealed(root, "accessibility", lambda record: record.__setitem__("human_verified", True))
            with self.assertRaisesRegex(KernelError, "E-WS-BROWSER-ACCESSIBILITY"):
                validate_directory(root)

    def test_resealed_candidate_resolution_is_rejected(self) -> None:
        directory, root = self.copied()
        with directory:
            mutate_resealed(root, "workflow", lambda record: record.__setitem__("candidates_unresolved", False))
            with self.assertRaisesRegex(KernelError, "E-WS-BROWSER-AUTHORITY"):
                validate_directory(root)


if __name__ == "__main__":
    unittest.main()
