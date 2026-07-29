from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

from tools.phase2_kernel import KernelError
from tools.phase4_workspace_reader_reuse.builder import (
    PACKAGE_CONTRACT,
    REPORT_CONTRACT,
    SELECTOR_JS,
    STATIC_ASSETS,
    build_reader_reuse_package,
    validate_package_index,
)

ROOT = Path(__file__).resolve().parents[3]


class ReaderReusePackageTests(unittest.TestCase):
    def _build(self):
        temporary = tempfile.TemporaryDirectory()
        output = Path(temporary.name) / "reader-reuse"
        index, report, validation = build_reader_reuse_package(ROOT, output)
        return temporary, output, index, report, validation

    def test_package_is_deterministic_and_valid(self):
        first_temp, first_output, first_index, first_report, first_validation = self._build()
        second_temp, second_output, second_index, second_report, second_validation = self._build()
        try:
            first_files = {
                path.relative_to(first_output).as_posix(): path.read_bytes()
                for path in first_output.rglob("*")
                if path.is_file()
            }
            second_files = {
                path.relative_to(second_output).as_posix(): path.read_bytes()
                for path in second_output.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first_files, second_files)
            self.assertEqual(first_index, second_index)
            self.assertEqual(first_report, second_report)
            self.assertEqual(first_validation, second_validation)
            self.assertEqual(first_index["contract"], PACKAGE_CONTRACT)
            self.assertEqual(first_report["contract"], REPORT_CONTRACT)
            self.assertEqual(first_validation["decision"], "valid-reader-reuse-package-candidate")
        finally:
            first_temp.cleanup()
            second_temp.cleanup()

    def test_both_packages_reuse_identical_reader_assets(self):
        temporary, output, index, _, _ = self._build()
        try:
            for name in STATIC_ASSETS:
                recommender = (output / "packages/recommender" / name).read_bytes()
                catalase = (output / "packages/catalase" / name).read_bytes()
                accepted = (ROOT / "apps/workspace-shell" / name).read_bytes()
                self.assertEqual(recommender, accepted)
                self.assertEqual(catalase, accepted)
            self.assertTrue(index["regression"]["accepted_reader_assets_byte_identical"])
        finally:
            temporary.cleanup()

    def test_package_index_has_only_one_generalized_fixture(self):
        temporary, _, index, report, _ = self._build()
        try:
            self.assertEqual([item["id"] for item in index["fixtures"]], ["recommender", "catalase"])
            self.assertEqual(report["counts"]["generalized_fixtures"], 1)
            self.assertFalse(index["authority"]["second_generalized_fixture_authorized"])
        finally:
            temporary.cleanup()

    def test_unknown_fixture_has_explicit_refusal(self):
        self.assertIn("Unknown fixture rejected", SELECTOR_JS)
        self.assertIn("no fallback package loaded", SELECTOR_JS)
        self.assertNotIn('ACCEPTED_FIXTURES.get(requested) ||', SELECTOR_JS)

    def test_browser_evidence_is_not_claimed(self):
        temporary, _, index, report, validation = self._build()
        try:
            self.assertFalse(index["browser_evidence_included"])
            self.assertFalse(report["browser_evidence_included"])
            self.assertFalse(report["slice2_recommendation_issued"])
            self.assertFalse(validation["browser_evidence_included"])
        finally:
            temporary.cleanup()

    def test_package_authority_tampering_is_rejected(self):
        temporary, _, index, _, _ = self._build()
        try:
            candidate = copy.deepcopy(index)
            candidate["authority"]["canonical_mutation"] = True
            with self.assertRaisesRegex(KernelError, "E-READER-REUSE-AUTHORITY"):
                validate_package_index(candidate)
        finally:
            temporary.cleanup()

    def test_second_fixture_tampering_is_rejected(self):
        temporary, _, index, _, _ = self._build()
        try:
            candidate = copy.deepcopy(index)
            candidate["fixtures"].append(copy.deepcopy(candidate["fixtures"][1]))
            candidate["fixtures"][-1]["id"] = "second-catalase"
            with self.assertRaisesRegex(KernelError, "E-READER-REUSE-FIXTURE"):
                validate_package_index(candidate)
        finally:
            temporary.cleanup()

    def test_unknown_fixture_fallback_tampering_is_rejected(self):
        temporary, _, index, _, _ = self._build()
        try:
            candidate = copy.deepcopy(index)
            candidate["selector"]["unknown_fixture_fallback"] = "recommender"
            with self.assertRaisesRegex(KernelError, "E-READER-REUSE-FALLBACK"):
                validate_package_index(candidate)
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
