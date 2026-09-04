---
id: seo.monitoring.competitors
type: workflow
owner_system: seo-aeo
reads:
- SEOAssetState
- Asset
- MetricObservation
- ChangeEvent
- Opportunity
- Observation
- OrganicCompetitorState
- Competitor
writes:
- MetricObservation
- Opportunity
- Incident
- SEOAssetState
updates:
  SEOAssetState:
  - organic_performance
---
# Competitor Monitoring

## Purpose
Review business/search/answer competitor movements that may materially affect organic-discovery decisions without duplicating Competitor Intelligence or creating an SEO dispatch loop.

## Business Outcome
Keep organic competitive context current enough to recognize meaningful shifts while separating SEO-visible movement from broader competitor strategy and proven effectiveness.

## Run When
Use for a bounded organic-competitor check when the user requests it, saved monitoring intent indicates another check would be useful, or evidence suggests a material competitive/search change. Any recurring execution belongs to the active harness/runtime.

## Process
1. [HYBRID] Retrieve decision-relevant visibility, major assets, answer citations, backlinks/mentions, local/reputation, offers, and meaningful site changes for prioritized organic competitors using current evidence available to the harness.
2. [AI] Identify sustained gains/losses, new assets/formats, migrations, campaigns, authority events, or category/positioning changes while keeping observation separate from inferred cause.
3. [AI] Distinguish industry/search-surface-wide changes from competitor-specific movement.
4. [AI] Judge relevance to owned organic opportunities only when the actual market, audience, query/task, asset, offer, or discovery surface makes the comparison meaningful.
5. [AI] Novel tactics or hypotheses may be considered through SEO ecosystem intelligence/domain Learning or Competitor Intelligence when useful; monitoring does not send or route them automatically.
6. [HYBRID] Update OrganicCompetitorState/measurement evidence when durable and preserve material observations. Create a separate Opportunity/Incident only when the evidence actually justifies that organizational meaning.

## Verification
- Organic competitor movement, inferred strategy, and evidence of effectiveness remain distinct.
- Cross-domain competitor meaning is not duplicated merely because SEO observed a change.
- Any recurring check is runtime-owned; AURA stores only useful monitoring intent/state/evidence.
