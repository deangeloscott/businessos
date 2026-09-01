---
id: seo.diagnosis.detectors.traffic-decay
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
- traffic time series landing page dimensions conversion
updates:
  Opportunity:
  - diagnosis
  - evidence_links
  - priority_assessment
  - recommended_intervention_types
---
# Organic Traffic Decay Detector

## Purpose
Separate material traffic decline into demand, visibility, CTR/result, analytics, conversion-path, and technical explanations.

## Business Outcome
Identify the real mechanism behind valuable organic traffic loss without assuming rank decline or creating a generic traffic-recovery task.

## Run When
Use when fresh relevant traffic/search observations exist and the user/model needs to diagnose **organic traffic decay**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Identify material decline in qualified organic sessions/users/landing-page visits using comparison windows and seasonality controls appropriate to the evidence.
2. [HYBRID] Check analytics/measurement health relevant to this diagnosis before treating the movement as real; do not create a separate provider-health lifecycle.
3. [HYBRID] Decompose traffic using available demand, visibility/position, click behavior, index/access, and landing-path evidence at the most useful granularity.
4. [HYBRID] Compare new/returning, device, geography, landing pages, branded/nonbrand, and conversion quality only where those dimensions materially help.
5. [AI] Judge the supported primary contributors: demand decline, rank decline, CTR/SERP change, deindex/technical, tracking change, migration, another business change, or unknown.
6. [AI] Create/update a targeted Opportunity or Incident only when severity/business value and a plausible controllable mechanism are supported; otherwise preserve uncertainty and useful evidence.

## Verification
- Reconcile search visibility, analytics, and conversion evidence before concluding the site lost demand or rank.
