---
id: marketing.assets.comparison
type: playbook
version: 1.2.0
owner_system: marketing-synthesis
artifact_role: customer_facing_production_root
reads:
- Opportunity
- type: Insight
  owner_system: customer-intelligence
- type: Insight
  owner_system: competitor-intelligence
- Asset
- WorkRequest
- ProofRecord
writes:
- WorkRequest
- Asset
capabilities:
  required:
  - none
  optional:
  - creative.text.generate
  - email.send
  - social.ad.publish
  - cms.page.publish
  - experiment.run
  - tracking.read
context:
- AudienceSegment
- Brand
- Offer
---
# Comparison & Alternative Persuasion

## Purpose
Help qualified buyers evaluate alternatives honestly using customer decision criteria and current competitive evidence.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed comparison & alternative persuasion that matches audience awareness, offer, proof, and acquisition context.

## Run When
Run when an Opportunity or WorkRequest requires comparison & alternative persuasion to remove a commercial persuasion gap or create the required conversion asset.

## Process
1. [AI] Define comparison audience, stage, alternatives, decision criteria, and the action the asset should support.
2. [HYBRID] Load current canonical Competitor facts and Customer criteria; do not invent weakness claims.
3. [AI] Build fair comparison dimensions including contexts where each alternative may fit better.
4. [HYBRID] Distinguish factual differences, subjective tradeoffs, and our interpretation; timestamp volatile pricing/features.
5. [AI] Present our differentiated value/proof against criteria rather than attacking competitor brand.
6. [HYBRID] Add appropriate CTA and delegate final content/media production; create refresh dependency on competitor state.
