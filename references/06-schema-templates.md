# 06 — Schema Templates

Only add schema for content that is visible and accurate on the page. Validate before publishing.

## Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "[PRODUCT]",
  "url": "https://[DOMAIN]/",
  "logo": "https://[DOMAIN]/logo.png",
  "sameAs": [
    "https://www.linkedin.com/company/[PRODUCT_SLUG]",
    "https://x.com/[HANDLE]"
  ],
  "description": "[ONE_SENTENCE_ENTITY_DESCRIPTION]"
}
```

## WebSite with SearchAction

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "[PRODUCT]",
  "url": "https://[DOMAIN]/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://[DOMAIN]/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
```

## Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[TITLE]",
  "description": "[META_DESCRIPTION]",
  "author": {
    "@type": "Person",
    "name": "[AUTHOR_NAME]",
    "url": "[AUTHOR_URL]"
  },
  "publisher": {
    "@type": "Organization",
    "name": "[PRODUCT]",
    "url": "https://[DOMAIN]/"
  },
  "datePublished": "YYYY-MM-DD",
  "dateModified": "YYYY-MM-DD",
  "mainEntityOfPage": "https://[DOMAIN]/[PATH]"
}
```

## FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[QUESTION_1]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[ANSWER_1_VISIBLE_ON_PAGE]"
      }
    },
    {
      "@type": "Question",
      "name": "[QUESTION_2]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[ANSWER_2_VISIBLE_ON_PAGE]"
      }
    }
  ]
}
```

## HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "[HOW_TO_TITLE]",
  "description": "[HOW_TO_DESCRIPTION]",
  "step": [
    {
      "@type": "HowToStep",
      "name": "[STEP_1_TITLE]",
      "text": "[STEP_1_TEXT]"
    },
    {
      "@type": "HowToStep",
      "name": "[STEP_2_TITLE]",
      "text": "[STEP_2_TEXT]"
    }
  ]
}
```

## SoftwareApplication

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "[PRODUCT]",
  "applicationCategory": "[CATEGORY]",
  "operatingSystem": "Web",
  "url": "https://[DOMAIN]/",
  "description": "[ONE_SENTENCE_DESCRIPTION]",
  "offers": {
    "@type": "Offer",
    "price": "[PRICE_OR_0]",
    "priceCurrency": "[CURRENCY]",
    "url": "[PRICING_URL]"
  }
}
```

## BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://[DOMAIN]/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "[SECTION]",
      "item": "https://[DOMAIN]/[SECTION_PATH]"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "[PAGE_TITLE]",
      "item": "https://[DOMAIN]/[PATH]"
    }
  ]
}
```
