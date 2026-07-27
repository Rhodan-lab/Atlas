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
EXPECTED_BATCH_ID = "principia-atlas:offline-batch:thermal-control:0001"
EXPECTED_ATLAS_SNAPSHOT = {
    "governance_merge_commit": "9370cc746e9756e433ac3772d56d079c9803b144",
    "governance_pull_request": 21,
    "implementation_merge_commit": "1cc4aec6908a8703a7f505478329c633a23b4ef9",
    "implementation_pull_request": 20,
    "path": "integration/principia-atlas/pilot/atlas-phase2-importer.snapshot.v02.json",
    "sha256": "255afa6be2e5b1c34f67da29b8f264f1980b2183a5233e9290847a23cc24543a",
}
EXPECTED_SNAPSHOT_FILES = {
    "integration/principia-atlas/exports/feedback-instability.external-dependent.fixture.json": (
        "content/fixtures/phase2_bridge/principia-feedback-pr16-v02.json",
        "a0ab1e098b17a5cfe9fee521394513461a2f4e51",
    ),
    "integration/principia-atlas/exports/room-cooling.external-dependent.fixture.json": (
        "content/fixtures/phase2_protocol/room-cooling.external-dependent.v02.json",
        "e2857218e60d60b39003c0541166ea946cdbcbdd",
    ),
    "integration/principia-atlas/exports/refrigerator.external-dependent.fixture.json": (
        "content/fixtures/phase2_protocol/refrigerator.external-dependent.v02.json",
        "65e3471e4d66a515dd0c048ae8bbd7f087dde3e0",
    ),
    "integration/principia-atlas/pilot/thermal-control.multi-artifact.batch.v02.json": (
        "content/fixtures/phase2_protocol/thermal-control.multi-artifact.batch.v02.json",
        "7a466a8e4503e6aed9c30e549a3ace184788bd98",
    ),
    "integration/principia-atlas/pilot/thermal-control.multi-artifact.receipt.v02.json": (
        "content/fixtures/phase2_protocol/thermal-control.multi-artifact.receipt.v02.json",
        "d3a7e84d42d7ba62697738cb8e70943abd99f7fc",
    ),
    "integration/principia-atlas/pilot/thermal-control.lifecycle-events.v01.json": (
        "content/fixtures/phase2_protocol/thermal-control.lifecycle-events.v01.json",
        "f2f2bbdc3a4a72c5633ec3fd04670acdb59908f7",
    ),
    "integration/principia-atlas/pilot/thermal-control.lifecycle-acknowledgements.v01.json": (
        "content/fixtures/phase2_protocol/thermal-control.lifecycle-acknowledgements.v01.json",
        "7060a49303cba9d8bd600136ec087115f40b7262",
    ),
    "integration/principia-atlas/pilot/thermal-control.event-protocol-chain.v01.json": (
        "content/fixtures/phase2_protocol/thermal-control.event-protocol-chain.v01.json",
        "19c1cf5f64a25cdf818de404b6f8c6fadb022d5b",
    ),
    "integration/principia-atlas/pilot/thermal-control.reconciliation-report.v01.json": (
        "content/fixtures/phase2_protocol/thermal-control.reconciliation-report.v01.json",
        "77c8104b0a04f81df187e33a2265181343e31df7",
    ),
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
EXPECTED_PROTOCOL_IDS = {
    "event_stream": "principia-atlas:offline-lifecycle-events:thermal-control:0001",
    "acknowledgement_stream": "principia-atlas:offline-lifecycle-acks:thermal-control:0001",
    "chain": "principia-atlas:offline-event-protocol-chain:thermal-control:0001",
    "reconciliation": "principia-atlas:offline-reconciliation:thermal-control:0001",
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
    if not isinstance(files, list) or len(files) != len(EXPECTED_SNAPSHOT_FILES):
        raise KernelError(
            "E-SNAPSHOT-FILES",
            "accepted snapshot has the wrong file count",
        )
    root = snapshot_path.resolve().parents[3]
    actual: dict[str, tuple[str, str]] = {}
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
        blob = item.get("source_blob_sha")
        if not isinstance(blob, str):
            raise KernelError("E-SNAPSHOT-BLOB", "source_blob_sha must be a string")
        if source in actual:
            raise KernelError("E-SNAPSHOT-DUPLICATE", "snapshot source paths must be unique")
        actual[source] = (fixture, blob)
    if actual != EXPECTED_SNAPSHOT_FILES:
        raise KernelError(
            "E-SNAPSHOT-MAPPING",
            "snapshot source, fixture, or Git blob mapping differs from the accepted baseline",
        )
    return snapshot


def load_pinned_snapshot_documents(
    snapshot_path: Path,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    validate_pinned_snapshot(snapshot_path)
    return load_snapshot_documents(snapshot_path)


def validate_pinned_batch(batch: Mapping[str, Any]) -> None:
    if batch.get("batch_id") != EXPECTED_BATCH_ID:
        raise KernelError("E-BATCH-ID", "pinned batch identity mismatch")
    if batch.get("sequence") != 1 or batch.get("previous_receipt_sha256") is not None:
        raise KernelError("E-BATCH-SEQUENCE", "pinned batch sequence baseline mismatch")
    if batch.get("atlas_snapshot") != EXPECTED_ATLAS_SNAPSHOT:
        raise KernelError(
            "E-BATCH-ATLAS-SNAPSHOT",
            "batch does not pin the complete accepted Atlas snapshot",
        )


def validate_pinned_receipt(receipt: Mapping[str, Any]) -> None:
    if receipt.get("batch_id") != EXPECTED_BATCH_ID:
        raise KernelError("E-RECEIPT-BATCH", "pinned receipt batch identity mismatch")
    if receipt.get("receipt_id") != "principia-atlas:offline-receipt:thermal-control:0001":
        raise KernelError("E-RECEIPT-ID", "pinned receipt identity mismatch")
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
    if event_stream.get("stream_id") != EXPECTED_PROTOCOL_IDS["event_stream"]:
        raise KernelError("E-EVENT-STREAM-ID", "event stream identity mismatch")
    if acknowledgement_stream.get("stream_id") != EXPECTED_PROTOCOL_IDS[
        "acknowledgement_stream"
    ]:
        raise KernelError("E-ACK-STREAM-ID", "acknowledgement stream identity mismatch")
    if chain.get("chain_id") != EXPECTED_PROTOCOL_IDS["chain"]:
        raise KernelError("E-CHAIN-ID", "event-protocol chain identity mismatch")
    if reconciliation.get("reconciliation_id") != EXPECTED_PROTOCOL_IDS[
        "reconciliation"
    ]:
        raise KernelError("E-RECONCILIATION-ID", "reconciliation identity mismatch")
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
    if len(event_stream.get("events", [])) != 2:
        raise KernelError("E-EVENT-COUNT", "accepted event stream must contain two events")
    if len(acknowledgement_stream.get("acknowledgements", [])) != 2:
        raise KernelError(
            "E-ACK-COUNT",
            "accepted acknowledgement stream must contain two acknowledgements",
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
