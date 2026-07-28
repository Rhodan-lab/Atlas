#!/usr/bin/env python3
"""Validate the bounded Catalase workspace fixture without changing accepted contracts."""
from __future__ import annotations

import copy
from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository
from tools.phase4_workspace_generalization.constants import (
    EXPECTED_AUTHORITY,
    FIXTURE_CONTRACT,
    MODE,
    PRIOR_EXPORT_DIGEST,
    PRIOR_EXPORT_SHA256,
    REUSED_CONTRACTS,
    SELECTION_CONTRACT,
    SELECTED_ENTRY_KEYS,
    SOURCE_DIGEST,
    SOURCE_POOL,
    SOURCE_POOL_SHA256,
    VALIDATION_CONTRACT,
    exact_key,
    json_sha256,
    require_mapping,
    require_string,
    seal,
    validate_no_nondeterminism,
)


def _require_exact(repository: KernelRepository, reference: Mapping[str, Any], code: str) -> dict[str, Any]:
    key = exact_key(reference, code)
    try:
        return repository.exact(str(reference["id"]), int(reference["revision"]))
    except KernelError as exc:
        raise KernelError(code, f"unavailable exact revision {key}") from exc


def _source_maps(fixture: Mapping[str, Any]) -> dict[str, Any]:
    candidates = fixture.get("candidate_records")
    principia = fixture.get("principia_records")
    warnings = fixture.get("warning_records")
    if not isinstance(candidates, list) or len(candidates) != 2:
        raise KernelError("E-GENERALIZATION-CANDIDATE", "fixture requires two candidate records")
    if not isinstance(principia, list) or len(principia) != 1:
        raise KernelError("E-GENERALIZATION-PRINCIPIA", "fixture requires one Principia record")
    if not isinstance(warnings, list) or len(warnings) != 1:
        raise KernelError("E-GENERALIZATION-WARNING", "fixture requires one warning record")
    return {
        "candidates": {str(item.get("id")): item for item in candidates if isinstance(item, Mapping)},
        "principia": {(str(item.get("id")), item.get("revision")): item for item in principia if isinstance(item, Mapping)},
        "warnings": {(str(item.get("id")), item.get("revision")): item for item in warnings if isinstance(item, Mapping)},
    }


def _validate_selection(fixture: Mapping[str, Any], repository: KernelRepository) -> tuple[Mapping[str, Any], Mapping[str, Any]]:
    selection = require_mapping(fixture.get("selection"), "E-GENERALIZATION-SELECTION", "generalization selection is required")
    if selection.get("contract") != SELECTION_CONTRACT:
        raise KernelError("E-GENERALIZATION-SELECTION", f"expected {SELECTION_CONTRACT!r}")
    source_pool = selection.get("source_pool")
    if source_pool != SOURCE_POOL:
        raise KernelError("E-GENERALIZATION-DOMAIN", "source pool differs from the authorized Catalase records")
    if json_sha256(source_pool) != SOURCE_POOL_SHA256:
        raise KernelError("E-GENERALIZATION-DETERMINISM", "source-pool digest mismatch")
    for reference in source_pool:
        exact_reference = require_mapping(reference, "E-GENERALIZATION-REVISION", "source reference must be an object")
        _require_exact(repository, exact_reference, "E-GENERALIZATION-REVISION")
        entity_id = str(reference["id"])
        if "catalase" not in entity_id and not entity_id.startswith("src:"):
            raise KernelError("E-GENERALIZATION-DOMAIN", "source pool contains a non-Catalase record")

    filter_record = require_mapping(selection.get("filter"), "E-GENERALIZATION-SELECTION", "selection filter is required")
    if filter_record.get("id") != "filter:en:catalase-assay-methodology" or filter_record.get("revision") != 1:
        raise KernelError("E-GENERALIZATION-SELECTION", "selection filter identity mismatch")

    ranking = require_mapping(selection.get("ranking_reference"), "E-GENERALIZATION-SELECTION", "ranking reference is required")
    required_ranking = {
        "baseline_contract": SELECTION_CONTRACT,
        "index_build_digest": SOURCE_DIGEST,
        "index_contract": "atlas-kernel-runtime/0.1",
        "result_set_sha256": SOURCE_POOL_SHA256,
    }
    for field, expected in required_ranking.items():
        if ranking.get(field) != expected:
            raise KernelError("E-GENERALIZATION-SELECTION", f"ranking reference requires {field}={expected!r}")

    query = require_mapping(selection.get("query_snapshot"), "E-GENERALIZATION-SELECTION", "query snapshot is required")
    if query.get("id") != "query:workspace:catalase-assay-scope" or not isinstance(query.get("text"), str):
        raise KernelError("E-GENERALIZATION-SELECTION", "query snapshot identity mismatch")

    trail = require_mapping(selection.get("trail"), "E-GENERALIZATION-TRAIL", "selection trail is required")
    if trail.get("id") != "trail:en:catalase-assay-scope-review" or trail.get("revision") != 1:
        raise KernelError("E-GENERALIZATION-TRAIL", "trail identity mismatch")
    entries = trail.get("entries")
    if not isinstance(entries, list) or len(entries) != 5:
        raise KernelError("E-GENERALIZATION-TRAIL", "trail requires exactly five entries")
    keys = [f"{entry.get('id')}@{entry.get('revision')}" for entry in entries if isinstance(entry, Mapping)]
    if keys != SELECTED_ENTRY_KEYS:
        raise KernelError("E-GENERALIZATION-TRAIL", "trail order differs from the authorized five-entry selection")
    questions = trail.get("open_questions")
    if not isinstance(questions, list) or len(questions) != 2 or len(set(questions)) != 2:
        raise KernelError("E-GENERALIZATION-TRAIL", "trail requires two unique open questions")
    return selection, trail


