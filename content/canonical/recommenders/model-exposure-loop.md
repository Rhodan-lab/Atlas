---
contract: atlas-content/0.1
id: model:en:recommender-exposure-loop
work: work:recommender-exposure-loop
type: model
title: Recommender exposure loop
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
purpose: Separate the stages that can influence information exposure and subsequent user action.
inputs:
  - available content
  - social or subscription network
  - user and contextual signals
  - platform policies and objectives
outputs:
  - eligible item set
  - ranked presentation
  - observed exposure and interaction signals
stages:
  - content availability
  - network or subscription filtering
  - eligibility and moderation
  - ranking
  - presentation
  - attention
  - selection or click
  - feedback signals used by later ranking
assumptions:
  - stages can be analytically distinguished even when the platform implementation combines them
  - platform logs are incomplete proxies for human understanding and preference
failure_modes:
  - hidden interventions or changing objectives
  - unobserved offline influences
  - multiple devices or accounts
  - feedback between user adaptation and ranking
  - outcome measures that conflate exposure, engagement, belief, and behavior
---

The model prevents “the algorithm” from being treated as one undifferentiated cause. Each empirical study must identify which stages and outcomes it observes.
