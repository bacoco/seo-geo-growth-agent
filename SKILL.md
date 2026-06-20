---
name: seo-geo-growth-agent
description: |-
  SEO + GEO Growth Agent Skill v1.1.1. Use this when a user asks for SEO, Generative Engine Optimization, AI search visibility, ChatGPT Search / Perplexity / Claude citations, Google AI Overview or AI Mode readiness, Search Console and Bing Webmaster reporting, keyword strategy, structured data, IndexNow, robots.txt for AI crawlers, llms.txt, agent-friendly UX, accessibility-tree/DOM readiness, AI citation tracking, comparison pages, content briefs, CTR optimization, or an autonomous SEO/GEO daily operating workflow.
  Triggers: SEO, GEO, Generative Engine Optimization, AI search optimization, AEO, ChatGPT SEO, Perplexity SEO, Claude SEO, AI Overview, AI Mode, AI citations, AI referrals, agent-friendly website, accessibility tree, AI crawler, crawler policy, robots.txt AI crawlers, Google-Extended, GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, IndexNow, GSC, GA4, Bing Webmaster Tools, AI Performance, query fan-out, grounding query, schema markup, JSON-LD, llms.txt, content SEO, technical SEO, SEO agent, GEO patrol.
---

# SEO + GEO Growth Agent Skill

## Purpose

Help the user win **two discovery surfaces at once**:

1. **Traditional search visibility** — crawling, indexing, ranking, snippets, CTR, and conversions from Google/Bing-style search.
2. **AI answer visibility** — being retrieved, understood, cited, linked, and acted on by AI search, answer engines, and browser/commerce agents.

This skill combines a strategic playbook with a daily execution SOP. It is adapted from the Gingiris `gingiris-seo-geo` strategy dataset and `gingiris-seo-geo-agent` execution dataset, under their MIT license, with additional research-derived guardrails and v1.1 modules for source-led research, AI crawler policy, agent-friendly UX, AI-search measurement, citability, entity/earned-media strategy, and agentic commerce readiness.

## Activation rules

Use this skill whenever the user asks to:

- audit a website, product page, blog, docs site, SaaS site, ecommerce site, marketplace, local business site, or open-source project for SEO/GEO;
- improve visibility in ChatGPT, Perplexity, Claude, Gemini, Google AI Overview / AI Mode, Bing/Copilot-style answers, or other AI answer engines;
- create or prioritize keywords, fan-out queries, grounding queries, content briefs, comparison pages, topic clusters, BOFU/MOFU/TOFU maps, CTA blocks, or internal links;
- generate or validate structured data, JSON-LD, robots.txt, sitemap, IndexNow, llms.txt, AI crawler access policies, or WAF allowlists;
- produce daily/weekly/monthly SEO reports from Google Search Console, GA4, Bing Webmaster Tools, DataForSEO, Ahrefs, Semrush, SerpApi, server logs, or supplied CSV exports;
- run an “SEO agent”, “SEO patrol”, “GEO patrol”, “AI visibility patrol”, or autonomous daily operating loop;
- make a site more usable by browser agents through semantic HTML, accessibility tree clarity, stable UI, and machine-readable commerce or booking flows.

## First-use bootstrap

If this skill was just installed, or the user asks how to start, read `runbooks/bootstrap.md` before producing work. Use it to choose one starting mode: audit, `/for-ai` package, content brief, or crawler and measurement policy.

## Non-negotiable guardrails

1. **Do not fabricate metrics.** If impressions, clicks, CTR, position, index coverage, rankings, traffic, conversions, citations, or AI referrals are not supplied or retrieved from tools, label them as `unknown` or `requires data`.
2. **Separate evidence from recommendations.** Use sections named `Observed`, `Inferred`, and `Recommended` when there is any ambiguity.
3. **Use source tiers.** Prefer official platform docs, product documentation, and first-party analytics. Treat academic papers as hypotheses to test. Treat GitHub and Reddit as idea sources, not proof.
4. **Current crawler policies can change.** When giving crawler names, robots.txt rules, WAF allowlists, or AI search inclusion advice, verify current vendor docs if browsing or docs access is available.
5. **No fake authority.** Do not invent customer logos, awards, backlinks, citations, reviews, ratings, founder stories, testimonials, datasets, benchmarks, or performance claims.
6. **No SEO/GEO spam.** Avoid keyword stuffing, doorway pages, scaled thin content, fake schema, hidden text, auto-generated review spam, and inauthentic mentions intended to manipulate search or AI answers.
7. **Structured data must match visible page content.** JSON-LD should represent what users can actually see on the page.
8. **Treat `llms.txt` as optional.** It may help some agents, docs workflows, or internal retrieval pipelines, but do not claim that it improves Google Search ranking or Google generative AI visibility.
9. **Robots.txt is a traffic-management signal, not security.** It cannot enforce privacy, and some crawlers may ignore or interpret it differently. Sensitive content must be protected by authentication or removal.
10. **Every page should have a conversion purpose.** If a page is not conversion-focused, define a softer conversion such as newsletter signup, docs signup, GitHub star, demo booking, trial start, contact, download, or internal next-click.
11. **Prioritize BOFU first.** For commercial sites, high-intent pages usually come before educational scale content.
12. **Make outputs executable.** Prefer tables, checklists, code snippets, file templates, ranked action plans, and owner assignments over generic advice.

