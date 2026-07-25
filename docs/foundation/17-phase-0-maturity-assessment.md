# Phase 0 Maturity Assessment

## Assessment status

**Assessment date:** 2026-07-26  
**Foundation state:** mature draft, not complete  
**Recommendation:** continue Phase 0 review; do not resume product feature development

This report evaluates whether Atlas has moved from an idea and prototype into a sufficiently explicit knowledge foundation. It does not certify scientific accuracy of the reference slices and does not approve an implementation architecture.

## Maturity scale

- **Undefined** — requirement is absent or determined accidentally by implementation.
- **Defined** — policy or contract exists.
- **Exercised** — representative positive or negative fixtures use the rule.
- **Reviewed** — appropriate human review has evaluated the rule and fixtures.
- **Accepted** — evidence and review are sufficient for the current phase gate.

## Executive assessment

Atlas Phase 0 is now **structurally mature enough for serious review**. The project has:

- an explicit product charter and non-goals;
- a differentiated ontology;
- claim-level evidence and relation semantics;
- lifecycle, uncertainty, review, translation, access, migration, and staleness rules;
- three materially different vertical slices;
- invalid fixtures with expected diagnostics;
- a decision process preventing languages and storage from defining knowledge accidentally.

Phase 0 is **not complete** because:

- reference slices remain bundled and unreviewed;
- source locators and interpretations need independent verification;
- relation compatibility has not been executed by a validator;
- multilingual behavior has policy but no complete Indonesian translation fixture;
- migration behavior has policy but no executable or manually verified before/after fixture;
- first validator architecture remains intentionally undecided;
- no independent reviewer has signed the completion gate.

## Gate assessment

| Gate | State | Evidence | Remaining work |
|---|---|---|---|
| Product purpose and non-goals | defined | `00-charter.md` | editorial review and user-scenario challenge |
| Canonical entity meanings | exercised | ontology plus three slices | split bundles into entity fixtures; review whether argument or protocol needs entity status |
| Stable identity | exercised | language-specific `id` plus shared `work` policy | alias, rename, collision, and federation fixtures |
| Claim-level provenance | exercised | all three slices | independent source and domain review |
| Evidence access and copyright | defined | access classes and excerpt policy | restricted-source fixture with metadata-only review |
| Quantitative evidence lineage | exercised | catalase measurement proxy and feedback sequence | missing-data and conversion fixtures with expected output |
| Claim atomicity and scope | exercised | observation, model-derived, causal, interpretive, and normative claims | editorial calibration across reviewers |
| Argument representation | exercised | feedback and recommender argument blocks | decide after split fixtures whether embedding creates duplication |
| Relation vocabulary | exercised | all slices and invalid reversed-support fixture | machine compatibility validation and ambiguous-pair tests |
| Uncertainty and confidence | exercised | scoped confidence across three domains | reviewer calibration and formal uncertainty examples |
| Review governance | defined | role, outcome, conflict, disagreement, and staleness policies | independent review records on actual slice revisions |
| Multilingual authoring | defined | translation identity policy | one complete Indonesian translation with stale-source test |
| Revision impact | defined | material/navigational dependency and staleness rules | dependency-path fixtures and review outcome records |
| Contract versioning | defined | `atlas-content/0.1` and migration policy | concrete 0.1-to-0.2 sample migration |
| Positive reference corpus | exercised | three vertical slices | canonical file split and review |
| Negative fixture corpus | exercised | 24 invalid scenarios | validator diagnostic implementation and snapshot tests |
| Derived-format independence | defined | authority and compilation rules | clean rebuild demonstration after Phase 1 validator exists |
| Implementation restraint | accepted | feature freeze and architecture policy | maintain freeze until gate closure |

## Reference slice assessment

### Slice A — catalase and assay conditions

**Strengths**

- separates source, published evidence, synthetic observation, proxy measurement, claim, concept, model, and synthesis;
- prevents a classroom proxy from being presented as purified enzyme kinetics;
- exposes method, organism, temperature, pH, and assay scope;
- identifies protocol representation as an ontology question.

**Review risks**

