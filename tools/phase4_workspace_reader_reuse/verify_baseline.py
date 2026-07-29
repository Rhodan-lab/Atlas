#!/usr/bin/env python3
"""Verify the immutable Workstream 4 static-reader reuse package baseline."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, load_json
from tools.phase4_workspace_reader_reuse.builder import validate_package_index

BASELINE_CONTRACT = "atlas-phase4-workspace-reader-reuse-baseline/0.1"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def verify_baseline(baseline: Mapping[str, Any], package_dir: Path) -> dict[str, Any]:
    _require(baseline.get("contract") == BASELINE_CONTRACT, "E-READER-REUSE-BASELINE", "baseline contract mismatch")
    expected_files = baseline.get("files")
    _require(isinstance(expected_files, Mapping) and expected_files, "E-READER-REUSE-BASELINE", "baseline files are required")
    observed_paths = sorted(
        path.relative_to(package_dir).as_posix()
        for path in package_dir.rglob("*")
        if path.is_file() and path.name != "identities.sha256"
    )
    _require(observed_paths == sorted(expected_files), "E-READER-REUSE-BASELINE-FILES", "package file set differs")
    for relative in observed_paths:
        payload = (package_dir / relative).read_bytes()
        expected = expected_files[relative]
        _require(isinstance(expected, Mapping), "E-READER-REUSE-BASELINE", f"identity missing for {relative}")
        _require(expected.get("bytes") == len(payload), "E-READER-REUSE-BASELINE", f"byte length drift for {relative}")
        _require(
            expected.get("sha256") == hashlib.sha256(payload).hexdigest(),
            "E-READER-REUSE-BASELINE",
            f"SHA-256 drift for {relative}",
        )
    index = json.loads((package_dir / "package-index.json").read_text(encoding="utf-8"))
    validation = validate_package_index(index)
    _require(
        baseline.get("package_index_digest") == index.get("report_digest"),
        "E-READER-REUSE-BASELINE",
        "package index digest differs",
    )
    authority = baseline.get("authority")
    _require(isinstance(authority, Mapping), "E-READER-REUSE-BASELINE", "baseline authority is required")
    for field in (
        "canonical_mutation",
        "lifecycle_mutation",
        "review_mutation",
        "candidate_resolution_authorized",
        "account_required",
        "cloud_required",
        "external_network_required",
        "production_frontend_architecture_selected",
        "live_principia_dependency",
        "repository_mutation",
    ):
        _require(authority.get(field) is False, "E-READER-REUSE-BASELINE-AUTHORITY", f"baseline requires {field}=false")
    return {
        "contract": "atlas-phase4-workspace-reader-reuse-baseline-validation/0.1",
        "decision": "valid-reader-reuse-package-baseline",
        "file_count": len(observed_paths),
        "package_index_digest": index["report_digest"],
        "reader_reuse_validation": validation["decision"],
        "browser_evidence_included": False,
        "live": False,
        "repository_mutation": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workspace_reader_reuse/reader-reuse-baseline.json"),
    )
    parser.add_argument("--package-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    result = verify_baseline(load_json(args.baseline), args.package_dir)
    print(f"reader-reuse-baseline-files={result['file_count']}")
    print(f"reader-reuse-baseline-digest={result['package_index_digest']}")
    print("reader-reuse-baseline=valid; browser-evidence=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
