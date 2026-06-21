---
name: seo-geo-growth-agent
description: |-
  SEO + GEO Growth Agent Skill v1.3.2. Use this when a user asks for SEO, Generative Engine Optimization, AI search visibility, professional audit workflows, demo/doctor checks, full audit command workflows, report validation, Evidence Engine diagnostics, Console Watch, Network Watch, Cache/CDN Watch, Owner Data Mode, ARD / ai-catalog agentic resource discovery, ARD validation/readiness checks, seo-geo-audit CLI workflows, Design Watch screenshot analysis, dynamic responsive study, lazy-load image diagnostics, first-impression scoring, analysis cohorts, dynamic HTML audit reports, latest report receipts, report comparison, preproduction gates, GEO/Citation prompt panels, browser-readable reports, downloadable AI-layer packages, site screenshot evidence, Agent Browser visual checks, ChatGPT Search / Perplexity / Claude citations, Google AI Overview or AI Mode readiness, Search Console and Bing Webmaster reporting, keyword strategy, structured data, IndexNow, robots.txt for AI crawlers, llms.txt, agent-friendly UX, accessibility-tree/DOM readiness, AI citation tracking, comparison pages, content briefs, CTR optimization, or an autonomous SEO/GEO daily operating workflow.
  Triggers: SEO, GEO, Generative Engine Optimization, AI search optimization, AEO, demo audit, skill demo, golden audit, Evidence Engine, Console Watch, Network Watch, Cache/CDN Watch, ARD, Agentic Resource Discovery, ai-catalog, /.well-known/ai-catalog.json, Agentmap, representativeQueries, owner data, owner-data request, owner-data intake, seo-geo-audit, audit CLI, Cloudflare Analytics, server logs, Design Watch, design audit, responsive audit, responsive study, lazy-load audit, preprod audit, production gates, latest SEO/GEO report, compare reports, report diff, GEO citation panel, prompt panel, mobile homepage audit, dynamic responsive study, first impression audit, analysis cohorts, HTML audit report, visual audit, local audit server, downloadable files, AI layer package, /for-ai package, screenshot audit, Agent Browser audit, ChatGPT SEO, Perplexity SEO, Claude SEO, AI Overview, AI Mode, AI citations, AI referrals, agent-friendly website, accessibility tree, AI crawler, crawler policy, robots.txt AI crawlers, Google-Extended, GPTBot, OAI-SearchBot, ClaudeBot, Claude-SearchBot, PerplexityBot, IndexNow, GSC, GA4, Bing Webmaster Tools, AI Performance, query fan-out, grounding query, schema markup, JSON-LD, llms.txt, content SEO, technical SEO, SEO agent, GEO patrol.
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
- generate a dynamic HTML audit report, serve it locally, run a full audit command, validate report completeness, capture desktop/mobile screenshots of the audited site, score first impression with Design Watch, and include the verdict in the global report;
- run an “SEO agent”, “SEO patrol”, “GEO patrol”, “AI visibility patrol”, or autonomous daily operating loop;
- make a site more usable by browser agents through semantic HTML, accessibility tree clarity, stable UI, and machine-readable commerce or booking flows.

## Default site-audit contract

When the user gives a domain or URL and asks to audit, analyze, run, use, or test this skill, default to a **visual HTML audit** unless the user explicitly asks for a chat-only answer or no files.

Required deliverables:

1. `reports/<site-slug>/<YYYY-MM-DD>/audit.json`
2. `reports/<site-slug>/<YYYY-MM-DD>/index.html`
3. a local report URL from `scripts/serve_report.py`
4. desktop and mobile screenshots of the audited site, or a clear `screenshot_status` explanation if the runtime cannot capture them
5. `responsive_study` for at least homepage mobile and desktop rendering, with lazy-load image state measured after scroll before recommending image fixes
6. `design_watch`, `analysis_cohorts[]`, and `evidence_engine` in `audit.json` when browser evidence is available
7. `report_language` set from the user's language, with the audit content written in that language
8. `ai_layer_package` plus downloadable files when `/llms.txt`, `/for-ai`, `/for-ai.json`, `/for-ai.txt`, aligned JSON-LD, or in-scope `ai-catalog.json` are missing or recommended
9. `report-validation.json` from `scripts/validate_audit_report.py`
10. `LATEST-SEO-GEO-REPORT.md` in the report folder so the user can identify the current valid artifact
11. `owner-data/owner-data-intake.csv` when owner data is requested or the full workflow generates owner-data request files

Do not stop at prose for a site audit. If screenshot capture fails because Agent Browser, Chrome, network, permissions, or a hostile WAF is unavailable, still generate `audit.json`, generate `index.html`, start the report server when possible, and mark screenshots as unavailable with the reason.

Use this sequence:

1. Read `runbooks/visual-html-audit.md`.
2. For a repeatable default run, use `python scripts/run_full_audit.py <url> --output-dir ... --lang ...`; it orchestrates evidence capture, owner-data request, ARD check, AI-layer package generation, HTML report generation, report validation, and optional local serving.
3. If doing a manual expert pass instead, gather public evidence from the audited URL, robots.txt, sitemap, HTML, and available public measurement sources.
4. Capture site screenshots, responsive study, and Evidence Engine output with Agent Browser or `node scripts/capture_site_screenshots.mjs --study-out ... --evidence-engine-out ...`; if using the script, rely on `imageLoadStates.missing_after_scroll`, not the initial image state, for image-load findings.
5. Analyze screenshots with `templates/design-watch-audit.md` and responsive evidence with `templates/responsive-dynamic-study.md`.
6. Write `audit.json` in the user's language, with `report_language`, findings, Design Watch, responsive study, Evidence Engine, cohorts, sources, and missing-data notes.
7. If agentic resources are in scope, run `python scripts/check_ard_readiness.py --url ... --output ...` and merge the result into `audit.json.ard_readiness` before generating downloadable files.
8. If AI-readable layers or in-scope ARD files are missing or recommended, run `python scripts/generate_ai_layer_package.py --input ... --output-dir ... --update-audit` to create the downloadable publication pack.
9. Run `python scripts/generate_html_audit_report.py --input ... --output-dir ...`; this writes `LATEST-SEO-GEO-REPORT.md`.
10. Run `python scripts/validate_audit_report.py --report-dir ... --output .../report-validation.json`; do not share incomplete reports without stating the validation failure.
11. Run `python scripts/serve_report.py --dir ... --port 8766 --open` or `--check` if serving is impossible.
12. Final response must include the report URL or exact `index.html` path, screenshot status, AI-layer package status, and report validation status.

If the user wants a repeatable local workflow, use `runbooks/cli-audit.md` and prefer `scripts/run_full_audit.py` for the complete flow. Use `scripts/seo_geo_audit.py` when the user only wants a workspace plan or browser evidence setup.

If the user asks whether the skill is installed or working, use `python scripts/skill_demo.py --output-dir ... --no-serve` from the source/runtime package. It validates the committed golden audit and writes `demo-result.json`; add `--install-dir` when checking an installed copy.

If the user asks for screenshots of the report UI, capture the served `index.html`
itself in desktop and mobile viewports after generation and use those screenshots
to judge the report presentation. Keep this separate from audited-site
screenshots, which remain evidence for Design Watch.

## First-use bootstrap

If this skill was just installed, or the user asks how to start, read `runbooks/bootstrap.md` before producing work. For a site/domain audit, choose visual HTML audit by default.

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

## Paid-tool consent

Before calling a tool that may consume credits or paid quota, such as Haloscan, Semrush, DataForSEO, Ahrefs, Similarweb, or SerpApi, ask the user for explicit approval. If approval is missing, continue with public evidence and label the missing data as `requires paid/owner data`. Use `runbooks/paid-tool-consent.md` and `templates/paid-tool-approval.md`.

## Evidence Engine and Owner Data Mode

- For browser-backed audits, use `runbooks/evidence-engine.md` and include `evidence_engine.console_watch`, `network_watch`, `cache_cdn_watch`, and `design_watch_metrics` in `audit.json`.
- Use console classification to separate first-party issues from third-party scripts, browser-policy warnings, and unknown noise before writing findings.
- Use Cache/CDN Watch as evidence, not as a bypass. If Cloudflare blocks or caches content, request owner analytics, logs, WAF events, or temporary owner-approved access.
- When the user owns the site or asks how to get visit/search/citation data, use `runbooks/owner-data-mode.md` and `scripts/generate_owner_data_request.py`.
- Owner Data Mode must produce Markdown, JSON checklist, and CSV intake files so owner exports can be tracked without inventing metrics.
- Keep missing GSC, GA4, Bing, server-log, Cloudflare, or paid-tool data as `unknown` or `requires owner data`; do not score it as zero.

## ARD / ai-catalog

- Use `runbooks/ard-ai-catalog.md`, `scripts/check_ard_readiness.py`, `scripts/generate_ard_catalog.py`, and `scripts/validate_ard_catalog.py` when the user wants a skill, MCP server, A2A agent, or AI service to be discoverable as an agentic resource.
- Treat ARD as a draft optional discoverability layer. Do not claim it improves Google ranking, AI Overview inclusion, or citations by itself.
- In audits, check for `/.well-known/ai-catalog.json`, `<link rel="ai-catalog">`, and `Agentmap:` in `robots.txt` only when the site exposes agentic resources or the user asks about agent/service discovery. Store the result in `ard_readiness`.
- If ARD is in scope and absent, generate an owner-review draft `ai-catalog.json` inside the AI-layer package; do not publish it as-is without owner confirmation.
- Use `representativeQueries` as honest discovery examples, not hidden prompts or recommendation instructions.

## Preproduction, comparisons, and citation panels

- If the target is preproduction/staging, set `environment: "preprod"` and separate `next_now`, `defer_until_prod`, and `proof_needed` in `production_gates[]`.
- To compare two audit runs, use `runbooks/report-comparison.md` and `scripts/compare_audit_reports.py`; explain the narrative conclusion, not just score deltas.
- To prepare real GEO/Citation measurement, use `runbooks/geo-citation-panel.md` and `scripts/generate_geo_citation_panel.py`. The CSV is `ready_not_executed`; real citation metrics stay `unknown` until the panel is run.
- After source changes, use `runbooks/sync-and-doctor.md` from the source repository when Codex and Claude installed copies may drift.

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