## Source-led research policy

When the user asks for “deep research”, “latest”, AI crawler policies, AI-search measurement, platform changes, legal/high-stakes claims, or any niche/current topic:

1. Start with official sources.
2. Add primary technical docs and standards where relevant.
3. Add academic research only with uncertainty labels.
4. Add GitHub/open-source repos for implementation ideas.
5. Add Reddit/forums as community pain points and hypotheses, never as definitive evidence.
6. Convert findings into action items only when they pass the **Evidence → Impact → Effort → Risk** test.

Use `templates/source-led-deepresearch.md` to record source, date checked, finding, confidence, and proposed change.

## Core mental model

SEO and GEO share the same foundation: **a crawlable, useful, well-structured, credible page that answers a real user need.**

| Layer | SEO outcome | GEO / AI-answer outcome | Agentic outcome | Shared work |
|---|---|---|---|---|
| Crawlability | Search bots can fetch pages | AI search crawlers/fetchers can access pages | Agents can inspect required pages | robots.txt, sitemap, canonical, status codes, WAF rules |
| Indexability | Pages can enter search index | Pages can be retrieved by answer systems | Pages can be chosen as source of truth | noindex checks, canonical clarity, internal links |
| Relevance | Page ranks for target query | Page is selected as supporting source | Page answers a user task | keyword intent, fan-out coverage, headings, entity clarity |
| Extractability | Snippets/rich results can parse page | LLMs can quote facts/tables/steps | Agents can read facts and states | structured sections, facts tables, FAQ, comparison matrices |
| Trust | User and ranking systems trust page | AI systems prefer reliable sources | Agents avoid risky/ambiguous flows | bylines, dates, citations, first-hand proof, policies |
| Actionability | Search visit becomes business value | AI referral becomes business value | Agent can complete task | semantic buttons, labels, checkout/booking APIs, CTA tracking |

## Operating principles

### 1. BOFU → MOFU → TOFU

Start with bottom-funnel pages because they convert and clarify the business:

- pricing, alternatives, competitor comparison, “best X for Y”, “X vs Y”, migration, integration, template, calculator, use-case pages;
- then expand to middle-funnel guides, category pages, implementation docs, checklists;
- then scale top-funnel educational content only after the conversion path, internal linking, measurement, and entity clarity are ready.

### 2. One keyword intent = one primary landing page

Maintain a keyword-to-landing-page map. Avoid cannibalization by assigning exactly one primary page per important query cluster. Add fan-out queries and grounding queries to the same map rather than creating thin pages for every variation.

### 3. Structure for extraction, not just ranking

For every strategic page, include:

- a one-paragraph direct answer near the top;
- a key facts or key stats table when facts exist;
- a claim ledger for any statistic, benchmark, comparison, or claim that might be quoted;
- comparison tables for alternatives and use cases;
- concise FAQs that reflect visible page content;
- clear dates, authorship, methodology, and sources where relevant;
- JSON-LD only when it accurately represents visible content;
- visible text alternatives for important images, videos, PDFs, or charts.

### 4. Content must sound like a real operator

Use founder/operator voice, specific experience, tradeoffs, real examples, screenshots, benchmarks, implementation notes, “what we tried” sections, and limitations. Avoid generic AI prose.

### 5. Every recommendation maps to a measurable outcome

Every action should state expected movement in one or more of:

- impressions;
- clicks;
- CTR;
- average position;
- Top 3 / Top 10 / Top 30 count;
- index coverage;
- AI citations, AI impressions, or AI referrals;
- cited pages and grounding queries;
- crawl/log visibility from AI bots;
- CTA clicks;
- signups, purchases, demos, GitHub stars, downloads, or other goals.

## Required input fields

When possible, collect or infer:

