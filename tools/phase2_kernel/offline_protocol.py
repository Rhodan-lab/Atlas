"""Offline multi-artifact and lifecycle-protocol verification for Atlas Phase 2.

The protocol layer consumes pinned Principia evidence only. It never calls the
Principia repository, mutates canonical Atlas content, changes either
repository's status, or treats bounded synthetic lifecycle events as real Atlas
transitions.
"""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping, Sequence

from .bridge import import_principia_candidate, lifecycle_impact_report
from .kernel import KernelError, KernelRepository, exact_key, render_json

PRINCIPIA_BATCH_CONTRACT = "principia-atlas-offline-import-batch/0.2"
PRINCIPIA_RECEIPT_CONTRACT = "principia-atlas-offline-batch-receipt/0.2"
PRINCIPIA_EVENT_CONTRACT = "principia-atlas-offline-lifecycle-event/0.1"
PRINCIPIA_EVENT_STREAM_CONTRACT = (
    "principia-atlas-offline-lifecycle-event-stream/0.1"
)
PRINCIPIA_ACK_CONTRACT = (
    "principia-atlas-offline-lifecycle-acknowledgement/0.1"
)
PRINCIPIA_ACK_STREAM_CONTRACT = (
    "principia-atlas-offline-lifecycle-acknowledgement-stream/0.1"
)
PRINCIPIA_CHAIN_CONTRACT = "principia-atlas-offline-event-protocol-chain/0.1"
PRINCIPIA_RECONCILIATION_CONTRACT = (
    "principia-atlas-offline-reconciliation-report/0.1"
)
ATLAS_BATCH_RECEIPT_CONTRACT = "atlas-principia-offline-batch-receipt/0.1"
ATLAS_PROTOCOL_AUDIT_CONTRACT = "atlas-principia-offline-protocol-audit/0.1"
SNAPSHOT_CONTRACT = "atlas-principia-offline-snapshot/0.1"

ATLAS_IMPLEMENTATION_MERGE = "1cc4aec6908a8703a7f505478329c633a23b4ef9"
ATLAS_GOVERNANCE_MERGE = "9370cc746e9756e433ac3772d56d079c9803b144"
PRINCIPIA_REPOSITORY = "Rhodan-lab/principle-to-system"

_HEX_64 = re.compile(r"^[0-9a-f]{64}$")
_HEX_40 = re.compile(r"^[0-9a-f]{40}$")
_EVENT_TARGETS = {"deprecated", "retracted"}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_document(value: Mapping[str, Any]) -> str:
    return sha256_bytes(render_json(value).encode("utf-8"))


def git_blob_sha(value: bytes) -> str:
    header = f"blob {len(value)}\0".encode("ascii")
    return hashlib.sha1(header + value).hexdigest()


