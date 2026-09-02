---
id: seo.execution.on-page.organic-conversion-alignment
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- conversion CRM revenue best available proxy
---
# Organic Experience & Conversion Alignment

## Purpose
Determine whether organic acquisition intent, search/result promise, destination choice, and landing experience align well enough to create the intended user and business outcome—and improve the part SEO/AEO can actually influence.

## Business Outcome
Increase useful progression from organic discovery without forcing broader marketing, product, sales, or customer-journey problems into SEO or optimizing conversion at the expense of search-task satisfaction.

## Run When
Use when important organic visitors appear to land on the wrong experience, fail to progress at an unexpected rate, or when the user wants to improve the relationship between discovery intent and the destination experience.

## Process
1. [HYBRID] Define the relevant organic segment and intended outcome using query/prompt intent, landing page, audience/market, awareness/readiness stage, conversion event, and downstream quality/value where available. Compare against an appropriate page/intent/market baseline rather than a generic sitewide conversion rate.
2. [AI] Check whether the acquisition promise and destination are aligned: does the ranking/cited page answer the task that brought the visitor, match the Offer and audience, provide the information needed at that stage, and create a reasonable next path?
3. [HYBRID] Examine only mechanisms that can materially explain the gap: CTA relevance/visibility, proof/trust/reputation, pricing/contact expectations, forms/checkout, mobile usability, performance, information completeness, offer-message consistency, post-click fulfillment, and traffic-intent quality.
4. [AI] Distinguish an SEO/AEO-owned mechanism—such as query/page mismatch, wrong destination, insufficient task fulfillment, discovery promise mismatch, or organic-specific pathing—from broader persuasion, Customer Optimization, product, sales, operational, or measurement causes. When another domain owns the real problem, state that plainly and use the relevant operating knowledge directly rather than manufacturing a routing object.
5. [AI] If organic alignment is the controllable problem, choose the smallest useful change. Match the next action to readiness: an early informational visitor may need deeper education or comparison paths rather than a forced bottom-funnel CTA; a high-intent visitor may need clearer proof, terms, or actionability.
6. [HYBRID] Apply justified changes through the actual site/content controls available, preserving customer-facing truth and the original search task. Do not sacrifice answer quality or misrepresent the page merely to increase a conversion metric.
7. [HYBRID] Verify measurement before interpreting before/after movement, then evaluate both the intended conversion/progression signal and guardrails such as traffic quality, search engagement/task fulfillment, downstream value, or other evidence relevant to the change.
8. [AI] Preserve an SEO Opportunity only when a materially valuable SEO-owned problem remains. Create a durable WorkRequest only when a real handoff across people/models/sessions genuinely needs to survive—not to represent ordinary model decomposition.

## Verification
- Search intent, result promise, landing experience, persuasion, journey friction, and downstream business value remain distinguishable.
- Conversion changes do not degrade truthful task fulfillment or force premature commercial action.
- Non-SEO causes are not relabeled as SEO merely because the visitor arrived organically.
- Outcome claims distinguish measured conversion/progression change from inferred business impact.
