"""Run, validate, and serialize Workstream 4 generalization evidence."""
from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository, compile_canonical, render_json
from tools.phase4_workspace.contracts import (
    ENTRY_CONTRACT,
    MANIFEST_CONTRACT,
    REPORT_CONTRACT,
    WORKSPACE_CONTRACT,
    validate_fixture_bundle,
    validate_workspace,
)

from .bundle import build_bundle
from .constants import (
    ELIGIBLE_IDS,
    EVALUATION_CONTRACT,
    RECOMMENDATION,
    VALIDATION_CONTRACT,
    json_sha256,
    require,
    seal,
    sha256_bytes,
)
from .selection import build_selection
from .spec import validate_spec


def _expect_workspace_error(
    workspace: Mapping[str, Any],
    expected: str | set[str],
    repository: KernelRepository,
    research_fixture: Mapping[str, Any],
    research_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    bridge_fixture: Mapping[str, Any],
) -> str:
    try:
        validate_workspace(workspace, repository, research_fixture, research_baseline, structured_baseline, bridge_fixture)
    except KernelError as exc:
        allowed = {expected} if isinstance(expected, str) else expected
        if exc.code not in allowed:
            raise KernelError("E-W4-NEGATIVE", f"expected {sorted(allowed)}, observed {exc.code}") from exc
        return exc.code
    raise KernelError("E-W4-NEGATIVE", "negative mutation was accepted")


