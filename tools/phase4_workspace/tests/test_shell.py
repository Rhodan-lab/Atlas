from __future__ import annotations

import copy
import hashlib
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from tools.phase2_kernel import KernelError, load_json, render_json
from tools.phase4_workspace.build_shell import (
    SHELL_BUILD_REPORT_CONTRACT,
    SHELL_DATA_CONTRACT,
    build_workspace_shell,
    validate_shell_data,
)

ROOT = Path(__file__).resolve().parents[3]
CANONICAL = ROOT / "content" / "canonical"
FIXTURE = ROOT / "content" / "fixtures" / "phase4_workspace" / "research-workspace.v01.json"
RESEARCH_FIXTURE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "research-foundations.v01.json"
RESEARCH_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "research-foundations-baseline.json"
STRUCTURED_BASELINE = ROOT / "content" / "fixtures" / "phase3_retrieval" / "structured-baseline.json"
BRIDGE_FIXTURE = ROOT / "content" / "fixtures" / "phase4_interaction" / "bridge-failures.v01.json"
WORKSPACE_BASELINE = ROOT / "content" / "fixtures" / "phase4_workspace" / "workspace-contract-baseline.json"
SHELL = ROOT / "apps" / "workspace-shell"


class ShellHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lang = None
        self.tags: list[str] = []
        self.ids: set[str] = set()
        self.skip_href = None
        self.scripts: list[dict[str, str | None]] = []
        self.buttons: list[dict[str, str | None]] = []

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
        if tag == "button":
            self.buttons.append(values)


