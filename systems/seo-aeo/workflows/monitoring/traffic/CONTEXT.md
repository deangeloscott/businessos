---
id: seo.monitoring.traffic
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
writes:
- MetricObservation
- Opportunity
- Incident
- SEOAssetState
evidence_inputs:
- traffic time series landing page dimensions conversion
updates:
  SEOAssetState:
  - organic_performance
---
# Organic Traffic Monitoring

## Purpose
Review material changes in qualified organic site/app traffic and landing behavior without treating analytics movement as self-explanatory.

## Business Outcome
Keep organic traffic evidence current enough to distinguish meaningful acquisition changes from demand, seasonality, tracking, search visibility, and downstream-quality effects.

## Run When
Use for a bounded organic-traffic check when the user requests it, saved monitoring intent indicates another review would be useful, or a material site/search/business change warrants comparison. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve current organic sessions/users/landing-page and relevant quality/business-action evidence from the strongest available first-party measurement sources.
2. [HYBRID] Segment by Asset, topic, market, device, new/returning, brand/nonbrand, and source surface only where those dimensions are trustworthy and decision-relevant.
3. [HYBRID] Compare appropriate rolling/prior/YoY baselines while accounting for seasonality and known campaign/site/business changes.
4. [HYBRID] Check measurement/data quality relevant to the observed movement before concluding that demand, visibility, or traffic actually changed. Do not create a separate AURA provider-health state machine.
5. [AI] Decide whether a material unexplained loss/gain warrants deeper traffic-decay/root-cause diagnosis, an Opportunity, attribution review, Learning, or no additional durable state. Monitoring does not route these automatically.
6. [HYBRID] Preserve useful MetricObservation/SEOAssetState evidence and keep quality/conversion visible so raw visitor growth cannot hide worse business outcomes.

## Verification
- Reconcile search visibility, analytics, and conversion evidence before concluding the site lost demand or rank.
- Measurement health is assessed only as evidence quality for the current question, not as an AURA-owned provider/runtime subsystem.
- Recurring collection remains owned by the active harness/runtime.
