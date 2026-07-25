from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .parser import IngestError, compile_directory, load_notes, summaries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="atlas-ingest",
        description="Compile structured Markdown notes into a deterministic Atlas graph.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build = subparsers.add_parser("build", help="compile a note directory")
    build.add_argument("input", type=Path)
    build.add_argument("--output", "-o", type=Path, required=True)

    validate = subparsers.add_parser("validate", help="validate notes without writing output")
    validate.add_argument("input", type=Path)

    inspect = subparsers.add_parser("inspect", help="show deterministic IDs and titles")
    inspect.add_argument("input", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "build":
            document = compile_directory(args.input, args.output)
            print(
                f"compiled {document.concept_count} concepts and "
                f"{document.relation_count} relations -> {args.output}"
            )
        elif args.command == "validate":
            document = load_notes(args.input)
            print(f"valid: {document.concept_count} concepts, {document.relation_count} relations")
        elif args.command == "inspect":
            document = load_notes(args.input)
            print("\n".join(summaries(document)))
        else:  # pragma: no cover - argparse enforces the command set
            raise AssertionError(f"unsupported command: {args.command}")
    except (IngestError, OSError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
