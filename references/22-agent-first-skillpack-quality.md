# 22 — Agent-First Skillpack Quality

This repository is a skill package, not an app. Treat the package itself as a product.

## Transferable patterns

These patterns are adapted as original guidance after reviewing Garry Tan's `gstack` and `gbrain` repositories.

| Pattern | Why it matters here | Local implementation |
|---|---|---|
| Agent-first install | The fastest user path is a sentence pasted into Codex or Claude Code, not a developer README | `INSTALL_FOR_AGENTS.md` and README raw URL |
| Pinned install | Installing from a moving branch makes adoption hard to reproduce | versioned Git tags such as `v1.1.2` |
| Bootstrap runbook | After installation, the agent needs a first useful action, not a file list | `runbooks/bootstrap.md` |
| Routing evals | A skill should prove which requests trigger it and which do not | `evals/routing-eval.jsonl` |
| Thin harness, fat skill | Deterministic code should validate and install; judgment belongs in the skill and references | `scripts/validate_skill.py`, `scripts/install.sh`, `SKILL.md`, `references/` |
| No hidden executor | Post-install content should be displayed or read by the agent, not auto-run as untrusted logic | runbooks are instructions, not executable hooks |

## Quality bar

Before tagging a release, the package should satisfy:

1. The agent install protocol is versioned and fetchable by raw URL.
2. The runtime install contains only files the skill needs.
3. The manifest points to real files.
4. Internal references resolve.
5. JSON and JSONL fixtures parse.
6. Routing evals include positive and negative examples.
7. Reinstalling preserves the previous install as a backup.
8. The first-use runbook can get a user from install to first useful output in one question.

## Non-goals

Do not turn this repository into a multi-skill platform unless the SEO/GEO workflow truly splits into independent skills. The current shape should stay small: one domain skill, strong references, reusable templates, deterministic validation, and a simple agent-first install path.
