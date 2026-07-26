# Phase 2 — Minimal Knowledge Kernel

## Status

Active after Phase 1 completion under the explicitly labeled AI-reviewed policy.

The first implementation workstream is the deterministic kernel and bounded Principia bridge receiver on `agent/phase-2-principia-bridge-kernel`.

## Goal

Build the smallest dependable runtime that compiles and queries `atlas-content/0.1` without changing authored Markdown meaning.

## Required capabilities

1. deterministic canonical Markdown compilation;
2. exact entity ID and revision lookup;
3. read-only entity repository;
4. typed relation traversal;
5. synthesis-to-source provenance traversal;
6. reverse dependency and revision-impact queries;
7. visible lifecycle, staleness, confidence, and review level;
8. deterministic errors for malformed, missing, stale, or incompatible input;
9. compatibility tests against all three English slices;
10. representative performance measurements.

## Current workstream

The initial kernel work provides:

- `atlas-kernel-runtime/0.1` deterministic compilation;
- exact `ENTITY_ID@REVISION` lookup;
- typed relation and synthesis-to-source traversal;
- internal reverse-dependency impact;
- `principia-atlas-bridge-export/0.1` validation;
- deterministic external-dependent normalization;
- Principia impact reporting without status mutation;
- positive and negative bridge fixtures;
- Python 3.11 and 3.13 CI.

The receiver rejects the former ID-only Principia export because `depends_on: [ID, ...]` does not preserve exact revisions.

## Non-goals

- polished UI;
- specialized retrieval or ranking;
- vector database selection;
- synchronization;
- plugins;
- active translated corpus;
- a live Principia dependency;
- cloning or calling Principia during Atlas validation;
- changing canonical authored semantics;
- treating `ai-reviewed` as `human-verified`.

## Architecture rule

Authored Markdown remains the source of truth. Any runtime database, index, serialized representation, or API is replaceable and must be reproducible from canonical content.

## Principia compatibility

Phase 2 may implement the read-only receiving and validation boundary for future Principia exports. It does not activate a live cross-repository dependency.

Compatibility is limited to stable artifact identity, exact Atlas IDs and revisions, declared dependency roles, provenance, and dependency-impact semantics. Principia pedagogical and release status fields are rejected, and neither repository changes the other's status.

See:

- `docs/phase-2/kernel-contract.md`;
- `docs/phase-2/bridge-receiver.md`;
- `content/fixtures/phase2_bridge/`;
- `tools/phase2_kernel/`.

## Exit evidence

Phase 2 closes only when:

- compilation is deterministic;
- exact-revision queries are correct;
- relation and provenance traversal are tested;
- reverse dependency impact is correct;
- malformed and incompatible data fail safely;
- all three English reference slices compile;
- performance is measured on representative data;
- the selected kernel remains replaceable;
- a completion report recommends or rejects retrieval work.
