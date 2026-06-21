# Examples

These examples are committed reference artifacts for the skill workflow.

They are not market research, traffic data, ranking proof, conversion evidence, or AI citation evidence. They exist to show the expected file structure and validation behavior without inventing owner-only metrics.

## Reference Audit

`examples/reference-audit/` is the golden audit for the public `bacoco/seo-geo-growth-agent` GitHub repository. It contains:

- `audit.json`
- `index.html`
- `LATEST-SEO-GEO-REPORT.md`
- `report-validation.json`
- `ai-layer-package/`
- `ai-layer-package.zip`

Validate it with:

```bash
python3 scripts/validate_audit_report.py --report-dir examples/reference-audit
```
