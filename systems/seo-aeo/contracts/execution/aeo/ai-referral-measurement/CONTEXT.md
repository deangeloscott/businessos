---
id: seo.execution.aeo.ai-referral-measurement
type: playbook
version: 1.1.0
owner_system: seo-aeo
risk: low
autonomy_ceiling: 4
reads:
- SEOAssetState
- Asset
- Observation
writes:
- SEOAssetState
- ChangeEvent
- Asset
capabilities:
  required:
  - ai_answer.observe
  optional:
  - research.web.read
  - cms.page.read
  - cms.page.update
  - analytics.read
evidence_inputs:
- prompt/question observations, answer text, citations, mentions, and competing sources
- conversion CRM revenue best available proxy
---
# AI Referral and Assisted Conversion Measurement

## Purpose
Measure observable visits and business outcomes from answer surfaces without treating unobservable influence as zero.

## Business Outcome
Improve valuable organic discovery through ai referral and assisted conversion measurement, with a clear SEO/AEO mechanism and connection to the active business Objective.

## Run When
Run only when an approved Action Packet routes to **AI Referral and Assisted Conversion Measurement**, or when an authorized incident response requires it.

## Process
1. [AI] Define known referrer/source patterns and platform-specific tracking capabilities from AnalyticsProvider.
2. [DETERMINISTIC] Normalize sessions/users/events/leads/revenue attributed to recognizable AI/answer referrals and preserve attribution model.
3. [HYBRID] Separate direct referral from assisted/influenced outcomes where CRM/survey/first-party evidence exists.
4. [DETERMINISTIC] Join referral performance with prompt/citation observations cautiously; do not claim causal attribution from temporal coincidence alone.
5. [HYBRID] Report conversion rate, value, landing assets, new/returning behavior, and downstream assisted outcomes where available.
6. [HYBRID] Use proxy visibility metrics only when direct value cannot be observed and label them explicitly as proxies.


