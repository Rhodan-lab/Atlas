#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CORE_BIN="${ATLAS_CORE_BIN:-$ROOT/build/engine/cpp/atlas}"
SEARCH_BIN="${ATLAS_SEARCH_BIN:-$ROOT/services/search-rs/target/debug/atlas-search}"
GENERATED="${ATLAS_DATA:-$ROOT/data/generated.atlas}"

if [[ ! -x "$CORE_BIN" ]]; then
    cmake -S . -B build -DCMAKE_BUILD_TYPE=Debug
    cmake --build build --parallel
fi
if [[ ! -x "$SEARCH_BIN" ]]; then
    cargo build --manifest-path services/search-rs/Cargo.toml
fi

PYTHONPATH=tools/ingest-py python3 -m atlas_ingest build examples/notes --output "$GENERATED"
"$CORE_BIN" validate "$GENERATED"

stats_json="$($CORE_BIN stats-json "$GENERATED")"
search_json="$($SEARCH_BIN "$GENERATED" "knowledge evidence" --limit 5)"

STATS_JSON="$stats_json" SEARCH_JSON="$search_json" python3 - <<'PY'
import json
import os

stats = json.loads(os.environ["STATS_JSON"])
search = json.loads(os.environ["SEARCH_JSON"])
assert stats == {"concepts": 7, "relations": 9, "formatVersion": 1}, stats
assert search["count"] >= 1, search
assert any(result["concept"]["title"] == "Knowledge" for result in search["results"]), search
print("native contract checks passed")
PY

ATLAS_DATA="$GENERATED" ATLAS_CORE_BIN="$CORE_BIN" ATLAS_SEARCH_BIN="$SEARCH_BIN" \
node --experimental-strip-types --input-type=module <<'JS'
import { AtlasRuntime } from "./apps/api-ts/src/runtime.ts";

const runtime = new AtlasRuntime({
    dataFile: process.env.ATLAS_DATA,
    coreBinary: process.env.ATLAS_CORE_BIN,
    searchBinary: process.env.ATLAS_SEARCH_BIN,
});
const stats = await runtime.stats();
const results = await runtime.search("knowledge", 3);
if (stats.concepts !== 7 || results.count < 1) {
    throw new Error(`unexpected integration response: ${JSON.stringify({ stats, results })}`);
}
console.log("TypeScript orchestration check passed");
JS
