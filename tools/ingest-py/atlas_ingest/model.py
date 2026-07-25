from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ConceptSource:
    title: str
    locator: str


@dataclass(frozen=True, slots=True)
class NoteRelation:
    relation_type: str
    target_slug: str
    weight: float = 1.0
    note: str = ""


@dataclass(slots=True)
class Note:
    slug: str
    title: str
    summary: str
    tags: list[str] = field(default_factory=list)
    sources: list[ConceptSource] = field(default_factory=list)
    relations: list[NoteRelation] = field(default_factory=list)
    source_path: Path | None = None


@dataclass(frozen=True, slots=True)
class AtlasDocument:
    notes: tuple[Note, ...]
    ids_by_slug: dict[str, int]

    @property
    def concept_count(self) -> int:
        return len(self.notes)

    @property
    def relation_count(self) -> int:
        return sum(len(note.relations) for note in self.notes)
