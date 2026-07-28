"""Deterministic helpers for workspace generalization evidence."""
from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping

from tools.phase2_kernel import KernelError


def json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
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


def require_list(value: Any, code: str, message: str) -> list[Any]:
    if not isinstance(value, list):
        raise KernelError(code, message)
    return value


def exact_key(reference: Mapping[str, Any], code: str) -> str:
    entity_id = reference.get("id")
    revision = reference.get("revision")
    if not isinstance(entity_id, str) or not entity_id:
        raise KernelError(code, "exact reference requires an entity ID")
    if revision == "latest":
        raise KernelError("E-WORKSPACE-LATEST", "implicit latest is forbidden")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise KernelError(code, "exact reference requires a positive integer revision")
    return f"{entity_id}@{revision}"
