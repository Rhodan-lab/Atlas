#!/usr/bin/env python3
"""Compile or query the accepted Principia evidence impact index."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import compile_canonical
from .evidence_impact import (
    compile_evidence_impact_index,
    query_evidence_impact,
)
from .evidence_review import load_review_index
from .kernel import KernelError, load_json, render_json
from .repository import KernelRepository

DEFAULT_REGISTRY = Path(
    "content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json"
)
DEFAULT_REVIEW_ROOT = Path("content/reviews/ai")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--review-root", type=Path, default=DEFAULT_REVIEW_ROOT)
    parser.add_argument("--runtime", type=Path)
    parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="repository root used to resolve registered snapshots",
    )
    parser.add_argument("--entity", help="query one Atlas entity ID")
    parser.add_argument("--revision", type=int, help="query one exact revision")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.revision is not None and args.entity is None:
        print("--revision requires --entity", file=sys.stderr)
        return 2
    try:
        runtime = (
            load_json(args.runtime)
            if args.runtime
            else compile_canonical(args.canonical_root)
        )
        index = compile_evidence_impact_index(
            load_json(args.registry),
            KernelRepository(runtime),
            load_review_index(args.review_root),
            args.repository_root,
        )
        payload = (
            query_evidence_impact(index, args.entity, args.revision)
            if args.entity
            else index
        )
        rendered = render_json(payload)
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
