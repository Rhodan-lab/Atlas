#!/usr/bin/env python3
"""Build two deterministic packages over the unchanged accepted workspace reader."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path
from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase4_workspace.build_shell import (
    _artifact,
    _routes,
    _seal,
    build_workspace_shell,
    validate_shell_data,
)
from tools.phase4_workspace_generalization.fixture import build_fixture
from tools.phase4_workspace_generalization.report import validate_generalization_bundle

PACKAGE_CONTRACT = "atlas-phase4-workspace-reader-reuse-package/0.1"
REPORT_CONTRACT = "atlas-phase4-workspace-reader-reuse-report/0.1"
VALIDATION_CONTRACT = "atlas-phase4-workspace-reader-reuse-validation/0.1"
MODE = "interactive-experience-foundation"
STATIC_ASSETS = ("index.html", "styles.css", "app.js")
PACKAGE_IDS = ("recommender", "catalase")
PROHIBITED_SELECTOR_TEXT = (
    "localStorage",
    "sessionStorage",
    "https://",
    "http://",
    "credential",
    "token",
    "api_key",
)

SELECTOR_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Atlas Research Workspace Packages</title>
  <link rel="stylesheet" href="./selector.css">
  <script src="./selector.js" defer></script>
</head>
<body>
  <a class="skip-link" href="#package-selection">Skip to package selection</a>
  <header>
    <p class="eyebrow">ATLAS · LOCAL READER REUSE</p>
    <h1>Choose one accepted research package</h1>
    <p>Both packages use the same static reader assets. Selection changes only the pinned local data package.</p>
  </header>
  <main id="package-selection" tabindex="-1">
    <section aria-labelledby="selection-title">
      <h2 id="selection-title">Available fixtures</h2>
      <ul class="package-list">
        <li>
          <a data-fixture="recommender" href="./packages/recommender/index.html#overview">
            <strong>Recommender-system reference package</strong>
            <span>Accepted Workstream 3 regression baseline.</span>
          </a>
        </li>
        <li>
          <a data-fixture="catalase" href="./packages/catalase/index.html#overview">
            <strong>Catalase assay-methodology package</strong>
            <span>Accepted Workstream 4 Slice 1 fixture.</span>
          </a>
        </li>
      </ul>
    </section>
    <section id="selector-status" class="status" role="status" aria-live="polite"></section>
    <section id="selector-error" class="error" role="alert" hidden>
      <h2>Workspace fixture unavailable</h2>
      <p>The requested fixture is not in the accepted package index. Silent fallback is refused.</p>
      <dl>
        <div><dt>Requested fixture</dt><dd id="requested-fixture"></dd></div>
        <div><dt>Fallback</dt><dd>refused</dd></div>
        <div><dt>Package mutation</dt><dd>none</dd></div>
      </dl>
      <a href="./index.html">Return to package selection</a>
    </section>
  </main>
</body>
</html>
"""

SELECTOR_JS = """const ACCEPTED_FIXTURES = new Map([
  ["recommender", "./packages/recommender/index.html#overview"],
  ["catalase", "./packages/catalase/index.html#overview"],
]);

const params = new URLSearchParams(window.location.search);
const requested = params.get("fixture");
const status = document.querySelector("#selector-status");
const error = document.querySelector("#selector-error");
const requestedOutput = document.querySelector("#requested-fixture");

if (requested === null) {
  status.textContent = "No fixture preselected · choose one accepted local package.";
} else if (ACCEPTED_FIXTURES.has(requested)) {
  const link = document.querySelector(`[data-fixture="${CSS.escape(requested)}"]`);
  status.textContent = `Accepted fixture selected: ${requested}. Activate the matching package link to continue.`;
  link?.focus();
} else {
  document.querySelector(".package-list").hidden = true;
  requestedOutput.textContent = requested || "(empty)";
  error.hidden = false;
  status.textContent = "Unknown fixture rejected · no fallback package loaded.";
  error.querySelector("a")?.focus();
}
"""

