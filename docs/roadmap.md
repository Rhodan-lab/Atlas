# Atlas Roadmap

## Roadmap status

Atlas uses **evidence-based phase gates**, not a feature checklist. Authoritative definitions are in [`docs/foundation/05-phase-gates.md`](foundation/05-phase-gates.md).

The C++, Rust, Python ingestion, TypeScript, SQL, `.atlas`, and browser work remains an experimental prototype. It is maintained for regression and comparison, not counted as completed product architecture.

The active authored corpus is English-only. Language-neutral translation semantics remain dormant infrastructure and may be exercised only through synthetic fixtures until a later phase explicitly reopens multilingual authoring.

## Phase 0 — Knowledge foundation

**Status: accepted for `atlas-content/0.1`**

Completed foundation outputs:

- charter and non-goals;
- canonical entity model and invariants;
- claim-level evidence and provenance;
- evidence, review, disagreement, revision, translation, migration, and staleness governance;
- governed relation vocabulary;
- language-qualified identity with shared work IDs;
- versioned authored Markdown contract;
- three split English canonical vertical slices;
- invalid, migration, identity, federation, and synthetic stale-translation fixtures;
- accepted minimum validator ADR;
- deterministic Python 3.11/3.13 validation matrix;
- source-verification and review registers;
- closure report.

Phase 0 acceptance stabilizes the foundation. It does not promote example content from `draft`.

### Language amendment

The Phase 0 contract retains multilingual capability, but the active corpus and current review program use English only. Future multilingual work requires an explicit reopening decision, reviewer plan, terminology governance, and migration assessment.

## Phase 1 — Reviewed English reference corpus and validator hardening

**Status: active**

Primary work:

- execute revision-specific source, editorial, domain, methodological, reproducibility, ethical, legal-context, and conflict reviews;
- preserve reviewer disagreement and conflicts;
- promote only entities that pass required review types;
- calibrate confidence and domain-native uncertainty;
- exercise contradiction, deprecation, retraction, and revision impact;
- harden deterministic diagnostics, coverage, and provenance reports;
- generate review backlogs that separate automation-eligible and human-required work;
- expand migration and identity fixtures when review exposes real gaps;
- reopen Phase 0 decisions when evidence demonstrates ontology failure;
- derive minimal knowledge-kernel requirements from reviewed workflows.

Current reference goal:

- bring the complete English delayed-feedback vertical slice through sufficient exact-revision review coverage;
- keep both the formal result and its model-to-world inference boundary load-bearing;
- produce a Phase 1 completion report before entering Phase 2.

Non-scope:

- product UI expansion;
- specialized search architecture;
- synchronization or plugins;
- active translated corpus or language-specific review programs;
- autonomous synthesis;
- new programming-language boundaries;
- live Principia integration.

## Phase 2 — Minimal knowledge kernel

Implement only the dependable runtime required by reviewed Phase 1 workflows.

Expected outcomes:

- canonical-to-runtime compilation;
- read-only entity repository;
- typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- deterministic command or library interface;
- compatibility and failure tests;
- representative performance measurements.

The kernel must remain replaceable without changing authored Markdown.

## Phase 3 — Retrieval and research trails

Add inspectable retrieval after the knowledge kernel is dependable.

Expected outcomes:

- lexical baseline and documented relevance tests;
- field-, status-, and evidence-aware ranking;
- filters and saved research trails;
- contradiction and duplicate candidates;
- ranking explanations;
- specialized indexing only after benchmark approval.

## Phase 4 — Principia & Atlas interactive experience

Build interfaces over proven semantics.

Expected outcomes:

- Atlas evidence, claim, model, review, revision, and provenance views;
- Principia long-form explanation, pathways, investigations, simulations, and system dossiers;
- explicit bridge references and dependency-impact warnings;
- accessible exploration without mandatory graph visualization;
- visible review status, uncertainty, provenance, and staleness;
- local-first packaging.

The two domains may share one product identity without erasing their separate authority boundaries.

## Phase 5 — Assisted synthesis and extensions

Introduce advanced assistance only after authority and governance are dependable.

Possible outcomes:

- AI-assisted draft extraction and synthesis;
- citation-aware research workflows;
- domain-specific validators and model adapters;
- synchronization preserving local ownership;
- permissioned plugins;
- multilingual authoring only after an accepted reopening gate.

AI output remains draft until reviewed and cannot bypass source verification.

## Global non-goals until prerequisites exist

- autonomous rewriting of authoritative knowledge;
- opaque vector-only retrieval;
- mandatory cloud accounts;
- polished visual design before reviewed workflows;
- plugin marketplaces before versioned contracts and permissions;
- active language expansion without accountable review capacity;
- describing machine conformance as scientific validity.

## Progress rule

A phase is complete only when its own authority boundary and exit criteria are demonstrated. Code quantity, language count, screenshots, or build success are not sufficient measures of maturity.
