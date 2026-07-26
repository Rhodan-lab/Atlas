# Authoring Language and Translation Policy

## Status

**Accepted for `atlas-content/0.1`, amended during Phase 1.**

The amendment narrows the active reference corpus to English while preserving language-neutral translation semantics for future use.

## Decision

Atlas uses **English as the only active authored language** for the current foundation, reference corpus, review program, generated reports, and future Principia compatibility work.

- Canonical metadata keys, entity types, lifecycle states, relation types, contract identifiers, and authored reference content use English.
- Current canonical IDs use English language tags where a language-qualified ID is required.
- No translated vertical slice is part of the active corpus.
- No translation packet, translation review queue, or bilingual terminology program is active in Phase 1.
- Translation capability remains represented by language-neutral contracts and synthetic fixtures only.

This prevents language review from expanding the scope before the English knowledge and governance foundation is mature.

## Active-corpus rule

For the current project phase:

```yaml
language: en
```

is the only accepted language for authored canonical and learner-facing knowledge content.

New authored files under language-specific translation directories are out of scope. A future phase may reopen multilingual authoring through an explicit ADR and migration plan.

## Language-neutral structure

The following remain language-neutral technical tokens:

- entity types such as `claim`, `evidence`, `model`, and `synthesis`;
- lifecycle states such as `draft`, `reviewed`, and `contested`;
- relation types such as `supports`, `contradicts`, and `derived-from`;
- confidence labels and material flags;
- review-type identifiers;
- contract versions;
- date, revision, and federation formats.

The storage model must not require redesign if multilingual authoring is introduced later.

## Dormant translation capability

Atlas retains the ability to represent a translation as a separate authored entity with:

```yaml
id: claim:fr:synthetic-example
work: work:synthetic-example
language: fr
translation_of: claim:en:synthetic-example
translation:
  source_revision: 1
  method: fixture
```

This example is a **synthetic contract fixture**, not active corpus content.

Translation semantics continue to require:

- a distinct language-qualified entity ID;
- a shared language-neutral `work` identity;
- an exact source entity and source revision;
- independent staleness tracking;
- no automatic inheritance of lifecycle or review status;
- explicit editorial and domain review if multilingual authoring is later activated.

## Why capability is preserved

Removing active translated content does not justify deleting the underlying semantics. Future international use may still require:

- stable cross-language identity;
- source-revision pinning;
- stale-translation detection;
- translation-specific review authority;
- protection against semantic drift;
- independent lifecycle decisions.

The current phase tests those rules only with bounded synthetic fixtures.

## Synthetic fixture boundary

Translation fixtures may exist only when they:

- are clearly identified as test or migration fixtures;
- do not appear in the authored reference corpus;
- do not create a reviewer packet or promotion backlog;
- do not imply a supported product language;
- use minimal content needed to exercise the contract;
- cannot be mistaken for reviewed knowledge.

## Review boundary

Machine validation may establish that translation metadata is structurally valid or stale.

It cannot establish:

- translation equivalence;
- cultural or technical appropriateness;
- bilingual editorial quality;
- domain fidelity;
- authority to promote a translated entity.

No translated entity can become reviewed without a future policy reopening multilingual authoring and defining accountable human authority.

## Future reopening gate

Multilingual authored content may return only when an accepted decision records:

1. why another language is required;
2. which corpus or vertical slice is in scope;
3. contributor and reviewer qualifications;
4. terminology governance;
5. source-revision and staleness behavior;
6. migration effects on IDs, search, and interfaces;
7. resource requirements that do not weaken English review quality;
8. rollback and deprecation procedures.

Until that gate is passed, English remains the only active authored language.

## Invalid patterns

Reject or flag:

- non-English authored canonical content in the active corpus;
- translated content presented as a product-supported language;
- a translation without `translation_of` and source revision;
- inherited review status across languages;
- machine translation presented as reviewed human authorship;
- a language-specific review backlog created without an accepted reopening decision;
- changing a `work` identity merely because language changes;
- silently translating quoted source material as if verbatim.
