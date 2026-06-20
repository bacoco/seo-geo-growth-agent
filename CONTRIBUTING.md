# Contributing

Thanks for improving the SEO + GEO Growth Agent Skill.

## Contribution principles

1. Prefer official platform documentation over vendor claims, social posts, and experiments.
2. Do not add tactics that depend on fake citations, fabricated authority, hidden text, cloaking, or bot manipulation.
3. Label evidence clearly: `Observed`, `Inferred`, or `Recommended`.
4. Add source dates for platform-specific claims because AI search reports, crawler names, and robots policies change.
5. Keep templates practical and auditable.

## Local validation

Run:

```bash
python3 scripts/validate_skill.py
```

The validator checks that `manifest.json` points to files that exist, that `SKILL.md` exists, and that common repository files are present.

## Pull request checklist

- [ ] I updated `CHANGELOG.md` if behavior or templates changed.
- [ ] I updated `manifest.json` when adding/removing templates or references.
- [ ] I added/updated source notes when adding external claims.
- [ ] I ran `python3 scripts/validate_skill.py`.