def _extra_negatives(
    spec: Mapping[str, Any],
    workspace: Mapping[str, Any],
    repository: KernelRepository,
    research_fixture: Mapping[str, Any],
    research_baseline: Mapping[str, Any],
    structured_baseline: Mapping[str, Any],
    bridge_fixture: Mapping[str, Any],
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []

    def record(case_id: str, observed: str) -> None:
        results.append({
            "id": case_id,
            "observed_error": observed,
            "preserved_previous_valid_workspace": True,
            "decision": "rejected-as-required",
        })

    mutations = [
        ("negative:workstream4-non-catalase-entry", "E-W4-DOMAIN", lambda s: s["selected_entries"][0].update(
            {"exact_reference": {"id": "claim:en:recommender-effects-are-context-dependent", "revision": 1}}
        )),
        ("negative:workstream4-duplicate-selection", "E-W4-SELECTION", lambda s: s["selected_entries"][1].update(
            {"exact_reference": dict(s["selected_entries"][0]["exact_reference"])}
        )),
        ("negative:workstream4-browser-implementation", "E-W4-AUTHORITY", lambda s: s["authority"].update(
            {"browser_implementation_authorized": True}
        )),
        ("negative:workstream4-canonical-authoring", "E-W4-AUTHORITY", lambda s: s["authority"].update(
            {"new_canonical_authoring_authorized": True}
        )),
    ]
    for case_id, expected, mutate in mutations:
        candidate = copy.deepcopy(spec)
        mutate(candidate)
        try:
            validate_spec(candidate, repository)
        except KernelError as exc:
            require(exc.code == expected, "E-W4-NEGATIVE", f"{case_id} observed {exc.code}")
            record(case_id, exc.code)
        else:
            raise KernelError("E-W4-NEGATIVE", f"{case_id} was accepted")

    workspace_mutations: list[tuple[str, str | set[str], Any]] = [
        ("negative:workstream4-reordered-trail", {"E-WORKSPACE-ORDER", "E-WORKSPACE-UPSTREAM"}, lambda w: w["entries"].__setitem__(slice(0, 2), [w["entries"][1], w["entries"][0]])),
        ("negative:workstream4-modified-contract", "E-WORKSPACE-CONTRACT", lambda w: w.update({"contract": "atlas-research-workspace/0.2"})),
        ("negative:workstream4-inherited-principia-status", "E-WORKSPACE-PRINCIPIA-STATUS", lambda w: w["principia_references"][0].update({"automatic_status_inheritance": True})),
        ("negative:workstream4-account-required", "E-WORKSPACE-NETWORK", lambda w: w["authority"].update({"account_required": True})),
        ("negative:workstream4-cloud-required", "E-WORKSPACE-NETWORK", lambda w: w["authority"].update({"cloud_required": True})),
        ("negative:workstream4-production-architecture", "E-WORKSPACE-AUTHORITY", lambda w: w["authority"].update({"production_frontend_architecture_selected": True})),
        ("negative:workstream4-credential", "E-WORKSPACE-DETERMINISM", lambda w: w.update({"credential": "forbidden"})),
    ]
    for case_id, expected, mutate in workspace_mutations:
        candidate = copy.deepcopy(workspace)
        mutate(candidate)
        observed = _expect_workspace_error(
            candidate, expected, repository, research_fixture, research_baseline, structured_baseline, bridge_fixture
        )
        record(case_id, observed)
    return results


def run_generalization(
    spec: Mapping[str, Any],
    canonical_root: Path,
    structured_baseline: Mapping[str, Any],
) -> dict[str, Any]:
    repository = KernelRepository(compile_canonical(canonical_root))
    spec_validation = validate_spec(spec, repository)
    selection, selected = build_selection(spec, canonical_root, repository, structured_baseline)
    fixture, research_fixture, research_baseline, bridge_fixture = build_bundle(spec, selected, selection)
    workspace_report, export, manifest = validate_fixture_bundle(
        fixture, repository, research_fixture, research_baseline, structured_baseline, bridge_fixture
    )
    negatives = [
        *workspace_report["negative_validations"],
        *_extra_negatives(
            spec,
            fixture["workspace"],
            repository,
            research_fixture,
            research_baseline,
            structured_baseline,
            bridge_fixture,
        ),
    ]
    gates = {
        "one_fixture_authorized": spec.get("fixture_count_authorized") == 1,
        "eligible_exact_revisions_available": spec_validation["eligible_count"] == 8,
        "five_catalase_entries_selected": len(fixture["workspace"]["entries"]) == 5 and all(
            item["exact_reference"]["id"] in ELIGIBLE_IDS for item in fixture["workspace"]["entries"]
        ),
        "accepted_workspace_contracts_reused": (
            fixture["workspace"]["contract"] == WORKSPACE_CONTRACT
            and all(item["contract"] == ENTRY_CONTRACT for item in fixture["workspace"]["entries"])
            and export["contract"] == "atlas-research-workspace-export/0.1"
            and manifest["contract"] == MANIFEST_CONTRACT
            and workspace_report["contract"] == REPORT_CONTRACT
        ),
        "methodological_scope_preserved": "universal" in spec["query"]["text"].lower(),
        "candidates_unresolved_and_advisory": all(
            item["resolution"] == "unresolved" and item["advisory_only"] is True
            for item in export["candidate_references"]
        ),
        "principia_status_separate_and_non_live": (
            export["principia_references"][0]["principia_status_separate"] is True
            and export["principia_references"][0]["live"] is False
        ),
        "unavailable_revision_warning_explicit": (
            export["warning_references"][0]["impact_state"] == "unavailable"
            and export["warning_references"][0]["implicit_latest"] is False
        ),
        "non_graph_summary_complete": len(export["non_graph_summary"]) >= len(export["entries"]),
        "structured_selection_bound_to_accepted_index": selection["index_build_digest"] == structured_baseline["index_build_digest"],
        "deterministic_export_and_manifest": workspace_report["deterministic_export"] is True and manifest["deterministic_export"] is True,
        "negative_authority_and_failure_cases_rejected": len(negatives) == 21 and all(
            item["decision"] == "rejected-as-required" for item in negatives
        ),
        "all_mutation_and_production_boundaries_frozen": (
            workspace_report["canonical_mutation"] is False
            and workspace_report["lifecycle_mutation"] is False
            and workspace_report["review_mutation"] is False
            and workspace_report["repository_mutation"] is False
            and workspace_report["production_frontend_architecture_selected"] is False
            and workspace_report["live_principia_dependency"] is False
            and spec["authority"]["browser_implementation_authorized"] is False
        ),
    }
    failed = sorted(name for name, passed in gates.items() if not passed)
    if failed:
        raise KernelError("E-W4-EXIT-GATE", f"Workstream 4 gates failed: {failed}")

    report = seal({
        "contract": EVALUATION_CONTRACT,
        "mode": "interactive-experience-foundation",
        "phase": 4,
        "workstream": 4,
        "slice": 1,
        "state": "generalization-candidate",
        "decision": RECOMMENDATION,
        "implementation_authorized": False,
        "separate_governance_required": True,
        "spec": {"contract": spec["contract"], "id": spec["id"], "version": spec["version"], "sha256": json_sha256(spec)},
        "structured_selection": {
            "contract": selection["contract"],
            "index_build_digest": selection["index_build_digest"],
            "report_digest": selection["report_digest"],
            "selected_count": len(selection["selected"]),
        },
        "workspace_fixture": {"contract": fixture["contract"], "id": fixture["id"], "sha256": json_sha256(fixture)},
        "workspace_contract_report": {
            "contract": workspace_report["contract"],
            "report_digest": workspace_report["report_digest"],
            "negative_case_count": len(workspace_report["negative_validations"]),
        },
        "workspace_export": {"contract": export["contract"], "report_digest": export["report_digest"]},
        "workspace_manifest": {"contract": manifest["contract"], "report_digest": manifest["report_digest"]},
        "counts": {
            "eligible_exact_revisions": 8,
            "entries": workspace_report["counts"]["entries"],
            "candidates": workspace_report["counts"]["candidates"],
            "principia_references": workspace_report["counts"]["principia_references"],
            "warnings": workspace_report["counts"]["warnings"],
            "open_questions": workspace_report["counts"]["open_questions"],
            "negative_cases": len(negatives),
            "exit_gates": len(gates),
        },
        "decision_counts": dict(workspace_report["decision_counts"]),
        "negative_validations": negatives,
        "exit_gates": gates,
        "replaceability": {
            "workspace_contracts_unchanged": True,
            "generated_artifacts_disposable": True,
            "accepted_workstream3_preserved_as_previous_valid_state": True,
            "rollback": "delete generated Workstream 4 artifacts and continue using the accepted Workstream 3 fixture",
        },
        "authority": {
            "workspace_authority": "ephemeral-research-only",
            "browser_implementation_authorized": False,
            "production_implementation_authorized": False,
            "canonical_copy_authority": False,
            "canonical_mutation": False,
            "lifecycle_mutation": False,
            "review_mutation": False,
            "automatic_merge_or_resolution": False,
            "account_required": False,
            "cloud_required": False,
            "external_network_required": False,
            "production_frontend_architecture_selected": False,
            "live_principia_dependency": False,
            "live": False,
            "repository_mutation": False,
        },
        "limitations": [
            "This is one Catalase fixture, not a production workspace-generalization claim.",
            "The structured selection is bounded to the accepted 34-entity corpus.",
            "The Principia envelope is fixture-only and does not assert a published matching artifact.",
            "No browser reuse, human usability, assistive-technology review, or accessibility certification is claimed.",
        ],
    })
    validation = validate_evaluation_report(report)
    return {
        "spec_validation": spec_validation,
        "selection": selection,
        "fixture": fixture,
        "research_fixture": research_fixture,
        "research_baseline": research_baseline,
        "bridge_fixture": bridge_fixture,
        "workspace_report": workspace_report,
        "export": export,
        "manifest": manifest,
        "evaluation_report": report,
        "evaluation_validation": validation,
    }


def validate_evaluation_report(report: Mapping[str, Any]) -> dict[str, Any]:
    require(report.get("contract") == EVALUATION_CONTRACT, "E-W4-REPORT", f"expected {EVALUATION_CONTRACT!r}")
    require(report.get("phase") == 4 and report.get("workstream") == 4 and report.get("slice") == 1, "E-W4-REPORT", "scope mismatch")
    require(report.get("state") == "generalization-candidate", "E-W4-REPORT", "unexpected state")
    require(report.get("decision") == RECOMMENDATION, "E-W4-DECISION", "unexpected recommendation")
    require(
        report.get("implementation_authorized") is False and report.get("separate_governance_required") is True,
        "E-W4-DECISION",
        "recommendation may not authorize itself",
    )
    gates = report.get("exit_gates")
    require(isinstance(gates, Mapping) and len(gates) == 13 and all(value is True for value in gates.values()), "E-W4-GATES", "all gates must pass")
    counts = report.get("counts")
    require(isinstance(counts, Mapping) and counts.get("entries") == 5 and counts.get("candidates") == 2 and counts.get("negative_cases") == 21, "E-W4-COUNTS", "bounded counts mismatch")
    authority = report.get("authority")
    require(isinstance(authority, Mapping), "E-W4-AUTHORITY", "report authority is required")
    for field, expected in {
        "browser_implementation_authorized": False,
        "production_implementation_authorized": False,
        "canonical_copy_authority": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "automatic_merge_or_resolution": False,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "live": False,
        "repository_mutation": False,
    }.items():
        require(authority.get(field) == expected, "E-W4-AUTHORITY", f"report requires {field}={expected!r}")
    digest = report.get("report_digest")
    require(isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None, "E-W4-DIGEST", "digest must be SHA-256")
    unsigned = dict(report)
    unsigned.pop("report_digest", None)
    require(json_sha256(unsigned) == digest, "E-W4-DIGEST", "report digest mismatch")
    return {
        "contract": VALIDATION_CONTRACT,
        "decision": "valid-workstream4-generalization-candidate",
        "recommendation": report["decision"],
        "exit_gate_count": len(gates),
        "entry_count": counts["entries"],
        "negative_case_count": counts["negative_cases"],
        "report_digest": digest,
        "implementation_authorized": False,
        "live": False,
        "repository_mutation": False,
    }


def write_outputs(result: Mapping[str, Any], output_dir: Path) -> dict[str, dict[str, Any]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {
        "structured-selection.json": result["selection"],
        "catalase-workspace-fixture.json": result["fixture"],
        "catalase-research-fixture.json": result["research_fixture"],
        "catalase-research-baseline.json": result["research_baseline"],
        "catalase-bridge-fixture.json": result["bridge_fixture"],
        "catalase-workspace-report.json": result["workspace_report"],
        "catalase-workspace-export.json": result["export"],
        "catalase-workspace-manifest.json": result["manifest"],
        "workstream4-generalization-report.json": result["evaluation_report"],
        "workstream4-generalization-validation.json": result["evaluation_validation"],
    }
    identities: dict[str, dict[str, Any]] = {}
    for name, record in files.items():
        payload = render_json(record).encode("utf-8")
        (output_dir / name).write_bytes(payload)
        identities[name] = {
            "bytes": len(payload),
            "sha256": sha256_bytes(payload),
            "contract": record.get("contract"),
            "report_digest": record.get("report_digest"),
        }
    return identities
