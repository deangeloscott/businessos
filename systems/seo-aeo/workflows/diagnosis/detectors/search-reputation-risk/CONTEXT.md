---
id: seo.diagnosis.detector.search-reputation-risk
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
- Observation
writes:
- Opportunity
context:
- AudienceSegment
- Market
- Objective
- Offer
evidence_inputs:
- review mention reputation response history
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Search Reputation Risk Detector

## Purpose
Detect reputation/review conditions that materially affect organic/local discovery or search-result trust without owning broad sentiment/reputation management.

## Business Outcome
Identify search-relevant reputation risks and the actual underlying mechanism without treating operational complaints as an SEO problem or creating automatic reputation workflows.

## Run When
Use when fresh relevant reputation/search observations exist and the user/model needs to diagnose a **search reputation risk/gap**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Compare rating/review volume/recency/themes/response coverage and third-party profile accuracy by relevant location/product/source.
2. [HYBRID] Relate search/local/AI observations to where reputation evidence is actually visible in the decision path.
3. [AI] Determine whether the likely problem is insufficient authentic review generation, response backlog, an operational complaint pattern, inaccurate profile information, misinformation, or another mechanism.
4. [AI] When the root cause belongs outside SEO, state that plainly and let the active model/user continue with the appropriate business method; create a durable handoff only if another owner genuinely needs one.
5. [AI] Create/update an ethical SEO reputation Opportunity only when a search/discovery intervention is materially supported by evidence.
6. [HYBRID] Define later evaluation using relevant reputation/trust and business-choice evidence rather than review count alone.

## Verification
- Search visibility, reputation evidence, operational root cause, and business impact remain distinct.
- No synthetic review/manipulation tactic is recommended merely to improve a metric.
