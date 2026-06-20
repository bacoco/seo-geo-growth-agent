# AI Crawler Policy

Use this reference to draft robots.txt, WAF, and crawler-access recommendations. Always verify current vendor docs before production deployment.

## Crawler categories

| Category | Purpose | Policy question |
|---|---|---|
| Search/index crawler | Crawls or indexes content for AI/search answers and citations | Do we want visibility in that answer engine? |
| Training crawler | Collects content for model training or improvement | Do we allow training use? |
| User-triggered fetcher | Retrieves a page because a user requested it in a chat/agent session | Should users be able to ask the assistant to access our content? |
| Ads/validation crawler | Validates landing pages or product/ads experiences | Do ads or merchant experiences require access? |
| Unknown/spoofed crawler | Claims a bot identity but may not be verified | Should WAF/log rules verify IP/user-agent alignment? |

## Policy design pattern

1. Start from the business objective: visibility, content protection, bandwidth control, privacy, or compliance.
2. Decide separately for each crawler category.
3. Use official user-agent tokens only.
4. Use WAF/IP verification only from vendor-published IP ranges when available.
5. Keep a rollback plan.
6. Monitor logs for 7–14 days after deployment.
7. Review quarterly because crawler names and product use cases change.

## Selective allow/block example

This is a policy pattern, not a universal recommendation.

```txt
# Allow search/index surfaces where visibility is desired.
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

# Block or allow training crawlers based on owner policy.
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

# Google-Extended is a control token for some Google AI uses, not normal Search crawling.
User-agent: Google-Extended
Disallow: /

# Keep standard search crawl open unless the owner has a clear reason.
User-agent: Googlebot
Allow: /

User-agent: bingbot
Allow: /

Sitemap: https://[DOMAIN]/sitemap.xml
```

## Important cautions

- Robots.txt is not security and cannot protect private content.
- Some user-triggered fetchers are different from crawlers; do not assume robots.txt behavior is identical.
- A disallowed URL can sometimes still appear as a URL-only search result if other pages link to it.
- Do not place `Sitemap:` lines between user-agent groups in a way that confuses parser grouping.
- Avoid `crawl-delay` unless a specific crawler documents support for it.
- WAF rules should avoid blocking legitimate search bots because of generic “AI bot” labels.

## Log checks

Track:

- user-agent;
- resolved IP / ASN if available;
- vendor-published IP match;
- requested path;
- status code;
- robots.txt fetch before content fetch;
- crawl rate;
- bandwidth;
- conversion/AI referral impact after changes.

Use `templates/ai-crawler-policy-matrix.csv` and `templates/server-log-ai-bot-audit.md`.
