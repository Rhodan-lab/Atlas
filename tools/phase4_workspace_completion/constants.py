#!/usr/bin/env python3
"""Constants and shared helpers for Phase 4 Workstream 3 closure."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from tools.phase2_kernel import KernelError

MODE = "interactive-experience-foundation"
COMPLETION_CONTRACT = "atlas-phase4-workstream3-completion-report/0.1"
COMPLETION_VALIDATION_CONTRACT = "atlas-phase4-workstream3-completion-validation/0.1"
COMPLETION_BASELINE_CONTRACT = "atlas-phase4-workstream3-completion-baseline/0.1"
WORKSPACE_BASELINE_CONTRACT = "atlas-phase4-workspace-contract-baseline/0.1"
SHELL_BASELINE_CONTRACT = "atlas-phase4-workspace-shell-baseline/0.1"
BROWSER_BASELINE_CONTRACT = "atlas-phase4-workspace-browser-baseline/0.1"

ALLOWED_DECISIONS = frozenset({
    "proceed-bounded-workspace-fixture-evaluation",
    "hold-accepted-bounded-workspace",
    "reject-broader-workspace-implementation",
})

EXPECTED_WORKSPACE = {
    "fixture_bytes": 8961,
    "fixture_sha256": "3493c963163a2ba52d6de92fdf8193f9c7f9d7eb967211d7e13ef7b596b24f86",
    "report_bytes": 4186,
    "report_sha256": "41d555a077e63b47da5159e48a5aa37d93bc6cbd149b86baf372ff932b7e5a94",
    "report_digest": "6aec854b297b51b0dde2e65a944453d7af2a8e36b77bd78302cbb0e2f405b402",
    "export_bytes": 11347,
    "export_sha256": "43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a",
    "export_digest": "82f08c18ae76b4b4d091fe0d8be7d54cf5d10d989443132a26e550056af3f56a",
    "manifest_bytes": 1094,
    "manifest_sha256": "8240d78b29f610cb7c566dfad50432473949c5a63b9de9c522ab28751d80fd09",
    "manifest_digest": "9aefaf24b130718f284eecb5502b3c1dd144347f6fdcfc85b47d8ec6ce3fda68",
}

EXPECTED_SHELL = {
    "route_count": 13,
    "entry_route_count": 5,
    "shell_data_bytes": 5955,
    "shell_data_sha256": "a2dd3979c35cee4d081511cadf98499e325dfd22d814cae097cfd3e98f3f5c0c",
    "shell_build_digest": "b4aa3fab14ecc66ee602c9c40dc88b10add23d3391915a72c31968c681edcaee",
    "report_bytes": 1448,
    "report_sha256": "b8b29a61495ecfc420de9324006b6f8efac455905c7b2b69f03639d995e7f932",
    "report_digest": "f1b13c7c202f93a1682d9366fcbef5265a7ae36f335d4e10ddff71ce216e955b",
    "index_bytes": 3232,
    "index_sha256": "ae7eafc4dccae669f25ed4f6e6e5bc8e81bce8dcabcc81b5d585d4d09fb5e921",
}

EXPECTED_BROWSER = {
    "engine": {"name": "chromium", "playwright_version": "1.62.0", "version": "151.0.7922.34"},
    "routes": 13,
    "keyboard_routes": 13,
    "entries": 5,
    "candidates": 2,
    "principia_references": 1,
    "warnings": 1,
    "viewports": 2,
    "external_requests": 0,
    "report_bytes": 2281,
    "report_sha256": "a1f259d1cbfc40d87311a5955e6fe77f932e652b3e8ccfad19d12f629c5103f2",
    "report_digest": "971c44ef7863d313dceffc7356187b94a15d6543e346654cbf6eadc116213311",
}

EXPECTED_BROWSER_EVIDENCE = {
    "workflow": (
        "atlas-workspace-browser-workflow-evidence/0.1",
        8003,
        "c87b3a87aeb4fc97e01af33b08b9475a5fdf65790d972128b13b39eda22a1669",
        "8731d86f49f3a1baf4f52955e1b1bd9de88f7907730e75250205117a0191af59",
    ),
    "accessibility": (
        "atlas-workspace-browser-accessibility-report/0.1",
        990,
        "359cba535d1051dd90b2ce03e3a1932eec17c9b3adabd95bbf6b5a8633eae5e5",
        "c3047168d5e9a737452c69babf000caa7d2c2a89ae267127d1426296a921bf57",
    ),
    "network": (
        "atlas-workspace-browser-network-report/0.1",
        17517,
        "110e7baa552e0a41c0912ff116c79d51e6e4b6d68bf77f1080f18587e4d0a9cd",
        "1de7665443a296e1b81443d8fce8021640e0aaf52807259ced0bd52932cb490d",
    ),
    "failure": (
        "atlas-workspace-browser-failure-evidence/0.1",
        1145,
        "b41c10299e0b3998f4d3c5db6d59972f57f38fd2f47cb4105a67683b657f4bcb",
        "205915d16f6cf5009b04fb3cf404813d49bbdd35fba1640b174d4bc118d2603d",
    ),
    "manifest": (
        "atlas-phase4-workspace-browser-manifest/0.1",
        2688,
        "1515b645b7608ae26391f19c231169bc0567d6f5bdf518f8649119bbc5590e2e",
        "ef7a22a6be1f8c46b706b894bc44a10ae88a75b2e4a8e72695d9726e373f0131",
    ),
    "report": (
        "atlas-phase4-workspace-browser-report/0.1",
        2281,
        "a1f259d1cbfc40d87311a5955e6fe77f932e652b3e8ccfad19d12f629c5103f2",
        "971c44ef7863d313dceffc7356187b94a15d6543e346654cbf6eadc116213311",
    ),
}


def json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _require(record: Mapping[str, Any], field: str, expected: Any, code: str) -> None:
    if record.get(field) != expected:
        raise KernelError(code, f"expected {field}={expected!r}")


def _require_mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def _require_artifact(
    record: Mapping[str, Any],
    *,
    expected_bytes: int,
    expected_sha256: str,
    code: str,
) -> None:
    artifact = _require_mapping(record.get("artifact"), code, "artifact identity is required")
    _require(artifact, "bytes", expected_bytes, code)
    _require(artifact, "sha256", expected_sha256, code)
