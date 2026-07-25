#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

printf '\n== C++ engine ==\n'
cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --parallel
ctest --test-dir build --output-on-failure

printf '\n== Python ingestion ==\n'
PYTHONPATH=tools/ingest-py python3 -m unittest discover -s tools/ingest-py/tests -v
PYTHONPATH=tools/ingest-py python3 -m atlas_ingest validate examples/notes

printf '\n== TypeScript API ==\n'
node --experimental-strip-types --test apps/api-ts/test/*.test.ts

if command -v cargo >/dev/null 2>&1; then
    printf '\n== Rust search ==\n'
    cargo test --manifest-path services/search-rs/Cargo.toml
    "$ROOT/scripts/integration-check.sh"
else
    printf '\nwarning: cargo is not installed; Rust and full integration checks were skipped.\n' >&2
fi
