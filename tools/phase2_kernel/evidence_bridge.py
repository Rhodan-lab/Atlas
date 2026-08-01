"""Deterministic offline audit of Principia references to exact Atlas revisions."""
from __future__ import annotations

import re
from typing import Any, Mapping

from .kernel import ENTITY_ID_RE, KernelError

REFERENCE_SNAPSHOT_CONTRACT = "principia-atlas-reference-snapshot/0.1"
EVIDENCE_MANIFEST_CONTRACT = "atlas-principia-evidence-manifest/0.1"
PRINCIPIA_REPOSITORY = "Rhodan-lab/principle-to-system"
_HEX_40 = re.compile(r"^[0-9a-f]{40}$")
_ROUTE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_TOP_LEVEL_FIELDS = {
    "contract",
    "source_repository",
    "source_commit",
    "source_path",
    "source_blob_sha",
    "route_id",
    "live",
    "status_inheritance",
    "references",
}
_REFERENCE_FIELDS = {
    "entity_id",
    "revision",
    "declared_review_level",
    "declared_human_verified",
    "purpose",
}


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def validate_reference_snapshot(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a pinned, non-live Product Alpha reference snapshot."""
    _require(
        isinstance(payload, Mapping),
        "E-EVIDENCE-SNAPSHOT",
        "snapshot must be an object",
    )
    source = dict(payload)
    unknown = sorted(set(source) - _TOP_LEVEL_FIELDS)
    _require(
        not unknown,
        "E-EVIDENCE-SNAPSHOT-FIELD",
        f"unsupported snapshot fields: {unknown}",
    )
    _require(
        source.get("contract") == REFERENCE_SNAPSHOT_CONTRACT,
        "E-EVIDENCE-SNAPSHOT-CONTRACT",
        f"expected {REFERENCE_SNAPSHOT_CONTRACT!r}",
    )
    _require(
        source.get("source_repository") == PRINCIPIA_REPOSITORY,
        "E-EVIDENCE-SNAPSHOT-REPOSITORY",
        f"expected source_repository {PRINCIPIA_REPOSITORY!r}",
    )
    _require(
        isinstance(source.get("source_commit"), str)
        and bool(_HEX_40.fullmatch(source["source_commit"])),
        "E-EVIDENCE-SNAPSHOT-COMMIT",
        "source_commit must be a lowercase 40-character Git commit SHA",
    )
    _require(
        isinstance(source.get("source_blob_sha"), str)
        and bool(_HEX_40.fullmatch(source["source_blob_sha"])),
        "E-EVIDENCE-SNAPSHOT-BLOB",
        "source_blob_sha must be a lowercase 40-character Git blob SHA",
    )
    _require(
        isinstance(source.get("source_path"), str)
        and source["source_path"].startswith("software/product_alpha/routes/")
        and source["source_path"].endswith(".json"),
        "E-EVIDENCE-SNAPSHOT-PATH",
        "source_path must identify a Product Alpha route JSON file",
    )
    _require(
        isinstance(source.get("route_id"), str)
        and bool(_ROUTE_ID.fullmatch(source["route_id"])),
        "E-EVIDENCE-SNAPSHOT-ROUTE",
        "route_id must be canonical kebab-case",
    )
    _require(
        source.get("live") is False,
        "E-EVIDENCE-LIVE-FROZEN",
        "evidence bridge accepts only live=false snapshots",
    )
    _require(
        source.get("status_inheritance") == "prohibited",
        "E-EVIDENCE-STATUS-INHERITANCE",
        "status_inheritance must be 'prohibited'",
    )
    references = source.get("references")
    _require(
        isinstance(references, list) and bool(references),
        "E-EVIDENCE-REFERENCES",
        "references must be a non-empty list",
    )
    normalized: list[dict[str, Any]] = []
    seen: set[tuple[str, int]] = set()
    for index, reference in enumerate(references):
        _require(
            isinstance(reference, Mapping),
            "E-EVIDENCE-REFERENCE",
            f"references[{index}] must be an object",
        )
        item = dict(reference)
        unknown_reference = sorted(set(item) - _REFERENCE_FIELDS)
        _require(
            not unknown_reference,
            "E-EVIDENCE-REFERENCE-FIELD",
            f"references[{index}] has unsupported fields: {unknown_reference}",
        )
        entity_id = item.get("entity_id")
        revision = item.get("revision")
        _require(
            isinstance(entity_id, str) and bool(ENTITY_ID_RE.fullmatch(entity_id)),
            "E-EVIDENCE-ENTITY-ID",
            f"references[{index}] has an invalid Atlas entity ID",
        )
        _require(
            isinstance(revision, int)
            and not isinstance(revision, bool)
            and revision > 0,
            "E-EVIDENCE-REVISION",
            f"references[{index}] requires a positive exact revision",
        )
        key = (entity_id, revision)
        _require(
            key not in seen,
            "E-EVIDENCE-DUPLICATE",
            f"duplicate exact reference {entity_id}@{revision}",
        )
        seen.add(key)
        declared_level = item.get("declared_review_level")
        _require(
            declared_level is None or isinstance(declared_level, str),
            "E-EVIDENCE-REVIEW-LEVEL",
            f"references[{index}] declared_review_level must be text or null",
        )
        declared_human = item.get("declared_human_verified")
        _require(
            declared_human is None or isinstance(declared_human, bool),
            "E-EVIDENCE-HUMAN-VERIFIED",
            f"references[{index}] declared_human_verified must be boolean or null",
        )
        _require(
            isinstance(item.get("purpose"), str) and bool(item["purpose"].strip()),
            "E-EVIDENCE-PURPOSE",
            f"references[{index}] purpose must be non-empty text",
        )
        normalized.append(item)
    source["references"] = normalized
    return source


def _review_authority(entity: Mapping[str, Any]) -> tuple[str | None, bool | None]:
    level = (
        entity.get("review_level")
        if isinstance(entity.get("review_level"), str)
        else None
    )
    metadata = entity.get("metadata")
    review = metadata.get("review") if isinstance(metadata, Mapping) else None
    human = review.get("human_verified") if isinstance(review, Mapping) else None
    return level, human if isinstance(human, bool) else None


def _review_comparison(
    declared_level: Any,
    declared_human: Any,
    authoritative_level: Any,
    authoritative_human: Any,
) -> str:
    if authoritative_level is None and authoritative_human is None:
        return (
            "declared-without-atlas-review-record"
            if declared_level is not None or declared_human is not None
            else "not-declared-and-not-recorded"
        )
    if (
        declared_level == authoritative_level
        and declared_human == authoritative_human
    ):
        return "match"
    return "mismatch"


def _lifecycle_resolution(
    entity: Mapping[str, Any],
    revisions: list[int],
    requested: int,
) -> tuple[str, str]:
    status = entity.get("status")
    staleness = entity.get("staleness", "current")
    if status == "retracted":
        return "retracted", "block-release"
    if status == "deprecated":
        return "deprecated", "revalidate"
    if staleness in {"review-required", "confirmed-stale"}:
        return str(staleness), "revalidate"
    if revisions and max(revisions) > requested:
        return "superseded", "revalidate"
    return "current", "inspect"


def build_evidence_manifest(
    payload: Mapping[str, Any],
    repository: Any,
) -> dict[str, Any]:
    """Resolve every pinned reference and emit a deterministic read-only manifest."""
    snapshot = validate_reference_snapshot(payload)
    entries: list[dict[str, Any]] = []
    findings: list[dict[str, str]] = []
    action_rank = {"inspect": 0, "revalidate": 1, "block-release": 2}
    manifest_action = "inspect"
    for reference in snapshot["references"]:
        entity_id = reference["entity_id"]
        revision = reference["revision"]
        key = f"{entity_id}@{revision}"
        try:
            entity = repository.exact(entity_id, revision)
        except KernelError as exc:
            resolution = (
                "unavailable-revision"
                if exc.code == "E-REVISION-MISSING"
                else "missing-entity"
            )
            action = "block-release"
            entries.append(
                {
                    "key": key,
                    "entity_id": entity_id,
                    "revision": revision,
                    "purpose": reference["purpose"],
                    "resolution": resolution,
                    "required_action": action,
                    "review_comparison": "unresolved",
                    "provenance_state": "unresolved",
                    "provenance_sources": [],
                }
            )
            findings.append(
                {"code": exc.code, "key": key, "severity": "block"}
            )
            manifest_action = action
            continue
        revisions = repository.available_revisions(entity_id)
        resolution, action = _lifecycle_resolution(entity, revisions, revision)
        authoritative_level, authoritative_human = _review_authority(entity)
        comparison = _review_comparison(
            reference.get("declared_review_level"),
            reference.get("declared_human_verified"),
            authoritative_level,
            authoritative_human,
        )
        if (
            comparison in {"mismatch", "declared-without-atlas-review-record"}
            and action_rank[action] < action_rank["revalidate"]
        ):
            action = "revalidate"
        if comparison != "match":
            findings.append(
                {
                    "code": f"review-{comparison}",
                    "key": key,
                    "severity": "warning",
                }
            )
        sources = repository.provenance_sources(entity_id, revision)
        provenance = [
            {
                "key": source.get("key"),
                "path": source.get("path"),
                "source_sha256": source.get("source_sha256"),
            }
            for source in sources
        ]
        provenance_state = (
            "source-chain-present" if provenance else "no-source-entity-chain"
        )
        if not provenance:
            findings.append(
                {
                    "code": "provenance-source-chain-absent",
                    "key": key,
                    "severity": "notice",
                }
            )
        if action_rank[action] > action_rank[manifest_action]:
            manifest_action = action
        entries.append(
            {
                "key": key,
                "entity_id": entity_id,
                "revision": revision,
                "entity_type": entity.get("type"),
                "title": entity.get("title"),
                "canonical_path": entity.get("path"),
                "canonical_source_sha256": entity.get("source_sha256"),
                "canonical_body_sha256": entity.get("body_sha256"),
                "purpose": reference["purpose"],
                "resolution": resolution,
                "required_action": action,
                "declared_review_level": reference.get("declared_review_level"),
                "declared_human_verified": reference.get(
                    "declared_human_verified"
                ),
                "atlas_review_level": authoritative_level,
                "atlas_human_verified": authoritative_human,
                "review_comparison": comparison,
                "provenance_state": provenance_state,
                "provenance_sources": provenance,
            }
        )
    entries.sort(key=lambda item: (item["entity_id"], item["revision"]))
    findings.sort(
        key=lambda item: (item["severity"], item["code"], item["key"])
    )
    decision = {
        "inspect": "verified-offline-reference-manifest",
        "revalidate": "revalidate-principia-reference-metadata",
        "block-release": "block-principia-release",
    }[manifest_action]
    return {
        "contract": EVIDENCE_MANIFEST_CONTRACT,
        "source_snapshot_contract": REFERENCE_SNAPSHOT_CONTRACT,
        "source": {
            "repository": snapshot["source_repository"],
            "commit": snapshot["source_commit"],
            "path": snapshot["source_path"],
            "blob_sha": snapshot["source_blob_sha"],
            "route_id": snapshot["route_id"],
        },
        "reference_count": len(entries),
        "resolved_count": sum(
            item["resolution"]
            not in {"missing-entity", "unavailable-revision"}
            for item in entries
        ),
        "revalidate_count": sum(
            item["required_action"] == "revalidate" for item in entries
        ),
        "blocked_count": sum(
            item["required_action"] == "block-release" for item in entries
        ),
        "entries": entries,
        "findings": findings,
        "decision": decision,
        "live": False,
        "status_inheritance": "prohibited",
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }
