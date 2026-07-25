# Security Policy

Atlas is an early local-first project. Do not use it as the sole store for irreplaceable data yet.

## Reporting

Report vulnerabilities privately through GitHub's security reporting feature when enabled. Do not include sensitive personal knowledge files in a public issue.

## Current security boundaries

- The TypeScript API binds to `127.0.0.1` by default.
- Native commands are invoked with argument arrays, not shell interpolation.
- API numeric inputs and search limits are validated.
- Static file paths are normalized and constrained to the public directory.
- Ingestion rejects unresolved and duplicate graph references before producing data.
- The C++ loader builds a candidate graph and only replaces the active graph after complete validation.

## Known limitations

- There is no authentication because the server is intended for loopback-only local use.
- The `.atlas` format has no encryption or signature layer.
- Resource limits for very large graphs are not yet enforced.
