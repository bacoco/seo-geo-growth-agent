# Visual HTML Audit Runbook

Use this runbook when the user asks for a readable SEO/GEO audit report, a browser-viewable report, screenshots, Agent Browser validation, first-impression analysis, Design Watch scoring, or a served local report.

## Outcome

Produce an evidence-led report that can be opened in a browser:

```text
reports/<site-slug>/<YYYY-MM-DD>/
├── audit.json
├── index.html
├── ai-layer-package.zip
├── ai-layer-package/
└── screenshots/
    ├── desktop.png
    └── mobile.png
```

The HTML report is a presentation layer. It must not create facts. All metrics, statuses, sources, screenshots, and recommendations must come from observed evidence or be marked as unknown.

Screenshots are evidence for the audited site, not for the report. Capture the site or page being audited, analyze those screenshots, and feed the visual verdict back into `audit.json` before generating the report.

If the user asks to improve, score, or screenshot the report UI itself, capture the
generated `index.html` in desktop and mobile viewports after regeneration. Treat
those report screenshots as QA evidence for the presentation layer, not as site
audit evidence.

This workflow is mandatory for normal domain/URL audits. Do not stop at a prose
answer when the user asked to use the skill on a site. If screenshot capture
fails, continue: create `audit.json`, include `screenshot_status`, generate
`index.html`, and serve or validate the report.

## Required Inputs

Collect or infer from evidence:

| Field | Requirement |
|---|---|
| `site` | Domain or page being audited |
| `report_language` | Language used by the user, such as `fr` or `en` |
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
- `analysis_cohorts[]`
- `design_watch`
- `site_visual_evidence[]`
- `responsive_study`
- `screenshot_status`
- `public_measurements[]`
- `action_plan[]`
- `ai_layer_package`

## Workflow

1. Run the normal SEO/GEO audit first.
2. Capture desktop and mobile screenshots of the audited URL and run a dynamic responsive study. If this fails, record why in `screenshot_status`.
3. Analyze the screenshots and write a `design_watch` verdict. Analyze mobile/desktop rendering and write `responsive_study`. If screenshots are unavailable, write lower-confidence blocks based only on rendered/HTML evidence and state the limit.
4. Convert the audit into `audit.json` in the user's language. Set `report_language` to the language of the user's request.
5. If `/llms.txt`, `/for-ai`, `/for-ai.json`, `/for-ai.txt`, or aligned JSON-LD are missing or recommended, generate the downloadable AI-layer publication pack:

```bash
python scripts/generate_ai_layer_package.py \
  --input reports/<site-slug>/<YYYY-MM-DD>/audit.json \
  --output-dir reports/<site-slug>/<YYYY-MM-DD> \
  --update-audit
```

6. Generate the dynamic HTML report:

```bash
python scripts/generate_html_audit_report.py \
  --input reports/<site-slug>/<YYYY-MM-DD>/audit.json \
  --output-dir reports/<site-slug>/<YYYY-MM-DD>
```

7. Start the local server:

```bash
python scripts/serve_report.py \
  --dir reports/<site-slug>/<YYYY-MM-DD> \
  --port 8766 \
  --open
```

If the preferred port is busy, the server chooses a nearby free port and prints the URL.

8. When report UI quality is in scope, screenshot the served report itself in
desktop and mobile viewports, review the resulting images, and iterate on the
presentation layer until text hierarchy, spacing, wrapping, tabs, and visual
evidence are clean.

## Completion Checklist

Before finalizing, verify that all applicable deliverables exist:

| Deliverable | Required |
|---|---:|
| `audit.json` | yes |
| `index.html` | yes |
| local report URL or exact `index.html` path | yes |
| desktop and mobile site screenshots | yes, unless unavailable |
| `responsive_study` for mobile and desktop | yes |
| `screenshot_status` reason when screenshots are missing | yes, if screenshots failed |
| `design_watch` | yes |
| `analysis_cohorts[]` | yes for global reports |
| `report_language` matching the user's language | yes |
| downloadable AI-layer package | yes, when AI-readable layers are missing or recommended |
| report desktop/mobile screenshots | yes, when UI quality is requested |

## Design Watch From Site Screenshots

Prefer Agent Browser when the runtime exposes it.

Use Agent Browser to:

