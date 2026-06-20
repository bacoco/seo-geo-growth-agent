# Agent-Friendly UX Audit

AI agents increasingly use more than raw HTML. They may inspect screenshots, DOM structure, and the accessibility tree. This module checks whether important user journeys are understandable and executable by machines as well as people.

## When to use

Use this for ecommerce, SaaS signup, booking, comparison, quote request, local service, docs search, and support flows.

## Audit dimensions

| Dimension | Good signal | Common failure | Fix |
|---|---|---|---|
| Semantic controls | Real `<button>`, `<a>`, `<input>`, `<select>` | Clickable `<div>` with JS only | Use semantic HTML or role/tabindex fallback |
| Accessibility names | Buttons and inputs have descriptive labels | “Click here”, icon-only, unlabeled fields | Add visible text, aria-label only when needed, label `for` inputs |
| Stable layout | CTA stays in predictable position | Layout shifts, hover-only controls, carousels hiding actions | Reduce CLS, keep primary action visible |
| Blocking overlays | Essential controls not covered | Popups, cookie banners, transparent overlays | Ensure dismissible, non-blocking, accessible overlays |
| Visible facts | Price, availability, features, limits visible in HTML | Important facts in image, PDF, hidden tab, JS late render | Put facts in crawlable text |
| Step clarity | Checkout/booking steps and states are explicit | Ambiguous states, disabled controls without reason | Add state text, progress labels, validation messages |
| Error handling | Errors are visible and machine-readable | Toast only, color-only error | Use inline text and accessible error associations |
| Authentication boundary | Agent knows what requires login | Silent redirects or modal walls | State login requirements and public alternatives |

## Practical test

1. Identify the primary user task.
2. Walk the task with JavaScript enabled and disabled where possible.
3. Inspect rendered HTML and accessibility tree.
4. Confirm every required action has a semantic role and accessible name.
5. Confirm important facts are visible in text.
6. Confirm the CTA path can be followed without hover-only states.
7. Record blockers as P0 if they prevent purchase/signup/booking/quote.

## Output

Use `templates/agent-readiness-audit.md`.
