# Authoring Language and Translation Policy

## Status

**Accepted for `atlas-content/0.1`.** Revisit only if reference fixtures expose a material failure.

## Decision

Atlas supports multilingual authored knowledge from the beginning while keeping identifiers and structural vocabulary language-neutral.

- Canonical IDs use lowercase ASCII prefixes and stable slugs.
- Metadata keys, entity-type values, lifecycle states, relation types, and contract identifiers use English technical tokens.
- Human-readable titles, statements, explanations, limitations, and syntheses may be authored in any declared language.
- A translation is a separate authored entity linked to the same language-neutral `work` identity.
- Translation does not automatically inherit review status from the source-language entity.

This balances international interoperability with the ability to author serious knowledge in Indonesian or another language without forcing translation before review.

## Identity layers

Each authored entity has:

```yaml
id: claim:id:delayed-feedback-can-oscillate
work: work:delayed-feedback-can-oscillate
language: id
```

A corresponding English translation may use:

```yaml
id: claim:en:delayed-feedback-can-oscillate
work: work:delayed-feedback-can-oscillate
language: en
translation_of: claim:id:delayed-feedback-can-oscillate
```

`work` identifies the shared intellectual item across languages. `id` identifies one authored linguistic expression and its revision history.

## Why translations are separate entities

Translation can change:

- ambiguity;
- technical precision;
- implied scope;
- cultural interpretation;
- examples and terminology;
- confidence or review of phrasing.

Therefore, a translation is not merely a display layer. It requires its own editorial and, when meaning could shift, domain review.

## Canonical structural vocabulary

The following remain language-neutral technical tokens:

- entity types such as `claim`, `evidence`, and `synthesis`;
- statuses such as `draft`, `reviewed`, and `contested`;
- relations such as `supports`, `contradicts`, and `derived-from`;
- confidence labels when used as controlled metadata;
- review-type identifiers;
- contract versions;
- date and identifier formats.

Interfaces may localize their labels, but stored authored semantics retain canonical tokens.

## Language declaration

Use BCP 47 language tags where possible:

```yaml
language: id
```

Examples:

- `id` — Indonesian;
- `en` — English;
- `en-US` — U.S. English when the regional distinction matters;
- `jv` — Javanese.

Do not add a regional subtag unless it changes interpretation or editorial expectations.

## Terminology records

Important technical terms may use terminology records:

```yaml
id: term:id:umpan-balik
work: term:feedback
language: id
preferred: umpan balik
alternatives:
  - feedback
avoid:
  - balikan
scope_note: Preferred systems-science term in this corpus.
```

Terminology records help distinguish:

- preferred translations;
- accepted alternatives;
- misleading near-synonyms;
- domain-specific usage;
- terms intentionally retained in another language.

Terminology guidance does not erase legitimate variation in quoted or historical material.

## Translation lifecycle

1. Source-language item is authored and assigned a `work` identity.
2. Translation begins as `draft`.
3. Translator records the source revision used.
4. Editorial review checks clarity and fidelity.
5. Domain review checks technical meaning when necessary.
6. Translation status records the exact source revision it matches.
7. A material source revision marks translations as potentially stale.

## Review fields

```yaml
translation:
  source: claim:id:delayed-feedback-can-oscillate
  source_revision: 2
  method: human
  checked_by:
    - role: bilingual-editor
```

AI-assisted translation is allowed only as a draft transformation and must record the method. It cannot inherit or create `reviewed` status.

## Cross-language relations

Canonical semantic relations normally connect `work` identities in derived views, while authored files reference the specific language entity they actually discuss.

This prevents a translation mismatch from being hidden while still allowing a reader to navigate the same intellectual structure across languages.

## Search and interface behavior

Later implementations should:

- search the user’s preferred language first;
- expose available translations;
- show when a translation is stale or less reviewed;
- avoid combining sentences from different translations into one synthesis without disclosure;
- preserve original-language source titles and provide optional translated labels.

## Initial corpus policy

The Phase 0 reference corpus may use English metadata tokens and English primary records for interoperability. At least one complete vertical slice must include an Indonesian authored or translated entity to test multilingual identity, terminology, and review behavior.

## Invalid patterns

Reject or flag:

- two language files sharing the same `id`;
- a translation without `translation_of` and source revision;
- inherited review status without translation review;
- machine translation presented as reviewed human authorship;
- changing a `work` identity merely because the title is translated;
- silently translating source quotations or legal language as if verbatim.
