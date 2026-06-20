# 14 — Agentic Commerce Readiness

Use this for ecommerce, marketplaces, booking, local services, lead-gen, and any site where agents may compare, choose, reserve, or buy.

## Readiness layers

| Layer | Requirement | Why it matters |
|---|---|---|
| Product/catalog clarity | Product names, SKUs, variants, prices, availability, images, shipping/return info visible and current | Agents need reliable facts to compare and act |
| Merchant feeds/profiles | Merchant Center, product feeds, Business Profile, Bing Places, marketplaces where relevant | AI/search surfaces often use merchant/local data |
| Structured data | Product, Offer, AggregateRating only when visible/valid, LocalBusiness, FAQ, Breadcrumb, Organization | Helps machine interpretation and rich eligibility |
| Agent-friendly UX | Semantic add-to-cart/book/contact controls, labels, stable flow | Browser agents need executable actions |
| Policy clarity | Returns, cancellations, shipping, privacy, service area, support | Reduces ambiguity and user risk |
| Checkout/booking APIs | Cart, checkout, booking, quote, account linking capabilities when available | Enables future agentic flows |
| Security/review | Fraud, authorization, payment, data privacy, bot/WAF review | Prevents unsafe autonomous transactions |

## Commerce / booking audit

1. Can an agent identify product/service category, price, availability, and constraints from visible HTML?
2. Can it compare variants without opening hidden tabs or PDFs?
3. Can it find shipping, return, cancellation, support, and service-area policies?
4. Can it click the primary action using semantic controls?
5. Does the flow require hover-only interactions or invisible overlays?
6. Is there a public feed/profile source that search/AI systems can trust?
7. Are tracking, conversion events, and consent behavior clear?
8. Are payment/booking APIs and future protocols on the roadmap where relevant?

## Optional protocol watchlist

For advanced merchants, monitor emerging standards and product integrations such as Universal Commerce Protocol, MCP bindings, agent payment protocols, and platform-specific merchant experiences. Treat them as readiness work, not a replacement for product feeds, crawlable pages, and safe checkout UX.
