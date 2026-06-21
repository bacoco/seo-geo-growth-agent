# SEO + GEO Growth Agent Installation Guide for AI Agents

Read this entire file before running commands. Install only the runtime skill package, then verify it.

## Step 1: Choose The Target Host

Use one of these targets:

| Host | Command target | Installs to |
|---|---|---|
| Codex | `codex` | `${CODEX_HOME:-$HOME/.codex}/skills/seo-geo-growth-agent` |
| Claude Code | `claude` | `$HOME/.claude/skills/seo-geo-growth-agent` |
| Custom | `/absolute/path/to/skills/seo-geo-growth-agent` | That exact folder |

If both Codex and Claude Code are present and the user did not specify a host, ask which one to install.

## Step 2: Clone The Stable Release

```bash
INSTALL_TMP="$(mktemp -d)"
git clone --depth 1 --branch v1.3.1 https://github.com/bacoco/seo-geo-growth-agent.git "$INSTALL_TMP/seo-geo-growth-agent"
cd "$INSTALL_TMP/seo-geo-growth-agent"
```

If the tag is unavailable, stop and tell the user. Do not silently install from an unpinned branch unless the user explicitly approves it.

## Step 3: Validate Before Installing

```bash
python3 -m py_compile scripts/validate_skill.py
bash -n scripts/install.sh
python3 scripts/validate_skill.py
```

If validation fails, stop and report the failing command and output.

## Step 4: Install

For Codex:

```bash
./scripts/install.sh codex
```

For Claude Code:

```bash
./scripts/install.sh claude
```

For a custom destination:

```bash
./scripts/install.sh /absolute/path/to/skills/seo-geo-growth-agent
```

Custom destinations must end with `seo-geo-growth-agent`. The installer refuses ambiguous destinations and moves any previous install to a timestamped backup.

## Step 5: Verify The Installed Package

Check that the installed folder contains:

```text
SKILL.md
INSTALL_FOR_AGENTS.md
manifest.json
LICENSE
references/
templates/
runbooks/
evals/
examples/reference-audit/
scripts/generate_html_audit_report.py
scripts/run_full_audit.py
scripts/validate_audit_report.py
scripts/generate_ai_layer_package.py
scripts/generate_owner_data_request.py
scripts/generate_ard_catalog.py
scripts/validate_ard_catalog.py
scripts/check_ard_readiness.py
scripts/compare_audit_reports.py
scripts/generate_geo_citation_panel.py
scripts/seo_geo_audit.py
scripts/serve_report.py
scripts/capture_site_screenshots.mjs
scripts/skill_demo.py
scripts/skill_doctor.py
```

It must not contain repository maintenance files such as `.github/`, `.gitignore`, `assets/`, `scripts/install.sh`, or `scripts/validate_skill.py`.

## Step 6: First Use

Read `runbooks/bootstrap.md` from the installed folder and offer the user the relevant starting mode:

1. SEO/GEO audit
2. full audit command
3. demo/doctor check
4. visual HTML audit
5. `/for-ai` package
6. content brief
7. crawler and measurement policy
8. ARD / ai-catalog validation when the site exposes agentic resources

Then tell the user: `seo-geo-growth-agent is installed. Restart the agent session if skills are not auto-refreshed.`

Optional post-install doctor:

```bash
python3 /path/to/skills/seo-geo-growth-agent/scripts/skill_doctor.py /path/to/skills/seo-geo-growth-agent
```

Optional deterministic demo:

```bash
python3 /path/to/skills/seo-geo-growth-agent/scripts/skill_demo.py --output-dir /tmp/seo-geo-growth-agent-demo --no-serve
```
