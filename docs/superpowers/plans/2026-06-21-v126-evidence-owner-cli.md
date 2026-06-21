# v1.2.6 Evidence Owner CLI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an evidence-first audit layer that captures console/network/CDN evidence, supports owner-data collection, and exposes a simple CLI wrapper.

**Architecture:** Keep deterministic tooling in small scripts and let the skill instructions orchestrate them. Extend the existing HTML report to render optional evidence panels from `audit.json` without making live network calls during report generation.

**Tech Stack:** Python standard library, Node Chrome DevTools fallback, existing `audit.json` schema, shell installer.

---

### Task 1: Evidence Engine Tests

**Files:**
- Modify: `tests/test_site_capture.py`
- Create: `tests/test_cli_owner_and_evidence.py`

- [ ] Add failing tests that require `capture_site_screenshots.mjs` to emit `evidence-engine.json` with `console_watch`, `network_watch`, `cache_cdn_watch`, and `design_watch_metrics`.
- [ ] Add failing tests that require `scripts/generate_owner_data_request.py` to write an owner-data request markdown and JSON checklist.
- [ ] Add failing tests that require `scripts/seo_geo_audit.py --plan-only` to create a runnable audit workspace plan without browsing.

### Task 2: Evidence Engine Implementation

**Files:**
- Modify: `scripts/capture_site_screenshots.mjs`
- Modify: `scripts/generate_html_audit_report.py`
- Modify: `scripts/install.sh`
- Modify: `scripts/skill_doctor.py`
- Modify: `scripts/validate_skill.py`

- [ ] Add Chrome DevTools console, network, response header, and first-screen metric capture.
- [ ] Render the evidence engine in the technical tab of the HTML report.
- [ ] Include the new runtime scripts in install and doctor checks.

### Task 3: Owner Data Mode and CLI

**Files:**
- Create: `scripts/generate_owner_data_request.py`
- Create: `scripts/seo_geo_audit.py`
- Create: `runbooks/evidence-engine.md`
- Create: `runbooks/owner-data-mode.md`
- Create: `runbooks/cli-audit.md`
- Create: `templates/owner-data-request.md`

- [ ] Generate a clear owner-data collection request covering GSC, GA4, Bing Webmaster Tools, server logs, Cloudflare Analytics, and paid-tool consent boundaries.
- [ ] Add a simple CLI that creates a workspace, writes `audit-plan.json`, optionally runs browser capture, and prints next commands.
- [ ] Document when to use public evidence versus owner data.

### Task 4: Skill Metadata and Verification

**Files:**
- Modify: `manifest.json`
- Modify: `SKILL.md`
- Modify: `README.md`
- Modify: `INSTALL_FOR_AGENTS.md`
- Modify: `CHANGELOG.md`
- Modify: `evals/routing-eval.jsonl`

- [ ] Bump to `1.2.6`.
- [ ] Add routing triggers for Evidence Engine, Console Watch, Cache/CDN Watch, Owner Data Mode, and `seo-geo-audit`.
- [ ] Run tests, validation, syntax checks, commit, tag, and push.
