# Phase 1 — English Reference Corpus and Accountable Review

## Status

Active after:

- Phase 0 acceptance at `34afe253fc8c9cefb61adfe2831f6da82aa07e16`;
- initial review-gate merge at `09488b76c43fdbe46f94fcb14a27637472adfa38`;
- coverage and dependency-reporting merge at `c67457ae2c369d57b00b1cd22f454245ebf6ac13`;
- complete delayed-feedback readiness merge at `786bdaf4141be032554fe1b73439dfacb67c806d`;
- English-only corpus correction at `92b2cec5fbc310e065bdeca4486ca98d1dc5a7f2`;
- deterministic machine attestations at `a4d73fc4dfc7f8fa03aa7f913473110943b41f9e`.

The active authored and review corpus is English-only. Translation contracts remain dormant language-neutral infrastructure exercised only through neutral synthetic fixtures.

Phase 1 turns the accepted knowledge contract into an exact-revision review workflow. It does not build the general product and does not promote content merely because it parses, passes a machine check, generates a report, or appears in a reviewer bundle.

## Core question

Can Atlas prove, for an exact authored revision:

- what was reviewed;
- which procedure was used;
- whether the result came from a machine, AI assistance, or an accountable human;
- which qualifications, independence, and conflicts apply;
- which findings remain open;
- whether the review is still current;
- which review classes remain missing;
- which work may be automated and which requires accountable humans;
- which exact content snapshot was handed to a reviewer;
- which internal or external dependents may be affected;
- which lifecycle transition is permitted;
- why promotion or slice closure remains blocked?

## Workstreams

| Workstream | Output |
|---|---|
| Review contract | `atlas-review/0.1` schema and validation |
| Promotion gate | deterministic lifecycle decision with reasons |
| Coverage contract | `atlas-review-coverage/0.1` packet and slice reporting |
| Review backlog | `atlas-review-backlog/0.1` missing-review tasks |
| Machine attestations | deterministic structural and fully specified reproducibility records |
| Human handoff | `atlas-review-handoff/0.1` self-contained qualification-track bundles |
| Review packets | bounded English domain, methods, source, editorial, and legal-context packets |
| Lifecycle fixtures | reviewed, contested, deprecated, retracted, and stale cases |
| Dependency impact | internal reverse links and optional opaque external dependents |
| Contract challenge | reopen Phase 0 only when a representative fixture fails |

## Authority boundary

Machine validation may satisfy:

- structural conformance;
- reproducibility only where inputs, procedure, and expected calculation are fully specified and policy explicitly permits a machine record.

AI-assisted review may identify candidate defects, compare terminology, draft questions, flag evidence gaps, summarize limitations, and generate planning artifacts.

Machines, AI-assisted work, and handoff generators may not independently satisfy:

- final editorial accountability;
- source interpretation requiring human judgment;
- domain review;
- methodological or model-to-world inference review;
- ethical or legal-context review;
- accountable lifecycle acceptance.

Every machine and AI-assisted record sets `accountable: false` and `permits_promotion: false`. The handoff generator creates no review record and assigns no reviewer.

## Phase 1 artifacts

```text
content/reviews/
  records/            # exact-revision machine, AI-assisted, and human records
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
  templates/
  packets/
  reports/

tools/foundation-validator/
  phase1_review_gate.py
  phase1_coverage_report.py
  phase1_review_backlog.py
  phase1_machine_attestations.py
  phase1_human_review_handoff.py
  tests/
```

## Complete delayed-feedback slice

`content/reviews/coverage/feedback-complete-vertical-slice.json`:

- contains all ten split English entities;
- uses `coverage_requirement: all`;
- records the complete governance dependency graph;
- keeps the formal result and model-to-world inference boundary load-bearing;
- remains `draft` and `blocked`.

See [`feedback-vertical-slice-readiness.md`](feedback-vertical-slice-readiness.md).

## Completed machine work

The deterministic generator commits and checks:

- 10 structural machine records;
- 3 fully specified reproducibility machine records.

```bash
python tools/foundation-validator/phase1_machine_attestations.py check \
  --records-dir content/reviews/records
```

See [`machine-attestations.md`](machine-attestations.md).

## Remaining human work

After machine attestations:

- 25 gate tasks;
- 0 automation-eligible tasks;
- 25 human-required tasks;
- 0 advisory-only tasks.

The tasks group into:

- 7 domain-authority tasks;
- 7 editorial-and-scope tasks;
- 5 methods-and-inference tasks;
- 5 source-and-provenance tasks;
- 1 independent reproducibility task.

See [`feedback-human-review-plan.md`](feedback-human-review-plan.md).

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

The generated package contains:

- all 25 tasks exactly once;
- five JSON and Markdown qualification-track bundles;
- ten exact canonical Markdown snapshots;
- original repository paths and SHA-256 digests;
- existing records, blockers, dependents, and acceptance criteria;
- submission worksheets;
- `reviewer_assignment: null`.

See [`human-review-handoff.md`](human-review-handoff.md).

## Reviewer submission

A real qualified reviewer returns one `atlas-review/0.1` record per exact entity revision and review type.

```bash
python tools/foundation-validator/phase1_review_gate.py validate-record \
  content/reviews/records/<record>.json
```

A valid record may still fail coverage when authority, independence, horizon, promotion permission, findings, or another required review type remains insufficient.

## Future Principia & Atlas compatibility

A future Principia artifact may be listed as an opaque dependent of an Atlas revision without making Atlas import or validate Principia's pedagogical status.

- Atlas owns knowledge identity, evidence, provenance, review, lifecycle, and staleness.
- Principia may depend on models, claims, concepts, and syntheses.
- Atlas reports upstream knowledge impact.
- Principia owns explanation, investigation, simulation, pedagogy, and release status.
- Neither system inherits authority automatically.

The current handoff reviews Atlas knowledge only. No live Principia dependency is declared during Phase 1.

## Exit evidence

Phase 1 does not close because files, reports, or bundles exist. It closes when:

- review, promotion, coverage, backlog, attestation, and handoff semantics are executable;
- deterministic machine work is complete and bounded honestly;
- every human task is tied to an exact snapshot and accountable authority requirement;
- dishonest authority paths fail fixtures;
- lifecycle transitions preserve history;
- real reviewer records are valid and sufficient;
- the complete English delayed-feedback slice reaches its intended lifecycle state;
- dependency impact is visible;
- all remaining gaps are explicit;
- a completion report recommends or rejects Phase 2.

## Non-goals

- broad content production;
- polished product UI;
- search or retrieval redesign;
- active translated corpus;
- autonomous review approval;
- automatic reviewer assignment;
- replacing domain experts with AI;
- direct Principia integration or repository merger;
- selecting final runtime architecture.
