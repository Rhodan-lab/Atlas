from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from .model import AtlasDocument, ConceptSource, Note, NoteRelation


class IngestError(ValueError):
    """Raised when authored knowledge violates the Atlas source contract."""


_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _clean_summary(body: str) -> str:
    paragraphs = [" ".join(line.strip() for line in block.splitlines() if line.strip())
                  for block in re.split(r"\n\s*\n", body.strip())]
    return "\n\n".join(paragraph for paragraph in paragraphs if paragraph)


def _split_pipe(value: str, expected_minimum: int, field: str, path: Path) -> list[str]:
    parts = [part.strip() for part in value.split("|")]
    if len(parts) < expected_minimum or any(not part for part in parts[:expected_minimum]):
        raise IngestError(f"{path}: malformed {field}: {value!r}")
    return parts


def _parse_front_matter(text: str, path: Path) -> tuple[list[tuple[str, str]], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise IngestError(f"{path}: note must start with '---' front matter")

    metadata: list[tuple[str, str]] = []
    closing_index: int | None = None
    for index, raw_line in enumerate(lines[1:], start=1):
        if raw_line.strip() == "---":
            closing_index = index
            break
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            raise IngestError(f"{path}:{index + 1}: expected 'key: value'")
        key, value = raw_line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if not key or not value:
            raise IngestError(f"{path}:{index + 1}: metadata keys and values cannot be empty")
        metadata.append((key, value))

    if closing_index is None:
        raise IngestError(f"{path}: missing closing '---' front matter marker")
    body = "\n".join(lines[closing_index + 1 :])
    return metadata, body


def parse_note(path: Path) -> Note:
    metadata, body = _parse_front_matter(path.read_text(encoding="utf-8"), path)
    scalar: dict[str, str] = {}
    repeated: dict[str, list[str]] = {"source": [], "relation": []}
    allowed = {"slug", "title", "tags", "summary", "source", "relation"}

    for key, value in metadata:
        if key not in allowed:
            raise IngestError(f"{path}: unknown metadata key {key!r}")
        if key in repeated:
            repeated[key].append(value)
        elif key in scalar:
            raise IngestError(f"{path}: duplicate metadata key {key!r}")
        else:
            scalar[key] = value

    slug = scalar.get("slug", "")
    title = scalar.get("title", "")
    summary = scalar.get("summary", "") or _clean_summary(body)
    if not _SLUG_RE.fullmatch(slug):
        raise IngestError(f"{path}: slug must be lowercase kebab-case")
    if not title.strip():
        raise IngestError(f"{path}: title is required")
    if not summary.strip():
        raise IngestError(f"{path}: summary body or summary metadata is required")

    tags: list[str] = []
    seen_tags: set[str] = set()
    for raw_tag in scalar.get("tags", "").split(","):
        tag = raw_tag.strip()
        if not tag:
            continue
        normalized = tag.casefold()
        if normalized not in seen_tags:
            seen_tags.add(normalized)
            tags.append(tag)

    sources: list[ConceptSource] = []
    for raw_source in repeated["source"]:
        parts = _split_pipe(raw_source, 2, "source", path)
        sources.append(ConceptSource(parts[0], "|".join(parts[1:]).strip()))

    relations: list[NoteRelation] = []
    for raw_relation in repeated["relation"]:
        parts = _split_pipe(raw_relation, 2, "relation", path)
        relation_type, target_slug = parts[0], parts[1]
        try:
            weight = float(parts[2]) if len(parts) >= 3 and parts[2] else 1.0
        except ValueError as error:
            raise IngestError(f"{path}: relation weight must be numeric: {raw_relation!r}") from error
        if weight <= 0:
            raise IngestError(f"{path}: relation weight must be greater than zero")
        relation_note = "|".join(parts[3:]).strip() if len(parts) >= 4 else ""
        relations.append(NoteRelation(relation_type, target_slug, weight, relation_note))

    return Note(
        slug=slug,
        title=title.strip(),
        summary=summary.strip(),
        tags=tags,
        sources=sources,
        relations=relations,
        source_path=path,
    )


def load_notes(directory: Path) -> AtlasDocument:
    if not directory.is_dir():
        raise IngestError(f"input directory does not exist: {directory}")

    paths = sorted(path for path in directory.rglob("*.md") if path.is_file())
    if not paths:
        raise IngestError(f"no Markdown notes found in {directory}")

    notes = [parse_note(path) for path in paths]
    by_slug: dict[str, Note] = {}
    for note in notes:
        if note.slug in by_slug:
            first = by_slug[note.slug].source_path
            raise IngestError(f"duplicate slug {note.slug!r}: {first} and {note.source_path}")
        by_slug[note.slug] = note

    ordered = sorted(notes, key=lambda item: (item.slug, item.title.casefold()))
    ids_by_slug = {note.slug: index for index, note in enumerate(ordered, start=1)}
    relation_keys: set[tuple[str, str, str]] = set()

    for note in ordered:
        for relation in note.relations:
            if relation.target_slug not in ids_by_slug:
                raise IngestError(
                    f"{note.source_path}: relation target {relation.target_slug!r} does not exist"
                )
            if relation.target_slug == note.slug:
                raise IngestError(f"{note.source_path}: self-relations are not allowed in Atlas v1")
            key = (note.slug, relation.target_slug, relation.relation_type.casefold())
            if key in relation_keys:
                raise IngestError(f"{note.source_path}: duplicate relation {key}")
            relation_keys.add(key)

    return AtlasDocument(tuple(ordered), ids_by_slug)


def _quote(value: str) -> str:
    normalized = value.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return '"' + normalized.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_atlas(document: AtlasDocument) -> str:
    lines = ["ATLAS\t1"]
    for note in document.notes:
        concept_id = document.ids_by_slug[note.slug]
        lines.append(
            "\t".join(
                [
                    "C",
                    str(concept_id),
                    _quote(note.title),
                    _quote(note.summary),
                    _quote("|".join(note.tags)),
                ]
            )
        )
        for source in note.sources:
            lines.append(
                "\t".join(["S", str(concept_id), _quote(source.title), _quote(source.locator)])
            )

    for note in document.notes:
        source_id = document.ids_by_slug[note.slug]
        for relation in note.relations:
            target_id = document.ids_by_slug[relation.target_slug]
            lines.append(
                "\t".join(
                    [
                        "R",
                        str(source_id),
                        str(target_id),
                        _quote(relation.relation_type),
                        format(relation.weight, ".12g"),
                        _quote(relation.note),
                    ]
                )
            )
    return "\n".join(lines) + "\n"


def compile_directory(directory: Path, output: Path) -> AtlasDocument:
    document = load_notes(directory)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_atlas(document), encoding="utf-8")
    return document


def summaries(document: AtlasDocument) -> Iterable[str]:
    for note in document.notes:
        yield f"{document.ids_by_slug[note.slug]}\t{note.slug}\t{note.title}"
