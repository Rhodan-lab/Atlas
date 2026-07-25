# ADR 0001: Bounded Polyglot Architecture

- **Status:** Accepted
- **Date:** 2026-07-25

## Context

Atlas began as a C++ knowledge-graph kernel. The product direction now includes ingestion, search, an HTTP surface, and a local UI. Implementing every concern in C++ would increase delivery friction, while replacing the core would discard a useful native model.

## Decision

Use process-level polyglot boundaries:

- C++ remains authoritative for graph structure and traversal.
- Rust owns read-only search and future indexing.
- Python owns source compilation and validation.
- TypeScript owns local HTTP and browser integration.
- SQL describes the future durable store.

All components exchange a versioned `.atlas` file or JSON through standard input/output boundaries. No component imports another language through unstable in-process FFI at this phase.

## Consequences

### Positive

- Each component can evolve independently.
- Crashes and dependency problems remain isolated by process boundaries.
- The portable file format prevents vendor or runtime lock-in.
- Each language is used for a task aligned with its ecosystem.

### Negative

- Contributors need multiple toolchains for the entire stack.
- Integration tests are essential because unit tests cannot validate process contracts.
- Some parsing code exists in more than one read-only consumer.

## Guardrail

Atlas will not add another language unless it passes the admission test in `docs/language-decisions.md`.