def validate_generalization_fixture(fixture: Mapping[str, Any], repository: KernelRepository) -> dict[str, Any]:
    if fixture.get("contract") != FIXTURE_CONTRACT:
        raise KernelError("E-GENERALIZATION-FIXTURE", f"expected {FIXTURE_CONTRACT!r}")
    if fixture.get("mode") != MODE or fixture.get("version") != 1:
        raise KernelError("E-GENERALIZATION-FIXTURE", "fixture mode or version mismatch")
    if fixture.get("source_digest") != repository.runtime.get("source_digest") or fixture.get("source_digest") != SOURCE_DIGEST:
        raise KernelError("E-GENERALIZATION-FIXTURE", "fixture source digest mismatch")
    if fixture.get("new_canonical_authoring_authorized") is not False:
        raise KernelError("E-GENERALIZATION-AUTHORITY", "new canonical authoring is forbidden")
    if fixture.get("production_implementation_authorized") is not False:
        raise KernelError("E-GENERALIZATION-AUTHORITY", "production implementation is forbidden")
    if fixture.get("browser_implementation_authorized") is not False:
        raise KernelError("E-GENERALIZATION-BROWSER", "browser implementation is not authorized in Slice 1")

    validate_no_nondeterminism(fixture)
    prior = require_mapping(fixture.get("prior_accepted_workspace"), "E-GENERALIZATION-PRIOR", "prior accepted workspace identity is required")
    required_prior = {
        "baseline_contract": "atlas-phase4-workspace-contract-baseline/0.1",
        "export_report_digest": PRIOR_EXPORT_DIGEST,
        "export_sha256": PRIOR_EXPORT_SHA256,
        "preserved_as_previous_valid_state": True,
    }
    for field, expected in required_prior.items():
        if prior.get(field) != expected:
            raise KernelError("E-GENERALIZATION-PRIOR", f"prior workspace requires {field}={expected!r}")

    selection, trail = _validate_selection(fixture, repository)
    maps = _source_maps(fixture)
    workspace = require_mapping(fixture.get("workspace"), "E-GENERALIZATION-WORKSPACE", "workspace object is required")
    if workspace.get("contract") != REUSED_CONTRACTS["workspace"]:
        raise KernelError("E-GENERALIZATION-CONTRACT", "accepted workspace contract must be reused unchanged")
    if workspace.get("id") != "workspace:en:catalase-assay-scope-review" or workspace.get("revision") != 1:
        raise KernelError("E-GENERALIZATION-WORKSPACE", "workspace identity mismatch")
    if workspace.get("mode") != MODE or workspace.get("source_digest") != SOURCE_DIGEST:
        raise KernelError("E-GENERALIZATION-WORKSPACE", "workspace mode or source digest mismatch")

    authority = require_mapping(workspace.get("authority"), "E-GENERALIZATION-AUTHORITY", "workspace authority is required")
    for field, expected in EXPECTED_AUTHORITY.items():
        if authority.get(field) != expected:
            if field == "external_network_required":
                raise KernelError("E-GENERALIZATION-NETWORK", "external network is forbidden")
            raise KernelError("E-GENERALIZATION-AUTHORITY", f"workspace requires {field}={expected!r}")

    if workspace.get("filter_reference") != {"id": selection["filter"]["id"], "revision": selection["filter"]["revision"]}:
        raise KernelError("E-GENERALIZATION-UPSTREAM", "workspace filter differs from the selection")
    if workspace.get("trail_reference") != {"id": trail["id"], "revision": trail["revision"]}:
        raise KernelError("E-GENERALIZATION-UPSTREAM", "workspace trail differs from the selection")
    if workspace.get("query_snapshot") != selection.get("query_snapshot"):
        raise KernelError("E-GENERALIZATION-UPSTREAM", "workspace query differs from the selection")
    if workspace.get("ranking_reference") != selection.get("ranking_reference"):
        raise KernelError("E-GENERALIZATION-UPSTREAM", "workspace ranking reference differs from the selection")

    entries = workspace.get("entries")
    if not isinstance(entries, list) or len(entries) != 5:
        raise KernelError("E-GENERALIZATION-ENTRIES", "workspace requires exactly five entries")
    seen_entry_ids: set[str] = set()
    seen_exact: set[str] = set()
    decision_ids: set[str] = set()
    decision_counts = {"context": 0, "exclude": 0, "include": 0}
    for position, (entry, trail_entry) in enumerate(zip(entries, trail["entries"]), start=1):
        item = require_mapping(entry, "E-GENERALIZATION-ENTRIES", "workspace entry must be an object")
        if item.get("contract") != REUSED_CONTRACTS["entry"]:
            raise KernelError("E-GENERALIZATION-CONTRACT", "accepted entry contract must be reused unchanged")
        entry_id = require_string(item.get("id"), "E-GENERALIZATION-ENTRIES", "entry ID is required")
        if entry_id in seen_entry_ids:
            raise KernelError("E-GENERALIZATION-DUPLICATE", "workspace entry IDs must be unique")
        seen_entry_ids.add(entry_id)
        if item.get("position") != position:
            raise KernelError("E-GENERALIZATION-TRAIL", "workspace positions must be contiguous")
        reference = require_mapping(item.get("exact_reference"), "E-GENERALIZATION-REVISION", "entry exact reference is required")
        key = exact_key(reference, "E-GENERALIZATION-REVISION")
        if key in seen_exact:
            raise KernelError("E-GENERALIZATION-DUPLICATE", "workspace exact references must be unique")
        seen_exact.add(key)
        _require_exact(repository, reference, "E-GENERALIZATION-REVISION")
        if key not in SELECTED_ENTRY_KEYS:
            raise KernelError("E-GENERALIZATION-DOMAIN", "workspace entry is outside the authorized Catalase selection")
        if key != f"{trail_entry.get('id')}@{trail_entry.get('revision')}":
            raise KernelError("E-GENERALIZATION-TRAIL", "workspace entry order differs from the trail")
        decision = require_mapping(item.get("decision"), "E-GENERALIZATION-DECISION", "entry decision is required")
        if decision.get("contract") != REUSED_CONTRACTS["decision"]:
            raise KernelError("E-GENERALIZATION-CONTRACT", "accepted decision contract must be reused unchanged")
        decision_id = require_string(decision.get("id"), "E-GENERALIZATION-DECISION", "decision ID is required")
        if decision_id in decision_ids:
            raise KernelError("E-GENERALIZATION-DUPLICATE", "decision IDs must be unique")
        decision_ids.add(decision_id)
        action = decision.get("action")
        if action not in decision_counts:
            raise KernelError("E-GENERALIZATION-DECISION", "unsupported workspace decision")
        decision_counts[str(action)] += 1
        if decision.get("rationale") != trail_entry.get("rationale") or action != trail_entry.get("action"):
            raise KernelError("E-GENERALIZATION-TRAIL", "workspace decision differs from the trail")
        if decision.get("advisory_only") is not True or decision.get("canonical_mutation") is not False:
            raise KernelError("E-GENERALIZATION-AUTHORITY", "workspace decisions must remain advisory and non-mutating")
        if item.get("original_rank") != trail_entry.get("original_rank"):
            raise KernelError("E-GENERALIZATION-TRAIL", "workspace rank differs from the trail")

    candidate_refs = workspace.get("candidate_references")
    if not isinstance(candidate_refs, list) or len(candidate_refs) != 2:
        raise KernelError("E-GENERALIZATION-CANDIDATE", "workspace requires two advisory candidates")
    observed_kinds: set[str] = set()
    source_pool_keys = {f"{item['id']}@{item['revision']}" for item in SOURCE_POOL}
    for candidate in candidate_refs:
        ref = require_mapping(candidate, "E-GENERALIZATION-CANDIDATE", "candidate reference must be an object")
        source = maps["candidates"].get(str(ref.get("id")))
        if source is None:
            raise KernelError("E-GENERALIZATION-CANDIDATE", "candidate record is unavailable")
        kind = ref.get("kind")
        if kind not in {"contradiction", "duplicate"} or kind in observed_kinds:
            raise KernelError("E-GENERALIZATION-CANDIDATE", "candidate kinds must be contradiction and duplicate")
        observed_kinds.add(str(kind))
        if kind != source.get("kind") or ref.get("assessment") != source.get("assessment"):
            raise KernelError("E-GENERALIZATION-CANDIDATE", "candidate assessment differs from source evidence")
        for side in ("left", "right"):
            source_ref = require_mapping(source.get(side), "E-GENERALIZATION-CANDIDATE", "candidate exact reference is required")
            if exact_key(source_ref, "E-GENERALIZATION-REVISION") not in source_pool_keys:
                raise KernelError("E-GENERALIZATION-DOMAIN", "candidate reference is outside the Catalase source pool")
            _require_exact(repository, source_ref, "E-GENERALIZATION-REVISION")
        if ref.get("resolution") != "unresolved" or ref.get("automatic_resolution") is not False or ref.get("advisory_only") is not True:
            raise KernelError("E-GENERALIZATION-CANDIDATE", "candidates must remain unresolved and advisory")

    principia_refs = workspace.get("principia_references")
    if not isinstance(principia_refs, list) or len(principia_refs) != 1:
        raise KernelError("E-GENERALIZATION-PRINCIPIA", "workspace requires one Principia reference")
    pref = require_mapping(principia_refs[0], "E-GENERALIZATION-PRINCIPIA", "Principia reference must be an object")
    source_principia = maps["principia"].get((str(pref.get("id")), pref.get("revision")))
    if source_principia is None:
        raise KernelError("E-GENERALIZATION-PRINCIPIA", "pinned Principia envelope is unavailable")
    required_principia = {
        "fixture_only": True,
        "principia_status": source_principia.get("principia_status"),
        "principia_status_separate": True,
        "implicit_latest": False,
        "live": False,
        "automatic_status_inheritance": False,
    }
    for field, expected in required_principia.items():
        if pref.get(field) != expected:
            raise KernelError("E-GENERALIZATION-PRINCIPIA", f"Principia reference requires {field}={expected!r}")
    for reference in source_principia.get("atlas_references", []):
        exact_reference = require_mapping(reference, "E-GENERALIZATION-PRINCIPIA", "Principia Atlas reference must be an object")
        _require_exact(repository, exact_reference, "E-GENERALIZATION-REVISION")

    warning_refs = workspace.get("warning_references")
    if not isinstance(warning_refs, list) or len(warning_refs) != 1:
        raise KernelError("E-GENERALIZATION-WARNING", "workspace requires one explicit warning")
    wref = require_mapping(warning_refs[0], "E-GENERALIZATION-WARNING", "warning reference must be an object")
    source_warning = maps["warnings"].get((str(wref.get("id")), wref.get("revision")))
    if source_warning is None:
        raise KernelError("E-GENERALIZATION-WARNING", "warning record is unavailable")
    if source_warning.get("implicit_latest") is not False or source_warning.get("automatic_update") is not False:
        raise KernelError("E-GENERALIZATION-WARNING", "warning must forbid fallback and automatic update")
    target = require_mapping(source_warning.get("target"), "E-GENERALIZATION-WARNING", "warning target is required")
    try:
        repository.exact(str(target["id"]), int(target["revision"]))
    except KernelError:
        pass
    else:
        raise KernelError("E-GENERALIZATION-WARNING", "warning target must be unavailable")
    _require_exact(repository, {"id": target["id"], "revision": 1}, "E-GENERALIZATION-REVISION")

    if workspace.get("open_questions") != trail.get("open_questions"):
        raise KernelError("E-GENERALIZATION-UPSTREAM", "workspace open questions differ from the trail")
    non_graph = workspace.get("non_graph_summary")
    if not isinstance(non_graph, list) or len(non_graph) != 5 or not all(isinstance(item, str) and item for item in non_graph):
        raise KernelError("E-GENERALIZATION-NON-GRAPH", "non-graph summary must cover all five entries")

    validation = {
        "contract": VALIDATION_CONTRACT,
        "mode": MODE,
        "phase": 4,
        "workstream": 4,
        "slice": 1,
        "workspace_id": workspace["id"],
        "workspace_revision": workspace["revision"],
        "source_pool_count": len(SOURCE_POOL),
        "entry_count": len(entries),
        "decision_counts": decision_counts,
        "candidate_count": len(candidate_refs),
        "principia_reference_count": len(principia_refs),
        "warning_count": len(warning_refs),
        "open_question_count": len(workspace["open_questions"]),
        "negative_case_count": len(fixture.get("negative_cases", [])),
        "contract_reuse": dict(REUSED_CONTRACTS),
        "exact_revision_preserved": True,
        "domain_isolated": True,
        "prior_workspace_preserved": True,
        "browser_implementation_authorized": False,
        "new_canonical_authoring_authorized": False,
        "decision": "valid-catalase-contract-reuse-candidate",
        "live": False,
        "repository_mutation": False,
    }
    return seal(validation)


