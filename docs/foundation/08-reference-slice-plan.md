# Reference Vertical Slice Plan

## Purpose

Phase 0 must test the knowledge model with real examples. Each vertical slice starts with a scoped question and ends with a traceable synthesis.

## Requirements for every slice

Each slice must contain:

- one question;
- at least two sources;
- precise evidence records;
- atomic claims with scope and qualifiers;
- at least one concept and one model;
- typed relations;
- supporting and challenging material;
- limitations or uncertainty;
- one synthesis;
- one open question or revision trigger;
- appropriate review records;
- a complete path from synthesis back to source;
- invalid fixtures for likely authoring mistakes.

All items remain `draft` until review is completed.

## Slice A — Empirical science

**Question:** How do environmental conditions change a measurable biological process within a defined experiment, and which conclusions can be generalized?

This slice tests:

- observations versus explanations;
- qualitative and quantitative evidence;
- controlled variables and confounding;
- causal scope;
- measurement uncertainty;
- classroom observations versus wider research evidence.

## Slice B — Formal model and systems

**Question:** Under which assumptions can delayed corrective feedback produce oscillation or instability, and where does the model stop representing reality?

This slice tests:

- formal definitions;
- equations and parameters;
- model-derived versus empirical claims;
- simulation output;
- assumptions and failure modes;
- prerequisite relations;
- analogy across domains without treating analogy as proof.

## Slice C — Socio-technical and ethical reasoning

**Question:** How can a digital recommendation system influence user choice, and which responses follow from the evidence and stated values?

This slice tests:

- empirical, interpretive, predictive, and normative claims;
- observational evidence and causal limitations;
- competing definitions;
- stakeholder perspectives;
- conflicts of interest;
- explicit value assumptions;
- credible disagreement and contested synthesis.

## Cross-slice tests

Together, the slices must demonstrate:

- one canonical contract across different kinds of knowledge;
- quantitative and qualitative evidence;
- domain-appropriate uncertainty without a universal truth score;
- support, challenge, contradiction, context, and illustration roles;
- revisions affecting dependent items;
- cross-domain connections without semantic overreach;
- stable IDs independent of file order;
- reproducible generated output;
- review requirements that vary by entity and domain.

## Work order

1. Author questions and source records.
2. Add evidence with precise locators and context.
3. Split statements into atomic claims.
4. Add concepts and models only when required.
5. Add controlled relations.
6. Draft a synthesis and trace every conclusion backward.
7. Add limitations, disagreement, and invalid fixtures.
8. Review the slice and record contract failures.
9. Revise the foundation before building the general validator.

## Completion rule

A slice is complete when a reviewer can understand and challenge its synthesis without reading implementation code, and when deleting every generated artifact removes no authored meaning or provenance.
