#!/usr/bin/env python3
"""CLI for Phase 4 Workstream 4 Catalase generalization evidence."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from tools.phase2_kernel import load_json, render_json

from .evaluation import run_generalization, write_outputs


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--spec",
        type=Path,
        default=Path("content/fixtures/phase4_workspace_generalization/catalase-generalization.v01.json"),
    )
    parser.add_argument(
        "--structured-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/structured-baseline.json"),
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)

    result = run_generalization(load_json(args.spec), args.canonical_root, load_json(args.structured_baseline))
    if args.output_dir is None:
        sys.stdout.write(render_json(result["evaluation_report"]))
    else:
        identities = write_outputs(result, args.output_dir)
        print("wrote=" + str(args.output_dir))
        for name in sorted(identities):
            item = identities[name]
            print(f"{name}:bytes={item['bytes']};sha256={item['sha256']}")
    validation = result["evaluation_validation"]
    print(f"phase4-workstream4-report-digest={validation['report_digest']}")
    print(f"phase4-workstream4-exit-gates={validation['exit_gate_count']}")
    print(f"phase4-workstream4-negative-cases={validation['negative_case_count']}")
    print(f"phase4-workstream4-recommendation={validation['recommendation']}")
    print("phase4-workstream4=generalization-candidate; implementation-authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
