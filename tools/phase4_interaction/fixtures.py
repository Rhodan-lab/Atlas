#!/usr/bin/env python3
"""Load a deterministic multi-file Phase 4 interaction fixture set."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json
from tools.phase4_interaction.contracts import (
    FIXTURE_CONTRACT,
    MODE,
    validate_fixture_bundle,
)

MANIFEST_CONTRACT = "atlas-phase4-interaction-fixture-manifest/0.1"
PART_KEYS = frozenset({"views", "states", "bridge_and_failures", "negative_cases"})
ASSEMBLED_FIELDS = frozenset(
    {
        "views",
        "states",
        "principia_references",
        "impact_warnings",
        "failure_states",
        "negative_cases",
    }
)


def _require_mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def load_fixture_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    if manifest.get("contract") != MANIFEST_CONTRACT:
        raise KernelError("E-INTERACTION-MANIFEST-CONTRACT", f"expected {MANIFEST_CONTRACT!r}")
    if manifest.get("assembled_contract") != FIXTURE_CONTRACT:
        raise KernelError("E-INTERACTION-MANIFEST-ASSEMBLY", f"assembled_contract must be {FIXTURE_CONTRACT!r}")
    if manifest.get("mode") != MODE:
        raise KernelError("E-INTERACTION-MANIFEST-MODE", f"manifest mode must be {MODE!r}")
    fixture_id = manifest.get("id")
    version = manifest.get("version")
    source_digest = manifest.get("source_digest")
    if not isinstance(fixture_id, str) or not fixture_id.strip():
        raise KernelError("E-INTERACTION-MANIFEST-ID", "manifest id is required")
    if not isinstance(version, int) or isinstance(version, bool) or version < 1:
        raise KernelError("E-INTERACTION-MANIFEST-VERSION", "manifest version must be positive")
    if not isinstance(source_digest, str) or len(source_digest) != 64:
        raise KernelError("E-INTERACTION-MANIFEST-SOURCE", "manifest source_digest must be SHA-256")

    parts = _require_mapping(
        manifest.get("parts"),
        "E-INTERACTION-MANIFEST-PARTS",
        "manifest parts must be an object",
    )
    if set(parts) != PART_KEYS:
        raise KernelError(
            "E-INTERACTION-MANIFEST-PARTS",
            f"manifest parts must equal {sorted(PART_KEYS)}",
        )

    assembled: dict[str, Any] = {
        "contract": FIXTURE_CONTRACT,
        "id": fixture_id,
        "version": version,
        "mode": MODE,
        "source_digest": source_digest,
    }
    base = path.parent.resolve()
    for key in sorted(parts):
        relative = parts[key]
        if not isinstance(relative, str) or not relative.strip():
            raise KernelError("E-INTERACTION-MANIFEST-PARTS", f"part {key} path is required")
        candidate = (base / relative).resolve()
        if base not in candidate.parents:
            raise KernelError("E-INTERACTION-MANIFEST-PATH", "fixture part must remain inside manifest directory")
        part = _require_mapping(
            load_json(candidate),
            "E-INTERACTION-MANIFEST-PART",
            f"part {key} must be an object",
        )
        unknown = set(part) - ASSEMBLED_FIELDS
        if unknown:
            raise KernelError("E-INTERACTION-MANIFEST-PART", f"part {key} contains unknown fields {sorted(unknown)}")
        for field, value in part.items():
            if field in assembled:
                raise KernelError("E-INTERACTION-MANIFEST-PART", f"field {field} appears in multiple parts")
            assembled[field] = value

    missing = ASSEMBLED_FIELDS - set(assembled)
    if missing:
        raise KernelError("E-INTERACTION-MANIFEST-PART", f"assembled fixture misses fields {sorted(missing)}")
    return assembled


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/reference-interactions.v01.json"),
    )
    parser.add_argument("--assembled-output", type=Path)
    parser.add_argument("--report-output", type=Path)
    args = parser.parse_args(argv)

    repository = KernelRepository(compile_canonical(args.canonical_root))
    assembled = load_fixture_manifest(args.manifest)
    report, _ = validate_fixture_bundle(assembled, repository)

    if args.assembled_output is not None:
        args.assembled_output.parent.mkdir(parents=True, exist_ok=True)
        args.assembled_output.write_text(render_json(assembled), encoding="utf-8")
        print(f"wrote={args.assembled_output}")
    rendered = render_json(report)
    if args.report_output is None:
        sys.stdout.write(rendered)
    else:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(rendered, encoding="utf-8")
        print(f"wrote={args.report_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
