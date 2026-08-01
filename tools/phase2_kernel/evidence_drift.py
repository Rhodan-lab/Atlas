"""Deterministic offline comparison of accepted and candidate Principia evidence snapshots."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from .evidence_bridge import validate_reference_snapshot
from .evidence_review import build_review_aware_manifest
from .kernel import KernelError

EVIDENCE_DRIFT_CONTRACT = "atlas-principia-evidence-drift-report/0.1"


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _manifest_digest(manifest: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        manifest,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _source_view(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "repository": snapshot["source_repository"],
        "commit": snapshot["source_commit"],
        "path": snapshot["source_path"],
        "blob_sha": snapshot["source_blob_sha"],
        "route_id": snapshot["route_id"],
    }


def _reference_map(snapshot: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        f"{item['entity_id']}@{item['revision']}": dict(item)
        for item in snapshot["references"]
    }


def _references_by_id(
    references: Mapping[str, Mapping[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in references.values():
        grouped.setdefault(str(item["entity_id"]), []).append(dict(item))
    for entity_id in grouped:
        grouped[entity_id].sort(key=lambda item: int(item["revision"]))
    return grouped


def _manifest_entry_map(manifest: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    entries = manifest.get("entries")
    _require(
        isinstance(entries, list),
        "E-EVIDENCE-DRIFT-MANIFEST",
        "evidence manifest entries must be a list",
    )
    result: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        _require(
            isinstance(entry, Mapping) and isinstance(entry.get("key"), str),
            "E-EVIDENCE-DRIFT-MANIFEST",
            f"manifest entries[{index}] must have a string key",
        )
        key = str(entry["key"])
        _require(
            key not in result,
            "E-EVIDENCE-DRIFT-MANIFEST-DUPLICATE",
            f"duplicate manifest entry {key}",
        )
        result[key] = dict(entry)
    return result


def _revision_changes(
    baseline: Mapping[str, list[dict[str, Any]]],
    candidate: Mapping[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], set[str], set[str]]:
    changes: list[dict[str, Any]] = []
    consumed_baseline: set[str] = set()
    consumed_candidate: set[str] = set()
    for entity_id in sorted(set(baseline).intersection(candidate)):
        before = baseline[entity_id]
        after = candidate[entity_id]
        if len(before) != 1 or len(after) != 1:
            continue
        old_revision = int(before[0]["revision"])
        new_revision = int(after[0]["revision"])
        if old_revision == new_revision:
            continue
        old_key = f"{entity_id}@{old_revision}"
        new_key = f"{entity_id}@{new_revision}"
        changes.append(
            {
                "entity_id": entity_id,
                "from_revision": old_revision,
                "to_revision": new_revision,
                "from_key": old_key,
                "to_key": new_key,
            }
        )
        consumed_baseline.add(old_key)
        consumed_candidate.add(new_key)
    return changes, consumed_baseline, consumed_candidate


def _validation_changes(
    baseline_manifest: Mapping[str, Any],
    candidate_manifest: Mapping[str, Any],
) -> list[dict[str, Any]]:
    before = _manifest_entry_map(baseline_manifest)
    after = _manifest_entry_map(candidate_manifest)
    fields = (
        "resolution",
        "required_action",
        "review_comparison",
        "atlas_review_level",
        "atlas_human_verified",
    )
    changes: list[dict[str, Any]] = []
    for key in sorted(set(before).intersection(after)):
        changed = {
            field: {"from": before[key].get(field), "to": after[key].get(field)}
            for field in fields
            if before[key].get(field) != after[key].get(field)
        }
        before_authority = before[key].get("review_authority")
        after_authority = after[key].get("review_authority")
        if before_authority != after_authority:
            changed["review_authority"] = {
                "from": before_authority,
                "to": after_authority,
            }
        if changed:
            changes.append({"key": key, "fields": changed})
    return changes


def build_evidence_drift_report(
    baseline_payload: Mapping[str, Any],
    candidate_payload: Mapping[str, Any],
    repository: Any,
    review_index: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Compare one candidate snapshot with the accepted offline baseline."""
    baseline = validate_reference_snapshot(baseline_payload)
    candidate = validate_reference_snapshot(candidate_payload)

    scope_fields = ("source_repository", "source_path", "route_id")
    scope_mismatch = {
        field: {"baseline": baseline.get(field), "candidate": candidate.get(field)}
        for field in scope_fields
        if baseline.get(field) != candidate.get(field)
    }
    _require(
        not scope_mismatch,
        "E-EVIDENCE-DRIFT-SCOPE",
        f"candidate must describe the same route scope: {scope_mismatch}",
    )

    baseline_manifest = build_review_aware_manifest(
        baseline, repository, review_index
    )
    candidate_manifest = build_review_aware_manifest(
        candidate, repository, review_index
    )

    baseline_refs = _reference_map(baseline)
    candidate_refs = _reference_map(candidate)
    revisions, consumed_before, consumed_after = _revision_changes(
        _references_by_id(baseline_refs),
        _references_by_id(candidate_refs),
    )

    removed = sorted(set(baseline_refs) - set(candidate_refs) - consumed_before)
    added = sorted(set(candidate_refs) - set(baseline_refs) - consumed_after)
    shared = sorted(set(baseline_refs).intersection(candidate_refs))

    purpose_changes = [
        {
            "key": key,
            "from": baseline_refs[key]["purpose"],
            "to": candidate_refs[key]["purpose"],
        }
        for key in shared
        if baseline_refs[key]["purpose"] != candidate_refs[key]["purpose"]
    ]
    review_declaration_changes = []
    for key in shared:
        before = {
            "review_level": baseline_refs[key].get("declared_review_level"),
            "human_verified": baseline_refs[key].get(
                "declared_human_verified"
            ),
        }
        after = {
            "review_level": candidate_refs[key].get("declared_review_level"),
            "human_verified": candidate_refs[key].get(
                "declared_human_verified"
            ),
        }
        if before != after:
            review_declaration_changes.append(
                {"key": key, "from": before, "to": after}
            )

    source_identity_changes = {
        field: {"from": baseline[field], "to": candidate[field]}
        for field in ("source_commit", "source_blob_sha")
        if baseline[field] != candidate[field]
    }
    validation_changes = _validation_changes(
        baseline_manifest, candidate_manifest
    )

    change_classes: list[str] = []
    if source_identity_changes:
        change_classes.append("source-identity")
    if added:
        change_classes.append("reference-added")
    if removed:
        change_classes.append("reference-removed")
    if revisions:
        change_classes.append("revision-changed")
    if purpose_changes:
        change_classes.append("purpose-changed")
    if review_declaration_changes:
        change_classes.append("review-declaration-changed")
    if validation_changes:
        change_classes.append("validation-outcome-changed")
    if not change_classes:
        change_classes.append("none")

    blocked = int(candidate_manifest.get("blocked_count", 0))
    revalidate = int(candidate_manifest.get("revalidate_count", 0))
    if blocked:
        decision = "reject-unresolved-reference-refresh"
    elif revalidate:
        decision = "hold-for-evidence-revalidation"
    elif added or removed or revisions:
        decision = "review-reference-set-change"
    elif purpose_changes or review_declaration_changes or validation_changes:
        decision = "review-reference-metadata-change"
    elif source_identity_changes:
        decision = "proceed-source-identity-refresh-review"
    else:
        decision = "no-refresh-needed"

    return {
        "contract": EVIDENCE_DRIFT_CONTRACT,
        "baseline_snapshot_contract": baseline["contract"],
        "candidate_snapshot_contract": candidate["contract"],
        "baseline_source": _source_view(baseline),
        "candidate_source": _source_view(candidate),
        "baseline_manifest_sha256": _manifest_digest(baseline_manifest),
        "candidate_manifest_sha256": _manifest_digest(candidate_manifest),
        "candidate_manifest_decision": candidate_manifest.get("decision"),
        "change_classes": change_classes,
        "source_identity_changes": source_identity_changes,
        "reference_changes": {
            "added": added,
            "removed": removed,
            "revision_changes": revisions,
            "purpose_changes": purpose_changes,
            "review_declaration_changes": review_declaration_changes,
            "validation_changes": validation_changes,
        },
        "change_counts": {
            "added": len(added),
            "removed": len(removed),
            "revision_changes": len(revisions),
            "purpose_changes": len(purpose_changes),
            "review_declaration_changes": len(review_declaration_changes),
            "validation_changes": len(validation_changes),
        },
        "decision": decision,
        "live": False,
        "status_inheritance": "prohibited",
        "automatic_snapshot_acceptance": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }
