# Post-Mortem Product Patterns

Use this runbook after a real SEO/GEO audit session exposes workflow friction, false positives, or product ideas that should become reusable skill behavior.

## Product References To Keep

| Reference | Keep As | Useful Pattern | Guardrail |
|---|---|---|---|
| KateSEO / KateRadar-style workflows | Competitive product reference | Real citation and visibility checks require querying answer engines or dedicated tools, not only checking structure. | Do not claim measured AI citations unless a real panel was executed. |
| Haloscan-style domain visibility | SEO data reference | Domain-level keyword, traffic, page, and competitor views are useful when direct HTML access is blocked. | Ask before consuming paid or credit-based MCP/API tools. |
| Swing Digital field reports | Regression scenario | Lazy-load screenshots can create false positives if images are measured before scroll. | Fix the audit protocol before recommending site changes. |
| Served HTML reports | UX reference | A report must make the current valid artifact obvious: URL, path, date, target, version, and tunnel status. | Do not leave multiple local URLs without a current-report receipt. |

## Ideas Worth Implementing

| Priority | Idea | Status | Why It Matters | Minimum Useful Output |
|---:|---|---|---|---|
| 10 | Current report receipt | Implemented v1.2.5 | Users lose time finding the valid report when ports, folders, or tunnels change. | `LATEST-SEO-GEO-REPORT.md` with HTML path, local URL, remote URL if any, target, date, skill version. |
| 9 | Preproduction mode | Implemented v1.2.5 | Low measurement scores can be correct when analytics, GSC, Bing, and final domain are intentionally deferred. | `environment: preprod|production` plus `next_now`, `defer_until_prod`, `proof_needed`. |
| 9 | Report comparison | Implemented v1.2.5 | Iterating audits requires explaining what changed and why, not only showing two score tables. | Narrative diff plus score deltas between two `audit.json` files. |
| 8 | Console Watch | Backlog | Browser console noise mixes first-party issues, third-party iframes, CDN messages, and browser policy warnings. | Classified console messages: `first_party`, `third_party`, `browser_policy`, `unknown`. |
| 8 | Cache/CDN diagnostics | Backlog | CDN cache can make public evidence differ from local state. | Tested URL, cache headers, asset version, stale/public/local verdict. |
| 8 | Sync and doctor | Implemented v1.2.5 | Source, Codex, and Claude skill copies can drift. | Install to known destinations, run `skill_doctor.py`, print version receipt. |
| 8 | GEO/Citation panel template | Implemented v1.2.5 | Structural readiness is not citation measurement. | CSV with prompts, engines, cited sources, competitors, facts reused, errors, and date. |
| 7 | Paid-tool consent | Implemented v1.2.5 | MCP tools can consume credits. | Require explicit consent before Haloscan, Semrush, DataForSEO, or similar paid calls. |
| 7 | Design Watch measurable first screen | Backlog | A visual score is more useful when tied to viewport facts. | Hero height, CTA visible, trust signal visible, next section visible, tested viewport. |
| 7 | AI-layer package status | Backlog | Downloadable files need owner review when a site already has custom AI files. | `publish_as_is`, `adapt_before_publish`, `already_present`, or `conflict_with_existing_source`. |

## Rules From Field Evidence

- Lazy-load: use the after-scroll state for findings. `loaded_after_scroll > 0` with `broken = 0` and `still_deferred = 0` is positive evidence, not a site defect.
- Preproduction: mark owner-only metrics as production gates when intentionally unavailable. Do not score them as immediate preproduction fixes.
- GEO measurement: structure checks prove readiness only. Real AI citations remain `unknown` until a prompt panel or answer-engine measurement is executed.
- Paid tools: if a tool may spend credits, ask first and record the user approval in the audit notes.
- Current report: every served report should have a stable receipt so the user knows which artifact is valid.
