#!/usr/bin/env python3
"""Deterministic validator for the Atlas Phase 0 authored-content contract.

This tool checks conformance only. It does not judge scientific truth, rewrite
content, assign confidence, or grant review status.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

SUPPORTED_CONTRACT = "atlas-content/0.1"
ENTITY_TYPES = {
    "source",
    "evidence",
    "claim",
    "concept",
    "model",
    "question",
    "synthesis",
}
LIFECYCLE_STATUSES = {
    "draft",
    "in-review",
    "reviewed",
    "contested",
    "deprecated",
    "retracted",
}
STALENESS_STATES = {
    "current",
    "possibly-stale",
    "review-required",
    "confirmed-stale",
    "unaffected",
    "updated",
}
CLAIM_KINDS = {
    "factual",
    "descriptive",
    "causal",
    "correlational",
    "definitional",
    "methodological",
    "interpretive",
    "predictive",
    "normative",
    "hypothetical",
    "model-derived",
}
CONFIDENCE_LABELS = {
    "uncertain",
    "plausible",
    "well-supported",
    "strongly-supported",
}
ACCESS_CLASSES = {
    "open",
    "public-locator",
    "licensed",
    "private",
    "sensitive",
    "unavailable",
    "ephemeral",
}
REVIEW_TYPES = {
    "structural",
    "editorial",
    "source",
    "domain",
    "methodological",
    "reproducibility",
    "ethical",
    "translation",
}
RELATION_PAIRS: dict[str, set[tuple[str, str]]] = {
    "part-of": {("concept", "concept"), ("model", "model")},
    "instance-of": {("concept", "concept"), ("model", "concept")},
    "prerequisite-of": {("concept", "concept"), ("model", "model")},
    "supports": {("evidence", "claim")},
    "challenges": {("evidence", "claim"), ("claim", "claim")},
    "contradicts": {("claim", "claim")},
    "contextualizes": {
        ("evidence", "claim"),
        ("concept", "claim"),
        ("source", "synthesis"),
    },
    "illustrates": {("evidence", "concept"), ("concept", "concept")},
    "motivates": {
        ("source", "question"),
        ("evidence", "question"),
        ("claim", "question"),
        ("concept", "question"),
    },
    "replicates": {("evidence", "evidence"), ("evidence", "claim")},
    "fails-to-replicate": {("evidence", "evidence"), ("evidence", "claim")},
    "explains": {
        ("concept", "concept"),
        ("model", "claim"),
        ("model", "concept"),
        ("claim", "concept"),
    },
    "derived-from": {
        ("claim", "model"),
        ("synthesis", "claim"),
        ("evidence", "source"),
        ("evidence", "model"),
    },
    "refines": {
        ("claim", "claim"),
        ("concept", "concept"),
        ("model", "model"),
        ("question", "question"),
        ("synthesis", "synthesis"),
    },
    "supersedes": {
        ("source", "source"),
        ("evidence", "evidence"),
        ("claim", "claim"),
        ("concept", "concept"),
        ("model", "model"),
        ("question", "question"),
        ("synthesis", "synthesis"),
    },
    "causes": {
        ("concept", "concept"),
        ("claim", "claim"),
    },
    "correlates-with": {
        ("concept", "concept"),
        ("claim", "claim"),
    },
    "measured-by": {("concept", "model"), ("claim", "model")},
    "applies-to": {
        ("model", "concept"),
        ("concept", "concept"),
        ("synthesis", "question"),
    },
    "analogous-to": {("concept", "concept"), ("model", "model")},
}

COMMON_FIELDS = {
    "contract",
    "id",
    "work",
    "type",
    "title",
    "status",
    "revision",
    "created",
    "updated",
    "language",
    "tags",
    "aliases",
    "relations",
    "review",
    "review_horizon",
    "translation_of",
    "translation",
    "staleness",
    "depends_on",
    "verification",
}
TYPE_FIELDS: dict[str, set[str]] = {
    "source": {"source", "access", "limitations", "conflicts"},
    "evidence": {
        "source",
        "locator",
        "access",
        "measurement",
        "transformation",
        "integrity",
        "excerpt",
        "appraisal",
        "synthetic",
    },
    "claim": {
        "claim",
        "model",
        "values",
        "argument",
        "limitations",
        "confidence_rationale",
    },
    "concept": {
        "definition",
        "claims",
        "models",
        "questions",
        "boundaries",
        "examples",
        "limitations",
    },
    "model": {
        "purpose",
        "formal_structure",
        "inputs",
        "outputs",
        "parameters",
        "assumptions",
        "validation",
        "failure_modes",
        "stages",
        "latent_variable",
        "observed_proxies",
        "limitations",
    },
    "question": {
        "state",
        "question",
        "scope",
        "resolution_criteria",
        "related",
        "limitations",
    },
    "synthesis": {
        "question",
        "claims",
        "models",
        "evidence_selection",
        "conclusion",
        "confidence",
        "confidence_rationale",
        "disagreements",
        "open_questions",
        "revision_triggers",
        "argument",
        "scope",
        "audience",
        "limitations",
    },
}

CANONICAL_ID_RE = re.compile(
    r"^(?:src:[a-z0-9]+(?:-[a-z0-9]+)*|"
    r"(?:evidence|claim|concept|model|question|synthesis):[a-z]{2,3}:"
    r"[a-z0-9]+(?:-[a-z0-9]+)*)$"
)
WORK_ID_RE = re.compile(r"^work:[a-z0-9]+(?:-[a-z0-9]+)*$")
LANGUAGE_RE = re.compile(r"^[a-z]{2,3}(?:-[A-Z]{2})?$")


class DuplicateKeyError(ValueError):
    """Raised when YAML contains a duplicate mapping key."""


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise DuplicateKeyError(f"duplicate YAML key: {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


@dataclass(frozen=True, order=True)
class Diagnostic:
    path: str
    code: str
    severity: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
        }


@dataclass(frozen=True)
class Document:
    path: str
    metadata: dict[str, Any]
    body: str = ""

    @property
    def entity_id(self) -> str | None:
        value = self.metadata.get("id")
        return value if isinstance(value, str) else None

    @property
    def entity_type(self) -> str | None:
        value = self.metadata.get("type")
        return value if isinstance(value, str) else None


def _diag(path: str, code: str, message: str, severity: str = "error") -> Diagnostic:
    return Diagnostic(path=path, code=code, severity=severity, message=message)


def parse_markdown(path: Path) -> tuple[Document | None, list[Diagnostic]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [_diag(str(path), "E-FILE-READ", str(exc))]
    return parse_markdown_text(text, str(path))


def parse_markdown_text(text: str, path: str) -> tuple[Document | None, list[Diagnostic]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, [_diag(path, "E-FRONT-MATTER-MISSING", "file must start with '---'")]

    closing: int | None = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing = index
            break
    if closing is None:
        return None, [_diag(path, "E-FRONT-MATTER-UNCLOSED", "missing closing '---'")]

    raw_yaml = "\n".join(lines[1:closing])
    body = "\n".join(lines[closing + 1 :]).strip()
    try:
        metadata = yaml.load(raw_yaml, Loader=UniqueKeyLoader)
    except DuplicateKeyError as exc:
        return None, [_diag(path, "E-YAML-DUPLICATE-KEY", str(exc))]
    except yaml.YAMLError as exc:
        return None, [_diag(path, "E-YAML-PARSE", str(exc))]

    if not isinstance(metadata, dict):
        return None, [_diag(path, "E-FRONT-MATTER-TYPE", "front matter must be a mapping")]
    return Document(path=path, metadata=metadata, body=body), []


def _entity_type_from_id(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    prefix = value.split(":", 1)[0]
    return "source" if prefix == "src" else prefix if prefix in ENTITY_TYPES else None


def _is_date_like(value: Any) -> bool:
    return isinstance(value, (str, date)) and bool(str(value).strip())


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _iter_reference_values(metadata: Mapping[str, Any]) -> Iterable[tuple[str, Any]]:
    for field in ("claims", "models", "questions", "depends_on", "related"):
        for value in _as_list(metadata.get(field)):
            yield field, value
    question = metadata.get("question")
    if isinstance(question, str) and question.startswith("question:"):
        yield "question", question


def validate_document(
    document: Document,
    corpus: Mapping[str, Document],
) -> list[Diagnostic]:
    path = document.path
    meta = document.metadata
    diagnostics: list[Diagnostic] = []

    contract = meta.get("contract")
    if contract is None:
        diagnostics.append(_diag(path, "E-CONTRACT-MISSING", "contract is required"))
    elif contract != SUPPORTED_CONTRACT:
        diagnostics.append(
            _diag(path, "E-CONTRACT-UNSUPPORTED", f"unsupported contract {contract!r}")
        )

    entity_id = meta.get("id")
    if not isinstance(entity_id, str) or not CANONICAL_ID_RE.fullmatch(entity_id):
        diagnostics.append(
            _diag(path, "E-ID-NONCANONICAL", "id must be a stable canonical string")
        )

    entity_type = meta.get("type")
    if entity_type not in ENTITY_TYPES:
        diagnostics.append(_diag(path, "E-TYPE-UNSUPPORTED", f"unsupported type {entity_type!r}"))
        entity_type = None
    elif _entity_type_from_id(entity_id) != entity_type:
        diagnostics.append(
            _diag(path, "E-ID-TYPE-MISMATCH", "id prefix does not match entity type")
        )

    work = meta.get("work")
    if not isinstance(work, str) or not WORK_ID_RE.fullmatch(work):
        diagnostics.append(_diag(path, "E-WORK-ID", "work must be a stable work:* identifier"))

    title = meta.get("title")
    if not isinstance(title, str) or not title.strip():
        diagnostics.append(_diag(path, "E-TITLE-MISSING", "title is required"))

    status = meta.get("status")
    if status not in LIFECYCLE_STATUSES:
        diagnostics.append(_diag(path, "E-STATUS-UNSUPPORTED", f"unsupported status {status!r}"))

    revision = meta.get("revision")
    if not isinstance(revision, int) or revision < 1:
        diagnostics.append(_diag(path, "E-REVISION", "revision must be a positive integer"))

    for field in ("created", "updated"):
        if not _is_date_like(meta.get(field)):
            diagnostics.append(_diag(path, "E-DATE-MISSING", f"{field} is required"))

    language = meta.get("language")
    if not isinstance(language, str) or not LANGUAGE_RE.fullmatch(language):
        diagnostics.append(_diag(path, "E-LANGUAGE", "language must be a BCP-47-like code"))

    if entity_type:
        allowed = COMMON_FIELDS | TYPE_FIELDS[entity_type]
        for key in sorted(set(meta) - allowed):
            diagnostics.append(_diag(path, "E-FIELD-UNKNOWN", f"unknown field {key!r}"))

    staleness = meta.get("staleness")
    if staleness is not None and staleness not in STALENESS_STATES:
        diagnostics.append(_diag(path, "E-STALENESS", f"unsupported staleness {staleness!r}"))

    review = meta.get("review")
    if status == "reviewed":
        if not isinstance(review, dict):
            diagnostics.append(
                _diag(path, "E-REVIEW-RECORD-MISSING", "reviewed item requires review record")
            )
        else:
            if review.get("entity_revision") != revision:
                diagnostics.append(
                    _diag(
                        path,
                        "E-REVIEW-REVISION-MISMATCH",
                        "review.entity_revision must equal authored revision",
                    )
                )
            review_types = set(_as_list(review.get("types")))
            unknown_types = sorted(review_types - REVIEW_TYPES)
            if unknown_types:
                diagnostics.append(
                    _diag(path, "E-REVIEW-TYPE", f"unsupported review types: {unknown_types}")
                )

    translation_of = meta.get("translation_of")
    if translation_of is not None:
        translation = meta.get("translation")
        if not isinstance(translation_of, str):
            diagnostics.append(_diag(path, "E-TRANSLATION-REFERENCE", "translation_of must be an ID"))
        elif translation_of not in corpus:
            diagnostics.append(
                _diag(path, "E-REFERENCE-MISSING", f"translation source {translation_of!r} not found")
            )
        if not isinstance(translation, dict):
            diagnostics.append(_diag(path, "E-TRANSLATION-METADATA", "translation metadata is required"))
        else:
            if not isinstance(translation.get("source_revision"), int):
                diagnostics.append(
                    _diag(path, "E-TRANSLATION-SOURCE-REVISION", "source_revision is required")
                )
            method = translation.get("method")
            if method == "machine" and status != "draft":
                diagnostics.append(
                    _diag(
                        path,
                        "W-AI-ASSISTED-DRAFT-REQUIRED",
                        "machine translation must remain draft until independent review",
                        severity="warning",
                    )
                )
        if status == "reviewed":
            review_types = set(_as_list(review.get("types"))) if isinstance(review, dict) else set()
            if "translation" not in review_types:
                diagnostics.append(
                    _diag(
                        path,
                        "E-TRANSLATION-REVIEW-MISSING",
                        "reviewed translation requires translation review",
                    )
                )

    relations = meta.get("relations")
    if relations is not None:
        if not isinstance(relations, list):
            diagnostics.append(_diag(path, "E-RELATION-STRUCTURE", "relations must be a list"))
        else:
            seen_edges: set[tuple[str, str]] = set()
            for index, relation in enumerate(relations):
                if not isinstance(relation, dict):
                    diagnostics.append(
                        _diag(path, "E-RELATION-STRUCTURE", f"relation {index} must be a mapping")
                    )
                    continue
                relation_type = relation.get("type")
                target = relation.get("target")
                if relation_type not in RELATION_PAIRS:
                    diagnostics.append(
                        _diag(path, "E-RELATION-UNKNOWN", f"unknown relation {relation_type!r}")
                    )
                    continue
                if not isinstance(target, str):
                    diagnostics.append(
                        _diag(path, "E-RELATION-TARGET", f"relation {index} requires target ID")
                    )
                    continue
                edge_key = (relation_type, target)
                if edge_key in seen_edges:
                    diagnostics.append(
                        _diag(path, "E-RELATION-DUPLICATE", f"duplicate relation {edge_key}")
                    )
                seen_edges.add(edge_key)
                target_type = _entity_type_from_id(target)
                if entity_type and target_type and (entity_type, target_type) not in RELATION_PAIRS[relation_type]:
                    diagnostics.append(
                        _diag(
                            path,
                            "E-RELATION-PAIR",
                            f"{relation_type} does not allow {entity_type} -> {target_type}",
                        )
                    )
                if target not in corpus:
                    diagnostics.append(
                        _diag(path, "E-REFERENCE-MISSING", f"relation target {target!r} not found")
                    )
                if relation_type in {"supports", "derived-from", "supersedes"} and not relation.get("note"):
                    diagnostics.append(
                        _diag(
                            path,
                            "W-RELATION-RATIONALE-MISSING",
                            f"{relation_type} should include a rationale note",
                            severity="warning",
                        )
                    )

    for field, reference in _iter_reference_values(meta):
        if isinstance(reference, str) and reference not in corpus:
            diagnostics.append(
                _diag(path, "E-REFERENCE-MISSING", f"{field} reference {reference!r} not found")
            )

    if entity_type == "source":
        source_meta = meta.get("source")
        if not isinstance(source_meta, dict):
            diagnostics.append(_diag(path, "E-SOURCE-METADATA", "source metadata is required"))
        else:
            if not isinstance(source_meta.get("title"), str):
                diagnostics.append(_diag(path, "E-SOURCE-TITLE", "source.title is required"))
            if not source_meta.get("locator"):
                diagnostics.append(_diag(path, "E-SOURCE-LOCATOR", "source.locator is required"))
        access = meta.get("access")
        if not isinstance(access, dict) or access.get("class") not in ACCESS_CLASSES:
            diagnostics.append(_diag(path, "E-ACCESS-CLASS", "valid access.class is required"))

    if entity_type == "evidence":
        source_id = meta.get("source")
        if not isinstance(source_id, str):
            diagnostics.append(
                _diag(path, "E-EVIDENCE-SOURCE-MISSING", "evidence must identify a source")
            )
        elif source_id not in corpus:
            diagnostics.append(
                _diag(path, "E-REFERENCE-MISSING", f"evidence source {source_id!r} not found")
            )
        locator = meta.get("locator")
        if not isinstance(locator, dict) or not locator.get("kind") or locator.get("value") in (None, ""):
            diagnostics.append(
                _diag(path, "E-LOCATOR-STRUCTURE", "locator must contain kind and value")
            )
        _validate_measurement(meta.get("measurement"), path, diagnostics)
        transformation = meta.get("transformation")
        if isinstance(transformation, dict) and not transformation.get("inputs"):
            diagnostics.append(
                _diag(
                    path,
                    "E-TRANSFORMATION-INPUT-MISSING",
                    "derived evidence transformation requires input lineage",
                )
            )
        access = meta.get("access")
        if isinstance(access, dict) and access.get("class") in {"licensed", "private", "sensitive"}:
            excerpt = meta.get("excerpt")
            if isinstance(excerpt, str) and len(excerpt.split()) > 120:
                diagnostics.append(
                    _diag(
                        path,
                        "E-RESTRICTED-CONTENT-PUBLIC",
                        "restricted evidence contains an excessive public excerpt",
                    )
                )

    if entity_type == "claim":
        claim = meta.get("claim")
        if not isinstance(claim, dict):
            diagnostics.append(_diag(path, "E-CLAIM-METADATA", "claim metadata is required"))
        else:
            kind = claim.get("kind")
            statement = claim.get("statement")
            if kind not in CLAIM_KINDS:
                diagnostics.append(_diag(path, "E-CLAIM-KIND", f"unsupported claim kind {kind!r}"))
            if not isinstance(statement, str) or not statement.strip():
                diagnostics.append(_diag(path, "E-CLAIM-STATEMENT", "claim.statement is required"))
                statement = ""
            confidence = claim.get("confidence")
            if confidence is not None and confidence not in CONFIDENCE_LABELS:
                diagnostics.append(
                    _diag(path, "E-CONFIDENCE", f"unsupported confidence label {confidence!r}")
                )
            if kind == "normative" and not _as_list(meta.get("values")):
                diagnostics.append(
                    _diag(path, "E-NORMATIVE-VALUES-MISSING", "normative claim requires values")
                )
            if kind == "predictive":
                if not claim.get("horizon"):
                    diagnostics.append(
                        _diag(path, "E-PREDICTION-HORIZON-MISSING", "prediction requires horizon")
                    )
                if not claim.get("evaluation"):
                    diagnostics.append(
                        _diag(
                            path,
                            "E-PREDICTION-EVALUATION-MISSING",
                            "prediction requires evaluation criterion",
                        )
                    )
            if kind == "model-derived" and not isinstance(meta.get("model"), str):
                diagnostics.append(
                    _diag(path, "E-MODEL-REFERENCE-MISSING", "model-derived claim requires model")
                )
            if kind == "correlational" and re.search(r"\bcaus(?:e|es|ed|ing)\b", statement, re.I):
                diagnostics.append(
                    _diag(
                        path,
                        "W-CLAIM-KIND-LANGUAGE-CONFLICT",
                        "correlational claim uses causal wording",
                        severity="warning",
                    )
                )
            if re.search(r"\b(?:hash|digest)\b.*\bproves?\b.*\btrue\b", statement, re.I):
                diagnostics.append(
                    _diag(
                        path,
                        "W-INTEGRITY-SEMANTIC-OVERREACH",
                        "integrity digest cannot prove semantic truth",
                        severity="warning",
                    )
                )
        _validate_argument(meta.get("argument"), path, corpus, diagnostics)

    if entity_type == "concept":
        if not isinstance(meta.get("definition"), str) or not meta.get("definition", "").strip():
            diagnostics.append(_diag(path, "E-CONCEPT-DEFINITION", "concept.definition is required"))

    if entity_type == "model":
        for field in ("purpose", "inputs", "outputs", "assumptions", "failure_modes"):
            value = meta.get(field)
            if value in (None, "", []):
                diagnostics.append(_diag(path, "E-MODEL-FIELD", f"model requires {field}"))

    if entity_type == "question":
        if not isinstance(meta.get("question"), str) or not meta.get("question", "").strip():
            diagnostics.append(_diag(path, "E-QUESTION-TEXT", "question text is required"))
        if not meta.get("resolution_criteria"):
            diagnostics.append(
                _diag(path, "E-QUESTION-RESOLUTION", "question requires resolution criteria")
            )

    if entity_type == "synthesis":
        if not isinstance(meta.get("question"), str):
            diagnostics.append(_diag(path, "E-SYNTHESIS-QUESTION", "synthesis requires question ID"))
        if not _as_list(meta.get("claims")):
            diagnostics.append(_diag(path, "E-SYNTHESIS-CLAIMS", "synthesis requires material claims"))
        if not isinstance(meta.get("conclusion"), str) or not meta.get("conclusion", "").strip():
            diagnostics.append(_diag(path, "E-SYNTHESIS-CONCLUSION", "conclusion is required"))
        if not _as_list(meta.get("revision_triggers")):
            diagnostics.append(
                _diag(path, "E-SYNTHESIS-REVISION-TRIGGERS", "revision triggers are required")
            )
        _validate_argument(meta.get("argument"), path, corpus, diagnostics)

    return diagnostics


def _validate_measurement(value: Any, path: str, diagnostics: list[Diagnostic]) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        diagnostics.append(_diag(path, "E-MEASUREMENT-STRUCTURE", "measurement must be a mapping"))
        return

    values = value.get("values")
    if isinstance(values, list):
        for index, item in enumerate(values):
            if isinstance(item, dict) and isinstance(item.get("value"), (int, float)) and not item.get("unit"):
                diagnostics.append(
                    _diag(
                        path,
                        "E-MEASUREMENT-UNIT-MISSING",
                        f"measurement.values[{index}] requires unit",
                    )
                )
    elif isinstance(value.get("value"), (int, float)) and not value.get("unit"):
        diagnostics.append(
            _diag(path, "E-MEASUREMENT-UNIT-MISSING", "numeric measurement requires unit")
        )

    if value.get("transformation") == "converted":
        if value.get("original_value") is None or not value.get("original_unit"):
            diagnostics.append(
                _diag(
                    path,
                    "E-CONVERSION-LINEAGE-MISSING",
                    "converted measurement requires original value and unit",
                )
            )


def _validate_argument(
    argument: Any,
    path: str,
    corpus: Mapping[str, Document],
    diagnostics: list[Diagnostic],
) -> None:
    if argument is None:
        return
    if not isinstance(argument, dict):
        diagnostics.append(_diag(path, "E-ARGUMENT-STRUCTURE", "argument must be a mapping"))
        return
    premises = _as_list(argument.get("premises"))
    for premise in premises:
        if not isinstance(premise, str) or _entity_type_from_id(premise) != "claim":
            diagnostics.append(
                _diag(path, "E-ARGUMENT-PREMISE-TYPE", "argument premises must reference claims")
            )
        elif premise not in corpus:
            diagnostics.append(_diag(path, "E-REFERENCE-MISSING", f"premise {premise!r} not found"))
    conclusion = argument.get("conclusion")
    if isinstance(conclusion, str) and conclusion in corpus:
        target = corpus[conclusion]
        claim = target.metadata.get("claim")
        if isinstance(claim, dict) and claim.get("kind") == "normative":
            if argument.get("mode") != "normative" or not _as_list(argument.get("values")):
                diagnostics.append(
                    _diag(
                        path,
                        "W-NORMATIVE-INFERENCE-HIDDEN",
                        "normative conclusion requires normative mode and explicit values",
                        severity="warning",
                    )
                )


def validate_corpus(documents: Sequence[Document]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    corpus: dict[str, Document] = {}
    aliases: dict[str, str] = {}

    for document in sorted(documents, key=lambda item: item.path):
        entity_id = document.entity_id
        if entity_id:
            if entity_id in corpus:
                diagnostics.append(
                    _diag(
                        document.path,
                        "E-ID-DUPLICATE",
                        f"duplicate ID also declared in {corpus[entity_id].path}",
                    )
                )
            else:
                corpus[entity_id] = document
        for alias in _as_list(document.metadata.get("aliases")):
            if not isinstance(alias, str):
                diagnostics.append(_diag(document.path, "E-ALIAS", "aliases must be IDs"))
                continue
            existing = aliases.get(alias)
            if existing and existing != entity_id:
                diagnostics.append(
                    _diag(document.path, "E-ALIAS-COLLISION", f"alias already points to {existing}")
                )
            elif alias in corpus and alias != entity_id:
                diagnostics.append(
                    _diag(document.path, "E-ALIAS-COLLISION", "alias collides with canonical ID")
                )
            else:
                aliases[alias] = entity_id or ""

    for document in sorted(documents, key=lambda item: item.path):
        diagnostics.extend(validate_document(document, corpus))

    return sorted(diagnostics)


def discover_documents(paths: Sequence[Path]) -> tuple[list[Document], list[Diagnostic]]:
    documents: list[Document] = []
    diagnostics: list[Diagnostic] = []
    discovered: set[Path] = set()
    for root in paths:
        if root.is_file() and root.suffix.lower() == ".md":
            discovered.add(root)
        elif root.is_dir():
            discovered.update(path for path in root.rglob("*.md") if path.is_file())
        else:
            diagnostics.append(_diag(str(root), "E-PATH-MISSING", "input path does not exist"))
    for path in sorted(discovered):
        document, parse_diagnostics = parse_markdown(path)
        diagnostics.extend(parse_diagnostics)
        if document:
            documents.append(document)
    return documents, sorted(diagnostics)


def validate_migration_manifest(manifest: Mapping[str, Any], path: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    mode = manifest.get("mode")
    if mode == "mechanical":
        before = manifest.get("before")
        after = manifest.get("after")
        preserved = _as_list(manifest.get("preserve"))
        if not isinstance(before, dict) or not isinstance(after, dict):
            diagnostics.append(_diag(path, "E-MIGRATION-STRUCTURE", "before and after mappings required"))
        else:
            for field in preserved:
                if before.get(field) != after.get(field):
                    diagnostics.append(
                        _diag(path, "E-MIGRATION-PRESERVATION", f"field {field!r} changed")
                    )
    elif mode == "semantic-split":
        inputs = _as_list(manifest.get("inputs"))
        outputs = _as_list(manifest.get("outputs"))
        mappings = manifest.get("mappings")
        if not inputs or len(outputs) < 2 or not isinstance(mappings, dict):
            diagnostics.append(
                _diag(
                    path,
                    "E-MIGRATION-IDENTITY-MAPPING-MISSING",
                    "semantic split requires explicit one-to-many mappings",
                )
            )
        else:
            for source_id in inputs:
                mapped = _as_list(mappings.get(source_id))
                if sorted(mapped) != sorted(outputs):
                    diagnostics.append(
                        _diag(
                            path,
                            "E-MIGRATION-IDENTITY-MAPPING-MISSING",
                            f"input {source_id!r} is not mapped to every output",
                        )
                    )
    else:
        diagnostics.append(_diag(path, "E-MIGRATION-MODE", f"unsupported mode {mode!r}"))
    return diagnostics


def compute_translation_staleness(manifest: Mapping[str, Any]) -> str:
    source_revision = manifest.get("source_revision")
    translation_source_revision = manifest.get("translation_source_revision")
    return "possibly-stale" if source_revision != translation_source_revision else "current"


def validate_identity_manifest(manifest: Mapping[str, Any], path: str) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    canonical = set(_as_list(manifest.get("canonical_ids")))
    aliases: dict[str, str] = manifest.get("aliases", {}) if isinstance(manifest.get("aliases"), dict) else {}
    federated = _as_list(manifest.get("federated_ids"))

    if len(canonical) != len(_as_list(manifest.get("canonical_ids"))):
        diagnostics.append(_diag(path, "E-ID-DUPLICATE", "canonical identity collision"))
    for alias, target in aliases.items():
        if alias in canonical and alias != target:
            diagnostics.append(_diag(path, "E-ALIAS-COLLISION", f"alias {alias!r} collides with canonical ID"))
        if target not in canonical:
            diagnostics.append(_diag(path, "E-ALIAS-TARGET", f"alias target {target!r} does not exist"))
    if len(federated) != len(set(federated)):
        diagnostics.append(_diag(path, "E-FEDERATION-COLLISION", "federated IDs must be globally unique"))
    return diagnostics


def _documents_from_case(case: Mapping[str, Any]) -> list[Document]:
    documents: list[Document] = []
    for index, payload in enumerate(_as_list(case.get("documents"))):
        if not isinstance(payload, dict):
            continue
        metadata = payload.get("metadata")
        if isinstance(metadata, dict):
            documents.append(
                Document(
                    path=str(payload.get("path", f"case-{index}.md")),
                    metadata=dict(metadata),
                    body=str(payload.get("body", "")),
                )
            )
    return documents


def run_invalid_fixture_cases(path: Path) -> list[Diagnostic]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return [_diag(str(path), "E-FIXTURE-STRUCTURE", "fixture file must contain a list")]

    failures: list[Diagnostic] = []
    for index, case in enumerate(raw):
        if not isinstance(case, dict):
            failures.append(_diag(str(path), "E-FIXTURE-STRUCTURE", f"case {index} is not a mapping"))
            continue
        name = str(case.get("name", f"case-{index}"))
        kind = case.get("kind", "documents")
        expected = sorted(set(_as_list(case.get("expected_codes"))))
        diagnostics: list[Diagnostic]
        if kind == "documents":
            diagnostics = validate_corpus(_documents_from_case(case))
        elif kind == "migration":
            diagnostics = validate_migration_manifest(case.get("manifest", {}), name)
        elif kind == "identity":
            diagnostics = validate_identity_manifest(case.get("manifest", {}), name)
        elif kind == "translation":
            state = compute_translation_staleness(case.get("manifest", {}))
            diagnostics = []
            if state != case.get("expected_state"):
                diagnostics.append(
                    _diag(name, "E-TRANSLATION-STALE-STATE", f"computed {state!r}")
                )
        else:
            diagnostics = [_diag(name, "E-FIXTURE-KIND", f"unsupported fixture kind {kind!r}")]

        actual = sorted({diagnostic.code for diagnostic in diagnostics})
        if actual != expected:
            failures.append(
                _diag(
                    str(path),
                    "E-FIXTURE-EXPECTATION",
                    f"{name}: expected {expected}, got {actual}",
                )
            )
    return sorted(failures)


def _print_diagnostics(diagnostics: Sequence[Diagnostic], as_json: bool) -> None:
    if as_json:
        print(json.dumps([item.to_dict() for item in diagnostics], indent=2, sort_keys=True))
        return
    for item in diagnostics:
        print(f"{item.severity.upper()} {item.code} {item.path}: {item.message}")


def _has_errors(diagnostics: Iterable[Diagnostic]) -> bool:
    return any(item.severity == "error" for item in diagnostics)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON diagnostics")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate Markdown corpus")
    validate.add_argument("paths", nargs="+", type=Path)
    validate.add_argument(
        "--warnings-as-errors",
        action="store_true",
        help="fail when warnings are present",
    )

    fixtures = subparsers.add_parser("invalid-fixtures", help="execute invalid fixture cases")
    fixtures.add_argument("path", type=Path)

    migration = subparsers.add_parser("migration", help="validate migration manifest")
    migration.add_argument("path", type=Path)

    identity = subparsers.add_parser("identity", help="validate identity manifest")
    identity.add_argument("path", type=Path)

    translation = subparsers.add_parser("translation-staleness", help="compute translation staleness")
    translation.add_argument("path", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        documents, parse_diagnostics = discover_documents(args.paths)
        diagnostics = sorted(parse_diagnostics + validate_corpus(documents))
        _print_diagnostics(diagnostics, args.json)
        if _has_errors(diagnostics) or (args.warnings_as_errors and diagnostics):
            return 1
        return 0

    if args.command == "invalid-fixtures":
        diagnostics = run_invalid_fixture_cases(args.path)
        _print_diagnostics(diagnostics, args.json)
        return 1 if diagnostics else 0

    raw = json.loads(args.path.read_text(encoding="utf-8"))
    if args.command == "migration":
        diagnostics = validate_migration_manifest(raw, str(args.path))
        _print_diagnostics(diagnostics, args.json)
        return 1 if _has_errors(diagnostics) else 0
    if args.command == "identity":
        diagnostics = validate_identity_manifest(raw, str(args.path))
        _print_diagnostics(diagnostics, args.json)
        return 1 if _has_errors(diagnostics) else 0
    if args.command == "translation-staleness":
        state = compute_translation_staleness(raw)
        print(json.dumps({"staleness": state}) if args.json else state)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
