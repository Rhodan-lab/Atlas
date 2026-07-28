#!/usr/bin/env python3
"""Generate deterministic Catalase workspace generalization evidence."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from tools.phase2_kernel import KernelRepository, compile_canonical, load_json, render_json
from tools.phase4_workspace_generalization.artifacts import validate_fixture_bundle


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--fixture",
        type=Path,
        default=Path("content/fixtures/phase4_workspace_generalization/catalase-workspace.v01.json"),
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)

    repository = KernelRepository(compile_canonical(args.canonical_root))
    fixture = load_json(args.fixture)
    report, validation, export, manifest = validate_fixture_bundle(fixture, repository)

    rendered_report = render_json(report)
    if args.output_dir is None:
        sys.stdout.write(rendered_report)
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        files = {
            "catalase-generalization-report.json": report,
            "catalase-generalization-validation.json": validation,
            "workspace-export.json": export,
            "workspace-manifest.json": manifest,
        }
        for name, record in files.items():
            path = args.output_dir / name
            path.write_text(render_json(record), encoding="utf-8")
            print(f"wrote={path}")

    print(f"phase4-catalase-report-digest={report['report_digest']}")
    print(f"phase4-catalase-validation-digest={validation['report_digest']}")
    print(f"phase4-catalase-export-digest={export['report_digest']}")
    print(f"phase4-catalase-manifest-digest={manifest['report_digest']}")
    print("phase4-catalase=contract-reuse-candidate; browser-authorized=false; mutation=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
