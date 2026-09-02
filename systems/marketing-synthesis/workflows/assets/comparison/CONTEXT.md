---
id: marketing.assets.comparison
type: workflow
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
- Asset
context:
- AudienceSegment
- Brand
- Offer
---
# Comparison & Alternative Persuasion

## Purpose
Help qualified buyers evaluate alternatives honestly using customer decision criteria and current competitive evidence.

## Business Outcome
Increase the likelihood of the desired commercial action through evidence-backed comparison & alternative persuasion that matches audience awareness, Offer, proof, and acquisition context.

## Run When
Use when a comparison/alternative asset is useful to resolve a material buyer decision question. An Opportunity or real durable WorkRequest may provide context but is not required.

## Process
1. [AI] Define comparison audience, stage, alternatives, decision criteria, and the action the asset should support.
2. [HYBRID] Load current canonical Competitor facts and Customer criteria; do not invent weakness claims.
3. [AI] Build fair comparison dimensions including contexts where each alternative may fit better.
4. [HYBRID] Distinguish factual differences, subjective tradeoffs, and our interpretation; timestamp volatile pricing/features.
5. [AI] Present our differentiated value/proof against criteria rather than attacking competitor brand.
6. [HYBRID] Add an appropriate CTA and use relevant Content operating knowledge plus the active harness's real production capabilities directly for final media/document execution. Remember the competitor/source freshness dependency when it is materially useful; persist a WorkRequest only for a real durable organizational handoff.
