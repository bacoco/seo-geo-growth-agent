# Repository Structure

```text
.
├── SKILL.md                  # Main agent skill entrypoint
├── manifest.json             # Machine-readable skill metadata and file index
├── references/               # Operating doctrine, SOPs, policies, and research notes
├── templates/                # Reusable audit/report/strategy templates
├── scripts/                  # Validation, packaging, and GitHub helper scripts
├── docs/                     # Repo publishing and maintenance docs
└── .github/                  # CI, issue templates, and PR template
```

The canonical skill entrypoint is `SKILL.md`. When adding or removing files under `references/` or `templates/`, update `manifest.json` and run `python3 scripts/validate_skill.py`.
