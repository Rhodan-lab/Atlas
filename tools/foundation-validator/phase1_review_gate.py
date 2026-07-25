#!/usr/bin/env python3
"""Phase 1 review-record and lifecycle promotion gate for Atlas.

This tool validates review governance. It does not judge domain truth, write
content, or perform lifecycle transitions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

REVIEW_CONTRACT = "atlas-review/0.1"
PROMOTION_CONTRACT = "atlas-promotion/0.1"

REVIEW_TYPES = {
    "structural",
    "editorial",
    "source",
    "domain",
    "methodological",
    "reproducibility",
    "ethical",
    "translation",
    "legal-context",
    "conflict",
}
REVIEWER_KINDS = {"machine", "ai-assisted", "human"}
INDEPENDENCE = {"internal", "independent", "not-applicable"}
OUTCOMES = {
    "pass",
    "pass-with-minor-findings",
    "changes-required",
    "blocked",
    "not-applicable",
}
FINDING_SEVERITIES = {"critical", "major", "minor", "info"}
FINDING_STATUSES = {"open", "resolved", "accepted-risk", "not-applicable"}
STALENESS_STATES = {
    "current",
    "possibly-stale",
    "review-required",
    "confirmed-stale",
    "unaffected",
    "updated",
}
LIFECYCLE_STATES = {
    "draft",
    "in-review",
    "reviewed",
    "contested",
    "deprecated",
    "retracted",
}
ENTITY_TYPES = {
    "source",
    "evidence",
    "claim",
    "concept",
    "model",
    "question",
    "synthesis",
}
CLAIM_KINDS = {
    "factual",
    "descriptive",
    "causal",
    "correlational",
    "definitional",
    "methodological",
    "interpretive",
    "predictive",
    "normative",
    "hypothetical",
    "model-derived",
}

REVIEW_ID_RE = re.compile(
    r"^review:[a-z0-9]+(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*$"
)
FINDING_ID_RE = re.compile(
    r"^finding:[a-z0-9]+(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*$"
)

REVIEW_FIELDS = {
    "contract",
    "id",
    "entity",
    "review_type",
    "reviewer",
    "completed_at",
    "review_horizon",
    "outcome",
    "findings",
    "summary",
    "permits_promotion",
    "supersedes",
    "metadata",
}
REVIEWER_FIELDS = {
    "display_name",
    "kind",
    "independence",
    "qualification",
    "accountable",
    "conflicts",
}
FINDING_FIELDS = {
    "id",
    "severity",
    "status",
    "summary",
    "rationale",
    "affected_fields",
    "suggested_action",
    "references",
    "resolution_note",
}
PROMOTION_FIELDS = {
    "contract",
    "entity",
    "requested_status",
    "reviews",
    "decision_at",
    "accepted_by",
    "required_review_types",
    "transition",
}


@dataclass(frozen=True, order=True)
class Diagnostic:
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


@dataclass(frozen=True)
class PromotionResult:
    decision: str
    required_review_types: tuple[str, ...]
    satisfied_review_types: tuple[str, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "required_review_types": list(self.required_review_types),
            "satisfied_review_types": list(self.satisfied_review_types),
            "reasons": list(self.reasons),
        }


def _diag(path: str, code: str, message: str, severity: str = "error") -> Diagnostic:
    return Diagnostic(path, code, severity, message)


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _parse_date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def load_json(path: Path) -> tuple[Any | None, list[Diagnostic]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [_diag(str(path), "E-REVIEW-FILE-READ", str(exc))]
    except json.JSONDecodeError as exc:
        return None, [_diag(str(path), "E-REVIEW-JSON", str(exc))]


def validate_review_record(
    record: Mapping[str, Any], path: str = "<review>"
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    unknown = sorted(set(record) - REVIEW_FIELDS)
    for field in unknown:
        diagnostics.append(
            _diag(path, "E-REVIEW-FIELD-UNKNOWN", f"unknown field {field!r}")
        )

    if record.get("contract") != REVIEW_CONTRACT:
        diagnostics.append(
            _diag(path, "E-REVIEW-CONTRACT", f"contract must be {REVIEW_CONTRACT!r}")
        )

    review_id = record.get("id")
    if not isinstance(review_id, str) or not REVIEW_ID_RE.fullmatch(review_id):
        diagnostics.append(_diag(path, "E-REVIEW-ID", "review id is not canonical"))

    entity = record.get("entity")
    if not isinstance(entity, dict):
        diagnostics.append(_diag(path, "E-REVIEW-ENTITY", "entity mapping is required"))
        entity = {}
    if not isinstance(entity.get("id"), str):
        diagnostics.append(_diag(path, "E-REVIEW-ENTITY-ID", "entity.id is required"))
    if not isinstance(entity.get("revision"), int) or entity.get("revision", 0) < 1:
        diagnostics.append(
            _diag(
                path,
                "E-REVIEW-ENTITY-REVISION",
                "entity.revision must be positive",
            )
        )

    review_type = record.get("review_type")
    if review_type not in REVIEW_TYPES:
        diagnostics.append(
            _diag(path, "E-REVIEW-TYPE", f"unsupported review type {review_type!r}")
        )

    reviewer = record.get("reviewer")
    if not isinstance(reviewer, dict):
        diagnostics.append(_diag(path, "E-REVIEWER", "reviewer mapping is required"))
        reviewer = {}
    else:
        for field in sorted(set(reviewer) - REVIEWER_FIELDS):
            diagnostics.append(
                _diag(
                    path,
                    "E-REVIEWER-FIELD-UNKNOWN",
                    f"unknown reviewer field {field!r}",
                )
            )

    if not isinstance(reviewer.get("display_name"), str) or not reviewer.get(
        "display_name", ""
    ).strip():
        diagnostics.append(
            _diag(path, "E-REVIEWER-NAME", "reviewer.display_name is required")
        )
    kind = reviewer.get("kind")
    if kind not in REVIEWER_KINDS:
        diagnostics.append(
            _diag(path, "E-REVIEWER-KIND", f"unsupported reviewer kind {kind!r}")
        )
    independence = reviewer.get("independence")
    if independence not in INDEPENDENCE:
        diagnostics.append(
            _diag(
                path,
                "E-REVIEWER-INDEPENDENCE",
                f"unsupported independence {independence!r}",
            )
        )
    if not isinstance(reviewer.get("qualification"), str) or not reviewer.get(
        "qualification", ""
    ).strip():
        diagnostics.append(
            _diag(
                path,
                "E-REVIEWER-QUALIFICATION",
                "reviewer.qualification is required",
            )
        )
    accountable = reviewer.get("accountable")
    if not isinstance(accountable, bool):
        diagnostics.append(
            _diag(
                path,
                "E-REVIEWER-ACCOUNTABLE",
                "reviewer.accountable must be boolean",
            )
        )
    if not isinstance(reviewer.get("conflicts"), list):
        diagnostics.append(
            _diag(
                path,
                "E-REVIEWER-CONFLICTS",
                "reviewer.conflicts must be a list",
            )
        )
    if kind in {"machine", "ai-assisted"} and accountable is True:
        diagnostics.append(
            _diag(
                path,
                "E-NONHUMAN-ACCOUNTABILITY",
                "machine and AI-assisted review cannot be accountable",
            )
        )

    completed = _parse_date(record.get("completed_at"))
    if completed is None:
        diagnostics.append(
            _diag(
                path,
                "E-REVIEW-COMPLETED-AT",
                "completed_at must be an ISO date",
            )
        )
    horizon_value = record.get("review_horizon")
    if horizon_value is not None:
        horizon = _parse_date(horizon_value)
        if horizon is None:
            diagnostics.append(
                _diag(
                    path,
                    "E-REVIEW-HORIZON",
                    "review_horizon must be null or ISO date",
                )
            )
        elif completed and horizon < completed:
            diagnostics.append(
                _diag(
                    path,
                    "E-REVIEW-HORIZON",
                    "review_horizon cannot precede completed_at",
                )
            )

    outcome = record.get("outcome")
    if outcome not in OUTCOMES:
        diagnostics.append(
            _diag(path, "E-REVIEW-OUTCOME", f"unsupported outcome {outcome!r}")
        )

    findings = record.get("findings")
    if not isinstance(findings, list):
        diagnostics.append(_diag(path, "E-REVIEW-FINDINGS", "findings must be a list"))
        findings = []
    seen_findings: set[str] = set()
    for index, finding in enumerate(findings):
        finding_path = f"{path}#finding[{index}]"
        if not isinstance(finding, dict):
            diagnostics.append(
                _diag(finding_path, "E-FINDING-STRUCTURE", "finding must be a mapping")
            )
            continue
        for field in sorted(set(finding) - FINDING_FIELDS):
            diagnostics.append(
                _diag(
                    finding_path,
                    "E-FINDING-FIELD-UNKNOWN",
                    f"unknown field {field!r}",
                )
            )
        finding_id = finding.get("id")
        if not isinstance(finding_id, str) or not FINDING_ID_RE.fullmatch(finding_id):
            diagnostics.append(
                _diag(finding_path, "E-FINDING-ID", "finding id is not canonical")
            )
        elif finding_id in seen_findings:
            diagnostics.append(
                _diag(
                    finding_path,
                    "E-FINDING-DUPLICATE",
                    f"duplicate finding {finding_id!r}",
                )
            )
        else:
            seen_findings.add(finding_id)
        severity = finding.get("severity")
        status = finding.get("status")
        if severity not in FINDING_SEVERITIES:
            diagnostics.append(
                _diag(
                    finding_path,
                    "E-FINDING-SEVERITY",
                    f"unsupported severity {severity!r}",
                )
            )
        if status not in FINDING_STATUSES:
            diagnostics.append(
                _diag(
                    finding_path,
                    "E-FINDING-STATUS",
                    f"unsupported status {status!r}",
                )
            )
        if not isinstance(finding.get("summary"), str) or not finding.get(
            "summary", ""
        ).strip():
            diagnostics.append(
                _diag(finding_path, "E-FINDING-SUMMARY", "finding summary is required")
            )
        if not isinstance(finding.get("rationale"), str) or not finding.get(
            "rationale", ""
        ).strip():
            diagnostics.append(
                _diag(
                    finding_path,
                    "E-FINDING-RATIONALE",
                    "finding rationale is required",
                )
            )
        if severity == "critical" and status == "accepted-risk":
            diagnostics.append(
                _diag(
                    finding_path,
                    "E-CRITICAL-RISK-ACCEPTANCE",
                    "critical findings cannot be accepted risk",
                )
            )
        if severity in {"critical", "major"} and status == "resolved":
            if not isinstance(finding.get("resolution_note"), str) or not finding.get(
                "resolution_note", ""
            ).strip():
                diagnostics.append(
                    _diag(
                        finding_path,
                        "E-FINDING-RESOLUTION-NOTE",
                        "resolved major/critical finding needs resolution_note",
                    )
                )

    if not isinstance(record.get("summary"), str) or not record.get(
        "summary", ""
    ).strip():
        diagnostics.append(_diag(path, "E-REVIEW-SUMMARY", "summary is required"))
    permits = record.get("permits_promotion")
    if not isinstance(permits, bool):
        diagnostics.append(
            _diag(
                path,
                "E-REVIEW-PERMITS",
                "permits_promotion must be boolean",
            )
        )
    if kind in {"machine", "ai-assisted"} and permits is True:
        diagnostics.append(
            _diag(
                path,
                "E-NONHUMAN-PROMOTION",
                "machine and AI-assisted review cannot permit promotion",
            )
        )

    open_serious = [
        finding
        for finding in findings
        if isinstance(finding, dict)
        and finding.get("severity") in {"critical", "major"}
        and finding.get("status") in {"open", "accepted-risk"}
    ]
    open_nonminor = [
        finding
        for finding in findings
        if isinstance(finding, dict)
        and finding.get("status") == "open"
        and finding.get("severity") not in {"minor", "info"}
    ]
    if outcome == "pass" and any(
        isinstance(finding, dict) and finding.get("status") == "open"
        for finding in findings
    ):
        diagnostics.append(
            _diag(
                path,
                "E-REVIEW-PASS-OPEN-FINDING",
                "pass cannot retain open findings",
            )
        )
    if outcome == "pass-with-minor-findings" and open_nonminor:
        diagnostics.append(
            _diag(
                path,
                "E-REVIEW-MINOR-OUTCOME",
                "pass-with-minor-findings has non-minor open findings",
            )
        )
    if permits is True and open_serious:
        diagnostics.append(
            _diag(
                path,
                "E-REVIEW-PROMOTION-SERIOUS-FINDING",
                "promotion cannot be permitted with open serious findings",
            )
        )
    if permits is True and outcome not in {"pass", "pass-with-minor-findings"}:
        diagnostics.append(
            _diag(
                path,
                "E-REVIEW-PROMOTION-OUTCOME",
                "promotion requires a passing outcome",
            )
        )

    return sorted(diagnostics)


def required_review_types(entity: Mapping[str, Any]) -> set[str]:
    entity_type = entity.get("type")
    required: set[str] = {"structural"}
    translated = bool(entity.get("translation_of"))
    flags = set(_as_list(entity.get("material_flags")))

    if entity_type == "source":
        required |= {"source"}
    elif entity_type == "evidence":
        required |= {"source"}
        if (
            "empirical-method" in flags
            or "measurement" in flags
            or "transformation" in flags
        ):
            required.add("methodological")
        if "generated" in flags or "derived" in flags:
            required.add("reproducibility")
    elif entity_type == "claim":
        required.add("editorial")
        kind = entity.get("claim_kind")
        if kind in {
            "factual",
            "descriptive",
            "definitional",
            "interpretive",
            "methodological",
        }:
            required |= {"source", "domain"}
        elif kind in {"causal", "correlational"}:
            required |= {"source", "domain", "methodological"}
        elif kind == "model-derived":
            required |= {"domain", "methodological", "reproducibility"}
        elif kind == "normative":
            required.add("ethical")
        elif kind == "predictive":
            required |= {"source", "domain", "methodological"}
        if "legal" in flags:
            required.add("legal-context")
    elif entity_type == "concept":
        required |= {"editorial", "domain"}
    elif entity_type == "model":
        required |= {"editorial", "domain", "methodological"}
        if "executable" in flags or "derived" in flags:
            required.add("reproducibility")
    elif entity_type == "question":
        required.add("editorial")
        if "contested-terminology" in flags:
            required.add("domain")
    elif entity_type == "synthesis":
        required |= {"editorial", "source", "domain"}
        if "empirical-inference" in flags or "model-inference" in flags:
            required.add("methodological")
        if "normative" in flags:
            required.add("ethical")
        if "legal" in flags:
            required.add("legal-context")

    if translated:
        required.add("translation")
    return required


def _review_authority_satisfies(
    review_type: str, record: Mapping[str, Any], entity: Mapping[str, Any]
) -> bool:
    reviewer = record.get("reviewer")
    if not isinstance(reviewer, dict):
        return False
    kind = reviewer.get("kind")
    independence = reviewer.get("independence")
    accountable = reviewer.get("accountable") is True

    if review_type == "structural":
        return kind in {"machine", "human"}
    if review_type == "reproducibility" and "fully-specified-reproducibility" in set(
        _as_list(entity.get("material_flags"))
    ):
        return kind in {"machine", "human"}
    if review_type in {"editorial", "source", "conflict"}:
        return (
            kind == "human"
            and accountable
            and independence in {"internal", "independent"}
        )
    if review_type in {
        "domain",
        "methodological",
        "ethical",
        "translation",
        "legal-context",
    }:
        return kind == "human" and accountable and independence == "independent"
    if review_type == "reproducibility":
        return kind == "human" and accountable and independence == "independent"
    return False


def _review_is_passing(
    record: Mapping[str, Any], decision_at: date, entity: Mapping[str, Any]
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    outcome = record.get("outcome")
    if outcome not in {"pass", "pass-with-minor-findings"}:
        reasons.append(f"review {record.get('id')} outcome is {outcome!r}")
    findings = record.get("findings")
    if isinstance(findings, list):
        for finding in findings:
            if not isinstance(finding, dict):
                continue
            if finding.get("severity") in {"critical", "major"} and finding.get(
                "status"
            ) in {"open", "accepted-risk"}:
                reasons.append(
                    f"review {record.get('id')} has unresolved "
                    f"{finding.get('severity')} finding {finding.get('id')}"
                )
    horizon = _parse_date(record.get("review_horizon"))
    if horizon and horizon < decision_at:
        reasons.append(f"review {record.get('id')} expired on {horizon.isoformat()}")
    target = record.get("entity")
    if (
        not isinstance(target, dict)
        or target.get("id") != entity.get("id")
        or target.get("revision") != entity.get("revision")
    ):
        reasons.append(f"review {record.get('id')} targets another entity revision")
    return not reasons, reasons


def evaluate_promotion(
    manifest: Mapping[str, Any], path: str = "<promotion>"
) -> tuple[PromotionResult, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    for field in sorted(set(manifest) - PROMOTION_FIELDS):
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-FIELD-UNKNOWN",
                f"unknown field {field!r}",
            )
        )
    if manifest.get("contract") != PROMOTION_CONTRACT:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-CONTRACT",
                f"contract must be {PROMOTION_CONTRACT!r}",
            )
        )

    entity = manifest.get("entity")
    if not isinstance(entity, dict):
        diagnostics.append(
            _diag(path, "E-PROMOTION-ENTITY", "entity mapping is required")
        )
        entity = {}
    entity_type = entity.get("type")
    if entity_type not in ENTITY_TYPES:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-ENTITY-TYPE",
                f"unsupported entity type {entity_type!r}",
            )
        )
    if not isinstance(entity.get("id"), str):
        diagnostics.append(
            _diag(path, "E-PROMOTION-ENTITY-ID", "entity.id is required")
        )
    if not isinstance(entity.get("revision"), int) or entity.get("revision", 0) < 1:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-ENTITY-REVISION",
                "entity.revision must be positive",
            )
        )
    current_status = entity.get("status")
    if current_status not in LIFECYCLE_STATES:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-CURRENT-STATUS",
                f"unsupported current status {current_status!r}",
            )
        )
    staleness = entity.get("staleness", "current")
    if staleness not in STALENESS_STATES:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-STALENESS",
                f"unsupported staleness {staleness!r}",
            )
        )

    requested = manifest.get("requested_status")
    if requested not in LIFECYCLE_STATES:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-REQUESTED-STATUS",
                f"unsupported requested status {requested!r}",
            )
        )

    decision_at = _parse_date(manifest.get("decision_at"))
    if decision_at is None:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-DECISION-DATE",
                "decision_at must be an ISO date",
            )
        )
        decision_at = date.min

    accepted_by = manifest.get("accepted_by")
    if not isinstance(accepted_by, dict):
        diagnostics.append(
            _diag(path, "E-PROMOTION-ACCEPTOR", "accepted_by mapping is required")
        )
        accepted_by = {}
    if accepted_by.get("kind") != "human" or accepted_by.get("accountable") is not True:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-HUMAN-ACCEPTANCE",
                "an accountable human must accept the transition",
            )
        )
    if not isinstance(accepted_by.get("display_name"), str) or not accepted_by.get(
        "display_name", ""
    ).strip():
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-ACCEPTOR-NAME",
                "accepted_by.display_name is required",
            )
        )

    reviews = manifest.get("reviews")
    if not isinstance(reviews, list):
        diagnostics.append(
            _diag(path, "E-PROMOTION-REVIEWS", "reviews must be a list")
        )
        reviews = []

    valid_records: list[Mapping[str, Any]] = []
    for index, review in enumerate(reviews):
        review_path = f"{path}#review[{index}]"
        if not isinstance(review, dict):
            diagnostics.append(
                _diag(review_path, "E-REVIEW-STRUCTURE", "review must be a mapping")
            )
            continue
        record_diagnostics = validate_review_record(review, review_path)
        diagnostics.extend(record_diagnostics)
        if not record_diagnostics:
            valid_records.append(review)

    explicit_required = manifest.get("required_review_types")
    required = (
        set(_as_list(explicit_required))
        if explicit_required is not None
        else required_review_types(entity)
    )
    unknown_required = sorted(required - REVIEW_TYPES)
    for item in unknown_required:
        diagnostics.append(
            _diag(
                path,
                "E-PROMOTION-REQUIRED-TYPE",
                f"unsupported required review type {item!r}",
            )
        )
    required -= set(unknown_required)

    reasons: list[str] = []
    satisfied: set[str] = set()

    if requested == "reviewed":
        if staleness not in {"current", "unaffected", "updated"}:
            reasons.append(f"entity staleness is {staleness!r}")
        if entity.get("translation_of"):
            source_revision = entity.get("translation_source_revision")
            current_source_revision = entity.get("source_current_revision")
            if source_revision != current_source_revision:
                reasons.append(
                    "translation source revision does not match current source revision"
                )
        for review_type in sorted(required):
            candidates = [
                record
                for record in valid_records
                if record.get("review_type") == review_type
            ]
            accepted = False
            candidate_reasons: list[str] = []
            for record in candidates:
                passing, record_reasons = _review_is_passing(
                    record, decision_at, entity
                )
                if not passing:
                    candidate_reasons.extend(record_reasons)
                    continue
                if not _review_authority_satisfies(review_type, record, entity):
                    candidate_reasons.append(
                        f"review {record.get('id')} lacks authority for {review_type}"
                    )
                    continue
                if (
                    record.get("reviewer", {}).get("kind") == "human"
                    and record.get("permits_promotion") is not True
                ):
                    candidate_reasons.append(
                        f"review {record.get('id')} does not permit promotion"
                    )
                    continue
                accepted = True
                break
            if accepted:
                satisfied.add(review_type)
            else:
                reasons.append(f"missing acceptable {review_type} review")
                reasons.extend(candidate_reasons)
        decision = "eligible" if not reasons and not diagnostics else "blocked"

    elif requested == "contested":
        transition = manifest.get("transition")
        if not isinstance(transition, dict):
            reasons.append("contested transition metadata is required")
        else:
            if len(_as_list(transition.get("positions"))) < 2:
                reasons.append("contested state requires at least two material positions")
            if not _as_list(transition.get("unresolved_questions")):
                reasons.append("contested state requires unresolved questions")
            if not isinstance(transition.get("reason"), str) or not transition.get(
                "reason", ""
            ).strip():
                reasons.append("contested state requires a reason")
        decision = "eligible" if not reasons and not diagnostics else "blocked"

    elif requested in {"deprecated", "retracted"}:
        transition = manifest.get("transition")
        if not isinstance(transition, dict):
            reasons.append(f"{requested} transition metadata is required")
        else:
            if not isinstance(transition.get("reason"), str) or not transition.get(
                "reason", ""
            ).strip():
                reasons.append(f"{requested} state requires a reason")
            if _parse_date(transition.get("effective_date")) is None:
                reasons.append(f"{requested} state requires effective_date")
            if "replacement" not in transition:
                reasons.append(
                    f"{requested} state requires explicit replacement field"
                )
            if not isinstance(transition.get("affected_dependents"), list):
                reasons.append(
                    f"{requested} state requires affected_dependents list"
                )
            if requested == "retracted":
                if not _as_list(transition.get("evidence")):
                    reasons.append("retracted state requires evidence")
                if transition.get("current_use_prohibited") is not True:
                    reasons.append(
                        "retracted state must prohibit current evidentiary use"
                    )
        decision = "eligible" if not reasons and not diagnostics else "blocked"

    elif requested == "in-review":
        if current_status != "draft":
            reasons.append("only draft entities enter in-review through this gate")
        if "structural" not in {
            record.get("review_type") for record in valid_records
        }:
            reasons.append("structural review record is required")
        decision = "eligible" if not reasons and not diagnostics else "blocked"
    else:
        reasons.append(f"transition to {requested!r} is not implemented")
        decision = "blocked"

    result = PromotionResult(
        decision=decision,
        required_review_types=tuple(sorted(required)),
        satisfied_review_types=tuple(sorted(satisfied)),
        reasons=tuple(dict.fromkeys(reasons)),
    )
    return result, sorted(diagnostics)


def render_report(
    manifest: Mapping[str, Any],
    result: PromotionResult,
    diagnostics: Sequence[Diagnostic],
) -> str:
    entity = manifest.get("entity") if isinstance(manifest.get("entity"), dict) else {}
    lines = [
        "# Atlas Promotion Gate Report",
        "",
        f"- Entity: `{entity.get('id', 'unknown')}`",
        f"- Revision: `{entity.get('revision', 'unknown')}`",
        f"- Current status: `{entity.get('status', 'unknown')}`",
        f"- Requested status: `{manifest.get('requested_status', 'unknown')}`",
        f"- Decision: **{result.decision}**",
        "",
        "## Review coverage",
        "",
        f"- Required: {', '.join(result.required_review_types) or 'none'}",
        f"- Satisfied: {', '.join(result.satisfied_review_types) or 'none'}",
        "",
        "## Blocking reasons",
        "",
    ]
    if result.reasons:
        lines.extend(f"- {reason}" for reason in result.reasons)
    else:
        lines.append("- None")
    lines.extend(["", "## Contract diagnostics", ""])
    if diagnostics:
        lines.extend(
            f"- `{diagnostic.code}`: {diagnostic.message} ({diagnostic.path})"
            for diagnostic in diagnostics
        )
    else:
        lines.append("- None")
    lines.extend(
        [
            "",
            "This report is deterministic governance output. It does not itself change lifecycle status.",
            "",
        ]
    )
    return "\n".join(lines)


def _print_diagnostics(
    diagnostics: Iterable[Diagnostic], json_output: bool = False
) -> None:
    items = list(diagnostics)
    if json_output:
        print(json.dumps([item.to_dict() for item in items], indent=2, sort_keys=True))
    else:
        for item in items:
            print(
                f"{item.severity.upper()} {item.code} {item.path}: {item.message}"
            )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate-record")
    validate_parser.add_argument("paths", nargs="+", type=Path)
    validate_parser.add_argument("--json", action="store_true")

    promotion_parser = subparsers.add_parser("promotion")
    promotion_parser.add_argument("path", type=Path)
    promotion_parser.add_argument("--json", action="store_true")
    promotion_parser.add_argument("--report", type=Path)

    args = parser.parse_args(argv)

    if args.command == "validate-record":
        diagnostics: list[Diagnostic] = []
        for path in args.paths:
            payload, load_diagnostics = load_json(path)
            diagnostics.extend(load_diagnostics)
            if isinstance(payload, dict):
                diagnostics.extend(validate_review_record(payload, str(path)))
            elif payload is not None:
                diagnostics.append(
                    _diag(
                        str(path),
                        "E-REVIEW-STRUCTURE",
                        "review file must contain a mapping",
                    )
                )
        diagnostics = sorted(diagnostics)
        _print_diagnostics(diagnostics, args.json)
        return 1 if any(item.severity == "error" for item in diagnostics) else 0

    payload, diagnostics = load_json(args.path)
    if not isinstance(payload, dict):
        if payload is not None:
            diagnostics.append(
                _diag(
                    str(args.path),
                    "E-PROMOTION-STRUCTURE",
                    "promotion file must contain a mapping",
                )
            )
        result = PromotionResult(
            "blocked", (), (), ("promotion manifest is invalid",)
        )
    else:
        result, evaluation_diagnostics = evaluate_promotion(
            payload, str(args.path)
        )
        diagnostics.extend(evaluation_diagnostics)

    if args.report and isinstance(payload, dict):
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(
            render_report(payload, result, diagnostics), encoding="utf-8"
        )

    if args.json:
        print(
            json.dumps(
                {
                    "result": result.to_dict(),
                    "diagnostics": [item.to_dict() for item in diagnostics],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
        _print_diagnostics(diagnostics)

    return (
        0
        if result.decision == "eligible"
        and not any(item.severity == "error" for item in diagnostics)
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
