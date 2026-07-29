"""Build the single authorized Catalase workspace-generalization fixture."""
from __future__ import annotations

from typing import Any

from tools.phase4_workspace.contracts import (
    DECISION_CONTRACT,
    ENTRY_CONTRACT,
    FIXTURE_CONTRACT,
    MODE,
    WORKSPACE_CONTRACT,
)
from tools.phase4_workspace_generalization.constants import GENERALIZATION_FIXTURE_CONTRACT

SOURCE_DIGEST = "684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1"
INDEX_BUILD_DIGEST = "9eef481bf8a1da91f63fe2299cee7468c70cfb0f1ee4a3c6794343cb1e92ec31"
RESULT_SET_SHA256 = "6a02648cd28d7d1ad1878682723de7c0756ad3bd7dad30f7edd5e97f34709447"
STRUCTURED_BASELINE_SHA256 = "09f0962d042e41037057d9003135e875b8110b15843a607d1b76c8943ff70eb8"

QUERY = {
    "id": "query:retrieval:catalase-assay-comparability",
    "text": "Under what assay conditions may catalase activity be compared without treating one reported optimum as universal?",
}
FILTER = {"id": "filter:en:catalase-assay-comparability", "revision": 1}
RANKING = {
    "baseline_contract": "atlas-phase3-structured-baseline/0.1",
    "index_build_digest": INDEX_BUILD_DIGEST,
    "index_contract": "atlas-structured-index/0.1",
    "result_set_sha256": RESULT_SET_SHA256,
}
OPEN_QUESTIONS = [
    "Which assay variables must be held equivalent before two reported catalase activities can support a quantitative comparison?",
    "How should matrix effects and detection-method differences be represented when only partial methodological detail is available?",
]

ENTRY_SPECS = [
    (
        "claim:en:catalase-optimum-requires-assay-scope",
        "catalase-assay-scope-claim",
        "include",
        1,
        "Establishes the load-bearing rule that an optimum is meaningful only within its assay scope.",
        "Include the assay-scope claim because it prevents a reported optimum from being treated as universal.",
    ),
    (
        "synthesis:en:catalase-assay-conditions",
        "catalase-assay-synthesis",
        "include",
        2,
        "Integrates method, pH, substrate, temperature, matrix, and detection constraints into one comparison frame.",
        "Include the synthesis because it combines the methodological conditions that govern valid comparison.",
    ),
    (
        "evidence:en:fluorescent-catalase-assay-neutral-ph",
        "fluorescent-neutral-ph-evidence",
        "context",
        3,
        "Provides a method-specific neutral-pH observation without converting that observation into a universal optimum.",
        "Use the fluorescent neutral-pH evidence as method-specific context rather than a universal benchmark.",
    ),
    (
        "model:en:catalase-assay-observation",
        "catalase-assay-observation-model",
        "context",
        4,
        "Makes explicit that reported activity is an observation produced by enzyme, matrix, substrate, temperature, pH, and detection choices.",
        "Use the observation model to expose how assay choices jointly shape the reported activity.",
    ),
    (
        "concept:en:catalase",
        "catalase-concept-background",
        "exclude",
        8,
        "The broad enzyme concept is useful background but does not by itself determine whether two assay results are comparable.",
        "Exclude the broad Catalase concept from the comparison trail because it does not establish assay equivalence.",
    ),
]

CORE_NEGATIVES = [
    ("implicit-latest", "E-WORKSPACE-LATEST"),
    ("duplicate-entry-id", "E-WORKSPACE-DUPLICATE-ENTRY"),
    ("copied-authority", "E-WORKSPACE-COPIED-AUTHORITY"),
    ("resolve-candidate", "E-WORKSPACE-CANDIDATE-AUTHORITY"),
    ("unavailable-revision", "E-WORKSPACE-UNAVAILABLE-REVISION"),
    ("lifecycle-mutation", "E-WORKSPACE-LIFECYCLE-MUTATION"),
    ("live-principia", "E-WORKSPACE-PRINCIPIA-STATUS"),
    ("nondeterministic-timestamp", "E-WORKSPACE-DETERMINISM"),
    ("external-network", "E-WORKSPACE-NETWORK"),
    ("missing-non-graph", "E-WORKSPACE-NON-GRAPH"),
]

