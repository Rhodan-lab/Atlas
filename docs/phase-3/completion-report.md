# Phase 3 Completion Report — Retrieval and Research Trails

## Status

Closure candidate with pinned deterministic evidence.

```yaml
phase: 3
mode: retrieval-evaluation
state: closure-candidate
decision: proceed-phase4-interactive-experience
preferred_bounded_retrieval: structured-field-baseline
semantic_infrastructure_decision: defer-until-broader-benchmark-and-architecture-approval
retrieval_authority: advisory-only
exact_revision_required: true
live: false
repository_mutation: false
```

## Pinned closure evidence

The completion report was generated independently on Python 3.11 and Python 3.13. The substantive JSON artifacts were byte-identical.

```yaml
report_contract: atlas-phase3-completion-report/0.1
report_digest: 3823a2283bbecdc7a407c720e7ef60898a734253f0738442b365036e20401a70
report_artifact_sha256: 7b2029987c3fd1adf926df33bdf0232967260ad1c1b0332d88abd52cc7051de5
report_artifact_bytes: 5244
python_versions: [3.11, 3.13]
python_reports_byte_identical: true
exit_gate_count: 8
all_exit_gates_passed: true
```

Passed gates:

- documented relevance collection;
- visible review status and provenance;
- explainable ranking behavior;
- specialized boundaries passing architecture policy;
- retrieval failure unable to corrupt authority;
- operational filters and research trails;
- advisory candidate discovery;
- replaceable generated artifacts.

## Purpose

Determine whether Atlas has enough evidence to leave retrieval foundation work and begin Phase 4 — the Principia & Atlas interactive experience — without overstating search quality or weakening canonical authority.

## Completed scope

Phase 3 now contains:

- a versioned 34-entity, 13-query relevance collection;
- deterministic lexical BM25F retrieval;
- deterministic structured-field BM25F retrieval;
- exact-revision results with provenance, review, lifecycle, staleness, matched fields, and explanations;
- deterministic filters by entity type, status, domain, updated date, and evidence role;
- saved exact-revision research trails;
- advisory contradiction candidates;
- advisory duplicate candidates;
- one predeclared comparative rank-fusion experiment;
- explicit failure and replaceability tests.

## Preferred bounded retrieval

The accepted structured-field baseline remains preferred for the current fixture.

```yaml
precision_at_5: 0.366666666667
recall_at_5: 0.854166666667
mean_reciprocal_rank: 0.770833333333
ndcg_at_5: 0.754777384811
zero_result_rate: 0.0
unavailable_revision_rate: 1.0
tie_count: 0
canonical_body_indexed: false
external_services: false
embeddings: false
vector_database: false
replaceable: true
```

This is bounded fixture evidence, not a production-search quality claim.

## Comparative experiment

Equal-weight reciprocal-rank fusion was declared before evaluation and rejected afterward.

It improved all core metrics over lexical retrieval, but reduced all core metrics relative to structured retrieval. The negative result is retained rather than repaired through post-hoc weight tuning.

```yaml
candidate: equal-weight-reciprocal-rank-fusion
decision: rejected
recommendation: reject-candidate-no-quality-gain-over-structured
query_gains_vs_structured: 2
query_mixed_vs_structured: 1
query_regressions_vs_structured: 7
query_unchanged_vs_structured: 2
```

## Research foundations

Workstream 5 adds deterministic research workflow foundations:

```yaml
filters: 4
filter_result_items: 9
research_trails: 1
trail_entries: 5
contradiction_candidates: 1
duplicate_candidates: 1
negative_cases: 5
```

The contradiction candidate resolves only to `scope-difference-likely`; the duplicate candidate resolves only to `related-not-duplicate`. These outcomes preserve candidate uncertainty and prove that the system does not force an assertion.

Trails remain research-only exact-revision references. Candidate records remain advisory. Automatic merge, resolution, lifecycle change, or canonical copying is forbidden.

## Phase 3 exit gates

The closure proof maps the authoritative gates in `docs/foundation/05-phase-gates.md` to executable evidence:

1. **Documented relevance collection** — accepted query and judgment contract.
2. **Review status and provenance remain visible** — every ranked item exposes exact revision, lifecycle, staleness, review level, provenance, and canonical metadata.
3. **Ranking is explainable** — every result exposes matched fields and deterministic explanation evidence; ties are counted and deterministic.
4. **Specialized boundaries pass policy** — no external search service, embedding, learned model, or vector database was adopted; the added fusion layer was rejected by evidence.
5. **Retrieval failure cannot corrupt authority** — unavailable revisions fail explicitly, indexes are generated and replaceable, trails cannot copy canonical authority, and candidates cannot mutate knowledge state.
6. **Filters and trails are operational** — deterministic exact-revision fixtures and negative cases pass.
7. **Candidate discovery remains advisory** — contradiction and duplicate candidates require evidence and rationale without automatic resolution.
8. **Generated artifacts remain replaceable** — accepted indexes and reports can be deleted and deterministically rebuilt from canonical content and pinned fixtures.

## Semantic infrastructure decision

Embedding, vector, learned-ranking, and external semantic services are deferred.

The current collection is too small to justify infrastructure commitment. A future semantic experiment requires:

- a broader corpus and query set;
- hard negatives and candidate-discovery benchmarks;
- explicit comparison on quality, determinism, inspectability, latency, storage, failure behavior, and replaceability;
- a separate architecture decision.

## Phase 4 entry boundary

Phase 4 may build the unified Principia & Atlas interactive experience under these constraints:

```yaml
atlas_semantics_authoritative: true
principia_status_separate: true
exact_cross_repository_references: true
impact_warnings_required: true
graph_visualization_optional: true
accessibility_and_failure_tests_required: true
local_first: true
production_retrieval_quality_claim: false
vector_database: false
live_principia_dependency: false
canonical_mutation: false
```

Phase 4 should expose proven semantics rather than redefine them. Atlas remains the knowledge and governance layer. Principia remains the explanation, pathway, investigation, simulation, dossier, failure-analysis, and design-experience layer.

## Recommendation

Proceed to **Phase 4 — Principia & Atlas interactive experience** using:

- the accepted canonical and kernel contracts;
- structured-field retrieval as the preferred bounded baseline;
- exact-revision filters and research trails;
- advisory candidate discovery;
- separate Atlas and Principia status;
- local-first, accessible, failure-visible interaction design.

Do not activate production claims, semantic infrastructure, live cross-repository dependency, canonical writes, or automatic authority.
