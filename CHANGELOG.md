# Changelog

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
