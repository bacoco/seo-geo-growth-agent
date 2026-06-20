# GEO Risk Red-Team Checklist

Use this before publishing major SEO/GEO recommendations, content, schema, robots.txt, or measurement claims.

## Content manipulation risks

| Check | Pass condition |
|---|---|
| No fake stats | Every number has source/date/method or is removed |
| No fake citations | Every cited source exists and supports the claim |
| No fake reviews/ratings | Reviews are visible, real, and policy-compliant |
| No inauthentic mentions | No sockpuppet forum/Reddit/social tactics |
| No scaled thin pages | Each page has unique purpose, useful content, and conversion path |
| No hidden text | Users can see the same meaningful content machines see |
| No cloaking | Bots and users receive substantially the same content |
| No unsupported “best/#1” | Superlatives have criteria, source, and caveat |

## Technical risks

| Check | Pass condition |
|---|---|
| Robots syntax validated | Groups, user agents, sitemap lines, and wildcards are correct |
| Search bots preserved | Googlebot/bingbot not accidentally blocked |
| Desired AI search bots preserved | Search/index bots allowed where visibility is desired |
| Training policy intentional | Training bots allowed/blocked based on owner decision |
| WAF verified | Legitimate bots not blocked by generic anti-AI rules |
| No private content exposure | Sensitive data protected by auth/removal, not robots.txt |
| Sitemap fresh | Important URLs and hreflang/canonical states are current |
| Structured data visible | JSON-LD matches page content |

## Measurement risks

| Check | Pass condition |
|---|---|
| No fake uplift | Predictions are labeled as expected/estimated, not observed |
| Manual prompts labeled | Prompt-panel results are directional, not universal |
| AI referral regex reviewed | Known AI sources included, false positives checked |
| Bot logs verified | User-agent spoofing considered where possible |
| No vendor lock-in claim | Tool coverage limitations are disclosed |

## Safety output

If a tactic fails this checklist, return:

```markdown
I would not ship this as written because [risk].
Safer alternative: [rewrite/fix].
Evidence needed before publishing: [source/log/legal/product review].
```
