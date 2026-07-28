#!/usr/bin/env python3
"""Build and validate the deterministic Phase 4 Workstream 3 completion report."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from tools.phase2_kernel import load_json, render_json
from tools.phase4_workspace_completion.contracts import (
    run_workstream3_closure,
    validate_completion_report,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--workspace-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workspace/workspace-contract-baseline.json"),
    )
    parser.add_argument(
        "--shell-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workspace/workspace-shell-baseline.json"),
    )
    parser.add_argument(
        "--browser-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workspace/workspace-browser-baseline.json"),
    )
    parser.add_argument(
        "--decision",
        default="proceed-bounded-workspace-fixture-evaluation",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    report = run_workstream3_closure(
        load_json(args.workspace_baseline),
        load_json(args.shell_baseline),
        load_json(args.browser_baseline),
        decision=args.decision,
    )
    validation = validate_completion_report(report)
    rendered = render_json(report)
    if args.output is None:
        sys.stdout.write(rendered)
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
        print(f"wrote={args.output}")
    print(f"phase4-workstream3-report-digest={report['report_digest']}")
    print(f"phase4-workstream3-exit-gates={validation['exit_gate_count']}")
    print(f"phase4-workstream3-recommendation={validation['recommendation']}")
    print("phase4-workstream3=closure-candidate; implementation-authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
