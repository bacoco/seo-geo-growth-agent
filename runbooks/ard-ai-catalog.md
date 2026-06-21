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

## Guardrails

- Label ARD evidence as `draft` or `experimental` until the spec stabilizes.
- Do not claim ARD improves rankings or AI citations by itself.
- Keep trust, compliance, and source claims explicit and verifiable.
- Use `representativeQueries` as search/discovery examples, not manipulative hidden prompts.