def apply_negative_mutation(workspace_fixture: Mapping[str, Any], case: Mapping[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(workspace_fixture)
    mutation = case.get("mutation")
    if mutation == "implicit-latest":
        candidate["workspace"]["entries"][0]["exact_reference"]["revision"] = "latest"
    elif mutation == "domain-leakage":
        candidate["workspace"]["entries"][0]["exact_reference"] = {"id": "claim:en:recommender-effects-are-context-dependent", "revision": 1}
    elif mutation == "duplicate-entry":
        candidate["workspace"]["entries"][1]["id"] = candidate["workspace"]["entries"][0]["id"]
    elif mutation == "unavailable-revision":
        candidate["workspace"]["entries"][0]["exact_reference"]["revision"] = 99
    elif mutation == "contract-drift":
        candidate["workspace"]["contract"] = "atlas-research-workspace/0.2"
    elif mutation == "copied-authority":
        candidate["workspace"]["authority"]["canonical_copy_authority"] = True
    elif mutation == "resolve-candidate":
        candidate["workspace"]["candidate_references"][0]["resolution"] = "resolved"
        candidate["workspace"]["candidate_references"][0]["automatic_resolution"] = True
    elif mutation == "live-principia":
        candidate["workspace"]["principia_references"][0]["live"] = True
    elif mutation == "missing-non-graph":
        candidate["workspace"]["non_graph_summary"] = []
    elif mutation == "nondeterministic-timestamp":
        candidate["generated_at"] = "2026-07-29T00:00:00Z"
    elif mutation == "external-network":
        candidate["workspace"]["authority"]["external_network_required"] = True
    elif mutation == "lifecycle-mutation":
        candidate["workspace"]["authority"]["lifecycle_mutation"] = True
    elif mutation == "browser-implementation":
        candidate["browser_implementation_authorized"] = True
    else:
        raise KernelError("E-GENERALIZATION-NEGATIVE", f"unsupported negative mutation {mutation!r}")
    return candidate
