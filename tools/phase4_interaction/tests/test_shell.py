from __future__ import annotations

import copy
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from tools.phase2_kernel import KernelError, render_json
from tools.phase4_interaction.build_shell import (
    SHELL_BUILD_REPORT_CONTRACT,
    SHELL_DATA_CONTRACT,
    build_shell_data,
    validate_shell_data,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
MANIFEST = ROOT / "content" / "fixtures" / "phase4_interaction" / "reference-interactions.v01.json"
SHELL = ROOT / "apps" / "reference-shell"


class LandmarkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = None
        self.ids: set[str] = set()
        self.tags: list[str] = []
        self.skip_href = None
        self.scripts: list[dict[str, str | None]] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = values.get("lang")
        if values.get("id"):
            self.ids.add(values["id"])
        if tag == "a" and values.get("class") == "skip-link":
            self.skip_href = values.get("href")
        if tag == "script":
            self.scripts.append(values)


class Phase4ReferenceShellTests(unittest.TestCase):
    def test_build_is_deterministic_and_valid(self) -> None:
        first_data, first_report = build_shell_data(CANONICAL, MANIFEST)
        second_data, second_report = build_shell_data(CANONICAL, MANIFEST)
        self.assertEqual(render_json(first_data), render_json(second_data))
        self.assertEqual(render_json(first_report), render_json(second_report))
        validation = validate_shell_data(first_data)
        self.assertEqual(first_data["contract"], SHELL_DATA_CONTRACT)
        self.assertEqual(first_report["contract"], SHELL_BUILD_REPORT_CONTRACT)
        self.assertEqual(validation["decision"], "valid")
        self.assertEqual(validation["view_count"], 8)
        self.assertEqual(validation["state_count"], 8)
        self.assertEqual(validation["failure_count"], 5)
        self.assertFalse(first_report["api_required"])
        self.assertFalse(first_report["cloud_required"])
        self.assertFalse(first_report["account_required"])
        self.assertFalse(first_report["graph_required"])
        self.assertTrue(first_report["keyboard_navigation_required"])
        self.assertTrue(first_report["non_graph_navigation_required"])
        self.assertTrue(first_report["local_first"])
        self.assertTrue(first_report["replaceable"])
        self.assertFalse(first_report["live"])
        self.assertFalse(first_report["repository_mutation"])

    def test_build_digest_tampering_is_rejected(self) -> None:
        payload, _ = build_shell_data(CANONICAL, MANIFEST)
        tampered = copy.deepcopy(payload)
        tampered["views"][0]["title"] = "Tampered title"
        with self.assertRaises(KernelError) as context:
            validate_shell_data(tampered)
        self.assertEqual(context.exception.code, "E-SHELL-DATA-DIGEST")

    def test_routes_never_use_implicit_latest(self) -> None:
        payload, _ = build_shell_data(CANONICAL, MANIFEST)
        for state in payload["states"]:
            self.assertTrue(state["route"].startswith("/"))
            self.assertNotIn("latest", state["route"].lower())

    def test_static_html_has_required_landmarks(self) -> None:
        parser = LandmarkParser()
        parser.feed((SHELL / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(parser.lang, "en")
        self.assertIn("header", parser.tags)
        self.assertIn("nav", parser.tags)
        self.assertIn("main", parser.tags)
        self.assertIn("footer", parser.tags)
        self.assertIn("main-content", parser.ids)
        self.assertIn("view-list", parser.ids)
        self.assertIn("view-panel", parser.ids)
        self.assertIn("error-panel", parser.ids)
        self.assertEqual(parser.skip_href, "#main-content")
        self.assertEqual(len(parser.scripts), 1)
        self.assertEqual(parser.scripts[0].get("type"), "module")
        self.assertEqual(parser.scripts[0].get("src"), "./app.js")

    def test_static_assets_are_local_and_safe_by_default(self) -> None:
        for name in ("index.html", "styles.css", "app.js"):
            text = (SHELL / name).read_text(encoding="utf-8")
            self.assertNotIn("https://", text)
            self.assertNotIn("http://", text)
        script = (SHELL / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", script)
        self.assertNotIn("localStorage", script)
        self.assertNotIn("sessionStorage", script)
        self.assertIn("textContent", script)
        self.assertIn("fetch(DATA_URL", script)

    def test_builder_writes_only_replaceable_generated_data(self) -> None:
        payload, report = build_shell_data(CANONICAL, MANIFEST)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data_path = root / "data" / "reference-shell-data.json"
            data_path.parent.mkdir(parents=True)
            data_path.write_text(render_json(payload), encoding="utf-8")
            self.assertTrue(data_path.is_file())
            self.assertTrue(report["replaceable"])
            data_path.unlink()
            self.assertFalse(data_path.exists())
            rebuilt, _ = build_shell_data(CANONICAL, MANIFEST)
            data_path.write_text(render_json(rebuilt), encoding="utf-8")
            self.assertEqual(data_path.read_text(encoding="utf-8"), render_json(payload))


if __name__ == "__main__":
    unittest.main()
