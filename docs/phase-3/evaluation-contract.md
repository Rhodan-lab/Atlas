# Phase 3 Retrieval Evaluation Contract

## Status

```yaml
workstream: 1
mode: retrieval-evaluation
state: candidate
retrieval_authority: advisory-only
exact_revision_required: true
live: false
repository_mutation: false
```

This workstream defines the evidence boundary that every Phase 3 retrieval implementation must satisfy. It does not implement ranking, claim retrieval quality, select a vector database, activate synchronization, or change canonical knowledge.

## Contracts

### Query and judgment set

```text
atlas-retrieval-query-set/0.1
```

The query-set contract binds:

- a stable query-set ID and positive version;
- the exact canonical corpus contract and entity count;
- stable query IDs and English query text;
- an information-need statement;
- slice and difficulty metadata;
- ranked or expected-error outcomes;
- exact entity IDs and positive revisions;
- graded relevance rationales;
- explicit ambiguity records where needed;
- evaluation-only authority;
- `live: false` and `repository_mutation: false`.

The grade scale is:

```text
0 = nonrelevant
1 = marginally relevant context
2 = strongly relevant supporting material
3 = directly load-bearing answer target
```

For the pinned 34-entity corpus, every unlisted exact entity receives grade 0 for that query. This makes the judgment universe exhaustive for the pinned fixture version rather than silently treating unjudged documents as relevant or unknown.

### Retrieval result set

```text
atlas-retrieval-result-set/0.1
```

Every query receives exactly one response.

A ranked response must contain items with:

- consecutive rank starting at 1;
- finite, non-increasing score;
- exact entity ID and positive revision;
- canonical type, title, status, staleness, and review level;
- sorted unique matched fields;
- an inspectable explanation;
- sorted unique exact-revision provenance references.

Equal-score ties use ascending exact entity keys. An unavailable-revision query returns its expected deterministic error and may not contain ranked items.

Every result set binds a generated index contract, build digest, canonical source digest, replaceability declaration, and `canonical_mutation: false`.

### Metric report

```text
atlas-retrieval-metric-report/0.1
```

The metric contract requires:

- exact query-set ID and version;
- exact result-set SHA-256;
- a declared positive cutoff;
- complete ranked-query and expected-error coverage;
- precision at cutoff;
- recall at cutoff;
- mean reciprocal rank;
- normalized discounted cumulative gain at cutoff;
- zero-result rate;
- unavailable-revision rate;
- deterministic tie count.

Metric values are finite and bounded within `[0, 1]`. The contract does not prescribe an acceptable quality threshold yet; Workstreams 2 and 3 must establish evidence before a threshold decision.

## Reference fixture

The candidate fixture is:

```text
content/fixtures/phase3_retrieval/reference-query-set.v01.json
```

It contains:

```yaml
entity_count: 34
query_count: 13
ranked_query_count: 12
expected_error_query_count: 1
positive_judgment_count: 26
implicit_grade_zero_judgments: 382
```

Coverage:

```yaml
catalase: 4
feedback: 4
recommenders: 4
cross-slice: 1
```

Difficulty coverage:

```yaml
direct: 6
compositional: 4
ambiguous: 2
exact-revision-error: 1
```

## Query design

### Catalase

The catalase queries test:

- why an assay optimum cannot be universalized;
- why foam height is a proxy rather than purified kinetics;
- how experimental factors distort an observed assay signal;
- how retrieval should handle an underspecified optimum-temperature question.

### Delayed feedback

The feedback queries test:

- exact recurrence, parameter, and initial-history retrieval;
- the ordered-state proof of indefinite period-six repetition;
- the boundary between model behavior and real-system inference;
- deterministic rejection of unavailable revision 3 instead of substitution with revision 2.

### Recommendation systems

The recommender queries test:

- the Facebook network-ranking-click pathway;
- the Twitter randomized causal comparison;
- cross-platform generalization limits;
- the difference between empirical evidence and a contestable normative recommendation.

### Cross-slice reasoning

The cross-slice query tests whether retrieval can recognize a shared methodological pattern: catalase optimum claims and recommender effect claims both require explicit scope rather than universal generalization.

## Limitations

- The fixture covers only the current 34-entity English reference corpus.
- Judgments are authored evaluation fixtures, not human relevance consensus.
- The current set is too small for production-quality claims.
- No multilingual, adversarial, long-query, misspelling, or conversational cases are yet included.
- The exact set may evolve only through a new query-set version; existing judgments must not be silently rewritten.
- Grade 0 for unlisted entities is exhaustive only for this pinned corpus version.
- The fixture does not favor lexical, structured, embedding, vector, hybrid, or learned retrieval methods.

## Failure boundaries

The validator rejects:

- duplicate or malformed query IDs;
- missing information needs;
- incomplete slice or difficulty coverage;
- unknown or unavailable positive judgment targets;
- mismatched expected error codes or available revisions;
- result items without exact positive revisions;
- result metadata that disagrees with canonical records;
- duplicate results, malformed ranks, increasing scores, or nondeterministic ties;
- malformed or non-replaceable index records;
- metric values outside `[0, 1]`;
- live or repository-mutating fixtures, results, or metrics.

## Next workstream boundary

Once this candidate is accepted, Workstream 2 may implement a deterministic lexical baseline using the exact same query-set version.

It must not change judgments to improve its scores. Any fixture correction requires a new reviewed revision with the reason recorded. Structured, embedding, vector, hybrid, and learned approaches remain later comparisons rather than assumptions.
