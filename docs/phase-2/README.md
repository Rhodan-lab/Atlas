# Phase 2 — Minimal Knowledge Kernel

## Status

Active after Phase 1 completion under the explicitly labeled AI-reviewed policy.

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

## Non-goals

- polished UI;
- specialized retrieval or ranking;
- vector database selection;
- synchronization;
- plugins;
- active translated corpus;
- direct Principia integration;
- changing canonical authored semantics;
- treating `ai-reviewed` as `human-verified`.

## Architecture rule

Authored Markdown remains the source of truth. Any runtime database, index, serialized representation, or API is replaceable and must be reproducible from canonical content.

## Principia compatibility

The kernel should eventually support exact-revision references from Principia, but Phase 2 creates no live cross-repository dependency. Compatibility is limited to stable IDs, revisions, provenance, and dependency-impact semantics.

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
