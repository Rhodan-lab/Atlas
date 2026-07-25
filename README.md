# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)

**Atlas is a local-first knowledge system that turns notes and source material into an inspectable knowledge graph.**

It is intentionally polyglot. Each language is used where it provides a concrete technical advantage rather than to inflate the repository:

| Layer | Language | Responsibility | Why this language |
|---|---|---|---|
| Knowledge engine | C++20 | Graph model, validation, traversal, portable storage | Predictable performance, small native binary, strong control over core invariants |
| Search service | Rust | Ranking and full-text retrieval over Atlas datasets | Memory safety with native performance; suitable for future concurrent indexing |
| Ingestion pipeline | Python 3.11+ | Convert structured Markdown into canonical `.atlas` data | Fast parser development and strong data-processing ecosystem |
| Local API and UI | TypeScript on Node.js 22+ | HTTP boundary, process orchestration, browser interface | Shared web types, ergonomic APIs, and direct browser compatibility |
| Durable schema | SQL | Future SQLite persistence and migrations | Declarative constraints and portable local storage |

## What already works

- Parse a folder of Markdown knowledge notes into a deterministic `.atlas` graph.
- Validate unique concepts, relation targets, weights, tags, and source references.
- Load, save, inspect, mutate, and traverse the graph with the C++ engine.
- Return JSON for graph statistics, concepts, neighbors, and shortest paths.
- Search concepts with a standalone Rust CLI using weighted fields.
- Expose the native tools through a TypeScript HTTP API.
- Browse and search the starter graph through a small local web interface.
- Test each language independently and run an end-to-end integration check in CI.

## Repository map

```text
Atlas/
├── engine/cpp/          # authoritative graph domain model and CLI
├── services/search-rs/  # native search executable
├── tools/ingest-py/     # Markdown -> .atlas compiler
├── apps/api-ts/         # local HTTP API and browser interface
├── contracts/           # shared data-format contract
├── storage/             # future SQLite schema
├── examples/notes/      # source notes for the ingestion pipeline
├── data/                # canonical starter graph
├── docs/                # architecture, decisions, and roadmap
└── scripts/             # repeatable build and integration commands
```

## Fast start

### 1. Build and test the C++ core

```bash
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
```

### 2. Compile example notes into a graph

```bash
PYTHONPATH=tools/ingest-py python3 -m atlas_ingest build examples/notes \
  --output data/generated.atlas
```

### 3. Build and test the Rust search service

```bash
cargo test --manifest-path services/search-rs/Cargo.toml
cargo build --release --manifest-path services/search-rs/Cargo.toml
```

### 4. Run the API

```bash
ATLAS_DATA=data/generated.atlas \
ATLAS_CORE_BIN=build/engine/cpp/atlas \
ATLAS_SEARCH_BIN=services/search-rs/target/release/atlas-search \
node --experimental-strip-types apps/api-ts/src/server.ts
```

Open `http://127.0.0.1:4242`.

## CLI examples

```bash
./build/engine/cpp/atlas stats data/starter.atlas
./build/engine/cpp/atlas stats-json data/starter.atlas
./build/engine/cpp/atlas list-json data/starter.atlas
./build/engine/cpp/atlas neighbors-json data/starter.atlas 1
./build/engine/cpp/atlas path-json data/starter.atlas 4 5

cargo run --manifest-path services/search-rs/Cargo.toml -- \
  data/starter.atlas "knowledge evidence"
```

## One-command checks

```bash
./scripts/check.sh
```

The script tests every installed toolchain and clearly reports optional toolchains that are not present. GitHub Actions verifies all five layers.

## Design principles

1. **Knowledge before interface.** The domain model must remain useful without the UI.
2. **One canonical contract.** Languages communicate through a documented `.atlas` format and JSON process boundaries.
3. **Evidence is first-class.** Sources remain attached to the concepts they support.
4. **Connections before folders.** Concepts can participate in many contexts through typed relations.
5. **Local-first and portable.** The user owns readable files and can run the system offline.
6. **Polyglot with restraint.** A language is introduced only when its boundary is independently useful.
7. **Inspectable over magical.** Ranking, traversal, validation, and persistence remain understandable.

## Current phase

**Phase 2 — Polyglot Foundation.** The repository is a working software kernel and development platform, not yet a finished personal knowledge product. See [the roadmap](docs/roadmap.md).

## License

MIT
