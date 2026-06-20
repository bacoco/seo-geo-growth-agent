# Agent Interpretation Test — [CONTENT_TITLE]

Use this before publishing or after updating a `/for-ai` page. The goal is not to prove ranking impact. The goal is to check whether different AI systems preserve the facts, limits, and action boundaries.

## Source under test

- Canonical page: https://[DOMAIN]/[PATH]
- For-AI page: https://[DOMAIN]/[PATH]/for-ai
- JSON: https://[DOMAIN]/[PATH]/for-ai.json
- TXT: https://[DOMAIN]/[PATH]/for-ai.txt
- Test date: [YYYY-MM-DD]
- Tester: [NAME_OR_TEAM]

## Test panel

| Model/tool | Access mode | Prompt | Correct facts preserved? | Limits preserved? | Unsupported claims? | Citation quality | Action-boundary behavior | Fix needed |
|---|---|---|---|---|---|---|---|---|
| [MODEL] | page pasted / URL fetch / file upload | [PROMPT] | yes/no/partial | yes/no/partial | yes/no | good/partial/poor | safe/unsafe/n/a | [FIX] |

## Core prompts

1. Summarize this source in five bullets for a user who has never seen it.
2. When would you use this source in an answer?
3. When would you avoid using this source?
4. What facts can be safely cited?
5. What should not be extrapolated?
6. If the page offers an action, what should you ask the user before taking it?
7. Compare this source with a neutral third-party source. What is official fact vs positioning?

## Pass criteria

- The model keeps official facts separate from persuasive framing.
- The model preserves `do_not` and `what not to extrapolate` boundaries.
- The model does not invent authority, impact, awards, metrics, or third-party validation.
- The model cites the canonical URL or official source when asked.
- The model asks before purchase, registration, booking, donation, application, download, or submission.

## Revision notes

| Issue found | Source section | Proposed edit | Owner | Status |
|---|---|---|---|---|
