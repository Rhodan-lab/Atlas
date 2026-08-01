"""Build a deterministic review packet for an offline Principia evidence candidate."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import PurePosixPath
from typing import Any, Mapping

from .evidence_bridge import validate_reference_snapshot
from .evidence_drift import build_evidence_drift_report
from .evidence_registry import REGISTRY_STATE, validate_evidence_registry
from .evidence_review import build_review_aware_manifest
from .kernel import KernelError

EVIDENCE_PROMOTION_CONTRACT = "atlas-principia-evidence-promotion-packet/0.1"
_SNAPSHOT_ROOT = "content/fixtures/phase2_bridge/"
_SUBMISSION_BASIS = re.compile(r"^[a-z0-9][a-z0-9._-]{2,119}$")


def _require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def _canonical_bytes(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n"
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _snapshot_path(value: str, *, label: str) -> str:
    _require(
        isinstance(value, str) and bool(value),
        "E-EVIDENCE-PROMOTION-PATH",
        f"{label} snapshot path must be non-empty text",
    )
    path = PurePosixPath(value)
    _require(
        not path.is_absolute()
        and ".." not in path.parts
        and path.as_posix() == value
        and value.startswith(_SNAPSHOT_ROOT)
        and value.endswith(".json"),
        "E-EVIDENCE-PROMOTION-PATH",
        f"{label} snapshot path must be a repository-relative JSON file under {_SNAPSHOT_ROOT}",
    )
    return value


def _submission_basis(value: str) -> str:
    _require(
        isinstance(value, str) and bool(_SUBMISSION_BASIS.fullmatch(value)),
        "E-EVIDENCE-PROMOTION-BASIS",
        "submission_basis must be a lowercase slug of 3 to 120 characters",
    )
    return value


def _manifest_digest(manifest: Mapping[str, Any]) -> str:
    return _sha256(_canonical_bytes(manifest))


def _select_baseline(
    registry: Mapping[str, Any], route_id: str
) -> dict[str, Any]:
    entries = [
        dict(entry)
        for entry in registry["entries"]
        if entry["route_id"] == route_id
    ]
    _require(
        len(entries) == 1,
        "E-EVIDENCE-PROMOTION-ROUTE",
        f"registry must contain exactly one baseline for route {route_id!r}",
    )
    return entries[0]


def _decision(drift_decision: str) -> tuple[str, str, list[str]]:
    mapping = {
        "no-refresh-needed": (
            "candidate-redundant",
            "no-change",
            [],
        ),
        "proceed-source-identity-refresh-review": (
            "ready-for-source-refresh-review",
            "reviewable",
            ["source-identity-review"],
        ),
        "review-reference-metadata-change": (
            "requires-reference-metadata-review",
            "reviewable",
            ["reference-metadata-review"],
        ),
        "review-reference-set-change": (
            "requires-reference-set-review",
            "reviewable",
            ["reference-set-review"],
        ),
        "hold-for-evidence-revalidation": (
            "hold-for-evidence-revalidation",
            "hold",
            ["evidence-revalidation"],
        ),
        "reject-unresolved-reference-refresh": (
            "reject-unresolved-candidate",
            "blocked",
            [],
        ),
    }
    _require(
        drift_decision in mapping,
        "E-EVIDENCE-PROMOTION-DRIFT",
        f"unsupported drift decision: {drift_decision!r}",
    )
    return mapping[drift_decision]


def _acceptance_requirements(gate_state: str) -> list[str]:
    if gate_state == "reviewable":
        return [
            "review-promotion-packet",
            "merge-candidate-snapshot",
            "replace-route-registry-entry",
            "record-registration-commit",
            "rebuild-registry-catalog",
        ]
    if gate_state == "hold":
        return [
            "resolve-evidence-revalidation",
            "rebuild-promotion-packet",
        ]
    if gate_state == "blocked":
        return [
            "resolve-unavailable-atlas-references",
            "rebuild-promotion-packet",
        ]
    return []


def build_evidence_promotion_packet(
    registry_payload: Mapping[str, Any],
    baseline_payload: Mapping[str, Any],
    candidate_payload: Mapping[str, Any],
    repository: Any,
    review_index: Mapping[str, Mapping[str, Any]],
    *,
    baseline_snapshot_path: str,
    candidate_snapshot_path: str,
    submission_basis: str,
    registry_bytes: bytes | None = None,
    baseline_snapshot_bytes: bytes | None = None,
    candidate_snapshot_bytes: bytes | None = None,
) -> dict[str, Any]:
    """Combine registry, bridge, and drift evidence into one read-only gate packet."""
    registry = validate_evidence_registry(registry_payload)
    baseline = validate_reference_snapshot(baseline_payload)
    candidate = validate_reference_snapshot(candidate_payload)
    baseline_path = _snapshot_path(
        baseline_snapshot_path, label="baseline"
    )
    candidate_path = _snapshot_path(
        candidate_snapshot_path, label="candidate"
    )
    basis = _submission_basis(submission_basis)

    entry = _select_baseline(registry, candidate["route_id"])
    _require(
        entry["snapshot_path"] == baseline_path,
        "E-EVIDENCE-PROMOTION-BASELINE",
        "baseline path must match the accepted registry entry",
    )
    _require(
        baseline["route_id"] == entry["route_id"],
        "E-EVIDENCE-PROMOTION-BASELINE",
        "baseline snapshot route must match the registry entry",
    )

    drift = build_evidence_drift_report(
        baseline,
        candidate,
        repository,
        review_index,
    )
    candidate_manifest = build_review_aware_manifest(
        candidate,
        repository,
        review_index,
    )
    decision, gate_state, required_reviews = _decision(drift["decision"])
    reviewable = gate_state == "reviewable"

    proposed_replacement = None
    if reviewable:
        proposed_replacement = {
            "route_id": candidate["route_id"],
            "snapshot_path": candidate_path,
            "state": REGISTRY_STATE,
            "registration_basis": basis,
            "registration_commit": None,
        }

    registry_data = registry_bytes or _canonical_bytes(registry)
    baseline_data = baseline_snapshot_bytes or _canonical_bytes(baseline)
    candidate_data = candidate_snapshot_bytes or _canonical_bytes(candidate)

    return {
        "contract": EVIDENCE_PROMOTION_CONTRACT,
        "registry_contract": registry["contract"],
        "snapshot_contract": candidate["contract"],
        "drift_contract": drift["contract"],
        "manifest_contract": candidate_manifest["contract"],
        "route_id": candidate["route_id"],
        "submission_basis": basis,
        "baseline_registration": {
            "snapshot_path": entry["snapshot_path"],
            "state": entry["state"],
            "registration_basis": entry["registration_basis"],
            "registration_commit": entry["registration_commit"],
        },
        "baseline_source": drift["baseline_source"],
        "candidate_source": drift["candidate_source"],
        "baseline_snapshot_path": baseline_path,
        "candidate_snapshot_path": candidate_path,
        "hashes": {
            "registry_sha256": _sha256(registry_data),
            "baseline_snapshot_sha256": _sha256(baseline_data),
            "candidate_snapshot_sha256": _sha256(candidate_data),
            "drift_report_sha256": _manifest_digest(drift),
            "candidate_manifest_sha256": _manifest_digest(candidate_manifest),
        },
        "change_classes": list(drift["change_classes"]),
        "change_counts": dict(drift["change_counts"]),
        "drift_decision": drift["decision"],
        "candidate_evidence": {
            "reference_count": candidate_manifest["reference_count"],
            "resolved_count": candidate_manifest["resolved_count"],
            "review_record_count": candidate_manifest.get(
                "review_record_count", 0
            ),
            "revalidate_count": candidate_manifest["revalidate_count"],
            "blocked_count": candidate_manifest["blocked_count"],
            "manifest_decision": candidate_manifest["decision"],
        },
        "gate_state": gate_state,
        "decision": decision,
        "required_reviews": required_reviews,
        "acceptance_requirements": _acceptance_requirements(gate_state),
        "registry_update_eligible_after_review": reviewable,
        "proposed_registry_replacement": proposed_replacement,
        "live": False,
        "status_inheritance": "prohibited",
        "automatic_snapshot_acceptance": False,
        "automatic_registry_update": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
        "principia_publication_status_granted": False,
        "learner_effectiveness_claimed": False,
    }
