"""Strict policy wrapper for the accepted pinned Principia Phase 16-18 snapshot."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from .kernel import KernelError, KernelRepository
from .offline_protocol import (
    PRINCIPIA_REPOSITORY,
    SNAPSHOT_CONTRACT,
    audit_offline_protocol,
    import_offline_batch,
    load_snapshot_documents,
)

EXPECTED_PRINCIPIA_COMMIT = "4ecb41ad4f9f524e83cc0db43f672bd9dcf3b67a"
EXPECTED_PRINCIPIA_PR = 25
EXPECTED_ATLAS_SNAPSHOT = {
    "governance_merge_commit": "9370cc746e9756e433ac3772d56d079c9803b144",
    "governance_pull_request": 21,
    "implementation_merge_commit": "1cc4aec6908a8703a7f505478329c633a23b4ef9",
    "implementation_pull_request": 20,
    "path": "integration/principia-atlas/pilot/atlas-phase2-importer.snapshot.v02.json",
    "sha256": "255afa6be2e5b1c34f67da29b8f264f1980b2183a5233e9290847a23cc24543a",
}
EXPECTED_RECEIPT_IMPORTER = {
    "accepted_wire_contract": "principia-atlas-external-dependent/0.2",
    "adapter_contract": "atlas-principia-bridge-adapter/0.1",
    "operational_record_contract": "atlas-external-dependent/0.1",
    "repository": "Rhodan-lab/Atlas",
}
EXPECTED_IMPLEMENTATION = {
    "merge_commit": "1cc4aec6908a8703a7f505478329c633a23b4ef9",
    "pull_request": 20,
    "tested_head_commit": "379d88d620469a749cebb88b0b41d9960e667558",
}
EXPECTED_GOVERNANCE = {
    "head_commit": "c30bebf6a63263da8a4356f6c4dbc85f11a67bc4",
    "merge_commit": "9370cc746e9756e433ac3772d56d079c9803b144",
    "mode": "importer-candidate",
    "pull_request": 21,
    "state": "accepted",
}
EXPECTED_PHASE17_SOURCE = {
    "phase17_candidate_head_commit": "e260417ef7631ebf4f87c89faff7da45d571b63c",
    "phase17_merge_commit": "c9fba79f821d59b36030924e5c388f71a56f7787",
    "phase17_finalization_merge_commit": "806b03335a1d0b43e5a32ffecce8439350564152",
    "phase17_postmerge_path": "release/phase-17-postmerge.json",
    "phase17_postmerge_sha256": "0479849e0015d43c607bd9b65ae012c61050838a1ae3088b9e077f78fe787b28",
}


def _load_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise KernelError("E-POLICY-JSON", str(exc), str(path)) from exc
    if not isinstance(value, dict):
        raise KernelError(
            "E-POLICY-JSON-OBJECT",
            "document must be an object",
            str(path),
        )
    return value


def _validate_snapshot_identity(snapshot: Mapping[str, Any]) -> None:
    if snapshot.get("contract") != SNAPSHOT_CONTRACT:
        raise KernelError("E-SNAPSHOT-CONTRACT", "unsupported pinned snapshot contract")
    if snapshot.get("source_repository") != PRINCIPIA_REPOSITORY:
        raise KernelError("E-SNAPSHOT-REPOSITORY", "pinned snapshot repository mismatch")
    if snapshot.get("source_commit") != EXPECTED_PRINCIPIA_COMMIT:
        raise KernelError("E-SNAPSHOT-COMMIT", "pinned Principia commit mismatch")
    if snapshot.get("source_pull_request") != EXPECTED_PRINCIPIA_PR:
        raise KernelError("E-SNAPSHOT-PR", "pinned Principia pull request mismatch")
    if snapshot.get("mode") != "offline-protocol-audit-candidate":
        raise KernelError("E-SNAPSHOT-MODE", "unsupported snapshot mode")
    if snapshot.get("live") is not False:
        raise KernelError("E-SNAPSHOT-LIVE", "pinned snapshot must remain live=false")


def _safe_relative_path(value: Any, root: Path, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise KernelError("E-SNAPSHOT-PATH", f"{field} must be a non-empty path")
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise KernelError(
            "E-SNAPSHOT-PATH-ESCAPE",
            f"{field} escapes the repository root",
        )
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise KernelError(
            "E-SNAPSHOT-PATH-ESCAPE",
            f"{field} escapes the repository root",
        ) from exc
    return candidate.as_posix()


def validate_pinned_snapshot(snapshot_path: Path) -> dict[str, Any]:
    snapshot = _load_object(snapshot_path)
    _validate_snapshot_identity(snapshot)
    files = snapshot.get("files")
    if not isinstance(files, list) or len(files) != 9:
        raise KernelError(
            "E-SNAPSHOT-FILES",
            "accepted snapshot must contain exactly nine files",
        )
    root = snapshot_path.resolve().parents[3]
    source_paths: set[str] = set()
    fixture_paths: set[str] = set()
    for index, item in enumerate(files):
        if not isinstance(item, Mapping):
            raise KernelError("E-SNAPSHOT-FILE", f"files[{index}] must be an object")
        source = _safe_relative_path(
            item.get("source_path"),
            root,
            f"files[{index}].source_path",
        )
        fixture = _safe_relative_path(
            item.get("fixture_path"),
            root,
            f"files[{index}].fixture_path",
        )
        if not source.startswith("integration/principia-atlas/"):
            raise KernelError(
                "E-SNAPSHOT-SOURCE-PATH",
                "source path is outside the Principia integration boundary",
            )
        if not fixture.startswith("content/fixtures/"):
            raise KernelError(
                "E-SNAPSHOT-FIXTURE-PATH",
                "fixture path is outside Atlas fixture storage",
            )
        if source in source_paths or fixture in fixture_paths:
            raise KernelError("E-SNAPSHOT-DUPLICATE", "snapshot paths must be unique")
        source_paths.add(source)
        fixture_paths.add(fixture)
    return snapshot


def load_pinned_snapshot_documents(
    snapshot_path: Path,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    validate_pinned_snapshot(snapshot_path)
    return load_snapshot_documents(snapshot_path)


def validate_pinned_batch(batch: Mapping[str, Any]) -> None:
    if batch.get("atlas_snapshot") != EXPECTED_ATLAS_SNAPSHOT:
        raise KernelError(
            "E-BATCH-ATLAS-SNAPSHOT",
            "batch does not pin the complete accepted Atlas snapshot",
        )


def validate_pinned_receipt(receipt: Mapping[str, Any]) -> None:
    importer = receipt.get("atlas_importer")
    if not isinstance(importer, Mapping):
        raise KernelError("E-RECEIPT-IMPORTER", "atlas_importer must be an object")
    for field, expected in EXPECTED_RECEIPT_IMPORTER.items():
        if importer.get(field) != expected:
            raise KernelError(
                "E-RECEIPT-IMPORTER",
                f"receipt importer field {field!r} mismatch",
            )
    if importer.get("implementation") != EXPECTED_IMPLEMENTATION:
        raise KernelError(
            "E-RECEIPT-IMPLEMENTATION",
            "receipt implementation baseline mismatch",
        )
    if importer.get("governance_finalization") != EXPECTED_GOVERNANCE:
        raise KernelError(
            "E-RECEIPT-GOVERNANCE",
            "receipt governance baseline mismatch",
        )


def _unique_nested_ids(
    stream: Mapping[str, Any],
    collection_field: str,
    object_field: str,
    id_field: str,
    code: str,
) -> None:
    entries = stream.get(collection_field)
    if not isinstance(entries, list):
        raise KernelError(code, f"{collection_field} must be a list")
    seen: set[str] = set()
    for index, wrapper in enumerate(entries):
        if not isinstance(wrapper, Mapping) or not isinstance(
            wrapper.get(object_field),
            Mapping,
        ):
            raise KernelError(code, f"{collection_field}[{index}] is malformed")
        identifier = wrapper[object_field].get(id_field)
        if not isinstance(identifier, str) or not identifier:
            raise KernelError(
                code,
                f"{collection_field}[{index}] has no {id_field}",
            )
        if identifier in seen:
            raise KernelError(code, f"duplicate {id_field} {identifier!r}")
        seen.add(identifier)


def validate_pinned_protocol(
    event_stream: Mapping[str, Any],
    acknowledgement_stream: Mapping[str, Any],
    chain: Mapping[str, Any],
    reconciliation: Mapping[str, Any],
) -> None:
    _unique_nested_ids(
        event_stream,
        "events",
        "event",
        "event_id",
        "E-EVENT-DUPLICATE",
    )
    _unique_nested_ids(
        acknowledgement_stream,
        "acknowledgements",
        "acknowledgement",
        "acknowledgement_id",
        "E-ACK-DUPLICATE",
    )
    if chain.get("mode") != "offline-event-protocol":
        raise KernelError("E-CHAIN-MODE", "unsupported chain mode")
    source = reconciliation.get("source")
    if not isinstance(source, Mapping):
        raise KernelError(
            "E-RECONCILIATION-SOURCE",
            "reconciliation source must be an object",
        )
    for field, expected in EXPECTED_PHASE17_SOURCE.items():
        if source.get(field) != expected:
            raise KernelError(
                "E-RECONCILIATION-PROVENANCE",
                f"Phase 17 provenance field {field!r} mismatch",
            )


def import_pinned_offline_batch(
    batch: Mapping[str, Any],
    export_documents: Mapping[str, bytes],
    repository: KernelRepository,
) -> dict[str, Any]:
    validate_pinned_batch(batch)
    return import_offline_batch(batch, export_documents, repository)


def audit_pinned_offline_protocol(
    snapshot: Mapping[str, Any],
    batch: Mapping[str, Any],
    principia_receipt: Mapping[str, Any],
    event_stream: Mapping[str, Any],
    acknowledgement_stream: Mapping[str, Any],
    chain: Mapping[str, Any],
    reconciliation: Mapping[str, Any],
    export_documents: Mapping[str, bytes],
    repository: KernelRepository,
) -> dict[str, Any]:
    _validate_snapshot_identity(snapshot)
    validate_pinned_batch(batch)
    validate_pinned_receipt(principia_receipt)
    validate_pinned_protocol(
        event_stream,
        acknowledgement_stream,
        chain,
        reconciliation,
    )
    report = audit_offline_protocol(
        batch,
        principia_receipt,
        event_stream,
        acknowledgement_stream,
        chain,
        reconciliation,
        export_documents,
        repository,
    )
    report["source_repository"] = snapshot.get("source_repository")
    report["source_commit"] = snapshot.get("source_commit")
    report["source_pull_request"] = snapshot.get("source_pull_request")
    report["source_snapshot_contract"] = snapshot.get("contract")
    return report
