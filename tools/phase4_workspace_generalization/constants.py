"""Constants and deterministic helpers for Workstream 4."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from tools.phase2_kernel import KernelError

MODE = "interactive-experience-foundation"
SPEC_CONTRACT = "atlas-phase4-workstream4-generalization-fixture/0.1"
EVALUATION_CONTRACT = "atlas-phase4-workstream4-generalization-report/0.1"
VALIDATION_CONTRACT = "atlas-phase4-workstream4-generalization-validation/0.1"
BASELINE_CONTRACT = "atlas-phase4-workstream4-generalization-baseline/0.1"
SOURCE_DIGEST = "684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1"
STRUCTURED_BASELINE_SHA256 = "fc2bf63814e029ceffd6b66f493ae7f0fc30b8bff207ffd39393b8739de9dca5"
RECOMMENDATION = "proceed-static-reader-reuse-evaluation"
ELIGIBLE_IDS = frozenset({
    "question:en:how-assay-conditions-affect-catalase",
    "concept:en:catalase",
    "model:en:catalase-assay-observation",
    "evidence:en:fluorescent-catalase-assay-neutral-ph",
    "claim:en:catalase-optimum-requires-assay-scope",
    "synthesis:en:catalase-assay-conditions",
    "src:aebi-1984-catalase-in-vitro",
    "src:wu-lin-wolfbeis-2003-catalase-assay",
})


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


def require(condition: bool, code: str, message: str) -> None:
    if not condition:
        raise KernelError(code, message)


def exact_key(reference: Mapping[str, Any]) -> str:
    entity_id = reference.get("id")
    revision = reference.get("revision")
    if revision == "latest":
        raise KernelError("E-WORKSPACE-LATEST", "generalization references may not use implicit latest")
    if not isinstance(entity_id, str) or not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError("E-W4-REFERENCE", "generalization references require exact positive revisions")
    return f"{entity_id}@{revision}"
