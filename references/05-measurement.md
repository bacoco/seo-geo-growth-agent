# 05 — Measurement

## KPI hierarchy

| Layer | Metric | Source | Why it matters |
|---|---|---|---|
| Crawl/index | Indexed URLs / sitemap URLs | GSC, crawl | Pages cannot rank if not indexed |
| Visibility | Impressions, rankings, Top 10 count | GSC, rank API | Shows discovery and SERP progress |
| Engagement | CTR, organic sessions | GSC, GA4 | Shows snippet and intent fit |
| GEO | AI citations, AI-source sessions | Manual/API checks, GA4 | Shows AI-answer visibility and referral traffic |
| Conversion | CTA clicks, signups, demos, purchases | GA4, product analytics | Shows business outcome |

## Daily report calculations

- Top 10 count: number of tracked keywords with rank <= 10.
- Top 3 count: number of tracked keywords with rank <= 3.
- Top 30 count: number of tracked keywords with rank <= 30.
- Top 100 count: number of tracked keywords with rank <= 100.
- off-100: tracked keywords with no top-100 result.
- Index coverage: indexed canonical URLs / sitemap canonical URLs.
- CTR: clicks / impressions.
- Organic conversion rate: organic conversions / organic sessions.

Keep the tracked keyword set stable within a reporting period. When adding keywords, note the denominator change.

## High-impression low-CTR definition

A page/query is an opportunity when:

- Impressions are meaningfully above the site median or threshold.
- Average position is typically 1–20.
- CTR is below expected for that position and query type.
- The title/meta does not clearly match intent or lacks differentiation.

## AI-source tracking

Create a GA4 exploration or channel group for AI referral sources. Use this as a starter regex and update it as new sources appear:

```txt
(chatgpt|openai|perplexity|claude|anthropic|copilot|gemini|bard|deepseek|qwen|poe|you\.com|phind|edgeservices\.bing)
```

Recommended dimensions and metrics:

- Session source / medium.
- Landing page + query string.
- Sessions.
- Engagement rate.
- Key events / conversions.
- Revenue or pipeline value if available.

Caution: AI referrals can be under-attributed, stripped, or mixed into direct/referral traffic. Treat GA4 as a lower-bound indicator, not the full GEO picture.

## AI citation checks

Track a fixed set of queries weekly.

| Query | Engine | Date | Brand mentioned? | URL cited? | Competitors mentioned | Accuracy issue | Fix |
|---|---|---|---|---|---|---|---|

Use the same wording and market/language where possible. Record both citations and misstatements; correcting wrong entity descriptions is a GEO task.

## 2026 AI-search measurement addendum

When available, add separate sections for:

- Google Search generative AI impressions and pages from GSC.
- Bing Webmaster Tools AI Performance citations, cited pages, grounding queries, and page-level citation activity.
- GA4 AI Assistant sessions and conversions.
- Custom AI-source sessions using the regex/source group fallback.
- Manual prompt-test source selection and citation absorption.

Do not combine these into one metric. They answer different questions:

- GSC generative AI impressions = Google Search generative AI visibility.
- Bing AI citations = Microsoft/Bing AI-source exposure.
- GA4 AI Assistant sessions = visits with referrers from AI assistants.
- Manual prompt tests = observed answer behavior for a chosen prompt set.
- Absorption = whether cited content shaped the answer.

Use `references/09-ai-search-controls-measurement.md` and `templates/ai-visibility-test-plan.csv` for the workflow.
