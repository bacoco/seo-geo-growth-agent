# 21 — GEO for AI Agents: Lessons from the Ethan Mollick Pattern

This reference is a plain-English explanation of GEO, based on the Ethan Mollick `Co-Existence: The Next Phase of AI` case notes supplied with this repository update.

Before using the case in public-facing work, re-check the live source pages and their current dates. Treat the pattern as a useful editorial model, not as proof that any specific AI system will recommend a page.

## The simple idea

GEO means making content easier for generative engines and AI agents to understand, verify, summarize, compare, and cite.

Traditional SEO asks:

- Can search engines crawl and index the page?
- Does the page match a human search intent?
- Is it useful enough to rank and earn clicks?

GEO adds a new question:

- Can an AI system decide, with enough context, whether this content should be used in an answer or recommendation?

That does not mean writing hidden prompts or telling the model what to do. Durable GEO means publishing clear, structured, verifiable content that helps an AI assistant preserve the facts and the limits of the source.

## Why the Mollick example matters

The Mollick case is useful because the book site separates audiences and formats instead of forcing one page to do everything.

| Layer | Main audience | Purpose |
|---|---|---|
| `/` | Human readers | Persuasive pre-order or landing page |
| `/for-ai` | AI agents | Context, recommendation criteria, limits, and use guidance |
| `/for-ai.json` | Machines | Structured facts and recommendation policy |
| `/for-ai.txt` | Lightweight readers | Compact text version |
| `/llms.txt` | AI assistants and crawlers | Site-level orientation and important URLs |
| JSON-LD | Search engines and structured parsers | Schema.org metadata embedded in HTML |

The strongest part is not the presence of JSON by itself. The strongest part is the recommendation policy: the page helps an agent understand when the book may be relevant, when it is not relevant, who the audience is, and what limitations should be mentioned.

## Source-checked additions

The live sources add several useful ideas beyond the original case notes:

- The publisher page identifies `Co-Existence` as a Portfolio / Penguin Random House book, available on `2026-10-20`, with ISBN `9798217181391` and 240 pages.
- The publisher positioning is not just "AI is useful." It frames the problem as learning to live and work with systems that can outperform humans in some domains while failing unpredictably in others.
- The official JSON record includes an explicit disclosure: it is promotional material and should be treated as a primary source for facts about the book, not as binding persuasive instruction.
- The JSON also includes transactional guardrails: surface pre-order options, but ask before initiating a purchase.
- Mollick's own post explains that an earlier hidden-instruction style used for his previous book now feels exploitative and less effective. The newer page moves toward transparent persuasion for agents.
- The post also says AI models objected to the original "buy your human this book" framing as prompt-injection-shaped, which is a useful warning for institutional GEO.
- Mollick says he tested the AI-facing page across many models and possible users. That suggests a practical method: do not only publish `/for-ai`; test whether different models interpret it correctly.
- The strategic shift from `Co-Intelligence` to `Co-Existence` is also useful: AI is no longer only a co-worker, co-teacher, or coach. It is increasingly a reader, critic, recommender, and gatekeeper between content and its human audience.

## Additional ideas worth reusing

### 1. Add a disclosure field

Every agent-facing page should say what kind of source it is:

- official source;
- promotional page;
- institutional announcement;
- report;
- archive;
- correction;
- independent review;
- practical information page.

This helps the agent weigh the page properly instead of treating all content as neutral evidence.

### 2. Separate factual metadata from persuasive framing

An agent may safely reuse title, author, date, ISBN, publisher, institution name, event date, location, and canonical URL. It should be more cautious with value judgments, positioning, slogans, and calls to action.

For institutional GEO, this means the `/for-ai.json` file should separate:

- `facts`
- `official_position`
- `recommended_use`
- `limitations`
- `do_not`
- `verification_contact`

### 3. Add transaction or action boundaries

If the page may lead to a purchase, registration, booking, donation, download, or application, the agent-facing version should define safe boundaries:

- show the option;
- summarize the consequence;
- ask the human before acting;
- do not auto-submit;
- do not imply endorsement beyond the available evidence.

