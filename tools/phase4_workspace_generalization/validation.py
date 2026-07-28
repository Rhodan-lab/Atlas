"""Positive validation for one Catalase cross-domain fixture."""
from __future__ import annotations

from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository
from tools.phase4_workspace.contracts import (
    EXPORT_CONTRACT,
    FIXTURE_CONTRACT,
    MANIFEST_CONTRACT,
    MODE,
    validate_fixture_bundle as validate_workspace_fixture_bundle,
)
from tools.phase4_workspace_generalization.constants import (
    ALLOWED_RECOMMENDATIONS,
    EXPECTED_SOURCE_POOL,
    EXPECTED_TRAIL,
    GENERALIZATION_FIXTURE_CONTRACT,
    GENERALIZATION_VALIDATION_CONTRACT,
    REUSED_CONTRACTS,
)
from tools.phase4_workspace_generalization.util import exact_key, require_list, require_mapping, seal


def validate_boundaries(fixture: Mapping[str, Any]) -> Mapping[str, Any]:
    boundaries = require_mapping(
        fixture.get("boundaries"),
        "E-GENERALIZATION-BOUNDARY",
        "generalization fixture requires explicit boundaries",
    )
    required = {
        "fixture_count_authorized": 1,
        "cross_domain_required": True,
        "existing_canonical_revisions_only": True,
        "new_canonical_authoring_authorized": False,
        "browser_implementation_authorized": False,
        "production_implementation_authorized": False,
        "release_mutation": False,
        "candidate_resolution_authorized": False,
        "live_principia_dependency": False,
    }
    for field, expected in required.items():
        if boundaries.get(field) == expected:
            continue
        if field == "fixture_count_authorized":
            raise KernelError("E-GENERALIZATION-FIXTURE-COUNT", "exactly one fixture is authorized")
        if field in {"release_mutation", "candidate_resolution_authorized"}:
            raise KernelError("E-GENERALIZATION-AUTHORITY", f"{field} must remain false")
        raise KernelError("E-GENERALIZATION-BOUNDARY", f"{field} must be {expected!r}")
    return boundaries


def validate_source_pool(fixture: Mapping[str, Any], repository: KernelRepository) -> list[dict[str, Any]]:
    raw_pool = require_list(
        fixture.get("canonical_source_pool"),
        "E-GENERALIZATION-SOURCE-POOL",
        "canonical source pool must be a list",
    )
    keys: list[str] = []
    normalized: list[dict[str, Any]] = []
    for raw in raw_pool:
        ref = require_mapping(raw, "E-GENERALIZATION-SOURCE-POOL", "source-pool item must be an object")
        key = exact_key(ref, "E-GENERALIZATION-SOURCE-POOL")
        keys.append(key)
        try:
            repository.exact(str(ref["id"]), int(ref["revision"]))
        except KernelError as exc:
            raise KernelError(
                "E-GENERALIZATION-SOURCE-POOL",
                f"required exact canonical revision is unavailable: {key}",
            ) from exc
        normalized.append(dict(ref))
    if tuple(keys) != EXPECTED_SOURCE_POOL:
        raise KernelError(
            "E-GENERALIZATION-SOURCE-POOL",
            "source pool must bind the eight authorized Catalase exact revisions in order",
        )
    return normalized


def validate_catalase_selection(workspace: Mapping[str, Any]) -> list[str]:
    entries = require_list(workspace.get("entries"), "E-GENERALIZATION-TRAIL", "workspace entries must be a list")
    if len(entries) != 5:
        raise KernelError("E-GENERALIZATION-TRAIL", "Catalase trail must contain exactly five entries")
    keys: list[str] = []
    for entry in entries:
        record = require_mapping(entry, "E-GENERALIZATION-TRAIL", "workspace entry must be an object")
        ref = require_mapping(
            record.get("exact_reference"),
            "E-GENERALIZATION-TRAIL",
            "workspace entry requires exact_reference",
        )
        key = exact_key(ref, "E-GENERALIZATION-TRAIL")
        if "recommender" in key:
            raise KernelError("E-GENERALIZATION-DOMAIN", "recommender-system entries are forbidden")
        if key not in EXPECTED_SOURCE_POOL:
            raise KernelError("E-GENERALIZATION-DOMAIN", "workspace entry is outside the Catalase source pool")
        keys.append(key)
    if tuple(keys) != EXPECTED_TRAIL:
        raise KernelError("E-GENERALIZATION-ORDER", "Catalase accepted trail order differs from the authorized selection")
    return keys


def validate_scope_candidate(workspace: Mapping[str, Any], research_fixture: Mapping[str, Any]) -> None:
    refs = require_list(
        workspace.get("candidate_references"),
        "E-GENERALIZATION-CANDIDATE",
        "candidate references must be a list",
    )
    if len(refs) != 2:
        raise KernelError("E-GENERALIZATION-CANDIDATE", "exactly two unresolved candidates are required")
    evidence: dict[str, Mapping[str, Any]] = {}
    for field in ("contradiction_candidates", "duplicate_candidates"):
        items = require_list(research_fixture.get(field, []), "E-GENERALIZATION-CANDIDATE", f"{field} must be a list")
        for item in items:
            record = require_mapping(item, "E-GENERALIZATION-CANDIDATE", "candidate evidence must be an object")
            candidate_id = record.get("id")
            if isinstance(candidate_id, str):
                evidence[candidate_id] = record
    assessments: list[str] = []
    for ref in refs:
        record = require_mapping(ref, "E-GENERALIZATION-CANDIDATE", "candidate reference must be an object")
        candidate_id = record.get("id")
        source = evidence.get(candidate_id) if isinstance(candidate_id, str) else None
        if source is None:
            raise KernelError("E-GENERALIZATION-CANDIDATE", "candidate evidence is unavailable")
        assessment = source.get("assessment")
        if isinstance(assessment, str):
            assessments.append(assessment)
    if "scope-difference-likely" not in assessments:
        raise KernelError("E-GENERALIZATION-CANDIDATE", "at least one scope-difference assessment is required")


