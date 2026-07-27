#!/usr/bin/env python3
"""Public Phase 3 closure entry point with accepted lexical-fixture compatibility."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping

from tools.phase2_kernel import KernelError, load_json, render_json
from tools.phase3_retrieval.closure import (
    COMPLETION_CONTRACT,
    COMPLETION_VALIDATION_CONTRACT,
    run_phase3_closure as _run_phase3_closure,
    validate_completion_report,
)

_LEGACY_FALSE_FIELDS = frozenset(
    {
        "external_services",
        "embeddings",
        "vector_database",
    }
)


class _AcceptedLexicalBaselineView(dict[str, Any]):
    """Preserve the accepted JSON identity while exposing historical false defaults."""

    def __getitem__(self, key: str) -> Any:
        if key in _LEGACY_FALSE_FIELDS and key not in self:
            return False
        return super().__getitem__(key)


def _lexical_view(value: Mapping[str, Any]) -> Mapping[str, Any]:
    if isinstance(value, _AcceptedLexicalBaselineView):
        return value
    return _AcceptedLexicalBaselineView(value)


def run_phase3_closure(
    canonical_root: Path,
    query_set: Mapping[str, Any],
    lexical_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    fusion_baseline: Mapping[str, Any],
    research_fixtures: Mapping[str, Any],
    research_baseline: Mapping[str, Any],
) -> dict[str, Any]:
    """Run closure without rewriting the historically accepted lexical fixture."""
    return _run_phase3_closure(
        canonical_root,
        query_set,
        _lexical_view(lexical_baseline),
        structured_baseline,
        fusion_baseline,
        research_fixtures,
        research_baseline,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--query-set",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/reference-query-set.v01.json"),
    )
    parser.add_argument(
        "--lexical-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/lexical-baseline.json"),
    )
    parser.add_argument(
        "--structured-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/structured-baseline.json"),
    )
    parser.add_argument(
        "--fusion-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/rank-fusion.json"),
    )
    parser.add_argument(
        "--research-fixtures",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/research-foundations.v01.json"),
    )
    parser.add_argument(
        "--research-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/research-foundations-baseline.json"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = run_phase3_closure(
            args.canonical_root,
            load_json(args.query_set),
            load_json(args.lexical_baseline),
            load_json(args.structured_baseline),
            load_json(args.fusion_baseline),
            load_json(args.research_fixtures),
            load_json(args.research_baseline),
        )
        validation = validate_completion_report(report)
        rendered = render_json(report)
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"wrote={args.output}")
            print(f"phase3-closure={validation['decision']}")
            print(f"phase4-recommendation={validation['phase4_recommendation']}")
        return 0
    except (KernelError, OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
