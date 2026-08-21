---
id: seo.diagnosis.detectors.serp-feature
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
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# SERP / Discovery Feature Opportunity Detector

## Purpose
Find valuable result formats or surface features the brand could legitimately qualify for or better serve.

## Business Outcome
Detect and explain material serp / discovery feature opportunity early enough to prioritize the right SEO/AEO response and protect or improve valuable organic discovery.
## Run When
Run after fresh relevant observations are ingested, on the configured opportunity-scan cadence, or when an operator explicitly asks to diagnose **serp / discovery feature opportunity**. Do not create an Opportunity until the detector's evidence threshold is met.

## Process
1. [AI] Observe high-value result ecosystems and identify recurring local, image, video, product, rich-result, discussion, news, or other feature types.
2. [HYBRID] Verify the feature aligns with actual user intent and the brand has or can create eligible/useful content/data.
3. [HYBRID] Inspect current owned eligibility, structured information, media, product/local data, and competitor examples.
4. [HYBRID] Route to the relevant content, media, structured-data, local, product, or technical playbook.
5. [HYBRID] Create an Opportunity with feature-specific evidence rather than treating feature ownership as guaranteed.
6. [HYBRID] Define SEO monitoring and Core OutcomeEvaluation of feature presence and business effect after any later change.