GENERALIZATION_NEGATIVES = [
    ("non-catalase-entry", "E-GENERALIZATION-DOMAIN"),
    ("reordered-accepted-trail", "E-GENERALIZATION-ORDER"),
    ("modified-workspace-contract", "E-WORKSPACE-CONTRACT"),
    ("account-required", "E-WORKSPACE-NETWORK"),
    ("cloud-required", "E-WORKSPACE-NETWORK"),
    ("canonical-mutation", "E-WORKSPACE-LIFECYCLE-MUTATION"),
    ("review-mutation", "E-WORKSPACE-LIFECYCLE-MUTATION"),
    ("repository-mutation", "E-WORKSPACE-LIFECYCLE-MUTATION"),
    ("browser-implementation", "E-GENERALIZATION-BOUNDARY"),
    ("production-implementation", "E-GENERALIZATION-BOUNDARY"),
    ("release-mutation", "E-GENERALIZATION-AUTHORITY"),
    ("second-active-fixture", "E-GENERALIZATION-FIXTURE-COUNT"),
    ("production-architecture-selection", "E-WORKSPACE-AUTHORITY"),
    ("credential-required", "E-WORKSPACE-DETERMINISM"),
]


def _entry(position: int, spec: tuple[str, str, str, int, str, str]) -> dict[str, Any]:
    entity_id, slug, action, original_rank, rationale, _ = spec
    return {
        "contract": ENTRY_CONTRACT,
        "decision": {
            "action": action,
            "advisory_only": True,
            "canonical_mutation": False,
            "contract": DECISION_CONTRACT,
            "id": f"workspace-decision:en:{action}-{slug}",
            "rationale": rationale,
        },
        "exact_reference": {"id": entity_id, "revision": 1},
        "id": f"workspace-entry:en:{slug}",
        "original_rank": original_rank,
        "position": position,
    }


def _trail_entry(spec: tuple[str, str, str, int, str, str]) -> dict[str, Any]:
    entity_id, _, action, original_rank, rationale, _ = spec
    return {
        "action": action,
        "id": entity_id,
        "original_rank": original_rank,
        "rationale": rationale,
        "revision": 1,
    }


def _authority() -> dict[str, Any]:
    return {
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
    }


def _candidates() -> list[dict[str, Any]]:
    return [
        {
            "advisory_only": True,
            "assessment": "scope-difference-likely",
            "automatic_resolution": False,
            "id": "candidate:contradiction:catalase-assay-optima",
            "kind": "contradiction",
            "resolution": "unresolved",
        },
        {
            "advisory_only": True,
            "assessment": "related-not-duplicate",
            "automatic_resolution": False,
            "id": "candidate:duplicate:catalase-claim-synthesis",
            "kind": "duplicate",
            "resolution": "unresolved",
        },
    ]


def _workspace() -> dict[str, Any]:
    return {
        "authority": _authority(),
        "candidate_references": _candidates(),
        "contract": WORKSPACE_CONTRACT,
        "entries": [_entry(index, spec) for index, spec in enumerate(ENTRY_SPECS, start=1)],
        "filter_reference": dict(FILTER),
        "id": "workspace:en:catalase-assay-comparability",
        "mode": MODE,
        "non_graph_summary": [spec[5] for spec in ENTRY_SPECS],
        "open_questions": list(OPEN_QUESTIONS),
        "principia_references": [{
            "automatic_status_inheritance": False,
            "fixture_only": True,
            "id": "principia-reference:catalase:assay-comparability",
            "implicit_latest": False,
            "live": False,
            "principia_status": "draft",
            "principia_status_separate": True,
            "revision": 1,
        }],
        "query_snapshot": dict(QUERY),
        "ranking_reference": dict(RANKING),
        "revision": 1,
        "source_digest": SOURCE_DIGEST,
        "trail_reference": {"id": "trail:en:catalase-assay-comparability", "revision": 1},
        "warning_references": [{
            "id": "impact-warning:catalase:claim-revision-two-unavailable",
            "revision": 1,
        }],
    }


def _research_fixture() -> dict[str, Any]:
    return {
        "contradiction_candidates": [{
            "advisory_only": True,
            "assessment": "scope-difference-likely",
            "automatic_resolution": False,
            "id": "candidate:contradiction:catalase-assay-optima",
            "left": {"id": "src:aebi-1984-catalase-in-vitro", "revision": 1},
            "resolution": "unresolved",
            "right": {"id": "src:wu-lin-wolfbeis-2003-catalase-assay", "revision": 1},
        }],
        "duplicate_candidates": [{
            "advisory_only": True,
            "assessment": "related-not-duplicate",
            "automatic_resolution": False,
            "id": "candidate:duplicate:catalase-claim-synthesis",
            "left": {"id": "claim:en:catalase-optimum-requires-assay-scope", "revision": 1},
            "resolution": "unresolved",
            "right": {"id": "synthesis:en:catalase-assay-conditions", "revision": 1},
        }],
        "filters": [{
            **FILTER,
            "language": "en",
            "types": ["claim", "synthesis", "evidence", "model", "concept", "source"],
        }],
        "id": "research-fixture:phase4-catalase-generalization-v1",
        "source_digest": SOURCE_DIGEST,
        "structured_baseline_sha256": STRUCTURED_BASELINE_SHA256,
        "trails": [{
            "entries": [_trail_entry(spec) for spec in ENTRY_SPECS],
            "filter": dict(FILTER),
            "id": "trail:en:catalase-assay-comparability",
            "open_questions": list(OPEN_QUESTIONS),
            "query_snapshot": dict(QUERY),
            "ranking_reference": dict(RANKING),
            "revision": 1,
        }],
        "version": 1,
    }


