# v1.2.8 Full Audit Command Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reproducible command that runs the SEO/GEO audit workflow end to end and validates the generated report artifacts.

**Architecture:** Keep existing scripts as focused units. Add `run_full_audit.py` as a thin orchestrator, `validate_audit_report.py` as a deterministic quality gate, and a committed reference example generated from explicit fixture data.

**Tech Stack:** Python standard library, existing Node screenshot helper, existing HTML and AI-layer generators, unittest fixtures, zipfile validation.

---

### Task 1: Failing Tests

**Files:**
- Create: `tests/test_full_audit_workflow.py`
- Create: `tests/test_reference_examples.py`

- [ ] **Step 1: Add run_full_audit test**

Test a local HTTP fixture with `run_full_audit.py --skip-browser --no-serve`. Expect generated `audit.json`, `index.html`, `LATEST-SEO-GEO-REPORT.md`, `owner-data/`, `ard-readiness.json`, `ai-layer-package.zip`, and `report-validation.json`.

- [ ] **Step 2: Add validator failure test**

Create an incomplete report where `ai_layer_current_state` marks `/llms.txt` and `/for-ai` missing but no `ai_layer_package` exists. Expect `validate_audit_report.py` to exit non-zero and mention the package.

- [ ] **Step 3: Add example artifact test**

Assert `examples/reference-audit/audit.json`, `index.html`, `LATEST-SEO-GEO-REPORT.md`, `ai-layer-package.zip`, and listed package files exist, then run `validate_audit_report.py` against the example.

### Task 2: Implement Runtime Scripts

**Files:**
- Create: `scripts/validate_audit_report.py`
- Create: `scripts/run_full_audit.py`

- [ ] **Step 1: Implement report validator**

Load `audit.json`, verify required fields, screenshot/responsive evidence, AI-layer package consistency, ZIP members, and receipt.

- [ ] **Step 2: Implement full audit orchestrator**

Normalize URL, optionally capture browser evidence, generate owner-data request, check ARD, inspect AI-layer endpoints, create conservative `audit.json` when absent, generate package, generate HTML, validate report, and optionally serve.

### Task 3: Wire Runtime Package

**Files:**
- Modify: `manifest.json`
- Modify: `scripts/install.sh`
- Modify: `scripts/skill_doctor.py`
- Modify: `scripts/validate_skill.py`
- Modify: `INSTALL_FOR_AGENTS.md`

- [ ] **Step 1: Bump version**

Set version to `1.2.8` and update install URLs.

- [ ] **Step 2: Include new scripts**

Add `run_full_audit.py` and `validate_audit_report.py` to manifest, installed runtime, doctor, and install smoke tests.

### Task 4: Documentation And Example

**Files:**
- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `runbooks/visual-html-audit.md`
- Modify: `runbooks/cli-audit.md`
- Modify: `runbooks/bootstrap.md`
- Modify: `CHANGELOG.md`
- Modify: `evals/routing-eval.jsonl`
- Create: `examples/reference-audit/`

- [ ] **Step 1: Update docs**

Explain one-command workflow, validation gate, and analysis-plus-improvement positioning.

- [ ] **Step 2: Generate example**

Use fixture data to generate a reference audit directory and validate it.

### Task 5: Verification And Publish

**Files:**
- All changed files

- [ ] **Step 1: Run verification**

Run targeted tests, full test suite, `scripts/validate_skill.py`, Python compile, Node check, `git diff --check`.

- [ ] **Step 2: Commit and push**

Commit, tag `v1.2.8`, push `main` and tag.
