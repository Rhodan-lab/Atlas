#!/usr/bin/env python3
"""Generate a deterministic review backlog from Atlas coverage results.

The backlog is a planning artifact. It never performs review, assigns authority,
changes lifecycle status, or treats AI-assisted work as accountable approval.
It distinguishes automation-eligible checks from human-required authority work.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import phase1_coverage_report as coverage
import phase1_review_gate as gate

BACKLOG_CONTRACT = "atlas-review-backlog/0.1"
EXECUTION_MODES = {"automation-eligible", "human-required"}

QUALIFICATION_GUIDANCE = {
    "structural": "Atlas contract and schema conformance",
    "editorial": "Technical editing, claim atomicity, and scope control",
    "source": "Bibliographic verification and source-to-claim traceability",
    "domain": "Subject-matter expertise for the entity's scientific or technical domain",
    "methodological": "Methods, measurement, inference, and model-adequacy review",
    "reproducibility": "Independent recalculation or executable reproduction",
    "ethical": "Normative reasoning, values, trade-offs, and affected-party analysis",
    "translation": "Bilingual technical equivalence with domain competence",
    "legal-context": "Qualified legal-context review against current authoritative material",
    "conflict": "Conflict-of-interest and independence assessment",
}

TRACK_BY_REVIEW_TYPE = {
    "structural": "contract-conformance",
    "editorial": "editorial-and-scope",
    "source": "source-and-provenance",
    "domain": "domain-authority",
    "methodological": "methods-and-inference",
    "reproducibility": "reproducibility",
    "ethical": "ethics-and-values",
    "translation": "translation-equivalence",
    "legal-context": "legal-context",
    "conflict": "independence-and-conflicts",
}


@dataclass(frozen=True)
class ReviewerRequirement:
    allowed_kinds: tuple[str, ...]
    allowed_independence: tuple[str, ...]
    accountability_required: bool
    qualification: str

    @property
    def execution_mode(self) -> str:
        if "machine" in self.allowed_kinds and not self.accountability_required:
            return "automation-eligible"
        return "human-required"

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_kinds": list(self.allowed_kinds),
            "allowed_independence": list(self.allowed_independence),
            "accountability_required": self.accountability_required,
            "qualification": self.qualification,
        }


@dataclass(frozen=True)
class ReviewTask:
    id: str
    entity_id: str
    revision: int
    role: str
    review_type: str
    track: str
    priority: str
    execution_mode: str
    required_for_gate: bool
    reviewer_requirement: ReviewerRequirement
    existing_review_ids: tuple[str, ...]
    blockers: tuple[str, ...]
    internal_dependents: tuple[str, ...]
    external_dependents: tuple[str, ...]
    acceptance_criteria: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "entity": {"id": self.entity_id, "revision": self.revision},
            "role": self.role,
            "review_type": self.review_type,
            "track": self.track,
            "priority": self.priority,
            "execution_mode": self.execution_mode,
            "required_for_gate": self.required_for_gate,
            "reviewer_requirement": self.reviewer_requirement.to_dict(),
            "existing_review_ids": list(self.existing_review_ids),
            "blockers": list(self.blockers),
            "internal_dependents": list(self.internal_dependents),
            "external_dependents": list(self.external_dependents),
            "acceptance_criteria": list(self.acceptance_criteria),
        }


@dataclass(frozen=True)
class BacklogResult:
    coverage_id: str
    coverage_decision: str
    task_count: int
    gate_task_count: int
    advisory_task_count: int
    automation_eligible_task_count: int
    human_required_task_count: int
    gate_automation_eligible_task_count: int
    gate_human_required_task_count: int
    tasks: tuple[ReviewTask, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": BACKLOG_CONTRACT,
            "coverage_id": self.coverage_id,
            "coverage_decision": self.coverage_decision,
            "task_count": self.task_count,
            "gate_task_count": self.gate_task_count,
            "advisory_task_count": self.advisory_task_count,
            "automation_eligible_task_count": self.automation_eligible_task_count,
            "human_required_task_count": self.human_required_task_count,
            "gate_automation_eligible_task_count": self.gate_automation_eligible_task_count,
            "gate_human_required_task_count": self.gate_human_required_task_count,
            "tasks": [task.to_dict() for task in self.tasks],
            "authority_boundary": (
                "Automation-eligible means a machine record may satisfy the review policy "
                "when it passes exact-revision validation. Human-required tasks still need "
                "an accountable reviewer with the stated independence and qualification. "
                "This backlog itself performs neither kind of review."
            ),
        }


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "unknown"


def reviewer_requirement(
    review_type: str, entity: Mapping[str, Any]
) -> ReviewerRequirement:
    flags = set(entity.get("material_flags", []) or [])
    qualification = QUALIFICATION_GUIDANCE.get(review_type, review_type)

    if review_type == "structural":
        return ReviewerRequirement(
            allowed_kinds=("machine", "human"),
            allowed_independence=("not-applicable", "internal", "independent"),
            accountability_required=False,
            qualification=qualification,
        )
    if review_type == "reproducibility" and "fully-specified-reproducibility" in flags:
        return ReviewerRequirement(
            allowed_kinds=("machine", "human"),
            allowed_independence=("not-applicable", "internal", "independent"),
            accountability_required=False,
            qualification=qualification,
        )
    if review_type in {"editorial", "source", "conflict"}:
        return ReviewerRequirement(
            allowed_kinds=("human",),
            allowed_independence=("internal", "independent"),
            accountability_required=True,
            qualification=qualification,
        )
    return ReviewerRequirement(
        allowed_kinds=("human",),
        allowed_independence=("independent",),
        accountability_required=True,
        qualification=qualification,
    )


def _priority(item: coverage.EntityCoverage, required_for_gate: bool) -> str:
    if not required_for_gate:
        return "low"
    if item.role == "load-bearing" or item.external_dependents:
        return "high"
    return "medium"


def _acceptance_criteria(review_type: str, entity: Mapping[str, Any]) -> tuple[str, ...]:
    criteria = [
        "Target the exact entity ID and revision.",
        "Disclose reviewer qualification, independence, accountability, and conflicts.",
        "Record findings with severity, status, rationale, and affected fields.",
        "Set a review horizon when the conclusion can become stale.",
        "Do not permit promotion while any critical or major finding remains unresolved.",
    ]
    if review_type == "structural":
        criteria.append(
            "Produce an exact-revision machine or human review record after contract validation."
        )
    elif review_type == "reproducibility":
        criteria.append("Provide an independent recalculation or executable reproduction record.")
    elif review_type == "translation":
        criteria.append(
            "Confirm technical equivalence, qualifiers, equations, inference boundaries, and terminology."
        )
    elif review_type == "methodological":
        criteria.append(
            "Check assumptions, measurement meaning, model adequacy, and model-to-world inference limits."
        )
    elif review_type == "source":
        criteria.append("Verify source identity, locator, access class, and the bounded use claimed.")
    elif review_type == "domain":
        criteria.append("Confirm domain terminology, scope, and whether confidence language is calibrated.")
    if entity.get("translation_of"):
        criteria.append("Confirm the translation still targets the current source revision.")
    return tuple(criteria)


def build_backlog(
    manifest: Mapping[str, Any],
    review_records: Sequence[Mapping[str, Any]],
    path: str = "<coverage>",
) -> tuple[BacklogResult, list[coverage.CoverageDiagnostic]]:
    result, diagnostics = coverage.evaluate_coverage(manifest, review_records, path)
    entities = {
        (item.get("id"), item.get("revision")): item
        for item in manifest.get("entities", [])
        if isinstance(item, dict)
    }
    requirement = manifest.get("coverage_requirement", "all")
    coverage_id = str(manifest.get("id", "unknown"))
    scope_slug = _slug(coverage_id.replace("coverage:", ""))

    tasks: list[ReviewTask] = []
    for entity_result in result.entity_results:
        entity = entities.get((entity_result.entity_id, entity_result.revision), {})
        required_for_gate = requirement == "all" or entity_result.role == "load-bearing"
        for review_type in entity_result.missing_review_types:
            authority = reviewer_requirement(review_type, entity)
            task_id = (
                f"review-task:{scope_slug}:"
                f"{_slug(entity_result.entity_id)}-r{entity_result.revision}:"
                f"{_slug(review_type)}"
            )
            tasks.append(
                ReviewTask(
                    id=task_id,
                    entity_id=entity_result.entity_id,
                    revision=entity_result.revision,
                    role=entity_result.role,
                    review_type=review_type,
                    track=TRACK_BY_REVIEW_TYPE.get(review_type, "other"),
                    priority=_priority(entity_result, required_for_gate),
                    execution_mode=authority.execution_mode,
                    required_for_gate=required_for_gate,
                    reviewer_requirement=authority,
                    existing_review_ids=entity_result.review_ids,
                    blockers=entity_result.blockers,
                    internal_dependents=entity_result.internal_dependents,
                    external_dependents=entity_result.external_dependents,
                    acceptance_criteria=_acceptance_criteria(review_type, entity),
                )
            )

    priority_order = {"high": 0, "medium": 1, "low": 2}
    execution_order = {"human-required": 0, "automation-eligible": 1}
    tasks.sort(
        key=lambda task: (
            priority_order[task.priority],
            execution_order[task.execution_mode],
            task.track,
            task.entity_id,
            task.revision,
            task.review_type,
        )
    )
    gate_tasks = [task for task in tasks if task.required_for_gate]
    automation_tasks = [task for task in tasks if task.execution_mode == "automation-eligible"]
    human_tasks = [task for task in tasks if task.execution_mode == "human-required"]
    backlog = BacklogResult(
        coverage_id=coverage_id,
        coverage_decision=result.decision,
        task_count=len(tasks),
        gate_task_count=len(gate_tasks),
        advisory_task_count=len(tasks) - len(gate_tasks),
        automation_eligible_task_count=len(automation_tasks),
        human_required_task_count=len(human_tasks),
        gate_automation_eligible_task_count=sum(
            task.required_for_gate for task in automation_tasks
        ),
        gate_human_required_task_count=sum(task.required_for_gate for task in human_tasks),
        tasks=tuple(tasks),
    )
    return backlog, diagnostics


def _render_task(task: ReviewTask) -> list[str]:
    authority = task.reviewer_requirement
    lines = [
        f"- **{task.priority.upper()}** `{task.entity_id}@{task.revision}` — "
        f"`{task.review_type}`; mode: `{task.execution_mode}`; "
        f"kinds: {', '.join(authority.allowed_kinds)}; "
        f"independence: {', '.join(authority.allowed_independence)}; "
        f"accountable: {'required' if authority.accountability_required else 'not required'}"
    ]
    if task.existing_review_ids:
        lines.append(
            "  - Existing records that do not yet satisfy coverage: "
            + ", ".join(task.existing_review_ids)
        )
    for blocker in task.blockers:
        lines.append(f"  - Blocker: {blocker}")
    dependents = list(task.internal_dependents) + list(task.external_dependents)
    if dependents:
        lines.append(
            "  - Dependents requiring impact inspection: " + ", ".join(dependents)
        )
    return lines


def render_report(backlog: BacklogResult) -> str:
    lines = [
        "# Atlas Phase 1 Review Backlog",
        "",
        f"- Coverage ID: `{backlog.coverage_id}`",
        f"- Coverage decision: **{backlog.coverage_decision}**",
        f"- Open tasks: `{backlog.task_count}`",
        f"- Gate tasks: `{backlog.gate_task_count}`",
        f"- Advisory tasks: `{backlog.advisory_task_count}`",
        f"- Automation-eligible tasks: `{backlog.automation_eligible_task_count}` "
        f"(`{backlog.gate_automation_eligible_task_count}` gate)",
        f"- Human-required tasks: `{backlog.human_required_task_count}` "
        f"(`{backlog.gate_human_required_task_count}` gate)",
        "",
    ]

    for execution_mode, heading in (
        ("automation-eligible", "Automation-eligible work"),
        ("human-required", "Human-required authority work"),
    ):
        selected = [task for task in backlog.tasks if task.execution_mode == execution_mode]
        lines.extend([f"## {heading}", ""])
        if not selected:
            lines.append("- None")
            lines.append("")
            continue
        grouped: dict[str, list[ReviewTask]] = {}
        for task in selected:
            grouped.setdefault(task.track, []).append(task)
        for track in sorted(grouped):
            lines.extend([f"### {track}", ""])
            for task in grouped[track]:
                lines.extend(_render_task(task))
            lines.append("")

    lines.extend(
        [
            "## Authority boundary",
            "",
            "Automation-eligible does not mean already completed. A valid exact-revision machine review record must still be generated and pass the same contract checks.",
            "",
            "Human-required tasks need an accountable reviewer with the stated qualification and independence. AI-assisted records may identify defects but cannot satisfy that authority.",
            "",
            "This backlog is deterministic planning output. It does not assign a reviewer, perform review, resolve findings, or change lifecycle status.",
            "",
        ]
    )
    return "\n".join(lines)


def _print_diagnostics(
    diagnostics: Iterable[coverage.CoverageDiagnostic], json_output: bool = False
) -> None:
    items = list(diagnostics)
    if json_output:
        print(json.dumps([item.to_dict() for item in items], indent=2, sort_keys=True))
    else:
        for item in items:
            print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument(
        "--records-dir", type=Path, default=Path("content/reviews/records")
    )
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--expect", choices=["blocked", "coverage-complete"])
    args = parser.parse_args(argv)

    payload, diagnostics = coverage.load_json(args.manifest)
    records, record_diagnostics = coverage.load_review_records(args.records_dir)
    diagnostics.extend(record_diagnostics)
    if isinstance(payload, dict):
        backlog, evaluation_diagnostics = build_backlog(
            payload, records, str(args.manifest)
        )
        diagnostics.extend(evaluation_diagnostics)
    else:
        backlog = BacklogResult(
            coverage_id="unknown",
            coverage_decision="blocked",
            task_count=0,
            gate_task_count=0,
            advisory_task_count=0,
            automation_eligible_task_count=0,
            human_required_task_count=0,
            gate_automation_eligible_task_count=0,
            gate_human_required_task_count=0,
            tasks=(),
        )

    diagnostics = sorted(set(diagnostics))
    output = backlog.to_dict()
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(output, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(render_report(backlog), encoding="utf-8")

    if args.json:
        print(
            json.dumps(
                {
                    "backlog": output,
                    "diagnostics": [item.to_dict() for item in diagnostics],
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        print(json.dumps(output, indent=2, sort_keys=True))
        _print_diagnostics(diagnostics)

    has_errors = any(item.severity == "error" for item in diagnostics)
    if args.expect:
        return 0 if backlog.coverage_decision == args.expect and not has_errors else 1
    return 0 if not has_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
