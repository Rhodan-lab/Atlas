#!/usr/bin/env python3
"""Generate self-contained accountable-human review handoff bundles.

The generator consumes the live Phase 1 coverage manifest and review records. It
includes only remaining human-required gate tasks, snapshots the exact canonical
Markdown files, records SHA-256 digests, and groups work by reviewer qualification.
It never assigns a reviewer, performs review, resolves findings, permits promotion,
or changes lifecycle status.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

import atlas_foundation_validator as foundation
import phase1_coverage_report as coverage
import phase1_review_backlog as backlog

HANDOFF_CONTRACT = "atlas-review-handoff/0.1"
DEFAULT_MANIFEST = REPO_ROOT / "content" / "reviews" / "coverage" / "feedback-complete-vertical-slice.json"
DEFAULT_RECORDS_DIR = REPO_ROOT / "content" / "reviews" / "records"
DEFAULT_CANONICAL_ROOT = REPO_ROOT / "content" / "canonical"

TRACK_ORDER = (
    "domain-authority",
    "editorial-and-scope",
    "methods-and-inference",
    "source-and-provenance",
    "reproducibility",
)

TRACK_PROFILES: dict[str, dict[str, Any]] = {
    "domain-authority": {
        "title": "Domain Authority",
        "reviewer_profile": (
            "Independent reviewer with demonstrable control-systems, dynamical-systems, "
            "or difference-equation expertise."
        ),
        "focus": (
            "terminology, mathematical scope, stability language, confidence calibration, "
            "and domain adequacy"
        ),
    },
    "editorial-and-scope": {
        "title": "Editorial and Scope Accountability",
        "reviewer_profile": (
            "Accountable human technical editor able to evaluate claim atomicity, qualifiers, "
            "scope, consistency, and reader-facing interpretation."
        ),
        "focus": (
            "visible limitations, consistent language, confidence wording, and prevention of "
            "formal-to-empirical overstatement"
        ),
    },
    "methods-and-inference": {
        "title": "Methods and Inference",
        "reviewer_profile": (
            "Independent reviewer qualified in mathematical modeling, scientific inference, "
            "system identification, or closely related methodology."
        ),
        "focus": (
            "assumptions, generated-evidence meaning, model adequacy, inference boundaries, "
            "and distinction between demonstration and empirical validation"
        ),
    },
    "source-and-provenance": {
        "title": "Source and Provenance",
        "reviewer_profile": (
            "Accountable human reviewer able to inspect bibliographic identity, source use, "
            "locators, transformations, and source-to-claim provenance."
        ),
        "focus": (
            "source identity, locator accuracy, generated-source honesty, evidence lineage, "
            "and bounded source use"
        ),
    },
    "reproducibility": {
        "title": "Independent Reproducibility",
        "reviewer_profile": (
            "Independent accountable human able to reproduce the generated model-run source "
            "and inspect whether its procedure is complete and honestly described."
        ),
        "focus": (
            "independent source-level reproduction, hidden-step detection, and confirmation that "
            "generated output is not presented as empirical observation"
        ),
    },
}


@dataclass(frozen=True)
class EntitySnapshot:
    entity_id: str
    revision: int
    title: str
    entity_type: str
    canonical_path: str
    sha256: str
    content: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "revision": self.revision,
            "title": self.title,
            "entity_type": self.entity_type,
            "canonical_path": self.canonical_path,
            "sha256": self.sha256,
        }


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "unknown"


def _repo_relative(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def load_manifest(path: Path) -> Mapping[str, Any]:
    payload, diagnostics = coverage.load_json(path)
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors or not isinstance(payload, dict):
        detail = "; ".join(f"{item.code}: {item.message}" for item in errors)
        raise ValueError(f"invalid coverage manifest {path}: {detail or 'not a mapping'}")
    return payload


def discover_snapshots(
    canonical_root: Path,
    repo_root: Path = REPO_ROOT,
) -> dict[tuple[str, int], EntitySnapshot]:
    documents, diagnostics = foundation.discover_documents([canonical_root])
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        detail = "; ".join(f"{item.code}: {item.message}" for item in errors)
        raise ValueError(f"canonical discovery failed: {detail}")

    snapshots: dict[tuple[str, int], EntitySnapshot] = {}
    for document in documents:
        entity_id = document.metadata.get("id")
        revision = document.metadata.get("revision")
        if not isinstance(entity_id, str) or not isinstance(revision, int):
            continue
        path = Path(document.path)
        content = path.read_text(encoding="utf-8")
        snapshot = EntitySnapshot(
            entity_id=entity_id,
            revision=revision,
            title=str(document.metadata.get("title", entity_id)),
            entity_type=str(document.metadata.get("type", "unknown")),
            canonical_path=_repo_relative(path, repo_root),
            sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
            content=content,
        )
        key = (entity_id, revision)
        if key in snapshots:
            raise ValueError(f"duplicate canonical snapshot {entity_id}@{revision}")
        snapshots[key] = snapshot
    return snapshots


def _task_with_snapshot(
    task: backlog.ReviewTask,
    snapshot: EntitySnapshot,
) -> dict[str, Any]:
    payload = task.to_dict()
    payload["entity_snapshot"] = snapshot.to_dict()
    payload["submission_requirements"] = {
        "record_contract": "atlas-review/0.1",
        "one_record_per_review_type": True,
        "real_or_stable_accountable_identity_required": True,
        "qualification_required": True,
        "independence_required": True,
        "conflicts_required_even_when_empty": True,
        "structured_findings_required": True,
        "promotion_permission_bounded_to_exact_revision": True,
    }
    return payload


def build_handoff(
    manifest: Mapping[str, Any],
    review_records: Sequence[Mapping[str, Any]],
    snapshots: Mapping[tuple[str, int], EntitySnapshot],
    source_manifest: str,
) -> dict[str, Any]:
    result, diagnostics = backlog.build_backlog(manifest, review_records, source_manifest)
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        detail = "; ".join(f"{item.code}: {item.message}" for item in errors)
        raise ValueError(f"backlog generation failed: {detail}")
    if result.coverage_decision != "blocked":
        raise ValueError("human handoff is valid only while the slice remains blocked")
    if result.automation_eligible_task_count:
        raise ValueError(
            f"{result.automation_eligible_task_count} automation-eligible tasks remain; "
            "complete deterministic machine work before human handoff"
        )
    if result.advisory_task_count:
        raise ValueError("current human handoff expects gate tasks only")

    human_tasks = [
        task
        for task in result.tasks
        if task.required_for_gate and task.execution_mode == "human-required"
    ]
    if len(human_tasks) != result.gate_human_required_task_count:
        raise ValueError("human task count does not match backlog summary")

    grouped: dict[str, list[dict[str, Any]]] = {track: [] for track in TRACK_ORDER}
    all_task_ids: set[str] = set()
    entity_keys: set[tuple[str, int]] = set()

    for task in human_tasks:
        if task.track not in TRACK_PROFILES:
            raise ValueError(f"unsupported human review track {task.track!r}")
        if task.id in all_task_ids:
            raise ValueError(f"duplicate review task {task.id}")
        all_task_ids.add(task.id)
        if task.reviewer_requirement.allowed_kinds != ("human",):
            raise ValueError(f"human handoff task permits nonhuman reviewer: {task.id}")
        if not task.reviewer_requirement.accountability_required:
            raise ValueError(f"human handoff task lacks accountability requirement: {task.id}")

        key = (task.entity_id, task.revision)
        snapshot = snapshots.get(key)
        if snapshot is None:
            raise ValueError(f"missing canonical snapshot for {task.entity_id}@{task.revision}")
        entity_keys.add(key)
        grouped[task.track].append(_task_with_snapshot(task, snapshot))

    tracks: list[dict[str, Any]] = []
    for track_id in TRACK_ORDER:
        tasks = sorted(
            grouped[track_id],
            key=lambda item: (
                0 if item["priority"] == "high" else 1,
                item["entity"]["id"],
                item["entity"]["revision"],
                item["review_type"],
            ),
        )
        if not tasks:
            continue
        profile = TRACK_PROFILES[track_id]
        tracks.append(
            {
                "id": track_id,
                "title": profile["title"],
                "reviewer_profile": profile["reviewer_profile"],
                "focus": profile["focus"],
                "task_count": len(tasks),
                "task_ids": [task["id"] for task in tasks],
                "tasks": tasks,
            }
        )

    entity_snapshots = [snapshots[key].to_dict() for key in sorted(entity_keys)]
    handoff = {
        "contract": HANDOFF_CONTRACT,
        "coverage_id": result.coverage_id,
        "coverage_decision": result.coverage_decision,
        "source_manifest": source_manifest,
        "task_count": len(human_tasks),
        "track_count": len(tracks),
        "entity_snapshot_count": len(entity_snapshots),
        "tracks": tracks,
        "entity_snapshots": entity_snapshots,
        "reviewer_assignment": None,
        "authority_boundary": (
            "This handoff assigns no reviewer, performs no review, resolves no finding, "
            "permits no promotion, and changes no lifecycle state. Every task requires an "
            "accountable human record for the exact entity revision and review type."
        ),
    }
    validate_handoff(handoff)
    return handoff


def validate_handoff(handoff: Mapping[str, Any]) -> None:
    if handoff.get("contract") != HANDOFF_CONTRACT:
        raise ValueError("unsupported handoff contract")
    tracks = handoff.get("tracks")
    if not isinstance(tracks, list) or not tracks:
        raise ValueError("handoff requires non-empty tracks")
    if handoff.get("reviewer_assignment") is not None:
        raise ValueError("handoff must not assign a reviewer")

    task_ids: list[str] = []
    for track in tracks:
        if not isinstance(track, dict):
            raise ValueError("track must be a mapping")
        tasks = track.get("tasks")
        if not isinstance(tasks, list) or not tasks:
            raise ValueError(f"track {track.get('id')} requires tasks")
        if track.get("task_count") != len(tasks):
            raise ValueError(f"track {track.get('id')} task count mismatch")
        for task in tasks:
            if task.get("execution_mode") != "human-required":
                raise ValueError(f"nonhuman task entered handoff: {task.get('id')}")
            requirement = task.get("reviewer_requirement", {})
            if requirement.get("allowed_kinds") != ["human"]:
                raise ValueError(f"task permits nonhuman authority: {task.get('id')}")
            if requirement.get("accountability_required") is not True:
                raise ValueError(f"task does not require accountability: {task.get('id')}")
            snapshot = task.get("entity_snapshot", {})
            digest = snapshot.get("sha256")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                raise ValueError(f"task lacks valid entity digest: {task.get('id')}")
            task_ids.append(str(task.get("id")))

    if len(task_ids) != len(set(task_ids)):
        raise ValueError("handoff contains duplicate task IDs")
    if handoff.get("task_count") != len(task_ids):
        raise ValueError("handoff task count mismatch")
    if handoff.get("track_count") != len(tracks):
        raise ValueError("handoff track count mismatch")


def _render_task(task: Mapping[str, Any]) -> list[str]:
    entity = task["entity"]
    snapshot = task["entity_snapshot"]
    requirement = task["reviewer_requirement"]
    lines = [
        f"### `{entity['id']}@{entity['revision']}` — `{task['review_type']}`",
        "",
        f"- Task ID: `{task['id']}`",
        f"- Priority: `{task['priority']}`",
        f"- Entity role: `{task['role']}`",
        f"- Canonical file: `{snapshot['canonical_path']}`",
        f"- Snapshot SHA-256: `{snapshot['sha256']}`",
        f"- Required independence: {', '.join(requirement['allowed_independence'])}",
        f"- Qualification guidance: {requirement['qualification']}",
    ]
    if task["existing_review_ids"]:
        lines.append(
            "- Existing records that do not satisfy this task: "
            + ", ".join(f"`{item}`" for item in task["existing_review_ids"])
        )
    if task["blockers"]:
        lines.append("- Existing blockers:")
        lines.extend(f"  - {item}" for item in task["blockers"])
    dependents = list(task["internal_dependents"]) + list(task["external_dependents"])
    if dependents:
        lines.append("- Dependents requiring impact inspection:")
        lines.extend(f"  - `{item}`" for item in dependents)
    lines.append("- Acceptance criteria:")
    lines.extend(f"  - {item}" for item in task["acceptance_criteria"])
    lines.extend(
        [
            "",
            "Submission worksheet:",
            "",
            "- Reviewer identity or accountable role:",
            "- Qualification:",
            "- Independence:",
            "- Conflicts, including an explicit empty declaration when none are known:",
            "- Outcome:",
            "- Findings and affected fields:",
            "- Review horizon:",
            "- Does this exact review permit promotion for this review type?",
            "- Proposed `atlas-review/0.1` record filename:",
            "",
        ]
    )
    return lines


def render_track(track: Mapping[str, Any], coverage_id: str) -> str:
    lines = [
        f"# {track['title']} Review Bundle",
        "",
        f"- Handoff contract: `{HANDOFF_CONTRACT}`",
        f"- Coverage scope: `{coverage_id}`",
        f"- Track ID: `{track['id']}`",
        f"- Task count: `{track['task_count']}`",
        "",
        "## Reviewer profile",
        "",
        track["reviewer_profile"],
        "",
        "## Review focus",
        "",
        track["focus"],
        "",
        "## Authority boundary",
        "",
        "This bundle assigns no reviewer and records no completed review. Each task requires a separate exact-revision `atlas-review/0.1` record. A broad approval letter cannot silently satisfy unrelated review types.",
        "",
        "## Tasks",
        "",
    ]
    for task in track["tasks"]:
        lines.extend(_render_task(task))
    lines.extend(
        [
            "## Submission validation",
            "",
            "```bash",
            "python tools/foundation-validator/phase1_review_gate.py validate-record \\",
            "  content/reviews/records/<record>.json",
            "```",
            "",
            "After accepted records are added, regenerate coverage and the backlog. Do not edit canonical lifecycle status directly.",
            "",
        ]
    )
    return "\n".join(lines)


def render_index(handoff: Mapping[str, Any]) -> str:
    lines = [
        "# Atlas Phase 1 Human Review Handoff",
        "",
        f"- Contract: `{handoff['contract']}`",
        f"- Coverage scope: `{handoff['coverage_id']}`",
        f"- Coverage decision: **{handoff['coverage_decision']}**",
        f"- Human-required tasks: `{handoff['task_count']}`",
        f"- Qualification tracks: `{handoff['track_count']}`",
        f"- Exact entity snapshots: `{handoff['entity_snapshot_count']}`",
        "",
        "## Authority boundary",
        "",
        handoff["authority_boundary"],
        "",
        "## Bundles",
        "",
    ]
    for track in handoff["tracks"]:
        lines.append(
            f"- [`tracks/{track['id']}.md`](tracks/{track['id']}.md) — "
            f"{track['title']}: {track['task_count']} tasks"
        )
    lines.extend(
        [
            "",
            "## Exact content snapshots",
            "",
            "The `entities/` directory contains byte-for-byte copies of every canonical Markdown file referenced by the remaining human tasks. `handoff.json` records each original path and SHA-256 digest.",
            "",
            "## Submission rule",
            "",
            "Return one valid `atlas-review/0.1` record per entity revision and review type. Real qualification, independence, conflicts, findings, and promotion permission must be recorded honestly. Do not fabricate a reviewer or reuse a review across revisions.",
            "",
        ]
    )
    return "\n".join(lines)


def write_bundle(
    handoff: Mapping[str, Any],
    snapshots: Mapping[tuple[str, int], EntitySnapshot],
    output_dir: Path,
) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "tracks").mkdir(parents=True)
    (output_dir / "entities").mkdir(parents=True)

    (output_dir / "handoff.json").write_text(
        json.dumps(handoff, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output_dir / "README.md").write_text(render_index(handoff), encoding="utf-8")

    for track in handoff["tracks"]:
        track_id = track["id"]
        (output_dir / "tracks" / f"{track_id}.json").write_text(
            json.dumps(track, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        (output_dir / "tracks" / f"{track_id}.md").write_text(
            render_track(track, str(handoff["coverage_id"])), encoding="utf-8"
        )

    referenced = {
        (item["entity_id"], item["revision"])
        for item in handoff["entity_snapshots"]
    }
    for key in sorted(referenced):
        snapshot = snapshots[key]
        target = output_dir / "entities" / snapshot.canonical_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(snapshot.content, encoding="utf-8")


def directory_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def generate(
    manifest_path: Path,
    records_dir: Path,
    canonical_root: Path,
    output_dir: Path,
) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    records, diagnostics = coverage.load_review_records(records_dir)
    errors = [item for item in diagnostics if item.severity == "error"]
    if errors:
        detail = "; ".join(f"{item.code}: {item.message}" for item in errors)
        raise ValueError(f"review record load failed: {detail}")
    snapshots = discover_snapshots(canonical_root)
    handoff = build_handoff(
        manifest,
        records,
        snapshots,
        _repo_relative(manifest_path, REPO_ROOT),
    )
    write_bundle(handoff, snapshots, output_dir)
    return handoff


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--records-dir", type=Path, default=DEFAULT_RECORDS_DIR)
    parser.add_argument("--canonical-root", type=Path, default=DEFAULT_CANONICAL_ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--expect-task-count", type=int)
    parser.add_argument("--expect-track-count", type=int)
    args = parser.parse_args(argv)

    try:
        handoff = generate(
            args.manifest,
            args.records_dir,
            args.canonical_root,
            args.output_dir,
        )
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    if args.expect_task_count is not None and handoff["task_count"] != args.expect_task_count:
        print(
            f"expected {args.expect_task_count} tasks, got {handoff['task_count']}",
            file=sys.stderr,
        )
        return 1
    if args.expect_track_count is not None and handoff["track_count"] != args.expect_track_count:
        print(
            f"expected {args.expect_track_count} tracks, got {handoff['track_count']}",
            file=sys.stderr,
        )
        return 1

    print(
        json.dumps(
            {
                "contract": handoff["contract"],
                "task_count": handoff["task_count"],
                "track_count": handoff["track_count"],
                "entity_snapshot_count": handoff["entity_snapshot_count"],
                "output_dir": str(args.output_dir),
                "directory_sha256": directory_digest(args.output_dir),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
