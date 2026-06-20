# Visual HTML Audit Runbook

Use this runbook when the user asks for a readable SEO/GEO audit report, a browser-viewable report, screenshots, Agent Browser validation, or a served local report.

## Outcome

Produce an evidence-led report that can be opened in a browser:

```text
reports/<site-slug>/<YYYY-MM-DD>/
├── audit.json
├── index.html
└── screenshots/
    ├── desktop.png
    └── mobile.png
```

The HTML report is a presentation layer. It must not create facts. All metrics, statuses, sources, screenshots, and recommendations must come from observed evidence or be marked as unknown.

## Required Inputs

Collect or infer from evidence:

| Field | Requirement |
|---|---|
| `site` | Domain or page being audited |
| `generated_at` | ISO timestamp |
| `summary.headline` | One-sentence finding |
| `summary.status` | `ok`, `partial`, `missing`, or `unknown` |
| `summary.biggest_blocker` | Highest-impact issue, or `unknown` |
| `summary.fastest_win` | Best next action, or `unknown` |
| `summary.data_confidence` | `high`, `medium`, or `low` |
| `findings[]` | P0/P1/P2 findings with Observed, Inferred, Recommended |
| `sources[]` | URLs, files, APIs, or screenshots used |

Optional:

- `metrics[]`
- `scorecards[]`
- `visual_evidence[]`
- `public_measurements[]`
- `action_plan[]`

## Workflow

1. Run the normal SEO/GEO audit first.
2. Convert the audit into `audit.json`.
3. Generate the dynamic HTML report:

```bash
python scripts/generate_html_audit_report.py \
  --input reports/<site-slug>/<YYYY-MM-DD>/audit.json \
  --output-dir reports/<site-slug>/<YYYY-MM-DD>
```

4. Start the local server:

```bash
python scripts/serve_report.py \
  --dir reports/<site-slug>/<YYYY-MM-DD> \
  --port 8766 \
  --open
```

If the preferred port is busy, the server chooses a nearby free port and prints the URL.

## Visual Evidence

Prefer Agent Browser when the runtime exposes it.

Use Agent Browser to:

- open the audited site and the generated report;
- capture desktop and mobile screenshots;
- inspect visible hierarchy, readability, overlapping text, horizontal overflow, broken images, and mobile wrapping;
- add only observed visual facts to `visual_evidence[]`;
- regenerate the report after adding screenshot entries.

If Agent Browser is unavailable, use the Chrome/DevTools fallback:

```bash
node scripts/capture_report_screenshots.mjs \
  --url http://127.0.0.1:8766/ \
  --output-dir reports/<site-slug>/<YYYY-MM-DD>/screenshots \
  --evidence-out reports/<site-slug>/<YYYY-MM-DD>/visual-evidence.json
```

Then copy the relevant entries into `audit.json` under `visual_evidence[]` and regenerate the HTML report.

## Audit JSON Shape

```json
{
  "site": "example.com",
  "generated_at": "2026-06-20T18:00:00+02:00",
  "summary": {
    "headline": "Make example.com easier for agents to cite.",
    "description": "Short plain-language summary.",
    "status": "partial",
    "biggest_blocker": "No /llms.txt or /for-ai package",
    "fastest_win": "Add structured summaries to key pages",
    "data_confidence": "medium",
    "decision": "Prioritize evidence-led fixes before content scale."
  },
  "metrics": [
    {
      "label": "Crawl",
      "value": "OK",
      "detail": "Homepage returns 200"
    }
  ],
  "scorecards": [
    {
      "label": "SEO",
      "score": 7,
      "max": 10,
      "note": "Crawlable but missing metadata."
    }
  ],
  "findings": [
    {
      "priority": "P1",
      "title": "Missing agent-readable package",
      "observed": ["/llms.txt returns 404"],
      "inferred": ["Agents must infer citation guidance"],
      "recommended": ["Create /llms.txt and /for-ai pages"],
      "evidence": [
        {
          "label": "llms.txt",
          "url": "https://example.com/llms.txt",
          "status": "404"
        }
      ]
    }
  ],
  "visual_evidence": [
    {
      "label": "Homepage mobile",
      "path": "screenshots/mobile.png",
      "viewport": "390x1400",
      "notes": ["No horizontal overflow detected"]
    }
  ],
  "public_measurements": [
    {
      "source": "Chrome UX Report",
      "access": "public_if_enough_traffic",
      "metric": "Core Web Vitals field data",
      "limit": "No visit counts, queries, or conversions"
    }
  ],
  "action_plan": [
    {
      "when": "Day 1",
      "action": "Fix sitemaped 500 URLs",
      "outcome": "No known server errors in sampled sitemap URLs"
    }
  ],
  "sources": [
    {
      "label": "Homepage",
      "url": "https://example.com/"
    }
  ]
}
```

## Quality Bar

- Keep `Observed`, `Inferred`, and `Recommended` separate.
- Do not invent traffic, ranking, citation, or conversion metrics.
- Do not describe a visual issue unless it appears in a screenshot, DOM check, or browser observation.
- Do not use screenshots as proof of crawl/index status.
- Keep generated reports out of release packages unless the user explicitly asks for an example artifact.
