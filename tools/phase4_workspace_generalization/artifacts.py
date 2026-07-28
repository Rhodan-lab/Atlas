#!/usr/bin/env python3
"""Build deterministic Catalase workspace export, manifest, and generalization evidence."""
from __future__ import annotations

from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository, render_json
from tools.phase4_workspace_generalization.constants import (
    BASELINE_CONTRACT,
    EXPORT_CONTRACT,
    FAILURE_CONTRACT,
    MANIFEST_CONTRACT,
    MODE,
    RECOMMENDATION,
    REPORT_CONTRACT,
    REUSED_CONTRACTS,
    SELECTION_CONTRACT,
    SOURCE_POOL_SHA256,
    json_sha256,
    seal,
    sha256_bytes,
)
from tools.phase4_workspace_generalization.validation import (
    apply_negative_mutation,
    validate_generalization_fixture,
)


def _entity_metadata(repository: KernelRepository, entity_id: str, revision: int) -> dict[str, Any]:
    entity = repository.exact(entity_id, revision)
    provenance_entities = repository.provenance_sources(entity_id, revision)
    provenance = sorted(f"{item['id']}@{item['revision']}" for item in provenance_entities)
    return {
        "id": entity_id,
        "revision": revision,
        "type": entity.get("type"),
        "title": entity.get("title"),
        "status": entity.get("status"),
        "review_level": entity.get("review_level"),
        "staleness": entity.get("staleness"),
        "provenance": provenance,
    }


def _maps(fixture: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "candidates": {str(item["id"]): item for item in fixture["candidate_records"]},
        "principia": {(str(item["id"]), int(item["revision"])): item for item in fixture["principia_records"]},
        "warnings": {(str(item["id"]), int(item["revision"])): item for item in fixture["warning_records"]},
    }


def build_export(fixture: Mapping[str, Any], repository: KernelRepository) -> dict[str, Any]:
    validation = validate_generalization_fixture(fixture, repository)
    workspace = fixture["workspace"]
    selection = fixture["selection"]
    maps = _maps(fixture)

    entries: list[dict[str, Any]] = []
    for entry in workspace["entries"]:
        reference = entry["exact_reference"]
        entries.append({
            "entry_id": entry["id"],
            "position": entry["position"],
            "exact_reference": dict(reference),
            "decision": dict(entry["decision"]),
            "original_rank": entry["original_rank"],
            "visible_metadata": _entity_metadata(repository, str(reference["id"]), int(reference["revision"])),
        })

    candidates: list[dict[str, Any]] = []
    for reference in workspace["candidate_references"]:
        source = maps["candidates"][reference["id"]]
        candidates.append({
            "kind": reference["kind"],
            "id": reference["id"],
            "assessment": source["assessment"],
            "left": dict(source["left"]),
            "right": dict(source["right"]),
            "resolution": "unresolved",
            "advisory_only": True,
            "automatic_resolution": False,
        })

    principia: list[dict[str, Any]] = []
    for reference in workspace["principia_references"]:
        source = maps["principia"][(reference["id"], reference["revision"])]
        principia.append({
            "id": source["id"],
            "revision": source["revision"],
            "contract": source["contract"],
            "principia_artifact_id": source["principia_artifact_id"],
            "principia_artifact_revision": source["principia_artifact_revision"],
            "principia_status": source["principia_status"],
            "principia_status_separate": True,
            "atlas_references": [dict(item) for item in source["atlas_references"]],
            "fixture_only": True,
            "live": False,
            "automatic_status_inheritance": False,
        })

    warnings: list[dict[str, Any]] = []
    for reference in workspace["warning_references"]:
        source = maps["warnings"][(reference["id"], reference["revision"])]
        warnings.append({
            "id": source["id"],
            "revision": source["revision"],
            "contract": source["contract"],
            "severity": source["severity"],
            "impact_state": source["impact_state"],
            "target": dict(source["target"]),
            "message": source["message"],
            "implicit_latest": False,
            "automatic_update": False,
        })

    export = {
        "contract": EXPORT_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 1,
        "state": "workspace-generalization-candidate",
        "workspace": {
            "id": workspace["id"],
            "revision": workspace["revision"],
            "validation_digest": validation["report_digest"],
        },
        "source_digest": repository.runtime["source_digest"],
        "upstream_evidence": {
            "research_fixture": {
                "id": fixture["id"],
                "version": fixture["version"],
                "baseline_contract": BASELINE_CONTRACT,
                "report_digest": json_sha256(selection),
            },
            "structured_retrieval": {
                "contract": SELECTION_CONTRACT,
                "index_contract": selection["ranking_reference"]["index_contract"],
                "index_build_digest": selection["ranking_reference"]["index_build_digest"],
                "result_set_sha256": selection["ranking_reference"]["result_set_sha256"],
            },
            "trail": dict(workspace["trail_reference"]),
            "filter": dict(workspace["filter_reference"]),
            "query_snapshot": dict(workspace["query_snapshot"]),
        },
        "generalization_evidence": {
            "previous_fixture_domain": "recommender-systems",
            "candidate_fixture_domain": "catalase-assay-methodology",
            "cross_domain": True,
            "source_pool_sha256": SOURCE_POOL_SHA256,
            "accepted_contracts_reused": dict(REUSED_CONTRACTS),
            "prior_workspace_preserved": True,
            "new_canonical_authoring_authorized": False,
            "browser_implementation_authorized": False,
        },
        "entries": entries,
        "candidate_references": candidates,
        "principia_references": principia,
        "warning_references": warnings,
        "open_questions": list(workspace["open_questions"]),
        "non_graph_summary": list(workspace["non_graph_summary"]),
        "authority": dict(workspace["authority"]),
        "limitations": [
            "This is one non-production cross-domain fixture and does not establish general workspace quality.",
            "Workspace decisions remain research-only and do not change Atlas authority.",
            "Candidate references remain unresolved and do not prove contradiction or duplication.",
            "Principia status remains separate and the referenced envelope is fixture-only and non-live.",
            "The export contains exact references and visible metadata, not copied canonical body authority.",
            "Browser implementation, deployment, accounts, cloud persistence, and production architecture remain unauthorized.",
        ],
        "live": False,
        "repository_mutation": False,
    }
    return seal(export)


