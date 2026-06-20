# Responsive Dynamic Study

Use this after rendering the audited homepage or page in mobile and desktop
browser viewports.

## Goal

Determine whether the page responds correctly in a real browser and summarize
what a human or browser agent can conclude from the rendered page.

## Required Output

```json
{
  "method": "Agent Browser | Chrome DevTools fallback",
  "summary": {
    "status": "pass | warning | failed | unavailable",
    "verdict": "",
    "confidence": "low | medium | high"
  },
  "viewports": [
    {
      "label": "Mobile",
      "viewport": "390x1400",
      "status": "pass | warning | failed",
      "issues": [],
      "metrics": {
        "title": "",
        "horizontalOverflow": false,
        "scrollWidth": 390,
        "documentHeight": 0,
        "hasViewportMeta": true,
        "h1Count": 1,
        "h1Text": [],
        "missingImages": 0,
        "visibleTextLength": 0
      }
    }
  ]
}
```

## Checks

- Mobile viewport renders without horizontal overflow.
- Desktop viewport renders without unexpected overflow.
- Page has a title and clear H1.
- Main visible text is present.
- Images load or missing images are reported.
- Mobile navigation does not hide the main content.
- The first screen gives enough context to understand the page.

## Guardrails

- Do not infer traffic, SEO performance, ranking, or conversion from responsive rendering.
- If Agent Browser is unavailable, use the bundled Chrome fallback and state the method.
- If both Agent Browser and Chrome fallback fail, still generate the HTML report and include `screenshot_status` plus a lower-confidence `responsive_study`.