SELECTOR_CSS = """:root {
  color-scheme: light;
  font-family: Inter, ui-sans-serif, system-ui, sans-serif;
  background: #f3f1eb;
  color: #171a1f;
}
* { box-sizing: border-box; }
body { margin: 0; min-height: 100vh; }
.skip-link { position: absolute; left: 1rem; top: -5rem; padding: .75rem 1rem; background: white; z-index: 2; }
.skip-link:focus { top: 1rem; }
header, main { width: min(58rem, calc(100% - 2rem)); margin-inline: auto; }
header { padding: 5rem 0 2rem; border-bottom: 1px solid #b6b1a6; }
main { padding: 2rem 0 5rem; }
.eyebrow { letter-spacing: .16em; font-size: .78rem; font-weight: 700; }
h1 { max-width: 18ch; font-size: clamp(2.2rem, 7vw, 4.8rem); line-height: .98; }
.package-list { display: grid; gap: 1rem; padding: 0; list-style: none; }
.package-list a { display: grid; gap: .4rem; padding: 1.25rem; border: 1px solid #8e887b; background: #fff; color: inherit; text-decoration: none; }
.package-list a:hover, .package-list a:focus-visible { outline: 3px solid currentColor; outline-offset: 3px; }
.package-list span { color: #4d514f; }
.status, .error { margin-top: 1.5rem; padding: 1rem; border-left: .35rem solid #555b57; background: #fff; }
.error { border-left-color: #8b2c20; }
dl div { display: grid; grid-template-columns: minmax(8rem, 12rem) 1fr; gap: 1rem; padding-block: .35rem; }
dt { font-weight: 700; }
dd { margin: 0; overflow-wrap: anywhere; }
@media (max-width: 36rem) {
  header { padding-top: 4rem; }
  dl div { grid-template-columns: 1fr; gap: .15rem; }
}
@media (prefers-reduced-motion: reduce) {
  * { scroll-behavior: auto !important; }
}
"""


