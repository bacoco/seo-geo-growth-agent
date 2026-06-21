# Changelog

## 1.2.8 — Full audit command and report validation

### Added

- `scripts/run_full_audit.py` orchestrates the repeatable SEO/GEO workflow: evidence capture, owner-data request, ARD readiness, AI-layer endpoint checks, conservative `audit.json`, downloadable improvement files, HTML report, validation, and optional local serving.
- `scripts/validate_audit_report.py` fails incomplete reports before they are shared, including missing required files, missing screenshot status, missing responsive summary, and missing AI-layer package files.
- `examples/reference-audit/` provides a committed reference report with `audit.json`, `index.html`, receipt, validation JSON, AI-layer package folder, and ZIP.

### Changed

- README, SKILL, bootstrap, CLI, and visual audit runbooks now position the repository as analysis plus generated owner-review improvements.
- Runtime install, doctor, manifest, and validation coverage include the full-audit command and report validator.

## 1.2.7 — ARD validation and generated improvement packages

### Added

- `scripts/validate_ard_catalog.py` validates ARD / `ai-catalog.json` manifests for `specVersion`, `urn:air:` identifiers, `url` vs `data`, and representative query bounds.
- `scripts/check_ard_readiness.py` checks live sites for `/.well-known/ai-catalog.json`, `<link rel="ai-catalog">`, and `Agentmap:` in `robots.txt`, then emits an `ard_readiness` JSON block.
- AI-layer packages now include an owner-review `ai-catalog.json` draft when ARD or agentic resources are in scope.
- README now explains why ARD matters, where it fits, and why it is not a ranking factor.

### Changed

- The visual audit workflow now checks ARD before generating downloadable files so `ai-catalog.json` can be included in the ZIP when relevant.
- Runtime install, doctor, manifest, and validation coverage include the ARD checker and validator scripts.

## 1.2.6 — Evidence Engine, Owner Data Mode, CLI, and ARD drafts

### Added

- `scripts/capture_site_screenshots.mjs` can now emit `evidence-engine.json` with Console Watch, Network Watch, Cache/CDN Watch, and measurable first-screen Design Watch facts.
- HTML reports render Evidence Engine and ARD readiness blocks in the Technical tab.
- `scripts/generate_owner_data_request.py` creates owner-data requests for GSC, GA4, Bing Webmaster Tools, server logs, Cloudflare Analytics, and paid-tool consent.
- `scripts/seo_geo_audit.py` creates repeatable audit workspaces and plan-only command receipts.
- `scripts/generate_ard_catalog.py`, `templates/ai-catalog.json`, and `runbooks/ard-ai-catalog.md` add optional ARD / `/.well-known/ai-catalog.json` support for agentic resource discovery.
- AI-layer packages now expose `publication_status` and `status_reason` so drafts are not mistaken for owner-approved publication files.

## 1.2.5 — Receipts, preproduction gates, comparisons, and citation panels

### Added

- HTML report generation now writes `LATEST-SEO-GEO-REPORT.md` so the current valid report is explicit.
- Served reports update the receipt with the active local URL.
- Reports render `environment` and `production_gates[]` for preproduction vs production decisions.
- `scripts/compare_audit_reports.py` generates narrative Markdown and JSON comparisons between two audit runs.
- `scripts/generate_geo_citation_panel.py` creates ready-not-executed ChatGPT/Perplexity/Claude prompt panels.
- `scripts/sync_and_doctor.py` synchronizes Codex/Claude local installs from the source repo and runs doctors.
- Paid-tool consent runbook and approval template for tools that may consume credits.

## 1.2.4 — Lazy-load aware responsive evidence

### Added

- Responsive screenshot capture now records image state before and after scrolling the page.
- `responsive_study.viewports[].metrics.imageLoadStates` distinguishes images loaded initially, loaded after scroll, broken after scroll, and still deferred after scroll.
- HTML reports render lazy-load image counters in the responsive study.
- Post-mortem product patterns runbook captures reusable ideas from field reports, including current-report receipts, preproduction mode, comparison reports, Console Watch, sync-and-doctor, and real GEO/Citation panels.

### Changed

- Image findings now use `missing_after_scroll` instead of treating initially unloaded lazy images as site defects.
- The visual audit runbook explicitly forbids recommending removal of `loading="lazy"` when images load after scroll.

## 1.2.3 — Downloadable AI-layer packages

### Added

- Runtime generator for downloadable AI-layer publication packs when a site is missing `/llms.txt`, `/for-ai`, `/for-ai.json`, `/for-ai.txt`, or aligned JSON-LD.
- HTML report Downloads tab with ZIP and per-file links for generated AI-layer files.
- Skill contract, runbook, install protocol, doctor, validation, and routing eval coverage for AI-layer package generation.

## 1.2.2 — Mandatory visual reports and localized HTML

