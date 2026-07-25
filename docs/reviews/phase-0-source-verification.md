# Phase 0 Source Verification Ledger

## Status

- **Review type:** source verification
- **Date:** 2026-07-26
- **Method:** AI-assisted comparison against primary bibliographic indexes, author repositories, DOI records, and official legal text
- **Outcome:** metadata and locator checks completed for the canonical Phase 0 sources listed below
- **Authority limit:** this is not independent human domain, methodological, legal, or ethical review

The purpose of this ledger is to show what was checked and what was not. It does not promote any canonical entity from `draft`.

## Verification results

| Canonical source | Authority checked | Identifier or locator | Result | Remaining limitation |
|---|---|---|---|---|
| `src:aebi-1984-catalase-in-vitro` | PubMed | PMID 6727660; DOI 10.1016/S0076-6879(84)05016-3 | title, author, container, volume, pages, year, and DOI matched | PubMed record has no abstract; method interpretation needs full-text and domain review |
| `src:wu-lin-wolfbeis-2003-catalase-assay` | PubMed | PMID 12895476; DOI 10.1016/S0003-2697(03)00356-7 | title, authors, journal, date, pages, DOI, and abstract-level pH statement matched | the assay-specific interpretation needs methodological review and should not be universalized |
| `src:astrom-murray-2008-feedback-systems` | CaltechAUTHORS | author-repository record `yzs24-xsx88` | title, authors, publisher, year, and open repository locator matched | terminology and inference boundaries need control-systems review |
| `src:bakshy-messing-adamic-2015-diverse-news` | Science DOI and PubMed bibliographic record | PMID 25953820; DOI 10.1126/science.aaa1160 | title, authors, journal, volume, issue, pages, date, and DOI matched | source interpretation remains observational, platform-specific, and dependent on platform-controlled data |
| `src:huszar-et-al-2022-algorithmic-amplification` | PubMed and PMC | PMID 34934011; PMCID PMC8740571; DOI 10.1073/pnas.2025334119 | title, authors, journal, date, identifiers, randomized-control description, and disclosed employment/consulting context matched | political-content definitions, amplification metric, and generalization need methodological and domain review |
| `src:eu-2022-digital-services-act` | EUR-Lex official text | CELEX 32022R2065; Articles 27 and 38 | regulation identity, official locator, recommender transparency provision, and non-profiling option provision matched | legal interpretation and later authoritative guidance remain time-sensitive and require legal-context review |

## Internal generated source

`src:synthetic-feedback-run-delay-one-gain-one` is not an external publication. Its origin is the repository fixture itself, its procedure is explicit, and its output is independently recalculated by the validator test suite. It must never be presented as empirical evidence about a real system.

## Checks performed

- matched titles and author lists where authoritative metadata was available;
- matched publication containers, dates, pages, and identifiers;
- checked that canonical locators resolve to the intended source family;
- checked that evidence descriptions do not exceed the source scope visible in the verified record;
- recorded employment, data-access, assay-specific, observational, and time-sensitive legal limitations;
- avoided reproducing long source passages.

## Checks not performed

- complete full-text scientific review of every article;
- independent recalculation of published empirical results;
- domain-expert judgment of biochemical, control-system, recommender-system, political-communication, or legal claims;
- ethical approval of the normative recommender claim;
- verification that future amendments or guidance leave the DSA interpretation unchanged.

## Findings

### Resolved

- The fluorescent catalase source is correctly attributed to Meng Wu, Zhihong Lin, and Otto S. Wolfbeis.
- The Twitter source includes the reported randomized-control design and employment/consulting disclosure context.
- The DSA evidence is split into a legal-descriptive claim and does not claim empirical effectiveness.
- Synthetic feedback output has an explicit generated source and cannot be confused with observed-world evidence.

### Still pending external review

- biochemistry and assay-method interpretation;
- formal control-system terminology;
- platform-study methodology and generalization;
- legal-context interpretation and review horizon;
- ethical review of autonomy, accountability, and user-choice recommendations;
- Indonesian translation terminology and equivalence.

## Conclusion

The canonical source metadata and locator layer is sufficiently explicit for mechanical Phase 0 verification. The evidence and claims remain `draft` until the appropriate independent human reviews are recorded for their exact revisions.
