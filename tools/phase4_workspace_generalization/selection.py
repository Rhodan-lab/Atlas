"""Deterministically rank and select the Catalase exact revisions."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from tools.phase2_kernel import KernelRepository
from tools.phase3_retrieval.structured import build_structured_index, search_structured_index

from .constants import SOURCE_DIGEST, exact_key, require, seal


def build_selection(
    spec: Mapping[str, Any],
    canonical_root: Path,
    repository: KernelRepository,
    structured_baseline: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    index = build_structured_index(canonical_root)
    require(
        index.get("build_digest") == structured_baseline.get("index_build_digest"),
        "E-W4-STRUCTURED-INDEX",
        "rebuilt structured index differs from accepted baseline",
    )
    require(index.get("source_digest") == SOURCE_DIGEST, "E-W4-STRUCTURED-INDEX", "structured source mismatch")
    hits = search_structured_index(index, str(spec["query"]["text"]), limit=repository.runtime["entity_count"])
    rank_map = {
        f"{hit['document']['id']}@{hit['document']['revision']}": {
            "rank": rank,
            "score": hit["score"],
            "matched_fields": list(hit["matched_fields"]),
        }
        for rank, hit in enumerate(hits, start=1)
    }
    selected: list[dict[str, Any]] = []
    for item in spec["selected_entries"]:
        key = exact_key(item["exact_reference"])
        require(key in rank_map, "E-W4-RANKING", f"selected revision did not match query: {key}")
        selected.append({**dict(item), **rank_map[key]})
    selected.sort(key=lambda item: (int(item["rank"]), exact_key(item["exact_reference"])))
    snapshot = seal({
        "contract": "atlas-phase4-workstream4-structured-selection/0.1",
        "query": dict(spec["query"]),
        "index_contract": index["contract"],
        "index_build_digest": index["build_digest"],
        "selected": [
            {
                "exact_reference": dict(item["exact_reference"]),
                "rank": item["rank"],
                "score": item["score"],
                "matched_fields": list(item["matched_fields"]),
            }
            for item in selected
        ],
        "advisory_only": True,
        "canonical_mutation": False,
        "live": False,
        "repository_mutation": False,
    })
    return snapshot, selected