- open the audited site, not the generated report;
- capture desktop and mobile screenshots of the audited URL;
- run a dynamic responsive study of at least the homepage in mobile and desktop viewports;
- inspect first impression, visible hierarchy, brand trust, content clarity, mobile wrapping, horizontal overflow, broken images, and topic fit;
- write a `design_watch` object with score, verdict, observed facts, inferred risks, and recommended fixes;
- write a `responsive_study` object with method, pass/warning status, viewport metrics, issues, and a short verdict;
- add only observed visual facts to `site_visual_evidence[]`;
- regenerate the report after adding screenshot entries.

If Agent Browser is unavailable, use the Chrome/DevTools fallback:

```bash
node scripts/capture_site_screenshots.mjs \
  --url https://example.com/ \
  --output-dir reports/<site-slug>/<YYYY-MM-DD>/site-screenshots \
  --evidence-out reports/<site-slug>/<YYYY-MM-DD>/site-visual-evidence.json \
  --study-out reports/<site-slug>/<YYYY-MM-DD>/responsive-study.json
```

Then copy the relevant entries into `audit.json` under `site_visual_evidence[]`, copy `responsive-study.json` under `responsive_study`, add `design_watch`, and regenerate the HTML report.

For the responsive study, read `templates/responsive-dynamic-study.md`.

Use this scoring frame:

| Dimension | What to judge from screenshots |
|---|---|
| First 5 seconds | Is the subject, value, and credibility clear immediately? |
| Trust signal | Does the visual identity match the claimed expertise? |
| Information hierarchy | Can the reader or browser agent identify the main content path? |
| Mobile readability | Are headings, nav, body text, and calls to action readable without friction? |
| Topic fit | Do imagery, typography, and layout support the site topic instead of distracting? |

## Analysis Cohorts

Add `analysis_cohorts[]` when producing a global report. Cohorts keep the
analysis readable by separating audiences and systems:

| Cohort | Typical Lens |
|---|---|
| Search / crawl | Can Google/Bing fetch, understand, and index the site cleanly? |
| AI citation | Can answer engines identify source-worthy facts and limits? |
| Browser agent | Can an agent understand the page state and next action visually/semantically? |
| Design Watch | Does the first screen create trust and explain the site's value? |
| Measurement owner | Which claims require GSC, analytics, logs, or private owner data? |
| Skillpack quality | Did the generated report follow evidence, eval, and install guardrails? |

Each cohort should include `name`, `score`, `status`, `what_it_checks`,
`verdict`, `evidence`, and `next_action`.

## Audit JSON Shape

```json
{
  "site": "example.com",
  "report_language": "en",
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
  "analysis_cohorts": [
    {
      "name": "Design Watch",
      "score": "6/10",
      "status": "partial",
      "what_it_checks": "First impression, hierarchy, trust, and mobile readability",
      "verdict": "Readable but visually under-positioned",
      "evidence": "Desktop and mobile screenshots reviewed",
      "next_action": "Replace generic imagery with topic-relevant editorial identity"
    }
  ],
  "design_watch": {
    "score": "6/10",
    "verdict": "Readable but visually under-positioned",
    "summary": "The page is understandable, but the first impression weakens trust for a technical AI audience.",
    "confidence": "medium",
    "observed": ["Desktop and mobile screenshots show readable body content."],
    "inferred": ["The visual identity may reduce perceived authority before the article is read."],
    "recommended": ["Replace generic imagery with topic-specific editorial identity."]
  },
  "responsive_study": {
    "method": "Agent Browser",
    "summary": {
      "status": "pass",
      "verdict": "Homepage responds correctly on tested mobile and desktop viewports.",
      "confidence": "medium"
    },
    "viewports": [
      {
        "label": "Mobile",
        "viewport": "390x1400",
        "status": "pass",
        "issues": [],
        "metrics": {
          "title": "Example",
          "horizontalOverflow": false,
          "scrollWidth": 390,
          "documentHeight": 1400,
          "hasViewportMeta": true,
          "h1Count": 1,
          "h1Text": ["Example"],
          "missingImages": 0
        }
      }
    ]
  },
  "site_visual_evidence": [
    {
      "label": "Homepage mobile",
      "path": "site-screenshots/mobile.png",
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
  "ai_layer_package": {
    "status": "generated",
    "zip_path": "ai-layer-package.zip",
    "files": [
      {
        "label": "llms.txt",
        "path": "ai-layer-package/llms.txt",
        "purpose": "Site-level AI assistant index"
      }
    ]
  },
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
- Do not use screenshots of the generated report as evidence for the audited site.
- Keep generated reports out of release packages unless the user explicitly asks for an example artifact.
