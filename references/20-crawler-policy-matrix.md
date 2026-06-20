# 12 — Crawler Policy Matrix

## Principle

Do not write one blanket “AI bots” rule unless the owner explicitly wants that. Separate:

1. **Search/indexing crawlers** — used to discover or cite content in AI-search answers.
2. **Training crawlers** — used to improve foundation models or AI products.
3. **User-triggered agents/fetchers** — used when a user asks an assistant to visit or retrieve a page.
4. **Traditional search crawlers** — Googlebot/Bingbot-style crawlers for web search.

## Common crawler/control categories

| Vendor | Name/control | Type | Typical owner question |
|---|---|---|---|
| OpenAI | `OAI-SearchBot` | AI search/discovery | Should ChatGPT Search be able to cite us? |
| OpenAI | `GPTBot` | Training | Do we allow content for model training? |
| OpenAI | `ChatGPT-User` | User-triggered agent | Should user requests in ChatGPT be able to fetch our pages? |
| Perplexity | `PerplexityBot` | AI search/discovery | Should Perplexity answer search cite us? |
| Perplexity | `Perplexity-User` | User-triggered agent | Should user-directed Perplexity fetches access our pages? |
| Anthropic | `ClaudeBot` | Training | Do we allow future content for model training? |
| Anthropic | `Claude-SearchBot` | AI search quality/discovery | Should Claude search experiences index us? |
| Anthropic | `Claude-User` | User-triggered agent | Should user-directed Claude queries fetch us? |
| Google | `Googlebot` | Search crawler | Should pages be eligible for Google Search? |
| Google | `Google-Extended` | AI model/product improvement control | Should Google use content for certain AI improvement contexts? |
| Bing/Microsoft | `bingbot` / related Bing crawlers | Search and Microsoft discovery surfaces | Should Bing/Copilot surfaces discover us? |

## Default commercial policy pattern

For most commercial SaaS/ecommerce/local sites that want AI-search visibility but are cautious about model training:

```txt
User-agent: *
Allow: /

# Allow AI search/discovery and user-triggered fetches where desired
User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

# Optional: restrict model-training crawlers if owner/legal chooses
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

Sitemap: https://[DOMAIN]/sitemap.xml
```

This is a starting pattern, not a universal recommendation. Publishers, legal databases, paywalled content, research sites, and privacy-sensitive sites may choose a different policy.

## Verification checklist

- [ ] Confirm owner policy: allow AI search, block training, allow user-triggered agents, block all, or mixed.
- [ ] Verify current vendor docs for each crawler name.
- [ ] Check whether vendor provides IP ranges, reverse DNS verification, or WAF instructions.
- [ ] Confirm robots.txt is accessible at root and per subdomain.
- [ ] Test important URLs with desired crawler user agents only for diagnostics; do not rely on spoofed UA as proof.
- [ ] Ensure sitemap includes canonical, indexable, 200-status URLs.
- [ ] Confirm WAF/CDN does not block desired verified crawlers.
- [ ] Re-check quarterly.

## Policy output language

Use clear tradeoff language:

- “Allowing this search crawler may improve eligibility for citation/discovery, but it does not guarantee inclusion.”
- “Blocking this training crawler signals that future content should not be used for model training, but it is not the same as removing the page from search.”
- “Blocking user-triggered fetchers may reduce visibility when a user asks an assistant to retrieve or summarize the page.”
- “robots.txt is not an authentication system; use official IP/rDNS verification for WAF/security decisions.”
