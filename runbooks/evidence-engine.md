# Evidence Engine Runbook

Use this when a site audit needs proof beyond screenshots: console health, network failures, cache/CDN headers, and measurable first-screen facts.

## Command

```bash
node scripts/capture_site_screenshots.mjs \
  --url https://example.com/ \
  --output-dir reports/example.com/site-screenshots \
  --evidence-out reports/example.com/site-visual-evidence.json \
  --study-out reports/example.com/responsive-study.json \
  --evidence-engine-out reports/example.com/evidence-engine.json
```

## Output Contract

The generated `evidence-engine.json` contains:

- `console_watch`: console messages classified as `first_party`, `third_party`, `browser_policy`, or `unknown`.
- `network_watch`: response counts, failed requests, status counts, and samples.
- `cache_cdn_watch`: captured cache/CDN headers such as `cache-control`, `cf-cache-status`, `x-cache`, `age`, `etag`, and `server`.
- `design_watch_metrics`: CTA visibility, trust-signal visibility, hero-height ratio, and next-section visibility by viewport.

## Interpretation Rules

- Do not treat third-party iframe or browser-policy noise as a first-party bug without checking the source URL.
- Do not call CDN evidence stale unless public headers conflict with owner deployment evidence.
- Do not treat CTA or trust-signal checks as full design judgment; use them as measurable anchors for Design Watch.
- If the runtime cannot capture browser events, mark the Evidence Engine as unavailable instead of inventing results.
