---
id: seo.monitoring.search-reputation
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
- review mention reputation response history
updates:
  SEOAssetState:
  - organic_performance
---
# Reputation Monitoring

## Purpose
Review material review, rating, sentiment, profile, and high-visibility brand-claim changes that can affect organic discovery and customer choice.

## Business Outcome
Keep search-reputation evidence current enough to identify meaningful trust/visibility changes without turning public conversation into an automatic incident or response workflow.

## Run When
Use for a bounded reputation check when the user requests it, saved monitoring intent indicates another review would be useful, or a material brand/local/search event warrants reinspection. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve current review, mention, profile, and relevant response-history evidence for the scoped locations/products/sources.
2. [AI] Identify material rating shifts, review spikes/drops, recurring negative themes, response backlog, misinformation, impersonation, or unusually high-reach exposure while keeping direct evidence separate from inference.
3. [AI] Assess business/search impact, reach, severity, confidence, and relevant privacy/legal constraints.
4. [AI] Decide whether the evidence warrants normal reputation work, an Incident, an Opportunity, deeper customer research, or no additional durable state. Monitoring does not route these outcomes automatically.
5. [HYBRID] Relate trust/reputation changes to local/search/AEO discovery and customer choice only when evidence supports the connection.
6. [HYBRID] Preserve useful state/evidence and, on later reviews, compare resolution/recurrence when that history materially helps decisions.

## Verification
- Review prevalence, sentiment interpretation, search visibility, and business impact remain distinct.
- Public availability does not itself establish permission for promotional reuse of a person's statement/identity.
- Any recurring collection is external-runtime behavior, not AURA state.