def _sha(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _verify_artifact(record: Mapping[str, Any], payload: bytes, code: str, label: str) -> None:
    expected = record.get("artifact") if isinstance(record.get("artifact"), Mapping) else record
    _require(isinstance(expected, Mapping), code, f"{label} identity is missing")
    if expected.get("bytes") is not None:
        _require(expected.get("bytes") == len(payload), code, f"{label} byte length differs from accepted baseline")
    _require(expected.get("sha256") == _sha(payload), code, f"{label} SHA-256 differs from accepted baseline")


def _verify_generalization_baseline(
    baseline: Mapping[str, Any],
    fixture: Mapping[str, Any],
    report: Mapping[str, Any],
    core_report: Mapping[str, Any],
    export: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> dict[str, bytes]:
    _require(
        baseline.get("contract") == "atlas-phase4-workspace-generalization-baseline/0.1",
        "E-READER-REUSE-CATALASE-BASELINE",
        "Catalase baseline contract mismatch",
    )
    rendered = {
        "fixture": render_json(fixture).encode("utf-8"),
        "report": render_json(report).encode("utf-8"),
        "workspace_contract_report": render_json(core_report).encode("utf-8"),
        "export": render_json(export).encode("utf-8"),
        "manifest": render_json(manifest).encode("utf-8"),
    }
    records = {
        "report": report,
        "workspace_contract_report": core_report,
        "export": export,
        "manifest": manifest,
    }
    for name, payload in rendered.items():
        _verify_artifact(baseline[name], payload, "E-READER-REUSE-CATALASE-BASELINE", f"Catalase {name}")
        if name != "fixture":
            _require(
                baseline[name].get("report_digest") == records[name].get("report_digest"),
                "E-READER-REUSE-CATALASE-BASELINE",
                f"Catalase {name} semantic digest differs",
            )
    return rendered


def _verify_static_assets(
    source_dir: Path,
    shell_baseline: Mapping[str, Any],
) -> dict[str, bytes]:
    static_baseline = shell_baseline.get("static_assets")
    _require(isinstance(static_baseline, Mapping), "E-READER-REUSE-STATIC", "accepted static asset baseline is missing")
    assets: dict[str, bytes] = {}
    for name in STATIC_ASSETS:
        payload = (source_dir / name).read_bytes()
        expected = static_baseline.get(name)
        _require(isinstance(expected, Mapping), "E-READER-REUSE-STATIC", f"accepted identity missing for {name}")
        _require(expected.get("bytes") == len(payload), "E-READER-REUSE-STATIC", f"{name} byte length drift")
        _require(expected.get("sha256") == _sha(payload), "E-READER-REUSE-STATIC", f"{name} SHA-256 drift")
        assets[name] = payload
    return assets


def _shell_data_from_export(export: Mapping[str, Any], manifest: Mapping[str, Any]) -> dict[str, Any]:
    export_bytes = render_json(export).encode("utf-8")
    manifest_bytes = render_json(manifest).encode("utf-8")
    routes = _routes(export)
    shell_data = _seal({
        "contract": "atlas-workspace-shell-data/0.1",
        "mode": MODE,
        "phase": 4,
        "workstream": 3,
        "slice": 2,
        "state": "workspace-shell-candidate",
        "source_digest": export["source_digest"],
        "workspace": dict(export["workspace"]),
        "accepted_export": {
            "contract": export["contract"],
            "artifact": _artifact(export_bytes),
            "report_digest": export["report_digest"],
            "file": "data/workspace-export.json",
        },
        "accepted_manifest": {
            "contract": manifest["contract"],
            "artifact": _artifact(manifest_bytes),
            "report_digest": manifest["report_digest"],
            "file": "data/workspace-manifest.json",
        },
        "routes": routes,
        "counts": {
            "routes": len(routes),
            "entries": len(export["entries"]),
            "candidates": len(export["candidate_references"]),
            "principia_references": len(export["principia_references"]),
            "warnings": len(export["warning_references"]),
            "open_questions": len(export["open_questions"]),
            "limitations": len(export["limitations"]),
        },
        "download": {
            "file": "workspace-export.json",
            "bytes": len(export_bytes),
            "sha256": _sha(export_bytes),
            "local_only": True,
            "canonical_write": False,
        },
        "authority": {
            "workspace_authority": "ephemeral-research-only",
            "browser_state_authority": "ephemeral-only",
            "accepted_export_only": True,
            "exact_revision_required": True,
            "entry_order_preserved": True,
            "decisions_read_only": True,
            "candidates_unresolved": True,
            "principia_status_separate": True,
            "keyboard_workflow_required": True,
            "non_graph_workflow_required": True,
            "reduced_motion_required": True,
            "zero_external_requests_required": True,
            "canonical_mutation": False,
            "lifecycle_mutation": False,
            "review_mutation": False,
            "repository_mutation": False,
            "production_frontend_architecture_selected": False,
            "live_principia_dependency": False,
        },
    })
    validate_shell_data(shell_data)
    return shell_data


def _write_package(
    target: Path,
    assets: Mapping[str, bytes],
    shell_data: Mapping[str, Any],
    export: Mapping[str, Any],
    manifest: Mapping[str, Any],
) -> dict[str, Any]:
    target.mkdir(parents=True, exist_ok=True)
    data_dir = target / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    for name, payload in assets.items():
        (target / name).write_bytes(payload)
    records = {
        "workspace-shell-data.json": shell_data,
        "workspace-export.json": export,
        "workspace-manifest.json": manifest,
    }
    data_identities: dict[str, Any] = {}
    for name, record in records.items():
        payload = render_json(record).encode("utf-8")
        (data_dir / name).write_bytes(payload)
        data_identities[name] = {
            "bytes": len(payload),
            "sha256": _sha(payload),
            "contract": record.get("contract"),
            "report_digest": record.get("report_digest") or record.get("build_digest"),
        }
    return {
        "workspace": dict(export["workspace"]),
        "reader_assets": {
            name: {"bytes": len(payload), "sha256": _sha(payload)}
            for name, payload in sorted(assets.items())
        },
        "data": data_identities,
    }


def validate_package_index(index: Mapping[str, Any]) -> dict[str, Any]:
    _require(index.get("contract") == PACKAGE_CONTRACT, "E-READER-REUSE-PACKAGE", f"expected {PACKAGE_CONTRACT!r}")
    _require(
        index.get("phase") == 4
        and index.get("workstream") == 4
        and index.get("slice") == 2
        and index.get("state") == "reader-reuse-package-candidate",
        "E-READER-REUSE-PACKAGE",
        "package scope mismatch",
    )
    fixtures = index.get("fixtures")
    _require(isinstance(fixtures, list) and len(fixtures) == 2, "E-READER-REUSE-FIXTURE", "exactly two indexed packages are required")
    ids = [item.get("id") for item in fixtures if isinstance(item, Mapping)]
    _require(ids == list(PACKAGE_IDS), "E-READER-REUSE-FIXTURE", "fixture order or identity differs")
    reader_hashes = [
        tuple(sorted((name, record.get("sha256")) for name, record in item["reader_assets"].items()))
        for item in fixtures
    ]
    _require(reader_hashes[0] == reader_hashes[1], "E-READER-REUSE-STATIC", "both packages must reuse byte-identical reader assets")
    selector = index.get("selector")
    _require(isinstance(selector, Mapping), "E-READER-REUSE-SELECTOR", "selector identity is required")
    _require(selector.get("unknown_fixture_fallback") == "refused", "E-READER-REUSE-FALLBACK", "unknown fixture fallback must be refused")
    authority = index.get("authority")
    _require(isinstance(authority, Mapping), "E-READER-REUSE-AUTHORITY", "authority block is required")
    for field, expected in {
        "workspace_authority": "ephemeral-research-only",
        "browser_state_authority": "ephemeral-only",
        "existing_reader_assets_only": True,
        "second_generalized_fixture_authorized": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "candidate_resolution_authorized": False,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "repository_mutation": False,
    }.items():
        _require(authority.get(field) == expected, "E-READER-REUSE-AUTHORITY", f"package requires {field}={expected!r}")
    digest = index.get("report_digest")
    _require(isinstance(digest, str) and len(digest) == 64, "E-READER-REUSE-DIGEST", "package digest is required")
    unsigned = dict(index)
    unsigned.pop("report_digest", None)
    encoded = json.dumps(unsigned, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    _require(_sha(encoded) == digest, "E-READER-REUSE-DIGEST", "package digest mismatch")
    return {
        "contract": VALIDATION_CONTRACT,
        "decision": "valid-reader-reuse-package-candidate",
        "fixture_count": 2,
        "reader_asset_count": len(STATIC_ASSETS),
        "report_digest": digest,
        "browser_evidence_included": False,
        "live": False,
        "repository_mutation": False,
    }


def build_reader_reuse_package(
    repository_root: Path,
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    canonical_root = repository_root / "content/canonical"
    repository = KernelRepository(compile_canonical(canonical_root))
    static_source = repository_root / "apps/workspace-shell"
    shell_baseline = load_json(repository_root / "content/fixtures/phase4_workspace/workspace-shell-baseline.json")
    assets = _verify_static_assets(static_source, shell_baseline)

    recommender_shell, recommender_build_report, recommender_export, recommender_manifest, _ = build_workspace_shell(
        canonical_root,
        repository_root / "content/fixtures/phase4_workspace/research-workspace.v01.json",
        repository_root / "content/fixtures/phase3_retrieval/research-foundations.v01.json",
        repository_root / "content/fixtures/phase3_retrieval/research-foundations-baseline.json",
        repository_root / "content/fixtures/phase3_retrieval/structured-baseline.json",
        repository_root / "content/fixtures/phase4_interaction/bridge-failures.v01.json",
        repository_root / "content/fixtures/phase4_workspace/workspace-contract-baseline.json",
    )
    recommender_shell_bytes = render_json(recommender_shell).encode("utf-8")
    recommender_report_bytes = render_json(recommender_build_report).encode("utf-8")
    _verify_artifact(shell_baseline["shell_data"], recommender_shell_bytes, "E-READER-REUSE-RECOMMENDER", "recommender shell data")
    _verify_artifact(shell_baseline["build_report"], recommender_report_bytes, "E-READER-REUSE-RECOMMENDER", "recommender build report")

    catalase_fixture = build_fixture()
    catalase_report, catalase_core_report, catalase_export, catalase_manifest = validate_generalization_bundle(
        catalase_fixture,
        repository,
    )
    catalase_baseline = load_json(
        repository_root / "content/fixtures/phase4_workspace_generalization/catalase-generalization-baseline.json"
    )
    _verify_generalization_baseline(
        catalase_baseline,
        catalase_fixture,
        catalase_report,
        catalase_core_report,
        catalase_export,
        catalase_manifest,
    )
    catalase_shell = _shell_data_from_export(catalase_export, catalase_manifest)

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    selector_assets = {
        "index.html": SELECTOR_HTML.encode("utf-8"),
        "selector.js": SELECTOR_JS.encode("utf-8"),
        "selector.css": SELECTOR_CSS.encode("utf-8"),
    }
    for name, payload in selector_assets.items():
        _require(
            not any(token in payload.decode("utf-8") for token in PROHIBITED_SELECTOR_TEXT),
            "E-READER-REUSE-SELECTOR",
            f"selector contains prohibited text in {name}",
        )
        (output_dir / name).write_bytes(payload)

    recommender_identity = _write_package(
        output_dir / "packages/recommender",
        assets,
        recommender_shell,
        recommender_export,
        recommender_manifest,
    )
    catalase_identity = _write_package(
        output_dir / "packages/catalase",
        assets,
        catalase_shell,
        catalase_export,
        catalase_manifest,
    )
    recommender_identity.update({
        "id": "recommender",
        "label": "Recommender-system reference package",
        "accepted_baseline": "atlas-phase4-workspace-shell-baseline/0.1",
        "path": "packages/recommender/index.html#overview",
    })
    catalase_identity.update({
        "id": "catalase",
        "label": "Catalase assay-methodology package",
        "accepted_baseline": "atlas-phase4-workspace-generalization-baseline/0.1",
        "path": "packages/catalase/index.html#overview",
    })

    index = _seal({
        "contract": PACKAGE_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 2,
        "state": "reader-reuse-package-candidate",
        "fixtures": [recommender_identity, catalase_identity],
        "selector": {
            "default": "selection-only",
            "known_fixtures": list(PACKAGE_IDS),
            "unknown_fixture_fallback": "refused",
            "assets": {
                name: {"bytes": len(payload), "sha256": _sha(payload)}
                for name, payload in sorted(selector_assets.items())
            },
        },
        "regression": {
            "recommender_shell_build_digest": recommender_shell["build_digest"],
            "recommender_shell_report_digest": recommender_build_report["report_digest"],
            "catalase_generalization_report_digest": catalase_report["report_digest"],
            "catalase_workspace_export_digest": catalase_export["report_digest"],
            "accepted_reader_assets_byte_identical": True,
        },
        "authority": {
            "workspace_authority": "ephemeral-research-only",
            "browser_state_authority": "ephemeral-only",
            "existing_reader_assets_only": True,
            "second_generalized_fixture_authorized": False,
            "canonical_mutation": False,
            "lifecycle_mutation": False,
            "review_mutation": False,
            "candidate_resolution_authorized": False,
            "account_required": False,
            "cloud_required": False,
            "external_network_required": False,
            "production_frontend_architecture_selected": False,
            "live_principia_dependency": False,
            "repository_mutation": False,
        },
        "browser_evidence_included": False,
        "implementation_authorized_beyond_local_package": False,
        "live": False,
        "repository_mutation": False,
    }, field="report_digest")
    validation = validate_package_index(index)
    (output_dir / "package-index.json").write_bytes(render_json(index).encode("utf-8"))

    report = _seal({
        "contract": REPORT_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 2,
        "state": "reader-reuse-package-candidate",
        "decision": "reader-reuse-package-candidate",
        "package_index_digest": index["report_digest"],
        "counts": {
            "fixture_packages": 2,
            "generalized_fixtures": 1,
            "reader_assets_per_package": len(STATIC_ASSETS),
            "routes_per_package": 13,
            "entries_per_package": 5,
        },
        "static_gates": {
            "slice1_baseline_verified": True,
            "recommender_shell_baseline_preserved": True,
            "reader_assets_byte_identical": True,
            "same_shell_data_contract_used": True,
            "selector_unknown_fixture_fallback_refused": True,
            "packages_deterministically_addressable": True,
            "all_write_and_production_authority_frozen": True,
            "browser_evidence_pending": True,
        },
        "browser_evidence_included": False,
        "slice2_recommendation_issued": False,
        "next_required_evidence": "pinned-chromium-reader-reuse-evidence",
        "authority": dict(index["authority"]),
        "limitations": [
            "This candidate proves deterministic static packaging only; it does not yet claim real-browser behavior.",
            "The selector is local fixture-selection plumbing, not a new reader or frontend architecture.",
            "The accepted recommender package remains the rollback state.",
            "The Catalase package is the only generalized fixture.",
        ],
        "live": False,
        "repository_mutation": False,
    }, field="report_digest")
    (output_dir / "reader-reuse-report.json").write_bytes(render_json(report).encode("utf-8"))
    (output_dir / "reader-reuse-validation.json").write_bytes(render_json(validation).encode("utf-8"))
    return index, report, validation
