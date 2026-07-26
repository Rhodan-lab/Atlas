# Phase 0 Maturity Assessment

## Status

**Assessment date:** 2026-07-26  
**Historical state:** pre-closure mature draft  
**Current authority:** superseded by [`18-phase-0-closure-report.md`](18-phase-0-closure-report.md)

This document records the state before canonical splitting and executable validation. It is retained to show which blockers existed and how they were resolved. It must not be used as current project status.

## Original assessment

The pre-closure foundation had:

- an explicit charter and non-goals;
- differentiated canonical entities;
- claim-level evidence and relation semantics;
- lifecycle, uncertainty, review, translation, access, migration, and staleness rules;
- three bundled vertical slices;
- a catalog of invalid scenarios;
- architecture policy preventing implementation from defining knowledge accidentally.

It was considered mature enough for verification but not complete.

## Original blockers and resolution

| Pre-closure blocker | Resolution | Evidence |
|---|---|---|
| bundled slices rather than canonical records | split into 34 English canonical files | `content/canonical/` |
| language-qualified identity and staleness not demonstrated | added representative translation semantics and source-revision fixture | foundation contract and `content/fixtures/translation/` |
| source metadata and locators not independently compared | added explicit verification ledger | `docs/reviews/phase-0-source-verification.md` |
| relation compatibility not executable | implemented controlled pair checks | foundation validator and tests |
| no executable invalid fixtures | required scenarios exercised by tests | `tools/foundation-validator/tests/` |
| no migration examples | added mechanical and semantic split fixtures | `content/fixtures/migrations/` |
| alias, rename, collision, and federation untested | added identity fixture | `content/fixtures/identity/` |
| translation staleness untested | source-revision mismatch returns `possibly-stale` | `content/fixtures/translation/` |
| validator architecture undecided | accepted ADR-0001 Python baseline | `docs/adr/0001-phase-0-validator-baseline.md` |
| no completion report | added gate-by-gate closure report | `18-phase-0-closure-report.md` |
| prototype regression risk | existing CI remained green across tested components | PR #3 checks |

## Validation outcome

The Foundation Contract matrix completed successfully on Python 3.11 and 3.13:

- validator tests passed;
- canonical corpus produced no error diagnostics;
- migration fixtures passed;
- identity fixture passed;
- synthetic stale-translation state passed.

The first run caught one malformed YAML title containing an unquoted colon. The fixture was corrected and the full matrix reran successfully. The contract was not weakened.

## Maturity distinction

Closure analysis clarified two separate authorities:

1. **Phase 0 foundation acceptance** — contract, governance, identity, migration, language-neutral translation semantics, diagnostics, and executable fixtures;
2. **Phase 1 content review** — revision-specific scientific, methodological, legal-context, ethical, and editorial review.

Machine validation cannot promote content from `draft`. Requiring publication-grade content review before accepting the contract would incorrectly make example-content authority a prerequisite for stabilizing the review system itself.

## English-only amendment

Phase 1 later narrowed the active authored corpus to English-only.

- language-specific authored examples were removed;
- translation behavior remains tested by neutral synthetic fixtures;
- no active translation review program exists;
- future multilingual authoring requires an explicit reopening gate.

This amendment changes active scope without invalidating the original foundation semantics.

## Current conclusion

The concerns documented by this assessment produced the Phase 0 closure work. The current project authority is [`PROJECT_STATE.md`](../../PROJECT_STATE.md), and the accepted closure interpretation is recorded in [`18-phase-0-closure-report.md`](18-phase-0-closure-report.md).
