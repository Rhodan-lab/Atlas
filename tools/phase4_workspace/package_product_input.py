#!/usr/bin/env python3
"""Build and verify Atlas input for the unified Principia & Atlas product."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, render_json
from tools.phase4_workspace import build_shell

REPO_ROOT = Path(__file__).resolve().parents[2]
STATIC_ROOT = REPO_ROOT / "apps" / "workspace-shell"
REPORT_NAME = "workspace-shell-build-report.json"
STATIC_FILES = ("index.html", "styles.css", "app.js", "README.md")
GENERATED_FILES = (
    "data/workspace-shell-data.json",
    "data/workspace-export.json",
    "data/workspace-manifest.json",
)
PACKAGE_FILES = STATIC_FILES + GENERATED_FILES + (REPORT_NAME,)
MAX_FILE_BYTES = 16 * 1024 * 1024


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _json_digest(value: Mapping[str, Any], field: str) -> str:
    unsigned = dict(value)
    unsigned.pop(field, None)
    payload = json.dumps(
        unsigned,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return _sha256(payload)


def _read_regular(path: Path, label: str) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise KernelError("E-PRODUCT-INPUT-FILE", f"{label} must be a regular file")
    payload = path.read_bytes()
    if len(payload) > MAX_FILE_BYTES:
        raise KernelError("E-PRODUCT-INPUT-SIZE", f"{label} exceeds the byte limit")
    return payload


def _load_object(payload: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise KernelError("E-PRODUCT-INPUT-JSON", f"{label} is not valid UTF-8 JSON") from exc
    if not isinstance(value, dict):
        raise KernelError("E-PRODUCT-INPUT-JSON", f"{label} must be a JSON object")
    return value


def _actual_files(root: Path) -> set[str]:
    if root.is_symlink() or not root.is_dir():
        raise KernelError("E-PRODUCT-INPUT-DIR", "product input must be a regular directory")
    files: set[str] = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            raise KernelError(
                "E-PRODUCT-INPUT-SYMLINK",
                f"product input entry must not be a symlink: {relative}",
            )
        if path.is_dir():
            continue
        if not path.is_file():
            raise KernelError(
                "E-PRODUCT-INPUT-FILE",
                f"product input entry must be regular: {relative}",
            )
        files.add(relative)
    return files


def _default_inputs() -> tuple[Path, Path, Path, Path, Path, Path, Path]:
    return (
        REPO_ROOT / "content" / "canonical",
        REPO_ROOT / "content" / "fixtures" / "phase4_workspace" / "research-workspace.v01.json",
        REPO_ROOT / "content" / "fixtures" / "phase3_retrieval" / "research-foundations.v01.json",
        REPO_ROOT / "content" / "fixtures" / "phase3_retrieval" / "research-foundations-baseline.json",
        REPO_ROOT / "content" / "fixtures" / "phase3_retrieval" / "structured-baseline.json",
        REPO_ROOT / "content" / "fixtures" / "phase4_interaction" / "bridge-failures.v01.json",
        REPO_ROOT / "content" / "fixtures" / "phase4_workspace" / "workspace-contract-baseline.json",
    )


def verify_product_input(
    root: Path,
    *,
    static_root: Path = STATIC_ROOT,
) -> dict[str, Any]:
    actual = _actual_files(root)
    expected = set(PACKAGE_FILES)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise KernelError(
            "E-PRODUCT-INPUT-SHAPE",
            f"product input file set differs: missing={missing}, extra={extra}",
        )

    package_bytes = {
        relative: _read_regular(root / relative, f"product input {relative}")
        for relative in PACKAGE_FILES
    }
    for relative in STATIC_FILES:
        source = _read_regular(static_root / relative, f"Atlas source {relative}")
        if package_bytes[relative] != source:
            raise KernelError(
                "E-PRODUCT-INPUT-STATIC",
                f"product input static asset differs from Atlas source: {relative}",
            )

    shell = _load_object(package_bytes[GENERATED_FILES[0]], "workspace shell data")
    export = _load_object(package_bytes[GENERATED_FILES[1]], "workspace export")
    manifest = _load_object(package_bytes[GENERATED_FILES[2]], "workspace manifest")
    report = _load_object(package_bytes[REPORT_NAME], "workspace shell report")
    build_shell.validate_shell_data(shell)

    if report.get("contract") != build_shell.SHELL_BUILD_REPORT_CONTRACT:
        raise KernelError("E-PRODUCT-INPUT-REPORT", "workspace shell report contract mismatch")
    report_digest = report.get("report_digest")
    if not isinstance(report_digest, str) or _json_digest(report, "report_digest") != report_digest:
        raise KernelError("E-PRODUCT-INPUT-REPORT", "workspace shell report digest mismatch")
    if report.get("static_assets") != list(STATIC_FILES[:3]):
        raise KernelError("E-PRODUCT-INPUT-REPORT", "workspace shell static asset list mismatch")
    if report.get("generated_files") != list(GENERATED_FILES):
        raise KernelError("E-PRODUCT-INPUT-REPORT", "workspace shell generated file list mismatch")
    if report.get("shell_build_digest") != shell.get("build_digest"):
        raise KernelError("E-PRODUCT-INPUT-BINDING", "shell build digest is not report-bound")
    if report.get("export_digest") != export.get("report_digest"):
        raise KernelError("E-PRODUCT-INPUT-BINDING", "export digest is not report-bound")
    if report.get("manifest_digest") != manifest.get("report_digest"):
        raise KernelError("E-PRODUCT-INPUT-BINDING", "manifest digest is not report-bound")
    workspace = shell.get("workspace")
    if not isinstance(workspace, Mapping):
        raise KernelError("E-PRODUCT-INPUT-WORKSPACE", "workspace identity is missing")
    if export.get("workspace") != workspace:
        raise KernelError("E-PRODUCT-INPUT-WORKSPACE", "workspace identity differs across artifacts")
    if report.get("workspace_id") != workspace.get("id"):
        raise KernelError("E-PRODUCT-INPUT-WORKSPACE", "workspace ID is not report-bound")
    if report.get("workspace_revision") != workspace.get("revision"):
        raise KernelError("E-PRODUCT-INPUT-WORKSPACE", "workspace revision is not report-bound")

    for key, relative in (
        ("accepted_export", GENERATED_FILES[1]),
        ("accepted_manifest", GENERATED_FILES[2]),
    ):
        accepted = shell.get(key)
        artifact = accepted.get("artifact") if isinstance(accepted, Mapping) else None
        payload = package_bytes[relative]
        if not isinstance(artifact, Mapping):
            raise KernelError("E-PRODUCT-INPUT-BINDING", f"{key} artifact identity is missing")
        if artifact.get("bytes") != len(payload) or artifact.get("sha256") != _sha256(payload):
            raise KernelError("E-PRODUCT-INPUT-BINDING", f"{key} artifact identity mismatch")

    authority = shell.get("authority")
    if not isinstance(authority, Mapping):
        raise KernelError("E-PRODUCT-INPUT-AUTHORITY", "workspace authority is missing")
    required_false = (
        "canonical_mutation",
        "lifecycle_mutation",
        "review_mutation",
        "repository_mutation",
        "production_frontend_architecture_selected",
        "live_principia_dependency",
    )
    if any(authority.get(field) is not False for field in required_false):
        raise KernelError("E-PRODUCT-INPUT-AUTHORITY", "workspace authority boundary was relaxed")
    if authority.get("principia_status_separate") is not True:
        raise KernelError("E-PRODUCT-INPUT-AUTHORITY", "Principia status must remain separate")
    if authority.get("zero_external_requests_required") is not True:
        raise KernelError("E-PRODUCT-INPUT-AUTHORITY", "zero external requests must remain required")
    if any(report.get(field) is not False for field in (
        "external_network_required",
        "canonical_mutation",
        "repository_mutation",
        "production_frontend_architecture_selected",
        "live_principia_dependency",
    )):
        raise KernelError("E-PRODUCT-INPUT-AUTHORITY", "report authority boundary was relaxed")

    references = export.get("principia_references")
    if not isinstance(references, list) or not references:
        raise KernelError("E-PRODUCT-INPUT-REFERENCE", "exact Principia reference is required")
    for reference in references:
        if not isinstance(reference, Mapping):
            raise KernelError("E-PRODUCT-INPUT-REFERENCE", "Principia reference must be an object")
        if reference.get("principia_status_separate") is not True:
            raise KernelError("E-PRODUCT-INPUT-REFERENCE", "Principia status inheritance is prohibited")
        if reference.get("live") is not False:
            raise KernelError("E-PRODUCT-INPUT-REFERENCE", "live Principia dependency is prohibited")
        if reference.get("automatic_status_inheritance") is not False:
            raise KernelError("E-PRODUCT-INPUT-REFERENCE", "automatic status inheritance is prohibited")

    return {
        "contract": "atlas-principia-product-input-verification/0.1",
        "decision": "valid",
        "workspace_id": workspace["id"],
        "workspace_revision": workspace["revision"],
        "shell_build_digest": shell["build_digest"],
        "report_digest": report_digest,
        "file_count": len(package_bytes),
        "total_bytes": sum(len(payload) for payload in package_bytes.values()),
        "principia_reference_count": len(references),
        "live": False,
        "repository_mutation": False,
    }


def build_product_input(
    output: Path,
    *,
    static_root: Path = STATIC_ROOT,
) -> dict[str, Any]:
    if output.is_symlink() or output.exists():
        raise KernelError("E-PRODUCT-INPUT-OUTPUT", "product input output must not already exist")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(prefix=f".{output.name}.staging-", dir=output.parent)
    )
    try:
        for relative in STATIC_FILES:
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(_read_regular(static_root / relative, f"Atlas source {relative}"))
        shell, report, export, manifest, _ = build_shell.build_workspace_shell(*_default_inputs())
        generated = {
            GENERATED_FILES[0]: render_json(shell).encode("utf-8"),
            GENERATED_FILES[1]: render_json(export).encode("utf-8"),
            GENERATED_FILES[2]: render_json(manifest).encode("utf-8"),
            REPORT_NAME: render_json(report).encode("utf-8"),
        }
        for relative, payload in generated.items():
            target = staging / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        verification = verify_product_input(staging, static_root=static_root)
        os.replace(staging, output)
        return verification
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise


def _snapshot(root: Path) -> dict[str, bytes]:
    verify_product_input(root)
    return {relative: (root / relative).read_bytes() for relative in PACKAGE_FILES}


def check_determinism() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        first = root / "first"
        second = root / "second"
        first_verification = build_product_input(first)
        second_verification = build_product_input(second)
        if first_verification != second_verification or _snapshot(first) != _snapshot(second):
            raise KernelError("E-PRODUCT-INPUT-DETERMINISM", "product input build is not deterministic")
        return first_verification


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify", "check"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--package", type=Path)
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "build":
        if args.output is None:
            raise SystemExit("--output is required")
        result = build_product_input(args.output)
        print(f"wrote={args.output}")
    elif args.command == "verify":
        if args.package is None:
            raise SystemExit("--package is required")
        result = verify_product_input(args.package)
    else:
        result = check_determinism()
    print(render_json(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
