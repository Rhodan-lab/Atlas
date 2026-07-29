"""Construct a Catalase workspace bundle using accepted Workstream 3 contracts."""
from __future__ import annotations

import re
from typing import Any, Mapping

from tools.phase4_workspace.contracts import (
    DECISION_CONTRACT,
    ENTRY_CONTRACT,
    FIXTURE_CONTRACT,
    WORKSPACE_CONTRACT,
)

from .constants import MODE, SOURCE_DIGEST, STRUCTURED_BASELINE_SHA256, exact_key, seal


def _candidate_records(spec: Mapping[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    contradictions: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    for raw in spec["candidate_definitions"]:
        common = {
            "advisory_only": True,
            "assessment": raw["assessment"],
            "evidence_paths": [
                {"id": "src:aebi-1984-catalase-in-vitro", "revision": 1},
                {"id": "src:wu-lin-wolfbeis-2003-catalase-assay", "revision": 1},
            ],
            "exact_revision_required": True,
            "id": raw["id"],
            "left": dict(raw["left"]),
            "live": False,
            "rationale": raw["rationale"],
            "repository_mutation": False,
            "right": dict(raw["right"]),
        }
        if raw["kind"] == "contradiction":
            contradictions.append({
                **common,
                "contract": "atlas-contradiction-candidate/0.1",
                "automatic_resolution": False,
                "compared_statements": list(raw["compared_statements"]),
                "scope_analysis": list(raw["scope_analysis"]),
            })
        else:
            duplicates.append({
                **common,
                "contract": "atlas-duplicate-candidate/0.1",
                "automatic_merge": False,
                "similarity_basis": list(raw["similarity_basis"]),
                "semantic_differences": list(raw["semantic_differences"]),
            })
    return contradictions, duplicates


def build_bundle(
    spec: Mapping[str, Any],
    selected: list[dict[str, Any]],
    selection: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    trail_entries: list[dict[str, Any]] = []
    workspace_entries: list[dict[str, Any]] = []
    summaries: list[str] = []
    for position, item in enumerate(selected, start=1):
        ref = dict(item["exact_reference"])
        slug = re.sub(r"[^a-z0-9]+", "-", str(ref["id"]).lower()).strip("-")
        trail_entries.append({
            "action": item["action"],
            "id": ref["id"],
            "original_rank": item["rank"],
            "rationale": item["rationale"],
            "revision": ref["revision"],
        })
        workspace_entries.append({
            "contract": ENTRY_CONTRACT,
            "decision": {
                "action": item["action"],
                "advisory_only": True,
                "canonical_mutation": False,
                "contract": DECISION_CONTRACT,
                "id": f"workspace-decision:en:catalase-{item['action']}-{position}",
                "rationale": item["rationale"],
            },
            "exact_reference": ref,
            "id": f"workspace-entry:en:catalase-{slug}-{position}",
            "original_rank": item["rank"],
            "position": position,
        })
        summaries.append(item["summary"])

    filter_record = {
        "advisory_only": True,
        "contract": "atlas-retrieval-filter/0.1",
        "criteria": {
            "domains": ["catalase"],
            "entity_types": ["claim", "concept", "evidence", "model", "question", "source", "synthesis"],
        },
        "exact_revision_required": True,
        "expected_keys": sorted(exact_key(item) for item in spec["eligible_exact_references"]),
        "id": "filter:en:catalase-assay-methodology",
        "live": False,
        "preserve_input_order": True,
        "repository_mutation": False,
        "revision": 1,
    }
    trail = {
        "authority": "research-only",
        "automatic_status_change": False,
        "canonical_copy": False,
        "contract": "atlas-research-trail/0.1",
        "entries": trail_entries,
        "exact_revision_required": True,
        "filter": {"id": filter_record["id"], "revision": 1},
        "id": "trail:en:catalase-assay-methodology-generalization",
        "live": False,
        "open_questions": list(spec["open_questions"]),
        "query_snapshot": {"id": spec["query"]["id"], "text": spec["query"]["text"]},
        "ranking_reference": {
            "baseline_contract": "atlas-phase3-structured-baseline/0.1",
            "index_build_digest": selection["index_build_digest"],
            "index_contract": selection["index_contract"],
            "result_set_sha256": selection["report_digest"],
        },
        "repository_mutation": False,
        "revision": 1,
    }
    contradictions, duplicates = _candidate_records(spec)
    research_fixture = {
        "advisory_only": True,
        "automatic_merge_or_resolution": False,
        "canonical_copy_authority": False,
        "contract": "atlas-phase3-research-foundation-fixtures/0.1",
        "contradiction_candidates": contradictions,
        "duplicate_candidates": duplicates,
        "entity_count": 34,
        "filters": [filter_record],
        "id": "research-foundations:phase4-catalase-generalization-en-v1",
        "live": False,
        "mode": "retrieval-evaluation",
        "query_set": {"id": "retrieval-query-set:phase4-catalase-generalization-en-v1", "version": 1},
        "repository_mutation": False,
        "source_digest": SOURCE_DIGEST,
        "structured_baseline_sha256": STRUCTURED_BASELINE_SHA256,
        "trails": [trail],
        "version": 1,
    }
    research_baseline = seal({
        "advisory_only": True,
        "automatic_merge_or_resolution": False,
        "canonical_copy_authority": False,
        "contract": "atlas-phase3-research-foundation-baseline/0.1",
        "decision": "research-foundation-candidate",
        "fixture_id": research_fixture["id"],
        "fixture_version": 1,
        "live": False,
        "mode": "retrieval-evaluation",
        "repository_mutation": False,
        "source_digest": SOURCE_DIGEST,
        "structured_baseline_sha256": STRUCTURED_BASELINE_SHA256,
        "validated_candidates": {
            "contradiction": {"assessment": contradictions[0]["assessment"], "id": contradictions[0]["id"]},
            "duplicate": {"assessment": duplicates[0]["assessment"], "id": duplicates[0]["id"]},
        },
        "validated_trail": {"authority": "research-only", "entry_count": 5, "id": trail["id"], "revision": 1},
    })

    p = spec["principia_reference"]
    w = spec["warning"]
    bridge_fixture = {
        "failure_states": [],
        "impact_warnings": [{
            "automatic_release_action": False,
            "automatic_status_change": False,
            "automatic_update": False,
            "available_revisions": list(w["available_revisions"]),
            "canonical_mutation": False,
            "contract": "atlas-cross-repository-impact-warning/0.1",
            "id": w["id"],
            "impact_state": "unavailable",
            "implicit_latest": False,
            "live": False,
            "message": w["message"],
            "recovery_actions": ["show-available-revisions", "return-to-pinned-reference", "open-impact-details"],
            "repository_mutation": False,
            "revision": w["revision"],
            "severity": "blocking",
            "target": dict(w["target"]),
        }],
        "principia_references": [{
            "atlas_references": [dict(item) for item in p["atlas_references"]],
            "automatic_release_action": False,
            "automatic_status_change": False,
            "automatic_status_inheritance": False,
            "canonical_mutation": False,
            "contract": "atlas-principia-reference-envelope/0.1",
            "fixture_only": True,
            "id": p["id"],
            "impact_state": "fixture-only",
            "implicit_latest": False,
            "live": False,
            "principia_artifact_id": p["principia_artifact_id"],
            "principia_artifact_revision": p["principia_artifact_revision"],
            "principia_status": p["principia_status"],
            "principia_status_separate": True,
            "reference_purpose": p["reference_purpose"],
            "repository_mutation": False,
            "revision": p["revision"],
        }],
    }

    workspace = {
        "authority": {
            "account_required": False,
            "automatic_merge_or_resolution": False,
            "canonical_copy_authority": False,
            "canonical_mutation": False,
            "cloud_required": False,
            "deterministic_export_required": True,
            "exact_revision_required": True,
            "external_network_required": False,
            "lifecycle_mutation": False,
            "live_principia_dependency": False,
            "local_first": True,
            "non_graph_workflow_required": True,
            "principia_status_separate": True,
            "production_frontend_architecture_selected": False,
            "repository_mutation": False,
            "review_mutation": False,
            "workspace_authority": "ephemeral-research-only",
        },
        "candidate_references": [{
            "advisory_only": True,
            "assessment": item["assessment"],
            "automatic_resolution": False,
            "id": item["id"],
            "kind": item["kind"],
            "resolution": "unresolved",
        } for item in spec["candidate_definitions"]],
        "contract": WORKSPACE_CONTRACT,
        "entries": workspace_entries,
        "filter_reference": {"id": filter_record["id"], "revision": 1},
        "id": "workspace:en:catalase-assay-methodology-review",
        "mode": MODE,
        "non_graph_summary": summaries,
        "open_questions": list(spec["open_questions"]),
        "principia_references": [{
            "automatic_status_inheritance": False,
            "fixture_only": True,
            "id": p["id"],
            "implicit_latest": False,
            "live": False,
            "principia_status": p["principia_status"],
            "principia_status_separate": True,
            "revision": p["revision"],
        }],
        "query_snapshot": {"id": spec["query"]["id"], "text": spec["query"]["text"]},
        "ranking_reference": dict(trail["ranking_reference"]),
        "revision": 1,
        "source_digest": SOURCE_DIGEST,
        "trail_reference": {"id": trail["id"], "revision": 1},
        "warning_references": [{"id": w["id"], "revision": w["revision"]}],
    }
    negative_cases = [
        {"expected_error": "E-WORKSPACE-LATEST", "id": "negative:workspace-implicit-latest", "mutation": "implicit-latest"},
        {"expected_error": "E-WORKSPACE-DUPLICATE-ENTRY", "id": "negative:workspace-duplicate-entry-id", "mutation": "duplicate-entry-id"},
        {"expected_error": "E-WORKSPACE-COPIED-AUTHORITY", "id": "negative:workspace-copied-authority", "mutation": "copied-authority"},
        {"expected_error": "E-WORKSPACE-CANDIDATE-AUTHORITY", "id": "negative:workspace-resolved-candidate", "mutation": "resolve-candidate"},
        {"expected_error": "E-WORKSPACE-UNAVAILABLE-REVISION", "id": "negative:workspace-unavailable-revision", "mutation": "unavailable-revision"},
        {"expected_error": "E-WORKSPACE-LIFECYCLE-MUTATION", "id": "negative:workspace-lifecycle-mutation", "mutation": "lifecycle-mutation"},
        {"expected_error": "E-WORKSPACE-PRINCIPIA-STATUS", "id": "negative:workspace-live-principia", "mutation": "live-principia"},
        {"expected_error": "E-WORKSPACE-DETERMINISM", "id": "negative:workspace-nondeterministic-timestamp", "mutation": "nondeterministic-timestamp"},
        {"expected_error": "E-WORKSPACE-NETWORK", "id": "negative:workspace-external-network", "mutation": "external-network"},
        {"expected_error": "E-WORKSPACE-NON-GRAPH", "id": "negative:workspace-missing-non-graph", "mutation": "missing-non-graph"},
    ]
    fixture = {
        "contract": FIXTURE_CONTRACT,
        "id": "workspace-fixtures:phase4-catalase-generalization-en-v1",
        "mode": MODE,
        "negative_cases": negative_cases,
        "source_digest": SOURCE_DIGEST,
        "version": 1,
        "workspace": workspace,
    }
    return fixture, research_fixture, research_baseline, bridge_fixture
