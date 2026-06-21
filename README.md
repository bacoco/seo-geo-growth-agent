# SEO + GEO Growth Agent

<p align="center">
  <img src="assets/hero.png" alt="SEO + GEO Growth Agent turns a website into crawlable, understandable, citable AI-ready content" width="820">
</p>

Make your AI agent turn any website or institutional page into content that search engines can crawl, AI systems can understand, and assistants can cite without inventing facts.

Search is no longer just a list of blue links. AI assistants now read, summarize, compare, recommend, and sometimes act. This skill gives your agent a reusable operating system for that new layer: SEO fundamentals, GEO structure, agent-facing pages, crawler policy, measurement, templates, and hard guardrails against fake metrics or manipulative prompt tricks.

It does not stop at diagnosis: when AI-readable layers are missing, it generates an owner-review ZIP with the files to publish, the checks to run, and the limits the agent must preserve.

In short: it audits the site, explains the gaps, generates owner-review improvement files as drafts, renders a browser report, validates that the report is complete enough to share, and gives the site owner a clean intake path for real search, traffic, crawl, cache, and conversion data.

## Install

Paste this into Codex or Claude Code:

```text
Retrieve and follow the installation instructions at:
https://raw.githubusercontent.com/bacoco/seo-geo-growth-agent/v1.3.1/INSTALL_FOR_AGENTS.md
```

Or run it directly from a CLI:

```bash
codex "Retrieve and follow the installation instructions at https://raw.githubusercontent.com/bacoco/seo-geo-growth-agent/v1.3.1/INSTALL_FOR_AGENTS.md"
```

```bash
claude "Retrieve and follow the installation instructions at https://raw.githubusercontent.com/bacoco/seo-geo-growth-agent/v1.3.1/INSTALL_FOR_AGENTS.md"
```

Manual fallback:

```bash
git clone --depth 1 --branch v1.3.1 https://github.com/bacoco/seo-geo-growth-agent.git
cd seo-geo-growth-agent
./scripts/install.sh codex
```

```bash
./scripts/install.sh claude
```

For a custom skills folder:

```bash
./scripts/install.sh /absolute/path/to/skills/seo-geo-growth-agent
```

Custom paths must end with `seo-geo-growth-agent`. Existing installs are moved to a timestamped backup before the new files are copied. Then restart your agent session if installed skills are not auto-refreshed.

## Use It

```text
Use seo-geo-growth-agent to audit this site for SEO/GEO and rank the P0 fixes.
```

```text
Use seo-geo-growth-agent on this site and generate a dynamic HTML audit report served locally. Capture desktop/mobile screenshots of the audited site, run a responsive mobile/desktop study, run Design Watch, and add analysis cohorts.
```

```text
Use seo-geo-growth-agent to run the full audit workflow: collect evidence, generate missing AI-layer files, validate the report, and serve the HTML page.
```

```text
Use seo-geo-growth-agent demo mode to validate the golden audit, run the skill doctor if installed, and show me the next command to audit my own site.
```

```text
Use seo-geo-growth-agent with Evidence Engine: capture Console Watch, Network Watch, Cache/CDN Watch, owner-data request files, and a served HTML report.
```

```text
Generate an ARD /.well-known/ai-catalog.json draft for this skill or AI service, with representativeQueries and safe draft-status notes.
```

```text
Create a /for-ai page, /for-ai.json, and llms.txt plan for this institutional article.
```

```text
Build a BOFU keyword map, claim ledger, and content brief for this product.
```

```text
Write a safe robots.txt policy for search crawlers, AI search bots, user-triggered fetchers, and training crawlers.
```

## What It Solves

Most SEO playbooks stop at humans and Google. Most GEO advice is vague, hype-heavy, or dangerously close to prompt injection.

This skill solves the practical problem: how to publish content that is simultaneously useful to people, crawlable by search engines, readable by AI agents, and safe to cite.

It helps an agent produce:

- search and AI-readiness audits;
- keyword, fan-out, and grounding-query maps;
- direct-answer and evidence-led content briefs;
- `/for-ai`, `/for-ai.json`, `/for-ai.txt`, and `llms.txt` structures;
- downloadable AI-layer packages with `/llms.txt`, `/for-ai`, JSON, TXT, JSON-LD, optional `ai-catalog.json`, and an owner install checklist when those files are missing;
- crawler and robots.txt policy matrices;
- claim ledgers and citation-safe source registers;
- tabbed dynamic HTML audit reports with local serving, executive overview, animated readiness signal, lazy-load aware responsive mobile/desktop study, site screenshot analysis, Design Watch scoring, and analysis cohorts;
- Evidence Engine outputs for Console Watch, Network Watch, Cache/CDN Watch, and measurable first-screen Design Watch facts;
- ARD / `ai-catalog.json` drafts for agentic resource discovery, clearly marked as draft/optional;
- Owner Data Mode requests for GSC, GA4, Bing Webmaster Tools, server logs, Cloudflare Analytics, and paid-tool consent boundaries;
- a simple `scripts/seo_geo_audit.py` CLI that creates an audit workspace, browser evidence, owner-data request files, and next commands;
- a one-command `scripts/run_full_audit.py` workflow that collects evidence, creates a conservative `audit.json`, generates improvement files, renders the report, validates it, and can serve it locally;
- `scripts/validate_audit_report.py` to fail incomplete reports before they are shared;
- `scripts/skill_demo.py` to validate the committed golden audit and prove the local runtime is wired correctly;
- `LATEST-SEO-GEO-REPORT.md` receipts, preproduction/production gates, and narrative comparison between two reports;
- GEO/Citation prompt panels for ChatGPT, Perplexity, and Claude, clearly marked `ready_not_executed` until run;
- public-vs-owner-only measurement matrices plus owner-data intake CSVs for traffic, Search Console, GA4, logs, Cloudflare, and AI visibility;
- daily and weekly SEO/GEO reports;
- agent-readiness checks for DOM, accessibility tree, checkout, booking, and action flows.

