#!/usr/bin/env python3
"""Build and validate deterministic Phase 4 Workstream 4 completion evidence."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from tools.phase2_kernel import load_json, render_json
from tools.phase4_workstream4_completion.closure import build_completion_report, validate_completion_report


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--generalization-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workspace_generalization/catalase-generalization-baseline.json"),
    )
    parser.add_argument(
        "--package-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workspace_reader_reuse/reader-reuse-baseline.json"),
    )
    parser.add_argument(
        "--browser-baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workspace_reader_browser/reader-reuse-browser-baseline.json"),
    )
    parser.add_argument("--decision", default="proceed-phase4-completion-governance")
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--validation-output", type=Path)
    args = parser.parse_args(argv)

    report = build_completion_report(
        load_json(args.generalization_baseline),
        load_json(args.package_baseline),
        load_json(args.browser_baseline),
        decision=args.decision,
    )
    validation = validate_completion_report(report)
    report_text = render_json(report)
    validation_text = render_json(validation)

    if args.report_output is None:
        sys.stdout.write(report_text)
    else:
        args.report_output.parent.mkdir(parents=True, exist_ok=True)
        args.report_output.write_text(report_text, encoding="utf-8")
        print(f"wrote={args.report_output}")
    if args.validation_output is not None:
        args.validation_output.parent.mkdir(parents=True, exist_ok=True)
        args.validation_output.write_text(validation_text, encoding="utf-8")
        print(f"wrote={args.validation_output}")

    print(f"phase4-workstream4-report-digest={report['report_digest']}")
    print(f"phase4-workstream4-validation-digest={validation['report_digest']}")
    print(f"phase4-workstream4-exit-gates={validation['exit_gate_count']}")
    print(f"phase4-workstream4-negative-cases={validation['negative_case_count']}")
    print(f"phase4-workstream4-recommendation={validation['recommendation']}")
    print("phase4-workstream4=closure-candidate; implementation-authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
