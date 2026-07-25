---
contract: atlas-content/0.1
id: claim:en:users-should-have-recommender-explanation-and-choice
work: work:users-should-have-recommender-explanation-and-choice
type: claim
title: Users should have meaningful recommender explanation and choice
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
claim:
  kind: normative
  statement: Users should receive understandable information about major recommender parameters and meaningful options to influence or avoid profiling-based ranking where feasible.
  scope:
    systems: consumer-facing recommender systems that materially shape information exposure
  confidence: plausible
values:
  - autonomy
  - procedural fairness
  - accountability
  - accessibility
confidence_rationale: The recommendation follows only when the stated values are accepted and when explanation or choice can be implemented without creating greater harms.
argument:
  mode: normative
  premises:
    - claim:en:facebook-exposure-reflects-network-ranking-and-clicks
    - claim:en:twitter-ranking-changed-relative-political-amplification
    - claim:en:transparency-and-nonprofiling-are-eu-governance-responses
  values:
    - autonomy
    - accountability
    - accessibility
  conclusion: claim:en:users-should-have-recommender-explanation-and-choice
  alternatives:
    - independent auditing without individual controls
    - default chronological ordering
    - outcome-based safety requirements
limitations:
  - empirical evidence alone does not logically determine the normative conclusion
  - meaningful choice may conflict with safety, usability, privacy, or collective-risk objectives
---

This claim remains contestable and requires ethical review. The values and alternatives are part of the claim's reasoning, not hidden assumptions.
