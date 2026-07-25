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
3. Separate sources, evidence, claims, concepts, relations, models, questions, syntheses, and revisions.
4. Define provenance, uncertainty, contradiction, revision, and scientific review rules.
5. Define a stable authoring contract before a compiled storage format.
6. Build representative reference material that tests the model across different domains.
7. Choose implementation languages only after boundaries and measurable needs are established.

## Current foundation progress

### Drafted

- product charter and non-goals;
- canonical knowledge model and invariants;
- evidence and editorial policy;
- authoritative Markdown contract;
- controlled relation vocabulary;
- language and architecture decision policy;
- evidence-based phase gates;
- current-prototype audit;
- decision register;
- reference-slice plan;
- validation matrix;
- ADR template;
- contributor and agent governance.

### Not yet complete

- representative canonical content fixtures;
- three complete vertical slices;
- cross-document editorial review;
- domain review of the reference slices;
- contract version and migration policy;
- Phase 0 completion report;
- accepted decision for the first validator implementation.

Drafted means the material exists for review. It does not mean the foundation has passed its gate.

## Current blocking decisions

The most important unresolved items are recorded in `docs/foundation/07-decision-register.md`. Before the reference corpus grows, Phase 0 should resolve or deliberately constrain:

- canonical authoring-language and translation policy;
- evidence excerpt and restricted-source handling;
- claim granularity;
- whether argument needs a separate entity type;
- quantitative dataset and transformation metadata;
- review authority and reviewer disagreement;
- revision-impact propagation;
- exact scope of the first three vertical slices.

Implementation-language selection is intentionally blocked until the content and validation work exposes stable requirements.

## Required foundation outputs

- product charter and non-goals;
- canonical knowledge model and invariants;
- evidence and editorial policy;
- Markdown content contract;
- governed relation vocabulary;
- language and architecture decision policy;
- phased delivery gates;
- audit of the current prototype;
- unresolved decision register;
- reference vertical slices covering source → evidence → claim → concept or model → relation → synthesis;
- foundation validation report.

## Phase 0 exit gate

Phase 0 is complete only when:

- every canonical entity has a clear purpose, required fields, lifecycle, and identity rule;
- evidence can support or challenge individual claims rather than only whole concepts;
- uncertainty and disagreement can be represented without forcing false certainty;
- Markdown examples express at least three complete cross-domain knowledge trails;
- a reviewer can trace every reviewed factual claim back to its source material;
- relation direction and compatibility are validated consistently;
- generated formats are explicitly derived and reproducible;
- the minimum runtime boundary is selected through an architecture decision, not preference;
- no unresolved critical or major issue blocks the first reference implementation.

## Next permitted work

1. Review the foundation documents for internal consistency.
2. Resolve the blocking decisions needed by the three reference slices.
3. Author questions and source records before claims or concepts.
4. Build valid and invalid Markdown fixtures.
5. Apply the validation matrix and revise the ontology based on failures.
6. Produce the Phase 0 completion report.

Full software development resumes only after the Phase 0 gate is passed.
