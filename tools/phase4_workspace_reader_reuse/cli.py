#!/usr/bin/env python3
"""CLI for deterministic Workstream 4 static-reader reuse packaging."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Sequence

from .builder import build_reader_reuse_package


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=Path("."))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)

    index, report, validation = build_reader_reuse_package(args.repository_root, args.output_dir)
    for path in sorted(item for item in args.output_dir.rglob("*") if item.is_file()):
        payload = path.read_bytes()
        print(
            f"{path.relative_to(args.output_dir).as_posix()}:"
            f"bytes={len(payload)};sha256={hashlib.sha256(payload).hexdigest()}"
        )
    print(f"phase4-reader-reuse-index-digest={index['report_digest']}")
    print(f"phase4-reader-reuse-report-digest={report['report_digest']}")
    print(f"phase4-reader-reuse-validation={validation['decision']}")
    print("phase4-reader-reuse=static-package-candidate; browser-evidence=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
