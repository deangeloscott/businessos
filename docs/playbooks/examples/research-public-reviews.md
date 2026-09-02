# Example Playbook Flow: Research Public Reviews and Conversations

This example shows how a capable AI can use AURA memory and operating knowledge for one user-level request. It is **not a second set of rules**. The linked contracts remain authoritative.

## What the user can say

> “Research what customers are saying about us and our competitors. Find the biggest complaints, praise, objections, and useful customer language.”

The user does not need to name websites, tools, folders, contracts, or AURA systems unless they want to.

## How the work can proceed

### 1. Define what the research needs to answer

The AI uses relevant organizational context, the market, product/service, competitors, time window, and current decision to judge what evidence is worth collecting. It should not search every possible source just because a source exists.

### 2. Find the right review and conversation sources

Depending on the business, useful sources might include Google Business Profile, Trustpilot, Yelp, Reddit, industry review sites, social platforms, marketplaces, app stores, owned reviews, support data, or other relevant public/first-party sources. These are examples, not a fixed checklist.

### 3. Collect allowed source evidence

For each useful review or public conversation, the active model/harness first opens or retrieves the underlying item. A search result or URL can help find evidence, but it is not enough by itself for an important supported conclusion. Preserve the information that is actually available and allowed, such as:

- review/comment text
- rating
- date or timestamp
- source/platform
- page or permalink
- product, service, location, or thread context
- public author label only when it is needed
- useful public context such as thread or engagement information

### 4. Preserve a screenshot or snapshot when it adds value

Useful source text and metadata should normally remain searchable and checkable later. A screenshot is extra preservation, not a requirement for every review. When the source permits it and visual context, proof value, or page-change risk matters, the active model/harness can capture the original page/review and link it to the same source evidence.

### 5. Remove duplicates

Remove exact duplicates, syndicated copies, reposts, and repeated captures while keeping genuinely different people or meaningful follow-up comments separate.

### 6. Analyze each piece of evidence

The AI can extract:

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

Direct customer statements stay separate from interpretation. If the original evidence was not preserved or cannot be reliably revisited, the interpretation stays provisional instead of being marked as fully supported.

### 7. Look for patterns across the evidence

Compare reviews and conversations to find recurring themes, emerging issues, differences between products/locations/segments, and contradictions with other evidence such as interviews, support conversations, or sales calls.

### 8. Save reusable business knowledge

Useful evidence can become linked AURA objects instead of disappearing inside one chat:

- **SourceRecord** — where the evidence came from
- **Asset** — a screenshot or snapshot when one was captured
- **Observation** — what was directly observed
- **Insight** — a supported pattern or conclusion
- **ProofRecord** — reusable proof/testimonial evidence when the claim and permission rules support it

### 9. Reuse useful findings directly

One finding can matter to several kinds of work without being copied into separate truth stores or routed through internal AURA services. The active model can apply the same supported evidence wherever it is relevant:

- a repeated complaint can inform customer understanding
- a competitor complaint can inform competitor analysis
- checkout or service friction can inform customer-journey improvement
- strong customer language can inform marketing
- supported proof can be reused in content when relevant
- supported proof can be reused in SEO/AEO when relevant

### 10. Stop when more collection is unlikely to change the decision

Collect enough evidence to answer the current question responsibly. Do not keep researching simply because more data is available. If the organization wants ongoing monitoring, AURA may preserve the monitoring intent and prior evidence; the active host/runtime owns any actual recurring schedule or future check.

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

## Authoritative AURA playbooks

- [Review Intelligence](../../../systems/customer-intelligence/workflows/evidence-collection/reviews/CONTEXT.md) — `customer.evidence-collection.reviews`
- [Public Conversation Collection](../../../systems/customer-intelligence/workflows/evidence-collection/public-conversation/CONTEXT.md) — `customer.evidence-collection.public-conversation`
- [Before/After and Proof Extraction](../../../systems/customer-intelligence/workflows/analysis/before-after-proof/CONTEXT.md) — `customer.analysis.before-after-proof`
- [Register Reusable Proof](../../../core/workflows/intelligence/register-proof/CONTEXT.md) — `core.intelligence.register-proof`

These contracts define the actual operating knowledge. This page only explains the flow in simpler language.
