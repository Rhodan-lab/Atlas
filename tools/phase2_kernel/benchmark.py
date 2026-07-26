#!/usr/bin/env python3
"""Representative performance measurements for the Atlas Phase 2 kernel."""
from __future__ import annotations

import argparse
import json
import math
import platform
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Callable

from .bridge import import_principia_candidate, lifecycle_impact_report
from .compiler import compile_canonical
from .kernel import KernelError, KernelRepository, load_json

BENCHMARK_CONTRACT = "atlas-kernel-benchmark/0.1"
DEFAULT_BUDGETS_MS = {
    "compile": 5000.0,
    "exact_lookup": 5.0,
    "provenance": 25.0,
    "bridge_import": 25.0,
    "impact": 25.0,
}


def _measure(operation: Callable[[], object], iterations: int) -> dict[str, float | int]:
    if iterations < 1:
        raise ValueError("iterations must be positive")
    durations: list[float] = []
    operation()
    for _ in range(iterations):
        started = time.perf_counter_ns()
        operation()
        durations.append((time.perf_counter_ns() - started) / 1_000_000.0)
    ordered = sorted(durations)
    p95_index = min(
        len(ordered) - 1,
        max(0, math.ceil(len(ordered) * 0.95) - 1),
    )
    return {
        "iterations": iterations,
        "median_ms": round(statistics.median(ordered), 6),
        "p95_ms": round(ordered[p95_index], 6),
        "max_ms": round(max(ordered), 6),
    }


def run_benchmark(
    canonical_root: Path,
    fixture: Path,
    compile_iterations: int = 3,
    operation_iterations: int = 200,
) -> dict[str, Any]:
    payload = load_json(fixture)
    compile_metric = _measure(lambda: compile_canonical(canonical_root), compile_iterations)
    runtime = compile_canonical(canonical_root)
    repository = KernelRepository(runtime)
    imported = import_principia_candidate(payload, repository)

    metrics = {
        "compile": compile_metric,
        "exact_lookup": _measure(
            lambda: repository.exact("model:en:delayed-correction-recurrence", 2),
            operation_iterations,
        ),
        "provenance": _measure(
            lambda: repository.provenance_sources(
                "synthesis:en:delayed-feedback-and-oscillation", 2
            ),
            operation_iterations,
        ),
        "bridge_import": _measure(
            lambda: import_principia_candidate(payload, repository),
            operation_iterations,
        ),
        "impact": _measure(
            lambda: lifecycle_impact_report(
                repository,
                "model:en:delayed-correction-recurrence",
                2,
                [imported],
            ),
            operation_iterations,
        ),
    }
    return {
        "contract": BENCHMARK_CONTRACT,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "entity_count": runtime["entity_count"],
        "source_digest": runtime["source_digest"],
        "fixture_contract": payload.get("contract"),
        "metrics": metrics,
        "budgets_ms": DEFAULT_BUDGETS_MS,
    }


def enforce_budgets(report: dict[str, Any]) -> None:
    failures: list[str] = []
    metrics = report.get("metrics", {})
    for name, budget in DEFAULT_BUDGETS_MS.items():
        metric = metrics.get(name, {})
        p95 = metric.get("p95_ms") if isinstance(metric, dict) else None
        if not isinstance(p95, (int, float)):
            failures.append(f"{name}: missing p95_ms")
        elif p95 > budget:
            failures.append(f"{name}: p95 {p95:.6f} ms exceeds {budget:.3f} ms")
    if failures:
        raise KernelError("E-BENCHMARK-BUDGET", "; ".join(failures))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )
    parser.add_argument(
        "--fixture",
        type=Path,
        default=Path(
            "content/fixtures/phase2_bridge/principia-feedback-pr16-v02.json"
        ),
    )
    parser.add_argument("--compile-iterations", type=int, default=3)
    parser.add_argument("--operation-iterations", type=int, default=200)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args(argv)
    try:
        report = run_benchmark(
            args.canonical_root,
            args.fixture,
            compile_iterations=args.compile_iterations,
            operation_iterations=args.operation_iterations,
        )
        if args.enforce:
            enforce_budgets(report)
        rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"wrote={args.output}")
        else:
            sys.stdout.write(rendered)
        return 0
    except (KernelError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