```yaml
product_name: ""
domain: ""
primary_market: "US-en | UK-en | EU-en | FR-fr | EU-multilingual | zh-CN | ja-JP | ko-KR | other"
business_model: "SaaS | ecommerce | marketplace | agency | publisher | OSS | local | docs | community | other"
primary_cta_goal: "trial | demo | signup | purchase | contact | subscribe | star | download | booking | quote | other"
conversion_url: ""
target_audience: ""
competitors: []
existing_content_urls: []
gsc_export_or_access: "available | not_available"
ga4_export_or_access: "available | not_available"
bing_webmaster_export_or_access: "available | not_available"
server_log_access: "available | not_available"
rank_tool_export_or_access: "DataForSEO | Ahrefs | Semrush | SerpApi | other | not_available"
ai_visibility_tool_access: "available | not_available"
commerce_or_booking_flow: "none | product checkout | booking | quote request | local service | app signup | other"
constraints: "budget, CMS, dev access, language, legal/compliance, brand, privacy, WAF, rate limits"
```

If these are not available, proceed with a best-effort audit and clearly mark missing data.

## Default response shapes

### A. Site audit response

```markdown
# SEO/GEO Audit — [DOMAIN]

## Executive summary
- Current status: [observed / inferred]
- Biggest blocker: [P0]
- Fastest win: [P0/P1]
- Data confidence: High / Medium / Low

## P0 fixes — do first
| Priority | Issue | Evidence | Impact | Fix | Owner | Effort | Metric |
|---|---|---|---|---|---|---|---|

## Dual-engine readiness
| Area | SEO status | GEO/AI status | Agentic status | Recommendation |
|---|---|---|---|---|
| Crawlability | | | | |
| Indexability | | | | |
| Structured data | | | | |
| Direct answers | | | | |
| Tables/FAQ | | | | |
| Claims/sources | | | | |
| Internal links | | | | |
| Agent UX | | | | |
| Conversion tracking | | | | |

## Keyword / fan-out / grounding opportunities
| Cluster | Intent | Funnel | Primary page | Fan-out / grounding query | Evidence | Action |
|---|---|---|---|---|---|---|

## Technical snippets
[robots.txt / JSON-LD / IndexNow / redirects / canonical / WAF / accessibility-tree notes]

## 7-day action plan
Day 1...
```

### B. Daily SEO/GEO report

```markdown
# [PRODUCT] SEO/GEO Daily Report — YYYY-MM-DD

## Page-1 headline
- Google Top 10 keywords: N [▲/▼ vs previous period]
- Top 3: N | Top 30: N | Top 100: N
- Indexed URLs: N / sitemap total N (% coverage)
- Google generative AI impressions: N / unavailable
- Bing AI citations: N / unavailable
- AI referrals: N sessions | AI citations observed: N

## Keyword × landing page table
| Keyword | Page | Intent | Position | Δ | Impressions | Clicks | CTR | Volume | KD | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|

## AI-search measurement
| Source | Metric | Value | Pages | Confidence | Next action |
|---|---|---:|---|---|---|
| GSC Generative AI | Impressions | | | | |
| Bing AI Performance | Citations / grounding queries | | | | |
| GA4 | AI referral sessions | | | | |
| Server logs | AI bot hits | | | | |
| Manual prompt panel | Citations / mentions | | | | |

## High-impression / low-CTR pages
| Page | Query | Impressions | CTR | Position | Title fix | Meta fix |
|---|---|---:|---:|---:|---|---|

## Rank-push opportunities
| Keyword | Current position | Target | Page | Required action |
|---|---:|---:|---|---|

## GEO / AI-answer readiness
| Page | Direct answer | Key facts table | Claim ledger | FAQ | Schema | AI crawler access | Action |
|---|---|---|---|---|---|---|---|

## Agent readiness
| Flow | Semantic buttons/links | Labels | Stable layout | Blocking overlays | Test result | Action |
|---|---|---|---|---|---|---|

## Today’s 1–3 actions
1. [Action] → [expected metric]
2. [Action] → [expected metric]
3. [Action] → [expected metric]

## Owner blockers
- [OAuth/API/dev/CMS/legal/payment item]
```

### C. Content brief response

```markdown
# SEO/GEO Content Brief — [TARGET KEYWORD]

## Search intent
- Funnel: BOFU / MOFU / TOFU
- User job: [what the searcher is trying to decide/do]
- Primary CTA: [goal]

## Recommended URL and title
- URL slug:
- Title tag:
- Meta description:
- H1:

## Query model
| Seed query | Fan-out / related query | User sub-intent | Covered by section |
|---|---|---|---|

## Direct answer block
[40–80 words, citation-friendly, no unsupported claims]

## Claim ledger
| Claim | Evidence/source | Visible on page? | Last verified | Risk |
|---|---|---|---|---|

## Outline
H2/H3 structure with required sections.

## Required extraction assets
- Key facts table:
- Comparison table:
- FAQ questions:
- Schema type:
- Images/video/transcripts:

## Differentiation / trust
- Original experience to include:
- Data or screenshots to include:
- Founder/operator quote angle:
- Limitations/tradeoffs to state:

## Internal links
| From page | Anchor | To page | Purpose |
|---|---|---|---|
```

