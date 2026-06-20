# Design Watch Audit

Use this after capturing desktop and mobile screenshots of the audited site.

The goal is not to judge beauty in isolation. Judge whether the first visible
screen helps humans, search evaluators, and browser agents understand the
site's topic, trust level, and next action.

## Output

```json
{
  "score": "0/10",
  "verdict": "",
  "summary": "",
  "confidence": "low | medium | high",
  "observed": [],
  "inferred": [],
  "recommended": []
}
```

## Scoring Dimensions

| Dimension | Score | What To Check |
|---|---:|---|
| First 5 seconds | /2 | Topic, value, and credibility are clear without scrolling |
| Trust signal | /2 | Visual identity matches the claimed expertise and audience |
| Information hierarchy | /2 | H1, intro, navigation, and primary content path are obvious |
| Mobile readability | /2 | Text, nav, imagery, and calls to action work on mobile |
| Topic fit | /2 | Imagery, typography, and layout support the page subject |

## Required Separation

- `observed`: facts visible in screenshots or browser output.
- `inferred`: likely impact on trust, comprehension, citation, or conversion.
- `recommended`: concrete changes to test or implement.

## Guardrails

- Do not infer traffic, ranking, or conversion performance from screenshots.
- Do not criticize visual style without linking it to trust, comprehension,
  readability, citation quality, or task completion.
- Do not use screenshots of the generated report as site evidence.
