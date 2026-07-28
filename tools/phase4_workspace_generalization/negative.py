"""Negative-case execution for Catalase workspace generalization."""
from __future__ import annotations

import copy
from typing import Any, Mapping

from tools.phase2_kernel import KernelError, KernelRepository
from tools.phase4_workspace_generalization.util import require_list, require_mapping
from tools.phase4_workspace_generalization.validation import validate_positive


def apply_negative(fixture: Mapping[str, Any], case: Mapping[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(fixture)
    mutation = case.get("mutation")
    workspace = candidate["workspace_fixture"]["workspace"]
    authority = workspace["authority"]
    if mutation == "non-catalase-entry":
        workspace["entries"][0]["exact_reference"] = {
            "id": "claim:en:recommender-effects-are-context-dependent",
            "revision": 1,
        }
    elif mutation == "reordered-accepted-trail":
        workspace["entries"][0], workspace["entries"][1] = workspace["entries"][1], workspace["entries"][0]
    elif mutation == "modified-workspace-contract":
        workspace["contract"] = "atlas-research-workspace/9.9"
    elif mutation == "account-required":
        authority["account_required"] = True
    elif mutation == "cloud-required":
        authority["cloud_required"] = True
    elif mutation == "canonical-mutation":
        authority["canonical_mutation"] = True
    elif mutation == "review-mutation":
        authority["review_mutation"] = True
    elif mutation == "repository-mutation":
        authority["repository_mutation"] = True
    elif mutation == "browser-implementation":
        candidate["boundaries"]["browser_implementation_authorized"] = True
    elif mutation == "production-implementation":
        candidate["boundaries"]["production_implementation_authorized"] = True
    elif mutation == "release-mutation":
        candidate["boundaries"]["release_mutation"] = True
    elif mutation == "second-active-fixture":
        candidate["boundaries"]["fixture_count_authorized"] = 2
    elif mutation == "production-architecture-selection":
        authority["production_frontend_architecture_selected"] = True
    elif mutation == "credential-required":
        workspace["credential"] = "forbidden-placeholder"
    else:
        raise KernelError("E-GENERALIZATION-NEGATIVE", f"unsupported mutation {mutation!r}")
    return candidate


def validate_negative_cases(fixture: Mapping[str, Any], repository: KernelRepository) -> list[dict[str, Any]]:
    cases = require_list(
        fixture.get("generalization_negative_cases"),
        "E-GENERALIZATION-NEGATIVE",
        "generalization negative cases must be a list",
    )
    if len(cases) < 12:
        raise KernelError("E-GENERALIZATION-NEGATIVE", "at least twelve cross-domain negative cases are required")
    results: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in cases:
        case = require_mapping(raw, "E-GENERALIZATION-NEGATIVE", "negative case must be an object")
        case_id = case.get("id")
        expected = case.get("expected_error")
        if not isinstance(case_id, str) or not case_id or case_id in seen:
            raise KernelError("E-GENERALIZATION-NEGATIVE", "negative case IDs must be unique strings")
        if not isinstance(expected, str) or not expected:
            raise KernelError("E-GENERALIZATION-NEGATIVE", "negative case requires expected_error")
        seen.add(case_id)
        try:
            validate_positive(apply_negative(fixture, case), repository)
        except KernelError as exc:
            if exc.code != expected:
                raise KernelError(
                    "E-GENERALIZATION-NEGATIVE",
                    f"{case_id} expected {expected}, observed {exc.code}",
                ) from exc
            results.append({
                "id": case_id,
                "mutation": case.get("mutation"),
                "observed_error": exc.code,
                "preserved_previous_valid_workspace": True,
                "decision": "rejected-as-required",
            })
        else:
            raise KernelError("E-GENERALIZATION-NEGATIVE", f"{case_id} was accepted unexpectedly")
    return results
