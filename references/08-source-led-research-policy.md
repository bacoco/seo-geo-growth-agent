# Source-Led Research Policy

Use this reference whenever the agent is asked to do “deep research”, validate SEO/GEO claims, update crawler policies, review tooling, or add new tactics to the playbook.

## Evidence hierarchy

| Tier | Source type | How to use it | Confidence |
|---|---|---|---|
| 1 | Official platform documentation and help centers | Treat as source of truth for platform behavior, eligibility, reporting, robots.txt controls, and policy | High |
| 2 | Official standards/specifications and primary product docs | Use for technical implementation, syntax, APIs, and protocol readiness | High |
| 3 | First-party analytics and logs | Use for actual site performance, bot access, referrals, conversions, and index coverage | High |
| 4 | Academic research / benchmarks | Use as hypotheses and test design, not guaranteed production outcomes | Medium |
| 5 | Open-source repos and GitHub discussions | Use for implementation patterns and tooling inspiration | Medium-low |
| 6 | Reddit/forums/social | Use for pain points, edge cases, and warnings to investigate | Low |
| 7 | Vendor blogs / “ultimate GEO guides” | Use only after checking claims against tiers 1–4 | Low until verified |

## Research workflow

1. Define the claim or question.
2. Find official documentation first.
3. Record the exact source, date checked, and the practical implication.
4. Compare against analytics/logs where possible.
5. Convert only evidence-backed findings into skill changes.
6. Mark community and vendor findings as `Hypothesis` unless validated.
7. Add risky claims to the red-team checklist before recommending them.

## Output format

Use this structure in reports:

```markdown
## Finding
[One sentence]

## Evidence
- Official source: [URL / citation]
- Analytics/log source: [if available]
- Community/tool source: [if relevant]

## Confidence
High / Medium / Low

## Recommendation
[Action]

## Risk
[What could go wrong]

## Owner
SEO / Dev / Analytics / Content / Legal / Product
```

## Common false-positive traps

- Treating `llms.txt` as a universal AI-search ranking factor.
- Treating a GitHub crawler list as authoritative without checking vendor docs.
- Creating thin pages for every fan-out query.
- Adding statistics without sources.
- Claiming AI citation wins from manual prompt tests with no repeatability.
- Blocking training bots and accidentally blocking search/index bots.
- Reading Reddit bot traffic anecdotes as universal crawler behavior.
