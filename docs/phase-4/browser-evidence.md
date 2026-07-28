# Phase 4 Workstream 2 — Pinned Chromium Browser Evidence

## Status

Pinned evidence candidate.

```yaml
phase: 4
workstream: 2
mode: interactive-experience-foundation
state: browser-evidence-candidate
engine: chromium
engine_version: 151.0.7922.34
playwright: 1.62.0
production_frontend_architecture_selected: false
live_principia_dependency: false
canonical_mutation: false
repository_mutation: false
```

## Purpose

Use one pinned Chromium engine as a controlled measurement instrument to determine whether the accepted local reference shell is keyboard-operable, semantically inspectable, deterministic under deep links and browser history, complete without graph visualization, explicit under failure, responsive at two bounded viewports, and independent of external network services.

This is automated browser evidence. It is not human accessibility verification, accessibility certification, production browser support, or a frontend architecture decision.

## Toolchain

```yaml
package: playwright
package_version: 1.62.0
browser: chromium
browser_version: 151.0.7922.34
browser_install: chromium-only
ci_operating_system: ubuntu-24.04
node_major: 22
package_lock_sha256: 7d889a57ab2d7f5855f7ea31184b7da5808efc896c65ab3de01e2d7ab0ac8510
screenshots_authoritative: false
```

The package dependency graph is committed and installed with `npm ci`. Chromium and its Linux dependencies are installed from the pinned Playwright package.

## Evidence contracts

The runner emits and the independent validator checks:

- `atlas-phase4-browser-evidence-manifest/0.1`;
- `atlas-browser-workflow-evidence/0.1`;
- `atlas-browser-accessibility-report/0.1`;
- `atlas-browser-network-report/0.1`;
- `atlas-browser-failure-evidence/0.1`;
- `atlas-phase4-browser-evidence-report/0.1`;
- `atlas-phase4-browser-evidence-validation/0.1`.

The candidate is pinned by `atlas-phase4-browser-evidence-baseline/0.1`.

## Pinned evidence identities

```yaml
browser_manifest:
  artifact_bytes: 1459
  artifact_sha256: afaf4eece4b8cf423271510b7e6032bcf961063e7ecac4482d037d8cba461290
  report_digest: caa1c1e401047975ce546c6e9a953e5542b50b28bbcdcaa253881f1a50fb0694
browser_workflows:
  artifact_bytes: 6825
  artifact_sha256: e0f7f56f4a25fcd44b0f21a783f83fe5c939a2dcb59d548d8f928632fd1c18e3
  report_digest: 840293431f65bc2a5687df560240a07b275234dd7e06f92998760a28f3a9651d
browser_accessibility:
  artifact_bytes: 5007
  artifact_sha256: d950709b605d82ec3f5c37f1ba0df377a1533d0fce1a1947fc86117383912e9c
  report_digest: 10d45e37e222f103939d1a607f6d0aac3250f1c8ef150fdb836ca654198222f3
browser_network:
  artifact_bytes: 1142
  artifact_sha256: 28cb130e99715efd3e7a849d639e3bdea4c4b45b27fcd2e662a190240f6df954
  report_digest: 59f5344bc3768b462c4ac0c862bc019c05755d64283b5832ee19adccddc96580
browser_failures:
  artifact_bytes: 711
  artifact_sha256: f28af2b19f30cb9a3e4caf7566d6310f7f8cdab5406e75a27fb763973bdca662
  report_digest: d53524e315bc12fa461a219f940404348614f9154e83acae64dfb11773ca0156
browser_evidence_report:
  artifact_bytes: 2350
  artifact_sha256: b3e72b7969802edf75b96870ec283dde597fb12723fb7f56c297e86bf502f855
  report_digest: dd1242387ff68024b478c81c74cc7b11308a4c37aeb1b23dd1859be8caafb5e1
python_validation:
  artifact_bytes: 463
  artifact_sha256: 4298f75e90782ee706655e8e432db3217664da40d8f0b64fe7ee0f5cc57eb2ab
```

Both complete browser evidence directories were byte-identical.

## Browser matrix

```yaml
desktop:
  width: 1440
  height: 1000
  reduced_motion: no-preference
mobile:
  width: 390
  height: 844
  reduced_motion: reduce
```

This is a bounded matrix, not complete device certification.

