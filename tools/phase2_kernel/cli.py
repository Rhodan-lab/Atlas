#!/usr/bin/env python3
"""Command-line interface for the Atlas Phase 2 knowledge kernel."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .bridge import import_principia_candidate, lifecycle_impact_report
from .compiler import compile_canonical
from .kernel import (
    KernelError,
    KernelRepository,
    load_json,
    render_json,
)


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

    lookup_parser = subparsers.add_parser(
        "lookup", help="read one exact entity revision"
    )
    lookup_parser.add_argument("exact_reference")
    lookup_parser.add_argument("--runtime", type=Path)
    lookup_parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )

    provenance_parser = subparsers.add_parser(
        "provenance", help="trace an entity to source entities"
    )
    provenance_parser.add_argument("exact_reference")
    provenance_parser.add_argument("--runtime", type=Path)
    provenance_parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )

    bridge_validate = subparsers.add_parser(
        "bridge-validate", help="validate and normalize a Principia export"
    )
    bridge_validate.add_argument("export", type=Path)
    bridge_validate.add_argument("--runtime", type=Path)
    bridge_validate.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )

    bridge_import = subparsers.add_parser(
        "bridge-import", help="write a normalized external-dependent record"
    )
    bridge_import.add_argument("export", type=Path)
    bridge_import.add_argument("--output", type=Path, required=True)
    bridge_import.add_argument("--runtime", type=Path)
    bridge_import.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )

    impact = subparsers.add_parser(
        "impact", help="report internal and external lifecycle impact"
    )
    impact.add_argument("exact_reference")
    impact.add_argument("--external", type=Path, action="append", default=[])
    impact.add_argument("--runtime", type=Path)
    impact.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )
    impact.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "compile":
            _write_or_print(compile_canonical(args.canonical_root), args.output)
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
        return 0
    except KernelError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
