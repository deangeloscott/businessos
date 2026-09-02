---
id: seo.bootstrap.baseline.authority-baseline
type: workflow
owner_system: seo-aeo
reads:
- Asset
- Observation
writes:
- SEOAssetState
- Asset
- MetricObservation
context:
- Brand
- Business
- Market
- Offer
- ProductService
evidence_inputs:
- backlink/referring-domain/mention evidence and prospect records
- review mention reputation response history
updates:
  SEOAssetState:
  - external_authority
---
# Authority and Reputation Baseline

## Purpose
Establish a useful starting view of the organization’s external references, mentions, reviews, trust sources, and relevant competitive context.

## Business Outcome
Give later authority and reputation work evidence for what external trust/discovery signals exist now, where important gaps or dependencies may be, and how those signals could contribute to visibility, referral attention, and business opportunity.

## Run When
Use when current authority/reputation state is missing, materially stale, or needed for a concrete diagnosis, strategy, comparison, or change evaluation. Scope the baseline to the sources and markets that matter to the business question.

## Process
1. [HYBRID] Gather relevant backlinks/referring domains, unlinked mentions, important third-party profiles, ratings/reviews, press/community references, citations, and other legitimate external evidence available to the host.
2. [AI] Interpret sources by topical and audience relevance, source type, legitimacy, destination, context, market/location, and business usefulness rather than raw count or one synthetic authority metric.
3. [HYBRID] Describe distributions, concentration, quality, source diversity, and meaningful trends when historical evidence exists.
4. [AI] Compare with relevant competitors or market norms only where that comparison changes the decision; competitor external signals are observations/proxies, not access to their actual business outcomes.
5. [AI] Identify material strengths, gaps, risks, or dependencies and the plausible pathway through which they may affect discovery, trust, referral traffic, or other outcomes.
6. [HYBRID] Preserve the baseline evidence and conclusions that future work benefits from. Create an Opportunity only when an unresolved possibility is useful durable memory, not because the baseline found a difference.

## Verification
- Authority/reputation evidence remains source- and context-linked.
- External-link/reputation metrics are not collapsed into a universal authority score.
- Links, mentions, reviews, visibility, referrals, leads, and revenue remain distinct while their plausible causal/business pathways may inform judgment.
- No capability registry, scheduled pipeline, or mandatory routing is required.
