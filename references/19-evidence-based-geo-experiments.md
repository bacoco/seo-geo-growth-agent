# 11 — Evidence-Based GEO Experiments

## Core idea

GEO should be measured as an experiment over prompts, pages, engines, and answer outputs. Do not rely on a single prompt, a single answer, or a generic “AI visibility score”.

## Measurement definitions

| Metric | Definition | How to record |
|---|---|---|
| Search trigger | The engine fetched/searched external web sources | Yes/no if visible or inferable |
| Source selection | The domain/page appears in cited sources or source list | Yes/no, cited URL |
| Brand mention | The brand is mentioned in the generated answer | Yes/no, exact phrase |
| Citation position | Order of the cited URL among sources | 1, 2, 3... |
| Citation absorption | The final answer uses facts, definitions, steps, comparison logic, or wording from the page | 0–5 manual score |
| Support quality | The cited page actually supports the answer claim | 0–5 manual score |
| Competitor displacement | Competitors cited instead of the target domain | Domains and cited pages |
| Accuracy gap | Wrong, stale, or misleading statement in answer | Short note and correction page |

## Absorption scoring rubric

| Score | Meaning |
|---:|---|
| 0 | Page not cited or not used |
| 1 | Page cited as weak background only |
| 2 | One minor fact or navigational reference used |
| 3 | Several facts or one section clearly support the answer |
| 4 | Answer uses multiple facts/criteria/examples from the page |
| 5 | Page substantially shapes the answer’s structure, recommendation, or evidence |

## Evidence-container scorecard

Use `templates/evidence-container-scorecard.csv` to score important pages before and after rewriting.

Content features to improve:

- title/query alignment;
- direct answer block;
- modular headings;
- definitions;
- numerical facts;
- comparison table;
- step-by-step procedure;
- caveats/limitations;
- source links;
- visible author/date/methodology;
- internal links;
- schema match;
- current price/spec/product facts;
- agent-friendly semantic HTML.

## Test design

1. Build prompt families from keyword clusters, not random prompts.
2. Include BOFU, comparison, best-for, how-to, local/ecommerce, and brand/entity prompts as relevant.
3. Pick one target URL for each prompt family.
4. Run across the engines that matter to the user’s market.
5. Record raw output summary, cited URLs, competitor URLs, and answer claims.
6. Score selection and absorption separately.
7. Rewrite pages based on observed gaps.
8. Re-test after crawling/recrawl windows and content propagation.
9. Keep screenshots/exports where possible.

## Rewrite playbook by failure mode

| Failure mode | Likely cause | Rewrite/action |
|---|---|---|
| Brand absent, competitors cited | Weak entity/category association or authority | Improve about/entity pages, comparison pages, internal links, third-party proof |
| Page selected but low absorption | Page lacks extractable evidence | Add definitions, stats, comparison tables, steps, caveats, direct answer |
| Citation but wrong fact | Stale or ambiguous page facts | Update canonical pricing/specs, add date, clarify limitations |
| Page not selected for comparison prompts | Missing “vs”, alternatives, criteria content | Build or improve comparison page and internal links |
| Local answer misses business | Weak local profiles or NAP inconsistency | Update Google Business Profile, Bing Places, local schema, reviews, location pages |
| Ecommerce answer misses product facts | Poor feed/spec completeness | Fix Merchant Center/product feed, Product schema, availability, price/spec table |
| Agent cannot complete task | UI/accessibility blocker | Fix semantic controls, labels, stable layout, WAF/CAPTCHA path |

## Confidence labels

Use:

- `High` — repeated prompt tests + analytics/reporting + page evidence agree.
- `Medium` — one or two evidence sources agree, but sample is small.
- `Low` — one-off answer, community anecdote, or unverified tool score.

Never present a one-off AI answer as a stable market fact.
