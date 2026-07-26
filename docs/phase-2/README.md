# Phase 2 — Minimal Knowledge Kernel

## Status

Active after Phase 1 completion under the explicitly labeled AI-reviewed policy.

The first workstream built the deterministic kernel and bounded bridge receiver through PR #19. The second workstream consumes the exact non-live export merged through Principia PR #16.

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

## Implemented workstreams

### Kernel and receiver

- `atlas-kernel-runtime/0.1` deterministic compilation;
- path-form-independent source identity;
- exact `ENTITY_ID@REVISION` lookup;
- typed relation and explicit provenance traversal;
- internal reverse-dependency impact;
- deterministic external-dependent normalization;
- positive and negative bridge fixtures;
- Python 3.11 and 3.13 CI.

### Principia v0.2 compatibility

- exact snapshot of the export merged through Principia PR #16;
- `principia-atlas-external-dependent/0.2` adapter;
- validation that `depends_on` exactly mirrors `depends_on_exact`;
- exact model revision 2 admission;
- source pull request, commit, path, blob, and SHA-256 tracking;
- lifecycle escalation for deprecated, stale, and retracted entities;
- representative compilation, lookup, provenance, import, and impact benchmarks.

The old ID-only shape remains an explicit rejection fixture. The merged Principia v0.2 export is accepted because its `depends_on_exact` objects preserve exact revisions.

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

Authored Markdown remains the source of truth. Any runtime database, index, serialized representation, adapter, or API is replaceable and must be reproducible from canonical content and pinned external fixtures.

## Principia compatibility

Phase 2 implements a read-only receiving and validation boundary. It does not activate a live cross-repository dependency.

Compatibility is limited to stable artifact identity, exact Atlas IDs and revisions, declared dependency roles, provenance, and dependency-impact semantics. Principia pedagogical and release status fields are rejected, and neither repository changes the other's status.

Atlas distinguishes the action Principia declared from the effective action implied by Atlas lifecycle state. Atlas may escalate to `revalidate` or `block-release`, but it does not execute that action automatically.

See:

- `docs/phase-2/kernel-contract.md`;
- `docs/phase-2/bridge-receiver.md`;
- `docs/phase-2/principia-v02-compatibility.md`;
- `docs/phase-2/benchmark-policy.md`;
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
- performance is measured on representative and larger deterministic corpora;
- lifecycle escalation is tested;
- the selected kernel remains replaceable;
- a completion report recommends or rejects retrieval work.
