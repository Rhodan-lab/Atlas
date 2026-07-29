#!/usr/bin/env python3
"""Verify the immutable Phase 4 Workstream 4 completion baseline."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, load_json, render_json
from tools.phase4_workstream4_completion.closure import build_completion_report, validate_completion_report
from tools.phase4_workstream4_completion.constants import BASELINE_CONTRACT


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise KernelError("E-W4-CLOSURE-BASELINE", message)


def verify_baseline(
    baseline: Mapping[str, Any],
    report: Mapping[str, Any],
    validation: Mapping[str, Any],
) -> None:
    _require(baseline.get("contract") == BASELINE_CONTRACT, "completion baseline contract mismatch")
    _require(baseline.get("state") == "pinned-closure-candidate", "completion baseline state mismatch")
    _require(baseline.get("python_substantive_artifacts_byte_identical") is True, "cross-Python identity not pinned")
    _require(baseline.get("python_versions") == ["3.11", "3.13"], "Python version boundary drift")

    report_bytes = render_json(report).encode("utf-8")
    validation_bytes = render_json(validation).encode("utf-8")
    expected_report = baseline["completion_report"]
    expected_validation = baseline["completion_validation"]

    _require(len(report_bytes) == expected_report["artifact"]["bytes"], "completion report byte length drift")
    _require(hashlib.sha256(report_bytes).hexdigest() == expected_report["artifact"]["sha256"], "completion report SHA-256 drift")
    _require(report.get("contract") == expected_report["contract"], "completion report contract drift")
    _require(report.get("state") == expected_report["state"], "completion report state drift")
    _require(report.get("decision") == expected_report["decision"], "completion report decision drift")
    _require(report.get("report_digest") == expected_report["report_digest"], "completion report digest drift")
    _require(len(report.get("exit_gates", {})) == expected_report["exit_gate_count"], "completion gate count drift")
    _require(sorted(report["exit_gates"]) == baseline["exit_gates"], "completion gate registry drift")
    _require(all(report["exit_gates"].values()), "completion gate failure")

    _require(len(validation_bytes) == expected_validation["artifact"]["bytes"], "completion validation byte length drift")
    _require(hashlib.sha256(validation_bytes).hexdigest() == expected_validation["artifact"]["sha256"], "completion validation SHA-256 drift")
    _require(validation.get("contract") == expected_validation["contract"], "completion validation contract drift")
    _require(validation.get("decision") == expected_validation["decision"], "completion validation decision drift")
    _require(validation.get("recommendation") == expected_validation["recommendation"], "completion validation recommendation drift")
    _require(validation.get("report_digest") == expected_validation["report_digest"], "completion validation digest drift")

    _require(report.get("accepted_evidence") == baseline["accepted_evidence"], "accepted evidence binding drift")
    _require(report.get("authority") == baseline["authority"], "authority baseline drift")
    _require(len(report.get("limitations", [])) == baseline["limitations_count"], "limitations count drift")
    _require(len(report.get("negative_cases", [])) == baseline["negative_case_count"], "negative registry count drift")
    for field, value in baseline["recommendation"].items():
        _require(report["recommendation"].get(field) == value, f"recommendation drift: {field}")
    for field, value in baseline["replaceability"].items():
        _require(report["replaceability"].get(field) == value, f"replaceability drift: {field}")
    for field, value in baseline["rollback"].items():
        _require(report["rollback_boundary"].get(field) == value, f"rollback drift: {field}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--baseline",
        type=Path,
        default=Path("content/fixtures/phase4_workstream4_completion/workstream4-completion-baseline.json"),
    )
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
    args = parser.parse_args(argv)

    report = build_completion_report(
        load_json(args.generalization_baseline),
        load_json(args.package_baseline),
        load_json(args.browser_baseline),
    )
    validation = validate_completion_report(report)
    verify_baseline(load_json(args.baseline), report, validation)
    baseline_bytes = args.baseline.read_bytes()
    print("phase4-workstream4-completion-baseline-sha256=" + hashlib.sha256(baseline_bytes).hexdigest())
    print("phase4-workstream4-completion-baseline=pinned; gates=14; implementation-authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
