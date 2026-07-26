# PR #20 Representative Benchmark Evidence

## Scope

These measurements were produced by the Phase 2 Knowledge Kernel workflow for commit `82ce19f02695f74093fc348053deb8458fb934a6` using the current 34-entity canonical corpus and the pinned `principia-atlas-external-dependent/0.2` fixture.

They are operational evidence for regression detection only. They are not canonical knowledge, production capacity claims, or projections for a larger corpus.

## GitHub Actions measurements

| Operation | Python 3.11 median | Python 3.11 p95 | Python 3.13 median | Python 3.13 p95 | Budget p95 |
|---|---:|---:|---:|---:|---:|
| Canonical compilation | 69.292 ms | 69.292 ms | 73.353 ms | 73.353 ms | 5,000 ms |
| Exact lookup | 0.000341 ms | 0.000401 ms | 0.000361 ms | 0.000411 ms | 5 ms |
| Provenance traversal | 0.013364 ms | 0.014477 ms | 0.012533 ms | 0.013576 ms | 25 ms |
| Principia bridge import | 0.109804 ms | 0.189683 ms | 0.119714 ms | 0.174295 ms | 25 ms |
| Lifecycle impact report | 0.009848 ms | 0.011041 ms | 0.010290 ms | 0.010960 ms | 25 ms |

## Reproducibility markers

```text
benchmark contract: atlas-kernel-benchmark/0.1
canonical source digest: 684d08f23db50c2d994ea07293c6aaea2cbcb24492b062663b2e43144f07d3b1
fixture contract: principia-atlas-external-dependent/0.2
compile iterations: 3
operation iterations: 200
```

The raw JSON reports remain GitHub Actions artifacts for Python 3.11 and Python 3.13. Timing values should be regenerated when the corpus, runtime contract, benchmark operations, or CI environment materially changes.

## Interpretation

The current implementation has no obvious small-corpus performance blocker. Phase 2 still requires a larger deterministic synthetic-corpus benchmark before retrieval or indexing work is approved.
