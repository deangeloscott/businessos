---
id: seo.monitoring.organic-outcome-alignment
type: playbook
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
capabilities:
  required:
  - analytics.read
  optional:
  - search.performance.read
  - search.rank.read
  - search.index.inspect
  - backlink.read
  - ai_answer.observe
  - crawler.run
  - local_profile.read
evidence_inputs:
- conversion CRM revenue best available proxy
updates:
  SEOAssetState:
  - organic_performance
---
# Organic Conversion and Value Monitoring

## Purpose
Review downstream business outcomes from organic discovery and identify material quality/value changes without treating traffic as the outcome.

## Business Outcome
Keep organic business-value evidence current enough to distinguish valuable growth from low-quality traffic or changing conversion/economic conditions.

## Run When
Use for a bounded organic-outcome review when the user requests it, saved monitoring intent indicates another check would be useful, or material organic/business changes warrant comparison. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve the strongest available conversion, lead, opportunity, order, revenue, profit, or justified proxy evidence from the relevant first-party systems.
2. [HYBRID] Relate outcomes to organic landing/query/content/market paths while preserving attribution limitations and unresolved identity gaps.
3. [HYBRID] Compare conversion rate, qualified rate, value per visit/lead, and total value over decision-appropriate windows.
4. [AI] Identify traffic growth with value decline, lead-quality deterioration, offer/market/capacity issues, tracking changes, or other plausible explanations without assuming SEO caused the movement.
5. [AI] Decide whether the evidence warrants SEO conversion-gap diagnosis, a different business-domain investigation, an Opportunity, or no additional durable state. Monitoring does not route causes to domains automatically.
6. [HYBRID] Preserve useful MetricObservation/SEOAssetState evidence and update confidence/prioritization only to the precision supported by observed outcomes.

## Verification
- Organic discovery, attribution, conversion quality, and financial outcome remain distinct.
- Missing or weak attribution remains explicit rather than being converted to deterministic SEO credit.
- Any next method is selected by the active model/user, not by a monitoring lifecycle.
