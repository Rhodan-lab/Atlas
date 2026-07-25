# Atlas Foundation Charter

## Status

Draft foundation document for Phase 0. This document defines product intent before implementation architecture.

## Purpose

Atlas is a local-first knowledge environment for an independent learner, researcher, or builder who wants to understand not only **what** is stated, but also:

- what the statement means;
- what evidence supports or challenges it;
- how certain or limited it is;
- which concepts it depends on;
- what it explains, predicts, or enables;
- where credible disagreement remains;
- how the understanding has changed over time.

Atlas should turn a collection of notes and sources into an inspectable structure of reasoning. It is a map of knowledge, evidence, models, uncertainty, and revision—not merely a graph visualization or note database.

## Core user outcome

A user should be able to follow a path from a question to a synthesis and inspect every important step:

```text
Question
  → relevant concepts
  → explicit claims
  → evidence fragments
  → original sources
  → relations and models
  → limitations and disagreements
  → current synthesis
  → unresolved questions
```

The system must preserve enough context for the user to judge the result rather than asking the user to trust an opaque answer.

## Foundational knowledge map

Atlas may eventually organize material across many domains, but its first conceptual foundation should support these recurring lenses:

1. **Knowledge** — what counts as knowing, explaining, and understanding.
2. **Evidence** — observation, measurement, testimony, documents, and data.
3. **Logic and argument** — inference, assumptions, validity, and fallacies.
4. **Mathematics** — formal structures, quantities, transformations, and proof.
5. **Statistics and uncertainty** — variation, estimation, probability, and confidence.
6. **Scientific inquiry** — hypotheses, models, experiments, replication, and revision.
7. **Systems** — components, interactions, feedback, emergence, and scale.
8. **Computation** — representation, algorithms, complexity, simulation, and automation.
9. **Language and meaning** — definitions, ambiguity, interpretation, and communication.
10. **Human cognition** — attention, memory, bias, learning, and mental models.
11. **Decision and action** — goals, trade-offs, prediction, risk, and strategy.
12. **Ethics and responsibility** — consequences, values, power, accountability, and limits.

These are not school subjects or a fixed course order. They are interoperable viewpoints that help knowledge from different fields connect without being flattened into one taxonomy.

## Product principles

### 1. Knowledge before interface

The content and reasoning model must remain useful without a graphical interface.

### 2. Claims before summaries

Important factual statements must be individually inspectable. A polished paragraph must not hide where its claims came from.

### 3. Evidence before authority

Source reputation matters, but Atlas must preserve the specific evidence, context, and limitations used to support a claim.

### 4. Connections without forced certainty

The system must represent support, contradiction, uncertainty, alternatives, and unresolved questions—not only clean positive links.

### 5. Revision is normal

Knowledge changes. Atlas must preserve why an item changed, what it replaced, and which downstream material may be affected.

### 6. Local ownership

The user should be able to inspect, export, and retain authoritative content without a mandatory cloud account.

### 7. Inspectable computation

Search, ranking, synthesis, validation, and derived views should expose their inputs and rules. AI may assist later, but it must not become an invisible source of truth.

### 8. Polyglot only by demonstrated need

Programming languages are implementation choices, not product features. A language is introduced only when a stable boundary and measurable advantage justify its cost.

## Explicit non-goals

Atlas is not intended to become:

- a generic folder-based notes application;
- a social network or public feed;
- a rigid online course, grading system, quiz platform, or streak tracker;
- an AI chatbot that answers without showing its reasoning materials;
- a résumé, portfolio, or productivity dashboard;
- a decorative knowledge graph with weak evidence structure;
- a system that automatically rewrites user knowledge without review;
- a marketplace of plugins before its contracts and governance are stable.

## Foundation success conditions

The foundation is successful when a small but representative body of knowledge can be authored and reviewed such that:

- concepts remain understandable outside the software;
- claims can be traced to evidence and original sources;
- competing claims can coexist without data loss;
- relations have precise meanings and directions;
- uncertainty and scope limits are visible;
- a synthesis can be regenerated from its supporting structure;
- revisions do not erase prior reasoning;
- implementation choices can change without rewriting the authored knowledge.

## Current interpretation

Atlas is presently a **knowledge-foundation project with an experimental software prototype**. The immediate task is to mature the conceptual and editorial system. Product engineering follows after the foundation passes its phase gate.
