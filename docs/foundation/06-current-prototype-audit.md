# Current Prototype Audit

## Scope

This audit evaluates the existing C++, Rust, Python, TypeScript, SQL, `.atlas`, and browser prototype against the Phase 0 foundation. It does not judge whether the code is well written in isolation; it asks whether the prototype rests on a mature knowledge model.

## Executive finding

The prototype demonstrates useful engineering capabilities, but it was built before the product ontology and editorial system were sufficiently defined. It should be preserved as an experiment and test harness, not treated as the final foundation.

## What the prototype gets right

### Local-first posture

The current design uses inspectable local files and does not require a cloud account. This aligns with Atlas ownership and portability principles.

### Explicit component boundaries

Ingestion, graph operations, search, transport, and interface are separated rather than mixed into one application. This makes replacement and comparison possible.

### Deterministic intent

The Python compiler, portable format, JSON output, and CI structure aim for reproducible behavior.

### Inspectable algorithms

Graph traversal and weighted lexical search are understandable and testable. The design does not rely entirely on opaque vector retrieval.

### Basic engineering discipline

The repository includes tests, CI, documentation, failure boundaries, a license, contributing guidance, and security guidance.

These strengths should be retained as engineering lessons, not mistaken for proof that the architecture is final.

## Foundation gaps

### 1. The central entity is too broad

The prototype treats a `Concept` as the primary object containing title, summary, tags, and source references. This cannot reliably represent individual claims, evidence fragments, conflicting findings, models, questions, or syntheses.

### 2. Sources attach at the wrong level

A source reference attached to a whole concept does not explain which statement it supports or whether it supports, challenges, illustrates, or contextualizes that statement.

### 3. Review and uncertainty are missing

The runtime model does not encode draft status, review types, contested material, confidence rationale, revision history, deprecation, or retraction.

### 4. Relations are technically typed but not governed

The format accepts relation text without a canonical vocabulary, allowed entity pairs, semantic definitions, or migration rules. This risks a graph whose edges look structured but mean different things to different authors.

### 5. Canonical identity depends on compilation order

The current ingestion assigns numeric IDs deterministically from sorted source notes. This is reproducible for a fixed corpus, but IDs may change when slugs or ordering change and are not adequate as sole durable knowledge identity.

### 6. The compiled format arrived before the authoring contract

`.atlas` defines storage records before the project has finalized what must be authored, reviewed, revised, and preserved. Storage convenience is therefore shaping ontology.

### 7. Search was separated before retrieval needs were measured

The Rust boundary is technically plausible, but there is no documented relevance test set, corpus scale, latency target, memory target, or baseline comparison proving that a separate native search process is needed.

### 8. The web layer arrived before core workflows were proven

The TypeScript API and browser explorer demonstrate integration, but the most important workflows—claim inspection, evidence tracing, disagreement, review, and revision impact—do not yet exist in the model.

### 9. SQL mirrors an immature ontology

A durable schema should follow accepted entity and revision semantics. Encoding the current concept graph in SQL could make premature assumptions expensive to change.

### 10. The roadmap measured implementation rather than foundation

Calling the native and polyglot prototypes completed foundation phases overstated project maturity. A buildable system is not yet a trustworthy knowledge system.

## Risk assessment

### Highest risk: semantic lock-in

Continuing to add features around the current `Concept` model would make later claim-level provenance and revision difficult.

### High risk: duplicated domain logic

Multiple languages parsing or validating related records can drift unless one semantic owner and shared fixtures are established.

### High risk: operational complexity without user value

Four programming languages, multiple package managers, native binaries, and process orchestration create maintenance cost before the reference corpus proves the need.

### Medium risk: prototype credibility

A working UI and CI badge can make provisional assumptions appear settled, encouraging feature work before review policy exists.

## Disposition by component

| Component | Current disposition | Phase 0 action |
|---|---|---|
| Markdown note examples | useful but incomplete | replace with canonical entity fixtures |
| Python ingestion | prototype candidate | pause feature work; later compare as validator baseline |
| `.atlas` format | experimental derived format | do not extend until authoring contract is accepted |
| C++ engine | prototype candidate | preserve tests; do not treat domain model as canonical |
| Rust search | experiment | freeze until relevance and performance requirements exist |
| TypeScript API/UI | integration demonstration | freeze feature work |
| SQL schema | design sketch | revise only after ontology and revision model stabilize |
| CI | useful infrastructure | continue validating prototype; later add foundation fixtures |

## Immediate corrective actions

1. Mark the repository as Phase 0.
2. Make foundation documents authoritative over code.
3. Freeze feature expansion.
4. Define canonical entities and evidence roles.
5. Define the Markdown source contract.
6. Build real vertical-slice fixtures.
7. Evaluate the smallest reference implementation.
8. Reassess every existing component through an ADR.

## What should not happen

- deleting the prototype merely to appear clean;
- continuing it because effort has already been spent;
- rewriting it in a different language before requirements exist;
- adding more fields directly to `.atlas` without testing the authoring model;
- building visual polish around incomplete semantics;
- declaring the foundation complete because tests pass.

## Conclusion

The prototype is valuable evidence about possible implementation boundaries. It is not yet evidence that those boundaries are necessary. Atlas should now move backward deliberately—from software components to knowledge foundations—so later engineering is guided by meaning rather than momentum.
