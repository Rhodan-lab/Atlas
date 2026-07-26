#!/usr/bin/env python3
"""Validate explicit maintainer admission decisions for returned Atlas reviews.

Admission is distinct from scientific or lifecycle approval. It decides whether a
validated exact-snapshot review submission may be prepared for normal repository
review as a canonical review record. This tool never commits to
content/reviews/records, resolves findings, changes authored content, or promotes an
entity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

import phase1_review_gate as gate
import phase1_review_intake as intake

ADMISSION_CONTRACT = "atlas-review-admission/0.1"
ADMISSION_ID_RE = re.compile(
    r"^admission:[a-z0-9]+(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*$"
)
DECISIONS = {"accept", "request-changes", "reject"}
ADMISSION_FIELDS = {
    "contract",
    "id",
    "decision",
    "decided_at",
    "decider",
    "external_verification",
    "rationale",
    "test_fixture",
}
DECIDER_FIELDS = {
    "display_name",
    "kind",
    "role",
    "accountable",
    "conflicts",
}
VERIFICATION_FIELDS = {
    "reviewer_identity_checked",
    "qualification_checked",
    "independence_checked",
    "conflicts_checked",
    "method",
}
DEFAULT_RECORDS_DIR = REPO_ROOT / "content" / "reviews" / "records"


@dataclass(frozen=True, order=True)
class AdmissionDiagnostic:
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


def _diag(path: str, code: str, message: str) -> AdmissionDiagnostic:
    return AdmissionDiagnostic(path, code, "error", message)


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def load_json(path: Path) -> tuple[Any | None, list[AdmissionDiagnostic]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [_diag(str(path), "E-ADMISSION-FILE-READ", str(exc))]
    except json.JSONDecodeError as exc:
        return None, [_diag(str(path), "E-ADMISSION-JSON", str(exc))]


def canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def existing_record_ids(records_dir: Path) -> tuple[set[str], list[AdmissionDiagnostic]]:
    identifiers: set[str] = set()
    diagnostics: list[AdmissionDiagnostic] = []
    if not records_dir.exists():
        return identifiers, diagnostics
    for path in sorted(records_dir.glob("*.json")):
        payload, load_diagnostics = load_json(path)
        diagnostics.extend(load_diagnostics)
        if not isinstance(payload, dict):
            continue
        record_id = payload.get("id")
        if isinstance(record_id, str):
            if record_id in identifiers:
                diagnostics.append(
                    _diag(
                        str(path),
                        "E-ADMISSION-EXISTING-ID-DUPLICATE",
                        f"review ID {record_id!r} is already duplicated in the records directory",
                    )
                )
            identifiers.add(record_id)
    return identifiers, diagnostics


def validate_admission(
    admission: Mapping[str, Any],
    submission: Mapping[str, Any],
    handoff: Mapping[str, Any],
    known_record_ids: set[str] | None = None,
    path: str = "<admission>",
) -> list[AdmissionDiagnostic]:
    diagnostics: list[AdmissionDiagnostic] = []
    known_record_ids = known_record_ids or set()

    diagnostics.extend(
        AdmissionDiagnostic(item.path, item.code, item.severity, item.message)
        for item in intake.validate_submission(submission, handoff, "<submission>")
    )

    for field in sorted(set(admission) - ADMISSION_FIELDS):
        diagnostics.append(
            _diag(path, "E-ADMISSION-FIELD-UNKNOWN", f"unknown admission field {field!r}")
        )

    if admission.get("contract") != ADMISSION_CONTRACT:
        diagnostics.append(
            _diag(
                path,
                "E-ADMISSION-CONTRACT",
                f"contract must be {ADMISSION_CONTRACT!r}",
            )
        )

    admission_id = admission.get("id")
    if not isinstance(admission_id, str) or not ADMISSION_ID_RE.fullmatch(admission_id):
        diagnostics.append(_diag(path, "E-ADMISSION-ID", "admission id is not canonical"))

    decision = admission.get("decision")
    if decision not in DECISIONS:
        diagnostics.append(
            _diag(path, "E-ADMISSION-DECISION", f"unsupported decision {decision!r}")
        )

    decided_at = _parse_date(admission.get("decided_at"))
    if decided_at is None:
        diagnostics.append(
            _diag(path, "E-ADMISSION-DECIDED-AT", "decided_at must be an ISO date")
        )
    submitted_at = _parse_date(submission.get("submitted_at"))
    if decided_at is not None and submitted_at is not None and decided_at < submitted_at:
        diagnostics.append(
            _diag(
                path,
                "E-ADMISSION-DATE-ORDER",
                "decided_at cannot precede submission submitted_at",
            )
        )

    decider = admission.get("decider")
    if not isinstance(decider, dict):
        diagnostics.append(_diag(path, "E-ADMISSION-DECIDER", "decider must be a mapping"))
        decider = {}
    else:
        for field in sorted(set(decider) - DECIDER_FIELDS):
            diagnostics.append(
                _diag(
                    path,
                    "E-ADMISSION-DECIDER-FIELD",
                    f"unknown decider field {field!r}",
                )
            )
    for field in ("display_name", "role"):
        value = decider.get(field)
        if not isinstance(value, str) or not value.strip():
            diagnostics.append(
                _diag(path, f"E-ADMISSION-DECIDER-{field.upper().replace('_', '-')}", f"decider.{field} is required")
            )
    if decider.get("kind") != "human":
        diagnostics.append(
            _diag(path, "E-ADMISSION-DECIDER-KIND", "admission requires a human decider")
        )
    if decider.get("accountable") is not True:
        diagnostics.append(
            _diag(path, "E-ADMISSION-DECIDER-ACCOUNTABILITY", "decider must be accountable")
        )
    if not isinstance(decider.get("conflicts"), list):
        diagnostics.append(
            _diag(path, "E-ADMISSION-DECIDER-CONFLICTS", "decider.conflicts must be a list")
        )

    verification = admission.get("external_verification")
    if not isinstance(verification, dict):
        diagnostics.append(
            _diag(
                path,
                "E-ADMISSION-VERIFICATION",
                "external_verification must be a mapping",
            )
        )
        verification = {}
    else:
        for field in sorted(set(verification) - VERIFICATION_FIELDS):
            diagnostics.append(
                _diag(
                    path,
                    "E-ADMISSION-VERIFICATION-FIELD",
                    f"unknown verification field {field!r}",
                )
            )
    for field in sorted(VERIFICATION_FIELDS - {"method"}):
        if not isinstance(verification.get(field), bool):
            diagnostics.append(
                _diag(
                    path,
                    "E-ADMISSION-VERIFICATION-BOOLEAN",
                    f"external_verification.{field} must be boolean",
                )
            )
    method = verification.get("method")
    if not isinstance(method, str) or not method.strip():
        diagnostics.append(
            _diag(
                path,
                "E-ADMISSION-VERIFICATION-METHOD",
                "external_verification.method is required",
            )
        )

    if decision == "accept":
        required_checks = sorted(VERIFICATION_FIELDS - {"method"})
        missing_checks = [field for field in required_checks if verification.get(field) is not True]
        if missing_checks:
            diagnostics.append(
                _diag(
                    path,
                    "E-ADMISSION-VERIFICATION-INCOMPLETE",
                    f"accept requires completed external checks: {missing_checks}",
                )
            )

    rationale = admission.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        diagnostics.append(_diag(path, "E-ADMISSION-RATIONALE", "rationale is required"))

    if not isinstance(admission.get("test_fixture", False), bool):
        diagnostics.append(
            _diag(path, "E-ADMISSION-TEST-FIXTURE", "test_fixture must be boolean")
        )

    review_record = submission.get("review_record")
    if decision == "accept" and isinstance(review_record, dict):
        record_id = review_record.get("id")
        if isinstance(record_id, str) and record_id in known_record_ids:
            diagnostics.append(
                _diag(
                    path,
                    "E-ADMISSION-REVIEW-ID-EXISTS",
                    f"review record {record_id!r} already exists",
                )
            )

    return sorted(set(diagnostics))


def admission_receipt(
    admission: Mapping[str, Any],
    submission: Mapping[str, Any],
) -> dict[str, Any]:
    review_record = submission.get("review_record")
    record_payload = review_record if isinstance(review_record, dict) else {}
    return {
        "contract": ADMISSION_CONTRACT,
        "admission_id": admission.get("id"),
        "decision": admission.get("decision"),
        "decided_at": admission.get("decided_at"),
        "submission_contract": submission.get("contract"),
        "coverage_id": submission.get("coverage_id"),
        "task_id": submission.get("task_id"),
        "submission_sha256": canonical_sha256(submission),
        "proposed_record_id": record_payload.get("id"),
        "proposed_record_sha256": canonical_sha256(record_payload),
        "test_fixture": admission.get("test_fixture", False),
        "authority_boundary": (
            "Admission records whether a maintainer accepts a review record into Atlas history. "
            "It does not accept the reviewed knowledge, resolve findings, or promote an entity."
        ),
    }


def admitted_review_record(
    admission: Mapping[str, Any],
    submission: Mapping[str, Any],
    handoff: Mapping[str, Any],
    known_record_ids: set[str] | None = None,
) -> dict[str, Any]:
    diagnostics = validate_admission(
        admission, submission, handoff, known_record_ids=known_record_ids
    )
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        detail = "; ".join(f"{item.code}: {item.message}" for item in errors)
        raise ValueError(f"admission is invalid: {detail}")
    if admission.get("decision") != "accept":
        raise ValueError("only an accept decision may prepare an admitted review record")

    record = intake.normalized_review_record(submission, handoff)
    pre_admission_digest = canonical_sha256(record)
    metadata = record.get("metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    metadata["admission"] = {
        "contract": ADMISSION_CONTRACT,
        "id": admission["id"],
        "decision": "accept",
        "decided_at": admission["decided_at"],
        "decider": admission["decider"],
        "external_verification": admission["external_verification"],
        "rationale": admission["rationale"],
        "submission_sha256": canonical_sha256(submission),
        "pre_admission_record_sha256": pre_admission_digest,
        "test_fixture": admission.get("test_fixture", False),
    }
    record["metadata"] = metadata

    if admission.get("test_fixture") is True:
        record["permits_promotion"] = False

    remaining = gate.validate_review_record(record, "<admitted-review>")
    errors = [item for item in remaining if item.severity == "error"]
    if errors:
        detail = "; ".join(f"{item.code}: {item.message}" for item in errors)
        raise ValueError(f"prepared record is invalid: {detail}")
    return record


def _print_diagnostics(
    diagnostics: Sequence[AdmissionDiagnostic], json_output: bool
) -> None:
    if json_output:
        print(json.dumps([item.to_dict() for item in diagnostics], indent=2, sort_keys=True))
    else:
        for item in diagnostics:
            print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["validate", "receipt", "prepare"])
    parser.add_argument("admission", type=Path)
    parser.add_argument("submission", type=Path)
    parser.add_argument("--handoff", type=Path, required=True)
    parser.add_argument("--records-dir", type=Path, default=DEFAULT_RECORDS_DIR)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    admission, admission_load = load_json(args.admission)
    submission, submission_load = load_json(args.submission)
    handoff, handoff_load = intake.load_handoff(args.handoff)
    known_ids, records_diagnostics = existing_record_ids(args.records_dir)

    diagnostics = list(admission_load) + list(submission_load) + [
        AdmissionDiagnostic(item.path, item.code, item.severity, item.message)
        for item in handoff_load
    ] + list(records_diagnostics)

    if not isinstance(admission, dict):
        if admission is not None:
            diagnostics.append(
                _diag(str(args.admission), "E-ADMISSION-STRUCTURE", "admission must be a mapping")
            )
    if not isinstance(submission, dict):
        if submission is not None:
            diagnostics.append(
                _diag(str(args.submission), "E-ADMISSION-SUBMISSION", "submission must be a mapping")
            )
    if isinstance(admission, dict) and isinstance(submission, dict) and isinstance(handoff, dict):
        diagnostics.extend(
            validate_admission(
                admission,
                submission,
                handoff,
                known_record_ids=known_ids,
                path=str(args.admission),
            )
        )

    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        _print_diagnostics(sorted(set(diagnostics)), args.json)
        return 1

    assert isinstance(admission, dict)
    assert isinstance(submission, dict)
    assert isinstance(handoff, dict)

    if args.command == "validate":
        payload = admission_receipt(admission, submission)
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if args.out is None:
        print(f"{args.command} requires --out", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)

    if args.command == "receipt":
        payload = admission_receipt(admission, submission)
    else:
        try:
            payload = admitted_review_record(
                admission, submission, handoff, known_record_ids=known_ids
            )
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1

    args.out.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(str(args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
