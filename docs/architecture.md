# Atlas Prototype Architecture

## Status

**Experimental; not the approved Atlas architecture.**

This document records how the current prototype works so its behavior can be tested and compared. Authoritative product and knowledge decisions live in [`docs/foundation/`](foundation/). The prototype must not define the ontology merely because it already exists.

## Purpose of preserving the prototype

The existing implementation is useful for:

- testing whether authored notes can produce deterministic artifacts;
- exploring graph traversal and process boundaries;
- comparing single-language and polyglot alternatives later;
- identifying missing contracts and failure modes;
- preserving engineering work without turning it into sunk-cost architecture.

It is not evidence that Atlas needs four languages, multiple native binaries, an HTTP process, or the current `.atlas` record model.

## Current experimental flow

```text
Prototype Markdown notes
          |
          v
Python ingestion and validation
          |
          v
provisional .atlas format
          |
          +-----------------------+
          |                       |
          v                       v
C++ concept graph          Rust lexical search
          |                       |
          +-----------+-----------+
                      |
                      v
             TypeScript local API
                      |
                      v
                Browser demo
```

The flow is internally coherent for its original concept-graph model. It is incomplete for the canonical Phase 0 model, which distinguishes source, evidence, claim, concept, relation, model, question, synthesis, and revision.

## Current component behavior

### C++ graph engine

Current responsibilities:

- load and save the provisional `.atlas` format;
- validate concepts, source references, and relations;
- expose adjacency and shortest-path operations;
- emit JSON for command-line integration.

Current limitations:

- concept is too broad to be the canonical domain object;
- evidence and claims are not first-class;
- review, uncertainty, disagreement, and revision are absent;
- the need for a native core has not been benchmarked.

### Rust search executable

Current responsibilities:

- load the provisional file format;
- rank terms across title, summary, tags, and source references;
- emit JSON results.

Current limitations:

- no documented relevance test collection;
- no representative corpus scale or performance target;
- no proof that a separate process is needed;
- ranking cannot expose claim-level provenance because the model lacks it.

### Python ingestion tool

Current responsibilities:

- discover prototype Markdown notes;
- parse simple front matter;
- assign reproducible numeric IDs from sorted slugs;
- validate relation targets;
- compile the provisional format.

Current limitations:

- the note format is not the authoritative Phase 0 content contract;
- sorted numeric IDs are reproducible but not sufficient canonical identity;
- content types, editorial lifecycle, and review rules are incomplete;
- the parser may be replaced by the simplest Phase 1 validator.

### TypeScript API and browser demo

Current responsibilities:

- map HTTP routes to prototype executables;
- validate basic request parameters;
- serve a small browser interface.

Current limitations:

- the most important Atlas workflows do not exist yet;
- the interface can create a false appearance of product maturity;
- the need for an HTTP boundary has not been established;
- domain logic must never migrate into the orchestration layer.

### SQL schema

The existing schema is a design sketch for the concept graph. It is not an approved durable ontology. Persistence design must wait until identity, revision, claim, evidence, and review semantics stabilize.

## Prototype contracts

The current implementation uses:

1. `.atlas` as a portable tabular record format;
2. JSON on stdout for process integration.

Both are provisional. The authoritative Phase 0 contract is human-authored Markdown. Derived formats must be evaluated only after representative content fixtures exist.

## Existing strengths worth retaining

- local-first operation;
- inspectable files and algorithms;
- deterministic intent;
- bounded process outputs;
- independent tests;
- failure isolation;
- cross-platform CI;
- the ability to replace components.

## Existing assumptions requiring proof

- that graph traversal belongs in a native core;
- that search requires Rust and a separate process;
- that ingestion should be Python;
- that browser delivery should use a Node API;
- that SQL should mirror the current concept structure;
- that the `.atlas` format should remain the runtime contract;
- that the operational cost of several toolchains is justified.

## Architecture work permitted during Phase 0

- document observed prototype behavior;
- repair defects that block tests or inspection;
- create ADR templates and comparison criteria;
- build fixtures independent of the prototype;
- identify duplicated rules and hidden assumptions;
- measure the prototype only when measurements inform an open foundation decision.

## Architecture work prohibited during Phase 0

- adding prototype features;
- expanding the UI;
- adding languages or services;
- evolving `.atlas` as if it were canonical;
- encoding the new ontology directly into SQL before fixtures;
- implementing AI synthesis;
- optimizing unmeasured workloads.

## Path to an approved architecture

After the Phase 0 gate:

1. create canonical valid and invalid content fixtures;
2. implement the smallest validator and compiler baseline;
3. measure representative workflows;
4. identify stable semantic ownership;
5. compare the baseline with relevant prototype components;
6. write ADRs for retained or extracted boundaries;
7. version contracts and add compatibility tests;
8. promote only the justified architecture.

The approved architecture may reuse much of the prototype, use only part of it, or replace it. Authoritative knowledge must survive any of those outcomes.
