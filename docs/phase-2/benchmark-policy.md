# Phase 2 Benchmark Policy

## Purpose

The Phase 2 kernel needs representative performance evidence before retrieval work begins. The benchmark is a regression guard, not a claim about production capacity or a substitute for profiling at larger corpus sizes.

## Measured operations

`tools/phase2_kernel/benchmark.py` measures:

1. canonical Markdown compilation;
2. exact entity and revision lookup;
3. synthesis-to-source provenance traversal;
4. Principia v0.2 bridge import;
5. lifecycle-aware dependency-impact reporting.

Each metric records iteration count, median latency, 95th-percentile latency, and maximum observed latency. The report also records Python version, execution platform, entity count, canonical source digest, and fixture contract.

## CI budgets

The initial budgets are deliberately generous machine gates intended to detect severe regressions or accidental unbounded work:

| Operation | Maximum p95 |
|---|---:|
| Canonical compilation | 5,000 ms |
| Exact lookup | 5 ms |
| Provenance traversal | 25 ms |
| Bridge import | 25 ms |
| Impact report | 25 ms |

Passing these budgets does not establish internet-scale, enterprise-scale, or production-service performance. Results are valid only for the current representative Atlas corpus and the GitHub Actions environment used by the workflow.

## Reproducibility boundary

Timing values are inherently environment-dependent and are therefore emitted as CI artifacts rather than committed as canonical facts. The benchmark contract, operation definitions, fixture identity, budgets, and source digest are machine-readable and versioned.

## Expansion rule

Before Phase 2 closes, performance should also be measured on a larger deterministic synthetic corpus. Retrieval or indexing work should not begin merely because this small-corpus benchmark passes.
