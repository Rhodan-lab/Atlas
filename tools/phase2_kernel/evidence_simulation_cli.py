#!/usr/bin/env python3
"""Simulate proposed Atlas evidence changes against accepted Principia routes."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import compile_canonical
from .evidence_impact import compile_evidence_impact_index
from .evidence_review import load_review_index
from .evidence_simulation import simulate_evidence_impact
from .kernel import KernelError, load_json, render_json
from .repository import KernelRepository

DEFAULT_REGISTRY = Path(
    "content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json"
)
DEFAULT_SCENARIO = Path(
    "content/fixtures/phase2_bridge/evidence-impact-scenario.none.v01.json"
)
DEFAULT_REVIEW_ROOT = Path("content/reviews/ai")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, default=DEFAULT_SCENARIO)
    parser.add_argument("--impact-index", type=Path)
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
        help="repository root used to resolve accepted snapshots",
    )
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.impact_index is not None:
            impact_index = load_json(args.impact_index)
        else:
            runtime = (
                load_json(args.runtime)
                if args.runtime
                else compile_canonical(args.canonical_root)
            )
            impact_index = compile_evidence_impact_index(
                load_json(args.registry),
                KernelRepository(runtime),
                load_review_index(args.review_root),
                args.repository_root,
            )
        report = simulate_evidence_impact(
            impact_index,
            load_json(args.scenario),
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