## Why This One

It is opinionated where it matters and flexible where it should be.

- **No fake data:** unknown metrics stay unknown.
- **No hidden prompts:** agent-facing pages explain; they do not manipulate.
- **No SEO spam:** no fake authority, fake citations, fake reviews, doorway pages, or decorative schema.
- **Reusable templates:** every recommendation can become a file, table, checklist, or operating routine.
- **Agent-aware:** it treats AI systems as readers, recommenders, citation engines, and action intermediaries.
- **Verifiable:** the repository ships with a validation script and CI workflow.

## The Core Pattern

For important pages, the skill encourages a layered publication model:

```text
/article-or-page
/article-or-page/for-ai
/article-or-page/for-ai.json
/article-or-page/for-ai.txt
/llms.txt
JSON-LD in the HTML
```

The human page persuades and informs. The agent page clarifies context, fit, limits, and citation guidance. The JSON and TXT versions reduce ambiguity. `llms.txt` gives assistants a site map. JSON-LD keeps standard structured data aligned with visible content.

## Why ARD Matters

ARD / `ai-catalog.json` is for agentic resource discovery: skills, MCP servers, A2A agents, callable AI services, and other resources that an assistant may need to find before it can use them.

It answers a different question from SEO or `/for-ai`: not “should this page rank?” but “what agentic resource exists here, who publishes it, where is it, what can it do, and which honest representative queries describe when it is relevant?”

That is useful when a site exposes something operational, such as a skill, service, API, or agent workflow. The catalog can include `identifier`, `type`, `url` or inline `data`, `representativeQueries`, capabilities, and optional trust/provenance fields. It should be published at `/.well-known/ai-catalog.json`, referenced with `<link rel="ai-catalog">`, or pointed to from `robots.txt` with `Agentmap:` only after owner review.

Guardrail: ARD is draft discovery infrastructure, not a ranking factor, not a shortcut to Google visibility, and not a replacement for crawlable human content, schema.org, `/for-ai`, or verifiable sources.

## Make It Yours

After installing, start with:

1. `templates/owner-checklist.md` to collect access, sources, and constraints.
2. `templates/content-brief.md` for the first strategic page.
3. `templates/for-ai-page.md` and `templates/for-ai-json.json` for agent-facing content.
4. `templates/agent-interpretation-test.md` to test whether AI models preserve facts and limits.
5. `templates/claim-ledger.csv` to stop unsupported claims before they ship.

For the GEO idea behind `/for-ai`, read:

```text
references/21-mollick-geo-for-ai-agents.md
```

## What Gets Installed

`scripts/install.sh` copies only the runtime skill package:

```text
SKILL.md
INSTALL_FOR_AGENTS.md
manifest.json
LICENSE
references/
templates/
runbooks/
evals/
examples/reference-audit/
scripts/generate_html_audit_report.py
scripts/run_full_audit.py
scripts/validate_audit_report.py
scripts/generate_ai_layer_package.py
scripts/generate_owner_data_request.py
scripts/generate_ard_catalog.py
scripts/validate_ard_catalog.py
scripts/check_ard_readiness.py
scripts/compare_audit_reports.py
scripts/generate_geo_citation_panel.py
scripts/seo_geo_audit.py
scripts/serve_report.py
scripts/capture_site_screenshots.mjs
scripts/skill_demo.py
scripts/skill_doctor.py
```

Repository maintenance files such as `.github/`, `.gitignore`, `scripts/install.sh`, and `scripts/validate_skill.py` are not copied into the installed skill folder.

The installer refuses ambiguous custom destinations and only installs into a folder named `seo-geo-growth-agent`.

## Validate Changes

Before publishing changes to the repo:

```bash
python3 scripts/validate_skill.py
```

The validator checks required files, manifest paths, internal references, JSON/JSONL files, reference numbering, runtime script syntax, install smoke tests, backup behavior, and obvious secret patterns.

## Attribution

Adapted from `Gingiris/gingiris-seo-geo` and `Gingiris/gingiris-seo-geo-agent`.

Original source license: MIT License, Copyright (c) 2026 Gingiris (Iris Wei).
