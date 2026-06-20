# SEO + GEO Growth Agent Skill v1.1

A combined SEO/GEO skill package for auditing, planning, and operating a search growth workflow across traditional search engines, AI answer engines, and emerging browser/commerce agents.

This package merges the **strategy layer** from the Gingiris `gingiris-seo-geo` dataset with the **execution SOP layer** from `gingiris-seo-geo-agent`, then adds practical output formats, measurement guardrails, and research-derived cautions about AI-search claims.

## Install

Clone and install for Codex:

```bash
git clone https://github.com/bacoco/seo-geo-growth-agent.git
cd seo-geo-growth-agent
./scripts/install.sh codex
```

Install for Claude Code:

```bash
./scripts/install.sh claude
```

Install to a custom skill directory:

```bash
./scripts/install.sh /absolute/path/to/skills/seo-geo-growth-agent
```

Validate the repository before publishing changes:

```bash
python3 scripts/validate_skill.py
```

The install script copies only the runtime skill package: `SKILL.md`, `manifest.json`, `LICENSE`, `references/`, and `templates/`. Repository files such as `.github/`, `.gitignore`, and validation scripts stay outside the installed skill folder.

## What changed in v1.1

- Added a **source-led research policy** so official platform docs outrank hype, GitHub experiments, and Reddit claims.
- Added an **AI crawler policy module** that separates search/indexing bots, training bots, user-triggered fetchers, and ads/validation bots.
- Added **agent-friendly UX checks** for DOM, accessibility tree, semantic controls, stable layouts, labels, and checkout/booking flows.
- Added **AI-search measurement v2** covering Google Search Console generative AI impressions, Bing Webmaster Tools AI Performance, GA4 AI referrals, server logs, and fixed prompt panels.
- Added a **claim ledger and citability framework** so statistics, comparisons, and “best” claims are visible, sourced, and safe to quote.
- Added **earned-media/entity strategy** for authentic third-party sources, review surfaces, directories, community evidence, and brand consistency.
- Added an **agentic commerce readiness addendum** for ecommerce, local, booking, quote, and product-flow sites.
- Added a **red-team checklist** against manipulative GEO, fake mentions, thin scaled pages, unsupported stats, and crawler-policy mistakes.
- Added a plain-English guide to the Ethan Mollick GEO pattern for AI agents and institutional content.
- Added reusable `/for-ai`, `/for-ai.json`, and agent interpretation test templates.
- Fixed the v1 file tree references to match the actual `references/` and `templates/` directory names.

## Files

```text
seo-geo-growth-agent-skill-v2/
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── LICENSE
├── manifest.json
├── scripts/
│   ├── install.sh
│   └── validate_skill.py
├── references/
│   ├── 00-owner-setup.md
│   ├── 01-keyword-funnel.md
│   ├── 02-technical-seo-geo.md
│   ├── 03-content-production-sop.md
│   ├── 04-operations-sop.md
│   ├── 05-measurement.md
│   ├── 06-schema-templates.md
│   ├── 07-local-seo-addendum.md
│   ├── 08-source-led-research-policy.md
│   ├── 09-ai-crawler-policy.md
│   ├── 10-agent-friendly-ux.md
│   ├── 11-ai-search-measurement-v2.md
│   ├── 12-citability-and-claim-ledger.md
│   ├── 13-earned-media-entity-strategy.md
│   ├── 14-agentic-commerce-readiness.md
│   ├── 15-risk-red-team.md
│   ├── 16-deep-research-upgrades-2026.md
│   ├── 17-ai-search-controls-measurement.md
│   ├── 18-agent-experience-ax.md
│   ├── 19-evidence-based-geo-experiments.md
│   ├── 20-crawler-policy-matrix.md
│   ├── 21-mollick-geo-for-ai-agents.md
│   └── 99-source-register.md
└── templates/
    ├── agent-experience-audit.md
    ├── agent-readiness-audit.md
    ├── agent-interpretation-test.md
    ├── agentic-commerce-checklist.md
    ├── ai-citation-audit.md
    ├── ai-crawler-policy-matrix.csv
    ├── ai-feature-control-decision-matrix.md
    ├── ai-visibility-test-plan.csv
    ├── article-outline.md
    ├── bing-ai-performance-report.md
    ├── bot-access-policy-matrix.csv
    ├── claim-ledger.csv
    ├── comparison-page-outline.md
    ├── content-brief.md
    ├── daily-report.md
    ├── earned-media-entity-map.csv
    ├── evidence-container-scorecard.csv
    ├── for-ai-json.json
    ├── for-ai-page.md
    ├── ga4-ai-source-regex.txt
    ├── geo-red-team-checklist.md
    ├── grounding-query-map.csv
    ├── gsc-generative-ai-report.md
    ├── indexnow-request.json
    ├── keyword-map.csv
    ├── llms-full.txt
    ├── llms-generation-checklist.md
    ├── llms.txt
    ├── owner-checklist.md
    ├── query-fanout-map.csv
    ├── robots-ai-selective.txt
    ├── robots-ai.txt
    ├── server-log-ai-bot-audit.md
    ├── source-led-deepresearch.md
    └── weekly-report.md
```

## How to use

Place this folder wherever your agent or skill runner expects skills. The important root file is `SKILL.md`.

For a plain-English explanation of GEO through the Ethan Mollick `Co-Existence` case and an institutional article blueprint, read [`references/21-mollick-geo-for-ai-agents.md`](references/21-mollick-geo-for-ai-agents.md).

Example prompts:

```text
Audit my SaaS site for SEO/GEO and rank the P0 fixes.
Run today's SEO/GEO patrol from this GSC export and GA4 export.
Build a BOFU keyword map and query fan-out map for my product and competitors.
Create a comparison page brief for [Product] vs [Competitor] with a claim ledger.
Generate JSON-LD for this article, but only for visible content.
Write a robots.txt policy that allows AI search crawlers but blocks training crawlers where possible.
Audit whether my checkout flow is agent-friendly from DOM/accessibility-tree signals.
Use Bing AI Performance and Google generative AI impressions to prioritize pages.
```

## Data rules

The skill is intentionally strict about data quality. It should not invent rankings, traffic, conversions, citations, impressions, or AI visibility. If Search Console, GA4, Bing Webmaster Tools, server logs, DataForSEO, or another source is not available, it should say so and produce a best-effort checklist instead of fake metrics.

## Important cautions

- For Google Search generative AI surfaces, treat GEO as SEO fundamentals plus stronger content usefulness, crawlability, and technical clarity. Do not sell `llms.txt`, chunking, or “AI-only writing” as Google visibility hacks.
- `llms.txt` and `llms-full.txt` are optional artifacts for non-Google agents, docs workflows, or internal retrieval. They are not a substitute for crawlable HTML.
- Crawler names, IP lists, WAF policies, and AI-search reports change. Verify official docs before deploying production robots.txt or firewall changes.
- Reddit and GitHub are useful for discovering pain points and tool ideas; they are not proof that a tactic works.

## Attribution

Adapted from:

- `Gingiris/gingiris-seo-geo`
- `Gingiris/gingiris-seo-geo-agent`

Original source license: MIT License, Copyright (c) 2026 Gingiris (Iris Wei).

This derived package preserves the MIT license notice and adds new structure, guardrails, and templates.
