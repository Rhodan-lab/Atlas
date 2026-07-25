# Review Packet — Recommender Exposure and Governance

## Requested reviews

- domain: recommender systems and political communication
- methodological: observational and randomized platform studies
- legal-context: European Union Digital Services Act
- ethical: autonomy, accountability, accessibility, safety, and feasibility

## Exact primary targets

- `claim:en:facebook-exposure-reflects-network-ranking-and-selection`, revision 1
- `claim:en:twitter-ranking-changed-relative-political-amplification`, revision 1
- `claim:en:recommender-effects-require-context`, revision 1
- `claim:en:transparency-and-nonprofiling-are-eu-governance-responses`, revision 1
- `claim:en:meaningful-recommender-explanation-and-choice`, revision 1
- `synthesis:en:recommender-exposure-and-governance`, revision 1

## Evidence layers

### Observational platform evidence

The Facebook study is used for a platform- and period-specific pathway involving:

- social-network composition;
- ranking;
- potential exposure;
- encountered content;
- user selection or clicking.

The reviewer must confirm that observational evidence is not presented as a general causal estimate for all platforms.

### Randomized platform evidence

The Twitter study is used for a randomized comparison between ranked and reverse-chronological feeds under the study’s definitions and historical platform conditions.

The reviewer must confirm:

- the intervention and control condition;
- the meaning of algorithmic amplification;
- the population and period;
- limitations caused by platform-specific data and author relationships;
- whether causal wording remains within the experimental contrast.

### Legal context

The official DSA text is used narrowly:

- Article 27: recommender-system transparency and user influence options;
- Article 38: at least one non-profiling recommender option for covered very large services.

Review against the official consolidated text:

- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022R2065

The claim does not state that these measures are sufficient or empirically effective.

## Current legal and enforcement horizon

A July 10, 2026 European Commission preliminary finding concerning Instagram and Facebook focused on addictive design, including highly personalised recommender systems, infinite scroll, autoplay, and push notifications:

- https://digital-strategy.ec.europa.eu/en/news/commission-preliminarily-finds-addictive-design-instagram-and-facebook-breach-digital-services-act

This development is review context, not evidence that the canonical Article 27/38 claim is false. It demonstrates that current DSA recommender governance also involves systemic-risk and design obligations. Any new canonical claim requires a separate source, evidence record, and scoped revision.

## Methodological questions

1. Are exposure, attention, engagement, belief, and behavior kept distinct?
2. Are Facebook observational findings and Twitter randomized findings prevented from collapsing into one pooled effect?
3. Does the causal claim remain bounded to the randomized contrast and outcome definition?
4. Are platform employment and controlled-data access treated as conflicts requiring scrutiny rather than automatic invalidation?
5. Does historical product change trigger review-required or possibly-stale status?
6. Is the synthesis explicit about network, user, ranking, eligibility, moderation, and feedback-loop stages?
7. Would independent replication be possible from the available evidence?

## Ethical questions

- What makes an explanation meaningful rather than formally compliant?
- Which user choices are genuinely accessible and understandable?
- How should individual autonomy be balanced against safety and collective-risk objectives?
- Could user controls transfer responsibility from platforms to users without meaningful agency?
- Which groups may be disproportionately affected by profiling or non-profiling defaults?
- What alternatives should remain visible besides explanation and individual controls?

## Legal questions

- Is the Article 27 description exact and complete for the claim’s scope?
- Is Article 38 correctly limited to covered very large online platforms and search engines?
- Does the record need a consolidated-text date or applicability note?
- Which guidance, delegated acts, enforcement decisions, or judgments would trigger review?
- Is a three-month review horizon appropriate during active enforcement developments?

## Current AI-assisted findings

See:

`content/reviews/records/recommender-legal-context-ai-assisted.json`

Open findings:

- major: qualified legal-context review is required;
- minor: Articles 27 and 38 must not be presented as the complete DSA recommender-governance framework.

## Pass conditions

Each review type receives a separate `atlas-review/0.1` record. Promotion is blocked until:

- exact revision scope is confirmed;
- methodological and domain findings are resolved;
- legal applicability and horizon are confirmed;
- normative values and alternatives are reviewed;
- conflicts are disclosed;
- no open critical or major finding remains.
