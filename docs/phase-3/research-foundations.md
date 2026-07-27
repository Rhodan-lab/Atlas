# Phase 3 Workstream 5 — Research Trails and Candidate Discovery

## Status

Candidate foundation for the remaining Phase 3 research workflow.

```yaml
phase: 3
workstream: 5
mode: retrieval-evaluation
state: research-foundation-candidate
preferred_bounded_ranking: structured-field-baseline
retrieval_authority: advisory-only
exact_revision_required: true
canonical_copy_authority: false
automatic_merge_or_resolution: false
embeddings: false
vector_database: false
external_services: false
live: false
repository_mutation: false
```

## Purpose

Complete the research foundations required by the authoritative Phase 3 gate before any semantic-index or vector-database decision:

- deterministic retrieval filters;
- saved exact-revision research trails;
- advisory contradiction candidates;
- advisory duplicate candidates.

The workstream is contract-first. It does not add a product UI, autonomous agent, semantic model, or new knowledge authority.

## Filter contract

Contract: `atlas-retrieval-filter/0.1`.

Supported dimensions:

```yaml
entity_types: canonical entity type
statuses: canonical lifecycle status
domains: first canonical collection path segment
updated: inclusive ISO-date from/to range
evidence_roles: explicit authored relation type
```

The initial domain keys are the canonical collection directories:

- `catalase`;
- `feedback`;
- `recommenders`.

Evidence-role filtering is restricted to explicit relation vocabulary:

- `supports`;
- `derived-from`;
- `contextualizes`;
- `replicates`.

Filtering uses AND across dimensions and OR inside a dimension. It preserves canonical order, exact revisions, provenance, status, staleness, and review visibility. It may narrow advisory results; it may not silently substitute `latest`, rewrite ranking evidence, or mutate canonical content.

## Research-trail contract

Contract: `atlas-research-trail/0.1`.

A trail stores research references and decisions, not copied canonical knowledge. Each revision binds:

- stable trail ID and revision;
- accepted query ID and exact text snapshot;
- exact filter ID and revision;
- accepted structured-baseline contract, index digest, and result digest;
- exact selected entity revisions;
- original rank when available;
- action: `include`, `exclude`, or `context`;
- rationale for every action;
- open questions;
- created and updated dates.

Every trail entry must be inside the saved filter result. A trail cannot follow a newer revision automatically, change lifecycle status, or become canonical authority.

## Contradiction-candidate contract

Contract: `atlas-contradiction-candidate/0.1`.

A contradiction candidate requires:

- two different exact entity revisions;
- compared statements;
- scope analysis;
- evidence paths;
- rationale;
- an explicit assessment.

Initial assessments:

- `needs-review`;
- `scope-difference-likely`;
- `substantive-tension`.

A valid candidate means “inspect this possible tension.” It does not prove contradiction, resolve the issue, deprecate a claim, or alter review state. Automatic resolution is forbidden.

## Duplicate-candidate contract

Contract: `atlas-duplicate-candidate/0.1`.

A duplicate candidate requires:

- two different exact entity revisions;
- similarity basis;
- semantic differences;
- evidence paths;
- rationale;
- an explicit assessment.

Initial assessments:

- `needs-review`;
- `related-not-duplicate`;
- `probable-duplicate`.

A valid candidate does not prove duplication and cannot merge, redirect, supersede, or deprecate either entity automatically.

## Reference fixtures

`content/fixtures/phase3_retrieval/research-foundations.v01.json` contains:

- four deterministic filters;
- one saved cross-platform recommender research trail;
- one contradiction candidate assessed as likely scope difference;
- one duplicate candidate assessed as related but not duplicate;
- five negative identity, date, revision, pair, and authority cases.

The positive filters cover:

1. feedback draft models;
2. catalase evidence with explicit `supports` role;
3. recommender evidence with explicit `contextualizes` role;
4. recommender claims and synthesis records for a saved research trail.

