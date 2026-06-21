# ARD / ai-catalog Runbook

Use this when a site, skill, MCP server, A2A agent, or callable AI service should be discoverable as an agentic resource.

ARD is currently a draft specification. Treat it as an optional discoverability layer, not as a Google ranking factor and not as a replacement for `/llms.txt`, `/for-ai`, schema.org, or visible human content.

## Generate A Draft Catalog

```bash
python3 scripts/generate_ard_catalog.py \
  --publisher-domain example.com \
  --display-name "SEO GEO Growth Agent" \
  --resource-name seo-geo-growth-agent \
  --resource-url https://github.com/bacoco/seo-geo-growth-agent \
  --output ai-catalog.json
```

Publish the result at:

```text
/.well-known/ai-catalog.json
```

Validate the draft before it is sent to an owner or published:

```bash
python3 scripts/validate_ard_catalog.py ai-catalog.json
```

## Check A Site

When auditing a site that exposes a skill, MCP server, A2A agent, callable AI service, or other agentic resource, inspect all ARD discovery signals:

```bash
python3 scripts/check_ard_readiness.py \
  --url https://example.com/ \
  --output reports/example.com/2026-06-21/ard-readiness.json
```

Copy the resulting JSON object into `audit.json` as `ard_readiness`.

## Audit Checks

Check for:

- `/.well-known/ai-catalog.json`
- `<link rel="ai-catalog" href="...">`
- `Agentmap: https://example.com/catalog.json` in `robots.txt`
- valid `specVersion`
- `identifier` using `urn:air:<publisher>:<namespace>:<resource-name>`
- exactly one of `url` or `data` per entry
- 2 to 5 `representativeQueries`
- optional `trustManifest` for enterprise trust and provenance

If these signals are absent and ARD is in scope, generate an owner-review draft with `scripts/generate_ard_catalog.py` or include `ard_readiness.entries[]` before running `scripts/generate_ai_layer_package.py`. The downloadable AI-layer package will then include `ai-catalog.json` alongside `/llms.txt`, `/for-ai`, JSON, TXT, JSON-LD, and `AI_LAYER_INSTALL.md`.

## Guardrails

- Label ARD evidence as `draft` or `experimental` until the spec stabilizes.
- Do not claim ARD improves rankings or AI citations by itself.
- Keep trust, compliance, and source claims explicit and verifiable.
- Use `representativeQueries` as search/discovery examples, not manipulative hidden prompts.
