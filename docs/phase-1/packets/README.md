# Phase 1 Review Packets

## Purpose

Each packet freezes a bounded review scope around exact canonical revisions. Reviewers should not need to understand the validator implementation or the experimental Atlas runtime.

The active packet set is English-only.

## Packets

| Packet | Primary review | Promotion blocked until |
|---|---|---|
| [`catalase-methodology.md`](catalase-methodology.md) | biochemistry and assay methodology | full-text assay interpretation and scope are confirmed |
| [`feedback-domain.md`](feedback-domain.md) | control systems and formal terminology | periodicity, stability, and model-to-world language are confirmed |
| [`recommender-governance.md`](recommender-governance.md) | recommender methodology, legal context, and ethics | evidence layers, current DSA context, and normative boundaries are reviewed |

## Reviewer instructions

1. Verify the exact entity ID and revision.
2. Read the canonical entity and directly linked source or evidence records.
3. Evaluate only the requested review type unless qualified for additional types.
4. Record conflicts before findings.
5. Classify each finding as critical, major, minor, or informational.
6. Do not edit findings away silently.
7. Submit one `atlas-review/0.1` record per review type.
8. Set `permits_promotion` only for the bounded review type and exact revision.
9. Use a review horizon for time-sensitive legal, policy, or platform conclusions.
10. Preserve disagreement rather than forcing consensus.

## Language boundary

No language-specific packet or bilingual terminology program is active in Phase 1. Translation behavior is tested only through synthetic fixtures and cannot generate a supported-language claim or review queue.

## Current AI-assisted findings

The records in `content/reviews/records/` are review preparation only. They may identify useful questions or defects, but they cannot satisfy independent human review requirements.

## Promotion boundary

A packet may receive multiple passing reviews and still remain blocked when another required review type is missing. The promotion gate, not an individual packet or reviewer, calculates the final coverage result.