def _read_json_bytes(value: bytes, path: str) -> dict[str, Any]:
    try:
        payload = json.loads(value.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise KernelError("E-OFFLINE-JSON", str(exc), path) from exc
    if not isinstance(payload, dict):
        raise KernelError("E-OFFLINE-JSON-OBJECT", "document must be an object", path)
    return payload


def _expect_mapping(value: Any, code: str, message: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise KernelError(code, message)
    return value


def _expect_list(value: Any, code: str, message: str) -> list[Any]:
    if not isinstance(value, list):
        raise KernelError(code, message)
    return value


def _expect_keys(
    value: Mapping[str, Any],
    allowed: set[str],
    required: set[str],
    path: str,
) -> None:
    unknown = sorted(set(value) - allowed)
    missing = sorted(required - set(value))
    if unknown:
        raise KernelError(
            "E-OFFLINE-FIELD",
            f"unsupported fields: {unknown}",
            path,
        )
    if missing:
        raise KernelError(
            "E-OFFLINE-FIELD-MISSING",
            f"missing fields: {missing}",
            path,
        )


def _positive_int(value: Any, code: str, message: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise KernelError(code, message)
    return value


def _require_false(value: Any, code: str, message: str) -> None:
    if value is not False:
        raise KernelError(code, message)


def _require_digest(value: Any, code: str, message: str) -> str:
    if not isinstance(value, str) or not _HEX_64.fullmatch(value):
        raise KernelError(code, message)
    return value


def _require_commit(value: Any, code: str, message: str) -> str:
    if not isinstance(value, str) or not _HEX_40.fullmatch(value):
        raise KernelError(code, message)
    return value


def _validate_authority(value: Any, path: str, *, require_status_rule: bool = False) -> None:
    authority = _expect_mapping(
        value,
        "E-OFFLINE-AUTHORITY",
        f"{path} authority must be an object",
    )
    for field in (
        "automatic_status_change",
        "automatic_release_action",
        "repository_mutation",
    ):
        _require_false(
            authority.get(field),
            "E-OFFLINE-AUTOMATIC-MUTATION",
            f"{path}.{field} must be false",
        )
    if require_status_rule and authority.get("status_inheritance") != "prohibited":
        raise KernelError(
            "E-OFFLINE-STATUS-INHERITANCE",
            f"{path}.status_inheritance must be 'prohibited'",
        )


def load_snapshot_documents(
    snapshot_path: Path,
) -> tuple[dict[str, Any], dict[str, bytes]]:
    """Load and verify a pinned external fixture set without network access."""
    snapshot_raw = snapshot_path.read_bytes()
    snapshot = _read_json_bytes(snapshot_raw, str(snapshot_path))
    if snapshot.get("contract") != SNAPSHOT_CONTRACT:
        raise KernelError(
            "E-SNAPSHOT-CONTRACT",
            f"expected {SNAPSHOT_CONTRACT!r}, got {snapshot.get('contract')!r}",
            str(snapshot_path),
        )
    if snapshot.get("source_repository") != PRINCIPIA_REPOSITORY:
        raise KernelError(
            "E-SNAPSHOT-REPOSITORY",
            f"expected {PRINCIPIA_REPOSITORY!r}",
            str(snapshot_path),
        )
    _require_commit(
        snapshot.get("source_commit"),
        "E-SNAPSHOT-COMMIT",
        "source_commit must be a full commit SHA",
    )
    _require_false(
        snapshot.get("live"),
        "E-SNAPSHOT-LIVE",
        "snapshot must remain live=false",
    )
    files = _expect_list(
        snapshot.get("files"),
        "E-SNAPSHOT-FILES",
        "files must be a list",
    )
    documents: dict[str, bytes] = {}
    source_paths: set[str] = set()
    fixture_paths: set[str] = set()
    root = snapshot_path.resolve().parents[3]
    for index, item in enumerate(files):
        record = _expect_mapping(
            item,
            "E-SNAPSHOT-FILE",
            f"files[{index}] must be an object",
        )
        source_path = record.get("source_path")
        fixture_path = record.get("fixture_path")
        source_blob_sha = record.get("source_blob_sha")
        if not isinstance(source_path, str) or not source_path:
            raise KernelError("E-SNAPSHOT-PATH", "source_path must be non-empty")
        if not isinstance(fixture_path, str) or not fixture_path:
            raise KernelError("E-SNAPSHOT-PATH", "fixture_path must be non-empty")
        _require_commit(
            source_blob_sha,
            "E-SNAPSHOT-BLOB",
            "source_blob_sha must be a full Git blob SHA",
        )
        if source_path in source_paths or fixture_path in fixture_paths:
            raise KernelError(
                "E-SNAPSHOT-DUPLICATE",
                f"duplicate snapshot path at files[{index}]",
            )
        source_paths.add(source_path)
        fixture_paths.add(fixture_path)
        local_path = root / fixture_path
        try:
            raw = local_path.read_bytes()
        except OSError as exc:
            raise KernelError("E-SNAPSHOT-READ", str(exc), fixture_path) from exc
        actual_blob = git_blob_sha(raw)
        if actual_blob != source_blob_sha:
            raise KernelError(
                "E-SNAPSHOT-BLOB-MISMATCH",
                f"expected {source_blob_sha}, got {actual_blob}",
                fixture_path,
            )
        documents[source_path] = raw
    return snapshot, documents


def import_offline_batch(
    batch: Mapping[str, Any],
    export_documents: Mapping[str, bytes],
    repository: KernelRepository,
) -> dict[str, Any]:
    """Atomically validate and import a pinned Principia multi-artifact batch."""
    _expect_keys(
        batch,
        {
            "atlas_snapshot",
            "atomic",
            "batch_id",
            "contract",
            "inputs",
            "live",
            "mode",
            "previous_receipt_sha256",
            "sequence",
        },
        {
            "atlas_snapshot",
            "atomic",
            "batch_id",
            "contract",
            "inputs",
            "live",
            "mode",
            "previous_receipt_sha256",
            "sequence",
        },
        "$batch",
    )
    if batch.get("contract") != PRINCIPIA_BATCH_CONTRACT:
        raise KernelError(
            "E-BATCH-CONTRACT",
            f"expected {PRINCIPIA_BATCH_CONTRACT!r}",
        )
    if batch.get("atomic") is not True:
        raise KernelError("E-BATCH-ATOMIC", "batch must declare atomic=true")
    _require_false(batch.get("live"), "E-BATCH-LIVE", "batch must remain live=false")
    if batch.get("mode") != "offline-multi-artifact-pilot":
        raise KernelError("E-BATCH-MODE", "unsupported offline batch mode")
    batch_id = batch.get("batch_id")
    if not isinstance(batch_id, str) or not batch_id:
        raise KernelError("E-BATCH-ID", "batch_id must be non-empty")
    sequence = _positive_int(
        batch.get("sequence"),
        "E-BATCH-SEQUENCE",
        "sequence must be a positive integer",
    )
    previous = batch.get("previous_receipt_sha256")
    if previous is not None:
        _require_digest(
            previous,
            "E-BATCH-PREVIOUS",
            "previous_receipt_sha256 must be null or SHA-256",
        )

    atlas_snapshot = _expect_mapping(
        batch.get("atlas_snapshot"),
        "E-BATCH-ATLAS-SNAPSHOT",
        "atlas_snapshot must be an object",
    )
    if atlas_snapshot.get("implementation_merge_commit") != ATLAS_IMPLEMENTATION_MERGE:
        raise KernelError(
            "E-BATCH-ATLAS-IMPLEMENTATION",
            "batch does not pin the accepted Atlas importer implementation",
        )
    if atlas_snapshot.get("governance_merge_commit") != ATLAS_GOVERNANCE_MERGE:
        raise KernelError(
            "E-BATCH-ATLAS-GOVERNANCE",
            "batch does not pin the accepted Atlas importer governance record",
        )
    _require_digest(
        atlas_snapshot.get("sha256"),
        "E-BATCH-ATLAS-SNAPSHOT-DIGEST",
        "atlas snapshot SHA-256 is malformed",
    )

    inputs = _expect_list(batch.get("inputs"), "E-BATCH-INPUTS", "inputs must be a list")
    if len(inputs) < 2:
        raise KernelError("E-BATCH-INPUTS", "multi-artifact batch requires at least two inputs")

    artifact_ids: list[str] = []
    staged: list[dict[str, Any]] = []
    for index, item in enumerate(inputs):
        record = _expect_mapping(
            item,
            "E-BATCH-INPUT",
            f"inputs[{index}] must be an object",
        )
        _expect_keys(
            record,
            {
                "artifact_id",
                "artifact_revision",
                "dependency_count",
                "export_path",
                "export_sha256",
            },
            {
                "artifact_id",
                "artifact_revision",
                "dependency_count",
                "export_path",
                "export_sha256",
            },
            f"$batch.inputs[{index}]",
        )
        artifact_id = record.get("artifact_id")
        export_path = record.get("export_path")
        if not isinstance(artifact_id, str) or not artifact_id:
            raise KernelError("E-BATCH-ARTIFACT-ID", "artifact_id must be non-empty")
        if not isinstance(export_path, str) or export_path not in export_documents:
            raise KernelError(
                "E-BATCH-EXPORT-MISSING",
                f"pinned export {export_path!r} is unavailable",
            )
        artifact_revision = _positive_int(
            record.get("artifact_revision"),
            "E-BATCH-ARTIFACT-REVISION",
            "artifact_revision must be positive",
        )
        dependency_count = _positive_int(
            record.get("dependency_count"),
            "E-BATCH-DEPENDENCY-COUNT",
            "dependency_count must be positive",
        )
        expected_sha = _require_digest(
            record.get("export_sha256"),
            "E-BATCH-EXPORT-DIGEST",
            "export_sha256 must be a SHA-256 digest",
        )
        raw = export_documents[export_path]
        actual_sha = sha256_bytes(raw)
        if actual_sha != expected_sha:
            raise KernelError(
                "E-BATCH-EXPORT-DIGEST-MISMATCH",
                f"{export_path!r} expected {expected_sha}, got {actual_sha}",
            )
        payload = _read_json_bytes(raw, export_path)
        imported = import_principia_candidate(payload, repository)
        if imported.get("id") != artifact_id or imported.get("revision") != artifact_revision:
            raise KernelError(
                "E-BATCH-ARTIFACT-MISMATCH",
                f"batch metadata does not match {export_path!r}",
            )
        if len(imported.get("dependencies", [])) != dependency_count:
            raise KernelError(
                "E-BATCH-DEPENDENCY-COUNT-MISMATCH",
                f"batch metadata does not match dependency count for {artifact_id!r}",
            )
        artifact_ids.append(artifact_id)
        staged.append(imported)

    if artifact_ids != sorted(artifact_ids):
        raise KernelError("E-BATCH-ORDER", "inputs must use deterministic artifact ordering")
    if len(set(artifact_ids)) != len(artifact_ids):
        raise KernelError("E-BATCH-DUPLICATE", "artifact IDs must be unique")

    return {
        "contract": ATLAS_BATCH_RECEIPT_CONTRACT,
        "source_contract": PRINCIPIA_BATCH_CONTRACT,
        "batch_id": batch_id,
        "sequence": sequence,
        "previous_receipt_sha256": previous,
        "atomic": True,
        "mode": "offline-protocol-audit-candidate",
        "live": False,
        "record_count": len(staged),
        "records": sorted(staged, key=lambda value: (value["id"], value["revision"])),
        "status_inheritance": "prohibited",
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }


def verify_principia_receipt(
    batch: Mapping[str, Any],
    principia_receipt: Mapping[str, Any],
    atlas_receipt: Mapping[str, Any],
) -> dict[str, Any]:
    """Verify Principia's pinned receipt against a fresh Atlas re-import."""
    if principia_receipt.get("contract") != PRINCIPIA_RECEIPT_CONTRACT:
        raise KernelError("E-RECEIPT-CONTRACT", "unsupported Principia receipt contract")
    _require_false(
        principia_receipt.get("live"),
        "E-RECEIPT-LIVE",
        "receipt must remain live=false",
    )
    if principia_receipt.get("batch_id") != batch.get("batch_id"):
        raise KernelError("E-RECEIPT-BATCH", "receipt batch_id mismatch")
    if principia_receipt.get("sequence") != batch.get("sequence"):
        raise KernelError("E-RECEIPT-SEQUENCE", "receipt sequence mismatch")
    if principia_receipt.get("previous_receipt_sha256") != batch.get(
        "previous_receipt_sha256"
    ):
        raise KernelError("E-RECEIPT-PREVIOUS", "receipt predecessor mismatch")
    if principia_receipt.get("batch_sha256") != sha256_document(batch):
        raise KernelError("E-RECEIPT-BATCH-DIGEST", "receipt batch digest mismatch")

    importer = _expect_mapping(
        principia_receipt.get("atlas_importer"),
        "E-RECEIPT-IMPORTER",
        "atlas_importer must be an object",
    )
    implementation = _expect_mapping(
        importer.get("implementation"),
        "E-RECEIPT-IMPORTER",
        "implementation must be an object",
    )
    governance = _expect_mapping(
        importer.get("governance_finalization"),
        "E-RECEIPT-IMPORTER",
        "governance_finalization must be an object",
    )
    if implementation.get("merge_commit") != ATLAS_IMPLEMENTATION_MERGE:
        raise KernelError("E-RECEIPT-IMPLEMENTATION", "receipt pins wrong Atlas implementation")
    if governance.get("merge_commit") != ATLAS_GOVERNANCE_MERGE:
        raise KernelError("E-RECEIPT-GOVERNANCE", "receipt pins wrong Atlas governance")
    if governance.get("mode") != "importer-candidate" or governance.get("state") != "accepted":
        raise KernelError("E-RECEIPT-GOVERNANCE", "receipt importer baseline is not accepted")

    result = _expect_mapping(
        principia_receipt.get("result"),
        "E-RECEIPT-RESULT",
        "result must be an object",
    )
    _validate_authority(principia_receipt.get("authority"), "$receipt.authority")
    if result.get("accepted") is not True or result.get("atomic") is not True:
        raise KernelError("E-RECEIPT-RESULT", "receipt must be an accepted atomic result")
    if result.get("rejected_count") != 0:
        raise KernelError("E-RECEIPT-REJECTED", "receipt must not contain rejected records")
    if result.get("status_inheritance") != "prohibited":
        raise KernelError("E-OFFLINE-STATUS-INHERITANCE", "receipt status inheritance is prohibited")
    records = result.get("records")
    if records != atlas_receipt.get("records"):
        raise KernelError(
            "E-RECEIPT-REIMPORT-MISMATCH",
            "Principia receipt records differ from fresh Atlas import",
        )
    if result.get("accepted_count") != atlas_receipt.get("record_count"):
        raise KernelError("E-RECEIPT-COUNT", "receipt accepted_count mismatch")
    return {
        "contract": "atlas-principia-receipt-verification/0.1",
        "batch_id": batch.get("batch_id"),
        "record_count": atlas_receipt.get("record_count"),
        "verified": True,
        "live": False,
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }


def _repository_with_transition(
    repository: KernelRepository,
    entity_id: str,
    revision: int,
    target: str,
) -> KernelRepository:
    if target not in _EVENT_TARGETS:
        raise KernelError("E-EVENT-TRANSITION", f"unsupported synthetic target {target!r}")
    runtime = deepcopy(repository.runtime)
    key = exact_key(entity_id, revision)
    for entity in runtime.get("entities", []):
        if isinstance(entity, dict) and entity.get("key") == key:
            entity["status"] = target
            metadata = entity.get("metadata")
            if isinstance(metadata, dict):
                metadata["status"] = target
            break
    else:
        repository.exact(entity_id, revision)
        raise KernelError("E-EVENT-SUBJECT", f"subject {key!r} is unavailable")
    return KernelRepository(runtime)


def _verify_event_stream(
    event_stream: Mapping[str, Any],
    source_receipt: Mapping[str, Any],
    imported_records: Sequence[Mapping[str, Any]],
    repository: KernelRepository,
) -> list[dict[str, Any]]:
    if event_stream.get("contract") != PRINCIPIA_EVENT_STREAM_CONTRACT:
        raise KernelError("E-EVENT-STREAM-CONTRACT", "unsupported lifecycle event stream")
    _require_false(event_stream.get("live"), "E-EVENT-LIVE", "event stream must be live=false")
    if event_stream.get("mode") != "offline-event-protocol":
        raise KernelError("E-EVENT-MODE", "unsupported lifecycle event mode")
    _validate_authority(event_stream.get("authority"), "$events.authority")
    receipt_pointer = _expect_mapping(
        event_stream.get("source_receipt"),
        "E-EVENT-SOURCE-RECEIPT",
        "source_receipt must be an object",
    )
    if receipt_pointer.get("sha256") != sha256_document(source_receipt):
        raise KernelError("E-EVENT-SOURCE-RECEIPT", "source receipt digest mismatch")
    if receipt_pointer.get("sequence") != source_receipt.get("sequence"):
        raise KernelError("E-EVENT-SOURCE-RECEIPT", "source receipt sequence mismatch")

    entries = _expect_list(
        event_stream.get("events"),
        "E-EVENT-STREAM",
        "events must be a list",
    )
    if not entries:
        raise KernelError("E-EVENT-STREAM", "event stream must not be empty")
    previous: str | None = None
    verified: list[dict[str, Any]] = []
    for index, wrapper in enumerate(entries):
        item = _expect_mapping(
            wrapper,
            "E-EVENT-WRAPPER",
            f"events[{index}] must be an object",
        )
        event = _expect_mapping(
            item.get("event"),
            "E-EVENT",
            f"events[{index}].event must be an object",
        )
        digest = _require_digest(
            item.get("event_sha256"),
            "E-EVENT-DIGEST",
            "event_sha256 must be a digest",
        )
        if digest != sha256_document(event):
            raise KernelError("E-EVENT-DIGEST-MISMATCH", f"event {index + 1} digest mismatch")
        sequence = _positive_int(
            event.get("sequence"),
            "E-EVENT-SEQUENCE",
            "event sequence must be positive",
        )
        if sequence != index + 1:
            raise KernelError("E-EVENT-SEQUENCE", "event sequence is not contiguous")
        if event.get("previous_event_sha256") != previous:
            raise KernelError("E-EVENT-PREVIOUS", "event predecessor digest mismatch")
        if event.get("contract") != PRINCIPIA_EVENT_CONTRACT:
            raise KernelError("E-EVENT-CONTRACT", "unsupported lifecycle event contract")
        if event.get("fixture_kind") != "bounded-synthetic":
            raise KernelError("E-EVENT-FIXTURE", "only bounded-synthetic events are accepted")
        if event.get("source_repository") != "Rhodan-lab/Atlas":
            raise KernelError("E-EVENT-SOURCE", "event source repository must be Atlas")
        _require_false(event.get("live"), "E-EVENT-LIVE", "event must be live=false")
        _validate_authority(
            event.get("authority"),
            f"$events.events[{index}].event.authority",
            require_status_rule=True,
        )
        baseline = _expect_mapping(
            event.get("source_baseline"),
            "E-EVENT-BASELINE",
            "source_baseline must be an object",
        )
        if baseline.get("implementation_merge_commit") != ATLAS_IMPLEMENTATION_MERGE:
            raise KernelError("E-EVENT-BASELINE", "event pins wrong Atlas implementation")
        if baseline.get("governance_merge_commit") != ATLAS_GOVERNANCE_MERGE:
            raise KernelError("E-EVENT-BASELINE", "event pins wrong Atlas governance")
        if baseline.get("mode") != "importer-candidate":
            raise KernelError("E-EVENT-BASELINE", "event pins wrong importer mode")
        _require_false(baseline.get("live"), "E-EVENT-BASELINE", "baseline must be live=false")

        subject = _expect_mapping(
            event.get("subject"),
            "E-EVENT-SUBJECT",
            "subject must be an object",
        )
        entity_id = subject.get("id")
        revision = _positive_int(
            subject.get("revision"),
            "E-EVENT-SUBJECT",
            "subject revision must be positive",
        )
        if not isinstance(entity_id, str):
            raise KernelError("E-EVENT-SUBJECT", "subject id must be a string")
        entity = repository.exact(entity_id, revision)
        if subject.get("key") != exact_key(entity_id, revision):
            raise KernelError("E-EVENT-SUBJECT", "subject key mismatch")
        if subject.get("entity_type") != entity.get("type"):
            raise KernelError("E-EVENT-SUBJECT", "subject entity type mismatch")
        transition = _expect_mapping(
            event.get("transition"),
            "E-EVENT-TRANSITION",
            "transition must be an object",
        )
        if transition.get("from") != "current":
            raise KernelError("E-EVENT-TRANSITION", "synthetic transition must start at current")
        target = transition.get("to")
        if target not in _EVENT_TARGETS:
            raise KernelError("E-EVENT-TRANSITION", "unsupported transition target")
        synthetic = _repository_with_transition(repository, entity_id, revision, str(target))
        report = lifecycle_impact_report(
            synthetic,
            entity_id,
            revision,
            imported_records,
        )
        dependents = report.get("external_dependents", [])
        affected = sorted(
            [
                {"id": item.get("id"), "revision": item.get("revision")}
                for item in dependents
            ],
            key=lambda value: (str(value["id"]), int(value["revision"])),
        )
        actions = sorted({str(item.get("effective_action")) for item in dependents})
        if not affected:
            raise KernelError("E-EVENT-NO-DEPENDENTS", "event has no registered external dependents")
        if len(actions) != 1:
            raise KernelError("E-EVENT-ACTION-FANOUT", "event produces mixed required actions")
        verified.append(
            {
                "sequence": sequence,
                "event_id": event.get("event_id"),
                "event_sha256": digest,
                "subject": dict(subject),
                "transition": dict(transition),
                "required_action": actions[0],
                "affected_artifacts": affected,
            }
        )
        previous = digest
    return verified


def _verify_acknowledgements(
    acknowledgement_stream: Mapping[str, Any],
    verified_events: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    if acknowledgement_stream.get("contract") != PRINCIPIA_ACK_STREAM_CONTRACT:
        raise KernelError("E-ACK-STREAM-CONTRACT", "unsupported acknowledgement stream")
    _require_false(
        acknowledgement_stream.get("live"),
        "E-ACK-LIVE",
        "acknowledgement stream must be live=false",
    )
    if acknowledgement_stream.get("mode") != "offline-event-protocol":
        raise KernelError("E-ACK-MODE", "unsupported acknowledgement mode")
    _validate_authority(acknowledgement_stream.get("authority"), "$acks.authority")
    entries = _expect_list(
        acknowledgement_stream.get("acknowledgements"),
        "E-ACK-STREAM",
        "acknowledgements must be a list",
    )
    if len(entries) != len(verified_events):
        raise KernelError("E-ACK-COUNT", "event and acknowledgement counts differ")
    previous: str | None = None
    verified: list[dict[str, Any]] = []
    for index, wrapper in enumerate(entries):
        item = _expect_mapping(
            wrapper,
            "E-ACK-WRAPPER",
            f"acknowledgements[{index}] must be an object",
        )
        acknowledgement = _expect_mapping(
            item.get("acknowledgement"),
            "E-ACK",
            f"acknowledgements[{index}].acknowledgement must be an object",
        )
        digest = _require_digest(
            item.get("acknowledgement_sha256"),
            "E-ACK-DIGEST",
            "acknowledgement_sha256 must be a digest",
        )
        if digest != sha256_document(acknowledgement):
            raise KernelError("E-ACK-DIGEST-MISMATCH", f"acknowledgement {index + 1} digest mismatch")
        expected = verified_events[index]
        sequence = _positive_int(
            acknowledgement.get("sequence"),
            "E-ACK-SEQUENCE",
            "acknowledgement sequence must be positive",
        )
        if sequence != index + 1:
            raise KernelError("E-ACK-SEQUENCE", "acknowledgement sequence is not contiguous")
        if acknowledgement.get("previous_acknowledgement_sha256") != previous:
            raise KernelError("E-ACK-PREVIOUS", "acknowledgement predecessor mismatch")
        if acknowledgement.get("contract") != PRINCIPIA_ACK_CONTRACT:
            raise KernelError("E-ACK-CONTRACT", "unsupported acknowledgement contract")
        if acknowledgement.get("repository") != PRINCIPIA_REPOSITORY:
            raise KernelError("E-ACK-REPOSITORY", "acknowledgement repository mismatch")
        _require_false(acknowledgement.get("live"), "E-ACK-LIVE", "acknowledgement must be live=false")
        for field in (
            "automatic_status_change",
            "automatic_release_action",
            "repository_mutation",
        ):
            _require_false(
                acknowledgement.get(field),
                "E-OFFLINE-AUTOMATIC-MUTATION",
                f"acknowledgement {field} must be false",
            )
        if acknowledgement.get("status_inheritance") != "prohibited":
            raise KernelError("E-OFFLINE-STATUS-INHERITANCE", "acknowledgement status inheritance is prohibited")
        if acknowledgement.get("accepted") is not True:
            raise KernelError("E-ACK-REJECTED", "acknowledgement must be accepted")
        if acknowledgement.get("outcome") != "recorded-no-mutation":
            raise KernelError("E-ACK-OUTCOME", "acknowledgement outcome must be no-mutation")
        if acknowledgement.get("event_id") != expected.get("event_id"):
            raise KernelError("E-ACK-EVENT", "acknowledgement event_id mismatch")
        if acknowledgement.get("event_sha256") != expected.get("event_sha256"):
            raise KernelError("E-ACK-EVENT", "acknowledgement event digest mismatch")
        if acknowledgement.get("required_action") != expected.get("required_action"):
            raise KernelError("E-ACK-ACTION", "acknowledgement weakens or changes required action")
        affected = acknowledgement.get("affected_artifacts")
        if affected != expected.get("affected_artifacts"):
            raise KernelError("E-ACK-AFFECTED", "acknowledgement affected-artifact set mismatch")
        verified.append(
            {
                "sequence": sequence,
                "acknowledgement_id": acknowledgement.get("acknowledgement_id"),
                "acknowledgement_sha256": digest,
                "event_id": acknowledgement.get("event_id"),
                "event_sha256": acknowledgement.get("event_sha256"),
                "required_action": acknowledgement.get("required_action"),
                "affected_artifacts": affected,
            }
        )
        previous = digest
    return verified


def _verify_chain(
    chain: Mapping[str, Any],
    events: Sequence[Mapping[str, Any]],
    acknowledgements: Sequence[Mapping[str, Any]],
) -> None:
    if chain.get("contract") != PRINCIPIA_CHAIN_CONTRACT:
        raise KernelError("E-CHAIN-CONTRACT", "unsupported event-protocol chain")
    _require_false(chain.get("live"), "E-CHAIN-LIVE", "chain must be live=false")
    _validate_authority(chain.get("authority"), "$chain.authority")
    links = _expect_list(chain.get("links"), "E-CHAIN-LINKS", "links must be a list")
    if len(links) != len(events) or len(links) != len(acknowledgements):
        raise KernelError("E-CHAIN-COUNT", "chain link count mismatch")
    for index, link_value in enumerate(links):
        link = _expect_mapping(
            link_value,
            "E-CHAIN-LINK",
            f"links[{index}] must be an object",
        )
        event = events[index]
        acknowledgement = acknowledgements[index]
        expected = {
            "sequence": index + 1,
            "event_id": event.get("event_id"),
            "event_sha256": event.get("event_sha256"),
            "previous_event_sha256": None if index == 0 else events[index - 1].get("event_sha256"),
            "acknowledgement_id": acknowledgement.get("acknowledgement_id"),
            "acknowledgement_sha256": acknowledgement.get("acknowledgement_sha256"),
            "previous_acknowledgement_sha256": (
                None if index == 0 else acknowledgements[index - 1].get("acknowledgement_sha256")
            ),
        }
        if dict(link) != expected:
            raise KernelError("E-CHAIN-LINK", f"chain link {index + 1} mismatch")
    if chain.get("event_head_sequence") != len(events):
        raise KernelError("E-CHAIN-HEAD", "event head sequence mismatch")
    if chain.get("acknowledgement_head_sequence") != len(acknowledgements):
        raise KernelError("E-CHAIN-HEAD", "acknowledgement head sequence mismatch")
    if chain.get("event_head_sha256") != events[-1].get("event_sha256"):
        raise KernelError("E-CHAIN-HEAD", "event head digest mismatch")
    if chain.get("acknowledgement_head_sha256") != acknowledgements[-1].get(
        "acknowledgement_sha256"
    ):
        raise KernelError("E-CHAIN-HEAD", "acknowledgement head digest mismatch")


def _verify_reconciliation(
    reconciliation: Mapping[str, Any],
    event_stream: Mapping[str, Any],
    acknowledgement_stream: Mapping[str, Any],
    chain: Mapping[str, Any],
    events: Sequence[Mapping[str, Any]],
    acknowledgements: Sequence[Mapping[str, Any]],
) -> None:
    if reconciliation.get("contract") != PRINCIPIA_RECONCILIATION_CONTRACT:
        raise KernelError("E-RECONCILIATION-CONTRACT", "unsupported reconciliation report")
    _require_false(
        reconciliation.get("live"),
        "E-RECONCILIATION-LIVE",
        "reconciliation must be live=false",
    )
    if reconciliation.get("mode") != "offline-reconciliation-simulation":
        raise KernelError("E-RECONCILIATION-MODE", "unsupported reconciliation mode")
    _validate_authority(
        reconciliation.get("authority"),
        "$reconciliation.authority",
        require_status_rule=True,
    )
    source = _expect_mapping(
        reconciliation.get("source"),
        "E-RECONCILIATION-SOURCE",
        "source must be an object",
    )
    if source.get("events_sha256") != sha256_document(event_stream):
        raise KernelError("E-RECONCILIATION-SOURCE", "event stream digest mismatch")
    if source.get("acknowledgements_sha256") != sha256_document(acknowledgement_stream):
        raise KernelError("E-RECONCILIATION-SOURCE", "acknowledgement stream digest mismatch")
    if source.get("chain_sha256") != sha256_document(chain):
        raise KernelError("E-RECONCILIATION-SOURCE", "chain digest mismatch")

    records = _expect_list(
        reconciliation.get("records"),
        "E-RECONCILIATION-RECORDS",
        "records must be a list",
    )
    if len(records) != len(events):
        raise KernelError("E-RECONCILIATION-COUNT", "reconciliation record count mismatch")
    for index, record_value in enumerate(records):
        record = _expect_mapping(
            record_value,
            "E-RECONCILIATION-RECORD",
            f"records[{index}] must be an object",
        )
        event = events[index]
        acknowledgement = acknowledgements[index]
        for field in ("sequence", "event_id", "event_sha256", "subject", "transition", "required_action"):
            if record.get(field) != event.get(field):
                raise KernelError("E-RECONCILIATION-EVENT", f"record {index + 1} {field} mismatch")
        if record.get("acknowledgement_id") != acknowledgement.get("acknowledgement_id"):
            raise KernelError("E-RECONCILIATION-ACK", "acknowledgement id mismatch")
        if record.get("acknowledgement_sha256") != acknowledgement.get(
            "acknowledgement_sha256"
        ):
            raise KernelError("E-RECONCILIATION-ACK", "acknowledgement digest mismatch")
        if record.get("result") != "reconciled":
            raise KernelError("E-RECONCILIATION-RESULT", "record must be reconciled")
        affected = _expect_list(
            record.get("affected_artifacts"),
            "E-RECONCILIATION-AFFECTED",
            "affected_artifacts must be a list",
        )
        expected_affected = acknowledgement.get("affected_artifacts")
        simplified: list[dict[str, Any]] = []
        for item in affected:
            artifact = _expect_mapping(
                item,
                "E-RECONCILIATION-AFFECTED",
                "affected artifact must be an object",
            )
            artifact_id = artifact.get("artifact_id")
            acknowledged_revision = artifact.get("acknowledged_revision")
            current_revision = artifact.get("current_revision")
            if acknowledged_revision != current_revision:
                raise KernelError("E-RECONCILIATION-STALE", f"artifact {artifact_id!r} is stale")
            if artifact.get("reconciliation_state") != "current":
                raise KernelError("E-RECONCILIATION-STALE", f"artifact {artifact_id!r} is not current")
            simplified.append({"id": artifact_id, "revision": acknowledged_revision})
        if simplified != expected_affected:
            raise KernelError("E-RECONCILIATION-AFFECTED", "reconciled affected-artifact set mismatch")

    summary = _expect_mapping(
        reconciliation.get("summary"),
        "E-RECONCILIATION-SUMMARY",
        "summary must be an object",
    )
    expected_summary = {
        "event_count": len(events),
        "acknowledgement_count": len(acknowledgements),
        "reconciled_count": len(records),
        "unacknowledged_count": 0,
        "orphan_acknowledgement_count": 0,
        "stale_artifact_reference_count": 0,
        "action_mismatch_count": 0,
        "decision": "reconciled-no-mutation",
    }
    if dict(summary) != expected_summary:
        raise KernelError("E-RECONCILIATION-SUMMARY", "reconciliation summary mismatch")


def audit_offline_protocol(
    batch: Mapping[str, Any],
    principia_receipt: Mapping[str, Any],
    event_stream: Mapping[str, Any],
    acknowledgement_stream: Mapping[str, Any],
    chain: Mapping[str, Any],
    reconciliation: Mapping[str, Any],
    export_documents: Mapping[str, bytes],
    repository: KernelRepository,
) -> dict[str, Any]:
    """Re-import and audit the full pinned Principia Phase 16-18 evidence chain."""
    atlas_receipt = import_offline_batch(batch, export_documents, repository)
    receipt_verification = verify_principia_receipt(batch, principia_receipt, atlas_receipt)
    imported_records = atlas_receipt["records"]
    events = _verify_event_stream(
        event_stream,
        principia_receipt,
        imported_records,
        repository,
    )
    acknowledgements = _verify_acknowledgements(acknowledgement_stream, events)
    _verify_chain(chain, events, acknowledgements)
    _verify_reconciliation(
        reconciliation,
        event_stream,
        acknowledgement_stream,
        chain,
        events,
        acknowledgements,
    )
    return {
        "contract": ATLAS_PROTOCOL_AUDIT_CONTRACT,
        "source_contracts": {
            "batch": PRINCIPIA_BATCH_CONTRACT,
            "receipt": PRINCIPIA_RECEIPT_CONTRACT,
            "event_stream": PRINCIPIA_EVENT_STREAM_CONTRACT,
            "acknowledgement_stream": PRINCIPIA_ACK_STREAM_CONTRACT,
            "chain": PRINCIPIA_CHAIN_CONTRACT,
            "reconciliation": PRINCIPIA_RECONCILIATION_CONTRACT,
        },
        "mode": "offline-protocol-audit-candidate",
        "live": False,
        "batch_id": batch.get("batch_id"),
        "record_count": atlas_receipt.get("record_count"),
        "event_count": len(events),
        "acknowledgement_count": len(acknowledgements),
        "reconciled_count": len(reconciliation.get("records", [])),
        "receipt_verified": receipt_verification.get("verified"),
        "decision": "verified-no-mutation",
        "fixture_kind": "bounded-synthetic",
        "status_inheritance": "prohibited",
        "automatic_status_change": False,
        "automatic_release_action": False,
        "repository_mutation": False,
    }
