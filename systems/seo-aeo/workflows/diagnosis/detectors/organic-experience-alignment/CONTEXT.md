---
id: seo.diagnosis.detector.organic-experience-alignment
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
Detect when organic acquisition intent, ranking destination, search promise, or landing experience is misaligned and distinguish SEO acquisition problems from broader persuasion/journey friction.

## Business Outcome
Identify the real owner/mechanism of an organic conversion gap without forcing non-SEO problems into SEO Opportunities or cross-domain routing machinery.

## Run When
Use when fresh relevant organic/conversion observations exist and the user/model needs to diagnose an **organic conversion/experience alignment gap**. If an external runtime invokes this from saved monitoring intent, that runtime owns the schedule. Do not create an Opportunity until evidence and model judgment support one.

## Process
1. [HYBRID] Select sufficiently decision-relevant organic segments and relate landing page, query/intent, audience/market, conversion events, and downstream quality/value where available.
2. [HYBRID] Compare against appropriate page/intent/market baselines rather than a sitewide conversion rate.
3. [AI] Inspect Offer match, CTA, form/checkout usability, trust/reputation, page speed, device issues, information completeness, and traffic-intent quality as possible mechanisms.
4. [AI] Distinguish SEO acquisition/intent mismatch from broader Marketing, Customer Optimization, product, sales, or operational causes.
5. [AI] Create/update an SEO Opportunity only when SEO owns a materially supported intervention. Otherwise state the likely non-SEO mechanism and let the active model/user use the relevant operating knowledge directly.
6. [HYBRID] Define the downstream business-outcome and guardrail evidence needed after any intervention.
7. [AI] Create a WorkRequest only if a genuine durable handoff to another owner must survive the current session; do not route ordinary model continuation through AURA.

## Verification
- Search intent, landing experience, persuasion, journey friction, and downstream business value remain distinct.
- No cross-domain Opportunity/WorkRequest is manufactured merely to encode model decomposition.
