# 02 — Technical SEO/GEO Foundations

## Technical SEO checklist

| Area | Check | Good state |
|---|---|---|
| Crawlability | robots.txt | Important public pages are not blocked |
| Indexability | noindex/canonical | Canonical pages are indexable; duplicates are canonicalized |
| Sitemap | sitemap.xml | Contains only canonical, indexable, 200-status URLs |
| Status codes | Crawl export | No important 4xx/5xx; redirects are intentional |
| Titles/metas | Crawl export | Unique, intent-matched, not truncated where possible |
| Headings | Page HTML | One clear H1; H2/H3 structure answers intent |
| Internal links | Crawl graph | Key pages reachable in 1–3 clicks; descriptive anchors |
| Performance | Core Web Vitals | No severe LCP/INP/CLS issues on key templates |
| Schema | Rich Results / validator | Valid and matches visible content |
| Freshness | Page content | Last updated date where relevant |

## GEO readiness checklist

| GEO factor | Implementation |
|---|---|
| Direct answer | First 100–150 words answer the core query clearly |
| Evidence table | Include facts, proof, comparisons, or criteria in a table |
| Entity clarity | Define what the product is, who it is for, and how it differs |
| Author/source trust | Add author, company, experience, proof, and contact/about links |
| FAQ | 5–8 high-intent questions with visible answers and FAQPage schema when appropriate |
| Structured data | Article, FAQPage, HowTo, SoftwareApplication, Product, Organization, BreadcrumbList as appropriate |
| AI crawler access | Review robots.txt policy for AI crawlers; deploy intentionally |
| llms.txt | Optional but useful for docs-heavy or agent-facing sites |
| IndexNow | Push new and significantly changed canonical URLs |
| Measurement | Track AI-source sessions and manual/API citation checks |

## robots.txt guidance

Use robots.txt intentionally. Do not blindly allow or block AI crawlers. Confirm the owner’s policy first.

Minimum pattern:

```txt
User-agent: *
Allow: /

Sitemap: https://[DOMAIN]/sitemap.xml
```

AI crawler entries can be added if the owner wants AI-search discovery. Keep a quarterly review because crawler names and policies change.

## llms.txt guidance

Use `llms.txt` to give AI agents a compact map of your canonical resources. It should not replace sitemap or schema.

Include:

- Product summary.
- Canonical docs and product pages.
- Pricing and comparison pages.
- Support, security, changelog, API docs.
- Contact/about pages.
- Rules for citations and brand/entity naming.

## IndexNow guidance

Use IndexNow for canonical URLs after:

- New page publication.
- Major page refresh.
- Pricing/package update.
- Comparison page update.
- Removal or redirect of important URLs.

Do not push duplicate, redirected, parameterized, or noindex URLs.

## 2026 technical addendum: crawler policy and agent readiness

- Separate AI search/discovery crawlers, model-training crawlers, user-triggered agents, and traditional search crawlers.
- Use the owner’s policy before drafting robots rules.
- Verify official crawler names and IP/rDNS guidance before deployment.
- Avoid blocking desired verified crawlers through WAF/CDN rules.
- Inspect key templates through HTML, rendered screenshot, and accessibility tree lenses.
- Prefer semantic buttons, links, labels, headings, and tables for both accessibility and agent readability.
- For docs-heavy sites, maintain optional `llms.txt` and `llms-full.txt` from the canonical sitemap/docs source of truth.

Use `references/10-agent-experience-ax.md`, `references/12-crawler-policy-matrix.md`, and the templates in `templates/`.
