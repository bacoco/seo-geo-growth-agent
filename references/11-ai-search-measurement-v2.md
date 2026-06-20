# AI-Search Measurement v2

AI-search visibility is under-attributed. Use multiple signals instead of relying on one tool.

## Measurement stack

| Signal | What it tells you | Limits | Owner |
|---|---|---|---|
| Google Search Console generative AI report | Impressions in Google generative AI Search features when available | Rollout may be partial; query-level data may be limited/unavailable | SEO / Analytics |
| Bing Webmaster Tools AI Performance | Cited pages and grounding query phrases in Microsoft/Bing AI answers | May be preview/limited; sparse citations may not surface | SEO |
| GA4 AI referral sessions | Sessions from ChatGPT, Perplexity, Claude, Gemini, Copilot, etc. | Referral sources can be inconsistent or missing | Analytics |
| Server logs | Bot access, crawl frequency, WAF blocks, status codes | Requires log access and bot verification | DevOps / SEO |
| Fixed prompt panel | Repeatable citation/mention monitoring across engines | Personalized, location/device/model variability | SEO |
| Rank tools / AI visibility tools | Scaled monitoring | Tool coverage and methodology vary | SEO |
| Conversion tracking | Business value of AI/search traffic | Attribution can be weak; UTMs not always present | Growth |

## Daily workflow

1. Pull search ranking and GSC data.
2. Pull GSC generative AI impressions if available.
3. Pull Bing AI Performance if available.
4. Pull GA4 AI referral segment using the regex template.
5. Check server logs for important bot blocks or unusual crawl spikes.
6. Run a fixed prompt panel for 10–30 priority queries.
7. Record whether the brand is cited, mentioned, absent, or misrepresented.
8. Prioritize pages with:
   - high traditional impressions but low CTR;
   - AI impressions without clicks/conversions;
   - Bing citations but stale/weak page structure;
   - bot access errors;
   - manual prompt mentions of competitors but not the brand.

## Fixed prompt panel design

For each business line, include:

- 5 BOFU prompts: “best [category] for [audience]”, “[brand] vs [competitor]”, “alternatives to [competitor]”.
- 5 MOFU prompts: “how to choose [category]”, “[category] implementation checklist”.
- 5 support/docs prompts: “how to do [task] in [tool/category]”.
- 3 brand prompts: “[brand] pricing”, “[brand] integrations”, “[brand] reviews”.

For each run, record:

- engine;
- account/location/language if known;
- date/time;
- exact prompt;
- cited URLs;
- brand mention position;
- sentiment/accuracy;
- wrong claims to fix;
- page to improve.

## Do not overclaim

Manual prompts are not a statistically complete measurement system. Use them as directional diagnostics and combine them with analytics and logs.