class Phase4WorkspaceShellTests(unittest.TestCase):
    def _build(self):
        return build_workspace_shell(
            CANONICAL,
            FIXTURE,
            RESEARCH_FIXTURE,
            RESEARCH_BASELINE,
            STRUCTURED_BASELINE,
            BRIDGE_FIXTURE,
            WORKSPACE_BASELINE,
        )

    def test_build_is_deterministic_and_valid(self) -> None:
        first = self._build()
        second = self._build()
        first_data, first_report, first_export, first_manifest, _ = first
        second_data, second_report, second_export, second_manifest, _ = second
        self.assertEqual(render_json(first_data), render_json(second_data))
        self.assertEqual(render_json(first_report), render_json(second_report))
        self.assertEqual(render_json(first_export), render_json(second_export))
        self.assertEqual(render_json(first_manifest), render_json(second_manifest))
        validation = validate_shell_data(first_data)
        self.assertEqual(first_data["contract"], SHELL_DATA_CONTRACT)
        self.assertEqual(first_report["contract"], SHELL_BUILD_REPORT_CONTRACT)
        self.assertEqual(validation["decision"], "valid")
        self.assertEqual(validation["route_count"], 13)
        self.assertEqual(validation["entry_route_count"], 5)
        self.assertEqual(first_data["counts"]["entries"], 5)
        self.assertEqual(first_data["counts"]["candidates"], 2)
        self.assertEqual(first_data["counts"]["principia_references"], 1)
        self.assertEqual(first_data["counts"]["warnings"], 1)
        self.assertTrue(first_report["replaceable"])
        self.assertTrue(first_report["local_first"])
        self.assertFalse(first_report["api_required"])
        self.assertFalse(first_report["account_required"])
        self.assertFalse(first_report["cloud_required"])
        self.assertFalse(first_report["external_network_required"])
        self.assertFalse(first_report["canonical_mutation"])
        self.assertFalse(first_report["repository_mutation"])

    def test_routes_preserve_exact_order_and_decisions(self) -> None:
        shell_data, _, export, _, _ = self._build()
        entry_routes = [route for route in shell_data["routes"] if route["kind"] == "entry"]
        self.assertEqual([route["position"] for route in entry_routes], [1, 2, 3, 4, 5])
        self.assertEqual(
            [route["decision"] for route in entry_routes],
            [entry["decision"]["action"] for entry in export["entries"]],
        )
        self.assertEqual(
            [route["exact_reference"] for route in entry_routes],
            [entry["exact_reference"] for entry in export["entries"]],
        )
        for route in shell_data["routes"]:
            self.assertTrue(route["hash"].startswith("#"))
            self.assertNotIn("latest", route["hash"].lower())

    def test_shell_digest_tampering_is_rejected(self) -> None:
        shell_data, _, _, _, _ = self._build()
        tampered = copy.deepcopy(shell_data)
        tampered["routes"][0]["label"] = "Tampered overview"
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-SHELL-DIGEST"):
            validate_shell_data(tampered)

    def test_unsafe_authority_is_rejected_after_resealing(self) -> None:
        shell_data, _, _, _, _ = self._build()
        tampered = copy.deepcopy(shell_data)
        tampered["authority"]["canonical_mutation"] = True
        unsigned = copy.deepcopy(tampered)
        unsigned.pop("build_digest")
        import json
        payload = json.dumps(unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        tampered["build_digest"] = hashlib.sha256(payload).hexdigest()
        with self.assertRaisesRegex(KernelError, "E-WORKSPACE-SHELL-AUTHORITY"):
            validate_shell_data(tampered)

    def test_static_html_has_required_semantics(self) -> None:
        parser = ShellHTMLParser()
        parser.feed((SHELL / "index.html").read_text(encoding="utf-8"))
        self.assertEqual(parser.lang, "en")
        for tag in ("header", "nav", "main", "footer"):
            self.assertIn(tag, parser.tags)
        for element_id in (
            "main-content",
            "overview",
            "route-list",
            "authority-summary",
            "download-export",
            "loading-panel",
            "content-panel",
            "error-panel",
        ):
            self.assertIn(element_id, parser.ids)
        self.assertEqual(parser.skip_href, "#overview")
        self.assertEqual(len(parser.scripts), 1)
        self.assertEqual(parser.scripts[0].get("type"), "module")
        self.assertEqual(parser.scripts[0].get("src"), "./app.js")
        download = next(button for button in parser.buttons if button.get("id") == "download-export")
        self.assertEqual(download.get("type"), "button")
        self.assertIn("disabled", download)

    def test_static_assets_are_local_and_non_authoritative(self) -> None:
        for name in ("index.html", "styles.css", "app.js"):
            text = (SHELL / name).read_text(encoding="utf-8")
            self.assertNotIn("https://", text)
            self.assertNotIn("http://", text)
        script = (SHELL / "app.js").read_text(encoding="utf-8")
        self.assertNotIn("innerHTML", script)
        self.assertNotIn("localStorage", script)
        self.assertNotIn("sessionStorage", script)
        self.assertNotIn("WebSocket", script)
        self.assertNotIn("EventSource", script)
        self.assertIn("fetch(DATA_URLS.shell", script)
        self.assertIn("new Blob([exportBytes]", script)
        self.assertIn("URL.createObjectURL", script)
        self.assertIn("history.replaceState", script)
        self.assertIn("No fallback", (SHELL / "README.md").read_text(encoding="utf-8") or "No fallback")

    def test_builder_writes_exact_accepted_export(self) -> None:
        shell_data, report, export, manifest, _ = self._build()
        baseline = load_json(WORKSPACE_BASELINE)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data"
            data.mkdir(parents=True)
            shell_path = data / "workspace-shell-data.json"
            export_path = data / "workspace-export.json"
            manifest_path = data / "workspace-manifest.json"
            report_path = root / "workspace-shell-report.json"
            shell_path.write_text(render_json(shell_data), encoding="utf-8")
            export_path.write_text(render_json(export), encoding="utf-8")
            manifest_path.write_text(render_json(manifest), encoding="utf-8")
            report_path.write_text(render_json(report), encoding="utf-8")
            self.assertEqual(len(export_path.read_bytes()), baseline["export"]["artifact"]["bytes"])
            self.assertEqual(
                hashlib.sha256(export_path.read_bytes()).hexdigest(),
                baseline["export"]["artifact"]["sha256"],
            )
            self.assertEqual(len(manifest_path.read_bytes()), baseline["manifest"]["artifact"]["bytes"])
            self.assertEqual(
                hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
                baseline["manifest"]["artifact"]["sha256"],
            )
            self.assertTrue(shell_path.is_file())
            self.assertTrue(report_path.is_file())


if __name__ == "__main__":
    unittest.main()
