# 16 — Deep Research Upgrades 2026

Research date: 2026-06-20

This file translates external research into operational improvements for the SEO/GEO Growth Agent. Treat this as a living research note, not a frozen standard.

## 1. Official search/analytics changes to add

### Google Search generative AI surfaces

Operational implications:

- Google AI Overview / AI Mode visibility should be treated as part of Google Search eligibility, not as a separate “LLM ranking” shortcut.
- Start with crawlability, indexability, helpful content, page experience, internal links, visible text, structured data that matches visible content, merchant/local feeds, and snippet controls.
- Do not claim `llms.txt` or AI-only schema is required for Google AI features.
- Use Search Console generative AI reporting/control features only if the property has access. Do not imply all accounts have it.
- When the owner wants to limit participation in Google generative AI features, document the difference between Search generative AI inclusion controls, snippet controls, `Google-Extended`, and `noindex`.

### Bing / Microsoft AI Performance

Operational implications:

- Add Bing Webmaster Tools AI Performance to the measurement stack when available.
- Track total citations, cited pages, sample grounding queries, page-level citation activity, and competitor patterns.
- Use IndexNow for freshness after publishing, refreshing, deleting, or redirecting important canonical URLs.
- For local businesses, include Bing Places alongside Google Business Profile.

### GA4 AI Assistant traffic

Operational implications:

- Use native GA4 AI Assistant traffic/channel/source grouping where available.
- Keep a custom fallback channel group or exploration for known AI referrers because source names change and rollout may differ by property.
- Remember that Google AI Overviews and AI Mode are typically counted within Organic Search, not the AI Assistant channel.
- Do not merge Google AI feature impressions with AI assistant referrals; they answer different questions.

## 2. Academic GEO findings to operationalize

### Selection is not absorption

A source can appear in a citation list without materially shaping the answer. The v1.1 skill therefore measures:

1. **Search trigger** — did the engine search/fetch?
2. **Source selection** — was the domain/page selected or cited?
3. **Citation position** — where did it appear among citations?
4. **Citation absorption** — did the final answer reuse the page’s definitions, facts, steps, comparisons, or phrasing?
5. **Support quality** — does the cited page actually support the answer claim?
6. **Competitor displacement** — which competitor domains were used instead?

### Evidence-container content wins more often than formatting-only changes

Operational content pattern:

- one clear answer block;
- explicit definitions;
- numbers and statistics with sources;
- comparisons and decision criteria;
- procedural steps;
- caveats, limitations, and “when not to choose” sections;
- modular headings aligned with likely prompts;
- visible author, date, methodology, and source transparency.

Avoid treating FAQ formatting, authoritative tone, or keyword repetition as the intervention. The value is the evidence inside the page.

## 3. GitHub/open-source tooling ideas to borrow carefully

Observed useful patterns from open-source tooling:

- `llms.txt` generators that crawl sitemaps and output curated model-readable resource maps.
- AI-referrer regex repositories for GA4/channel grouping.
- GEO audit CLIs that score pages, generate robots/schema/llms recommendations, and test whether AI engines cite a site.
- CI/CD-friendly workflows for running crawl, schema, freshness, and citation tests after deployment.

Operational cautions:

- Do not adopt abandoned tools blindly.
- Do not copy inflated claims from tool READMEs into client recommendations.
- Prefer using the patterns: sitemap-to-resource-map, repeatable audit scorecards, prompt test CSVs, and CI checks.
- Keep any generated `llms.txt` or `llms-full.txt` synchronized with canonical URLs and page facts.

## 4. Reddit/community observations

Community measurement discussions are useful for discovering practical GA4 regex patterns and rollout surprises, but they are not authoritative.

Operational use:

- Use Reddit/forum patterns as weak signals only.
- Prefer official GA4 channel definitions when available.
- Keep a custom source regex in parallel because AI referrer names change and properties may see different rollout behavior.
- Split Google AI feature impressions, AI Assistant referrals, and manual citation tests into separate metrics.

## 5. v1.1 upgrade checklist

- [ ] Add GSC Search generative AI report fields to daily/weekly reports.
- [ ] Add Bing Webmaster Tools AI Performance fields to reports.
- [ ] Add GA4 AI Assistant + custom source regex workflow.
- [ ] Add citation absorption to AI visibility audits.
- [ ] Add evidence-container scorecard to content briefs.
- [ ] Add crawler policy matrix with crawler type and desired owner policy.
- [ ] Add agent-friendly UX/accessibility tree audit.
- [ ] Add `llms.txt` generation checklist and `llms-full.txt` template.
- [ ] Add freshness workflow: last updated dates, changelog, sitemap `lastmod`, IndexNow, ETag/Last-Modified where applicable.
- [ ] Add local/ecommerce visibility sources: Merchant Center, Google Business Profile, Bing Places, product feeds, price/spec completeness.

## Source categories checked

- Google Search Central / Google Analytics official docs and blog posts.
- Bing Webmaster Tools official blog.
- OpenAI, Perplexity, Anthropic crawler documentation.
- Google/web.dev agent-friendly website guidance.
- arXiv GEO and AI citation measurement papers.
- GitHub repositories for `llms.txt`, GEO audit tools, and AI-referrer regexes.
- Reddit/community GA4 and AI-referrer measurement discussions.
