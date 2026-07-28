#!/usr/bin/env python3
"""Deterministic Phase 4 read-only research workspace contracts and exports."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, load_json, render_json

MODE = "interactive-experience-foundation"
FIXTURE_CONTRACT = "atlas-phase4-workspace-fixtures/0.1"
WORKSPACE_CONTRACT = "atlas-research-workspace/0.1"
ENTRY_CONTRACT = "atlas-research-workspace-entry/0.1"
DECISION_CONTRACT = "atlas-research-workspace-decision/0.1"
EXPORT_CONTRACT = "atlas-research-workspace-export/0.1"
MANIFEST_CONTRACT = "atlas-research-workspace-manifest/0.1"
FAILURE_CONTRACT = "atlas-research-workspace-failure/0.1"
REPORT_CONTRACT = "atlas-phase4-workspace-contract-report/0.1"
RESEARCH_BASELINE_CONTRACT = "atlas-phase3-research-foundation-baseline/0.1"
STRUCTURED_BASELINE_CONTRACT = "atlas-phase3-structured-baseline/0.1"

WORKSPACE_ID_RE = re.compile(r"^workspace:en:[a-z0-9]+(?:-[a-z0-9]+)*$")
ENTRY_ID_RE = re.compile(r"^workspace-entry:en:[a-z0-9]+(?:-[a-z0-9]+)*$")
DECISION_ID_RE = re.compile(r"^workspace-decision:en:[a-z0-9]+(?:-[a-z0-9]+)*$")
DECISIONS = frozenset({"include", "exclude", "context"})
CANDIDATE_KINDS = frozenset({"contradiction", "duplicate"})
PROHIBITED_KEYS = frozenset({
    "timestamp", "generated_at", "created_at", "updated_at", "random_id",
    "machine_path", "absolute_path", "credential", "token", "api_key",
})


def _json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _seal(record: Mapping[str, Any]) -> dict[str, Any]:
    unsigned = dict(record)
    unsigned.pop("report_digest", None)
    sealed = dict(record)
    sealed["report_digest"] = _json_sha256(unsigned)
    return sealed


def _require_mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def _require_string(value: Any, code: str, message: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KernelError(code, message)
    return value


def _require_string_list(
    value: Any,
    code: str,
    message: str,
    *,
    allow_empty: bool = False,
) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise KernelError(code, message)
    if not allow_empty and not value:
        raise KernelError(code, message)
    if len(value) != len(set(value)):
        raise KernelError(code, message + " and may not contain duplicates")
    return list(value)


def _exact_key(value: Mapping[str, Any], code: str, field: str) -> str:
    entity_id = _require_string(value.get("id"), code, f"{field} requires entity ID")
    revision = value.get("revision")
    if revision == "latest" or (isinstance(revision, str) and revision.lower() == "latest"):
        raise KernelError("E-WORKSPACE-LATEST", f"{field} may not use implicit latest")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError(code, f"{field} requires a positive exact revision")
    return f"{entity_id}@{revision}"


def _validate_no_nondeterminism(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in PROHIBITED_KEYS:
                raise KernelError("E-WORKSPACE-DETERMINISM", f"prohibited nondeterministic field at {path}.{key}")
            _validate_no_nondeterminism(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _validate_no_nondeterminism(item, f"{path}[{index}]")


def _require_authority(workspace: Mapping[str, Any]) -> None:
    required = {
        "workspace_authority": "ephemeral-research-only",
        "canonical_copy_authority": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "automatic_merge_or_resolution": False,
        "exact_revision_required": True,
        "principia_status_separate": True,
        "non_graph_workflow_required": True,
        "local_first": True,
        "deterministic_export_required": True,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "repository_mutation": False,
    }
    authority = _require_mapping(
        workspace.get("authority"),
        "E-WORKSPACE-AUTHORITY",
        "workspace authority block is required",
    )
    for field, expected in required.items():
        if authority.get(field) != expected:
            if field == "canonical_copy_authority":
                raise KernelError("E-WORKSPACE-COPIED-AUTHORITY", "workspace may not copy canonical authority")
            if field in {"lifecycle_mutation", "review_mutation", "repository_mutation", "canonical_mutation"}:
                raise KernelError("E-WORKSPACE-LIFECYCLE-MUTATION", f"workspace requires {field}=false")
            if field in {"external_network_required", "cloud_required", "account_required"}:
                raise KernelError("E-WORKSPACE-NETWORK", f"workspace requires {field}=false")
            if field == "live_principia_dependency":
                raise KernelError("E-WORKSPACE-PRINCIPIA-STATUS", "workspace may not activate a live Principia dependency")
            if field == "non_graph_workflow_required":
                raise KernelError("E-WORKSPACE-NON-GRAPH", "workspace requires a non-graph equivalent")
            raise KernelError("E-WORKSPACE-AUTHORITY", f"workspace requires {field}={expected!r}")


def _upstream_maps(research_fixture: Mapping[str, Any], bridge_fixture: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "trails": {
            (str(item["id"]), int(item["revision"])): item
            for item in research_fixture.get("trails", [])
        },
        "filters": {
            (str(item["id"]), int(item["revision"])): item
            for item in research_fixture.get("filters", [])
        },
        "contradictions": {
            str(item["id"]): item for item in research_fixture.get("contradiction_candidates", [])
        },
        "duplicates": {
            str(item["id"]): item for item in research_fixture.get("duplicate_candidates", [])
        },
        "principia": {
            (str(item["id"]), int(item["revision"])): item
            for item in bridge_fixture.get("principia_references", [])
        },
        "warnings": {
            (str(item["id"]), int(item["revision"])): item
            for item in bridge_fixture.get("impact_warnings", [])
        },
    }


def validate_workspace(
    workspace: Mapping[str, Any],
    repository: KernelRepository,
    research_fixture: Mapping[str, Any],
    research_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    bridge_fixture: Mapping[str, Any],
) -> dict[str, Any]:
    if workspace.get("contract") != WORKSPACE_CONTRACT:
        raise KernelError("E-WORKSPACE-CONTRACT", f"expected {WORKSPACE_CONTRACT!r}")
    workspace_id = workspace.get("id")
    if not isinstance(workspace_id, str) or not WORKSPACE_ID_RE.fullmatch(workspace_id):
        raise KernelError("E-WORKSPACE-ID", "workspace ID must be workspace:en:<slug>")
    revision = workspace.get("revision")
    if revision == "latest":
        raise KernelError("E-WORKSPACE-LATEST", "workspace revision may not be latest")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError("E-WORKSPACE-REVISION", "workspace revision must be positive")
    if workspace.get("mode") != MODE:
        raise KernelError("E-WORKSPACE-MODE", f"workspace mode must be {MODE!r}")
    if workspace.get("source_digest") != repository.runtime["source_digest"]:
        raise KernelError("E-WORKSPACE-SOURCE", "workspace source digest differs from canonical runtime")
    _validate_no_nondeterminism(workspace)
    _require_authority(workspace)

    if research_baseline.get("contract") != RESEARCH_BASELINE_CONTRACT:
        raise KernelError("E-WORKSPACE-UPSTREAM", "research baseline contract mismatch")
    if structured_baseline.get("contract") != STRUCTURED_BASELINE_CONTRACT:
        raise KernelError("E-WORKSPACE-UPSTREAM", "structured baseline contract mismatch")
    if research_fixture.get("id") != research_baseline.get("fixture_id"):
        raise KernelError("E-WORKSPACE-UPSTREAM", "research fixture identity mismatch")
    if research_fixture.get("source_digest") != repository.runtime["source_digest"]:
        raise KernelError("E-WORKSPACE-UPSTREAM", "research fixture source digest mismatch")
    if research_fixture.get("structured_baseline_sha256") != research_baseline.get("structured_baseline_sha256"):
        raise KernelError("E-WORKSPACE-UPSTREAM", "structured baseline fixture identity mismatch")
    if structured_baseline.get("source_digest") != repository.runtime["source_digest"]:
        raise KernelError("E-WORKSPACE-UPSTREAM", "structured baseline source digest mismatch")

    maps = _upstream_maps(research_fixture, bridge_fixture)
    trail_ref = _require_mapping(
        workspace.get("trail_reference"),
        "E-WORKSPACE-UPSTREAM",
        "trail reference is required",
    )
    trail_key = (_require_string(trail_ref.get("id"), "E-WORKSPACE-UPSTREAM", "trail ID required"), trail_ref.get("revision"))
    if trail_key not in maps["trails"]:
        raise KernelError("E-WORKSPACE-UPSTREAM", "workspace references unavailable trail revision")
    trail = maps["trails"][trail_key]
    filter_ref = _require_mapping(
        workspace.get("filter_reference"),
        "E-WORKSPACE-UPSTREAM",
        "filter reference is required",
    )
    filter_key = (_require_string(filter_ref.get("id"), "E-WORKSPACE-UPSTREAM", "filter ID required"), filter_ref.get("revision"))
    if filter_key not in maps["filters"] or trail.get("filter") != dict(filter_ref):
        raise KernelError("E-WORKSPACE-UPSTREAM", "workspace filter does not match accepted trail")
    if workspace.get("query_snapshot") != trail.get("query_snapshot"):
        raise KernelError("E-WORKSPACE-UPSTREAM", "workspace query snapshot differs from accepted trail")
    if workspace.get("ranking_reference") != trail.get("ranking_reference"):
        raise KernelError("E-WORKSPACE-UPSTREAM", "workspace ranking reference differs from accepted trail")

    entries = workspace.get("entries")
    if not isinstance(entries, list) or not entries:
        raise KernelError("E-WORKSPACE-ENTRIES", "workspace entries must be a nonempty list")
    upstream_entries = trail.get("entries", [])
    if len(entries) != len(upstream_entries):
        raise KernelError("E-WORKSPACE-ENTRIES", "workspace entry count must match accepted trail")
    seen_ids: set[str] = set()
    seen_exact: set[str] = set()
    decisions: list[str] = []
    for index, (entry, upstream) in enumerate(zip(entries, upstream_entries), start=1):
        entry_record = _require_mapping(entry, "E-WORKSPACE-ENTRY", "workspace entry must be an object")
        if entry_record.get("contract") != ENTRY_CONTRACT:
            raise KernelError("E-WORKSPACE-ENTRY", f"expected {ENTRY_CONTRACT!r}")
        entry_id = entry_record.get("id")
        if not isinstance(entry_id, str) or not ENTRY_ID_RE.fullmatch(entry_id):
            raise KernelError("E-WORKSPACE-ENTRY", "entry ID must be workspace-entry:en:<slug>")
        if entry_id in seen_ids:
            raise KernelError("E-WORKSPACE-DUPLICATE-ENTRY", "workspace entry IDs must be unique")
        seen_ids.add(entry_id)
        if entry_record.get("position") != index:
            raise KernelError("E-WORKSPACE-ORDER", "workspace positions must be contiguous and ordered")
        exact_ref = _require_mapping(
            entry_record.get("exact_reference"),
            "E-WORKSPACE-REVISION",
            "entry exact_reference is required",
        )
        exact_key = _exact_key(exact_ref, "E-WORKSPACE-REVISION", "entry exact_reference")
        try:
            repository.exact(str(exact_ref["id"]), int(exact_ref["revision"]))
        except KernelError as exc:
            raise KernelError("E-WORKSPACE-UNAVAILABLE-REVISION", f"unavailable workspace revision {exact_key}") from exc
        if exact_key in seen_exact:
            raise KernelError("E-WORKSPACE-DUPLICATE-ENTRY", "workspace exact references must be unique")
        seen_exact.add(exact_key)
        decision = _require_mapping(
            entry_record.get("decision"),
            "E-WORKSPACE-DECISION",
            "entry decision is required",
        )
        if decision.get("contract") != DECISION_CONTRACT:
            raise KernelError("E-WORKSPACE-DECISION", f"expected {DECISION_CONTRACT!r}")
        decision_id = decision.get("id")
        if not isinstance(decision_id, str) or not DECISION_ID_RE.fullmatch(decision_id):
            raise KernelError("E-WORKSPACE-DECISION", "decision ID must be workspace-decision:en:<slug>")
        action = decision.get("action")
        if action not in DECISIONS:
            raise KernelError("E-WORKSPACE-DECISION", "unsupported workspace decision")
        rationale = _require_string(
            decision.get("rationale"),
            "E-WORKSPACE-DECISION",
            "workspace decision requires rationale",
        )
        expected_upstream = {
            "id": upstream.get("id"),
            "revision": upstream.get("revision"),
        }
        if dict(exact_ref) != expected_upstream:
            raise KernelError("E-WORKSPACE-UPSTREAM", "workspace entry order or exact reference differs from trail")
        if action != upstream.get("action") or rationale != upstream.get("rationale"):
            raise KernelError("E-WORKSPACE-UPSTREAM", "workspace decision differs from accepted trail")
        if entry_record.get("original_rank") != upstream.get("original_rank"):
            raise KernelError("E-WORKSPACE-UPSTREAM", "workspace rank differs from accepted trail")
        if decision.get("advisory_only") is not True or decision.get("canonical_mutation") is not False:
            raise KernelError("E-WORKSPACE-DECISION", "workspace decisions must remain advisory and non-mutating")
        decisions.append(str(action))

    candidate_refs = workspace.get("candidate_references")
    if not isinstance(candidate_refs, list) or len(candidate_refs) != 2:
        raise KernelError("E-WORKSPACE-CANDIDATE", "workspace must reference two advisory candidates")
    candidate_ids: set[str] = set()
    for candidate_ref in candidate_refs:
        ref = _require_mapping(candidate_ref, "E-WORKSPACE-CANDIDATE", "candidate reference must be an object")
        kind = ref.get("kind")
        candidate_id = _require_string(ref.get("id"), "E-WORKSPACE-CANDIDATE", "candidate ID required")
        if kind not in CANDIDATE_KINDS:
            raise KernelError("E-WORKSPACE-CANDIDATE", "unsupported candidate kind")
        source = maps["contradictions"].get(candidate_id) if kind == "contradiction" else maps["duplicates"].get(candidate_id)
        if source is None:
            raise KernelError("E-WORKSPACE-CANDIDATE", "workspace references unavailable candidate")
        if candidate_id in candidate_ids:
            raise KernelError("E-WORKSPACE-CANDIDATE", "candidate references may not repeat")
        candidate_ids.add(candidate_id)
        if ref.get("assessment") != source.get("assessment"):
            raise KernelError("E-WORKSPACE-CANDIDATE", "candidate assessment differs from accepted evidence")
        if ref.get("resolution") != "unresolved" or ref.get("automatic_resolution") is not False:
            raise KernelError("E-WORKSPACE-CANDIDATE-AUTHORITY", "workspace candidates must remain unresolved")
        if ref.get("advisory_only") is not True:
            raise KernelError("E-WORKSPACE-CANDIDATE-AUTHORITY", "workspace candidates must remain advisory")

    principia_refs = workspace.get("principia_references")
    if not isinstance(principia_refs, list) or len(principia_refs) != 1:
        raise KernelError("E-WORKSPACE-PRINCIPIA-STATUS", "workspace requires one pinned Principia reference")
    principia_ref = _require_mapping(
        principia_refs[0],
        "E-WORKSPACE-PRINCIPIA-STATUS",
        "Principia reference must be an object",
    )
    pkey = (
        _require_string(principia_ref.get("id"), "E-WORKSPACE-PRINCIPIA-STATUS", "Principia reference ID required"),
        principia_ref.get("revision"),
    )
    source_principia = maps["principia"].get(pkey)
    if source_principia is None:
        raise KernelError("E-WORKSPACE-PRINCIPIA-STATUS", "workspace references unavailable pinned Principia envelope")
    if principia_ref.get("principia_status") != source_principia.get("principia_status"):
        raise KernelError("E-WORKSPACE-PRINCIPIA-STATUS", "Principia status differs from pinned envelope")
    if (
        principia_ref.get("fixture_only") is not True
        or principia_ref.get("principia_status_separate") is not True
        or principia_ref.get("implicit_latest") is not False
        or principia_ref.get("live") is not False
        or principia_ref.get("automatic_status_inheritance") is not False
    ):
        raise KernelError("E-WORKSPACE-PRINCIPIA-STATUS", "Principia reference must remain pinned, separate, fixture-only, and non-live")

    warning_refs = workspace.get("warning_references")
    if not isinstance(warning_refs, list) or len(warning_refs) != 1:
        raise KernelError("E-WORKSPACE-WARNING", "workspace requires one explicit impact warning reference")
    warning_ref = _require_mapping(warning_refs[0], "E-WORKSPACE-WARNING", "warning reference must be an object")
    warning_key = (
        _require_string(warning_ref.get("id"), "E-WORKSPACE-WARNING", "warning ID required"),
        warning_ref.get("revision"),
    )
    if warning_key not in maps["warnings"]:
        raise KernelError("E-WORKSPACE-WARNING", "workspace references unavailable impact warning")

    open_questions = _require_string_list(
        workspace.get("open_questions"),
        "E-WORKSPACE-QUESTIONS",
        "workspace open questions must be unique strings",
    )
    if open_questions != trail.get("open_questions"):
        raise KernelError("E-WORKSPACE-UPSTREAM", "workspace open questions differ from accepted trail")
    non_graph = _require_string_list(
        workspace.get("non_graph_summary"),
        "E-WORKSPACE-NON-GRAPH",
        "workspace requires complete non-graph summary",
    )
    if len(non_graph) < len(entries):
        raise KernelError("E-WORKSPACE-NON-GRAPH", "non-graph summary must cover every workspace entry")

    validation = {
        "contract": "atlas-research-workspace-validation/0.1",
        "id": workspace_id,
        "revision": revision,
        "entry_count": len(entries),
        "decision_counts": {name: decisions.count(name) for name in sorted(DECISIONS)},
        "candidate_count": len(candidate_refs),
        "principia_reference_count": len(principia_refs),
        "warning_count": len(warning_refs),
        "open_question_count": len(open_questions),
        "exact_revision_preserved": True,
        "authority": "ephemeral-research-only",
        "decision": "valid",
        "live": False,
        "repository_mutation": False,
    }
    validation["report_digest"] = _json_sha256(validation)
    return validation


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


def build_export(
    workspace: Mapping[str, Any],
    repository: KernelRepository,
    research_fixture: Mapping[str, Any],
    research_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    bridge_fixture: Mapping[str, Any],
) -> dict[str, Any]:
    validation = validate_workspace(
        workspace,
        repository,
        research_fixture,
        research_baseline,
        structured_baseline,
        bridge_fixture,
    )
    maps = _upstream_maps(research_fixture, bridge_fixture)
    entries: list[dict[str, Any]] = []
    for entry in workspace["entries"]:
        ref = entry["exact_reference"]
        entries.append({
            "entry_id": entry["id"],
            "position": entry["position"],
            "exact_reference": dict(ref),
            "decision": dict(entry["decision"]),
            "original_rank": entry.get("original_rank"),
            "visible_metadata": _entity_metadata(repository, str(ref["id"]), int(ref["revision"])),
        })
    candidates: list[dict[str, Any]] = []
    for ref in workspace["candidate_references"]:
        source = maps["contradictions"][ref["id"]] if ref["kind"] == "contradiction" else maps["duplicates"][ref["id"]]
        candidates.append({
            "kind": ref["kind"],
            "id": ref["id"],
            "assessment": source["assessment"],
            "left": dict(source["left"]),
            "right": dict(source["right"]),
            "resolution": "unresolved",
            "advisory_only": True,
            "automatic_resolution": False,
        })
    principia: list[dict[str, Any]] = []
    for ref in workspace["principia_references"]:
        source = maps["principia"][(ref["id"], ref["revision"])]
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
    for ref in workspace["warning_references"]:
        source = maps["warnings"][(ref["id"], ref["revision"])]
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
        "workstream": 3,
        "state": "workspace-contract-candidate",
        "workspace": {
            "id": workspace["id"],
            "revision": workspace["revision"],
            "validation_digest": validation["report_digest"],
        },
        "source_digest": repository.runtime["source_digest"],
        "upstream_evidence": {
            "research_fixture": {
                "id": research_fixture["id"],
                "version": research_fixture["version"],
                "baseline_contract": research_baseline["contract"],
                "report_digest": research_baseline["report_digest"],
            },
            "structured_retrieval": {
                "contract": structured_baseline["contract"],
                "index_contract": structured_baseline["index_contract"],
                "index_build_digest": structured_baseline["index_build_digest"],
                "result_set_sha256": structured_baseline["result_set_sha256"],
            },
            "trail": dict(workspace["trail_reference"]),
            "filter": dict(workspace["filter_reference"]),
            "query_snapshot": dict(workspace["query_snapshot"]),
        },
        "entries": entries,
        "candidate_references": candidates,
        "principia_references": principia,
        "warning_references": warnings,
        "open_questions": list(workspace["open_questions"]),
        "non_graph_summary": list(workspace["non_graph_summary"]),
        "authority": dict(workspace["authority"]),
        "limitations": [
            "Workspace decisions are research-only and do not change Atlas authority.",
            "Candidate references remain unresolved and do not prove contradiction or duplication.",
            "Principia status remains separate and the referenced envelope is fixture-only.",
            "The export contains exact references and visible metadata, not copied canonical body authority.",
            "This bounded fixture is not a production retrieval, workspace, accessibility, or browser-support claim.",
        ],
        "live": False,
        "repository_mutation": False,
    }
    return _seal(export)


def build_manifest(export: Mapping[str, Any], export_bytes: bytes) -> dict[str, Any]:
    manifest = {
        "contract": MANIFEST_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 3,
        "state": "workspace-contract-candidate",
        "workspace": dict(export["workspace"]),
        "files": [{
            "file": "workspace-export.json",
            "contract": EXPORT_CONTRACT,
            "bytes": len(export_bytes),
            "sha256": _sha256_bytes(export_bytes),
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
    }
    return _seal(manifest)


def validate_manifest(manifest: Mapping[str, Any], export: Mapping[str, Any], export_bytes: bytes) -> dict[str, Any]:
    if manifest.get("contract") != MANIFEST_CONTRACT:
        raise KernelError("E-WORKSPACE-MANIFEST", f"expected {MANIFEST_CONTRACT!r}")
    if manifest.get("mode") != MODE or manifest.get("phase") != 4 or manifest.get("workstream") != 3:
        raise KernelError("E-WORKSPACE-MANIFEST", "workspace manifest phase or mode mismatch")
    expected_digest = manifest.get("report_digest")
    if not isinstance(expected_digest, str) or len(expected_digest) != 64:
        raise KernelError("E-WORKSPACE-MANIFEST", "workspace manifest requires SHA-256 report_digest")
    unsigned = dict(manifest)
    unsigned.pop("report_digest", None)
    if _json_sha256(unsigned) != expected_digest:
        raise KernelError("E-WORKSPACE-MANIFEST", "workspace manifest digest mismatch")
    files = manifest.get("files")
    if not isinstance(files, list) or len(files) != 1 or not isinstance(files[0], Mapping):
        raise KernelError("E-WORKSPACE-MANIFEST", "workspace manifest must bind one export file")
    entry = files[0]
    if (
        entry.get("file") != "workspace-export.json"
        or entry.get("contract") != EXPORT_CONTRACT
        or entry.get("bytes") != len(export_bytes)
        or entry.get("sha256") != _sha256_bytes(export_bytes)
        or entry.get("report_digest") != export.get("report_digest")
    ):
        raise KernelError("E-WORKSPACE-MANIFEST", "workspace export identity mismatch")
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
            raise KernelError("E-WORKSPACE-MANIFEST", f"workspace manifest requires {field}={expected!r}")
    return {
        "contract": "atlas-research-workspace-manifest-validation/0.1",
        "decision": "valid",
        "workspace": dict(manifest["workspace"]),
        "file_count": 1,
        "manifest_digest": expected_digest,
        "live": False,
        "repository_mutation": False,
    }


def _apply_negative(workspace: Mapping[str, Any], case: Mapping[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(workspace)
    mutation = case.get("mutation")
    if mutation == "implicit-latest":
        candidate["entries"][0]["exact_reference"]["revision"] = "latest"
    elif mutation == "duplicate-entry-id":
        candidate["entries"][1]["id"] = candidate["entries"][0]["id"]
    elif mutation == "copied-authority":
        candidate["authority"]["canonical_copy_authority"] = True
    elif mutation == "resolve-candidate":
        candidate["candidate_references"][0]["resolution"] = "resolved"
        candidate["candidate_references"][0]["automatic_resolution"] = True
    elif mutation == "unavailable-revision":
        candidate["entries"][0]["exact_reference"]["revision"] = 999
    elif mutation == "lifecycle-mutation":
        candidate["authority"]["lifecycle_mutation"] = True
    elif mutation == "live-principia":
        candidate["principia_references"][0]["live"] = True
    elif mutation == "nondeterministic-timestamp":
        candidate["generated_at"] = "2026-07-28T00:00:00Z"
    elif mutation == "external-network":
        candidate["authority"]["external_network_required"] = True
    elif mutation == "missing-non-graph":
        candidate["non_graph_summary"] = []
    else:
        raise KernelError("E-WORKSPACE-NEGATIVE", f"unsupported negative mutation {mutation!r}")
    return candidate


def validate_fixture_bundle(
    fixture: Mapping[str, Any],
    repository: KernelRepository,
    research_fixture: Mapping[str, Any],
    research_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    bridge_fixture: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    if fixture.get("contract") != FIXTURE_CONTRACT:
        raise KernelError("E-WORKSPACE-FIXTURE", f"expected {FIXTURE_CONTRACT!r}")
    if fixture.get("mode") != MODE or fixture.get("version") != 1:
        raise KernelError("E-WORKSPACE-FIXTURE", "workspace fixture mode or version mismatch")
    if fixture.get("source_digest") != repository.runtime["source_digest"]:
        raise KernelError("E-WORKSPACE-FIXTURE", "workspace fixture source digest mismatch")
    workspace = _require_mapping(
        fixture.get("workspace"),
        "E-WORKSPACE-FIXTURE",
        "workspace fixture requires workspace object",
    )
    validation = validate_workspace(
        workspace,
        repository,
        research_fixture,
        research_baseline,
        structured_baseline,
        bridge_fixture,
    )
    export = build_export(
        workspace,
        repository,
        research_fixture,
        research_baseline,
        structured_baseline,
        bridge_fixture,
    )
    export_bytes = render_json(export).encode("utf-8")
    manifest = build_manifest(export, export_bytes)
    validate_manifest(manifest, export, export_bytes)

    negative_cases = fixture.get("negative_cases")
    if not isinstance(negative_cases, list) or len(negative_cases) != 10:
        raise KernelError("E-WORKSPACE-NEGATIVE", "workspace fixture requires ten negative cases")
    negative_results: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for case in negative_cases:
        case_record = _require_mapping(case, "E-WORKSPACE-NEGATIVE", "negative case must be an object")
        case_id = _require_string(case_record.get("id"), "E-WORKSPACE-NEGATIVE", "negative case ID required")
        expected_error = _require_string(
            case_record.get("expected_error"),
            "E-WORKSPACE-NEGATIVE",
            "negative case expected_error required",
        )
        if case_id in seen_ids:
            raise KernelError("E-WORKSPACE-NEGATIVE", "negative case IDs must be unique")
        seen_ids.add(case_id)
        candidate = _apply_negative(workspace, case_record)
        try:
            validate_workspace(
                candidate,
                repository,
                research_fixture,
                research_baseline,
                structured_baseline,
                bridge_fixture,
            )
        except KernelError as exc:
            if exc.code != expected_error:
                raise KernelError(
                    "E-WORKSPACE-NEGATIVE",
                    f"{case_id} expected {expected_error}, observed {exc.code}",
                ) from exc
            negative_results.append({
                "id": case_id,
                "mutation": case_record["mutation"],
                "observed_error": exc.code,
                "preserved_previous_valid_workspace": True,
                "decision": "rejected-as-required",
            })
        else:
            raise KernelError("E-WORKSPACE-NEGATIVE", f"{case_id} was accepted unexpectedly")

    report = {
        "contract": REPORT_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 3,
        "state": "workspace-contract-candidate",
        "decision": "workspace-contract-candidate",
        "fixture_id": fixture.get("id"),
        "fixture_version": fixture.get("version"),
        "source_digest": repository.runtime["source_digest"],
        "entity_count": repository.runtime["entity_count"],
        "workspace_validation_digest": validation["report_digest"],
        "export_digest": export["report_digest"],
        "manifest_digest": manifest["report_digest"],
        "counts": {
            "entries": validation["entry_count"],
            "candidates": validation["candidate_count"],
            "principia_references": validation["principia_reference_count"],
            "warnings": validation["warning_count"],
            "open_questions": validation["open_question_count"],
            "negative_cases": len(negative_results),
        },
        "decision_counts": validation["decision_counts"],
        "negative_validations": negative_results,
        "exact_revision_preserved": True,
        "deterministic_export": True,
        "replaceable": True,
        "workspace_authority": "ephemeral-research-only",
        "canonical_copy_authority": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "automatic_merge_or_resolution": False,
        "principia_status_separate": True,
        "non_graph_workflow_complete": True,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "live": False,
        "repository_mutation": False,
    }
    return _seal(report), export, manifest


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument(
        "--fixture",
        type=Path,
        default=Path("content/fixtures/phase4_workspace/research-workspace.v01.json"),
    )
    parser.add_argument(
        "--research-fixture",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/research-foundations.v01.json"),
    )
    parser.add_argument(
        "--research-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/research-foundations-baseline.json"),
    )
    parser.add_argument(
        "--structured-baseline",
        type=Path,
        default=Path("content/fixtures/phase3_retrieval/structured-baseline.json"),
    )
    parser.add_argument(
        "--bridge-fixture",
        type=Path,
        default=Path("content/fixtures/phase4_interaction/bridge-failures.v01.json"),
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)

    repository = KernelRepository(compile_canonical(args.canonical_root))
    fixture = load_json(args.fixture)
    report, export, manifest = validate_fixture_bundle(
        fixture,
        repository,
        load_json(args.research_fixture),
        load_json(args.research_baseline),
        load_json(args.structured_baseline),
        load_json(args.bridge_fixture),
    )
    rendered_report = render_json(report)
    if args.output_dir is None:
        sys.stdout.write(rendered_report)
    else:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        export_path = args.output_dir / "workspace-export.json"
        manifest_path = args.output_dir / "workspace-manifest.json"
        report_path = args.output_dir / "workspace-report.json"
        export_path.write_text(render_json(export), encoding="utf-8")
        manifest_path.write_text(render_json(manifest), encoding="utf-8")
        report_path.write_text(rendered_report, encoding="utf-8")
        print(f"wrote={export_path}")
        print(f"wrote={manifest_path}")
        print(f"wrote={report_path}")
    print(f"phase4-workspace-report-digest={report['report_digest']}")
    print(f"phase4-workspace-export-digest={export['report_digest']}")
    print(f"phase4-workspace-manifest-digest={manifest['report_digest']}")
    print("phase4-workspace=contract-candidate; authority=ephemeral-research-only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
