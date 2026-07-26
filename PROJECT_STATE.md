# Atlas Project State

## Current status

**Phase 2 — Minimal Knowledge Kernel (active)**

Phase 1 is closed under an explicitly **AI-reviewed** policy. No human or expert verification is claimed.

Accepted history:

- Phase 0 foundation — PR #3, commit `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- review and promotion experiments — PR #4, commit `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency reporting — PR #5, commit `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- delayed-feedback readiness — PR #6, commit `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only authored corpus — PR #7, commit `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations — PR #8, commit `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- optional human handoff — PR #9, commit `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`;
- optional exact-snapshot intake — PR #10, commit `9809bcb523954770e87c78154cdb124f37aadf46`;
- optional admission boundary — PR #17, commit `01feffc696cc207305ef74c92d600f37f1e240a4`.

The active Phase 1 completion evidence is:

- `content/reviews/ai/feedback-delayed-comprehensive.json`;
- `docs/phase-1/ai-review-report.md`;
- `tools/foundation-validator/phase1_ai_review.py`;
- corrected delayed-feedback canonical revisions.

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

Human verification is an optional stronger layer. Existing handoff, intake, admission, coverage, and promotion tools remain available for future use, but they are not active Phase 1 gates and do not block Phase 2.

Atlas must never convert an AI review into a human review or invent reviewer identity, credentials, independence, or accountability.

## Phase 1 completion

### Scope

The complete English delayed-feedback slice contains:

- research question;
- authoritative and generated sources;
- generated evidence;
- exact model-derived claim;
- model-to-world inference-boundary claim;
- feedback and oscillation concepts;
- delayed corrective recurrence;
- synthesis.

### AI review result

The comprehensive review covers all ten entities and records `overall_outcome: pass`.

The reviewer is `GPT-5.6 Thinking`, reviewer kind `ai`, with `human_verified: false` and `human_review_required: false`.

### Corrected findings

1. **Periodicity proof — resolved**
   - The original eight displayed states did not alone prove indefinite repetition.
   - The corrected model, evidence, claim, and synthesis use return of the deterministic ordered state pair.
   - The orbit has exact period 6.

2. **Oscillation versus instability — resolved**
   - A bounded periodic orbit is not automatically unstable.
   - The corrected material no longer makes or implies that overclaim.

3. **Source-use boundary — resolved**
   - Åström and Murray support feedback, dynamic-behavior, and stability terminology.
   - The exact Atlas recurrence and period-six proof are independently derived and are not attributed to the textbook.

### Exact mathematical result

For:

```text
x[t+1] = x[t] - x[t-1]
x0 = 1
x1 = 0
```

the states are:

```text
1, 0, -1, -1, 0, 1, 1, 0, ...
```

The ordered pair `(x1, x0) = (0, 1)` returns as `(x7, x6) = (0, 1)`. Determinism proves repetition with period dividing 6; the state block excludes periods 1, 2, and 3, so the exact period is 6.

The orbit is bounded and periodic. This is not empirical evidence about a real system and is not a general theorem that delay causes instability.

## Authority order

1. `PROJECT_STATE.md`
2. accepted foundation documents in `docs/foundation/`
3. accepted ADRs
4. canonical authored content
5. identified review records and reports, with review level visible
6. generated manifests and operational artifacts
7. experimental runtime code

AI review may support development decisions, identify defects, verify formal calculations, inspect source metadata, and assess internal consistency. It does not become human professional accountability by being thorough.

## Phase 2 objective

Phase 2 builds the smallest dependable runtime over the authored Markdown contract.

Required outcomes:

- canonical-to-runtime compilation;
- read-only entity repository;
- typed relation traversal;
- synthesis-to-source provenance queries;
- dependency and revision-impact queries;
- deterministic command or library interface;
- compatibility and failure tests;
- representative performance measurements;
- no change to authored Markdown meaning.

## Future Principia & Atlas boundary

Atlas is the knowledge and governance layer of the future **Principia & Atlas** system.

- Atlas owns canonical knowledge identity, sources, evidence, claims, models, provenance, revision, review level, lifecycle, and staleness.
- Principia owns causal explanation, learning pathways, investigations, simulations, system dossiers, failure analysis, and design experiences.
- Principia may reference exact Atlas revisions.
- Atlas may report dependency impact when upstream knowledge changes.
- Neither repository inherits the other repository's status automatically.
- No live cross-repository dependency is declared at the start of Phase 2.

## Current restrictions

Still frozen:

- polished product UI;
- specialized retrieval and ranking;
- synchronization and plugins;
- active translated corpus;
- hidden or autonomous authority claims;
- automatic conversion of AI review into human verification;
- direct repository merger with Principia;
- treating prototype runtime formats as canonical before kernel evaluation.

Allowed:

- minimal knowledge-kernel implementation;
- deterministic compilation and queries;
- English canonical content corrections;
- explicitly labeled AI reviews;
- optional human verification that remains separately labeled;
- compatibility boundaries for future Principia references;
- prototype regression maintenance.

## Immediate next actions

1. define the Phase 2 kernel contract and non-goals;
2. compile canonical Markdown into a deterministic runtime representation;
3. implement read-only exact-revision lookup;
4. implement typed relation and provenance traversal;
5. implement dependency-impact queries;
6. test malformed, stale, missing, and incompatible inputs;
7. benchmark representative slices;
8. produce a Phase 2 completion report before retrieval work.

**Phase 1 is complete under the AI-reviewed policy. Phase 2 is active. Human verification remains optional and must never be implied when it did not occur.**