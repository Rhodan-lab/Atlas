#!/usr/bin/env python3
"""Scaled synthetic-corpus and offline receipt-replay validation for Atlas Phase 2."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import platform
import statistics
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from .bridge import import_principia_candidate, lifecycle_impact_report
from .compiler import compile_canonical
from .kernel import KernelError, load_json, render_json
from .offline_protocol import (
    import_offline_batch,
    load_snapshot_documents,
    sha256_document,
)
from .repository import KernelRepository

SCALE_PROFILE_CONTRACT = "atlas-phase2-scale-profile/0.1"
SCALED_BENCHMARK_CONTRACT = "atlas-kernel-scaled-benchmark/0.1"
RECEIPT_LEDGER_CONTRACT = "atlas-principia-offline-receipt-ledger/0.1"
REPLAY_RESULT_CONTRACT = "atlas-principia-offline-replay-result/0.1"
REPLAY_MATRIX_CONTRACT = "atlas-principia-offline-replay-matrix/0.1"
MODE = "scale-replay-candidate"

SCALED_BUDGETS_MS = {
    "compile": 20000.0,
    "runtime_admission": 5000.0,
    "exact_lookup": 10.0,
    "provenance": 150.0,
    "bridge_import_all": 10000.0,
    "impact_all": 10000.0,
}


def _measure(operation: Callable[[], object], iterations: int) -> dict[str, float | int]:
    if iterations < 1:
        raise KernelError("E-SCALE-ITERATIONS", "iterations must be positive")
    operation()
    durations: list[float] = []
    for _ in range(iterations):
        started = time.perf_counter_ns()
        operation()
        durations.append((time.perf_counter_ns() - started) / 1_000_000.0)
    ordered = sorted(durations)
    p95_index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * 0.95) - 1))
    return {
        "iterations": iterations,
        "median_ms": round(statistics.median(ordered), 6),
        "p95_ms": round(ordered[p95_index], 6),
        "max_ms": round(max(ordered), 6),
    }


def _write_document(path: Path, metadata: Mapping[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    front_matter = json.dumps(dict(metadata), sort_keys=True, ensure_ascii=True)
    path.write_text(f"---\n{front_matter}\n---\n{body}\n", encoding="utf-8")


def write_synthetic_corpus(root: Path, groups: int) -> dict[str, Any]:
    """Write a deterministic, isolated canonical corpus for scale measurements."""
    if groups < 1:
        raise KernelError("E-SCALE-GROUPS", "groups must be positive")
    root.mkdir(parents=True, exist_ok=True)
    source_root = "src:synthetic-scale-root"
    concept_root = "concept:en:synthetic-scale-root"
    _write_document(
        root / "root" / "source.md",
        {
            "contract": "atlas-content/0.1",
            "id": source_root,
            "revision": 1,
            "title": "Synthetic scale root source",
            "type": "source",
        },
        "Deterministic synthetic source used only for Phase 2 scale testing.",
    )
    _write_document(
        root / "root" / "concept.md",
        {
            "contract": "atlas-content/0.1",
            "id": concept_root,
            "revision": 1,
            "source": source_root,
            "title": "Synthetic scale root concept",
            "type": "concept",
        },
        "Synthetic root concept.",
    )

    synthesis_keys: list[str] = []
    claim_keys: list[str] = []
    for index in range(1, groups + 1):
        token = f"{index:06d}"
        source_id = f"src:synthetic-scale-{token}"
        concept_id = f"concept:en:synthetic-scale-{token}"
        claim_id = f"claim:en:synthetic-scale-{token}"
        synthesis_id = f"synthesis:en:synthetic-scale-{token}"
        group = root / f"group-{token}"
        _write_document(
            group / "source.md",
            {
                "contract": "atlas-content/0.1",
                "id": source_id,
                "revision": 1,
                "title": f"Synthetic source {token}",
                "type": "source",
            },
            f"Synthetic source {token}.",
        )
        _write_document(
            group / "concept.md",
            {
                "contract": "atlas-content/0.1",
                "id": concept_id,
                "parent": concept_root,
                "revision": 1,
                "source": source_id,
                "title": f"Synthetic concept {token}",
                "type": "concept",
            },
            f"Synthetic concept {token}.",
        )
        _write_document(
            group / "claim.md",
            {
                "concept": concept_id,
                "contract": "atlas-content/0.1",
                "id": claim_id,
                "revision": 1,
                "title": f"Synthetic claim {token}",
                "type": "claim",
            },
            f"Synthetic claim {token}.",
        )
        _write_document(
            group / "synthesis.md",
            {
                "claim": claim_id,
                "contract": "atlas-content/0.1",
                "id": synthesis_id,
                "relations": [
                    {
                        "note": "Synthetic provenance edge.",
                        "target": claim_id,
                        "type": "derived-from",
                    }
                ],
                "revision": 1,
                "title": f"Synthetic synthesis {token}",
                "type": "synthesis",
            },
            f"Synthetic synthesis {token}.",
        )
        claim_keys.append(f"{claim_id}@1")
        synthesis_keys.append(f"{synthesis_id}@1")

    return {
        "groups": groups,
        "entity_count": 2 + 4 * groups,
        "root_concept": f"{concept_root}@1",
        "last_claim": claim_keys[-1],
        "last_synthesis": synthesis_keys[-1],
    }


def synthetic_principia_payload(index: int) -> dict[str, Any]:
    if index < 1:
        raise KernelError("E-SCALE-DEPENDENT", "external dependent index must be positive")
    token = f"{index:06d}"
    claim_id = f"claim:en:synthetic-scale-{token}"
    root_id = "concept:en:synthetic-scale-root"
    return {
        "atlas_content_contract": "atlas-content/0.1",
        "bridge_mode": "bridge-candidate",
        "contract": "principia-atlas-external-dependent/0.2",
        "depends_on": [claim_id, root_id],
        "depends_on_exact": [
            {
                "change_policy": "block-release",
                "entity_type": "claim",
                "id": claim_id,
                "revision": 1,
                "role": "load-bearing",
                "use": "claim-boundary",
            },
            {
                "change_policy": "inspect",
                "entity_type": "concept",
                "id": root_id,
                "revision": 1,
                "role": "context",
                "use": "definition",
            },
        ],
        "id": f"principia:artifact:synthetic-scale-{token}",
        "kind": "principia-artifact",
        "live": False,
        "repository": "Rhodan-lab/principle-to-system",
        "revision": 1,
        "role": "load-bearing",
    }


def _split_exact(value: str) -> tuple[str, int]:
    entity_id, separator, revision = value.rpartition("@")
    if not separator or not revision.isdigit():
        raise KernelError("E-SCALE-EXACT", "expected ENTITY_ID@REVISION")
    return entity_id, int(revision)


def run_scaled_benchmark(profile: Mapping[str, Any]) -> dict[str, Any]:
    if profile.get("contract") != SCALE_PROFILE_CONTRACT:
        raise KernelError("E-SCALE-PROFILE", "unsupported scale profile contract")
    if profile.get("mode") != MODE or profile.get("live") is not False:
        raise KernelError("E-SCALE-PROFILE", "scale profile must remain non-live")
    groups = profile.get("groups")
    dependents = profile.get("external_dependents")
    compile_iterations = profile.get("compile_iterations")
    operation_iterations = profile.get("operation_iterations")
    for value, name in (
        (groups, "groups"),
        (dependents, "external_dependents"),
        (compile_iterations, "compile_iterations"),
        (operation_iterations, "operation_iterations"),
    ):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            raise KernelError("E-SCALE-PROFILE", f"{name} must be a positive integer")
    if dependents > groups:
        raise KernelError("E-SCALE-PROFILE", "external_dependents cannot exceed groups")

    with tempfile.TemporaryDirectory(prefix="atlas-phase2-scale-") as temporary:
        root = Path(temporary) / "canonical"
        identity = write_synthetic_corpus(root, groups)
        compile_metric = _measure(lambda: compile_canonical(root), compile_iterations)
        runtime_a = compile_canonical(root)
        runtime_b = compile_canonical(root)
        if render_json(runtime_a) != render_json(runtime_b):
            raise KernelError("E-SCALE-DETERMINISM", "scaled runtime compilation drifted")
        admission_metric = _measure(lambda: KernelRepository(runtime_a), operation_iterations)
        repository = KernelRepository(runtime_a)
        payloads = [synthetic_principia_payload(index) for index in range(1, dependents + 1)]
        imported = [import_principia_candidate(payload, repository) for payload in payloads]
        lookup_id, lookup_revision = _split_exact(identity["last_claim"])
        provenance_id, provenance_revision = _split_exact(identity["last_synthesis"])

        metrics = {
            "compile": compile_metric,
            "runtime_admission": admission_metric,
            "exact_lookup": _measure(
                lambda: repository.exact(lookup_id, lookup_revision), operation_iterations
            ),
            "provenance": _measure(
                lambda: repository.provenance_sources(provenance_id, provenance_revision),
                operation_iterations,
            ),
            "bridge_import_all": _measure(
                lambda: [import_principia_candidate(payload, repository) for payload in payloads],
                operation_iterations,
            ),
            "impact_all": _measure(
                lambda: lifecycle_impact_report(
                    repository,
                    "concept:en:synthetic-scale-root",
                    1,
                    imported,
                ),
                operation_iterations,
            ),
        }
        impact = lifecycle_impact_report(
            repository,
            "concept:en:synthetic-scale-root",
            1,
            imported,
        )
        if len(impact["external_dependents"]) != dependents:
            raise KernelError("E-SCALE-FANOUT", "scaled impact fan-out is incomplete")
        return {
            "budgets_ms": SCALED_BUDGETS_MS,
            "contract": SCALED_BENCHMARK_CONTRACT,
            "deterministic_runtime": True,
            "entity_count": runtime_a["entity_count"],
            "external_dependent_count": dependents,
            "groups": groups,
            "live": False,
            "metrics": metrics,
            "mode": MODE,
            "mutation": False,
            "platform": platform.platform(),
            "python": platform.python_version(),
            "runtime_source_digest": runtime_a["source_digest"],
        }


def enforce_scaled_budgets(report: Mapping[str, Any]) -> None:
    metrics = report.get("metrics")
    if not isinstance(metrics, Mapping):
        raise KernelError("E-SCALE-BUDGET", "scaled benchmark metrics are missing")
    failures: list[str] = []
    for name, budget in SCALED_BUDGETS_MS.items():
        metric = metrics.get(name)
        p95 = metric.get("p95_ms") if isinstance(metric, Mapping) else None
        if not isinstance(p95, (int, float)):
            failures.append(f"{name}: missing p95_ms")
        elif p95 > budget:
            failures.append(f"{name}: p95 {p95:.6f} ms exceeds {budget:.3f} ms")
    if failures:
        raise KernelError("E-SCALE-BUDGET", "; ".join(failures))


def new_receipt_ledger() -> dict[str, Any]:
    return {
        "automatic_release_action": False,
        "automatic_status_change": False,
        "contract": RECEIPT_LEDGER_CONTRACT,
        "entries": [],
        "head_receipt_sha256": None,
        "head_sequence": 0,
        "live": False,
        "mode": MODE,
        "repository_mutation": False,
    }


def validate_receipt_ledger(ledger: Mapping[str, Any]) -> dict[str, Any]:
    if ledger.get("contract") != RECEIPT_LEDGER_CONTRACT:
        raise KernelError("E-REPLAY-LEDGER-CONTRACT", "unsupported receipt ledger contract")
    if ledger.get("mode") != MODE or ledger.get("live") is not False:
        raise KernelError("E-REPLAY-LEDGER-MODE", "receipt ledger must remain non-live")
    for field in ("automatic_release_action", "automatic_status_change", "repository_mutation"):
        if ledger.get(field) is not False:
            raise KernelError("E-REPLAY-MUTATION", f"{field} must remain false")
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        raise KernelError("E-REPLAY-LEDGER", "entries must be a list")
    previous: str | None = None
    batch_ids: set[str] = set()
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, Mapping):
            raise KernelError("E-REPLAY-LEDGER", "ledger entry must be an object")
        receipt = entry.get("receipt")
        if not isinstance(receipt, Mapping):
            raise KernelError("E-REPLAY-LEDGER", "ledger entry receipt must be an object")
        if entry.get("sequence") != index or receipt.get("sequence") != index:
            raise KernelError("E-REPLAY-LEDGER-SEQUENCE", "ledger sequences must be contiguous")
        if receipt.get("previous_receipt_sha256") != previous:
            raise KernelError("E-REPLAY-LEDGER-PREDECESSOR", "ledger predecessor chain is invalid")
        digest = sha256_document(receipt)
        if entry.get("receipt_sha256") != digest:
            raise KernelError("E-REPLAY-LEDGER-DIGEST", "ledger receipt digest mismatch")
        batch_id = receipt.get("batch_id")
        if not isinstance(batch_id, str) or batch_id in batch_ids:
            raise KernelError("E-REPLAY-LEDGER-BATCH", "ledger batch IDs must be unique")
        batch_ids.add(batch_id)
        previous = digest
    if ledger.get("head_sequence") != len(entries):
        raise KernelError("E-REPLAY-LEDGER-HEAD", "head_sequence does not match entries")
    if ledger.get("head_receipt_sha256") != previous:
        raise KernelError("E-REPLAY-LEDGER-HEAD", "head receipt digest does not match entries")
    return {
        "contract": RECEIPT_LEDGER_CONTRACT,
        "entry_count": len(entries),
        "head_receipt_sha256": previous,
        "head_sequence": len(entries),
        "live": False,
        "mode": MODE,
        "mutation": False,
    }


def apply_offline_batch(
    ledger: Mapping[str, Any],
    batch: Mapping[str, Any],
    export_documents: Mapping[str, bytes],
    repository: KernelRepository,
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_receipt_ledger(ledger)
    receipt = import_offline_batch(batch, export_documents, repository)
    receipt_digest = sha256_document(receipt)
    sequence = receipt["sequence"]
    entries = ledger["entries"]
    for entry in entries:
        if entry["sequence"] == sequence:
            if entry["receipt_sha256"] == receipt_digest:
                unchanged = copy.deepcopy(dict(ledger))
                return unchanged, {
                    "contract": REPLAY_RESULT_CONTRACT,
                    "decision": "idempotent-no-op",
                    "ledger_head_receipt_sha256": ledger["head_receipt_sha256"],
                    "ledger_head_sequence": ledger["head_sequence"],
                    "live": False,
                    "mutation": False,
                    "receipt_sha256": receipt_digest,
                    "sequence": sequence,
                }
            raise KernelError("E-REPLAY-CONFLICT", "same sequence has a different receipt digest")
    if any(entry["receipt"]["batch_id"] == receipt["batch_id"] for entry in entries):
        raise KernelError("E-REPLAY-BATCH-ID", "batch ID was already accepted at another sequence")
    expected = ledger["head_sequence"] + 1
    if sequence < expected:
        raise KernelError("E-REPLAY-STALE", f"sequence {sequence} is behind expected {expected}")
    if sequence > expected:
        raise KernelError("E-REPLAY-SKIPPED", f"sequence {sequence} skips expected {expected}")
    if receipt["previous_receipt_sha256"] != ledger["head_receipt_sha256"]:
        raise KernelError("E-REPLAY-PREDECESSOR", "batch predecessor does not match ledger head")
    updated = copy.deepcopy(dict(ledger))
    updated["entries"].append(
        {
            "receipt": receipt,
            "receipt_sha256": receipt_digest,
            "sequence": sequence,
        }
    )
    updated["head_sequence"] = sequence
    updated["head_receipt_sha256"] = receipt_digest
    validate_receipt_ledger(updated)
    return updated, {
        "contract": REPLAY_RESULT_CONTRACT,
        "decision": "accepted",
        "ledger_head_receipt_sha256": receipt_digest,
        "ledger_head_sequence": sequence,
        "live": False,
        "mutation": False,
        "receipt_sha256": receipt_digest,
        "sequence": sequence,
    }


def continued_batch(
    baseline: Mapping[str, Any],
    *,
    sequence: int,
    previous_receipt_sha256: str | None,
    batch_id: str,
    input_count: int | None = None,
) -> dict[str, Any]:
    batch = copy.deepcopy(dict(baseline))
    batch["batch_id"] = batch_id
    batch["sequence"] = sequence
    batch["previous_receipt_sha256"] = previous_receipt_sha256
    if input_count is not None:
        batch["inputs"] = batch["inputs"][:input_count]
    return batch


def _expect_error(
    name: str,
    expected: str,
    operation: Callable[[], object],
) -> dict[str, str]:
    try:
        operation()
    except KernelError as exc:
        if exc.code != expected:
            raise KernelError(
                "E-REPLAY-MATRIX",
                f"{name} expected {expected}, got {exc.code}",
            ) from exc
        return {"case": name, "error": exc.code, "decision": "rejected"}
    raise KernelError("E-REPLAY-MATRIX", f"{name} unexpectedly succeeded")


def run_replay_recovery_matrix(
    baseline_batch: Mapping[str, Any],
    export_documents: Mapping[str, bytes],
    repository: KernelRepository,
) -> dict[str, Any]:
    ledger0 = new_receipt_ledger()
    ledger1, first = apply_offline_batch(ledger0, baseline_batch, export_documents, repository)
    replayed, replay = apply_offline_batch(ledger1, baseline_batch, export_documents, repository)
    if render_json(ledger1) != render_json(replayed):
        raise KernelError("E-REPLAY-IDEMPOTENCE", "exact replay changed the ledger")
    batch2 = continued_batch(
        baseline_batch,
        sequence=2,
        previous_receipt_sha256=ledger1["head_receipt_sha256"],
        batch_id="principia-atlas:offline-batch:thermal-control:0002",
        input_count=2,
    )
    ledger2, second = apply_offline_batch(ledger1, batch2, export_documents, repository)

    skipped = continued_batch(
        baseline_batch,
        sequence=4,
        previous_receipt_sha256=ledger2["head_receipt_sha256"],
        batch_id="principia-atlas:offline-batch:thermal-control:0004",
        input_count=2,
    )
    conflict = continued_batch(
        baseline_batch,
        sequence=2,
        previous_receipt_sha256=ledger1["head_receipt_sha256"],
        batch_id="principia-atlas:offline-batch:thermal-control:conflict",
        input_count=3,
    )
    wrong_predecessor = continued_batch(
        baseline_batch,
        sequence=3,
        previous_receipt_sha256="0" * 64,
        batch_id="principia-atlas:offline-batch:thermal-control:0003",
        input_count=2,
    )
    duplicate_batch_id = continued_batch(
        baseline_batch,
        sequence=3,
        previous_receipt_sha256=ledger2["head_receipt_sha256"],
        batch_id=batch2["batch_id"],
        input_count=2,
    )
    corrupted_ledger = copy.deepcopy(ledger2)
    corrupted_ledger["entries"][0]["receipt_sha256"] = "f" * 64

    rejected = [
        _expect_error(
            "skipped-sequence",
            "E-REPLAY-SKIPPED",
            lambda: apply_offline_batch(ledger2, skipped, export_documents, repository),
        ),
        _expect_error(
            "conflicting-sequence",
            "E-REPLAY-CONFLICT",
            lambda: apply_offline_batch(ledger2, conflict, export_documents, repository),
        ),
        _expect_error(
            "wrong-predecessor",
            "E-REPLAY-PREDECESSOR",
            lambda: apply_offline_batch(ledger2, wrong_predecessor, export_documents, repository),
        ),
        _expect_error(
            "duplicate-batch-id",
            "E-REPLAY-BATCH-ID",
            lambda: apply_offline_batch(ledger2, duplicate_batch_id, export_documents, repository),
        ),
        _expect_error(
            "corrupted-ledger",
            "E-REPLAY-LEDGER-DIGEST",
            lambda: validate_receipt_ledger(corrupted_ledger),
        ),
    ]
    return {
        "accepted_sequences": [first["sequence"], second["sequence"]],
        "automatic_release_action": False,
        "automatic_status_change": False,
        "contract": REPLAY_MATRIX_CONTRACT,
        "decision": "verified-no-mutation",
        "final_head_receipt_sha256": ledger2["head_receipt_sha256"],
        "final_head_sequence": ledger2["head_sequence"],
        "idempotent_replay": replay["decision"] == "idempotent-no-op",
        "live": False,
        "mode": MODE,
        "rejected_cases": rejected,
        "repository_mutation": False,
    }


def _write_report(report: Mapping[str, Any], output: Path | None) -> None:
    rendered = render_json(report)
    if output is None:
        sys.stdout.write(rendered)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"wrote={output}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    benchmark = subparsers.add_parser("benchmark", help="run the scaled synthetic benchmark")
    benchmark.add_argument("--profile", type=Path, required=True)
    benchmark.add_argument("--output", type=Path)
    benchmark.add_argument("--enforce", action="store_true")
    replay = subparsers.add_parser("replay-matrix", help="run the offline receipt replay matrix")
    replay.add_argument(
        "--snapshot",
        type=Path,
        default=Path("content/fixtures/phase2_protocol/principia-phase18.snapshot.json"),
    )
    replay.add_argument(
        "--batch",
        type=Path,
        default=Path("content/fixtures/phase2_protocol/thermal-control.multi-artifact.batch.v02.json"),
    )
    replay.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    replay.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "benchmark":
            report = run_scaled_benchmark(load_json(args.profile))
            if args.enforce:
                enforce_scaled_budgets(report)
            _write_report(report, args.output)
            return 0
        _, documents = load_snapshot_documents(args.snapshot)
        repository = KernelRepository(compile_canonical(args.canonical_root))
        report = run_replay_recovery_matrix(load_json(args.batch), documents, repository)
        _write_report(report, args.output)
        return 0
    except (KernelError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
