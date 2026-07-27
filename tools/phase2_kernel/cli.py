#!/usr/bin/env python3
"""Command-line interface for the Atlas Phase 2 knowledge kernel."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .bridge import import_principia_candidate, lifecycle_impact_report
from .compiler import compile_canonical
from .kernel import KernelError, load_json, render_json
from .offline_protocol_policy import (
    audit_pinned_offline_protocol,
    import_pinned_offline_batch,
    load_pinned_snapshot_documents,
)
from .repository import KernelRepository, validate_runtime

PROTOCOL_FIXTURES = Path("content/fixtures/phase2_protocol")


def _write_or_print(payload: dict[str, object], output: Path | None) -> None:
    rendered = render_json(payload)
    if output is None:
        sys.stdout.write(rendered)
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"wrote={output}")


def _repository(runtime: Path | None, canonical_root: Path) -> KernelRepository:
    payload = load_json(runtime) if runtime else compile_canonical(canonical_root)
    return KernelRepository(payload)


def _split_exact(value: str) -> tuple[str, int]:
    entity_id, separator, revision = value.rpartition("@")
    if not separator or not revision.isdigit() or int(revision) < 1:
        raise KernelError("E-EXACT-REFERENCE", "expected ENTITY_ID@REVISION")
    return entity_id, int(revision)


def _add_repository_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--runtime", type=Path)
    parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )


def _add_protocol_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=PROTOCOL_FIXTURES / "principia-phase18.snapshot.json",
    )
    parser.add_argument(
        "--batch",
        type=Path,
        default=PROTOCOL_FIXTURES / "thermal-control.multi-artifact.batch.v02.json",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    compile_parser = subparsers.add_parser(
        "compile", help="compile canonical Markdown deterministically"
    )
    compile_parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )
    compile_parser.add_argument("--output", type=Path)

    runtime_validate = subparsers.add_parser(
        "runtime-validate",
        help="strictly validate a serialized Atlas runtime before query use",
    )
    runtime_validate.add_argument("runtime", type=Path)
    runtime_validate.add_argument("--output", type=Path)

    lookup_parser = subparsers.add_parser(
        "lookup", help="read one exact entity revision"
    )
    lookup_parser.add_argument("exact_reference")
    _add_repository_arguments(lookup_parser)

    provenance_parser = subparsers.add_parser(
        "provenance", help="trace an entity to source entities"
    )
    provenance_parser.add_argument("exact_reference")
    _add_repository_arguments(provenance_parser)

    bridge_validate = subparsers.add_parser(
        "bridge-validate", help="validate and normalize a Principia export"
    )
    bridge_validate.add_argument("export", type=Path)
    _add_repository_arguments(bridge_validate)

    bridge_import = subparsers.add_parser(
        "bridge-import", help="write a normalized external-dependent record"
    )
    bridge_import.add_argument("export", type=Path)
    bridge_import.add_argument("--output", type=Path, required=True)
    _add_repository_arguments(bridge_import)

    impact = subparsers.add_parser(
        "impact", help="report internal and external lifecycle impact"
    )
    impact.add_argument("exact_reference")
    impact.add_argument("--external", type=Path, action="append", default=[])
    _add_repository_arguments(impact)
    impact.add_argument("--output", type=Path)

    offline_batch = subparsers.add_parser(
        "offline-batch-import",
        help="atomically re-import the pinned Principia multi-artifact batch",
    )
    _add_protocol_arguments(offline_batch)
    _add_repository_arguments(offline_batch)
    offline_batch.add_argument("--output", type=Path)

    offline_audit = subparsers.add_parser(
        "offline-protocol-audit",
        help="audit the pinned Principia batch, events, acknowledgements, and reconciliation",
    )
    _add_protocol_arguments(offline_audit)
    _add_repository_arguments(offline_audit)
    offline_audit.add_argument(
        "--receipt",
        type=Path,
        default=PROTOCOL_FIXTURES / "thermal-control.multi-artifact.receipt.v02.json",
    )
    offline_audit.add_argument(
        "--events",
        type=Path,
        default=PROTOCOL_FIXTURES / "thermal-control.lifecycle-events.v01.json",
    )
    offline_audit.add_argument(
        "--acknowledgements",
        type=Path,
        default=PROTOCOL_FIXTURES
        / "thermal-control.lifecycle-acknowledgements.v01.json",
    )
    offline_audit.add_argument(
        "--chain",
        type=Path,
        default=PROTOCOL_FIXTURES / "thermal-control.event-protocol-chain.v01.json",
    )
    offline_audit.add_argument(
        "--reconciliation",
        type=Path,
        default=PROTOCOL_FIXTURES / "thermal-control.reconciliation-report.v01.json",
    )
    offline_audit.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "compile":
            _write_or_print(compile_canonical(args.canonical_root), args.output)
            return 0
        if args.command == "runtime-validate":
            _write_or_print(validate_runtime(load_json(args.runtime)), args.output)
            return 0
        repository = _repository(args.runtime, args.canonical_root)
        if args.command == "lookup":
            entity_id, revision = _split_exact(args.exact_reference)
            _write_or_print(repository.exact(entity_id, revision), None)
        elif args.command == "provenance":
            entity_id, revision = _split_exact(args.exact_reference)
            _write_or_print(
                {
                    "contract": "atlas-provenance-report/0.1",
                    "entity": args.exact_reference,
                    "sources": repository.provenance_sources(entity_id, revision),
                },
                None,
            )
        elif args.command in {"bridge-validate", "bridge-import"}:
            imported = import_principia_candidate(load_json(args.export), repository)
            if args.command == "bridge-validate":
                print(
                    f"bridge=pass; artifact={imported['id']}@{imported['revision']}; "
                    f"dependencies={len(imported['dependencies'])}; "
                    f"source-contract={imported['source_contract']}; live=false"
                )
            else:
                _write_or_print(imported, args.output)
        elif args.command == "impact":
            entity_id, revision = _split_exact(args.exact_reference)
            external = [load_json(path) for path in args.external]
            _write_or_print(
                lifecycle_impact_report(
                    repository, entity_id, revision, external
                ),
                args.output,
            )
        elif args.command == "offline-batch-import":
            _, documents = load_pinned_snapshot_documents(args.snapshot)
            receipt = import_pinned_offline_batch(
                load_json(args.batch),
                documents,
                repository,
            )
            _write_or_print(receipt, args.output)
        elif args.command == "offline-protocol-audit":
            snapshot, documents = load_pinned_snapshot_documents(args.snapshot)
            report = audit_pinned_offline_protocol(
                snapshot,
                load_json(args.batch),
                load_json(args.receipt),
                load_json(args.events),
                load_json(args.acknowledgements),
                load_json(args.chain),
                load_json(args.reconciliation),
                documents,
                repository,
            )
            _write_or_print(report, args.output)
        return 0
    except (KernelError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
