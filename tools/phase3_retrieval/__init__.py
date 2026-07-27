"""Atlas Phase 3 retrieval evaluation interfaces."""

from .contracts import (
    METRIC_REPORT_CONTRACT,
    MODE,
    QUERY_SET_CONTRACT,
    RESULT_SET_CONTRACT,
    VALIDATION_REPORT_CONTRACT,
    validate_metric_report,
    validate_query_set,
    validate_result_set,
)
from .lexical import (
    LEXICAL_BASELINE_REPORT_CONTRACT,
    LEXICAL_INDEX_CONTRACT,
    SCORING_CONTRACT,
    TOKENIZER_CONTRACT,
    build_lexical_index,
    evaluate_result_set,
    run_lexical_baseline,
    run_lexical_queries,
    search_lexical_index,
    tokenize,
    validate_lexical_index,
)

__all__ = [
    "LEXICAL_BASELINE_REPORT_CONTRACT",
    "LEXICAL_INDEX_CONTRACT",
    "METRIC_REPORT_CONTRACT",
    "MODE",
    "QUERY_SET_CONTRACT",
    "RESULT_SET_CONTRACT",
    "SCORING_CONTRACT",
    "TOKENIZER_CONTRACT",
    "VALIDATION_REPORT_CONTRACT",
    "build_lexical_index",
    "evaluate_result_set",
    "run_lexical_baseline",
    "run_lexical_queries",
    "search_lexical_index",
    "tokenize",
    "validate_lexical_index",
    "validate_metric_report",
    "validate_query_set",
    "validate_result_set",
]
