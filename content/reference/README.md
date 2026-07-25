# Phase 0 Reference Corpus

## Status

All material in this directory is a **draft foundation fixture**. It tests whether `atlas-content/0.1` can represent different forms of knowledge. It is not a reviewed encyclopedia and must not be presented as authoritative learning content.

## Why records are bundled here

The final authoring layout separates sources, evidence, claims, concepts, models, questions, and syntheses into individual files. During Phase 0, each vertical slice is bundled into one inspectable document so reviewers can evaluate the whole reasoning trail before the project commits to large-scale file organization.

Each bundled record includes the intended canonical ID and can be split mechanically after the contract passes review.

## Slices

| Slice | Primary test | Status |
|---|---|---|
| [`slice-a-catalase.md`](slice-a-catalase.md) | empirical observation, assay proxy, pH/temperature scope, mechanistic explanation | draft |
| [`slice-b-feedback.md`](slice-b-feedback.md) | formal model, derivation, assumptions, oscillation, analogy limits | draft |
| [`slice-c-recommenders.md`](slice-c-recommenders.md) | observational versus experimental evidence, platform context, normative reasoning, contested synthesis | draft |

## Required review

Before any slice can be marked reviewed:

- structural review of every bundled record;
- source and locator verification;
- editorial review of claim atomicity and scope;
- domain review;
- methodological review where inference is material;
- reproducibility review for calculations or simulations;
- ethical review for normative socio-technical conclusions;
- translation review for multilingual records.

## Fixture conventions

- Contract: `atlas-content/0.1`
- Structural tokens: English
- Human-readable content: English unless a translation fixture says otherwise
- Lifecycle status: `draft`
- Confidence labels include written rationale
- Numeric results include units or explicit unitless status
- Source descriptions use paraphrase and bibliographic metadata, not long copyrighted excerpts
- Synthetic observations are labeled synthetic and cannot support real-world factual claims

## Phase 0 acceptance test

The corpus succeeds only if reviewers can:

1. trace each material synthesis conclusion to claims, evidence, and source;
2. distinguish source facts, observations, model-derived results, interpretation, and values;
3. identify what would trigger revision;
4. detect invalid overgeneralization;
5. delete all generated artifacts without losing authored meaning;
6. split bundled records into canonical files without inventing new semantics.
