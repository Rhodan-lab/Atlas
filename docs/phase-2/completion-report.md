# Phase 2 Completion Report

## Candidate decision

```yaml
phase: 2
workstream: 6
mode: phase2-closure-candidate
decision: phase2-complete-candidate
retrieval_entry: proceed-bounded-retrieval-evaluation
next_phase: phase-3-retrieval-evaluation-candidate
live: false
repository_mutation: false
```

This report closes the evidence gap left after scale, replay, and recovery. It does not activate retrieval in production, select a vector database, create a live Principia dependency, or grant retrieval output authority over canonical knowledge.

## Exit-criterion review

Phase 2 required deterministic compilation, exact-revision lookup, typed relation and provenance traversal, reverse dependency impact, safe failures, three English reference slices, atomic offline protocol validation, representative and scaled measurements, lifecycle escalation, deterministic replay/recovery, kernel replaceability, and an explicit retrieval recommendation.

Workstreams 1–5 established every requirement except the final replaceability proof and retrieval-entry decision. Workstream 6 provides those remaining artifacts through:

```text
tools/phase2_kernel/closure.py
content/fixtures/phase2_closure/closure-baseline.json
.github/workflows/phase2-closure.yml
```

## Replaceability proof

The closure command compiles canonical Markdown repeatedly and requires byte-identical `atlas-kernel-runtime/0.1` output. It then exports:

```yaml
contract: atlas-kernel-portable-snapshot/0.1
live: false
mutation: false
```

The portable snapshot deliberately excludes:

- `source_root`;
- `revisions_by_id`;
- `reverse_dependencies`.

Those fields are generated implementation indexes, not knowledge authority. The snapshot retains exact entity records, source and body hashes, metadata, exact references, relations, and the canonical source digest.

An independent `PortableKernelRepository` reconstructs its own revision and reverse-dependency indexes. It does not subclass or call the standard `KernelRepository` query engine. The closure matrix compares both implementations for every canonical exact entity revision across:

1. exact lookup;
2. relation traversal;
3. provenance-to-source traversal;
4. transitive internal impact.

The current baseline contains 34 exact entity revisions, producing 136 full-query equivalence checks. Any divergence fails deterministically with `E-CLOSURE-QUERY-DIVERGENCE`.

## Migration boundary

A valid migration may replace runtime storage or indexing only when:

- canonical `atlas-content/0.1` Markdown remains authoritative;
- every generated representation preserves the canonical source digest;
- exact entity IDs and positive revisions remain mandatory;
- metadata, references, relations, lifecycle visibility, staleness, and review level remain intact;
- query behavior remains equivalent under the closure matrix;
- generated indexes remain disposable and reproducible;
- no migration changes canonical authored meaning.

The portable snapshot is evidence for interchange and comparison. It is not a second canonical corpus.

## Rollback expectation

Rollback means deleting a generated runtime or alternate index and rebuilding from canonical Markdown and pinned external fixtures. Closure requires the rebuilt runtime to be byte-identical to the original deterministic runtime.

Rollback does not mean restoring mutable database state as knowledge authority. Operational caches, search indexes, and portable snapshots may be discarded without loss of canonical meaning.

## Retrieval-entry recommendation

The Phase 2 evidence supports proceeding to a bounded Phase 3 retrieval evaluation.

Allowed:

- lexical and structured retrieval baselines;
- deterministic relevance evaluation over versioned entities;
- replaceable generated indexes;
- result records carrying exact entity IDs, revisions, and provenance.

Still blocked:

- production retrieval-quality claims;
- choosing a vector database before comparative evaluation;
- unversioned or implicit `latest` entity lookup;
- canonical writes generated from retrieval output;
- automatic lifecycle or release mutation;
- live Principia synchronization.

## Why the recommendation is bounded

Phase 2 proves that Atlas can compile, admit, query, validate, scale, replay, recover, migrate, and roll back its minimal knowledge kernel. It does not prove retrieval relevance, ranking quality, citation usability, robustness against ambiguous queries, multilingual performance, or production capacity.

Phase 3 must therefore begin as an evaluation phase rather than a product deployment phase.

## Required Phase 3 entry gates

Before any retrieval implementation can be described as accepted, Phase 3 must define:

- a versioned query-and-judgment fixture set;
- lexical and structured baselines before embedding or vector commitments;
- relevance metrics and deterministic tie handling;
- exact-revision result identity;
- provenance and review-level visibility in every result;
- failure behavior for unavailable revisions and malformed indexes;
- index deletion and canonical rebuild tests;
- explicit separation between retrieval ranking and Atlas lifecycle authority.

## Authority boundary

```yaml
canonical_authority: content/canonical/**/*.md
runtime_authority: generated-and-replaceable
retrieval_authority: advisory-only
principia_live_dependency: false
automatic_status_change: false
automatic_release_action: false
repository_mutation: false
```

Phase 2 may be marked complete only after the exact closure candidate passes its dedicated workflow and the complete Atlas regression suite. The accepted completion record must preserve the tested head and merge commit separately from this candidate report.
