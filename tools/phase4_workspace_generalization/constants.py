#!/usr/bin/env python3
"""Constants and deterministic helpers for Catalase workspace generalization."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from tools.phase2_kernel import KernelError
from tools.phase4_workspace.contracts import (
    DECISION_CONTRACT,
    ENTRY_CONTRACT,
    EXPORT_CONTRACT,
    FAILURE_CONTRACT,
    MANIFEST_CONTRACT,
    MODE,
    WORKSPACE_CONTRACT,
)

FIXTURE_CONTRACT = "atlas-phase4-workspace-generalization-fixtures/0.1"
SELECTION_CONTRACT = "atlas-phase4-workspace-generalization-selection/0.1"
VALIDATION_CONTRACT = "atlas-phase4-workspace-generalization-validation/0.1"
REPORT_CONTRACT = "atlas-phase4-workspace-generalization-report/0.1"
BASELINE_CONTRACT = "atlas-phase4-workspace-generalization-baseline/0.1"
RECOMMENDATION = "proceed-static-reader-reuse-evaluation"

SOURCE_DIGEST = "684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1"
SOURCE_POOL_SHA256 = "ce2db090fe0432a9b52194b3d981285cfcf388717db05bd23dc3d86caaa37f23"
PRIOR_EXPORT_SHA256 = "43f28738c4678dfcd0f7a3e4d31480f891112a8c9bd220929f8f32cd80edb98a"
PRIOR_EXPORT_DIGEST = "82f08c18ae76b4b4d091fe0d8be7d54cf5d10d989443132a26e550056af3f56a"

SOURCE_POOL = [
    {"id": "question:en:how-assay-conditions-affect-catalase", "revision": 1},
    {"id": "concept:en:catalase", "revision": 1},
    {"id": "model:en:catalase-assay-observation", "revision": 1},
    {"id": "evidence:en:fluorescent-catalase-assay-neutral-ph", "revision": 1},
    {"id": "claim:en:catalase-optimum-requires-assay-scope", "revision": 1},
    {"id": "synthesis:en:catalase-assay-conditions", "revision": 1},
    {"id": "src:aebi-1984-catalase-in-vitro", "revision": 1},
    {"id": "src:wu-lin-wolfbeis-2003-catalase-assay", "revision": 1},
]

SELECTED_ENTRY_KEYS = [
    "question:en:how-assay-conditions-affect-catalase@1",
    "claim:en:catalase-optimum-requires-assay-scope@1",
    "synthesis:en:catalase-assay-conditions@1",
    "model:en:catalase-assay-observation@1",
    "evidence:en:fluorescent-catalase-assay-neutral-ph@1",
]

PROHIBITED_KEYS = frozenset({
    "timestamp", "generated_at", "created_at", "updated_at", "random_id",
    "machine_path", "absolute_path", "credential", "token", "api_key",
})

EXPECTED_AUTHORITY = {
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

REUSED_CONTRACTS = {
    "workspace": WORKSPACE_CONTRACT,
    "entry": ENTRY_CONTRACT,
    "decision": DECISION_CONTRACT,
    "export": EXPORT_CONTRACT,
    "manifest": MANIFEST_CONTRACT,
    "failure": FAILURE_CONTRACT,
}


def json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def seal(record: Mapping[str, Any]) -> dict[str, Any]:
    unsigned = dict(record)
    unsigned.pop("report_digest", None)
    sealed = dict(record)
    sealed["report_digest"] = json_sha256(unsigned)
    return sealed


def require_mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def require_string(value: Any, code: str, message: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise KernelError(code, message)
    return value


def exact_key(reference: Mapping[str, Any], code: str) -> str:
    entity_id = require_string(reference.get("id"), code, "exact reference requires an entity ID")
    revision = reference.get("revision")
    if isinstance(revision, str) and revision.lower() == "latest":
        raise KernelError("E-GENERALIZATION-LATEST", "implicit latest is forbidden")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError(code, "exact reference requires a positive integer revision")
    return f"{entity_id}@{revision}"


def validate_no_nondeterminism(value: Any, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if key in PROHIBITED_KEYS:
                raise KernelError("E-GENERALIZATION-DETERMINISM", f"prohibited field at {path}.{key}")
            validate_no_nondeterminism(item, f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            validate_no_nondeterminism(item, f"{path}[{index}]")
