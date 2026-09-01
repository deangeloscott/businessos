---
id: seo.monitoring.backlinks
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
- backlink/referring-domain/mention evidence and prospect records
updates:
  SEOAssetState:
  - organic_performance
---
# Backlink and Mention Monitoring

## Purpose
Review meaningful new, lost, or changed external references and authority signals without treating link-provider noise as organizational truth.

## Business Outcome
Keep authority/mention understanding current enough to identify real losses, gains, or opportunities while measuring relevance and business value rather than raw volume.

## Run When
Use for a bounded backlink/mention check when the user requests it, saved monitoring intent indicates another review would be useful, or a material site/PR/market change warrants re-observation. Any recurring execution belongs to the active harness/runtime.

## Process
1. [INTEGRATION] Retrieve current link/mention evidence from appropriate available sources and preserve the exact source/target/time context needed for comparison.
2. [HYBRID] Verify significant new/lost references and distinguish provider noise, redirects, site migrations, spam, and true editorial changes.
3. [HYBRID] Attribute earned links/mentions to outreach, PR, Assets, or other causes only when evidence supports that relationship.
4. [AI] Judge whether a valuable loss, unlinked mention, competitor gap, harmful anomaly, or authority pattern is materially worth deeper work. Relevant authority/incident playbooks may be useful methods; monitoring does not route them automatically.
5. [AI] Assess source relevance/quality for the current fact type without treating synthetic authority scores as truth.
6. [HYBRID] Preserve useful measurement/state and compare referral/business value and topic relevance alongside counts. Create an Opportunity or Incident only when that durable organizational meaning is genuinely justified.

## Verification
- Target relevance and legitimacy matter more than raw link volume.
- Material observations remain traceable to actual link/mention evidence.
- Saved monitoring intent never claims a background checker exists; runtime owns recurring execution.