def _bridge_fixture() -> dict[str, Any]:
    return {
        "impact_warnings": [{
            "automatic_update": False,
            "contract": "atlas-reference-impact-warning/0.1",
            "id": "impact-warning:catalase:claim-revision-two-unavailable",
            "impact_state": "unavailable-exact-revision",
            "implicit_latest": False,
            "message": "Revision 2 is unavailable. Preserve the warning and do not substitute revision 1 or implicit latest.",
            "revision": 1,
            "severity": "warning",
            "target": {"id": "claim:en:catalase-optimum-requires-assay-scope", "revision": 2},
        }],
        "principia_references": [{
            "atlas_references": [
                {"id": "claim:en:catalase-optimum-requires-assay-scope", "revision": 1},
                {"id": "model:en:catalase-assay-observation", "revision": 1},
                {"id": "synthesis:en:catalase-assay-conditions", "revision": 1},
            ],
            "automatic_status_inheritance": False,
            "contract": "atlas-principia-reference-envelope/0.1",
            "fixture_only": True,
            "id": "principia-reference:catalase:assay-comparability",
            "live": False,
            "principia_artifact_id": "principia:dossier:catalase-assay-comparability",
            "principia_artifact_revision": 1,
            "principia_status": "draft",
            "principia_status_separate": True,
            "revision": 1,
        }],
    }


def build_fixture() -> dict[str, Any]:
    """Return a fresh deterministic fixture record."""
    source_pool = [
        "question:en:how-assay-conditions-affect-catalase",
        "concept:en:catalase",
        "model:en:catalase-assay-observation",
        "evidence:en:fluorescent-catalase-assay-neutral-ph",
        "claim:en:catalase-optimum-requires-assay-scope",
        "synthesis:en:catalase-assay-conditions",
        "src:aebi-1984-catalase-in-vitro",
        "src:wu-lin-wolfbeis-2003-catalase-assay",
    ]
    return {
        "boundaries": {
            "browser_implementation_authorized": False,
            "candidate_resolution_authorized": False,
            "cross_domain_required": True,
            "existing_canonical_revisions_only": True,
            "fixture_count_authorized": 1,
            "live_principia_dependency": False,
            "new_canonical_authoring_authorized": False,
            "production_implementation_authorized": False,
            "release_mutation": False,
        },
        "bridge_fixture": _bridge_fixture(),
        "canonical_source_pool": [{"id": entity_id, "revision": 1} for entity_id in source_pool],
        "contract": GENERALIZATION_FIXTURE_CONTRACT,
        "domain": "catalase-assay-methodology",
        "generalization_negative_cases": [
            {
                "expected_error": expected,
                "id": f"negative:generalization-{mutation}",
                "mutation": mutation,
            }
            for mutation, expected in GENERALIZATION_NEGATIVES
        ],
        "id": "generalization-fixture:phase4-catalase-en-v1",
        "mode": MODE,
        "phase": 4,
        "recommendation": "proceed-static-reader-reuse-evaluation",
        "research_baseline": {
            "contract": "atlas-phase3-research-foundation-baseline/0.1",
            "fixture_id": "research-fixture:phase4-catalase-generalization-v1",
            "report_digest": "8137f52625f2a0fcf693fd4b8fd3ba3281f602f4d8add2c57293fc8f6efb50d5",
            "structured_baseline_sha256": STRUCTURED_BASELINE_SHA256,
        },
        "research_fixture": _research_fixture(),
        "slice": 1,
        "source_digest": SOURCE_DIGEST,
        "structured_baseline": {
            "contract": "atlas-phase3-structured-baseline/0.1",
            "index_build_digest": INDEX_BUILD_DIGEST,
            "index_contract": "atlas-structured-index/0.1",
            "result_set_sha256": RESULT_SET_SHA256,
            "source_digest": SOURCE_DIGEST,
        },
        "version": 1,
        "workspace_fixture": {
            "contract": FIXTURE_CONTRACT,
            "id": "workspace-fixtures:phase4-catalase-generalization-en-v1",
            "mode": MODE,
            "negative_cases": [
                {
                    "expected_error": expected,
                    "id": f"negative:catalase-{mutation}",
                    "mutation": mutation,
                }
                for mutation, expected in CORE_NEGATIVES
            ],
            "source_digest": SOURCE_DIGEST,
            "version": 1,
            "workspace": _workspace(),
        },
        "workstream": 4,
    }
