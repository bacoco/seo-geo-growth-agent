# Crawler Policy Freshness Check

Use this before publishing robots.txt or WAF advice involving AI crawlers.

## Date Checked

YYYY-MM-DD

## Vendors

| Vendor | Official doc URL | Crawler / fetcher names checked | Changed? | Action |
|---|---|---|---:|---|
| OpenAI |  |  | unknown |  |
| Google |  |  | unknown |  |
| Anthropic |  |  | unknown |  |
| Perplexity |  |  | unknown |  |
| Microsoft/Bing |  |  | unknown |  |

## Rules

- Verify current official docs before naming crawlers.
- Separate search/index crawlers, training crawlers, and user-triggered fetchers.
- Do not treat robots.txt as security.
- Do not block user-triggered fetchers if the owner wants assistants to cite or retrieve public pages.
