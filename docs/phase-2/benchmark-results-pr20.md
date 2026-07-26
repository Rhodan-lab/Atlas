# PR #20 Representative Benchmark Evidence

## Scope

These measurements were produced by the Phase 2 Knowledge Kernel workflow for commit `4bf5078147ce46c7071997c1420f8e3817f9c8e0` using the current 34-entity canonical corpus and the pinned `principia-atlas-external-dependent/0.2` fixture.

They are operational evidence for regression detection only. They are not canonical knowledge, production capacity claims, or projections for a larger corpus.

## GitHub Actions measurements

| Operation | Python 3.11 median | Python 3.11 p95 | Python 3.13 median | Python 3.13 p95 | Budget p95 |
|---|---:|---:|---:|---:|---:|
| Canonical compilation | 46.258 ms | 47.056 ms | 84.903 ms | 86.857 ms | 5,000 ms |
| Exact lookup | 0.000240 ms | 0.000320 ms | 0.000361 ms | 0.000411 ms | 5 ms |
| Provenance traversal | 0.009003 ms | 0.009574 ms | 0.014627 ms | 0.023704 ms | 25 ms |
| Principia bridge import | 0.075392 ms | 0.084095 ms | 0.120015 ms | 0.161954 ms | 25 ms |
| Lifecycle impact report | 0.007301 ms | 0.007681 ms | 0.010450 ms | 0.011973 ms | 25 ms |

## Reproducibility markers

```text
benchmark contract: atlas-kernel-benchmark/0.1
canonical source digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
fixture contract: principia-atlas-external-dependent/0.2
compile iterations: 3
operation iterations: 200
p95 method: nearest-rank
```

The raw JSON reports remain GitHub Actions artifacts for Python 3.11 and Python 3.13. Timing values should be regenerated when the corpus, runtime contract, benchmark operations, percentile method, or CI environment materially changes.

## Interpretation

The current implementation has no obvious small-corpus performance blocker. Phase 2 still requires a larger deterministic synthetic-corpus benchmark before retrieval or indexing work is approved.
