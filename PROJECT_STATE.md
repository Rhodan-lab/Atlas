# Atlas Project State

## Current status

**Phase 2 — Minimal Knowledge Kernel (active)**

Phase 1 is closed under an explicitly **AI-reviewed** policy. No human or expert verification is claimed.

## Accepted history

- Phase 0 foundation — PR #3, commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- review and promotion experiments — PR #4, commit `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency reporting — PR #5, commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- delayed-feedback readiness — PR #6, commit `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only authored corpus — PR #7, commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations — PR #8, commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- optional human handoff — PR #9, commit `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`;
- optional exact-snapshot intake — PR #10, commit `9809bcb523954770e87c78154cdb124f37aadf46`;
- optional admission boundary — PR #17, commit `01feffc696cc207305ef74c92d600f37f1e240a4`;
- Phase 1 AI review and Phase 2 activation — PR #18, commit `f90fa53f99ec9780451c9c50c57625759ba3b2b5`;
- first Phase 2 kernel and bridge receiver — PR #19, commit `8f1e473578d9086a73dae44f0b6001b246cfbc20`.

## Language policy

The active authored and review corpus is English-only.

Language-neutral translation identity, revision lineage, and staleness semantics remain dormant contract capabilities exercised only through synthetic fixtures. They do not represent an active translated corpus.

## Review policy

Atlas distinguishes review levels instead of presenting all review as equivalent.

### AI-reviewed

An AI-reviewed artifact has:

- an identified AI reviewer;
- explicit model and non-human status;
- exact entity revisions;
- source-use checks;
- reproducibility or mathematical checks where applicable;
- recorded findings and corrections;
- explicit limitations;
- `human_verified: false`.

AI review is sufficient for the current Atlas development phase and does not require a separate human reviewer duty.

### Human-verified

Human verification is an optional stronger layer. Existing handoff, intake, admission, coverage, and promotion tools remain available for future use, but they are not active Phase 2 gates.

Atlas must never convert an AI review into a human review or invent reviewer identity, credentials, independence, or accountability.

## Phase 1 completion evidence

The active completion evidence remains:

- `content/reviews/ai/feedback-delayed-comprehensive.json`;
- `docs/phase-1/ai-review-report.md`;
- `tools/foundation-validator/phase1_ai_review.py`;
- corrected delayed-feedback canonical revisions.

The reviewer is `GPT-5.6 Thinking`, reviewer kind `ai`, with `human_verified: false` and `human_review_required: false`.

For:

```text
x[t+1] = x[t] - x[t-1]
x0 = 1
x1 = 0
```

the orbit is bounded and periodic with exact period 6. This is a formal result for one recurrence and initial history. It is not empirical evidence about a real system and not a general theorem that delay causes instability.

## Authority order

1. `PROJECT_STATE.md`;
2. accepted foundation documents in `docs/foundation/`;
3. accepted ADRs;
4. canonical authored content;
5. identified review records and reports, with review level visible;
6. generated manifests and operational artifacts;
7. experimental runtime and adapter code.

## Phase 2 objective

Phase 2 builds the smallest dependable runtime over authored `atlas-content/0.1` Markdown.

Required outcomes:

- canonical-to-runtime compilation;
- read-only exact-revision entity repository;
- typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- deterministic command and library interfaces;
- compatibility and failure tests;
- representative and scaled performance measurements;
- no change to authored Markdown meaning.

## Phase 2 workstream 1 — accepted

PR #19 implemented:

- `atlas-kernel-runtime/0.1` deterministic compilation;
- path-form-independent source identity;
- exact `ENTITY_ID@REVISION` lookup;
- typed relation and explicit provenance traversal;
- internal reverse-dependency impact queries;
- Atlas-local bridge receiver validation;
- normalized `atlas-external-dependent/0.1` operational records;
- deterministic rejection of ID-only exports, stale revisions, status inheritance, and `live: true`;
- Python 3.11 and 3.13 machine gates.

This receiver is not a live integration. It does not clone Principia, call Principia during Atlas validation, copy Principia status, or modify canonical Atlas meaning.

## Phase 2 workstream 2 — PR #20 candidate

PR #20 consumes the exact bridge candidate merged through Principia PR #16.

Source identity:

```text
Principia contract: principia-atlas-external-dependent/0.2
Principia PR: #16
Principia head: 405cfabb6eba71b42bd42ed81b922b458f9175e7
Principia merge: eb3a00dfbfdfaa5470cb40505fa213e5349a917f
mode: bridge-candidate
live: false
```

Implemented candidate evidence:

- pinned copy of the generated Principia export;
- source path, Git blob SHA, and SHA-256 verification;
- adapter from the Principia v0.2 wire format into the Atlas receiver;
- verification that `depends_on` exactly mirrors `depends_on_exact`;
- exact delayed-feedback model revision 2 admission;
- preserved separation of Atlas and Principia status;
- lifecycle-aware impact escalation;
- representative benchmarks for compilation, lookup, provenance, bridge import, and impact reporting.

Lifecycle policy:

```text
current              -> preserve declared action
deprecated           -> at least revalidate
review-required stale -> at least revalidate
confirmed stale      -> at least revalidate
retracted            -> block-release
```

Atlas reports both the Principia-declared action and the effective lifecycle action. It does not mutate either repository or execute the action automatically.

Initial PR #20 measurements on the 34-entity corpus passed their regression budgets on Python 3.11 and 3.13. These measurements are operational small-corpus evidence, not production-scale claims.

## Principia & Atlas boundary

Atlas is the knowledge and governance layer of the future **Principia & Atlas** system.

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns causal explanation, learning pathways, investigations, simulations, system dossiers, failure analysis, and design experiences.
- Principia may reference exact Atlas revisions.
- Atlas may report dependency impact when upstream knowledge changes.
- Neither repository inherits the other repository's status automatically.
- The repositories remain separate and independently buildable.
- No live cross-repository dependency is declared during Phase 2.

## Current restrictions

Still frozen:

- polished product UI;
- specialized retrieval and ranking;
- vector database selection;
- synchronization and plugins;
- active translated corpus;
- hidden or autonomous authority claims;
- automatic conversion of AI review into human verification;
- direct repository merger with Principia;
- live Principia dependency;
- automatic status or release mutation;
- treating prototype runtime formats as canonical before kernel evaluation.

Allowed:

- minimal knowledge-kernel implementation;
- deterministic compilation and queries;
- English canonical content corrections;
- explicitly labeled AI reviews;
- optional human verification that remains separately labeled;
- read-only exact-revision Principia compatibility;
- pinned external fixtures and impact reports;
- lifecycle escalation reporting;
- benchmark and regression maintenance.

## Immediate next actions

1. merge PR #20 only after the exact tested head passes all Phase 2, foundation, AI-review, and repository-wide workflows;
2. add malformed runtime and missing canonical-reference fixtures beyond bridge-specific cases;
3. build a larger deterministic synthetic corpus for scaled benchmarks;
4. test multiple external dependents and mixed lifecycle states;
5. define bounded deprecation and retraction event fixtures without activating synchronization;
6. keep `live: false` until independent machine contracts pass in both repositories and a separate activation decision is recorded;
7. produce the Phase 2 completion report before retrieval work.

**Phase 1 is complete under the AI-reviewed policy. Phase 2 is active. PR #19 is accepted; PR #20 is the non-live exact Principia v0.2 compatibility candidate. Human verification remains optional and must never be implied when it did not occur.**
