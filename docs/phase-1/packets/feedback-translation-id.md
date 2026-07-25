# Review Packet — Indonesian Delayed-Feedback Translation

## Requested review

- translation equivalence by an accountable Indonesian–English reviewer
- control-systems domain competence or paired domain reviewer

## Exact primary target

- Entity: `claim:id:rekurensi-tertunda-yang-dinyatakan-berosilasi`
- Revision: `1`
- Translation source: `claim:en:stated-delayed-recurrence-oscillates`, revision 1
- Current staleness: `current`
- Current status: `draft`

## Full translated path

- `question:id:kapan-koreksi-tertunda-dapat-berosilasi`
- `model:id:rekurensi-koreksi-tertunda`
- `evidence:id:urutan-periodik-rekurensi-tertunda`
- `claim:id:rekurensi-tertunda-yang-dinyatakan-berosilasi`
- `claim:id:osilasi-model-tidak-membuktikan-osilasi-sistem-nyata`
- `concept:id:umpan-balik`
- `concept:id:osilasi`
- `synthesis:id:umpan-balik-tertunda-dan-osilasi`

Review stops if an English or Indonesian source revision changes.

## Equivalence requirements

The translation must preserve:

- exact recurrence;
- exact initial values;
- exact finite sequence;
- formal/model-derived claim kind;
- confidence limited to the stated mathematics;
- limitation that the model is not empirical evidence for a real system;
- distinction between oscillation, boundedness, convergence, and stability;
- distinction between feedback as a structural idea and one specific recurrence.

## Terminology table to review

| English | Current Indonesian | Review question |
|---|---|---|
| feedback | umpan balik | Is this standard and unambiguous in the intended educational register? |
| delayed feedback | umpan balik tertunda | Does “tertunda” preserve time-delay meaning? |
| recurrence | rekurensi | Should an explanatory gloss be added for senior-high or independent learners? |
| state | keadaan | Is “keadaan” sufficiently mathematical in context? |
| oscillation | osilasi | Does it avoid implying empirical periodic motion? |
| oscillatory sequence | urutan berosilasi | Is this the best technical rendering? |
| stability | kestabilan | Which qualified stability definition is intended? |
| bounded | terbatas | Could this be confused with a restricted domain rather than bounded magnitude? |
| convergence | konvergensi | Is the mathematical sense clear? |

## Sentence-level checks

For each translated entity:

1. Compare title, statement, scope, confidence rationale, and limitations.
2. Identify omitted or strengthened qualifiers.
3. Identify ambiguity introduced by word order or register.
4. Confirm that IDs and `work` identity match the intended source entity.
5. Confirm `translation.source_revision` equals the current English revision.
6. Confirm that examples and explanations do not exceed the source meaning.

## Current AI-assisted findings

See:

`content/reviews/records/feedback-translation-ai-assisted.json`

Open findings:

- major: accountable bilingual domain review of “urutan berosilasi” and the formal limitation is missing;
- minor: a controlled bilingual terminology register is needed.

## Pass conditions

A passing translation review should:

- target the exact Indonesian revision;
- name the English source revision;
- evaluate the complete translated path, not one isolated sentence;
- confirm or correct technical terms;
- preserve all qualifiers and limitations;
- record conflicts and qualifications;
- use a separate domain review when the translation reviewer cannot validate the mathematics.

## Promotion boundary

A passing translation review alone does not promote the translated model-derived claim. Structural, editorial, domain, methodological, and reproducibility coverage must also satisfy the promotion policy.
