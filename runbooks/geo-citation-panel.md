# GEO Citation Panel

Use when structural readiness is not enough and the user needs a repeatable prompt panel for ChatGPT, Perplexity, Claude, or another answer engine.

## Command

```bash
python3 scripts/generate_geo_citation_panel.py \
  --site example.com \
  --output reports/example/<date>/geo-citation-panel.csv
```

## Rule

The generated CSV is `ready_not_executed`. It is not evidence that the site is cited or not cited. Real citation metrics remain `unknown` until someone runs the panel and records the answers.

Minimum prompt families:

- `brand_discovery`
- `category_discovery`
- `concept_explanation`
- `project_discovery`
- `booking_boundary`
- `source_integrity`
