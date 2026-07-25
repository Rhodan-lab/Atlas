# Atlas

[![Atlas CI](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/Rhodan-lab/Atlas/actions/workflows/ci.yml)

> **Current status: Phase 0 — Knowledge Foundation**
>
> Feature development is intentionally frozen while the product charter, ontology, evidence model, review policy, content contract, and architecture gates are matured.

## What Atlas is

Atlas is a local-first knowledge environment for an independent learner, researcher, or builder. Its purpose is to make knowledge inspectable:

- what a claim means;
- what evidence supports or challenges it;
- how limited or uncertain it is;
- how it connects to concepts and models;
- where credible disagreement remains;
- how understanding changes through revision.

Atlas is not merely a notes application, graph visualization, textbook, course platform, or chatbot. The long-term product should allow a user to trace a path from question to synthesis and from every important claim back to evidence and original sources.

## Why the project returned to Phase 0

The repository already contains an experimental C++, Rust, Python, TypeScript, SQL, and browser prototype. That prototype proves that local ingestion, graph traversal, search, process boundaries, and testing are possible.

It does **not** yet prove that the underlying knowledge model is mature.

The first implementation moved too quickly from an idea to a polyglot architecture. In particular, it treated broad concepts and concept-level source references as the center of the system before defining claim-level evidence, disagreement, review, models, questions, syntheses, and revisions.

The prototype is therefore preserved, tested, and explicitly classified as **non-authoritative experimental work**. The foundation documents now govern future engineering.

## Authority order

During Phase 0, project authority is:

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/`](docs/foundation/)
3. accepted architecture decision records
4. reviewed content contracts and reference fixtures
5. implementation code and generated artifacts

When code conflicts with the foundation, the code is provisional.

## Canonical knowledge units

The foundation currently distinguishes:

- **Source** — identifiable origin of information
- **Evidence** — the relevant passage, observation, measurement, or data context
- **Claim** — an individually evaluable statement
- **Concept** — an explanatory structure organizing claims and meaning
- **Relation** — a governed typed and directed connection
- **Model** — a representation used to explain, calculate, simulate, or predict
- **Question** — an explicit knowledge need or unresolved problem
- **Synthesis** — a scoped integration of claims, evidence, models, and disagreement
- **Revision** — a traceable change and its consequences

These distinctions are more important than any current storage format or language choice.

## Foundational lenses

Atlas is intended to connect knowledge through recurring lenses rather than a rigid school-subject sequence:

- knowledge and evidence;
- logic and argument;
- mathematics;
- statistics and uncertainty;
- scientific inquiry;
- systems;
- computation;
- language and meaning;
- human cognition;
- decision and action;
- ethics and responsibility.

This is a map for exploration, not a fixed course with grades, scores, streaks, or a final test.

## Foundation reading order

1. [`PROJECT_STATE.md`](PROJECT_STATE.md)
2. [`docs/foundation/00-charter.md`](docs/foundation/00-charter.md)
3. [`docs/foundation/01-knowledge-model.md`](docs/foundation/01-knowledge-model.md)
4. [`docs/foundation/02-evidence-and-editorial-policy.md`](docs/foundation/02-evidence-and-editorial-policy.md)
5. [`docs/foundation/03-content-contract.md`](docs/foundation/03-content-contract.md)
6. [`docs/foundation/04-language-and-architecture-policy.md`](docs/foundation/04-language-and-architecture-policy.md)
7. [`docs/foundation/05-phase-gates.md`](docs/foundation/05-phase-gates.md)
8. [`docs/foundation/06-current-prototype-audit.md`](docs/foundation/06-current-prototype-audit.md)
9. [`docs/foundation/07-decision-register.md`](docs/foundation/07-decision-register.md)

Contributors and agents must also follow [`AGENTS.md`](AGENTS.md).

## Current repository structure

```text
Atlas/
├── docs/foundation/      # authoritative Phase 0 product and knowledge foundation
├── PROJECT_STATE.md      # active phase, authority, freeze, and exit gate
├── AGENTS.md             # mandatory contributor and agent rules
├── engine/cpp/           # experimental graph-engine prototype
├── services/search-rs/   # experimental search prototype
├── tools/ingest-py/      # experimental ingestion prototype
├── apps/api-ts/          # experimental API and browser prototype
├── contracts/            # provisional derived-format contracts
├── storage/              # provisional persistence design
├── examples/notes/       # prototype examples; not yet canonical fixtures
└── scripts/              # prototype build and integration checks
```

## Development rule

Until the Phase 0 gate is passed:

- do not add product features, services, plugins, or languages;
- do not promote new content beyond `draft` without its required review;
- do not make `.atlas`, SQL, or runtime models more authoritative than Markdown;
- do not introduce a language boundary without an ADR, baseline, and measurable need;
- focus on ontology testing, evidence governance, content fixtures, and decision closure.

## Next milestone

The next milestone is not a larger application. It is a reviewed **reference foundation** containing at least three complete vertical slices:

```text
question → source → evidence → claim → concept/model → cross-domain relation → synthesis → limitation
```

Only after those examples prove the contract will Atlas select the smallest reference implementation and reassess which parts of the current prototype deserve to survive.

## Prototype validation

The existing prototype remains buildable for comparison and regression testing:

```bash
./scripts/check.sh
```

Passing prototype tests means the experiment is internally consistent. It does not mean the product foundation is complete.

## License

MIT
