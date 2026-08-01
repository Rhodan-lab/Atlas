#!/usr/bin/env python3
"""Compare a candidate Principia reference snapshot with the accepted Atlas baseline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import compile_canonical
from .evidence_drift import build_evidence_drift_report
from .evidence_review import load_review_index
from .kernel import KernelError, load_json, render_json
from .repository import KernelRepository

DEFAULT_BASELINE = Path(
    "content/fixtures/phase2_bridge/product-alpha-refrigerator.references.v01.json"
)
DEFAULT_REVIEW_ROOT = Path("content/reviews/ai")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--review-root", type=Path, default=DEFAULT_REVIEW_ROOT)
    parser.add_argument("--runtime", type=Path)
    parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        runtime = (
            load_json(args.runtime)
            if args.runtime
            else compile_canonical(args.canonical_root)
        )
        report = build_evidence_drift_report(
            load_json(args.baseline),
            load_json(args.candidate),
            KernelRepository(runtime),
            load_review_index(args.review_root),
        )
        rendered = render_json(report)
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"wrote={args.output}")
        return 0
    except (KernelError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