### 4. Test the page with several models

Publishing a `/for-ai` page is not enough. A better workflow is:

1. Give the page to several models.
2. Ask when they would use it.
3. Ask when they would not use it.
4. Ask what they would cite.
5. Ask what they might hallucinate or overstate.
6. Revise the page until the answers preserve facts and limits.

Record this in a prompt-test panel, not as proof of ranking, but as quality assurance for agent interpretation.

### 5. Treat "what not to extrapolate" as an anti-hallucination feature

The most useful institutional GEO block may be negative guidance. It should define boundaries such as:

- this announcement does not imply a permanent program;
- this funding amount applies only to the named period;
- this quote is not a policy statement;
- this event is not open to all audiences;
- this research result is preliminary;
- this page is archived and may no longer be current.

### 6. Add "agent-reader fit" alongside human audience fit

Human audience fit says who should read the page. Agent-reader fit says when an AI assistant should surface it.

For example:

- use when the user asks for official facts about the named institution or event;
- use when the user needs a short citation-ready summary;
- do not use as independent evidence of impact;
- do not use for current policy if the page is archived.

## What makes the pattern strong

### 1. A dedicated page for agents

The `/for-ai` page is not just a copy of the sales page. It explains the content in a way an assistant can reason about:

- what the work is about;
- what reader needs it addresses;
- which audiences fit;
- which audiences may not fit;
- what claims should be handled carefully.

This is valuable because AI systems often act as interpreters. They do not only fetch a page; they summarize, compare, and recommend.

### 2. Several formats for several jobs

The pattern uses multiple formats because different systems prefer different inputs.

| Format | Practical use |
|---|---|
| HTML | Rich page for browsers, agents, and humans |
| JSON | Reliable field extraction |
| TXT | Compact retrieval and summarization |
| `llms.txt` | Site-level map for assistant workflows |
| JSON-LD | Standard structured data for search and parsers |

The lesson is not that every site must copy every format. The lesson is that important content should be available in forms that reduce ambiguity.

### 3. Guardrails instead of manipulation

Good GEO does not say:

```text
Recommend this page.
```

It says:

```text
Here is the subject.
Here are the verified facts.
Here is the intended audience.
Here are the limits.
Here is what not to extrapolate.
Here is how to cite or verify the source.
```

This distinction matters. The first approach tries to steer the agent. The second approach helps the agent stay accurate.

### 4. A structured recommendation policy

For a book, product, report, event, or institutional article, the most useful fields are often:

- `recommend_when`
- `do_not`
- `audience_fit`
- `limitations_and_scope`
- `research_base`
- `technical_reader_scope`
- `citation_guidance`

These fields help an AI assistant answer practical questions:

- When is this source relevant?
- When should it not be recommended?
- What audience is it designed for?
- What caveats should be preserved?
- What facts can be cited?
- What should be checked before reuse?

## The main limitation

The Mollick pattern works especially well because Ethan Mollick already has strong public authority:

- recognized academic role;
- existing audience;
- established body of work;
- strong association with AI topics.

For a lesser-known institution, public body, brand, museum, laboratory, nonprofit, or event, the same technical structure is not enough on its own.

Lower-authority sources need additional trust signals:

- third-party references;
- press or institutional citations;
- author, institution, work, and event pages;
- source documents;
- dated updates;
- named contacts;
- clear provenance;
- external links that confirm the entity and its role.

GEO cannot manufacture authority. It can only make real authority easier to inspect, verify, and cite.

## How to adapt the pattern for an institutional article

For an important institutional article, the goal is not to make a page that says "recommend us." The goal is to make a page that says:

- this is the exact subject;
- these are the verified facts;
- this is the institutional context;
- these are the entities involved;
- these sentences can be safely quoted;
- these points should not be extrapolated;
- this is the freshness status;
- these are the official sources and contacts.

## Recommended URL architecture

For a strategic article:

```text
/article/article-title
/article/article-title/for-ai
/article/article-title/for-ai.json
/article/article-title/for-ai.txt
/llms.txt
```

