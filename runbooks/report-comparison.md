# Report Comparison

Use when the user has two SEO/GEO audit JSON files and wants to know what changed.

## Command

```bash
python3 scripts/compare_audit_reports.py \
  --before reports/<site>/<old-date>/audit.json \
  --after reports/<site>/<new-date>/audit.json \
  --output-dir reports/<site>/<new-date>/comparison
```

Outputs:

- `audit-comparison.json`
- `audit-comparison.md`

## Reading Rule

Prefer the narrative conclusion for user-facing discussion. Tables are useful for QA, but the final answer should explain whether the newer report is better, worse, stable, or blocked by missing evidence.
