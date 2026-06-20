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
| `/for-ai` package | The page is important enough to be cited by agents | `/for-ai`, `/for-ai.json`, `/for-ai.txt`, `llms.txt` plan |
| Content brief | The user wants to create or rewrite a strategic page | keyword map, brief, outline, claim ledger |
| Crawler and measurement policy | The user asks about AI bots, robots.txt, visibility, or reporting | crawler matrix, robots draft, measurement plan |

## Execution Rules

1. Read `SKILL.md` first.
2. Read only the references needed for the selected mode.
3. Prefer templates over free-form prose.
4. Separate `Observed`, `Inferred`, and `Recommended`.
5. Never claim a metric, citation, source, customer, ranking, date, or crawler rule without evidence.
6. Treat `llms.txt` as optional and never as a Google ranking factor.
7. Show what cannot be concluded from the available data.

## First Useful Prompt

```text
Use seo-geo-growth-agent on [URL or page]. Start with an evidence-led SEO/GEO audit, rank P0 fixes, and mark missing data as unknown.
```

For an institutional article:

```text
Create a citation-safe /for-ai package for this article: [URL or text]. Include facts, limits, do-not-extrapolate guidance, and source/contact fields.
```
