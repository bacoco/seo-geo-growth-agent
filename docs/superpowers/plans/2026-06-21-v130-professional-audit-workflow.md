# v1.3.0 Professional Audit Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the skill from an audit toolkit into a professional, demonstrable audit-and-improvement package with a stable demo, stronger owner-data intake, and release-ready documentation.

**Architecture:** Keep the existing script-first architecture. Add one small demo/doctor script, strengthen owner-data outputs, promote the reference example into a real golden audit, and wire everything through manifest/install/validation.

**Tech Stack:** Python standard library, existing Markdown/JSON templates, existing shell installer, Git/GitHub release flow.

---

### Task 1: Golden Audit Uses Real Repository Evidence

**Files:**
- Modify: `examples/reference-audit/audit.json`
- Regenerate: `examples/reference-audit/index.html`
- Regenerate: `examples/reference-audit/LATEST-SEO-GEO-REPORT.md`
- Regenerate: `examples/reference-audit/report-validation.json`
- Test: `tests/test_reference_examples.py`

- [ ] Replace fictional `example.test` fields with `https://github.com/bacoco/seo-geo-growth-agent` and repo-specific facts.
- [ ] Keep all unknown visit/search/conversion metrics marked unknown or absent.
- [ ] Regenerate HTML and validation artifacts.
- [ ] Extend the reference example test to assert the golden audit is tied to the real repo.

### Task 2: Demo Command

**Files:**
- Create: `scripts/skill_demo.py`
- Modify: `manifest.json`
- Modify: `scripts/install.sh`
- Modify: `scripts/skill_doctor.py`
- Modify: `scripts/validate_skill.py`
- Test: `tests/test_professional_workflow.py`

- [ ] Add a CLI that validates the committed golden audit, runs `skill_doctor.py` when an install dir is supplied, writes `demo-result.json`, and can optionally serve the report.
- [ ] Keep default mode non-network and non-serving so CI is deterministic.
- [ ] Install the script in runtime packages.
- [ ] Validate the script appears in manifest and installed skill doctors.

### Task 3: Owner Data Intake Pack

**Files:**
- Modify: `scripts/generate_owner_data_request.py`
- Modify: `runbooks/owner-data-mode.md`
- Create: `templates/owner-data-intake.csv`
- Test: `tests/test_professional_workflow.py`

- [ ] Generate `owner-data-intake.csv` alongside Markdown and JSON.
- [ ] Include source, owner, export path, date range, property, status, and notes columns.
- [ ] Document that these are owner-provided exports, not public scraping or bypasses.

### Task 4: Release Positioning

**Files:**
- Modify: `README.md`
- Modify: `INSTALL_FOR_AGENTS.md`
- Modify: `SKILL.md`
- Modify: `runbooks/bootstrap.md`
- Modify: `CHANGELOG.md`
- Modify: `manifest.json`
- Test: existing validation suite.

- [ ] Bump version to `1.3.0`.
- [ ] Reposition the repo as “audit plus owner-reviewed improvement package.”
- [ ] Add one-line install prompt and one-line demo prompt.
- [ ] Add changelog entry.

### Task 5: Verification And Publication

**Files:**
- All changed files.

- [ ] Run targeted tests.
- [ ] Run full test suite and repository validator.
- [ ] Commit, tag `v1.3.0`, push `main` and the tag.
- [ ] Create a GitHub release for `v1.3.0` if GitHub CLI auth is available.
