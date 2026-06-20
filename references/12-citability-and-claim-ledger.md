# 12 — Citability and Claim Ledger

A page is easier for AI systems and humans to cite when claims are explicit, sourced, current, and visible in HTML.

## Citability assets

| Asset | Purpose | Rules |
|---|---|---|
| Direct answer block | Gives a concise, quote-friendly answer | 40–80 words; no unsupported claims |
| Key facts table | Makes facts extractable | Include date, source/method, caveat |
| Comparison table | Supports BOFU decisions | State objective criteria; avoid fake superiority |
| Methodology box | Explains how data was collected | Include sample, date, limitations |
| Claim ledger | Tracks every risky/quotable claim | Source, owner, last verified, visible location |
| FAQ | Captures decision questions | Must match visible content and user intent |
| Update history | Signals freshness | Show material changes and review date |

## Claim risk levels

| Risk | Examples | Requirement |
|---|---|---|
| Low | Product feature, public integration, neutral description | Verify against product/source |
| Medium | “faster”, “cheaper”, “best for”, category comparison | Provide criteria and caveat |
| High | Statistics, benchmark, regulatory/legal/medical/financial claims | Provide source, date, methodology, owner review |
| Prohibited unless proven | “#1”, “guaranteed”, fake reviews, fake awards, fabricated customer outcomes | Do not publish |

## Page-level process

1. Extract every claim that could be quoted.
2. Add it to `templates/claim-ledger.csv`.
3. Remove or rewrite unsupported claims.
4. Make supporting evidence visible on the page, not only in schema.
5. Add dates and methodology for original data.
6. Link to primary sources where possible.
7. Re-check before refreshing comparison/pricing pages.

## GEO research insight, handled safely

Academic GEO work suggests that citations, relevant quotations, and statistics can increase visibility in generative-engine responses in controlled settings. Treat this as a content-quality hypothesis: add real sources, real quotes, and real statistics only when they improve the user’s understanding and can be verified. Never add fake citations or decorative numbers.
