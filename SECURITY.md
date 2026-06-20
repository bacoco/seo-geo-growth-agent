# Security Policy

This repository contains an agent skill and templates. It should not contain credentials, private analytics exports, raw server logs, or customer data.

## Reporting a concern

Open a private security advisory or contact the repository owner directly if you find:

- hardcoded credentials or API tokens;
- unsafe instructions that encourage cloaking, fake citations, or deceptive SEO/GEO behavior;
- templates that could leak private analytics, customer, or log data;
- crawler or robots.txt examples that are misleading or materially unsafe.

## Data-handling guidance

When using the skill with real sites, sanitize exports before sharing them in issues or pull requests. Remove user IDs, IP addresses, emails, order IDs, customer names, query parameters containing tokens, and private conversion data.
