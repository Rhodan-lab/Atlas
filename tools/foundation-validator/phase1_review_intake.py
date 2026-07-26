#!/usr/bin/env python3
"""Validate accountable-human review submissions against an Atlas handoff bundle.

A valid submission proves that a returned review record targets one active human
handoff task and the exact canonical snapshot supplied to the reviewer. Validation
does not accept the review, resolve findings, permit promotion, or change lifecycle
state. Maintainers must still commit the extracted review record and regenerate
coverage through the normal Phase 1 gates.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import phase1_human_review_handoff as handoff_tool
import phase1_review_gate as gate

SUBMISSION_CONTRACT = "atlas-review-submission/0.1"
SUBMISSION_FIELDS = {
    "contract",
    "coverage_id",
    "task_id",
    "snapshot",
    "submitted_at",
    "reviewed_exact_snapshot",
    "ai_assistance",
    "review_record",
}
SNAPSHOT_FIELDS = {"entity_id", "revision", "sha256"}
AI_FIELDS = {"used", "description"}


@dataclass(frozen=True, order=True)
class IntakeDiagnostic:
    path: str
    code: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
        }


def _diag(path: str, code: str, message: str) -> IntakeDiagnostic:
    return IntakeDiagnostic(path, code, "error", message)


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def load_json(path: Path) -> tuple[Any | None, list[IntakeDiagnostic]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [_diag(str(path), "E-INTAKE-FILE-READ", str(exc))]
    except json.JSONDecodeError as exc:
        return None, [_diag(str(path), "E-INTAKE-JSON", str(exc))]


def load_handoff(path: Path) -> tuple[Mapping[str, Any] | None, list[IntakeDiagnostic]]:
    payload, diagnostics = load_json(path)
    if not isinstance(payload, dict):
        if payload is not None:
            diagnostics.append(
                _diag(str(path), "E-INTAKE-HANDOFF-STRUCTURE", "handoff must be a mapping")
            )
        return None, diagnostics
    try:
        handoff_tool.validate_handoff(payload)
    except ValueError as exc:
        diagnostics.append(_diag(str(path), "E-INTAKE-HANDOFF", str(exc)))
        return None, diagnostics
    return payload, diagnostics


def task_index(handoff: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for track in handoff.get("tracks", []):
        if not isinstance(track, dict):
            continue
        for task in track.get("tasks", []):
            if not isinstance(task, dict):
                continue
            task_id = task.get("id")
            if not isinstance(task_id, str):
                continue
            if task_id in result:
                raise ValueError(f"duplicate task ID in handoff: {task_id}")
            result[task_id] = task
    return result


def validate_submission(
    submission: Mapping[str, Any],
    handoff: Mapping[str, Any],
    path: str = "<submission>",
) -> list[IntakeDiagnostic]:
    diagnostics: list[IntakeDiagnostic] = []

    for field in sorted(set(submission) - SUBMISSION_FIELDS):
        diagnostics.append(
            _diag(path, "E-INTAKE-FIELD-UNKNOWN", f"unknown submission field {field!r}")
        )

    if submission.get("contract") != SUBMISSION_CONTRACT:
        diagnostics.append(
            _diag(
                path,
                "E-INTAKE-CONTRACT",
                f"contract must be {SUBMISSION_CONTRACT!r}",
            )
        )

    coverage_id = submission.get("coverage_id")
    if coverage_id != handoff.get("coverage_id"):
        diagnostics.append(
            _diag(
                path,
                "E-INTAKE-COVERAGE",
                "submission coverage_id does not match the handoff",
            )
        )

    try:
        tasks = task_index(handoff)
    except ValueError as exc:
        diagnostics.append(_diag(path, "E-INTAKE-HANDOFF-TASKS", str(exc)))
        tasks = {}

    task_id = submission.get("task_id")
    task = tasks.get(task_id) if isinstance(task_id, str) else None
    if task is None:
        diagnostics.append(
            _diag(path, "E-INTAKE-TASK", "task_id is not active in the handoff")
        )
    else:
        if task.get("execution_mode") != "human-required":
            diagnostics.append(
                _diag(path, "E-INTAKE-TASK-AUTHORITY", "task is not human-required")
            )
        if task.get("required_for_gate") is not True:
            diagnostics.append(
                _diag(path, "E-INTAKE-TASK-GATE", "task is not an active gate task")
            )

    submitted_at = _parse_date(submission.get("submitted_at"))
    if submitted_at is None:
        diagnostics.append(
            _diag(path, "E-INTAKE-SUBMITTED-AT", "submitted_at must be an ISO date")
        )

    if submission.get("reviewed_exact_snapshot") is not True:
        diagnostics.append(
            _diag(
                path,
                "E-INTAKE-SNAPSHOT-ATTESTATION",
                "reviewed_exact_snapshot must be true",
            )
        )

    snapshot = submission.get("snapshot")
    if not isinstance(snapshot, dict):
        diagnostics.append(
            _diag(path, "E-INTAKE-SNAPSHOT", "snapshot must be a mapping")
        )
        snapshot = {}
    else:
        for field in sorted(set(snapshot) - SNAPSHOT_FIELDS):
            diagnostics.append(
                _diag(path, "E-INTAKE-SNAPSHOT-FIELD", f"unknown snapshot field {field!r}")
            )

    ai = submission.get("ai_assistance")
    if not isinstance(ai, dict):
        diagnostics.append(
            _diag(path, "E-INTAKE-AI", "ai_assistance must be a mapping")
        )
        ai = {}
    else:
        for field in sorted(set(ai) - AI_FIELDS):
            diagnostics.append(
                _diag(path, "E-INTAKE-AI-FIELD", f"unknown AI field {field!r}")
            )
    used_ai = ai.get("used")
    description = ai.get("description")
    if not isinstance(used_ai, bool):
        diagnostics.append(
            _diag(path, "E-INTAKE-AI-USED", "ai_assistance.used must be boolean")
        )
    elif used_ai:
        if not isinstance(description, str) or not description.strip():
            diagnostics.append(
                _diag(
                    path,
                    "E-INTAKE-AI-DISCLOSURE",
                    "AI-assisted submissions require a non-empty description",
                )
            )
    elif description not in (None, ""):
        diagnostics.append(
            _diag(
                path,
                "E-INTAKE-AI-DISCLOSURE",
                "description must be null or empty when AI assistance was not used",
            )
        )

    review_record = submission.get("review_record")
    if not isinstance(review_record, dict):
        diagnostics.append(
            _diag(path, "E-INTAKE-REVIEW", "review_record must be a mapping")
        )
        review_record = {}
    else:
        diagnostics.extend(
            IntakeDiagnostic(item.path, item.code, item.severity, item.message)
            for item in gate.validate_review_record(review_record, f"{path}#review_record")
        )

    if task is not None:
        entity = task.get("entity", {})
        task_snapshot = task.get("entity_snapshot", {})
        task_requirement = task.get("reviewer_requirement", {})
        record_entity = review_record.get("entity", {}) if isinstance(review_record, dict) else {}

        expected_entity_id = entity.get("id")
        expected_revision = entity.get("revision")
        if snapshot.get("entity_id") != expected_entity_id:
            diagnostics.append(
                _diag(path, "E-INTAKE-SNAPSHOT-ENTITY", "snapshot entity_id does not match task")
            )
        if snapshot.get("revision") != expected_revision:
            diagnostics.append(
                _diag(path, "E-INTAKE-SNAPSHOT-REVISION", "snapshot revision does not match task")
            )
        if snapshot.get("sha256") != task_snapshot.get("sha256"):
            diagnostics.append(
                _diag(path, "E-INTAKE-SNAPSHOT-DIGEST", "snapshot SHA-256 does not match handoff")
            )

        if record_entity.get("id") != expected_entity_id:
            diagnostics.append(
                _diag(path, "E-INTAKE-REVIEW-ENTITY", "review record entity does not match task")
            )
        if record_entity.get("revision") != expected_revision:
            diagnostics.append(
                _diag(path, "E-INTAKE-REVIEW-REVISION", "review record revision does not match task")
            )
        if review_record.get("review_type") != task.get("review_type"):
            diagnostics.append(
                _diag(path, "E-INTAKE-REVIEW-TYPE", "review record type does not match task")
            )

        reviewer = review_record.get("reviewer", {}) if isinstance(review_record, dict) else {}
        if reviewer.get("kind") != "human":
            diagnostics.append(
                _diag(path, "E-INTAKE-HUMAN", "handoff submissions require a human reviewer")
            )
        if reviewer.get("accountable") is not True:
            diagnostics.append(
                _diag(path, "E-INTAKE-ACCOUNTABILITY", "reviewer must be accountable")
            )
        allowed_independence = task_requirement.get("allowed_independence", [])
        if reviewer.get("independence") not in allowed_independence:
            diagnostics.append(
                _diag(
                    path,
                    "E-INTAKE-INDEPENDENCE",
                    "reviewer independence does not satisfy the handoff task",
                )
            )
        qualification = reviewer.get("qualification")
        if not isinstance(qualification, str) or not qualification.strip():
            diagnostics.append(
                _diag(path, "E-INTAKE-QUALIFICATION", "reviewer qualification is required")
            )
        if not isinstance(reviewer.get("conflicts"), list):
            diagnostics.append(
                _diag(path, "E-INTAKE-CONFLICTS", "reviewer conflicts must be a list")
            )

        completed_at = _parse_date(review_record.get("completed_at"))
        if submitted_at is not None and completed_at is not None and submitted_at < completed_at:
            diagnostics.append(
                _diag(path, "E-INTAKE-DATE-ORDER", "submitted_at cannot precede completed_at")
            )

    return sorted(set(diagnostics))


def normalized_review_record(
    submission: Mapping[str, Any],
    handoff: Mapping[str, Any],
) -> dict[str, Any]:
    diagnostics = validate_submission(submission, handoff)
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        detail = "; ".join(f"{item.code}: {item.message}" for item in errors)
        raise ValueError(f"submission is invalid: {detail}")

    record = json.loads(json.dumps(submission["review_record"]))
    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    metadata["intake"] = {
        "submission_contract": SUBMISSION_CONTRACT,
        "coverage_id": submission["coverage_id"],
        "task_id": submission["task_id"],
        "snapshot": submission["snapshot"],
        "submitted_at": submission["submitted_at"],
        "reviewed_exact_snapshot": True,
        "ai_assistance": submission["ai_assistance"],
    }
    record["metadata"] = metadata
    return record


def _print_diagnostics(diagnostics: Sequence[IntakeDiagnostic], json_output: bool) -> None:
    if json_output:
        print(json.dumps([item.to_dict() for item in diagnostics], indent=2, sort_keys=True))
    else:
        for item in diagnostics:
            print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "extract"])
    parser.add_argument("submission", type=Path)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    submission, submission_diagnostics = load_json(args.submission)
    handoff, handoff_diagnostics = load_handoff(args.handoff)
    diagnostics = list(submission_diagnostics) + list(handoff_diagnostics)

    if not isinstance(submission, dict):
        if submission is not None:
            diagnostics.append(
                _diag(str(args.submission), "E-INTAKE-STRUCTURE", "submission must be a mapping")
            )
    elif handoff is not None:
        diagnostics.extend(validate_submission(submission, handoff, str(args.submission)))

    diagnostics = sorted(set(diagnostics))
    _print_diagnostics(diagnostics, args.json)
    if any(item.severity == "error" for item in diagnostics):
        return 1

    if args.command == "extract":
        if args.out is None:
            print("--out is required for extract", file=sys.stderr)
            return 1
        assert isinstance(submission, dict) and handoff is not None
        record = normalized_review_record(submission, handoff)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        print(f"extracted review record to {args.out}")
    else:
        print("review submission is valid for the active exact-snapshot handoff task")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
