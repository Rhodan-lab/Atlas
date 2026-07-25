#!/usr/bin/env python3
"""Deterministic Phase 1 review-coverage and dependency-impact reporting.

The report aggregates exact-revision review records for a bounded vertical slice.
It never changes lifecycle status, grants authority, or imports external content.
External dependents are opaque identifiers supplied by another repository; this
allows a future Principia bridge without making Atlas depend on Principia.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import phase1_review_gate as gate

COVERAGE_CONTRACT = "atlas-review-coverage/0.1"
COVERAGE_REQUIREMENTS = {"all", "load-bearing"}
ENTITY_ROLES = {"load-bearing", "supporting", "context"}
EXTERNAL_KINDS = {
    "principia-artifact",
    "documentation",
    "application",
    "dataset",
    "other",
}

COVERAGE_ID_RE = re.compile(
    r"^coverage:[a-z0-9]+(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*$"
)

MANIFEST_FIELDS = {
    "contract",
    "id",
    "title",
    "intended_status",
    "decision_at",
    "coverage_requirement",
    "entities",
    "external_dependents",
    "metadata",
}
ENTITY_FIELDS = {
    "id",
    "revision",
    "type",
    "status",
    "staleness",
    "claim_kind",
    "material_flags",
    "translation_of",
    "translation_source_revision",
    "source_current_revision",
    "role",
    "depends_on",
    "required_review_types",
}
EXTERNAL_FIELDS = {
    "id",
    "kind",
    "repository",
    "revision",
    "role",
    "depends_on",
}


@dataclass(frozen=True, order=True)
class CoverageDiagnostic:
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
class EntityCoverage:
    entity_id: str
    revision: int
    role: str
    required_review_types: tuple[str, ...]
    satisfied_review_types: tuple[str, ...]
    missing_review_types: tuple[str, ...]
    review_ids: tuple[str, ...]
    blockers: tuple[str, ...]
    internal_dependents: tuple[str, ...]
    external_dependents: tuple[str, ...]

    @property
    def complete(self) -> bool:
        return not self.missing_review_types and not self.blockers

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "revision": self.revision,
            "role": self.role,
            "complete": self.complete,
            "required_review_types": list(self.required_review_types),
            "satisfied_review_types": list(self.satisfied_review_types),
            "missing_review_types": list(self.missing_review_types),
            "review_ids": list(self.review_ids),
            "blockers": list(self.blockers),
            "internal_dependents": list(self.internal_dependents),
            "external_dependents": list(self.external_dependents),
        }


@dataclass(frozen=True)
class CoverageResult:
    decision: str
    coverage_requirement: str
    required_entity_count: int
    complete_entity_count: int
    entity_results: tuple[EntityCoverage, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision": self.decision,
            "coverage_requirement": self.coverage_requirement,
            "required_entity_count": self.required_entity_count,
            "complete_entity_count": self.complete_entity_count,
            "reasons": list(self.reasons),
            "entities": [item.to_dict() for item in self.entity_results],
        }


def _diag(
    path: str, code: str, message: str, severity: str = "error"
) -> CoverageDiagnostic:
    return CoverageDiagnostic(path, code, severity, message)


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


def load_json(path: Path) -> tuple[Any | None, list[CoverageDiagnostic]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [_diag(str(path), "E-COVERAGE-FILE-READ", str(exc))]
    except json.JSONDecodeError as exc:
        return None, [_diag(str(path), "E-COVERAGE-JSON", str(exc))]


def validate_manifest(
    manifest: Mapping[str, Any], path: str = "<coverage>"
) -> list[CoverageDiagnostic]:
    diagnostics: list[CoverageDiagnostic] = []

    for field in sorted(set(manifest) - MANIFEST_FIELDS):
        diagnostics.append(
            _diag(path, "E-COVERAGE-FIELD-UNKNOWN", f"unknown field {field!r}")
        )

    if manifest.get("contract") != COVERAGE_CONTRACT:
        diagnostics.append(
            _diag(
                path,
                "E-COVERAGE-CONTRACT",
                f"contract must be {COVERAGE_CONTRACT!r}",
            )
        )

    coverage_id = manifest.get("id")
    if not isinstance(coverage_id, str) or not COVERAGE_ID_RE.fullmatch(coverage_id):
        diagnostics.append(
            _diag(path, "E-COVERAGE-ID", "coverage id is not canonical")
        )

    if not isinstance(manifest.get("title"), str) or not manifest.get(
        "title", ""
    ).strip():
        diagnostics.append(_diag(path, "E-COVERAGE-TITLE", "title is required"))

    intended_status = manifest.get("intended_status")
    if intended_status not in gate.LIFECYCLE_STATES:
        diagnostics.append(
            _diag(
                path,
                "E-COVERAGE-INTENDED-STATUS",
                f"unsupported intended status {intended_status!r}",
            )
        )

    if _parse_date(manifest.get("decision_at")) is None:
        diagnostics.append(
            _diag(
                path,
                "E-COVERAGE-DECISION-DATE",
                "decision_at must be an ISO date",
            )
        )

    requirement = manifest.get("coverage_requirement")
    if requirement not in COVERAGE_REQUIREMENTS:
        diagnostics.append(
            _diag(
                path,
                "E-COVERAGE-REQUIREMENT",
                f"unsupported coverage requirement {requirement!r}",
            )
        )

    metadata = manifest.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        diagnostics.append(
            _diag(path, "E-COVERAGE-METADATA", "metadata must be a mapping")
        )

    entities = manifest.get("entities")
    if not isinstance(entities, list) or not entities:
        diagnostics.append(
            _diag(path, "E-COVERAGE-ENTITIES", "entities must be a non-empty list")
        )
        entities = []

    seen: set[tuple[str, int]] = set()
    known_ids: set[str] = set()
    for index, entity in enumerate(entities):
        entity_path = f"{path}#entity[{index}]"
        if not isinstance(entity, dict):
            diagnostics.append(
                _diag(entity_path, "E-COVERAGE-ENTITY", "entity must be a mapping")
            )
            continue
        for field in sorted(set(entity) - ENTITY_FIELDS):
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-ENTITY-FIELD-UNKNOWN",
                    f"unknown field {field!r}",
                )
            )

        entity_id = entity.get("id")
        revision = entity.get("revision")
        if not isinstance(entity_id, str) or not entity_id.strip():
            diagnostics.append(
                _diag(entity_path, "E-COVERAGE-ENTITY-ID", "entity.id is required")
            )
        else:
            known_ids.add(entity_id)
        if not isinstance(revision, int) or revision < 1:
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-ENTITY-REVISION",
                    "entity.revision must be positive",
                )
            )
        elif isinstance(entity_id, str):
            key = (entity_id, revision)
            if key in seen:
                diagnostics.append(
                    _diag(
                        entity_path,
                        "E-COVERAGE-ENTITY-DUPLICATE",
                        f"duplicate exact revision {entity_id}@{revision}",
                    )
                )
            seen.add(key)

        entity_type = entity.get("type")
        if entity_type not in gate.ENTITY_TYPES:
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-ENTITY-TYPE",
                    f"unsupported entity type {entity_type!r}",
                )
            )
        if entity.get("status") not in gate.LIFECYCLE_STATES:
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-ENTITY-STATUS",
                    f"unsupported lifecycle state {entity.get('status')!r}",
                )
            )
        if entity.get("staleness", "current") not in gate.STALENESS_STATES:
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-ENTITY-STALENESS",
                    f"unsupported staleness {entity.get('staleness')!r}",
                )
            )
        if entity_type == "claim" and entity.get("claim_kind") not in gate.CLAIM_KINDS:
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-CLAIM-KIND",
                    f"unsupported claim kind {entity.get('claim_kind')!r}",
                )
            )
        if not isinstance(entity.get("material_flags", []), list):
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-MATERIAL-FLAGS",
                    "material_flags must be a list",
                )
            )
        if entity.get("role") not in ENTITY_ROLES:
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-ENTITY-ROLE",
                    f"unsupported entity role {entity.get('role')!r}",
                )
            )
        if not isinstance(entity.get("depends_on", []), list) or not all(
            isinstance(item, str) for item in entity.get("depends_on", [])
        ):
            diagnostics.append(
                _diag(
                    entity_path,
                    "E-COVERAGE-ENTITY-DEPENDENCIES",
                    "depends_on must be a list of entity IDs",
                )
            )
        explicit = entity.get("required_review_types")
        if explicit is not None:
            if not isinstance(explicit, list) or not all(
                isinstance(item, str) for item in explicit
            ):
                diagnostics.append(
                    _diag(
                        entity_path,
                        "E-COVERAGE-REQUIRED-REVIEWS",
                        "required_review_types must be a list of strings",
                    )
                )
            else:
                for item in sorted(set(explicit) - gate.REVIEW_TYPES):
                    diagnostics.append(
                        _diag(
                            entity_path,
                            "E-COVERAGE-REQUIRED-REVIEW-TYPE",
                            f"unsupported review type {item!r}",
                        )
                    )

        if entity.get("translation_of"):
            source_revision = entity.get("translation_source_revision")
            current_revision = entity.get("source_current_revision")
            if not isinstance(source_revision, int) or source_revision < 1:
                diagnostics.append(
                    _diag(
                        entity_path,
                        "E-COVERAGE-TRANSLATION-SOURCE-REVISION",
                        "translation_source_revision must be positive",
                    )
                )
            if not isinstance(current_revision, int) or current_revision < 1:
                diagnostics.append(
                    _diag(
                        entity_path,
                        "E-COVERAGE-SOURCE-CURRENT-REVISION",
                        "source_current_revision must be positive",
                    )
                )

    external = manifest.get("external_dependents", [])
    if not isinstance(external, list):
        diagnostics.append(
            _diag(
                path,
                "E-COVERAGE-EXTERNAL-DEPENDENTS",
                "external_dependents must be a list",
            )
        )
        external = []
    seen_external: set[str] = set()
    for index, dependent in enumerate(external):
        dependent_path = f"{path}#external[{index}]"
        if not isinstance(dependent, dict):
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL",
                    "external dependent must be a mapping",
                )
            )
            continue
        for field in sorted(set(dependent) - EXTERNAL_FIELDS):
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-FIELD-UNKNOWN",
                    f"unknown field {field!r}",
                )
            )
        dependent_id = dependent.get("id")
        if not isinstance(dependent_id, str) or not dependent_id.strip():
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-ID",
                    "external dependent id is required",
                )
            )
        elif dependent_id in seen_external:
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-DUPLICATE",
                    f"duplicate external dependent {dependent_id!r}",
                )
            )
        else:
            seen_external.add(dependent_id)
        if dependent.get("kind") not in EXTERNAL_KINDS:
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-KIND",
                    f"unsupported external kind {dependent.get('kind')!r}",
                )
            )
        if not isinstance(dependent.get("repository"), str) or not dependent.get(
            "repository", ""
        ).strip():
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-REPOSITORY",
                    "external repository is required",
                )
            )
        revision = dependent.get("revision")
        if revision is not None and (not isinstance(revision, int) or revision < 1):
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-REVISION",
                    "external revision must be positive or omitted",
                )
            )
        if dependent.get("role") not in ENTITY_ROLES:
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-ROLE",
                    f"unsupported external role {dependent.get('role')!r}",
                )
            )
        depends_on = dependent.get("depends_on")
        if not isinstance(depends_on, list) or not depends_on or not all(
            isinstance(item, str) for item in depends_on
        ):
            diagnostics.append(
                _diag(
                    dependent_path,
                    "E-COVERAGE-EXTERNAL-DEPENDENCIES",
                    "external depends_on must be a non-empty list of entity IDs",
                )
            )
        else:
            for target in depends_on:
                if target not in known_ids:
                    diagnostics.append(
                        _diag(
                            dependent_path,
                            "E-COVERAGE-EXTERNAL-TARGET",
                            f"external dependent targets unknown in-scope entity {target!r}",
                        )
                    )

    return sorted(set(diagnostics))


def load_review_records(
    records_dir: Path,
) -> tuple[list[Mapping[str, Any]], list[CoverageDiagnostic]]:
    records: list[Mapping[str, Any]] = []
    diagnostics: list[CoverageDiagnostic] = []
    try:
        paths = sorted(records_dir.glob("*.json"))
    except OSError as exc:
        return [], [_diag(str(records_dir), "E-COVERAGE-RECORD-DIR", str(exc))]

    if not paths:
        diagnostics.append(
            _diag(
                str(records_dir),
                "W-COVERAGE-NO-RECORDS",
                "no review record files were found",
                severity="warning",
            )
        )
        return records, diagnostics

    for path in paths:
        payload, load_diagnostics = gate.load_json(path)
        diagnostics.extend(
            _diag(item.path, item.code, item.message, item.severity)
            for item in load_diagnostics
        )
        if not isinstance(payload, dict):
            if payload is not None:
                diagnostics.append(
                    _diag(
                        str(path),
                        "E-COVERAGE-REVIEW-STRUCTURE",
                        "review record must contain a mapping",
                    )
                )
            continue
        record_diagnostics = gate.validate_review_record(payload, str(path))
        diagnostics.extend(
            _diag(item.path, item.code, item.message, item.severity)
            for item in record_diagnostics
        )
        if not record_diagnostics:
            records.append(payload)
    return records, sorted(set(diagnostics))


def _required_entity(role: str, requirement: str) -> bool:
    return requirement == "all" or role == "load-bearing"


def evaluate_coverage(
    manifest: Mapping[str, Any],
    review_records: Sequence[Mapping[str, Any]],
    path: str = "<coverage>",
) -> tuple[CoverageResult, list[CoverageDiagnostic]]:
    diagnostics = validate_manifest(manifest, path)
    decision_at = _parse_date(manifest.get("decision_at")) or date.min
    requirement = manifest.get("coverage_requirement")
    if requirement not in COVERAGE_REQUIREMENTS:
        requirement = "all"

    entities = [item for item in _as_list(manifest.get("entities")) if isinstance(item, dict)]
    external = [
        item
        for item in _as_list(manifest.get("external_dependents"))
        if isinstance(item, dict)
    ]

    internal_dependents: dict[str, set[str]] = {}
    for entity in entities:
        dependent_id = entity.get("id")
        for target in _as_list(entity.get("depends_on")):
            if isinstance(target, str) and isinstance(dependent_id, str):
                internal_dependents.setdefault(target, set()).add(dependent_id)

    external_dependents: dict[str, set[str]] = {}
    for dependent in external:
        dependent_id = dependent.get("id")
        for target in _as_list(dependent.get("depends_on")):
            if isinstance(target, str) and isinstance(dependent_id, str):
                external_dependents.setdefault(target, set()).add(dependent_id)

    entity_results: list[EntityCoverage] = []
    overall_reasons: list[str] = []
    required_count = 0
    complete_count = 0

    for entity in sorted(
        entities,
        key=lambda item: (str(item.get("id", "")), int(item.get("revision", 0) or 0)),
    ):
        entity_id = entity.get("id") if isinstance(entity.get("id"), str) else "unknown"
        revision = entity.get("revision") if isinstance(entity.get("revision"), int) else 0
        role = entity.get("role") if entity.get("role") in ENTITY_ROLES else "context"
        required = gate.required_review_types(entity)
        explicit = entity.get("required_review_types")
        if isinstance(explicit, list):
            required |= {item for item in explicit if item in gate.REVIEW_TYPES}

        exact_records = [
            record
            for record in review_records
            if isinstance(record.get("entity"), dict)
            and record.get("entity", {}).get("id") == entity_id
            and record.get("entity", {}).get("revision") == revision
        ]
        review_ids = tuple(
            sorted(
                str(record.get("id"))
                for record in exact_records
                if isinstance(record.get("id"), str)
            )
        )
        satisfied: set[str] = set()
        blockers: list[str] = []

        staleness = entity.get("staleness", "current")
        if staleness not in {"current", "unaffected", "updated"}:
            blockers.append(f"entity staleness is {staleness!r}")
        if entity.get("translation_of"):
            if entity.get("translation_source_revision") != entity.get(
                "source_current_revision"
            ):
                blockers.append(
                    "translation source revision does not match current source revision"
                )

        for review_type in sorted(required):
            candidates = [
                record
                for record in exact_records
                if record.get("review_type") == review_type
            ]
            accepted = False
            candidate_reasons: list[str] = []
            for record in candidates:
                passing, reasons = gate._review_is_passing(record, decision_at, entity)
                if not passing:
                    candidate_reasons.extend(reasons)
                    continue
                if not gate._review_authority_satisfies(review_type, record, entity):
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
            elif candidate_reasons:
                blockers.extend(candidate_reasons)

        missing = required - satisfied
        required_for_gate = _required_entity(role, requirement)
        if required_for_gate:
            required_count += 1
            if not missing and not blockers:
                complete_count += 1
            else:
                overall_reasons.append(
                    f"{entity_id}@{revision} is missing acceptable review coverage"
                )

        entity_results.append(
            EntityCoverage(
                entity_id=entity_id,
                revision=revision,
                role=role,
                required_review_types=tuple(sorted(required)),
                satisfied_review_types=tuple(sorted(satisfied)),
                missing_review_types=tuple(sorted(missing)),
                review_ids=review_ids,
                blockers=tuple(dict.fromkeys(blockers)),
                internal_dependents=tuple(sorted(internal_dependents.get(entity_id, set()))),
                external_dependents=tuple(sorted(external_dependents.get(entity_id, set()))),
            )
        )

    has_errors = any(item.severity == "error" for item in diagnostics)
    decision = (
        "coverage-complete"
        if required_count > 0 and complete_count == required_count and not has_errors
        else "blocked"
    )
    if required_count == 0:
        overall_reasons.append("no entity is required by the selected coverage policy")
    if has_errors:
        overall_reasons.append("coverage manifest or review records have contract errors")

    result = CoverageResult(
        decision=decision,
        coverage_requirement=requirement,
        required_entity_count=required_count,
        complete_entity_count=complete_count,
        entity_results=tuple(entity_results),
        reasons=tuple(dict.fromkeys(overall_reasons)),
    )
    return result, sorted(set(diagnostics))


def render_report(
    manifest: Mapping[str, Any],
    result: CoverageResult,
    diagnostics: Sequence[CoverageDiagnostic],
) -> str:
    lines = [
        "# Atlas Phase 1 Coverage Report",
        "",
        f"- Coverage ID: `{manifest.get('id', 'unknown')}`",
        f"- Title: {manifest.get('title', 'unknown')}",
        f"- Intended lifecycle state: `{manifest.get('intended_status', 'unknown')}`",
        f"- Coverage policy: `{result.coverage_requirement}`",
        f"- Decision date: `{manifest.get('decision_at', 'unknown')}`",
        f"- Decision: **{result.decision}**",
        f"- Complete required entities: `{result.complete_entity_count}/{result.required_entity_count}`",
        "",
        "## Entity coverage",
        "",
        "| Entity revision | Role | Required reviews | Satisfied | Missing | Dependents |",
        "|---|---|---|---|---|---|",
    ]

    for item in result.entity_results:
        dependents = list(item.internal_dependents) + list(item.external_dependents)
        lines.append(
            "| "
            f"`{item.entity_id}@{item.revision}` | "
            f"{item.role} | "
            f"{', '.join(item.required_review_types) or 'none'} | "
            f"{', '.join(item.satisfied_review_types) or 'none'} | "
            f"{', '.join(item.missing_review_types) or 'none'} | "
            f"{', '.join(dependents) or 'none'} |"
        )

    lines.extend(["", "## Blocking detail", ""])
    blocked_entities = [item for item in result.entity_results if not item.complete]
    if not blocked_entities:
        lines.append("- None")
    else:
        for item in blocked_entities:
            lines.append(f"### `{item.entity_id}@{item.revision}`")
            lines.append("")
            lines.append(
                f"- Missing review types: {', '.join(item.missing_review_types) or 'none'}"
            )
            lines.append(f"- Review records found: {', '.join(item.review_ids) or 'none'}")
            if item.blockers:
                lines.extend(f"- Blocker: {blocker}" for blocker in item.blockers)
            if item.internal_dependents:
                lines.append(
                    f"- Internal dependents: {', '.join(item.internal_dependents)}"
                )
            if item.external_dependents:
                lines.append(
                    f"- External dependents: {', '.join(item.external_dependents)}"
                )
            lines.append("")

    lines.extend(["## Overall reasons", ""])
    if result.reasons:
        lines.extend(f"- {reason}" for reason in result.reasons)
    else:
        lines.append("- None")

    lines.extend(["", "## Contract diagnostics", ""])
    if diagnostics:
        lines.extend(
            f"- `{item.code}`: {item.message} ({item.path})" for item in diagnostics
        )
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "External dependents are opaque impact references. Atlas does not validate their pedagogical or release status and does not inherit authority across repositories.",
            "",
            "This report is deterministic governance output. It never changes lifecycle status or substitutes for accountable human review.",
            "",
        ]
    )
    return "\n".join(lines)


def _print_diagnostics(
    diagnostics: Iterable[CoverageDiagnostic], json_output: bool = False
) -> None:
    items = list(diagnostics)
    if json_output:
        print(json.dumps([item.to_dict() for item in items], indent=2, sort_keys=True))
    else:
        for item in items:
            print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate-manifest")
    validate_parser.add_argument("paths", nargs="+", type=Path)
    validate_parser.add_argument("--json", action="store_true")

    coverage_parser = subparsers.add_parser("coverage")
    coverage_parser.add_argument("path", type=Path)
    coverage_parser.add_argument(
        "--records-dir",
        type=Path,
        default=Path("content/reviews/records"),
    )
    coverage_parser.add_argument(
        "--expect", choices=["blocked", "coverage-complete"]
    )
    coverage_parser.add_argument("--json", action="store_true")
    coverage_parser.add_argument("--report", type=Path)

    args = parser.parse_args(argv)

    if args.command == "validate-manifest":
        diagnostics: list[CoverageDiagnostic] = []
        for path in args.paths:
            payload, load_diagnostics = load_json(path)
            diagnostics.extend(load_diagnostics)
            if isinstance(payload, dict):
                diagnostics.extend(validate_manifest(payload, str(path)))
            elif payload is not None:
                diagnostics.append(
                    _diag(
                        str(path),
                        "E-COVERAGE-STRUCTURE",
                        "coverage file must contain a mapping",
                    )
                )
        diagnostics = sorted(set(diagnostics))
        _print_diagnostics(diagnostics, args.json)
        return 1 if any(item.severity == "error" for item in diagnostics) else 0

    payload, diagnostics = load_json(args.path)
    records, record_diagnostics = load_review_records(args.records_dir)
    diagnostics.extend(record_diagnostics)
    if not isinstance(payload, dict):
        if payload is not None:
            diagnostics.append(
                _diag(
                    str(args.path),
                    "E-COVERAGE-STRUCTURE",
                    "coverage file must contain a mapping",
                )
            )
        result = CoverageResult(
            decision="blocked",
            coverage_requirement="all",
            required_entity_count=0,
            complete_entity_count=0,
            entity_results=(),
            reasons=("coverage manifest is invalid",),
        )
    else:
        result, evaluation_diagnostics = evaluate_coverage(
            payload, records, str(args.path)
        )
        diagnostics.extend(evaluation_diagnostics)
        diagnostics = sorted(set(diagnostics))

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

    has_errors = any(item.severity == "error" for item in diagnostics)
    if args.expect:
        return 0 if result.decision == args.expect and not has_errors else 1
    return 0 if result.decision == "coverage-complete" and not has_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
