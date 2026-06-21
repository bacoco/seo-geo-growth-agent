# v1.2.7 ARD Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make ARD a verified, documented, and downloadable part of the SEO/GEO skill when a site exposes or should expose agentic resources.

**Architecture:** Add deterministic ARD validation and site-readiness scripts, wire them into the runtime manifest/install flow, and extend the existing AI-layer package generator so missing files become downloadable owner-review drafts. Documentation explains ARD as optional discovery infrastructure, not a ranking factor.

**Tech Stack:** Python standard library scripts and tests, existing Markdown runbooks, JSON/JSONL manifests, shell installer.

---

### Task 1: Lock The Behavior With Tests

**Files:**
- Create: `tests/test_ard_hardening.py`
- Modify: `tests/test_ai_layer_package.py`

- [ ] **Step 1: Add failing ARD script and README tests**

Create tests that expect `scripts/validate_ard_catalog.py` and `scripts/check_ard_readiness.py` to exist, validate a generated catalog, reject invalid catalog variants, inspect a local fixture site for `/.well-known/ai-catalog.json`, `<link rel="ai-catalog">`, and `Agentmap:`, and require a README section titled `Why ARD Matters`.

- [ ] **Step 2: Add failing package test**

Extend the AI-layer package fixture with `ard_readiness.entries[]` and expect `ai-layer-package/ai-catalog.json` inside the generated folder, ZIP, audit metadata, and package manifest.

- [ ] **Step 3: Run RED tests**

Run:

```bash
python3 tests/test_ard_hardening.py
python3 tests/test_ai_layer_package.py
```

Expected: failures caused by missing ARD checker/validator scripts and missing `ai-catalog.json` package output.

### Task 2: Implement ARD Validation And Site Readiness

**Files:**
- Create: `scripts/validate_ard_catalog.py`
- Create: `scripts/check_ard_readiness.py`

- [ ] **Step 1: Implement local/URL catalog validation**

`validate_ard_catalog.py` must load a local path or URL, require root object shape, `specVersion: "1.0"`, non-empty `entries[]`, `urn:air:` identifiers, exactly one of `url` or `data`, and 2-5 `representativeQueries` when present.

- [ ] **Step 2: Implement live readiness checks**

`check_ard_readiness.py` must fetch the target origin, inspect well-known, homepage link, and robots `Agentmap`, validate the discovered catalog, and write a JSON result usable in `audit.json.ard_readiness`.

- [ ] **Step 3: Run GREEN ARD tests**

Run:

```bash
python3 tests/test_ard_hardening.py
```

Expected: pass.

### Task 3: Include ARD In Downloadable Missing-File Packages

**Files:**
- Modify: `scripts/generate_ai_layer_package.py`
- Modify: `tests/test_ai_layer_package.py`

- [ ] **Step 1: Add ARD package payload generation**

When `audit.ard_readiness.entries[]`, `audit.agentic_resources`, or `audit.include_ard_catalog` is present, write `ai-layer-package/ai-catalog.json` using explicit audit entries or a conservative generated draft.

- [ ] **Step 2: Update install guide and manifest output**

The package manifest and returned `ai_layer_package.files[]` must list `ai-catalog.json`; `AI_LAYER_INSTALL.md` must explain publishing it at `/.well-known/ai-catalog.json` only when the owner confirms the resource metadata.

- [ ] **Step 3: Run package tests**

Run:

```bash
python3 tests/test_ai_layer_package.py
```

Expected: pass.

### Task 4: Update Skill Contract, Runtime Packaging, And Docs

**Files:**
- Modify: `README.md`
- Modify: `SKILL.md`
- Modify: `INSTALL_FOR_AGENTS.md`
- Modify: `CHANGELOG.md`
- Modify: `manifest.json`
- Modify: `scripts/install.sh`
- Modify: `scripts/skill_doctor.py`
- Modify: `scripts/validate_skill.py`
- Modify: `runbooks/ard-ai-catalog.md`
- Modify: `runbooks/visual-html-audit.md`
- Modify: `runbooks/cli-audit.md`
- Modify: `evals/routing-eval.jsonl`

- [ ] **Step 1: Version and runtime wiring**

Bump to `1.2.7`, include the two new scripts in manifest/install/doctor/validator paths, and update install URLs to tag `v1.2.7`.

- [ ] **Step 2: Explain ARD clearly**

Add a README section `Why ARD Matters` covering discoverability of skills, MCP/A2A/callable services, honest `representativeQueries`, trust/provenance, and the guardrail that ARD is not a ranking factor.

- [ ] **Step 3: Update runbooks and routing evals**

Document `validate_ard_catalog.py`, `check_ard_readiness.py`, AI-layer package generation with optional ARD files, and routing examples for validating/checking ARD.

### Task 5: Verify, Commit, Tag, Push

**Files:**
- All changed files

- [ ] **Step 1: Run full validation**

Run:

```bash
python3 tests/test_ard_hardening.py
python3 tests/test_ai_layer_package.py
python3 tests/test_cli_owner_and_evidence.py
python3 tests/test_visual_html_audit.py
python3 tests/test_report_receipt_compare_and_panels.py
python3 tests/test_skill_doctor.py
python3 scripts/validate_skill.py
python3 -m py_compile scripts/*.py
node --check scripts/capture_site_screenshots.mjs
git diff --check
```

Expected: all pass.

- [ ] **Step 2: Publish**

Run:

```bash
git add -A
git commit -m "Harden ARD catalog workflows"
git tag v1.2.7
git push origin main
git push origin v1.2.7
```

Expected: remote `main` and tag `v1.2.7` point to the new commit.
