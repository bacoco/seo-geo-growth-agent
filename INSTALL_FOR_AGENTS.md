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
rm -rf /tmp/seo-geo-growth-agent-install
git clone --depth 1 --branch v1.1.1 https://github.com/bacoco/seo-geo-growth-agent.git /tmp/seo-geo-growth-agent-install
cd /tmp/seo-geo-growth-agent-install
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
```

It must not contain repository maintenance files such as `.github/`, `.gitignore`, `assets/`, or `scripts/`.

## Step 6: First Use

Read `runbooks/bootstrap.md` from the installed folder and offer the user one of four starting modes:

1. SEO/GEO audit
2. `/for-ai` package
3. content brief
4. crawler and measurement policy

Then tell the user: `seo-geo-growth-agent is installed. Restart the agent session if skills are not auto-refreshed.`
