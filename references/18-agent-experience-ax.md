# 10 — Agent Experience / Agentic Website Readiness

## Goal

Make the website usable not only for humans and crawlers, but also for browser agents and AI assistants that navigate pages through screenshots, HTML, DOM, accessibility trees, and sometimes APIs.

## Agent-critical journeys

Identify the journeys that matter commercially:

| Business model | Critical agent journeys |
|---|---|
| SaaS | find pricing, compare plans, understand feature limits, start trial, book demo, read docs, fetch security page |
| Ecommerce | find product, compare specs, check price/availability, add to cart, shipping/returns, support |
| Local | find service area, hours, address, phone, pricing note, book appointment, request quote |
| Publisher | find article, cite source, check author/date, subscribe, navigate related coverage |
| Open source | find install docs, license, examples, changelog, GitHub repo, API reference |

## Agent-friendly page checklist

| Check | Why it matters | Good state |
|---|---|---|
| Semantic buttons and links | Agents infer actionability from DOM and accessibility tree | Use `<button>` for actions and `<a href>` for navigation |
| Labels attached to inputs | Agents need to know what a field means | Use `<label for>` and clear accessible names |
| Stable layout | Screenshot-based agents get confused by shifting controls | Avoid layout shift on key journeys |
| Visible actions | Agents may ignore covered/transparent/hidden elements | Avoid ghost overlays and hidden click targets |
| Clear product containers | Agents map product facts to the correct CTA | Keep product title, price, specs, availability, and CTA in the same semantic container |
| Machine-readable facts | AI answer engines and agents need extractable truth | Use tables, lists, schema, canonical docs, feeds, and stable URLs |
| Auth/CAPTCHA/WAF clarity | Agents can stall at unexplained barriers | Provide human fallback and avoid blocking verified desired crawlers |
| Error messages | Agents need recoverable state | Use specific validation messages and visible next steps |
| Destructive actions | Agents must avoid unsafe actions | Label destructive buttons clearly and require confirmation |

## Accessibility tree audit

For key templates, inspect:

- page title;
- H1/H2 hierarchy;
- landmark roles;
- link text;
- button names;
- input labels;
- table headers;
- product cards;
- modals;
- popups;
- cookie banners;
- checkout/demo forms.

## Optional API / agent interface

For sites where agents need to complete tasks, consider exposing stable documentation or APIs:

| Need | Possible interface |
|---|---|
| Product catalog lookup | Product feed, structured data, API docs |
| Pricing/plan comparison | Pricing table, schema, stable `/pricing`, JSON endpoint if appropriate |
| Docs retrieval | Markdown docs, `llms.txt`, `llms-full.txt`, OpenAPI docs |
| Search | Site search endpoint, sitemap, docs index |
| Booking/demo | Accessible form, clear calendar flow, API only if safe |
| Commerce/cart | Standard checkout, product feeds, emerging commerce protocols only after legal/security review |

## AX audit output

Use `templates/agent-experience-audit.md`.

Prioritize fixes that improve both accessibility and AI-agent clarity. Most agent-friendly improvements are also user-friendly and SEO-friendly: semantic HTML, clear copy, stable URLs, structured content, and accessible forms.
