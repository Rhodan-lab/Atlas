# Foundation Validation Matrix

## Purpose

This matrix turns foundation statements into testable obligations. Phase 0 documents are not considered mature merely because they are detailed; representative fixtures must demonstrate that their rules are usable and non-contradictory.

| Area | Foundation requirement | Positive fixture | Negative fixture | Review needed | Phase gate |
|---|---|---|---|---|---|
| Identity | Canonical IDs remain stable when files move or reorder | same entities compiled from reordered files | identity changes because numeric order changes | structural | Phase 0 |
| Entity separation | Source, evidence, claim, concept, model, question, synthesis, and revision retain distinct roles | full vertical slice | concept page containing untraceable mixed assertions | structural + editorial | Phase 0 |
| Evidence | Evidence has source, locator, context, and role | evidence supporting a scoped claim | source URL attached without relevant locator | source | Phase 0 |
| Claims | Claims are atomic and qualified | one causal statement with conditions | compound statement containing unrelated assertions | editorial + domain | Phase 0 |
| Relations | Relation type, direction, and allowed entity pair are valid | claim supported by evidence | undefined relation or reversed prerequisite | structural + semantic | Phase 0 |
| Disagreement | Credible conflict remains visible | two claims linked by contradiction with scope comparison | one claim silently replacing the other | domain + editorial | Phase 0 |
| Review | New material begins as draft and records review types | reviewed item tied to a version | status changed to reviewed without record | structural + editorial | Phase 0 |
| Revision | Prior meaning and reason for change are preserved | revised claim linked to superseded version | history overwritten | editorial | Phase 0 |
| Synthesis | Conclusions trace to material claims and evidence | provenance path from synthesis to sources | summary with unsupported conclusion | source + domain | Phase 0 |
| Models | Assumptions, inputs, outputs, validation, and failure modes are visible | model-derived claim with assumptions | equation presented as universally applicable | methodological + domain | Phase 0 |
| Uncertainty | Confidence includes scope and rationale | claim with domain measure and explanation | unsupported global truth score | methodological | Phase 0 |
| Normative reasoning | Values are explicit and not presented as empirical deduction | recommendation with stated principles | “data proves what society should do” | ethical + editorial | Phase 0 |
| Compilation | Derived artifacts are reproducible | clean rebuild matches expected output | compiler changes meaning or promotes status | reproducibility | Phase 1 |
| Migration | Contract changes preserve provenance | fixture migrated with stable identity | migration drops evidence role | structural + editorial | Phase 1 |
| Retrieval | Search exposes status and provenance | reviewed and draft results clearly distinct | ranking hides contested status | relevance + editorial | Phase 3 |
| Architecture | A language boundary has measured justification | accepted ADR and compatibility fixtures | service added without baseline | architecture review | Phase 2+ |

## Validation layers

### Document consistency

Check that foundation documents use the same entity names, statuses, relation meanings, authority order, and phase definitions.

### Fixture validation

Create small valid and invalid Markdown examples for every row. Negative fixtures must fail for the intended reason rather than a coincidental parser error.

### Vertical-slice review

Evaluate the complete path from question to synthesis. Reviewers should be able to identify why each conclusion is present and which evidence could change it.

### Implementation independence

At least one fixture review must be performed without running the prototype. This confirms that authored knowledge is understandable outside the software.

### Rebuild validation

After Phase 1 begins, delete generated artifacts, rebuild them from authoritative Markdown, and compare deterministic output and provenance reports.

## Blocking severity

- **Critical** — could lose meaning, evidence, identity, review state, or revision history. Blocks the current phase.
- **Major** — produces ambiguity, misleading presentation, or inconsistent semantics. Blocks reviewed status.
- **Minor** — reduces clarity or ergonomics without changing meaning. May be deferred with a recorded issue.

## Phase 0 completion report

Before Phase 0 closes, produce a report containing:

- each matrix row and fixture location;
- pass, fail, or deferred status;
- reviewer and review type;
- discovered ontology changes;
- unresolved critical or major issues;
- decisions accepted or reopened;
- recommendation for the first reference implementation.