def validate_unavailable_warning(
    workspace: Mapping[str, Any], bridge_fixture: Mapping[str, Any], repository: KernelRepository
) -> str:
    refs = require_list(
        workspace.get("warning_references"),
        "E-GENERALIZATION-WARNING",
        "workspace warning references must be a list",
    )
    if len(refs) != 1:
        raise KernelError("E-GENERALIZATION-WARNING", "exactly one unavailable-revision warning is required")
    ref = require_mapping(refs[0], "E-GENERALIZATION-WARNING", "warning reference must be an object")
    warning = None
    for raw in require_list(
        bridge_fixture.get("impact_warnings", []),
        "E-GENERALIZATION-WARNING",
        "impact warnings must be a list",
    ):
        item = require_mapping(raw, "E-GENERALIZATION-WARNING", "impact warning must be an object")
        if item.get("id") == ref.get("id") and item.get("revision") == ref.get("revision"):
            warning = item
            break
    if warning is None:
        raise KernelError("E-GENERALIZATION-WARNING", "pinned warning is unavailable")
    target = require_mapping(warning.get("target"), "E-GENERALIZATION-WARNING", "warning requires an exact target")
    target_key = exact_key(target, "E-GENERALIZATION-WARNING")
    try:
        repository.exact(str(target["id"]), int(target["revision"]))
    except KernelError:
        return target_key
    raise KernelError("E-GENERALIZATION-WARNING", "warning target unexpectedly resolves; unavailable state was not preserved")


def validate_positive(
    fixture: Mapping[str, Any], repository: KernelRepository
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    if fixture.get("contract") != GENERALIZATION_FIXTURE_CONTRACT:
        raise KernelError("E-GENERALIZATION-CONTRACT", f"expected {GENERALIZATION_FIXTURE_CONTRACT!r}")
    if fixture.get("mode") != MODE or fixture.get("phase") != 4 or fixture.get("workstream") != 4:
        raise KernelError("E-GENERALIZATION-MODE", "generalization phase, workstream, or mode mismatch")
    if fixture.get("slice") != 1 or fixture.get("version") != 1:
        raise KernelError("E-GENERALIZATION-MODE", "generalization slice and version must both equal 1")
    if fixture.get("domain") != "catalase-assay-methodology":
        raise KernelError("E-GENERALIZATION-DOMAIN", "only the Catalase assay methodology fixture is authorized")
    if fixture.get("source_digest") != repository.runtime["source_digest"]:
        raise KernelError("E-GENERALIZATION-SOURCE", "generalization source digest differs from canonical runtime")

    validate_boundaries(fixture)
    source_pool = validate_source_pool(fixture, repository)
    workspace_fixture = require_mapping(
        fixture.get("workspace_fixture"),
        "E-GENERALIZATION-FIXTURE",
        "generalization fixture requires an embedded accepted workspace fixture",
    )
    if workspace_fixture.get("contract") != FIXTURE_CONTRACT:
        raise KernelError("E-GENERALIZATION-CONTRACT-REUSE", "accepted workspace fixture contract changed")
    workspace = require_mapping(
        workspace_fixture.get("workspace"),
        "E-GENERALIZATION-FIXTURE",
        "embedded workspace fixture requires a workspace",
    )
    selected = validate_catalase_selection(workspace)
    research_fixture = require_mapping(fixture.get("research_fixture"), "E-GENERALIZATION-UPSTREAM", "research fixture is required")
    research_baseline = require_mapping(fixture.get("research_baseline"), "E-GENERALIZATION-UPSTREAM", "research baseline is required")
    structured_baseline = require_mapping(fixture.get("structured_baseline"), "E-GENERALIZATION-UPSTREAM", "structured baseline is required")
    bridge_fixture = require_mapping(fixture.get("bridge_fixture"), "E-GENERALIZATION-UPSTREAM", "bridge fixture is required")
    validate_scope_candidate(workspace, research_fixture)
    unavailable_target = validate_unavailable_warning(workspace, bridge_fixture, repository)

    core_report, export, manifest = validate_workspace_fixture_bundle(
        workspace_fixture,
        repository,
        research_fixture,
        research_baseline,
        structured_baseline,
        bridge_fixture,
    )
    if export.get("contract") != EXPORT_CONTRACT or manifest.get("contract") != MANIFEST_CONTRACT:
        raise KernelError("E-GENERALIZATION-CONTRACT-REUSE", "accepted export or manifest contract changed")
    recommendation = fixture.get("recommendation")
    if recommendation not in ALLOWED_RECOMMENDATIONS:
        raise KernelError("E-GENERALIZATION-RECOMMENDATION", "generalization recommendation is not allowed")

    validation = seal({
        "contract": GENERALIZATION_VALIDATION_CONTRACT,
        "phase": 4,
        "workstream": 4,
        "slice": 1,
        "fixture_id": fixture.get("id"),
        "domain": fixture.get("domain"),
        "source_pool_count": len(source_pool),
        "selected_entry_count": len(selected),
        "candidate_count": len(workspace.get("candidate_references", [])),
        "unavailable_target": unavailable_target,
        "accepted_contracts_reused": list(REUSED_CONTRACTS),
        "accepted_contracts_modified": False,
        "decision": "valid",
        "repository_mutation": False,
        "live": False,
    })
    return validation, core_report, export, manifest, dict(workspace)
