#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

./scripts/build.sh
PYTHONPATH=tools/ingest-py python3 -m atlas_ingest build examples/notes --output data/generated.atlas

export ATLAS_DATA="$ROOT/data/generated.atlas"
export ATLAS_CORE_BIN="$ROOT/build/engine/cpp/atlas"
export ATLAS_SEARCH_BIN="$ROOT/services/search-rs/target/release/atlas-search"
exec node --experimental-strip-types apps/api-ts/src/server.ts
