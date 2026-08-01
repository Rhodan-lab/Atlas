"""Machine-readable Atlas review authority for the Principia evidence bridge."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .evidence_bridge import build_evidence_manifest
from .kernel import ENTITY_ID_RE, KernelError

AI_REVIEW_CONTRACT = "atlas-ai-review/0.1"


def load_review_index(review_root: Path) -> dict[str, dict[str, Any]]:
    """Index exact entity outcomes from machine-readable Atlas AI reviews."""
    root = review_root.resolve()
    if not root.is_dir():
        raise KernelError(
            "E-EVIDENCE-REVIEW-ROOT",
            f"review root is unavailable: {review_root}",
        )
    index: dict[str, dict[str, Any]] = {}
    for path in sorted(item for item in root.rglob("*.json") if item.is_file()):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise KernelError(
                "E-EVIDENCE-REVIEW-READ", str(exc), str(path)
            ) from exc
        if (
            not isinstance(payload, Mapping)
            or payload.get("contract") != AI_REVIEW_CONTRACT
        ):
            continue
        review_id = payload.get("id")
        review_level = payload.get("review_level")
        reviewer = payload.get("reviewer")
        human_verified = (
            reviewer.get("human_verified")
            if isinstance(reviewer, Mapping)
            else None
        )
        entities = payload.get("entities")
        if (
            not isinstance(review_id, str)
            or not isinstance(review_level, str)
            or not isinstance(entities, list)
        ):
            raise KernelError(
                "E-EVIDENCE-REVIEW-STRUCTURE",
                f"malformed AI review record: {path}",
            )
        for position, entity in enumerate(entities):
            if not isinstance(entity, Mapping):
                raise KernelError(
                    "E-EVIDENCE-REVIEW-STRUCTURE",
                    f"{path}: entities[{position}] must be an object",
                )
            entity_id = entity.get("id")
            revision = entity.get("revision")
            if (
                not isinstance(entity_id, str)
                or not ENTITY_ID_RE.fullmatch(entity_id)
            ):
                raise KernelError(
                    "E-EVIDENCE-REVIEW-ENTITY",
                    f"{path}: invalid reviewed entity ID",
                )
            if (
                not isinstance(revision, int)
                or isinstance(revision, bool)
                or revision < 1
            ):
                raise KernelError(
                    "E-EVIDENCE-REVIEW-REVISION",
                    f"{path}: invalid reviewed revision",
                )
            key = f"{entity_id}@{revision}"
            if key in index:
                raise KernelError(
                    "E-EVIDENCE-REVIEW-DUPLICATE",
                    f"duplicate review authority for {key}",
                )
            index[key] = {
                "source": "machine-readable-review",
                "record_id": review_id,
                "record_path": path.relative_to(root.parent.parent).as_posix(),
                "reviewed_at": payload.get("reviewed_at"),
                "review_level": review_level,
                "human_verified": (
                    human_verified if isinstance(human_verified, bool) else None
                ),
                "outcome": entity.get("outcome"),
            }
    return index


def _base_action(resolution: str) -> str:
    if resolution in {"missing-entity", "unavailable-revision", "retracted"}:
        return "block-release"
    if resolution in {
        "deprecated",
        "superseded",
        "review-required",
        "confirmed-stale",
    }:
        return "revalidate"
    return "inspect"


def build_review_aware_manifest(
    payload: Mapping[str, Any],
    repository: Any,
    review_index: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Resolve review authority without rewriting immutable canonical revisions."""
    manifest = build_evidence_manifest(payload, repository)
    findings = [
        dict(item)
        for item in manifest["findings"]
        if not str(item.get("code", "")).startswith("review-")
    ]
    for entry in manifest["entries"]:
        key = entry["key"]
        record = review_index.get(key)
        action = _base_action(entry["resolution"])
        if record is None:
            if entry.get("review_comparison") != "match":
                action = (
                    "block-release"
                    if action == "block-release"
                    else "revalidate"
                )
                findings.append(
                    {
                        "code": "review-authority-unavailable",
                        "key": key,
                        "severity": "warning",
                    }
                )
            entry["required_action"] = action
            entry["review_authority"] = {
                "source": "canonical-inline"
                if entry.get("atlas_review_level") is not None
                else "none",
                "record_id": None,
                "record_path": None,
                "reviewed_at": None,
                "review_level": entry.get("atlas_review_level"),
                "human_verified": entry.get("atlas_human_verified"),
                "outcome": None,
            }
            continue
        level = record.get("review_level")
        human = record.get("human_verified")
        comparison = (
            "match"
            if entry.get("declared_review_level") == level
            and entry.get("declared_human_verified") == human
            and record.get("outcome") == "pass"
            else "mismatch"
        )
        entry["atlas_review_level"] = level
        entry["atlas_human_verified"] = human
        entry["review_comparison"] = comparison
        entry["review_authority"] = dict(record)
        if comparison != "match" and action != "block-release":
            action = "revalidate"
            findings.append(
                {
                    "code": "review-authority-mismatch",
                    "key": key,
                    "severity": "warning",
                }
            )
        entry["required_action"] = action

    manifest["findings"] = sorted(
        findings,
        key=lambda item: (item["severity"], item["code"], item["key"]),
    )
    manifest["revalidate_count"] = sum(
        entry["required_action"] == "revalidate"
        for entry in manifest["entries"]
    )
    manifest["blocked_count"] = sum(
        entry["required_action"] == "block-release"
        for entry in manifest["entries"]
    )
    manifest["review_record_count"] = sum(
        entry["review_authority"]["source"] == "machine-readable-review"
        for entry in manifest["entries"]
    )
    if manifest["blocked_count"]:
        manifest["decision"] = "block-principia-release"
    elif manifest["revalidate_count"]:
        manifest["decision"] = "revalidate-principia-reference-metadata"
    else:
        manifest["decision"] = "verified-offline-reference-manifest"
    manifest["review_authority_contract"] = AI_REVIEW_CONTRACT
    return manifest