## Pinned candidate evidence

The exact evidence is pinned in `content/fixtures/phase3_retrieval/research-foundations-baseline.json`.

```yaml
fixture_id: research-foundations:phase3-reference-en-v1
fixture_version: 1
entity_count: 34
filters: 4
filter_result_items: 9
trails: 1
trail_entries: 5
contradiction_candidates: 1
duplicate_candidates: 1
negative_cases: 5
report_digest: 733aeb28a3147a36d1cc7d3406ab98fa81522cb4b4e87e3aa792aaf54893a394
report_artifact_sha256: bdf56d085025e624b80fd7e0b35a362e16331e593185184d5500c7603b3910bd
filter_result_artifact_sha256: 3f25421b72350be1d8d820baaa9b549ead5d9d8caa5bb61538cd0ecc545c3f67
python_substantive_artifacts_byte_identical: true
```

The four filter results contain exact entity counts `1, 1, 1, 6` and preserve these exact keys:

```text
model:en:delayed-correction-recurrence@2

evidence:en:fluorescent-catalase-assay-neutral-ph@1

evidence:en:dsa-recommender-transparency-and-choice@1

claim:en:facebook-exposure-reflects-network-ranking-and-clicks@1
claim:en:recommender-effects-are-context-dependent@1
claim:en:transparency-and-nonprofiling-are-eu-governance-responses@1
claim:en:twitter-ranking-changed-relative-political-amplification@1
claim:en:users-should-have-recommender-explanation-and-choice@1
synthesis:en:recommender-exposure-and-governance@1
```

Python 3.11 and Python 3.13 produced byte-identical research reports and filter-result artifacts. Unittest transcripts differ only in elapsed-time text and are not treated as substantive evidence.

The validated research trail is:

```yaml
id: trail:en:recommender-cross-platform-generalization
revision: 1
entry_count: 5
authority: research-only
```

The validated advisory candidates are:

```yaml
contradiction:
  id: candidate:contradiction:facebook-twitter-exposure-effects
  assessment: scope-difference-likely
  decision: valid-candidate-not-proven-contradiction
duplicate:
  id: candidate:duplicate:recommender-context-claim-and-synthesis
  assessment: related-not-duplicate
  decision: valid-candidate-not-proven-duplicate
```

The candidate intentionally demonstrates that discovery may conclude “likely scope difference” or “related but not duplicate.” Candidate generation is not forced to produce a contradiction or duplicate.

## Validation and negative boundaries

Machine validation reconstructs filter results from the canonical runtime and rejects:

- unavailable domain or entity-type values;
- unsupported evidence roles;
- inverted or malformed date ranges;
- unavailable exact revisions;
- trail entries outside the saved filter snapshot;
- changed query text or accepted ranking identity;
- repeated exact entities inside one trail;
- contradiction candidates comparing the same exact entity;
- automatic contradiction resolution;
- automatic duplicate merging;
- canonical-copy or lifecycle authority escalation;
- live or repository-mutating records.

The pinned negative errors are:

```text
E-FILTER-DOMAIN
E-FILTER-DATE
E-REVISION-MISSING
E-CANDIDATE-PAIR
E-DUPLICATE-AUTHORITY
```

## Semantic-infrastructure boundary

This candidate does not justify embeddings or vector infrastructure. Those remain deferred until:

1. these research-foundation contracts are accepted;
2. the relevance collection expands beyond 34 entities and 13 queries;
3. hard negatives and candidate-discovery cases are included;
4. any semantic architecture is compared on quality, determinism, inspectability, storage, latency, failure behavior, and replaceability.

## Non-goals

This candidate does not:

- claim production retrieval quality;
- provide a polished research UI;
- copy canonical content into trails;
- prove contradictions or duplicates;
- merge, deprecate, promote, review, or release entities;
- use embeddings, learned ranking, external semantic services, or a vector database;
- activate live Principia synchronization.
