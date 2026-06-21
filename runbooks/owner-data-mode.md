# Owner Data Mode Runbook

Use this when public evidence is not enough and the site owner can provide exports or access.

## Generate The Request

```bash
python3 scripts/generate_owner_data_request.py \
  --site https://example.com/ \
  --output-dir reports/example.com/owner-data \
  --language en
```

For French:

```bash
python3 scripts/generate_owner_data_request.py \
  --site https://example.com/ \
  --output-dir reports/example.com/owner-data \
  --language fr
```

## Ask For

- Google Search Console performance and indexing exports.
- GA4 landing page, source/medium, conversion, engagement, and AI-referral exports.
- Bing Webmaster Tools search, crawl, IndexNow, and AI Performance data when available.
- Server logs for search crawlers, AI search crawlers, training crawlers, and user-triggered fetchers.
- Cloudflare Analytics for traffic, cache, WAF/firewall, bot, and response-status evidence.

## Guardrails

- Do not bypass Cloudflare or other protections. Use owner analytics, logs, cache headers, WAF events, or temporary owner-approved access.
- Ask before using paid or credit-consuming tools.
- Keep absent owner data as `unknown` or `requires owner data`; do not score it as zero.
- Record the source, export date, property/domain, and audit window for every owner-supplied file.
