# Atlas Project State

## Current status

**Phase 0 — Knowledge Foundation (verification-ready mature draft)**

Atlas has a substantially defined knowledge and editorial foundation, but Phase 0 is not complete. The project has moved from broad conceptual design into verification, fixture splitting, and independent review.

The existing C++, Rust, Python, TypeScript, SQL, and UI work remains an **experimental prototype**. It may inform later architecture comparisons but is not authoritative and remains feature-frozen.

## Development freeze

Until Phase 0 closes:

- do not add product features, interfaces, services, plugins, or programming languages;
- do not expand `.atlas`, SQL, or runtime models as canonical contracts;
- do not duplicate semantic rules across implementations;
- do not promote reference content beyond `draft` without required review;
- keep authored Markdown and foundation decisions authoritative.

Allowed work:

- fixture splitting and validation;
- source, editorial, domain, method, reproducibility, ethics, and translation review;
- contract consistency corrections;
- migration and staleness fixtures;
- ADR comparison for the smallest Phase 1 validator;
- prototype bug fixes needed for inspection or comparison.

## Authority order

1. `PROJECT_STATE.md`
2. `docs/foundation/`
3. accepted ADRs
4. reviewed canonical content and fixtures
5. implementation code and generated artifacts

When code conflicts with the foundation, code is provisional.

## Foundation now defined

- product charter and explicit non-goals;
- canonical entity set and invariants;
- `atlas-content/0.1` authoring contract;
- claim-level evidence and provenance;
- controlled relation direction and compatibility;
- lifecycle, review roles, conflicts, and reviewer disagreement;
- multilingual identity and translation review;
- claim granularity and embedded argument structure;
- evidence access, copyright, private sources, units, data, and transformation lineage;
- confidence and domain-appropriate uncertainty;
- contract versioning and migration invariants;
- revision impact, dependency propagation, and staleness states;
- architecture and language-admission policy;
- evidence-based phase gates;
- prototype audit;
- decision register;
- invalid fixture catalog with expected diagnostics.

## Reference corpus

Three bundled draft vertical slices now exercise the model:

1. **Catalase and assay conditions** — empirical and synthetic observation, measurement proxies, biological scope, and method limitations.
2. **Delayed feedback and oscillation** — formal model, exact derived evidence, assumptions, reproducibility, and analogy limits.
3. **Recommendation systems and user choice** — observational and randomized evidence, platform conflicts, legal context, contested interpretation, and normative values.

Location: `content/reference/`.

These slices are ontology tests, not reviewed educational content.

## Resolved former blockers

Accepted policies now resolve:

- authoring language and translation identity;
- evidence excerpt and restricted-source handling;
- claim granularity;
- argument representation for `0.1`;
- quantitative evidence and transformation lineage;
- review authority and reviewer disagreement;
- revision-impact propagation;
- exact scope of the first three vertical slices;
- initial contract version and migration policy.

## Remaining major blockers

1. Split bundled slices into one canonical file per entity without semantic change.
2. Independently verify source metadata, locators, and evidence descriptions.
3. Record structural, editorial, domain, methodological, reproducibility, ethics, and translation review.
4. Create a complete Indonesian translation path and stale-translation fixture.
5. Create concrete mechanical and semantic migration fixtures.
6. Execute invalid fixtures through a deterministic validator.
7. Test identifier alias, rename, collision, and federation behavior.
8. Resolve open questions on formal expressions, protocol representation, and legal interpretation lifecycle where required by fixtures.
9. Compare validator implementation options and accept one ADR.
10. Produce a signed Phase 0 completion report.

## Phase 0 exit gate

Phase 0 closes only when:

- canonical records are split and structurally valid;
- every material factual claim can be traced to reviewed evidence and source;
- relation direction and pair compatibility pass fixtures;
- multilingual, migration, and staleness behavior are demonstrated;
- required review findings contain no unresolved critical or major issue;
- derived-output reproducibility requirements are implementable without changing authored meaning;
- the smallest Phase 1 validator is selected through an accepted ADR;
- a completion report recommends entry into Phase 1.

## Next work order

1. Split the three bundles into canonical records.
2. Add the Indonesian translation and stale-source case.
3. Add migration and identity fixtures.
4. Conduct manual review and record findings.
5. Write the validator ADR from fixture requirements.
6. Build only the approved Phase 1 validator.
7. Run the completion gate.

**Product development remains frozen. Phase 0 is mature enough for verification, not complete enough for implementation expansion.**