def build_manifest(export: Mapping[str, Any], export_bytes: bytes) -> dict[str, Any]:
    return seal({
        "contract": MANIFEST_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 1,
        "state": "workspace-generalization-candidate",
        "workspace": dict(export["workspace"]),
        "files": [{
            "file": "workspace-export.json",
            "contract": EXPORT_CONTRACT,
            "bytes": len(export_bytes),
            "sha256": sha256_bytes(export_bytes),
            "report_digest": export["report_digest"],
        }],
        "deterministic_export": True,
        "replaceable": True,
        "external_network_required": False,
        "account_required": False,
        "cloud_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "canonical_mutation": False,
        "repository_mutation": False,
    })


def validate_manifest(manifest: Mapping[str, Any], export: Mapping[str, Any], export_bytes: bytes) -> dict[str, Any]:
    if manifest.get("contract") != MANIFEST_CONTRACT:
        raise KernelError("E-GENERALIZATION-MANIFEST", f"expected {MANIFEST_CONTRACT!r}")
    if manifest.get("mode") != MODE or manifest.get("phase") != 4 or manifest.get("workstream") != 4 or manifest.get("slice") != 1:
        raise KernelError("E-GENERALIZATION-MANIFEST", "manifest phase, workstream, slice, or mode mismatch")
    digest = manifest.get("report_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise KernelError("E-GENERALIZATION-MANIFEST", "manifest requires a SHA-256 report_digest")
    unsigned = dict(manifest)
    unsigned.pop("report_digest", None)
    if json_sha256(unsigned) != digest:
        raise KernelError("E-GENERALIZATION-MANIFEST", "manifest digest mismatch")
    files = manifest.get("files")
    if not isinstance(files, list) or len(files) != 1 or not isinstance(files[0], Mapping):
        raise KernelError("E-GENERALIZATION-MANIFEST", "manifest must bind one export file")
    entry = files[0]
    if (
        entry.get("file") != "workspace-export.json"
        or entry.get("contract") != EXPORT_CONTRACT
        or entry.get("bytes") != len(export_bytes)
        or entry.get("sha256") != sha256_bytes(export_bytes)
        or entry.get("report_digest") != export.get("report_digest")
    ):
        raise KernelError("E-GENERALIZATION-MANIFEST", "manifest export identity mismatch")
    for field, expected in {
        "deterministic_export": True,
        "replaceable": True,
        "external_network_required": False,
        "account_required": False,
        "cloud_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "canonical_mutation": False,
        "repository_mutation": False,
    }.items():
        if manifest.get(field) != expected:
            raise KernelError("E-GENERALIZATION-MANIFEST", f"manifest requires {field}={expected!r}")
    return {
        "contract": "atlas-phase4-workspace-generalization-manifest-validation/0.1",
        "decision": "valid",
        "workspace": dict(manifest["workspace"]),
        "file_count": 1,
        "manifest_digest": digest,
        "live": False,
        "repository_mutation": False,
    }


def validate_fixture_bundle(fixture: Mapping[str, Any], repository: KernelRepository) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    validation = validate_generalization_fixture(fixture, repository)
    export = build_export(fixture, repository)
    export_bytes = render_json(export).encode("utf-8")
    manifest = build_manifest(export, export_bytes)
    validate_manifest(manifest, export, export_bytes)

    negative_cases = fixture.get("negative_cases")
    if not isinstance(negative_cases, list) or len(negative_cases) != 13:
        raise KernelError("E-GENERALIZATION-NEGATIVE", "fixture requires thirteen negative cases")
    negative_results: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for case in negative_cases:
        if not isinstance(case, Mapping):
            raise KernelError("E-GENERALIZATION-NEGATIVE", "negative case must be an object")
        case_id = str(case.get("id"))
        expected_error = str(case.get("expected_error"))
        if not case_id or case_id in seen_ids:
            raise KernelError("E-GENERALIZATION-NEGATIVE", "negative case IDs must be unique")
        seen_ids.add(case_id)
        candidate = apply_negative_mutation(fixture, case)
        try:
            validate_generalization_fixture(candidate, repository)
        except KernelError as exc:
            if exc.code != expected_error:
                raise KernelError("E-GENERALIZATION-NEGATIVE", f"{case_id} expected {expected_error}, observed {exc.code}") from exc
            negative_results.append({
                "id": case_id,
                "mutation": case["mutation"],
                "observed_error": exc.code,
                "failure_contract": FAILURE_CONTRACT,
                "preserved_prior_accepted_workspace": True,
                "decision": "rejected-as-required",
            })
        else:
            raise KernelError("E-GENERALIZATION-NEGATIVE", f"{case_id} was accepted unexpectedly")

    report = {
        "contract": REPORT_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 1,
        "state": "workspace-generalization-candidate",
        "decision": RECOMMENDATION,
        "fixture_id": fixture["id"],
        "fixture_version": fixture["version"],
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "workspace_validation_digest": validation["report_digest"],
        "selection_digest": json_sha256(fixture["selection"]),
        "export_digest": export["report_digest"],
        "manifest_digest": manifest["report_digest"],
        "counts": {
            "source_pool": validation["source_pool_count"],
            "entries": validation["entry_count"],
            "candidates": validation["candidate_count"],
            "principia_references": validation["principia_reference_count"],
            "warnings": validation["warning_count"],
            "open_questions": validation["open_question_count"],
            "negative_cases": len(negative_results),
        },
        "decision_counts": dict(validation["decision_counts"]),
        "contract_reuse": dict(REUSED_CONTRACTS),
        "negative_validations": negative_results,
        "cross_domain": True,
        "previous_fixture_domain": "recommender-systems",
        "candidate_fixture_domain": "catalase-assay-methodology",
        "prior_workspace_preserved": True,
        "exact_revision_preserved": True,
        "domain_isolated": True,
        "deterministic_export": True,
        "replaceable": True,
        "non_graph_workflow_complete": True,
        "principia_status_separate": True,
        "candidate_resolution_authorized": False,
        "new_canonical_authoring_authorized": False,
        "browser_implementation_authorized": False,
        "implementation_authorized": False,
        "separate_governance_required": True,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "live": False,
        "repository_mutation": False,
        "limitations": [
            "One Catalase fixture cannot establish general workspace quality.",
            "The selection is fixture-bound and does not modify accepted canonical records.",
            "The accepted recommender workspace remains the previous valid state.",
            "Candidates remain advisory and unresolved.",
            "The Principia envelope remains fixture-only, non-live, and status-separate.",
            "Browser reuse requires a separate governance transition.",
            "No production architecture, deployment, account, cloud, or accessibility claim is authorized.",
        ],
        "recommendation": {
            "decision": RECOMMENDATION,
            "purpose": "evaluate whether the accepted static reader can render the Catalase export without contract or authority changes",
            "implementation_authorized": False,
            "separate_governance_required": True,
        },
    }
    return seal(report), validation, export, manifest
