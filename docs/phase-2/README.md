# Phase 2 — Minimal Knowledge Kernel

## Status

Active after Phase 1 completion under the explicitly labeled AI-reviewed policy.

The first workstream built the deterministic kernel and bounded bridge receiver through PR #19. The second workstream accepted the exact non-live Principia v0.2 importer baseline through PRs #20 and #21. The third workstream accepted the later Principia Phase 16–18 offline evidence audit through PRs #22 and #23. The fourth workstream hardens serialized-runtime admission and canonical failure semantics.

## Goal

Build the smallest dependable runtime that compiles and queries `atlas-content/0.1` without changing authored Markdown meaning.

## Required capabilities

1. deterministic canonical Markdown compilation;
2. exact entity ID and revision lookup;
3. read-only entity repository;
4. typed relation traversal;
5. synthesis-to-source provenance traversal;
6. reverse dependency and revision-impact queries;
7. visible lifecycle, staleness, confidence, and review level;
8. deterministic errors for malformed, missing, stale, or incompatible input;
9. compatibility tests against all three English slices;
10. representative and scaled performance measurements.

## Implemented workstreams

### Kernel and receiver

- `atlas-kernel-runtime/0.1` deterministic compilation;
- path-form-independent source identity;
- exact `ENTITY_ID@REVISION` lookup;
- typed relation and explicit provenance traversal;
- internal reverse-dependency impact;
- deterministic external-dependent normalization;
- positive and negative bridge fixtures;
- Python 3.11 and 3.13 CI.

### Principia v0.2 compatibility

- exact snapshot of the export merged through Principia PR #16;
- `principia-atlas-external-dependent/0.2` adapter;
- validation that `depends_on` exactly mirrors `depends_on_exact`;
- exact delayed-correction model revision 2 admission;
- source pull request, commit, path, blob, and SHA-256 tracking;
- lifecycle escalation for deprecated, stale, and retracted entities;
- representative compilation, lookup, provenance, import, and impact benchmarks.

The old ID-only shape remains an explicit rejection fixture. The merged Principia v0.2 export is accepted because its `depends_on_exact` objects preserve exact revisions.

### Offline multi-artifact and protocol audit

The accepted workstream pins the Principia repository at commit `4ecb41ad4f9f524e83cc0db43f672bd9dcf3b67a`, which contains the merged Phase 18 offline reconciliation simulation. It adds:

- byte-exact Git-blob verification for nine pinned Principia files;
- atomic re-import of three Principia artifacts;
- record-for-record comparison with Principia's Phase 16 receipt;
- independent recomputation of affected external dependents;
- digest and predecessor verification for two lifecycle events;
- verification of two Principia acknowledgements;
- rejection of weakened actions or altered affected-artifact sets;
- event/acknowledgement chain-head validation;
- Phase 18 reconciliation verification;
- deterministic failure tests for partial batches, digest corruption, stale artifact references, and `live: true`.

The lifecycle events are accepted only as `bounded-synthetic` test fixtures. They do not establish that Atlas actually deprecated or retracted an entity. The audit reports `verified-no-mutation` and never changes canonical Atlas content, lifecycle state, Principia pedagogical status, Principia release status, or either repository.

### Runtime hardening and failure semantics

The active candidate adds a strict public admission boundary for `atlas-kernel-runtime/0.1`.

- `KernelRepository` validates the runtime before indexing it;
- `runtime-validate` emits `atlas-runtime-validation-report/0.1`;
- entity identity, ordering, metadata, digests, references, relations, revision indexes, and reverse indexes must agree exactly;
- malformed records are rejected rather than dropped or repaired;
- missing canonical references and malformed authored structures fail before runtime emission;
- deterministic corruption manifests cover runtime and canonical failure cases;
- validation remains read-only with `mutation: false`.

## Non-goals

- polished UI;
- specialized retrieval or ranking;
- vector database selection;
- synchronization;
- plugins;
- active translated corpus;
- a live Principia dependency;
- cloning or calling Principia during Atlas validation;
- recognizing Principia-authored synthetic events as real Atlas lifecycle transitions;
- changing canonical authored semantics;
- treating `ai-reviewed` as `human-verified`.

## Architecture rule

Authored Markdown remains the source of truth. Any runtime database, index, serialized representation, adapter, or API is replaceable and must be reproducible from canonical content and pinned external fixtures.

## Principia compatibility

Phase 2 implements a read-only receiving, recomputation, and validation boundary. It does not activate a live cross-repository dependency.

Compatibility is limited to stable artifact identity, exact Atlas IDs and revisions, declared dependency roles, pinned offline evidence, provenance, and dependency-impact semantics. Principia pedagogical and release status remain Principia-owned observations and are never imported into Atlas lifecycle authority.

Atlas distinguishes the action Principia declared from the effective action implied by a bounded synthetic Atlas lifecycle state. Atlas may verify that an acknowledgement preserves `revalidate` or `block-release`, but it does not execute that action automatically.

See:

- `docs/phase-2/kernel-contract.md`;
- `docs/phase-2/bridge-receiver.md`;
- `docs/phase-2/principia-v02-compatibility.md`;
- `docs/phase-2/offline-protocol-audit.md`;
- `docs/phase-2/runtime-hardening.md`;
- `docs/phase-2/benchmark-policy.md`;
- `content/fixtures/phase2_bridge/`;
- `content/fixtures/phase2_protocol/`;
- `content/fixtures/phase2_runtime/`;
- `tools/phase2_kernel/`.

## Exit evidence

Phase 2 closes only when:

- compilation is deterministic;
- exact-revision queries are correct;
- relation and provenance traversal are tested;
- reverse dependency impact is correct;
- malformed and incompatible data fail safely;
- all three English reference slices compile;
- multi-artifact import and protocol evidence fail atomically and deterministically;
- performance is measured on representative and larger deterministic corpora;
- lifecycle escalation is tested;
- the selected kernel remains replaceable;
- a completion report recommends or rejects retrieval work.
