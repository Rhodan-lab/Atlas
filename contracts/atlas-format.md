# Atlas File Format v1

An Atlas file is UTF-8, line-oriented, deterministic, and human-inspectable.

## Header

The first line must be:

```text
ATLAS<TAB>1
```

## Records

Fields are separated by tab characters. Text fields use C-style quoted strings with `\\` as the escape character. Writers normalize literal tabs and line breaks inside text fields to spaces so every record remains one physical line.

### Concept

```text
C<TAB>numeric-id<TAB>"title"<TAB>"summary"<TAB>"tag-a|tag-b"
```

Rules:

- IDs are positive unsigned integers.
- Titles are non-empty.
- Tags are case-preserving in storage but compared case-insensitively.
- Concept IDs are unique.

### Source

```text
S<TAB>concept-id<TAB>"source title"<TAB>"locator"
```

A source must reference an existing concept.

### Relation

```text
R<TAB>from-id<TAB>to-id<TAB>"type"<TAB>positive-weight<TAB>"note"
```

Rules:

- endpoints must exist;
- self-relations are rejected in v1;
- `(from, to, type)` is unique;
- weight must be greater than zero.

## Ordering

Writers should produce records in this order:

1. concepts ordered by numeric ID;
2. each concept's sources in source order;
3. relations in deterministic source order.

Readers must not rely on source or relation records appearing after concepts; they may resolve references after parsing the complete file.

## Compatibility

Readers must reject unknown major versions. Additive record types require a future format version so older readers fail clearly rather than silently dropping knowledge.
