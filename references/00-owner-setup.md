# 00 — Owner Setup

Before the agent can operate, collect the project variables and access boundaries.

## Project variables

| Variable | Value | Notes |
|---|---:|---|
| Product / brand | `[PRODUCT]` | Exact spelling and casing |
| Domain | `[DOMAIN]` | Primary canonical domain |
| Market/language | `[MARKET]` | Example: `US-en`, `FR-fr`, `Global-en` |
| Category | `[CATEGORY]` | The entity/category AI engines should understand |
| Audience | `[AUDIENCE]` | Buyer/user/persona |
| CTA goal | `[CTA_GOAL]` | Signup, trial, demo, contact, purchase |
| CTA URL | `[CTA_URL]` | Must be live and UTM-safe |
| Competitors | `[COMPETITORS]` | 3–10 alternatives |
| Blog/docs path | `[CONTENT_PATHS]` | `/blog`, `/docs`, `/resources`, etc. |
| Sitemap URL | `[SITEMAP_URL]` | Usually `https://[DOMAIN]/sitemap.xml` |
| Brand voice | `[VOICE]` | Founder-led, technical, formal, casual, etc. |

## Owner-only checklist

The agent should not pretend to complete these if it lacks access.

### Search and analytics

- [ ] Add and verify `[DOMAIN]` in Google Search Console.
- [ ] Submit sitemap in Google Search Console.
- [ ] Create or confirm GA4 property and web stream.
- [ ] Define `[CTA_GOAL]` as a GA4 conversion event.
- [ ] Create an AI-source exploration/report or channel group in GA4.
- [ ] Export or connect GSC query/page data.
- [ ] Export or connect GA4 landing-page and conversion data.

### Technical access

- [ ] Confirm the website is live and canonical domain redirects correctly.
- [ ] Confirm CMS/repo access for page updates.
- [ ] Confirm deployment pipeline.
- [ ] Confirm robots.txt and sitemap.xml can be edited.
- [ ] Confirm schema/JSON-LD can be inserted.
- [ ] Confirm redirects/canonicals can be modified.

### SEO/GEO data sources

- [ ] Choose a keyword/rank data source.
- [ ] Confirm whether AI Overview or SERP-feature data is available.
- [ ] Confirm whether crawl data is available.
- [ ] Confirm whether competitor rank/backlink data is available.

### Product truth sources

- [ ] Approved product description.
- [ ] Pricing and packaging facts.
- [ ] Feature list and limitations.
- [ ] Customer proof, case studies, numbers, testimonials.
- [ ] Legal/compliance claims that need approval.
- [ ] Competitor-claim approval process.

## Agent handoff prompt

```text
You are the SEO/GEO Growth Agent for [PRODUCT]. Use the attached skill package.
Your north-star is qualified organic visibility that leads to [CTA_GOAL].
Start with a baseline audit, create the keyword-to-page map, identify P0 fixes,
and produce the first 7-day execution plan. Do not invent missing metrics; mark
unknowns and list owner tasks.
```
