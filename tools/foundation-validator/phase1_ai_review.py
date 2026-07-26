#!/usr/bin/env python3
"""Validate an explicitly non-human comprehensive Atlas AI review.

The contract records reasoning, source checks, mathematical verification, findings,
and exact entity revisions. It does not claim human identity or professional
accountability. Human verification is an optional stronger layer, not a Phase 1 gate.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

CONTRACT = "atlas-ai-review/0.1"
ID_RE = re.compile(r"^ai-review:[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_DIMENSIONS = {
    "structural",
    "editorial",
    "source",
    "domain",
    "methodological",
    "reproducibility",
    "ethical",
    "legal-context",
}
ALLOWED_OUTCOMES = {"pass", "pass-with-minor-findings", "blocked"}
ALLOWED_FINDING_SEVERITIES = {"critical", "major", "minor", "info"}
ALLOWED_FINDING_STATUSES = {"open", "resolved", "accepted-risk"}
EXPECTED_ENTITIES = {
    "question:en:when-delayed-correction-can-oscillate": 1,
    "src:astrom-murray-2008-feedback-systems": 2,
    "src:synthetic-feedback-run-delay-one-gain-one": 1,
    "evidence:en:delayed-feedback-periodic-sequence": 2,
    "claim:en:stated-delayed-recurrence-oscillates": 2,
    "claim:en:model-oscillation-does-not-prove-real-system": 1,
    "concept:en:feedback": 1,
    "concept:en:oscillation": 1,
    "model:en:delayed-correction-recurrence": 2,
    "synthesis:en:delayed-feedback-and-oscillation": 2,
}


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"path": self.path, "code": self.code, "message": self.message}


def _diag(path: str, code: str, message: str) -> Diagnostic:
    return Diagnostic(path, code, message)


def load_json(path: Path) -> Mapping[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("AI review must be a JSON object")
    return payload


def _frontmatter(path: Path) -> Mapping[str, Any] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    payload = yaml.safe_load(text[4:end])
    return payload if isinstance(payload, dict) else None


def canonical_index(root: Path) -> dict[str, tuple[int, str]]:
    result: dict[str, tuple[int, str]] = {}
    for path in sorted(root.rglob("*.md")):
        meta = _frontmatter(path)
        if not meta:
            continue
        entity_id = meta.get("id")
        revision = meta.get("revision")
        if isinstance(entity_id, str) and isinstance(revision, int):
            if entity_id in result:
                raise ValueError(f"duplicate canonical entity ID: {entity_id}")
            result[entity_id] = (revision, str(path))
    return result


def validate_review(
    review: Mapping[str, Any], canonical_root: Path
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    if review.get("contract") != CONTRACT:
        diagnostics.append(_diag("review", "E-AI-CONTRACT", f"contract must be {CONTRACT}"))
    review_id = review.get("id")
    if not isinstance(review_id, str) or not ID_RE.fullmatch(review_id):
        diagnostics.append(_diag("review", "E-AI-ID", "review id is not canonical"))

    scope = review.get("scope")
    if not isinstance(scope, dict) or scope.get("language") != "en":
        diagnostics.append(_diag("review", "E-AI-SCOPE", "English scope is required"))

    reviewer = review.get("reviewer")
    if not isinstance(reviewer, dict):
        diagnostics.append(_diag("review", "E-AI-REVIEWER", "reviewer mapping is required"))
        reviewer = {}
    if reviewer.get("kind") != "ai":
        diagnostics.append(_diag("reviewer", "E-AI-KIND", "reviewer.kind must be ai"))
    if reviewer.get("human_verified") is not False:
        diagnostics.append(
            _diag("reviewer", "E-AI-HUMAN-CLAIM", "human_verified must be false")
        )
    if not isinstance(reviewer.get("display_name"), str) or not reviewer.get("display_name", "").strip():
        diagnostics.append(_diag("reviewer", "E-AI-NAME", "reviewer display name is required"))
    if not isinstance(reviewer.get("limitations"), list) or not reviewer.get("limitations"):
        diagnostics.append(_diag("reviewer", "E-AI-LIMITATIONS", "reviewer limitations are required"))

    source = review.get("source_verification")
    if not isinstance(source, dict):
        diagnostics.append(_diag("source_verification", "E-AI-SOURCE", "source verification is required"))
        source = {}
    if source.get("locator") != "https://authors.library.caltech.edu/records/yzs24-xsx88":
        diagnostics.append(_diag("source_verification", "E-AI-SOURCE-LOCATOR", "unexpected source locator"))
    matched = source.get("matched")
    if not isinstance(matched, list) or len(matched) < 6:
        diagnostics.append(_diag("source_verification", "E-AI-SOURCE-FIELDS", "source verification is incomplete"))

    math = review.get("mathematical_verification")
    if not isinstance(math, dict):
        diagnostics.append(_diag("mathematical_verification", "E-AI-MATH", "mathematical verification is required"))
        math = {}
    if math.get("states_x0_through_x7") != [1, 0, -1, -1, 0, 1, 1, 0]:
        diagnostics.append(_diag("mathematical_verification", "E-AI-SEQUENCE", "incorrect recurrence sequence"))
    if math.get("state_pair_start") != [0, 1] or math.get("state_pair_return") != [0, 1]:
        diagnostics.append(_diag("mathematical_verification", "E-AI-PAIR", "ordered state-pair return is incorrect"))
    if math.get("return_step_difference") != 6 or math.get("period") != 6:
        diagnostics.append(_diag("mathematical_verification", "E-AI-PERIOD", "exact period must be 6"))
    if not isinstance(math.get("proof"), str) or not math.get("proof", "").strip():
        diagnostics.append(_diag("mathematical_verification", "E-AI-PROOF", "period proof is required"))

    entities = review.get("entities")
    if not isinstance(entities, list):
        diagnostics.append(_diag("entities", "E-AI-ENTITIES", "entities must be a list"))
        entities = []
    seen: dict[str, int] = {}
    for index, item in enumerate(entities):
        path = f"entities[{index}]"
        if not isinstance(item, dict):
            diagnostics.append(_diag(path, "E-AI-ENTITY", "entity review must be a mapping"))
            continue
        entity_id = item.get("id")
        revision = item.get("revision")
        if not isinstance(entity_id, str) or not isinstance(revision, int):
            diagnostics.append(_diag(path, "E-AI-ENTITY-ID", "entity id and revision are required"))
            continue
        if entity_id in seen:
            diagnostics.append(_diag(path, "E-AI-ENTITY-DUPLICATE", f"duplicate entity {entity_id}"))
        seen[entity_id] = revision
        dimensions = item.get("dimensions")
        if not isinstance(dimensions, list) or not dimensions:
            diagnostics.append(_diag(path, "E-AI-DIMENSIONS", "review dimensions are required"))
        else:
            unknown = sorted(set(dimensions) - ALLOWED_DIMENSIONS)
            if unknown:
                diagnostics.append(_diag(path, "E-AI-DIMENSION", f"unsupported dimensions: {unknown}"))
        if item.get("outcome") not in ALLOWED_OUTCOMES:
            diagnostics.append(_diag(path, "E-AI-OUTCOME", "unsupported entity outcome"))
        if not isinstance(item.get("summary"), str) or not item.get("summary", "").strip():
            diagnostics.append(_diag(path, "E-AI-SUMMARY", "entity summary is required"))

    if seen != EXPECTED_ENTITIES:
        missing = sorted(set(EXPECTED_ENTITIES) - set(seen))
        extra = sorted(set(seen) - set(EXPECTED_ENTITIES))
        wrong = sorted(
            entity_id for entity_id in set(seen) & set(EXPECTED_ENTITIES)
            if seen[entity_id] != EXPECTED_ENTITIES[entity_id]
        )
        diagnostics.append(
            _diag("entities", "E-AI-ENTITY-SET", f"entity mismatch; missing={missing}; extra={extra}; wrong_revision={wrong}")
        )

    try:
        canonical = canonical_index(canonical_root)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        diagnostics.append(_diag(str(canonical_root), "E-AI-CANONICAL", str(exc)))
        canonical = {}
    for entity_id, expected_revision in EXPECTED_ENTITIES.items():
        actual = canonical.get(entity_id)
        if actual is None:
            diagnostics.append(_diag(entity_id, "E-AI-CANONICAL-MISSING", "canonical entity is missing"))
        elif actual[0] != expected_revision:
            diagnostics.append(
                _diag(entity_id, "E-AI-CANONICAL-REVISION", f"expected revision {expected_revision}, found {actual[0]}")
            )

    findings = review.get("findings")
    if not isinstance(findings, list):
        diagnostics.append(_diag("findings", "E-AI-FINDINGS", "findings must be a list"))
        findings = []
    finding_ids: set[str] = set()
    for index, finding in enumerate(findings):
        path = f"findings[{index}]"
        if not isinstance(finding, dict):
            diagnostics.append(_diag(path, "E-AI-FINDING", "finding must be a mapping"))
            continue
        finding_id = finding.get("id")
        if not isinstance(finding_id, str):
            diagnostics.append(_diag(path, "E-AI-FINDING-ID", "finding id is required"))
        else:
            finding_ids.add(finding_id)
        if finding.get("severity") not in ALLOWED_FINDING_SEVERITIES:
            diagnostics.append(_diag(path, "E-AI-FINDING-SEVERITY", "unsupported severity"))
        if finding.get("status") not in ALLOWED_FINDING_STATUSES:
            diagnostics.append(_diag(path, "E-AI-FINDING-STATUS", "unsupported status"))
        if finding.get("status") == "resolved" and not isinstance(finding.get("resolution"), str):
            diagnostics.append(_diag(path, "E-AI-FINDING-RESOLUTION", "resolved finding needs a resolution"))

    required_findings = {
        "finding:feedback:periodicity-proof",
        "finding:feedback:oscillation-instability-distinction",
        "finding:feedback:source-scope",
    }
    if not required_findings.issubset(finding_ids):
        diagnostics.append(_diag("findings", "E-AI-FINDING-SET", "required review findings are missing"))
    if any(isinstance(item, dict) and item.get("status") == "open" and item.get("severity") in {"critical", "major"} for item in findings):
        diagnostics.append(_diag("findings", "E-AI-OPEN-SERIOUS", "serious findings remain open"))

    if review.get("overall_outcome") != "pass":
        diagnostics.append(_diag("review", "E-AI-OVERALL", "overall outcome must be pass"))
    if review.get("review_level") != "ai-reviewed":
        diagnostics.append(_diag("review", "E-AI-LEVEL", "review level must be ai-reviewed"))
    if review.get("human_review_required") is not False:
        diagnostics.append(_diag("review", "E-AI-HUMAN-DUTY", "human_review_required must be false"))

    return sorted(set(diagnostics))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", type=Path)
    parser.add_argument("--canonical-root", type=Path, default=Path("content/canonical"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    try:
        review = load_json(args.review)
        diagnostics = validate_review(review, args.canonical_root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        diagnostics = [_diag(str(args.review), "E-AI-LOAD", str(exc))]

    if diagnostics:
        if args.json:
            print(json.dumps([item.to_dict() for item in diagnostics], indent=2, sort_keys=True))
        else:
            for item in diagnostics:
                print(f"ERROR {item.code} {item.path}: {item.message}")
        return 1

    print("ai-review=pass; entities=10; exact-period=6; human-review-required=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
