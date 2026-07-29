"""Validate the bounded Catalase generalization specification."""
from __future__ import annotations

from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository

from .constants import (
    ELIGIBLE_IDS,
    MODE,
    SOURCE_DIGEST,
    SPEC_CONTRACT,
    exact_key,
    require,
)


def validate_spec(spec: Mapping[str, Any], repository: KernelRepository) -> dict[str, Any]:
    require(spec.get("contract") == SPEC_CONTRACT, "E-W4-CONTRACT", f"expected {SPEC_CONTRACT!r}")
    require(spec.get("mode") == MODE, "E-W4-MODE", f"expected mode {MODE!r}")
    require(spec.get("version") == 1, "E-W4-VERSION", "generalization fixture version must be 1")
    require(
        spec.get("source_digest") == repository.runtime["source_digest"] == SOURCE_DIGEST,
        "E-W4-SOURCE",
        "source digest mismatch",
    )
    require(spec.get("fixture_count_authorized") == 1, "E-W4-FIXTURE-COUNT", "exactly one fixture is authorized")
    require(
        spec.get("domain") == "catalase-assay-methodology",
        "E-W4-DOMAIN",
        "only the Catalase assay-methodology fixture is authorized",
    )

    authority = spec.get("authority")
    require(isinstance(authority, Mapping), "E-W4-AUTHORITY", "authority block is required")
    required_authority = {
        "existing_canonical_revisions_only": True,
        "new_canonical_authoring_authorized": False,
        "browser_implementation_authorized": False,
        "production_implementation_authorized": False,
        "canonical_mutation": False,
        "lifecycle_mutation": False,
        "review_mutation": False,
        "repository_mutation": False,
        "production_frontend_architecture_selected": False,
        "live_principia_dependency": False,
        "account_required": False,
        "cloud_required": False,
        "external_network_required": False,
    }
    for field, expected in required_authority.items():
        require(authority.get(field) == expected, "E-W4-AUTHORITY", f"generalization requires {field}={expected!r}")

    eligible = spec.get("eligible_exact_references")
    require(isinstance(eligible, list) and len(eligible) == 8, "E-W4-ELIGIBLE", "exactly eight eligible references are required")
    eligible_keys = [exact_key(item) for item in eligible if isinstance(item, Mapping)]
    require(len(eligible_keys) == 8 and len(set(eligible_keys)) == 8, "E-W4-ELIGIBLE", "eligible references must be unique")
    require({key.rsplit("@", 1)[0] for key in eligible_keys} == ELIGIBLE_IDS, "E-W4-DOMAIN", "eligible pool differs from governance")
    for item in eligible:
        assert isinstance(item, Mapping)
        try:
            repository.exact(str(item["id"]), int(item["revision"]))
        except KernelError as exc:
            raise KernelError("E-W4-REVISION", f"eligible revision unavailable: {exact_key(item)}") from exc

    selected = spec.get("selected_entries")
    require(isinstance(selected, list) and len(selected) == 5, "E-W4-SELECTION", "exactly five entries are required")
    selected_keys: list[str] = []
    for item in selected:
        require(isinstance(item, Mapping), "E-W4-SELECTION", "selected entry must be an object")
        reference = item.get("exact_reference")
        require(isinstance(reference, Mapping), "E-W4-SELECTION", "selected entry requires exact_reference")
        key = exact_key(reference)
        selected_keys.append(key)
        entity_id = key.rsplit("@", 1)[0]
        require(entity_id in ELIGIBLE_IDS, "E-W4-DOMAIN", f"non-Catalase entry is forbidden: {entity_id}")
        require(not entity_id.startswith(("claim:en:recommender", "synthesis:en:recommender")), "E-W4-DOMAIN", "recommender entry is forbidden")
        require(item.get("action") in {"include", "exclude", "context"}, "E-W4-SELECTION", "unsupported action")
        for field in ("rationale", "summary"):
            require(isinstance(item.get(field), str) and item[field].strip(), "E-W4-SELECTION", f"selected entry requires {field}")
    require(len(set(selected_keys)) == 5, "E-W4-SELECTION", "selected entries must be unique")

    candidates = spec.get("candidate_definitions")
    require(isinstance(candidates, list) and len(candidates) == 2, "E-W4-CANDIDATE", "exactly two candidates are required")
    kinds = {item.get("kind") for item in candidates if isinstance(item, Mapping)}
    require(kinds == {"contradiction", "duplicate"}, "E-W4-CANDIDATE", "one contradiction and one duplicate are required")
    require(
        any(item.get("assessment") == "scope-difference-likely" for item in candidates if isinstance(item, Mapping)),
        "E-W4-CANDIDATE",
        "one scope-difference assessment is required",
    )

    require(
        spec.get("allowed_decisions") == [
            "proceed-static-reader-reuse-evaluation",
            "hold-for-contract-review",
            "reject-catalase-generalization",
        ],
        "E-W4-DECISION",
        "allowed decisions differ from governance",
    )
    query = spec.get("query")
    require(isinstance(query, Mapping), "E-W4-QUERY", "query snapshot is required")
    require(query.get("id") == "query:retrieval:catalase-assay-comparison-scope", "E-W4-QUERY", "unexpected query identity")
    require(isinstance(query.get("text"), str) and "universal" in query["text"].lower(), "E-W4-QUERY", "query must preserve scope boundary")

    return {
        "contract": "atlas-phase4-workstream4-generalization-spec-validation/0.1",
        "decision": "valid",
        "eligible_count": len(eligible_keys),
        "selected_count": len(selected_keys),
        "candidate_count": len(candidates),
        "source_digest": repository.runtime["source_digest"],
        "live": False,
        "repository_mutation": False,
    }
