# Atlas Architecture

## System goal

Atlas converts human-authored notes and evidence into a graph that can be queried by meaning, relationship, and provenance. The architecture keeps the domain model independent from ingestion, search, transport, and interface concerns.

## Runtime flow

```text
Markdown notes
      |
      v
Python ingestion + validation
      |
      v
portable .atlas contract
      |
      +-----------------------+
      |                       |
      v                       v
C++ graph engine        Rust search service
(traversal/invariants)  (ranking/retrieval)
      |                       |
      +-----------+-----------+
                  |
                  v
          TypeScript local API
                  |
                  v
             Browser UI
```

## Component boundaries

### C++ knowledge engine

The engine is the authority for graph validity and structural operations. It owns:

- concepts, tags, source references, and relations;
- referential integrity;
- graph mutation;
- incoming and outgoing adjacency queries;
- shortest-path traversal;
- reading and writing the `.atlas` format;
- stable JSON command output for other processes.

It does **not** parse Markdown, host HTTP, or own browser state.

### Rust search service

The Rust executable is an isolated retrieval component. It loads the same portable contract, builds an in-memory representation, scores query terms across fields, and emits JSON. Its boundary allows the search implementation to evolve toward inverted indexes, Tantivy, incremental indexing, or background concurrency without destabilizing the graph core.

It does **not** mutate the graph.

### Python ingestion pipeline

The Python tool treats a knowledge folder as source code and `.atlas` as a compiled artifact. It provides:

- deterministic file discovery and ID assignment;
- front-matter parsing;
- duplicate-slug detection;
- relation-target validation;
- source and tag normalization;
- reproducible `.atlas` generation.

It does **not** serve queries at runtime.

### TypeScript API and UI

The Node process is a thin orchestration boundary. It maps HTTP routes to the native executables, validates request parameters, exposes errors consistently, and serves static browser files. It should not duplicate ranking or graph algorithms.

### SQL schema

`storage/schema.sql` defines the intended durable relational representation for a later SQLite adapter. The current runtime deliberately uses the portable file contract first, keeping migration risk low while the domain model stabilizes.

## Shared contracts

Processes communicate through two deliberately small contracts:

1. `.atlas` for persistent graph exchange;
2. JSON on stdout for executable-to-API communication.

The file contract is documented in [`contracts/atlas-format.md`](../contracts/atlas-format.md). Native tools write diagnostics to stderr and machine-readable results to stdout.

## Failure isolation

- Invalid source notes fail during ingestion before runtime.
- Invalid graph records fail atomically during C++ loading.
- Search failures do not corrupt the graph because the Rust service is read-only.
- API process errors expose a bounded JSON error rather than raw command output.
- Each language has its own tests, and CI adds an integration path across boundaries.

## Why not a single language?

A single language would reduce toolchain count but create less natural boundaries:

- C++ is excellent for a stable engine but inefficient for rapidly evolving content parsers and browser delivery.
- Python is excellent for ingestion but not the preferred long-lived native core.
- TypeScript is excellent for web boundaries but should not own all graph invariants.
- Rust is a strong fit for a future concurrent indexer without forcing a rewrite of the existing C++ engine.

The trade-off is explicit: more build tooling in exchange for clear, independently replaceable components.
