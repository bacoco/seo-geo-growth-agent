# CLI Audit Runbook

Use the CLI when the user wants a repeatable audit workspace rather than a one-off chat workflow.

## Plan Only

```bash
python3 scripts/seo_geo_audit.py https://example.com/ \
  --output-dir reports/example.com/2026-06-21 \
  --lang fr \
  --plan-only
```

This writes `audit-plan.json` with expected outputs and next commands.

## Capture Browser Evidence

```bash
python3 scripts/seo_geo_audit.py https://example.com/ \
  --output-dir reports/example.com/2026-06-21 \
  --lang fr
```

This starts browser capture and owner-data request generation. It does not fabricate `audit.json`; the agent must still write the audit from observed evidence, owner data, and explicit unknowns.

## Complete The Report

After writing `audit.json`, run:

```bash
python3 scripts/check_ard_readiness.py --url https://example.com/ --output reports/example.com/2026-06-21/ard-readiness.json
python3 scripts/generate_ai_layer_package.py --input reports/example.com/2026-06-21/audit.json --output-dir reports/example.com/2026-06-21 --update-audit
python3 scripts/generate_html_audit_report.py --input reports/example.com/2026-06-21/audit.json --output-dir reports/example.com/2026-06-21
python3 scripts/serve_report.py --dir reports/example.com/2026-06-21 --port 8766 --open
```

Run the ARD check only when agentic resources are in scope, then merge `ard-readiness.json` into `audit.json.ard_readiness` before generating the package if `ai-catalog.json` should be included.

## Rule

The CLI creates the workspace and deterministic evidence. It does not replace the LLM analysis step.
