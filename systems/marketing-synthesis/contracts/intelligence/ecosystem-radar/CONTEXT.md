---
id: marketing.intelligence.ecosystem-radar
type: playbook
version: 1.0.0
owner_system: marketing-synthesis
reads:
- SourceProfile
- SourceRecord
- Observation
- Insight
- Learning
- Opportunity
- Asset
writes:
- Observation
- Insight
- Opportunity
- WorkRequest
capabilities:
  required:
  - research.web.read
  optional:
  - advertising.observe
  - social.observe
  - community.read
  - marketing.performance.read
  - conversion.read
  - analytics.read
context:
- Business
- Brand
- AudienceSegment
- Market
- Objective
- Offer
- ProductService
subcontracts:
  required:
  - id: core.intelligence.ecosystem.source-discovery
  - id: core.intelligence.ecosystem.evidence-triangulation
  conditional:
  - id: marketing.intelligence.relevance-evaluation
    when: External intelligence must be evaluated for marketing-specific relevance.
  - id: marketing.experimentation.message-test
    when: A promising marketing mechanism is testable and active-business evidence is insufficient.
  - id: marketing.learning.domain-learning
    when: Outcome evidence supports reusable marketing guidance.
---
# Marketing Ecosystem Tactic Radar

## Purpose
Discover and evaluate emerging positioning, messaging, offer-presentation, creative, advertising, funnel, landing-page, email, webinar, VSL, and campaign tactics before they influence marketing work.

## Business Outcome
Improve persuasion faster from credible external learning while avoiding copycat marketing, anecdotal best practices, and tactics that do not fit the active audience/offer/channel.

## Run When
Run from the Core ecosystem radar, on demand for marketing refresh, or when a material new persuasion/channel tactic or measured result appears.

## Process
1. [HYBRID] Reuse current Marketing Learnings, customer/competitor evidence, owned performance, prior experiments, and SourceProfiles before external expansion.
2. [AI] Discover tactic/mechanism claims across practitioners, primary experiments, case studies, research, competitors, communities, platform changes, and adjacent categories using semantic and known-source discovery.
3. [HYBRID] Preserve the underlying evidence and use Core triangulation to separate original measurements, independent replications, repeated case-study retellings, practitioner inference, commercial promotion, and direct counterevidence.
4. [AI] Identify the persuasion mechanism and conditions: audience awareness, segment, offer, proof, channel, creative format, traffic/source context, journey stage, and outcome measured.
5. [HYBRID] Evaluate whether the reported metric is a proxy or meaningful commercial result and whether confounders such as media mix, targeting, offer changes, seasonality, or funnel changes could explain it.
6. [HYBRID] Route weak claims to ignore/watch, evidence gaps to bounded investigation, and promising applicable uncertain tactics to `marketing.experimentation.message-test` with the smallest interpretable treatment.
7. [AI] Use owned outcomes to determine support/contradiction/inconclusive status and avoid generalizing one winning creative or offer across audiences/channels.
8. [DETERMINISTIC] Feed repeatable context-specific outcomes into `marketing.learning.domain-learning`; route customer truths back to Customer Intelligence and operational journey effects to Customer Optimization.

## Verification
- External tactics never bypass active Offer/Brand/customer evidence or authorization.
- Claimed lift is not treated as causal without a design that supports causality.

## Completion Criteria
- Material marketing tactics are ignored, watched, investigated, tested, or learned with explicit evidence and applicability.
