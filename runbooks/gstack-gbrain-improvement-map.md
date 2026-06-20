# GStack/GBrain Improvement Map

Use this map when improving the skillpack after reviewing GStack, GBrain, or adjacent SEO/GEO tools.

| # | Idea | Origin | Applied artifact |
|---:|---|---|---|
| 1 | Agent Browser first, fallback browser automation | GStack browser | `runbooks/visual-html-audit.md`, `scripts/capture_site_screenshots.mjs` |
| 2 | Desktop/mobile site screenshot evidence | GStack browser/QA | `site_visual_evidence[]` in audit JSON |
| 3 | Weighted health/readiness scoring | GStack health | `scorecards[]` in audit JSON |
| 4 | Browser-readable local report | GStack reports | `scripts/generate_html_audit_report.py`, `scripts/serve_report.py` |
| 5 | Public vs owner-only measurement matrix | GSC/GA4/CrUX | `runbooks/public-measurement-access.md`, `templates/measurement-access-matrix.csv` |
| 6 | Codify repeated browser audits | GStack scrape/skillify | `templates/browser-audit-codification.md` |
| 7 | Installed package doctor | GBrain skillpack-check | `scripts/skill_doctor.py` |
| 8 | Routing evals by mode | GBrain skillopt | `evals/routing-eval.jsonl` |
| 9 | Domain decision memory | GBrain memory | `templates/domain-decision-log.jsonl` |
| 10 | Domain notes per audited site | GStack domain-skills | `templates/domain-notes.md` |
| 11 | Before/after visual comparison | GStack QA/design-review | `templates/visual-diff-checklist.md` |
| 12 | Evidence-first artifacts | GStack QA | `audit.json`, `sources[]`, `findings[].evidence[]` |
| 13 | Source confidence scoring | GBrain citation discipline | `templates/source-confidence-register.csv` |
| 14 | Stable machine export | GStack reports | `audit.json` |
| 15 | Local private skill analytics | GStack telemetry pattern | `templates/local-skill-analytics.jsonl` |
| 16 | Report-only mode | GStack qa-only | `runbooks/visual-html-audit.md` |
| 17 | Skill optimization loop | GBrain skillopt | `runbooks/skill-optimization.md` |
| 18 | Source registry | GBrain memory/citations | `references/99-source-register.md` |
| 19 | Crawler policy freshness checks | SEO/GEO docs | `templates/crawler-policy-freshness-check.md` |
| 20 | Install doctor after setup | GBrain install/check | `INSTALL_FOR_AGENTS.md`, `scripts/skill_doctor.py` |
| 21 | Design Watch scoring from rendered screenshots | GStack design-review | `templates/design-watch-audit.md`, `design_watch`, `analysis_cohorts[]` |

Do not copy GStack/GBrain implementation details blindly. Keep this skill focused on SEO/GEO outputs, evidence, measurements, and safe installability.
