# Example Playbook Flow: Research Public Reviews and Conversations

This example shows what a user-level request can turn into inside BusinessOS. It is **not a second set of rules**. The linked contracts remain authoritative.

## What the user can say

> “Research what customers are saying about us and our competitors. Find the biggest complaints, praise, objections, and useful customer language.”

The user does not need to name websites, tools, folders, contracts, or BusinessOS systems unless they want to.

## What BusinessOS does

### 1. Define what the research needs to answer

BusinessOS uses the business, market, product/service, competitors, time window, and current decision to decide what evidence is worth collecting. It should not search every possible source just because a source exists.

### 2. Find the right review and conversation sources

Depending on the business, useful sources might include Google Business Profile, Trustpilot, Yelp, Reddit, industry review sites, social platforms, marketplaces, app stores, owned reviews, support data, or other relevant public/first-party sources. These are examples, not a fixed checklist.

### 3. Collect allowed source evidence

For each useful review or public conversation, BusinessOS first opens or retrieves the underlying item. A search result or URL can help find evidence, but it is not enough by itself for an important supported conclusion. BusinessOS preserves the information that is actually available and allowed, such as:

- review/comment text
- rating
- date or timestamp
- source/platform
- page or permalink
- product, service, location, or thread context
- public author label only when it is needed
- useful public context such as thread or engagement information

### 4. Preserve a screenshot or snapshot when it adds value

BusinessOS normally keeps the useful source text and metadata so the evidence can be searched and checked later. A screenshot is extra preservation, not a requirement for every review. When the source permits it and visual context, proof value, or page change risk matters, BusinessOS can capture the original page/review as a screenshot or snapshot and link it to the same source record.

### 5. Remove duplicates

BusinessOS removes exact duplicates, syndicated copies, reposts, and repeated captures while keeping genuinely different people or meaningful follow-up comments separate.

### 6. Analyze each piece of evidence

BusinessOS can extract:

- praise
- complaints
- pain points
- desired outcomes
- expectations
- objections
- comparisons
- buying or switching signals
- use cases
- before/after statements
- feature or service requests
- exact customer wording
- sentiment about specific parts of the experience

Direct customer statements stay separate from BusinessOS interpretation. If the original evidence was not preserved or cannot be reliably revisited, the interpretation stays provisional instead of being marked as fully supported.

### 7. Look for patterns across the evidence

BusinessOS compares reviews and conversations to find recurring themes, emerging issues, differences between products/locations/segments, and contradictions with other evidence such as interviews, support conversations, or sales calls.

### 8. Save reusable business knowledge

Useful evidence can become linked BusinessOS objects instead of disappearing inside one chat:

- **SourceRecord** — where the evidence came from
- **Asset** — a screenshot or snapshot when one was captured
- **Observation** — what was directly observed
- **Insight** — a supported pattern or conclusion
- **ProofRecord** — reusable proof/testimonial evidence when the claim and permission rules support it

### 9. Route useful findings to the right next work

One review can matter in several places without being copied into separate truth stores. BusinessOS routes a finding only to areas installed in this copy and only when the finding is relevant.

- a repeated complaint can inform **Customer Intelligence**
- a competitor complaint can inform **Competitor Intelligence**
- checkout or service friction can inform **Customer Optimization**
- strong customer language can inform **Marketing Synthesis**
- supported proof can be reused in **Content Synthesis** when relevant
- supported proof can be reused in **SEO/AEO** when relevant

### 10. Stop when more collection is unlikely to change the decision

BusinessOS should collect enough evidence to answer the current question responsibly. It should not keep scraping or researching simply because more data is available. If the job needs ongoing monitoring, it can preserve what was checked and later look for meaningful changes.

## What the user should get back

The final result should be useful to a business person, not just a pile of saved reviews. A good result could include:

- the most important themes
- what customers repeatedly praise or dislike
- useful exact customer language
- differences between the business and competitors
- important uncertainties or evidence gaps
- links/citations back to the source evidence
- saved screenshots where useful and allowed
- the best next action supported by the evidence

## Authoritative BusinessOS playbooks

- [Review Intelligence](../../../systems/customer-intelligence/contracts/evidence-collection/reviews/CONTEXT.md) — `customer.evidence-collection.reviews`
- [Public Conversation Collection](../../../systems/customer-intelligence/contracts/evidence-collection/public-conversation/CONTEXT.md) — `customer.evidence-collection.public-conversation`
- [Before/After and Proof Extraction](../../../systems/customer-intelligence/contracts/analysis/before-after-proof/CONTEXT.md) — `customer.analysis.before-after-proof`
- [Register Reusable Proof](../../../core/contracts/intelligence/register-proof/CONTEXT.md) — `core.intelligence.register-proof`

These contracts define the actual operating rules. This page only explains the flow in simpler language.
