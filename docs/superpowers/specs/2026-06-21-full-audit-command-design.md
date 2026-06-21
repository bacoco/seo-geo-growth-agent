# Full Audit Command Design

## Goal

Turn `seo-geo-growth-agent` from a collection of audit helpers into a reproducible analysis-and-improvement workflow: one command should create the audit workspace, collect deterministic evidence, generate owner-review improvement files, render the HTML report, and optionally serve it.

## Scope

This release adds:

- `scripts/run_full_audit.py`: orchestration for the common end-to-end workflow.
- `scripts/validate_audit_report.py`: deterministic report completeness validation.
- `examples/reference-audit/`: a committed reference artifact showing the expected output shape.
- README/SKILL/runbook updates that explain the “analysis plus generated improvements” model.

The command must not invent SEO metrics, traffic numbers, rankings, conversions, or citations. When data is unavailable, it writes explicit `unknown` or `requires owner data` values.

## Architecture

`run_full_audit.py` is an orchestrator, not a second audit engine. It uses existing scripts for browser evidence, owner-data requests, ARD readiness, AI-layer package generation, HTML rendering, report validation, and serving.

When no human-authored `audit.json` is supplied, the orchestrator writes an evidence-only draft from observed files and public endpoint checks. The draft is intentionally conservative: it can say files are missing, screenshots are unavailable, owner metrics are unknown, and generated files require owner review. It cannot claim rankings, traffic, authority, or AI citation performance.

`validate_audit_report.py` validates the report directory after generation. It checks required files, required audit fields, screenshot or screenshot-status evidence, responsive evidence or explicit limits, AI-layer package consistency, ZIP members, and latest-report receipt.

## Data Flow

1. Normalize URL and output directory.
2. Optionally capture screenshots/responsive study/evidence engine unless `--skip-browser` is set.
3. Generate owner-data request files.
4. Check ARD readiness.
5. Check public AI-layer endpoints: `/llms.txt`, `/for-ai`, `/for-ai.json`, `/for-ai.txt`.
6. Create or update `audit.json`.
7. Generate `ai-layer-package.zip` when AI-readable files are missing or `--force-package` is set.
8. Generate `index.html` and `LATEST-SEO-GEO-REPORT.md`.
9. Validate the report directory.
10. Optionally serve the report with `scripts/serve_report.py`.

## Validation Rules

The validator returns exit code `0` only when:

- `audit.json`, `index.html`, and `LATEST-SEO-GEO-REPORT.md` exist.
- `audit.json` has `site`, `audited_url`, `generated_at`, `report_language`, `summary`, `findings`, and `sources`.
- Site visual evidence exists, or `screenshot_status` explains why screenshots are unavailable.
- Responsive evidence exists, or `responsive_study.summary.status` is `unavailable` with a verdict.
- If `ai_layer_current_state` reports missing AI-readable files, `ai_layer_package` exists and every listed file exists.
- If `ai_layer_package.zip` is listed, the ZIP exists and contains every listed package file.

## Testing

Tests use a local HTTP fixture server to avoid external dependency and fake public metrics. The fixture is an explicit test site, not an invented market dataset.

Required tests:

- `run_full_audit.py --skip-browser --no-serve` creates `audit.json`, owner-data files, ARD readiness, AI-layer package, `index.html`, receipt, and validation report.
- `validate_audit_report.py` fails when missing AI-readable files are reported without a generated package.
- `examples/reference-audit/` contains a valid reference report and package.

## Documentation

README and SKILL must make the positioning explicit:

> The skill audits a site and produces owner-review improvement files. The generated files are drafts to adapt and publish, not claims that the site is already fixed.

## Release

Ship as `v1.2.8` after tests, `scripts/validate_skill.py`, syntax checks, and install smoke tests pass.
