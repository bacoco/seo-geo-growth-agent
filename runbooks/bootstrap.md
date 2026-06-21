# SEO + GEO Growth Agent Bootstrap

Use this runbook after installation or when starting a new project with the skill.

## First Question

Ask the user for the smallest real target:

```text
Which site, page, article, or product should I improve first?
```

Do not invent a domain, audience, metrics, competitors, sources, or claims. Unknown inputs stay `unknown`.

## Required Inputs

Collect or infer only from supplied evidence:

| Input | Status |
|---|---|
| Canonical URL or page path | required |
| Business or institution name | required |
| Primary audience | required |
| Primary conversion or citation goal | required |
| Market and language | required |
| Analytics access: GSC, GA4, Bing, logs | available / unavailable |
| Owner policy for AI crawlers and training crawlers | allow / block / undecided |
| Source material for factual claims | provided / missing |
| User language for the report | infer from prompt |

## Choose One Starting Mode

For a domain or URL audit, choose **Full audit command** or **Visual HTML audit** by default. Choose plain
`Audit` only when the user explicitly asks for a chat-only answer, no files, or
no local report.

| Mode | Use when | First outputs |
|---|---|---|
| Audit | The user explicitly wants a chat-only audit or no generated files | P0/P1/P2 fixes, evidence table, next actions |
| Full audit command | The user wants a repeatable analysis plus generated improvement files | `audit.json`, screenshots when available, AI-layer ZIP, `index.html`, `report-validation.json`, local URL |
| Demo / doctor check | The user wants to know whether the skill works before using it on a real site | `demo-result.json`, golden audit validation status, optional installed package doctor status |
| Visual HTML audit | The user wants a browser-readable report, local server, site screenshots, responsive mobile/desktop checks, Design Watch, analysis cohorts, or visual proof | `audit.json`, `index.html`, local URL, site screenshot evidence, responsive study, Design Watch verdict |
| Evidence Engine audit | The user wants console/network/cache/CDN evidence or a more defensible technical report | `evidence-engine.json`, Console Watch, Network Watch, Cache/CDN Watch, first-screen metrics |
| Owner Data Mode | The user owns the site and wants real search, traffic, crawl, cache, or conversion evidence | owner-data request Markdown, JSON checklist, and CSV intake table |
| CLI audit workspace | The user wants a repeatable local audit workflow | `audit-plan.json`, workspace folders, next commands |
| ARD / ai-catalog | The user exposes a skill, MCP server, A2A agent, or AI service and wants agentic resource discovery | ARD readiness check, `ai-catalog.json` draft, validation result |
| `/for-ai` package | The page is important enough to be cited by agents | `/for-ai`, `/for-ai.json`, `/for-ai.txt`, `llms.txt` plan |
| Content brief | The user wants to create or rewrite a strategic page | keyword map, brief, outline, claim ledger |
| Crawler and measurement policy | The user asks about AI bots, robots.txt, visibility, or reporting | crawler matrix, robots draft, measurement plan |
| Public measurement access | The user asks what analytics or traffic data can be obtained publicly or with site ownership | public vs owner-only matrix, setup plan |
| Skill optimization | The user asks to apply lessons from GStack/GBrain or improve the skill itself | improvement map, eval updates, doctor checks |

## Execution Rules

1. Read `SKILL.md` first.
2. Read only the references needed for the selected mode.
3. Prefer templates over free-form prose.
4. Separate `Observed`, `Inferred`, and `Recommended`.
5. Never claim a metric, citation, source, customer, ranking, date, or crawler rule without evidence.
6. Treat `llms.txt` as optional and never as a Google ranking factor.
7. Show what cannot be concluded from the available data.
8. For full audit command work, read `runbooks/cli-audit.md` and use `scripts/run_full_audit.py` to collect evidence, generate improvement files, render HTML, validate the report, and optionally serve it.
9. For demo/doctor checks, run `scripts/skill_demo.py --output-dir ... --no-serve` and include the `demo-result.json` path.
10. For visual HTML audits, read `runbooks/visual-html-audit.md`, capture screenshots of the audited site, run the responsive mobile/desktop study, run Evidence Engine, run Design Watch, add analysis cohorts when useful, write `audit.json` in the user's language with `report_language`, and generate the report from that explicit evidence file. If screenshots fail, still generate the HTML report and document why screenshots are unavailable.
11. For analytics or traffic data questions, read `runbooks/public-measurement-access.md` and never confuse public estimates with owner analytics.
12. For skill improvement work, read `runbooks/gstack-gbrain-improvement-map.md` and `runbooks/skill-optimization.md`.
13. For ARD / ai-catalog work, read `runbooks/ard-ai-catalog.md`, check live discovery signals first, validate generated catalogs, and label ARD as draft/optional.

## First Useful Prompt

```text
Use seo-geo-growth-agent on [URL or page]. Generate the default visual HTML audit report, serve it locally, capture audited-site screenshots, run a mobile/desktop responsive study, rank P0 fixes, and mark missing data as unknown.
```

For a repeatable one-command run:

```text
Use seo-geo-growth-agent to run the full audit workflow on [URL], generate missing AI-layer files, validate the report, and serve the HTML report locally.
```

For a deterministic local demo:

```text
Use seo-geo-growth-agent demo mode to validate the golden audit and tell me the next command for auditing my own site.
```

For a browser-readable visual audit:

```text
Use seo-geo-growth-agent on [URL]. Generate a dynamic HTML audit report, serve it locally, capture desktop/mobile screenshots of the audited site, run a responsive mobile/desktop study, run Design Watch, add analysis cohorts, and mark missing data as unknown.
```

For an institutional article:

```text
Create a citation-safe /for-ai package for this article: [URL or text]. Include facts, limits, do-not-extrapolate guidance, and source/contact fields.
```
