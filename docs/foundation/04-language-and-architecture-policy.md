# Language and Architecture Decision Policy

## Status

Draft decision policy for Phase 0. It prevents programming-language preference from becoming accidental product architecture.

## Governing principle

Atlas may use multiple programming languages, but only when a stable responsibility has a demonstrated need that outweighs the cost of another toolchain, runtime, contract, build path, security surface, and contributor skill requirement.

**Polyglot is permitted; premature polyglot is not.**

## Default position

For the first reference implementation:

1. prefer the smallest number of languages and processes;
2. keep domain semantics in one authoritative implementation;
3. preserve Markdown contracts independently from runtime choices;
4. measure actual bottlenecks before extracting specialized components;
5. introduce a boundary only after fixtures and compatibility tests exist.

A technically impressive design is not automatically a mature design.

## Required architecture decision record

Adding or assigning a language to an authoritative component requires an ADR containing:

- decision context;
- requirement being satisfied;
- responsibility and explicit non-responsibilities;
- alternatives considered, including extending the current language;
- expected benefit;
- measurable acceptance criteria;
- operational and maintenance costs;
- security and failure implications;
- data and process boundary;
- versioning and compatibility plan;
- rollback or replacement strategy;
- evidence from benchmarks, prototypes, or ecosystem constraints.

An ADR based only on “performance,” “safety,” “popularity,” or “best suited” is incomplete without a concrete workload and comparison.

## Decision dimensions

### Domain ownership

Which component owns each invariant? Domain rules must not be independently reimplemented across languages.

### Performance

Is there a measured workload that fails an accepted target? Include representative data size, latency, memory, throughput, startup, and build cost where relevant.

### Correctness and safety

Does the language materially reduce a demonstrated class of error? Explain which guarantees are provided and which remain procedural.

### Ecosystem fit

Does the component require mature libraries or tooling that would be expensive or unreliable elsewhere?

### Portability

Can the component run on the intended operating systems and packaging targets without unreasonable setup?

### Operability

How many runtimes, package managers, build systems, deployment units, logs, and failure modes are introduced?

### Maintainability

Can a contributor understand, test, and replace the component? Is the language boundary independently useful or merely organizational?

### Interoperability

How are data contracts versioned? What happens when one component is older, unavailable, or returns invalid output?

### Longevity

Can authoritative data outlive the implementation? Does the choice create format or vendor lock-in?

## Boundary requirements

A cross-language component must have:

- one clear owner of each semantic rule;
- a versioned contract;
- valid and invalid fixtures;
- compatibility tests;
- deterministic error behavior;
- bounded input and output;
- no hidden canonical state;
- a documented fallback or failure mode;
- independent usefulness sufficient to justify separation.

## Current prototype assessment

The existing components remain candidates, not approved final assignments.

### C++ graph engine

Potential strengths:

- explicit control of graph representation and invariants;
- portable native execution;
- predictable resource behavior.

Unproven assumptions:

- that Atlas requires a native core at its initial scale;
- that C++ maintenance and safety costs are justified;
- that graph traversal is the dominant workload;
- that the current concept-level model is the correct domain boundary.

### Rust search service

Potential strengths:

- memory-safe native indexing;
- strong concurrency and search ecosystem options.

Unproven assumptions:

- that search requires a separate native process;
- that an embedded index or single-language implementation is insufficient;
- that the operational boundary is worth the compatibility burden.

### Python ingestion

Potential strengths:

- rapid development of parsers, validation, research tooling, and data transformations.

Unproven assumptions:

- that ingestion should be a separate package rather than the first reference implementation;
- that Python-specific metadata rules will not leak into the canonical contract.

### TypeScript API and interface

Potential strengths:

- shared browser and server types;
- strong web tooling;
- accessible interface development.

Unproven assumptions:

- that an HTTP process or browser UI is needed before the content model stabilizes;
- that runtime orchestration belongs in Node rather than a later application shell.

### SQL and SQLite

Potential strengths:

- transactions, constraints, querying, indexing, and local durability.

Unproven assumptions:

- that the ontology and revision model are stable enough to encode;
- that relational persistence should be canonical rather than derived.

## Phase 0 rule for the current code

- Preserve it as a tested prototype.
- Do not expand it with new features.
- Do not use its data structures to define the ontology.
- Use it only to identify requirements, failure modes, and contract gaps.
- Expect parts to be rewritten, merged, or removed after foundation review.

## Approval gate for a polyglot boundary

A language boundary is approved only when:

1. the canonical content and knowledge contracts are already defined;
2. representative fixtures exist;
3. a single-runtime baseline has been measured or convincingly ruled out;
4. the proposed component has a stable responsibility;
5. acceptance criteria show a material advantage;
6. compatibility and failure tests exist;
7. maintenance cost is documented;
8. the decision is reversible without changing authoritative knowledge.

## Prohibited patterns

- separate languages implementing the same domain parser;
- a service boundary used only to showcase a language;
- database tables becoming the undocumented ontology;
- generated JSON becoming more authoritative than Markdown;
- performance claims without representative benchmarks;
- introducing an AI framework before evidence and review contracts exist;
- adding a plugin system before contracts are versioned;
- treating the current prototype as sunk cost that must be preserved.
