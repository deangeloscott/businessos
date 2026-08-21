---
id: seo.diagnosis.detector.organic-experience-alignment
type: detector
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- OrganicDemandUnit
- SEOAssetState
- Asset
- OrganicCompetitorState
- Competitor
- MetricObservation
- ChangeEvent
- Observation
writes:
- Opportunity
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.serp.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- conversion CRM revenue best available proxy
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Organic Experience Alignment Detector

## Purpose
Detect when organic acquisition intent, ranking destination, search promise, or landing experience is misaligned; route general persuasion or journey friction to the correct OS.

## Business Outcome
Detect and explain material organic experience alignment early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **conversion gap**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [DETERMINISTIC] Select sufficient-volume/value organic segments and join landing page, query/intent, audience/market, conversion events, and downstream quality/value where available.
2. [HYBRID] Compare against appropriate page/intent/market baselines rather than sitewide conversion rate.
3. [HYBRID] Inspect offer match, CTA, form/checkout usability, trust/reputation, page speed, device issues, information completeness, and traffic intent quality.
4. [HYBRID] Separate SEO acquisition mismatch from broader CRO/product/sales issues.
5. [HYBRID] Create an Opportunity routed to on-page/content/technical or an external business/CRO workflow as appropriate.
6. [HYBRID] Define the downstream business-outcome and guardrail measurements required after any intervention.
7. [AI] If the primary cause is offer/message persuasion rather than organic intent mapping, route a WorkRequest or relevance signal to Marketing Synthesis.
8. [AI] If the primary cause is form/checkout/sales/onboarding/process friction, route to Customer Optimization rather than retaining an SEO Opportunity.


