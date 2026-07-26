"""Atlas Phase 2 deterministic knowledge kernel."""

from .compiler import compile_canonical
from .kernel import (
    BRIDGE_EXPORT_CONTRACT,
    EXTERNAL_DEPENDENT_CONTRACT,
    RUNTIME_CONTRACT,
    KernelError,
    KernelRepository,
    impact_report,
    import_principia_export,
    load_json,
    render_json,
)

__all__ = [
    "BRIDGE_EXPORT_CONTRACT",
    "EXTERNAL_DEPENDENT_CONTRACT",
    "RUNTIME_CONTRACT",
    "KernelError",
    "KernelRepository",
    "compile_canonical",
    "impact_report",
    "import_principia_export",
    "load_json",
    "render_json",
]
