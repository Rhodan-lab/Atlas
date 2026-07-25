#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --parallel

if command -v cargo >/dev/null 2>&1; then
    cargo build --release --manifest-path services/search-rs/Cargo.toml
else
    echo "warning: cargo is not installed; skipped Rust release build" >&2
fi
