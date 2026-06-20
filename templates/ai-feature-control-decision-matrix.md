# AI Feature Control Decision Matrix — [DOMAIN]

Date: YYYY-MM-DD
Owner policy: allow AI search / block training / block all AI / mixed / unsure

## Decision table

| Surface/vendor | Control | Type | Current setting | Recommended setting | Tradeoff | Owner approval |
|---|---|---|---|---|---|---|
| Google Search | crawl/index/snippet eligibility | search eligibility | | | Needed for normal Search and many Google AI features | |
| Google generative AI features | GSC Search generative AI control, where available | AI feature inclusion | | | Excluding may reduce AI feature visibility but should not be used as ranking tactic | |
| Google snippets/AI previews | `nosnippet`, `max-snippet`, `data-nosnippet` | preview/content-use limit | | | Can reduce snippets and AI preview eligibility | |
| Google AI product improvement | `Google-Extended` | training/product improvement control | | | Separate from Google Search indexing | |
| OpenAI ChatGPT Search | `OAI-SearchBot` | AI search/discovery | | | Allow may help eligibility for ChatGPT Search citations | |
| OpenAI model training | `GPTBot` | training | | | Owner/legal choice | |
| OpenAI user fetches | `ChatGPT-User` | user-triggered agent | | | Blocking may affect user-requested access | |
| Perplexity search | `PerplexityBot` | AI search/discovery | | | Allow may help Perplexity citation eligibility | |
| Perplexity user fetches | `Perplexity-User` | user-triggered agent | | | Blocking may affect user-requested access | |
| Anthropic training | `ClaudeBot` | training | | | Owner/legal choice | |
| Anthropic search quality | `Claude-SearchBot` | AI search/discovery | | | Blocking may reduce Claude search visibility/accuracy | |
| Anthropic user fetches | `Claude-User` | user-triggered agent | | | Blocking may reduce user-directed web search visibility | |
| Bing/Microsoft | Bing Webmaster / Bingbot / IndexNow | search + AI discovery | | | Bing/Copilot visibility and freshness | |

## Required notes

- Do not deploy until crawler names and vendor docs are verified.
- For WAF/CDN allowlists, verify official IP/rDNS where available.
- Revisit after major legal/publisher policy changes.
- Record the reason for each training-crawler decision.
