# llms.txt / llms-full.txt Generation Checklist — [DOMAIN]

## Source of truth

- [ ] Canonical sitemap URL confirmed.
- [ ] Docs/blog/product URLs filtered to canonical, indexable, 200-status pages.
- [ ] Staging, parameterized, duplicate, redirect, noindex, and private URLs excluded.
- [ ] Product/pricing facts checked against approved source of truth.
- [ ] Last-updated dates included where useful.

## `/llms.txt` contents

- [ ] One-sentence brand/entity description.
- [ ] Category and audience definition.
- [ ] Canonical links to homepage, product, pricing, docs, comparisons, support, about, security, changelog, API docs.
- [ ] Entity naming guidance and common misclassification warnings.
- [ ] Citation preference and canonical URL instructions.
- [ ] Short enough to be reviewed manually.

## `/llms-full.txt` contents

- [ ] Expanded Markdown digest of the most important public pages.
- [ ] Each section includes source URL and last-updated date.
- [ ] No private, paywalled, regulated, or legally sensitive content included accidentally.
- [ ] Generated from canonical content, not from stale copy.
- [ ] Regenerated after major docs/product/pricing updates.

## Guardrails

- Do not claim `llms.txt` improves Google Search ranking or Google AI feature inclusion.
- Do not put instructions that conflict with visible public content.
- Do not use `llms.txt` as a substitute for schema, sitemap, internal links, or content quality.
- Treat it as a resource map for agents/tools and an internal quality-control artifact.

## Maintenance

- [ ] Add CI or monthly task to compare sitemap vs `llms.txt` links.
- [ ] Check for broken links.
- [ ] Check that pricing/docs pages are current.
- [ ] Re-run after site migrations.