- full-text source interpretation has not been independently checked;
- one bibliographic record requires author-field completion during source review;
- confidence labels need biochemistry and methodology review;
- the synthetic observation must remain visually and semantically separated from factual evidence.

### Slice B — delayed feedback model

**Strengths**

- contains a reproducible model-derived sequence;
- separates exact arithmetic from real-world inference;
- makes assumptions and failure modes explicit;
- tests formal evidence, argument mode, analogy, and model scope.

**Review risks**

- stability terminology needs control-systems review;
- equation representation remains plain text;
- exact sequence should be independently recalculated;
- broader claims about delay must not exceed the one demonstrated recurrence.

### Slice C — recommender exposure and autonomy

**Strengths**

- distinguishes observational and randomized evidence;
- preserves platform, population, outcome, and period scope;
- records employment and data-access conflicts;
- separates empirical, interpretive, legal, and normative claims;
- exposes autonomy, transparency, and control as values, not automatic deductions from data.

**Review risks**

- source and legal locators require independent verification;
- “amplification,” “exposure,” “choice,” and “autonomy” require careful terminology review;
- legal provisions may change or acquire new authoritative interpretations;
- normative alternatives require ethical review rather than majority preference.

## Cross-document consistency findings

### Resolved

- relation vocabulary is now a single source of truth;
- evidence `supports` claim direction is consistent;
- translations no longer share review status automatically;
- argument is explicitly embedded rather than accidentally omitted;
- lifecycle status and staleness are separate;
- contract, runtime, and application versions are separate;
- quantitative evidence and restricted evidence use the same provenance core;
- implementation languages are candidates rather than ontology owners.

### Remaining consistency work

- update the content contract examples to include `contract` and `work` consistently in every entity template;
- align all confidence examples with the same rationale fields;
- decide whether `source.kind: methodological-reference` belongs in the controlled source-type vocabulary;
- add review-horizon behavior to time-sensitive legal and platform claims;
- add terminology records for translated technical terms;
- test whether `supersedes` belongs as a relation, revision field, or both.

These are major editorial tasks but are not evidence that the ontology must be discarded.

## Critical and major blockers

### Critical blockers

None identified in the current draft. No known rule requires loss of identity, evidence, review history, or authored meaning.

### Major blockers

1. No independent structural, source, domain, methodological, translation, or ethical review has been recorded.
2. Bundled slices are not yet split into canonical records.
3. No validator has executed the invalid fixture diagnostics.
4. No migration fixture demonstrates identity and review preservation.
5. No complete multilingual vertical slice exists.
6. First reference implementation has no accepted ADR.

Phase 0 cannot close while these remain.

## Phase 0 completion work package

### Work package A — canonical fixture split

Split each bundled slice into entity files without changing meaning. Generate a provenance manifest showing the mapping from bundle sections to canonical IDs.

### Work package B — manual contract review

Apply structural, editorial, source, domain, methodological, reproducibility, ethical, and translation review where required. Record findings rather than editing them away silently.

### Work package C — migration and multilingual tests

- create one Indonesian translation of a complete claim-evidence-concept path;
- revise its source-language claim and verify stale translation behavior;
- create a synthetic `0.1` to `0.2` migration changing one optional field;
- create a semantic migration fixture splitting one compound claim.

### Work package D — validator ADR

Compare the smallest credible implementation options against:

- YAML/Markdown parsing reliability;
- deterministic diagnostics;
- schema and semantic validation;
- contributor setup;
- existing prototype reuse;
- future generated outputs;
- avoidance of duplicated domain logic.

Do not select the language before this comparison.

### Work package E — completion report

Produce a signed gate table with:

- fixture locations;
- review records;
- pass, fail, or deferred result;
- migration results;
- unresolved major findings;
- accepted validator ADR;
- recommendation to enter or remain outside Phase 1.

## Recommendation

The Phase 0 foundation is now mature enough to stop broad conceptual expansion and begin **verification and review**. New ontology ideas should be accepted only when one of the three slices or a negative fixture demonstrates a real gap.

The correct next move is not more architecture or UI. It is to split, validate, review, translate, migrate, and challenge the current foundation until the remaining major blockers are resolved.
