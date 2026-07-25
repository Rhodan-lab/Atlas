# Language Decisions

Atlas follows a **polyglot-with-restraint** rule. New languages require an architectural reason, an owned boundary, tests, and a documented removal path.

## Current decisions

| Language | Accepted use | Rejected use |
|---|---|---|
| C++20 | Domain model, persistence, graph algorithms, native CLI | HTTP templates, ad-hoc ingestion scripts |
| Rust | Read-only indexing and retrieval service | Duplicating graph mutation rules |
| Python | Build-time ingestion, validation, data migration, research tooling | Primary always-on server |
| TypeScript | HTTP adapters, web client, integration boundary | Authoritative graph implementation |
| SQL | Constraints and migrations for durable local storage | Business logic hidden in database triggers |
| Shell | Small repeatable developer commands | Complex portable application logic |

## Admission test for another language

A proposed language must answer all four questions:

1. What capability is materially better than extending an existing component?
2. What process or package boundary prevents logic duplication?
3. How will CI test and secure its dependency chain?
4. How could the component be replaced without rewriting Atlas data?

A language is rejected when its only justification is novelty, syntax preference, or repository statistics.
