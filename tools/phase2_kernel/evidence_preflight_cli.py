#!/usr/bin/env python3
"""Preflight candidate Atlas runtime changes against accepted Principia routes."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import compile_canonical
from .evidence_impact import compile_evidence_impact_index
from .evidence_preflight import analyze_evidence_runtime_preflight
from .evidence_review import load_review_index
from .kernel import KernelError, load_json, render_json
from .repository import KernelRepository

DEFAULT_REGISTRY = Path(
    "content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json"
)
DEFAULT_REVIEW_ROOT = Path("content/reviews/ai")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    baseline = parser.add_mutually_exclusive_group(required=True)
    baseline.add_argument("--baseline-runtime", type=Path)
    baseline.add_argument("--baseline-canonical-root", type=Path)
    candidate = parser.add_mutually_exclusive_group()
    candidate.add_argument("--candidate-runtime", type=Path)
    candidate.add_argument("--candidate-canonical-root", type=Path)
    parser.add_argument("--impact-index", type=Path)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--review-root", type=Path, default=DEFAULT_REVIEW_ROOT)
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="repository root used to resolve accepted snapshots",
    )
    parser.add_argument("--output", type=Path)
    return parser


def _runtime(runtime_path: Path | None, canonical_root: Path | None) -> dict:
    if runtime_path is not None:
        return load_json(runtime_path)
    if canonical_root is None:
        canonical_root = Path("content/canonical")
    return compile_canonical(canonical_root)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        baseline_runtime = _runtime(
            args.baseline_runtime,
            args.baseline_canonical_root,
        )
        candidate_runtime = _runtime(
            args.candidate_runtime,
            args.candidate_canonical_root,
        )
        if args.impact_index is not None:
            impact_index = load_json(args.impact_index)
        else:
            impact_index = compile_evidence_impact_index(
                load_json(args.registry),
                KernelRepository(baseline_runtime),
                load_review_index(args.review_root),
                args.repository_root,
            )
        report = analyze_evidence_runtime_preflight(
            impact_index,
            baseline_runtime,
            candidate_runtime,
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
