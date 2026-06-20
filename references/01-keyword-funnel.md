# 01 — Keyword Funnel Strategy

## Goal

Create a search strategy that starts with purchase-intent terms, expands into category-intent terms, then supports with educational content.

## Funnel definitions

| Funnel | Searcher state | Typical page types | CTA style |
|---|---|---|---|
| BOFU | Ready to decide or buy | Pricing, alternatives, vs pages, best-for pages, integration purchase pages | Strong CTA |
| MOFU | Comparing approaches and vendors | Category guides, use-case pages, listicles, implementation guides | Medium CTA |
| TOFU | Learning and problem-aware | How-to, definitions, templates, glossary, reports | Soft CTA |

## Keyword patterns

### BOFU patterns

- `[PRODUCT] pricing`
- `[PRODUCT] alternatives`
- `[PRODUCT] reviews`
- `[PRODUCT] vs [COMPETITOR]`
- `[COMPETITOR] alternative`
- `best [CATEGORY] software for [AUDIENCE]`
- `[CATEGORY] tool for [USE_CASE]`
- `[CATEGORY] with [INTEGRATION]`

### MOFU patterns

- `how to choose [CATEGORY] software`
- `[CATEGORY] comparison`
- `[CATEGORY] platforms`
- `[CATEGORY] for [INDUSTRY]`
- `[USE_CASE] workflow`
- `[INTEGRATION] + [CATEGORY]`
- `[CATEGORY] checklist`

### TOFU patterns

- `what is [CONCEPT]`
- `how to [TASK]`
- `[CONCEPT] examples`
- `[TASK] template`
- `[CATEGORY] best practices`
- `[CONCEPT] glossary`

## Prioritization score

Use 1–5 for each factor.

| Factor | 1 | 3 | 5 |
|---|---|---|---|
| Intent | Informational only | Researching solution | Ready to choose/buy |
| Business fit | Adjacent | Relevant | Core category/use case |
| Feasibility | Strong incumbents, high difficulty | Mixed SERP | Weak SERP / long-tail |
| Content gap | Already covered well | Needs refresh | Missing page |
| GEO citability | Narrative only | Some facts | Direct-answer/table/FAQ friendly |
| Conversion path | Weak | Soft | Direct CTA fit |

Suggested formula:

```text
Priority = Intent + Business fit + Feasibility + Content gap + GEO citability + Conversion path
```

## Keyword-to-page map rules

- One primary keyword has one primary URL.
- A page can target one primary keyword and several secondary terms with the same intent.
- Do not create separate pages for near-identical intent unless geography, audience, integration, or competitor creates a genuinely different decision context.
- Add internal links from informational content to BOFU/MOFU pages.
- Mark every keyword with status: `planned`, `drafting`, `published`, `indexed`, `ranking`, `refresh`, `merge`, or `retire`.

## Output template

```markdown
| Keyword | Funnel | Intent | Searcher job | Primary URL | Page type | Volume | KD | Priority | CTA | Status |
|---|---|---|---|---|---|---:|---:|---:|---|---|
```
