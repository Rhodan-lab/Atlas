from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError
from tools.phase4_workspace import package_product_input


class ProductInputTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.package = self.root / "atlas-product-input"

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_builds_exact_verified_principia_atlas_input(self) -> None:
        built = package_product_input.build_product_input(self.package)
        verified = package_product_input.verify_product_input(self.package)
        self.assertEqual(built, verified)
        self.assertEqual(
            {
                path.relative_to(self.package).as_posix()
                for path in self.package.rglob("*")
                if path.is_file()
            },
            set(package_product_input.PACKAGE_FILES),
        )
        self.assertEqual(built["contract"], "atlas-principia-product-input-verification/0.1")
        self.assertEqual(built["decision"], "valid")
        self.assertEqual(built["file_count"], 8)
        self.assertEqual(built["principia_reference_count"], 1)
        self.assertFalse(built["live"])
        report = json.loads(
            (self.package / package_product_input.REPORT_NAME).read_text(encoding="utf-8")
        )
        self.assertEqual(report["contract"], "atlas-workspace-shell-build-report/0.1")
        self.assertFalse(report["live_principia_dependency"])
        self.assertFalse(report["external_network_required"])

    def test_product_input_build_is_deterministic(self) -> None:
        result = package_product_input.check_determinism()
        self.assertEqual(result["decision"], "valid")
        self.assertEqual(result["file_count"], 8)

    def test_rejects_existing_output_without_mutation(self) -> None:
        self.package.mkdir()
        marker = self.package / "preserve.txt"
        marker.write_text("preserve", encoding="utf-8")
        with self.assertRaisesRegex(KernelError, "must not already exist"):
            package_product_input.build_product_input(self.package)
        self.assertEqual(marker.read_text(encoding="utf-8"), "preserve")

    def test_rejects_static_asset_drift(self) -> None:
        package_product_input.build_product_input(self.package)
        (self.package / "app.js").write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(KernelError, "differs from Atlas source"):
            package_product_input.verify_product_input(self.package)

    def test_rejects_generated_artifact_drift(self) -> None:
        package_product_input.build_product_input(self.package)
        export_path = self.package / "data" / "workspace-export.json"
        export_path.write_bytes(export_path.read_bytes() + b" ")
        with self.assertRaisesRegex(KernelError, "accepted_export artifact identity mismatch"):
            package_product_input.verify_product_input(self.package)

    def test_rejects_resealed_report_authority_drift(self) -> None:
        package_product_input.build_product_input(self.package)
        report_path = self.package / package_product_input.REPORT_NAME
        report = json.loads(report_path.read_text(encoding="utf-8"))
        report["live_principia_dependency"] = True
        report["report_digest"] = package_product_input._json_digest(
            report, "report_digest"
        )
        report_path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(KernelError, "authority boundary was relaxed"):
            package_product_input.verify_product_input(self.package)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks are unavailable")
    def test_rejects_symlinked_package_entry(self) -> None:
        package_product_input.build_product_input(self.package)
        app = self.package / "app.js"
        outside = self.root / "outside.js"
        outside.write_text("outside", encoding="utf-8")
        app.unlink()
        try:
            app.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"symlink creation unavailable: {exc}")
        with self.assertRaisesRegex(KernelError, "must not be a symlink"):
            package_product_input.verify_product_input(self.package)


if __name__ == "__main__":
    unittest.main()
