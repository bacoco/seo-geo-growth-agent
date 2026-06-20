# 00 — Owner Setup

Before running the SEO/GEO agent, define the business, conversion goal, measurement access, and risk limits.

## Required owner inputs

| Field | Why it matters |
|---|---|
| Product / domain | Establishes entity and site scope |
| Primary CTA | Prevents traffic-only SEO |
| Market / language | Changes query intent and SERP sources |
| Competitors | Seeds BOFU and comparison opportunities |
| CMS / stack | Determines implementation path |
| GSC / GA4 / Bing access | Enables measurement and prioritization |
| Server logs / WAF access | Enables crawler and AI bot audit |
| Legal / compliance limits | Prevents unsafe claims |

## Initial setup checklist

- [ ] Confirm canonical domain and protocol.
- [ ] Confirm sitemap location.
- [ ] Confirm robots.txt location.
- [ ] Confirm GSC property type and access.
- [ ] Confirm GA4 property and conversion events.
- [ ] Confirm Bing Webmaster Tools access, if available.
- [ ] Confirm rank-tracking or SERP API access, if available.
- [ ] Confirm AI-search tracking method, if available.
- [ ] Confirm conversion path and owner.
- [ ] Confirm content owner and publishing workflow.
- [ ] Confirm dev owner for technical fixes.
- [ ] Confirm whether the site has ecommerce, booking, quote, or checkout flows that agents may need to operate.

## Minimum measurement events

For most commercial sites, track:

- page view;
- CTA click;
- form start;
- form submit;
- signup;
- demo booking;
- purchase / checkout completed;
- GitHub star, package install, docs signup, or download for OSS/docs products;
- AI referral source where detectable.

## Data confidence labels

Use:

- `High`: direct platform data, logs, or verified crawl.
- `Medium`: partial export, sampled data, or inferred from multiple consistent sources.
- `Low`: public-only audit or no direct measurement access.

Never present inferred data as measured data.