## Workflow evidence

All eight accepted view kinds pass through keyboard operation:

1. entity;
2. provenance;
3. retrieval;
4. filter;
5. research trail;
6. advisory candidate;
7. Principia reference;
8. impact warning.

For every view, the record binds an exact workflow ID and revision, semantic keyboard input, visible focus result, expected and observed hash route, observed heading, exact Atlas reference count, equivalent non-graph route, and pass decision.

Additional passing evidence includes:

- skip-link operation and visible main-target focus;
- deterministic browser back and forward behavior;
- direct exact-revision deep-link reload;
- explicit rejection of `@latest` and unknown routes;
- all five accepted failure-state codes;
- impact-warning text;
- separate Principia status;
- offline operation after local package boot.

## Accessibility evidence

The automated report records:

- document language and title;
- banner, navigation, main, and contentinfo landmarks;
- heading levels and text;
- accessible names for every button;
- live and alert regions;
- skip-link and main-target focus;
- focus order across eight workflow controls and the failure control;
- visible focus checks;
- desktop and mobile horizontal overflow;
- reduced-motion scroll behavior;
- availability of all mobile workflow controls.

```yaml
keyboard_workflow_count: 9
visible_focus_verified: true
non_graph_workflow_equivalence: true
reduced_motion_verified: true
human_verified: false
accessibility_certified: false
assistive_technology_user_reviewed: false
```

## Network evidence

The browser-context policy records every request and permits only the exact loopback origin.

```yaml
request_count: 4
loopback_request_count: 4
external_request_count: 0
resources:
  - /
  - /app.js
  - /data/reference-shell-data.json
  - /styles.css
credentials_used: false
remote_assets_used: false
analytics_used: false
cloud_service_used: false
```

## Failure evidence

The browser verifies:

- five accepted failure states remain visible;
- unknown and malformed routes produce an explicit route failure;
- implicit `latest` is rejected;
- no silent fallback to the first view occurs;
- canonical and lifecycle mutation remain false.

## Authorized shell compatibility patch

The browser requirements exposed two defects in the original static shell:

1. the main skip-link target suppressed its visible outline;
2. unknown hash routes fell back silently to the first view.

The versioned `atlas-phase4-reference-shell-accessibility-patch/0.1` also adds atomic status semantics and labels dynamic content panels.

```yaml
interaction_semantics_changed: false
shell_data_sha256_unchanged: e0f9fcbff9b86cbd4fffcb43d9c2aff64c2eb602f9b2fa0a02b8804bd18eb762
shell_report_sha256_unchanged: c9ca4259944bc4a90c42df26c4927c3f546a8358235b4e08a40715c692fa1eff
current_index_sha256: 1b00a15a32ee2523cab99068b7d093569f8d033ad1c6f9b6b7c2e85928cd6e1a
current_styles_sha256: 7187549623ffc180420bff4dd58c04a15a7fbedcb168e82ff4439d9ba4bfc1b6
current_app_sha256: c95e09f93e0eac242fa63c88bd7c9b0fac947c7047fae4fad7271d96c6c67765
```

The Workstream 1 completion report remains byte-identical to its accepted historical evidence. The patch is validated separately and does not rewrite history.

## Independent validation and tamper resistance

The Python validator independently checks every contract, digest, file binding, engine identity, viewport, workflow, focus result, route, accessibility limitation, network record, failure outcome, and authority boundary.

Tampered evidence is resealed with valid digests and parent bindings, then still rejected for:

- external requests;
- implicit `latest`;
- false human-verification claims;
- removal of non-graph equivalence.

## Boundary

This candidate does not:

- claim human accessibility verification or conformance certification;
- select a production browser or frontend framework;
- add analytics, accounts, cloud services, or deployment architecture;
- alter canonical content or accepted retrieval judgments;
- activate live Principia integration;
- grant browser state lifecycle, merge, review, promotion, or release authority;
- make screenshots authoritative.

## Acceptance condition

Merge only after one immutable final head passes:

- pinned Phase 4 Browser Evidence;
- Workstream 1 Closure with byte-identical historical report;
- Phase 4 Reference Shell with the authorized patch;
- Phase 4 Interaction Contract;
- Foundation and Phase 1 authority checks;
- the complete Atlas platform matrix;
- end-to-end integration.