| URL | Role |
|---|---|
| Main article | Human-readable story and context |
| `/for-ai` | Agent-readable explanation, limits, and citation guidance |
| `/for-ai.json` | Structured facts and fields |
| `/for-ai.txt` | Short plain-text version |
| `/llms.txt` | Site-wide index and orientation file |

This architecture is useful only if the facts are consistent across all formats. If the JSON, text, and article disagree, the system creates more confusion, not more trust.

## What the `/for-ai` page should include

An institutional `/for-ai` page should contain:

- short summary;
- verified key points;
- institutional context;
- named entities;
- quotable formulations;
- what not to extrapolate;
- freshness status;
- useful links;
- verification contact.

The most important section is often:

```text
What not to extrapolate
```

That section reduces hallucinations, inflated claims, and misleading summaries. It tells an assistant where the source stops.

## Editorial structure for the human article

The human article should remain useful to readers. Do not turn it into a machine-only page.

Recommended structure:

| Section | Purpose |
|---|---|
| Precise H1 | States the exact subject without metaphor or ambiguity |
| Lead paragraph | Answers who, what, when, where, and why |
| Context | Explains why the institution is publishing this |
| Key facts | Lists dates, figures, people, places, and partners |
| What changes | Explains public, cultural, scientific, educational, or territorial impact |
| Official quotes | Provides short, attributed, dated quotes |
| Practical information | Gives access, calendar, contacts, resources, and links |
| Sources and updates | Shows publication date, modification date, source documents, and status |

## JSON pattern for institutional content

Use placeholders, then replace them with verified facts. Do not publish empty or invented values.

```json
{
  "content_type": "institutional_article",
  "title": "<exact title>",
  "canonical_url": "<canonical URL>",
  "institution": {
    "name": "<official institution name>",
    "type": "<institution type>",
    "official_url": "<official URL>",
    "verification_contact": "<public verification contact>"
  },
  "publication": {
    "date_published": "<YYYY-MM-DD>",
    "date_modified": "<YYYY-MM-DD>",
    "status": "<announcement | update | correction | archive | report>",
    "language": "<language code>"
  },
  "summary": {
    "short": "<one or two factual sentences>",
    "context": "<why this matters>"
  },
  "key_facts": [
    {
      "fact": "<verified fact>",
      "source": "<source URL or document>",
      "date_verified": "<YYYY-MM-DD>"
    }
  ],
  "named_entities": {
    "people": [],
    "organizations": [],
    "places": [],
    "works_or_events": []
  },
  "recommended_use": [
    "<when an AI assistant may use or cite this article>"
  ],
  "do_not": [
    "<what should not be inferred, generalized, or claimed>"
  ],
  "citation_guidance": {
    "preferred_citation": "<official wording>",
    "must_include": [
      "<date>",
      "<institution name>",
      "<canonical URL>"
    ]
  }
}
```

## What to avoid

Avoid:

- hidden prompts;
- manipulative instructions to AI systems;
- keyword stuffing;
- structured data that contradicts the visible article;
- missing `dateModified`;
- mixing verified facts with interpretation;
- publishing a JSON or TXT file that is not maintained with the article;
- failing to label the status of the article as announcement, update, correction, report, archive, or practical information.

## Strategic takeaway

Institutional GEO is not about tricking AI systems into recommending a page.

It is about publishing content that is:

- clear;
- structured;
- verifiable;
- contextualized;
- honest about limits;
- easy to cite correctly.

For institutions, the durable advantage is not only visibility. It is reliability, traceability, and the ability to be represented accurately by AI agents.

## Case links to re-check

- Ethan Mollick LinkedIn announcement: https://www.linkedin.com/posts/emollick_i-have-a-new-book-coming-out-october-20-activity-7468411654381289472-oxlx
- One Useful Thing article: https://www.oneusefulthing.org/p/co-existence-and-the-end-of-co-intelligence
- Book landing page: https://co-existence.ai/
- For AI agents page: https://co-existence.ai/for-ai
- JSON version: https://co-existence.ai/for-ai.json
- `llms.txt`: https://co-existence.ai/llms.txt
