#!/usr/bin/env python3
"""Generate and verify bounded Phase 1 machine review attestations.

This tool creates only review records that the current promotion policy permits a
machine to satisfy: structural conformance and fully specified reproducibility.
It never grants human accountability, permits promotion, changes lifecycle state,
or produces domain, methodological, editorial, source, ethical, legal, conflict,
or translation authority.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

import phase1_review_gate as gate

REVIEW_DATE = "2026-07-26"
RECORDS_DIR = REPO_ROOT / "content" / "reviews" / "records"

EXPECTED_SEQUENCE = [1, 0, -1, -1, 0, 1, 1, 0]


@dataclass(frozen=True)
class AttestationSpec:
    filename: str
    review_id: str
    entity_id: str
    revision: int
    review_type: str
    reviewer_name: str
    qualification: str
    summary: str
    metadata: dict[str, Any]


STRUCTURAL_ENTITIES = [
    (
        "feedback-question-structural-machine.json",
        "review:structural:feedback-question-r1:2026-07-26",
        "question:en:when-delayed-correction-can-oscillate",
        "content/canonical/feedback/question-delayed-correction.md",
    ),
    (
        "feedback-source-reference-structural-machine.json",
        "review:structural:feedback-source-reference-r1:2026-07-26",
        "src:astrom-murray-2008-feedback-systems",
        "content/canonical/feedback/source-astrom-murray-2008.md",
    ),
    (
        "feedback-source-synthetic-structural-machine.json",
        "review:structural:feedback-source-synthetic-r1:2026-07-26",
        "src:synthetic-feedback-run-delay-one-gain-one",
        "content/canonical/feedback/source-synthetic-model-run.md",
    ),
    (
        "feedback-evidence-sequence-structural-machine.json",
        "review:structural:feedback-evidence-sequence-r1:2026-07-26",
        "evidence:en:delayed-feedback-periodic-sequence",
        "content/canonical/feedback/evidence-periodic-sequence.md",
    ),
    (
        "feedback-claim-oscillation-structural-machine.json",
        "review:structural:feedback-claim-oscillation-r1:2026-07-26",
        "claim:en:stated-delayed-recurrence-oscillates",
        "content/canonical/feedback/claim-recurrence-oscillates.md",
    ),
    (
        "feedback-claim-inference-boundary-structural-machine.json",
        "review:structural:feedback-claim-inference-boundary-r1:2026-07-26",
        "claim:en:model-oscillation-does-not-prove-real-system",
        "content/canonical/feedback/claim-model-does-not-prove-real-system.md",
    ),
    (
        "feedback-concept-feedback-structural-machine.json",
        "review:structural:feedback-concept-feedback-r1:2026-07-26",
        "concept:en:feedback",
        "content/canonical/feedback/concept-feedback.md",
    ),
    (
        "feedback-concept-oscillation-structural-machine.json",
        "review:structural:feedback-concept-oscillation-r1:2026-07-26",
        "concept:en:oscillation",
        "content/canonical/feedback/concept-oscillation.md",
    ),
    (
        "feedback-model-structural-machine.json",
        "review:structural:feedback-model-r1:2026-07-26",
        "model:en:delayed-correction-recurrence",
        "content/canonical/feedback/model-delayed-correction.md",
    ),
    (
        "feedback-synthesis-structural-machine.json",
        "review:structural:feedback-synthesis-r1:2026-07-26",
        "synthesis:en:delayed-feedback-and-oscillation",
        "content/canonical/feedback/synthesis-delayed-feedback.md",
    ),
]

REPRODUCIBILITY_ENTITIES = [
    (
        "feedback-claim-oscillation-reproducibility-machine.json",
        "review:reproducibility:feedback-claim-oscillation-r1:2026-07-26",
        "claim:en:stated-delayed-recurrence-oscillates",
    ),
    (
        "feedback-evidence-sequence-reproducibility-machine.json",
        "review:reproducibility:feedback-evidence-sequence-r1:2026-07-26",
        "evidence:en:delayed-feedback-periodic-sequence",
    ),
    (
        "feedback-model-reproducibility-machine.json",
        "review:reproducibility:feedback-model-r1:2026-07-26",
        "model:en:delayed-correction-recurrence",
    ),
]


def recalculate_sequence() -> list[int]:
    values = [1, 0]
    for _ in range(6):
        values.append(values[-1] - values[-2])
    return values


def specs() -> tuple[AttestationSpec, ...]:
    result: list[AttestationSpec] = []
    structural_command = (
        "python tools/foundation-validator/atlas_foundation_validator.py "
        "validate content/canonical"
    )
    for filename, review_id, entity_id, canonical_path in STRUCTURAL_ENTITIES:
        result.append(
            AttestationSpec(
                filename=filename,
                review_id=review_id,
                entity_id=entity_id,
                revision=1,
                review_type="structural",
                reviewer_name="Atlas Foundation Validator",
                qualification="Deterministic atlas-content/0.1 structural validation",
                summary=(
                    "The exact revision passed the repository's deterministic "
                    "atlas-content/0.1 structural validation. This attestation "
                    "does not judge scientific meaning or permit promotion."
                ),
                metadata={
                    "generator": "phase1_machine_attestations.py",
                    "canonical_path": canonical_path,
                    "procedure": structural_command,
                    "result": "pass",
                    "authority_limit": "structural conformance only",
                },
            )
        )

    reproduction_metadata = {
        "generator": "phase1_machine_attestations.py",
        "procedure": "recalculate x[t+1] = x[t] - x[t-1] from x0=1 and x1=0",
        "inputs": {"x0": 1, "x1": 0, "gain": 1, "delay_steps": 1},
        "steps": 8,
        "observed_sequence": EXPECTED_SEQUENCE,
        "result": "pass",
        "authority_limit": "fully specified arithmetic fixture only",
    }
    for filename, review_id, entity_id in REPRODUCIBILITY_ENTITIES:
        result.append(
            AttestationSpec(
                filename=filename,
                review_id=review_id,
                entity_id=entity_id,
                revision=1,
                review_type="reproducibility",
                reviewer_name="Atlas Feedback Reproducibility Check",
                qualification="Deterministic recurrence recalculation for a fully specified fixture",
                summary=(
                    "The exact delayed-feedback sequence was recalculated from "
                    "the stated recurrence, parameters, and initial values. "
                    "This does not establish behavior of any real system or "
                    "permit promotion."
                ),
                metadata=dict(reproduction_metadata),
            )
        )
    return tuple(result)


def record_for(spec: AttestationSpec) -> dict[str, Any]:
    return {
        "contract": gate.REVIEW_CONTRACT,
        "id": spec.review_id,
        "entity": {"id": spec.entity_id, "revision": spec.revision},
        "review_type": spec.review_type,
        "reviewer": {
            "display_name": spec.reviewer_name,
            "kind": "machine",
            "independence": "not-applicable",
            "qualification": spec.qualification,
            "accountable": False,
            "conflicts": [],
        },
        "completed_at": REVIEW_DATE,
        "review_horizon": None,
        "outcome": "pass",
        "findings": [],
        "summary": spec.summary,
        "permits_promotion": False,
        "metadata": spec.metadata,
    }


def expected_records() -> dict[str, dict[str, Any]]:
    sequence = recalculate_sequence()
    if sequence != EXPECTED_SEQUENCE:
        raise RuntimeError(
            f"feedback recurrence changed: expected {EXPECTED_SEQUENCE}, got {sequence}"
        )
    records = {spec.filename: record_for(spec) for spec in specs()}
    for filename, record in records.items():
        diagnostics = gate.validate_review_record(record, filename)
        if diagnostics:
            messages = "; ".join(f"{item.code}: {item.message}" for item in diagnostics)
            raise RuntimeError(f"invalid generated record {filename}: {messages}")
    return records


def write_records(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for filename, record in expected_records().items():
        (directory / filename).write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def check_records(directory: Path) -> list[str]:
    failures: list[str] = []
    for filename, expected in expected_records().items():
        path = directory / filename
        try:
            actual = json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            failures.append(f"{filename}: {exc}")
            continue
        except json.JSONDecodeError as exc:
            failures.append(f"{filename}: invalid JSON: {exc}")
            continue
        if actual != expected:
            failures.append(f"{filename}: committed record differs from deterministic output")
    return failures


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["generate", "check", "print"])
    parser.add_argument("--records-dir", type=Path, default=RECORDS_DIR)
    args = parser.parse_args(argv)

    if args.command == "generate":
        write_records(args.records_dir)
        print(f"generated {len(expected_records())} machine attestations")
        return 0
    if args.command == "check":
        failures = check_records(args.records_dir)
        for failure in failures:
            print(failure, file=sys.stderr)
        if failures:
            return 1
        print(f"verified {len(expected_records())} deterministic machine attestations")
        return 0

    print(
        json.dumps(
            {name: record for name, record in expected_records().items()},
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
