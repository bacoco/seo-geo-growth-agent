# Public Measurement Access Runbook

Use this runbook when the user asks what traffic, SEO, GEO, AI visibility, or analytics data can be retrieved without owning the site, and what becomes available after ownership is verified.

## Rule

Do not invent visits, rankings, citations, conversions, or audience numbers. Public tools can expose crawl, performance, index, and estimate signals; first-party tools expose real site data only after verification or tracking installation.

## Public Without Site Ownership

| Source | Publicly accessible? | Gives | Does not give |
|---|---:|---|---|
| Site HTTP/HTML | Yes | status codes, redirects, headers, canonical, metadata, headings, schema, visible content | visits, conversions, Google impressions |
| `robots.txt` and sitemaps | Yes | crawl policy, sitemap URLs, lastmod hints | whether Google indexed or ranked each URL |
| Chrome UX Report / PageSpeed field data | Sometimes | aggregated Core Web Vitals for sufficiently visited origins/URLs | visit counts, queries, conversions |
| Lighthouse/PageSpeed lab data | Yes | lab performance, accessibility, SEO checks | real traffic |
| Bing/Google search operators | Partial | rough index presence and snippets | complete index coverage, clicks, impressions |
| Third-party SEO tools | Usually estimated | estimated organic traffic, backlinks, keywords | exact analytics |
| Server technology fingerprints | Yes | CMS, CDN, security headers, visible scripts | private logs |

## Requires Site Ownership Or Access

| Source | Access needed | Gives |
|---|---|---|
| Google Search Console | verified property | queries, impressions, clicks, CTR, average position, index and Core Web Vitals reports |
| GA4 | property access or tracking installed | sessions, users, events, conversions, source/medium, landing pages |
| Bing Webmaster Tools | verified property | Bing search performance, index signals, AI-related reports where available |
| Server/CDN logs | server or CDN owner access | bot hits, status codes, referrers, crawl patterns, AI crawler access |
| Microsoft Clarity | script installed or project access | heatmaps, session recordings, user behavior, AI visibility features where available |
| Cloudflare Web Analytics | zone access or beacon installed | pageviews, visits, referrers, countries, Web Vitals-style signals |
| Self-host analytics | installed script/server access | first-party pageviews, events, referrers, goals |

## Owner Setup

For a site the user owns, recommend this minimum stack:

1. Verify Google Search Console domain property.
2. Install GA4 or a privacy-first alternative such as Cloudflare Web Analytics, Umami, Matomo, or Plausible.
3. Add Microsoft Clarity if heatmaps/session replay are useful and privacy policy allows it.
4. Keep server/CDN logs for at least 30 days.
5. Add AI referrer detection in GA4 and server logs.
6. Export a weekly `measurement-access-matrix.csv` so audits can label every metric as public, owner-only, estimated, or unknown.

## Cloudflare

Do not bypass Cloudflare or anti-bot controls on third-party sites.

If the user owns the site, use legitimate access instead:

- create a temporary WAF allow rule for the audit agent IP;
- use Cloudflare API tokens to read analytics/logs;
- enable Cloudflare Web Analytics;
- use Cloudflare Access service tokens for protected staging pages;
- run the audit from an allowed network;
- create a temporary staging hostname with equivalent content and controlled access.
