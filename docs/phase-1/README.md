# Phase 1 — English Reference Corpus and Accountable Review

## Status

Active after:

- Phase 0 acceptance at `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- initial review-gate merge at `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency-reporting merge at `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- complete delayed-feedback readiness merge at `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only corpus correction at `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations at `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`;
- accountable-human handoff bundles at `5dcd4964b04617d1c40a4458b2c646c43ebd09ed`.

The active authored and review corpus is English-only. Translation contracts remain dormant language-neutral infrastructure exercised only through neutral synthetic fixtures.

Phase 1 turns the accepted knowledge contract into an exact-revision review workflow. It does not build the general product and does not promote content merely because it parses, passes a machine check, generates a report, appears in a reviewer bundle, or passes intake validation.

## Core question

Can Atlas prove, for an exact authored revision:

- what was reviewed;
- which procedure was used;
- whether the result came from a machine, AI assistance, or an accountable human;
- which qualifications, independence, and conflicts apply;
- which findings remain open;
- whether the review is still current;
- which review classes remain missing;
- which exact content snapshot was handed to a reviewer;
- whether the returned submission matches that active task and snapshot;
- which internal or external dependents may be affected;
- which lifecycle transition is permitted;
- why promotion or slice closure remains blocked?

## Workstreams

| Workstream | Output |
|---|---|
| Review contract | `atlas-review/0.1` exact-revision records |
| Promotion gate | `atlas-promotion/0.1` lifecycle decisions |
| Coverage | `atlas-review-coverage/0.1` packet and slice reporting |
| Review backlog | `atlas-review-backlog/0.1` missing-review tasks |
| Machine attestations | deterministic structural and bounded reproducibility records |
| Human handoff | `atlas-review-handoff/0.1` self-contained qualification-track bundles |
| Review intake | `atlas-review-submission/0.1` exact-task and exact-snapshot return envelopes |
| Lifecycle fixtures | reviewed, contested, deprecated, retracted, and stale cases |
| Dependency impact | internal reverse links and optional opaque external dependents |

## Authority boundary

Machine validation may satisfy structural conformance and explicitly permitted fully specified reproducibility.

AI-assisted work may identify defects, compare terminology, draft questions, flag evidence gaps, summarize limitations, and prepare planning artifacts.

Handoff and intake tools may transfer exact snapshots and verify return-package consistency.

None of those tools may independently satisfy final editorial accountability, source interpretation, domain review, methods review, ethical or legal-context review, reviewer identity, reviewer qualification, or lifecycle acceptance.

The handoff generator assigns no reviewer. Intake validation accepts no authority and writes no review record automatically.

## Phase 1 artifacts

```text
content/reviews/
  records/            # committed exact-revision records
  fixtures/           # promotion and lifecycle test cases
  coverage/           # bounded packets and complete English slice manifests

docs/phase-1/
  review-protocol.md
  promotion-policy.md
  coverage-and-dependency-reporting.md
  reviewer-submission-guide.md
  feedback-vertical-slice-readiness.md
  machine-attestations.md
  feedback-human-review-plan.md
  human-review-handoff.md
  review-intake.md
  templates/
  packets/
  reports/

tools/foundation-validator/
  phase1_review_gate.py
  phase1_coverage_report.py
  phase1_review_backlog.py
  phase1_machine_attestations.py
  phase1_human_review_handoff.py
  phase1_review_intake.py
  tests/
```

## Complete delayed-feedback slice

`content/reviews/coverage/feedback-complete-vertical-slice.json` contains all ten split English entities, uses `coverage_requirement: all`, preserves the complete dependency path, and keeps the formal result plus model-to-world limitation load-bearing.

The slice remains `draft` and `blocked`.

## Completed machine work

The repository commits and checks:

- 10 structural machine records;
- 3 fully specified recurrence-reproducibility records.

```bash
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

Every machine record is non-accountable and cannot permit promotion.

## Remaining human work

After machine attestations:

- 25 gate tasks;
- 0 automation-eligible tasks;
- 25 human-required tasks;
- 0 advisory-only tasks.

Tracks:

- 7 domain-authority tasks;
- 7 editorial-and-scope tasks;
- 5 methods-and-inference tasks;
- 5 source-and-provenance tasks;
- 1 independent reproducibility task.

## Generate the self-contained handoff

```bash
python tools/foundation-validator/phase1_human_review_handoff.py \
  content/reviews/coverage/feedback-complete-vertical-slice.json \
  --records-dir content/reviews/records \
  --canonical-root content/canonical \
  --output-dir phase1-reports/human-review-handoff \
  --expect-task-count 25 \
  --expect-track-count 5
```

The package contains all 25 tasks exactly once, five qualification-track bundles, ten exact canonical snapshots, original paths and SHA-256 digests, existing blockers and dependents, acceptance criteria, worksheets, and `reviewer_assignment: null`.

See [`human-review-handoff.md`](human-review-handoff.md).

## Return a review through exact-snapshot intake

Start from [`templates/reviewer-submission-envelope.json.example`](templates/reviewer-submission-envelope.json.example).

Validate:

```bash
python tools/foundation-validator/phase1_review_intake.py validate \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json
```

Extract a normalized proposed review record:

```bash
python tools/foundation-validator/phase1_review_intake.py extract \
  reviewer-submission.json \
  --handoff phase1-reports/human-review-handoff/handoff.json \
  --out phase1-reports/extracted-review.json
```

Intake verifies coverage ID, active task ID, exact entity revision, snapshot digest, review type, human accountability, independence, qualification, conflicts, date order, and AI-assistance disclosure.

The extracted record preserves `metadata.intake` lineage. It is not written to `content/reviews/records/` automatically and is not accepted merely because intake validation passes.

See [`review-intake.md`](review-intake.md) and [`reviewer-submission-guide.md`](reviewer-submission-guide.md).

## Maintainer acceptance

A maintainer must still:

1. inspect the real reviewer identity and qualification;
2. verify independence and conflicts;
3. inspect findings and promotion permission;
4. commit an acceptable record through normal review;
5. regenerate coverage, backlog, and handoff;
6. create a new canonical revision when findings require content changes;
7. preserve unresolved serious findings.

## Future Principia & Atlas compatibility

- Atlas owns knowledge identity, evidence, provenance, review, lifecycle, and staleness.
- Principia may depend on exact Atlas revisions.
- Atlas reports upstream knowledge impact.
- Principia owns explanation, investigation, simulation, pedagogy, and release status.
- Neither system inherits authority automatically.

The current handoff and intake review Atlas knowledge only. No live Principia dependency is declared during Phase 1.

## Exit evidence

Phase 1 closes only when:

- review, promotion, coverage, backlog, attestation, handoff, and intake semantics are executable;
- deterministic machine work is complete and bounded honestly;
- every human task is tied to an exact snapshot and accountable authority requirement;
- returned submissions preserve exact-snapshot provenance;
- dishonest authority paths fail fixtures;
- real reviewer records are valid and sufficient;
- the complete English delayed-feedback slice reaches its intended lifecycle state;
- all remaining gaps remain explicit;
- a completion report recommends or rejects Phase 2.

## Non-goals

- broad content production;
- polished product UI;
- search or retrieval redesign;
- active translated corpus;
- autonomous review approval;
- automatic reviewer assignment or record acceptance;
- replacing domain experts with AI;
- direct Principia integration or repository merger;
- selecting final runtime architecture.