## Priority algorithm

When many opportunities exist, score them:

```text
Opportunity Score = (Intent Fit × 3) + (Business Value × 3) + (Impression Potential × 2) + (Ease × 2) + (GEO Extractability × 2) + (Agent Actionability × 1) - (Difficulty × 2) - (Spam/Risk × 3)
```

Use 1–5 scoring for each factor. Prioritize the highest score, but always fix P0 technical, measurement, and conversion blockers first.

## P0/P1/P2 taxonomy

- **P0:** prevents crawling, indexing, measurement, conversion, or safe agent execution. Examples: site blocked, noindex on money pages, broken canonical, missing CTA path, no GSC/GA4, pages returning 4xx/5xx, robots blocking desired search/AI crawlers, WAF blocking verified bots, duplicate/cannibalized money pages, checkout buttons implemented as inaccessible divs, critical facts only in PDFs/images.
- **P1:** high-impact ranking, citation, or conversion improvement. Examples: missing BOFU pages, weak titles on high-impression queries, no internal links to pages ranking 11–20, missing direct answer/table/FAQ on strategic pages, stale comparison pages, missing claim sources, poor accessibility tree for important flows.
- **P2:** scale and polish. Examples: additional TOFU content, optional llms.txt / llms-full.txt for non-Google agents and docs workflows, schema enrichment, image/video enhancements, design/UX polish, expansion into new languages, optional AI visibility tool integrations.

## Skill references

Use the files in `references/` for the full workflow:

- `references/00-owner-setup.md`
- `references/01-keyword-funnel.md`
- `references/02-technical-seo-geo.md`
- `references/03-content-production-sop.md`
- `references/04-operations-sop.md`
- `references/05-measurement.md`
- `references/06-schema-templates.md`
- `references/07-local-seo-addendum.md`
- `references/08-source-led-research-policy.md`
- `references/09-ai-crawler-policy.md`
- `references/10-agent-friendly-ux.md`
- `references/11-ai-search-measurement-v2.md`
- `references/12-citability-and-claim-ledger.md`
- `references/13-earned-media-entity-strategy.md`
- `references/14-agentic-commerce-readiness.md`
- `references/15-risk-red-team.md`
- `references/16-deep-research-upgrades-2026.md`
- `references/17-ai-search-controls-measurement.md`
- `references/18-agent-experience-ax.md`
- `references/19-evidence-based-geo-experiments.md`
- `references/20-crawler-policy-matrix.md`
- `references/21-mollick-geo-for-ai-agents.md`
- `references/22-agent-first-skillpack-quality.md`
- `references/99-source-register.md`

Use the files in `templates/` for copy-paste outputs and CSV trackers:

- `templates/agent-experience-audit.md`
- `templates/agent-readiness-audit.md`
- `templates/agent-interpretation-test.md`
- `templates/agentic-commerce-checklist.md`
- `templates/ai-citation-audit.md`
- `templates/ai-crawler-policy-matrix.csv`
- `templates/ai-feature-control-decision-matrix.md`
- `templates/ai-visibility-test-plan.csv`
- `templates/article-outline.md`
- `templates/bing-ai-performance-report.md`
- `templates/bot-access-policy-matrix.csv`
- `templates/claim-ledger.csv`
- `templates/comparison-page-outline.md`
- `templates/content-brief.md`
- `templates/daily-report.md`
- `templates/earned-media-entity-map.csv`
- `templates/evidence-container-scorecard.csv`
- `templates/for-ai-json.json`
- `templates/for-ai-page.md`
- `templates/ga4-ai-source-regex.txt`
- `templates/geo-red-team-checklist.md`
- `templates/grounding-query-map.csv`
- `templates/gsc-generative-ai-report.md`
- `templates/indexnow-request.json`
- `templates/keyword-map.csv`
- `templates/llms-full.txt`
- `templates/llms-generation-checklist.md`
- `templates/llms.txt`
- `templates/owner-checklist.md`
- `templates/query-fanout-map.csv`
- `templates/robots-ai-selective.txt`
- `templates/robots-ai.txt`
- `templates/server-log-ai-bot-audit.md`
- `templates/source-led-deepresearch.md`
- `templates/weekly-report.md`

Use `runbooks/bootstrap.md` for first project onboarding. Use `evals/routing-eval.jsonl` as the routing contract for future validator or host-level skill discovery tests.
