# SEO + GEO Growth Agent

<p align="center">
  <img src="assets/hero.png" alt="SEO + GEO Growth Agent turns a website into crawlable, understandable, citable AI-ready content" width="820">
</p>

Make your AI agent turn any website or institutional page into content that search engines can crawl, AI systems can understand, and assistants can cite without inventing facts.

Search is no longer just a list of blue links. AI assistants now read, summarize, compare, recommend, and sometimes act. This skill gives your agent a reusable operating system for that new layer: SEO fundamentals, GEO structure, agent-facing pages, crawler policy, measurement, templates, and hard guardrails against fake metrics or manipulative prompt tricks.

## Install

Paste this into Codex or Claude Code:

```text
Install the SEO + GEO Growth Agent skill from https://github.com/bacoco/seo-geo-growth-agent, then tell me when it is ready to use.
```

Or run it directly from a CLI:

```bash
codex "Install the SEO + GEO Growth Agent skill from https://github.com/bacoco/seo-geo-growth-agent"
```

```bash
claude "Install the SEO + GEO Growth Agent skill from https://github.com/bacoco/seo-geo-growth-agent"
```

Manual fallback:

```bash
git clone https://github.com/bacoco/seo-geo-growth-agent.git
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
- crawler and robots.txt policy matrices;
- claim ledgers and citation-safe source registers;
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
manifest.json
LICENSE
references/
templates/
```

Repository maintenance files such as `.github/`, `.gitignore`, and validation scripts are not copied into the installed skill folder.

The installer refuses ambiguous custom destinations and only installs into a folder named `seo-geo-growth-agent`.

## Validate Changes

Before publishing changes to the repo:

```bash
python3 scripts/validate_skill.py
```

The validator checks that required files exist, `manifest.json` points to real templates and references, and obvious secret patterns are not present.

## Attribution

Adapted from `Gingiris/gingiris-seo-geo` and `Gingiris/gingiris-seo-geo-agent`.

Original source license: MIT License, Copyright (c) 2026 Gingiris (Iris Wei).
