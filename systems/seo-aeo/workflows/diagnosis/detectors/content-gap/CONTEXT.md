---
id: seo.diagnosis.detectors.content-gap
type: detector
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
- records topic intent evidence
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Content / Information Gap Detector

## Purpose
Find high-value buyer needs or answer components not adequately served by an owned Asset.

## Business Outcome
Identify useful information gaps with a real audience/business pathway while avoiding keyword-volume-driven content production and unnecessary Asset fragmentation.

## Run When
Use when fresh relevant demand/content observations exist and the user/model needs to diagnose a **content / information gap**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Relate Demand clusters, journey stages, competitor/answer-source coverage, owned Asset inventory, support/sales questions, and performance to the current business question.
2. [AI] Identify absent destinations, incomplete sections/evidence, obsolete information, or formats that users actually need.
3. [AI] Decide whether improving an existing Asset is better than creating a new one, accounting for fragmentation and cannibalization risk.
4. [AI] Define the missing user outcome/information rather than a target word count or generic keyword brief.
5. [AI] Create/update a content/on-page Opportunity only when the gap has a credible audience/business pathway and evidence.
6. [HYBRID] Reject content whose only justification is keyword volume without audience/business value.

## Verification
- Demand evidence, user need, existing coverage, and business relevance remain separately inspectable.
- The detector does not route production or require a new Asset merely because a gap exists.