### Changed

- Domain/URL audits now default to the visual HTML audit workflow unless the user explicitly asks for chat-only output.
- The skill now requires `audit.json`, `index.html`, a report URL or path, Design Watch, analysis cohorts, and site screenshot status for normal site audits.
- Dynamic responsive study now checks at least homepage mobile and desktop rendering, including overflow, title/H1, visible text, image load status, and viewport metadata.
- Generated reports now use tabbed pages with a stronger executive overview, animated readiness signal, and scannable cohort cards.
- HTML report labels now follow `report_language`, so reports can be rendered in the language used by the user.
- Visual audit instructions now require the audit content itself to be written in the user's language.

## 1.2.1 — Design Watch and analysis cohorts

### Added

- Design Watch audit template for scoring first impression from audited-site screenshots.
- Analysis cohorts in HTML reports to separate Search/Crawl, GEO/Citation, Browser Agent, Design Watch, Measurement, and Skillpack quality lenses.
- GStack/GBrain improvement map covering browser-first audits, skill doctors, domain notes, decision logs, codification, visual diffs, source confidence, local analytics, crawler freshness, and Design Watch.
- Installed skill doctor for runtime package verification.
- Skill optimization runbook and extra templates for domain notes, decision logs, browser audit codification, crawler freshness, source confidence, local analytics, and visual diffs.

### Changed

- Visual evidence now means screenshots of the audited site, not screenshots of the generated report.
- HTML report typography and layout are more compact and decision-oriented.
- Visual audit runbook now requires screenshot analysis before report generation.

## 1.2.0 — Visual HTML audit reports

### Added

- Dynamic HTML audit report generator from explicit `audit.json` evidence.
- Readiness scorecards inspired by health-dashboard workflows.
- Public-vs-owner-only measurement access runbook and reusable matrix.
- Local report server with port fallback and browser-open option.
- Chrome/DevTools screenshot fallback for desktop and mobile audited-site evidence when Agent Browser is unavailable.
- Visual HTML audit runbook covering Agent Browser-first screenshot workflow and evidence rules.
- Validation and install smoke tests for runtime report scripts.

### Changed

- Runtime installs now include only the report-generation scripts needed by the installed skill.
- Bootstrap offers visual HTML audit as a first-class starting mode.
- README and install protocol describe browser-readable reports and screenshot evidence.

## 1.1.2 — Agent-safe temporary install path

### Changed

- Replaced the agent install protocol's fixed `/tmp` cleanup command with a `mktemp -d` workspace, so stricter agent harnesses do not reject the setup as destructive.

## 1.1.1 — Agent-first install and skillpack quality fixtures

### Added

- Agent-readable `INSTALL_FOR_AGENTS.md` protocol for pinned installs.
- First-use bootstrap runbook for choosing the initial SEO/GEO workflow.
- Routing eval fixtures for positive and negative trigger cases.

### Changed

- Runtime installs now include the install protocol, runbooks, and eval fixtures.
- README install path now points agents to a versioned raw protocol.
- Validation now checks runbook and routing-eval manifest entries.

## 1.1.0 — Source-led SEO/GEO + agentic readiness update

### Added

- Source-led research policy and source register.
- AI crawler policy matrix and selective robots.txt template.
- Plain-English guide to the Ethan Mollick GEO pattern for AI agents and institutional articles.
- Reusable `/for-ai`, `/for-ai.json`, and agent interpretation test templates.
- Simple `scripts/install.sh` installer for Codex, Claude Code, and custom skill directories.
- Agent-friendly UX audit for DOM, accessibility tree, semantic controls, labels, and stable layout.
- Google Search Console generative AI report template.
- Bing AI Performance report template.
- Query fan-out and grounding-query maps.
- Claim ledger for citation-worthy content.
- Server-log AI bot audit template.
- Earned-media/entity map.
- Agentic commerce checklist.
- GEO red-team checklist.
- Optional `llms-full.txt` template.

### Changed

- Updated `SKILL.md` with evidence tiers, anti-hype rules, crawler-type distinctions, AI measurement v2, and agentic actionability.
- Fixed README/SKILL file tree references from v1 placeholder names to the actual numbered reference files.
- Extended priority algorithm with `Agent Actionability` and `Spam/Risk` factors.
- Hardened validation to catch broken internal references, invalid JSON templates, mismatched reference numbers, and installer regressions.
- Hardened `scripts/install.sh` to refuse ambiguous custom destinations and preserve previous installs as timestamped backups.
- Aligned late reference headings with their actual file numbers.

### Guardrails strengthened

- No unsupported claims, fake stats, fake citations, fake review/rating schema, or inauthentic mentions.
- `llms.txt` remains optional and must not be represented as a Google ranking or AI Overview requirement.
- Robots.txt is treated as a crawler traffic-management signal, not a privacy/security mechanism.
