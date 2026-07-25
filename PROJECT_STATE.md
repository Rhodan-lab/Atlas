# Atlas Project State

## Current status

**Phase 0 — Knowledge Foundation (active)**

Atlas is not yet treated as a finished software architecture. The existing C++, Rust, Python, TypeScript, SQL, and UI work is preserved as an **experimental prototype**. It may inform later decisions, but it is not the authoritative foundation and must not determine the knowledge model by accident.

## Development freeze

Until Phase 0 is complete:

- do not add product features, services, interfaces, plugins, or programming languages;
- do not expand the current `.atlas` format as if it were final;
- do not duplicate domain rules across language implementations;
- do not describe prototype components as completed product phases;
- keep authored knowledge and foundation documents in Markdown as the source of truth.

Bug fixes that prevent repository validation are allowed. New behavior requires a documented foundation decision first.

## Authoritative material

During Phase 0, authority is ordered as follows:

1. `PROJECT_STATE.md`
2. `docs/foundation/`
3. accepted architecture decision records
4. reviewed content contracts and reference examples
5. implementation code and generated artifacts

When code conflicts with the foundation documents, the code is considered provisional.

## Phase 0 objectives

1. Define exactly what Atlas is and is not.
2. Define the units of knowledge Atlas must represent.
3. Separate sources, evidence, claims, concepts, relations, models, questions, and syntheses.
4. Define provenance, uncertainty, contradiction, revision, and scientific review rules.
5. Define a stable authoring contract before a compiled storage format.
6. Build representative reference material that tests the model across different domains.
7. Choose implementation languages only after boundaries and measurable needs are established.

## Required foundation outputs

- product charter and non-goals;
- canonical knowledge model and invariants;
- evidence and editorial policy;
- Markdown content contract;
- language and architecture decision policy;
- phased delivery gates;
- audit of the current prototype;
- unresolved decision register;
- reference vertical slices covering source → evidence → claim → concept → relation → synthesis.

## Phase 0 exit gate

Phase 0 is complete only when:

- every canonical entity has a clear purpose, required fields, lifecycle, and identity rule;
- evidence can support or challenge individual claims rather than only whole concepts;
- uncertainty and disagreement can be represented without forcing false certainty;
- Markdown examples can express at least three complete cross-domain knowledge trails;
- a reviewer can trace every reviewed factual claim back to its source material;
- generated formats are explicitly derived and reproducible;
- the minimum runtime boundary is selected through an architecture decision, not preference;
- no unresolved issue blocks the first reference implementation.

## Next permitted work

The next work is documentation, ontology testing, and representative content modeling. Full software development resumes only after the Phase 0 gate is passed.
