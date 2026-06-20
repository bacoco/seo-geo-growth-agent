# 17 — AI Search Controls and Measurement

## Measurement stack

| Layer | Tool/source | What it measures | What it does not measure |
|---|---|---|---|
| Traditional Google Search | Google Search Console Performance | Queries, pages, clicks, impressions, CTR, position | AI Assistant referrals outside Google Search |
| Google generative AI features | GSC Search generative AI report, where available | Impressions from Google Search generative AI features by page/country/device/date | Conversions, answer accuracy, all AI assistant traffic |
| Google generative AI inclusion control | GSC Search generative AI control, where available | Whether a property is included/excluded from certain Google Search generative AI features | Google rankings outside those features, AI training control |
| Google snippet controls | `nosnippet`, `max-snippet`, `data-nosnippet` | Limits preview/direct snippet use in Google surfaces | Does not improve ranking; can reduce previews |
| Google training control | `Google-Extended` in robots.txt | Controls use for some Google AI model/product improvement contexts | Does not remove pages from Google Search indexing |
| Bing/Copilot AI | Bing Webmaster Tools AI Performance, where available | Citations, cited pages, grounding queries, page citation activity | Full answer absorption or GA4 conversions |
| Web analytics | GA4 AI Assistant channel/source group/custom exploration | Sessions and conversions from AI assistants that send referrers | Google AI Overview/AI Mode impressions; dark traffic; citations without clicks |
| Manual/API prompt tests | Controlled prompt set | Mentions, citations, competitor displacement, answer accuracy, absorption | Population-level demand unless prompt set is representative |

## Daily report fields

Add these when data exists:

```markdown
- GSC Search generative AI impressions: __ / unavailable / not enabled
- Bing AI citations: __ / unavailable
- GA4 AI Assistant sessions: __
- Other custom AI-source sessions: __
- Manual AI citation tests run: __
- Brand mention rate: __%
- Domain citation rate: __%
- Avg citation position: __
- Avg citation absorption score: __
```

## Google control decision matrix

| Goal | Recommended control | Notes |
|---|---|---|
| Appear in normal Google Search and Google AI features | Keep pages indexable, crawlable, snippet-eligible | Default for most commercial/local/SaaS pages |
| Exclude from Google generative AI features where control exists | Use GSC Search generative AI control if available | Document owner decision and expected visibility tradeoff |
| Limit text used in previews/AI features | Use `nosnippet`, `max-snippet`, or `data-nosnippet` | Can reduce snippet usefulness and click-through |
| Prevent Google Search indexing | Use `noindex` or remove/block appropriately | This is stronger than AI-feature exclusion |
| Restrict Google model/product improvement usage | Use `Google-Extended` robots directive | Separate from Search crawling/indexing |

## Bing measurement workflow

1. Verify the domain in Bing Webmaster Tools.
2. Check whether AI Performance is available for the site.
3. Export or record total citations, cited pages, sample grounding queries, and page-level activity.
4. Map cited pages to the keyword/prompt map.
5. Identify pages with citations but poor conversion paths.
6. Identify important pages with no citations but high commercial relevance.
7. Use IndexNow after major canonical updates.

## GA4 workflow

1. Check whether the property has native AI Assistant source/channel reporting.
2. Create a custom source group or channel group for AI referrers if needed.
3. Keep the custom group above generic Referrals when channel-group order matters.
4. Split AI Assistant referrals from Organic Search.
5. Treat Google AI Overviews / AI Mode as Organic Search unless GA4/GSC reports expose a separate metric.
6. Review source names monthly.
7. Track sessions, engaged sessions, conversions, landing pages, and assisted conversions from AI sources.

## Prompt-test measurement workflow

Use `templates/ai-visibility-test-plan.csv`.

Recommended minimum test set:

- 5 BOFU prompts;
- 5 comparison prompts;
- 5 category/best-for prompts;
- 5 how-to/implementation prompts;
- 5 brand/entity prompts;
- run each prompt across target engines;
- repeat important prompts 3–5 times or across sessions where possible;
- record engine, date, market, prompt, cited URLs, competitor domains, accuracy, and absorption.

## Reporting language

Use careful phrasing:

- Good: “In the tested prompt set, [DOMAIN] was cited in 4/20 prompts.”
- Good: “This suggests a selection gap for comparison prompts.”
- Bad: “AI engines will rank this page higher after adding FAQ.”
- Bad: “This `llms.txt` guarantees ChatGPT citations.”
