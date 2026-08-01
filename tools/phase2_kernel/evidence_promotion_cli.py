#!/usr/bin/env python3
"""Build a deterministic review packet for one offline Principia evidence candidate."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .compiler import compile_canonical
from .evidence_bridge import validate_reference_snapshot
from .evidence_promotion import build_evidence_promotion_packet
from .evidence_registry import validate_evidence_registry
from .evidence_review import load_review_index
from .kernel import KernelError, load_json, render_json
from .repository import KernelRepository

DEFAULT_REGISTRY = Path(
    "content/fixtures/phase2_bridge/accepted-evidence-registry.v01.json"
)
DEFAULT_REVIEW_ROOT = Path("content/reviews/ai")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--submission-basis", required=True)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--review-root", type=Path, default=DEFAULT_REVIEW_ROOT)
    parser.add_argument("--runtime", type=Path)
    parser.add_argument(
        "--canonical-root", type=Path, default=Path("content/canonical")
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=Path("."),
        help="repository root used to resolve registry and candidate snapshot paths",
    )
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = args.repository_root.resolve()
        registry_path = args.registry
        if not registry_path.is_absolute():
            registry_path = root / registry_path
        candidate_path = args.candidate
        if candidate_path.is_absolute():
            raise KernelError(
                "E-EVIDENCE-PROMOTION-PATH",
                "candidate must be a repository-relative path",
            )
        candidate_file = root / candidate_path

        registry_payload = load_json(registry_path)
        candidate_payload = load_json(candidate_file)
        registry = validate_evidence_registry(registry_payload)
        candidate = validate_reference_snapshot(candidate_payload)
        entries = [
            entry
            for entry in registry["entries"]
            if entry["route_id"] == candidate["route_id"]
        ]
        if len(entries) != 1:
            raise KernelError(
                "E-EVIDENCE-PROMOTION-ROUTE",
                f"registry must contain exactly one baseline for route {candidate['route_id']!r}",
            )
        baseline_relative = Path(entries[0]["snapshot_path"])
        baseline_file = root / baseline_relative
        baseline_payload = load_json(baseline_file)

        runtime = (
            load_json(args.runtime)
            if args.runtime
            else compile_canonical(args.canonical_root)
        )
        packet = build_evidence_promotion_packet(
            registry_payload,
            baseline_payload,
            candidate_payload,
            KernelRepository(runtime),
            load_review_index(args.review_root),
            baseline_snapshot_path=baseline_relative.as_posix(),
            candidate_snapshot_path=candidate_path.as_posix(),
            submission_basis=args.submission_basis,
            registry_bytes=registry_path.read_bytes(),
            baseline_snapshot_bytes=baseline_file.read_bytes(),
            candidate_snapshot_bytes=candidate_file.read_bytes(),
        )
        rendered = render_json(packet)
        if args.output is None:
            sys.stdout.write(rendered)
        else:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
            print(f"wrote={args.output}")
        return 0
    except (KernelError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
