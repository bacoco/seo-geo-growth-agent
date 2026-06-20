# Changelog

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
