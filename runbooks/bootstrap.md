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

## Choose One Starting Mode

| Mode | Use when | First outputs |
|---|---|---|
| Audit | The user has an existing site or page | P0/P1/P2 fixes, evidence table, next actions |
| Visual HTML audit | The user wants a browser-readable report, local server, site screenshots, Design Watch, analysis cohorts, or visual proof | `audit.json`, `index.html`, local URL, site screenshot evidence, Design Watch verdict |
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
8. For visual HTML audits, read `runbooks/visual-html-audit.md`, capture screenshots of the audited site, run Design Watch, add analysis cohorts when useful, and generate the report from an explicit `audit.json` evidence file.
9. For analytics or traffic data questions, read `runbooks/public-measurement-access.md` and never confuse public estimates with owner analytics.
10. For skill improvement work, read `runbooks/gstack-gbrain-improvement-map.md` and `runbooks/skill-optimization.md`.

## First Useful Prompt

```text
Use seo-geo-growth-agent on [URL or page]. Start with an evidence-led SEO/GEO audit, rank P0 fixes, and mark missing data as unknown.
```

For a browser-readable visual audit:

```text
Use seo-geo-growth-agent on [URL]. Generate a dynamic HTML audit report, serve it locally, capture desktop/mobile screenshots of the audited site, run Design Watch, add analysis cohorts, and mark missing data as unknown.
```

For an institutional article:

```text
Create a citation-safe /for-ai package for this article: [URL or text]. Include facts, limits, do-not-extrapolate guidance, and source/contact fields.
```
