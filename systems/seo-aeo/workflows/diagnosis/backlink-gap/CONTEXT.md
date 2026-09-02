---
id: seo.diagnosis.backlink-gap
type: workflow
owner_system: seo-aeo
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
writes:
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
---
# Authority & Backlink Gap

## Purpose
Identify relevant authority relationships, references, or assets present in the competitor/topic ecosystem that the organization could legitimately earn or create value for.

## Business Outcome
Find evidence-backed authority gaps worth addressing without optimizing for raw link volume or turning every competitor reference into an outreach task.

## Run When
Use when current backlink, referring-domain, mention, or ecosystem evidence can help answer whether a material authority gap exists.

## Process
1. [HYBRID] Compare owned and relevant competitor/topic-ecosystem referring sources at the topic, page, audience, and business-context level rather than only domain totals.
2. [AI] Exclude spam, irrelevant, manipulative, paid-only, or non-comparable sources and determine what legitimate audience value, relationship, resource, expertise, evidence, or context appears to explain meaningful references.
3. [AI] Decide whether the missing relationship points to an existing owned Asset/value proposition, a genuine prerequisite asset/evidence need, a specific acquisition method, a partnership/reputation/local opportunity, or no worthwhile action.
4. [AI] Judge audience/business relevance, realistic attainability, reputational/compliance constraints, material resource cost, and expected strategic value without fabricating a precise success probability.
5. [AI] Preserve an Authority Opportunity only when evidence supports a legitimate, valuable, plausibly attainable intervention. The active model/user chooses the acquisition method from the real context rather than following an automatic route.
6. [HYBRID] Reject approaches whose useful mechanism depends on deception, manipulative link schemes, undisclosed paid placement, or another practice contrary to actual legal/platform/organizational constraints.

## Verification
- Relevance, legitimacy, audience value, and business fit matter more than raw link counts or domain metrics.
- Competitor possession of a link/reference does not by itself establish that the organization should pursue it.
- Outreach/source provenance and applicable communication/compliance constraints remain available when relevant.
