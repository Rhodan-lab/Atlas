"""Public deterministic compiler boundary for the Atlas Phase 2 kernel."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .kernel import compile_canonical as _compile_canonical


def compile_canonical(canonical_root: Path) -> dict[str, Any]:
    """Compile a corpus while keeping source identity independent of path form."""
    runtime = _compile_canonical(canonical_root)
    resolved = canonical_root.resolve()
    runtime["source_root"] = (
        "/".join(resolved.parts[-2:])
        if len(resolved.parts) >= 2
        else resolved.name
    )
    return runtime
