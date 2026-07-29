#!/usr/bin/env python3
"""Build deterministic Phase 4 Workstream 4 Catalase generalization evidence."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Sequence

from tools.phase2_kernel import KernelRepository, compile_canonical
from tools.phase4_workspace_generalization.contracts import render_bundle, validate_generalization_bundle
from tools.phase4_workspace_generalization.fixture import build_fixture


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)

    repository = KernelRepository(compile_canonical(args.canonical_root))
    fixture = build_fixture()
    report, core_report, export, manifest = validate_generalization_bundle(fixture, repository)
    rendered = render_bundle(fixture, repository)

    if args.output_dir is None:
        print(rendered["catalase-generalization-report.json"], end="")
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for filename, payload in rendered.items():
            path = args.output_dir / filename
            path.write_text(payload, encoding="utf-8")
            print(f"wrote={path}")
            print(f"sha256:{filename}={hashlib.sha256(payload.encode('utf-8')).hexdigest()}")

    print(f"phase4-workstream4-report-digest={report['report_digest']}")
    print(f"phase4-workspace-contract-report-digest={core_report['report_digest']}")
    print(f"phase4-workspace-export-digest={export['report_digest']}")
    print(f"phase4-workspace-manifest-digest={manifest['report_digest']}")
    print(f"phase4-workstream4-recommendation={report['recommendation']}")
    print("phase4-workstream4=fixture-generalization-candidate; implementation-authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
