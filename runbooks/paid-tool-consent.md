# Paid Tool Consent

Use this runbook before any MCP/API call that may consume credits, paid quota, or billable usage, including Haloscan, Semrush, DataForSEO, Ahrefs, Similarweb, SerpApi, or equivalent tools.

## Rule

Ask for explicit approval before the paid call. Public fetches, local browser checks, local files, and free official docs do not require this approval.

## Approval Prompt

```text
This audit can use [TOOL] to retrieve [DATA]. It may consume paid credits or quota. Do you approve this call?
```

Record the answer in the audit notes or `templates/paid-tool-approval.md`.

## If Approval Is Missing

- Do not call the paid tool.
- Continue with public evidence.
- Mark the missing metric as `requires paid/owner data`.
- Add a production or owner-data gate if the metric is important.
